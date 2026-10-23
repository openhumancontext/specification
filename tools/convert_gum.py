#!/usr/bin/env python3
"""GUM import and export (spec/bindings/GUM.md).

Usage:
    python3 tools/convert_gum.py import <snapshot.sqlite|snapshot.json> --config importer-config.json --out <pkg>
                                 [--previous <pkg>] [--digest-only] [--at T] [--seed S]
    python3 tools/convert_gum.py export <pkg> --grant <grant id> --mode A|B --out <dir> [--at T] [--no-event] [--seed S]
                                 [--holder-key-file FILE]

Import (GUM.md §2):
- one ``import-run`` Event per snapshot; every imported record cites it in ``importedFrom.run``;
- the subject comes from the importer configuration only, never from the data (GUM has no subject column);
- observations become Sources asserted by an observer Party ``s-gum-<n>`` (numbered in order of first
  appearance), content in the vault (``--digest-only``: hash only, no vault object), ``maxRelease: index``,
  ``formulatedAt`` from ``created_at``, no ``capturedAt`` (lost at source);
- propositions become inferred Claims asserted by ``a-gum``, ``facet: other``, text verbatim, ``epistemic:
  hypothesis``, admission proposed; a null confidence stays absent (never 0);
- record ids are ``src-``/``c-`` plus UUIDv5 in the URL namespace over ``<gumInstanceId>:obs:<id>`` and
  ``<gumInstanceId>:<id>``;
- R-X4: a proposition whose text or reasoning speaks of affect, mood, stress, emotion, anxiety or mental condition
  and that rests on a biometric or behavioural observation (screen, keystrokes, voice, ...) is refused: it is not
  imported, and the importer reports how many were refused (never their text);
- R-X3: any other such proposition is quarantined (``special``, ``mental-health``, ``no-infer``, ``person-only``);
  when unsure, it quarantines;
- GUM timestamps are normalised to RFC 3339 UTC; when the stored string differs (SQLite's naive form), the raw
  string is kept in ``ext["gum.import"]`` (``createdAt``/``updatedAt``) so that Mode B returns it verbatim;
- with ``--previous``: a proposition missing from the new snapshot is retracted by ``a-gum`` (Review), unless a new
  proposition in the same ``revision_group`` supersedes it (``inferredLineage: true``). Nothing is deleted.

Export (GUM.md §3) needs a grant with purpose ``gum-export`` to the GUM instance Party. Records are selected by the
evaluation algorithm (SPECIFICATION.md §12.3) under that grant, then by the export filter: only active Claims that are
not declined, retracted, rejected, contested, superseded, special, ``no-infer``/``person-only``/``no-forward``,
frame-relative or interpretation-layer. Mode B writes the ``propositions`` columns of each exported imported Claim from
``ext["gum.import"]`` into an OHC JSON interchange file (GUM.md §4); it does not write into a GUM database, and
observations and the join table are one-way. The sidecar maps GUM ids to OHC ids. An ``export-run`` Event is appended
unless ``--no-event``.

``get_user_context`` is the gumcp-compatible read (MCP.md).
"""

import argparse
import base64
import datetime
import hashlib
import os
import re
import sqlite3
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ohclib import affect, grants, jsonio, model, vocab  # noqa: E402
from ohclib.package import Package, next_numbered_id  # noqa: E402

GUM_SYSTEM = "gum-ai"
GUM_VERSION = "0.1.11"
GUM_PARTY = {"id": "a-gum", "partyKind": "agent", "label": "GUM"}
POLICY_VERSION = "ohc-gum-export/0.1.0-draft"
CONFIDENCE_METHOD = "gum-ai 0.1.11 PROPOSE/REVISE"
DECLARED_ID_BASE = 1000
QUARANTINE = affect.QUARANTINE
NO_RESULTS = "No relevant context found for the given query and time window."
THIRD_PARTY = re.compile(
    r"(?i)\b(colleague|client|customer|partner|friend|wife|husband|spouse|manager|boss|mother|father|son|daughter|"
    r"sister|brother|neighbou?r|girlfriend|boyfriend|coworker|co-worker)s?\b")
HORIZON_DECAY = {"state": 2, "focus": 6, "foundation": 9}
HORIZON_FROM_DECAY = ((1, 4, "state"), (5, 7, "focus"), (8, 10, "foundation"))


# ---------------------------------------------------------------------- input
def load_snapshot(path):
    """A GUM snapshot as {observations, propositions, observation_proposition, ...}."""
    if path.endswith(".json"):
        return jsonio.load_json(path)
    connection = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
    connection.row_factory = sqlite3.Row
    try:
        out = {}
        for table in ("observations", "propositions", "observation_proposition"):
            rows = connection.execute("SELECT * FROM %s ORDER BY rowid" % table).fetchall()
            out[table] = [dict(row) for row in rows]
        return out
    finally:
        connection.close()


def gum_time(value):
    """GUM timestamps as RFC 3339 UTC (``Z``)."""
    if value is None:
        return None
    moment = model.parse_time(str(value).replace(" ", "T") if "T" not in str(value) else value)
    if moment is None:
        moment = datetime.datetime.fromisoformat(str(value)).replace(tzinfo=datetime.timezone.utc)
    return model.format_time(moment)


def observation_id(instance, raw):
    return "src-" + str(uuid.uuid5(uuid.NAMESPACE_URL, "%s:obs:%s" % (instance, raw)))


def proposition_id(instance, raw):
    return "c-" + str(uuid.uuid5(uuid.NAMESPACE_URL, "%s:%s" % (instance, raw)))


def source_kind(observer):
    lowered = (observer or "").lower()
    if "screen" in lowered:
        return "screen-observation"
    if "calendar" in lowered:
        return "calendar"
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-") or "observer"
    return "x-gum:" + slug


def observation_bytes(observation):
    """(bytes, mediaType, extension) of an observation's content."""
    content = observation.get("content") or ""
    if observation.get("content_type") == "input_image":
        data = content if isinstance(content, bytes) else base64.b64decode(content)
        if data[:8] == b"\x89PNG\r\n\x1a\n":
            return data, "image/png", "png"
        return data, "image/jpeg", "jpg"
    return content.encode("utf-8") if isinstance(content, str) else bytes(content), "text/markdown", "md"


def quarantined(proposition):
    return affect.affect_text(proposition.get("text"), proposition.get("reasoning"))


def raw_time(value):
    """The stored GUM timestamp string when it differs from its RFC 3339 normalisation, else None."""
    if value is None:
        return None
    raw = str(value)
    return raw if raw != gum_time(value) else None


# ---------------------------------------------------------------------- import
def run_import(snapshot_path, config, out, previous=None, digest_only=None, at=None, seed=None, horizon=False):
    spec = vocab.Spec()
    snapshot = load_snapshot(snapshot_path)
    subject_id = config.get("subjectId")
    instance = config.get("gumInstanceId")
    if not subject_id or not instance:
        raise SystemExit("importer configuration needs subjectId and gumInstanceId")
    digest_only = config.get("digestOnly", False) if digest_only is None else digest_only
    synthetic = snapshot.get("synthetic") is True or config.get("synthetic") is True
    at = at or gum_time(snapshot.get("snapshotTakenAt")) or model.format_time(
        datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))
    package = Package(out, spec, previous=previous)
    if not package.exists():
        manifest = {
            "format": "ohc.context", "specVersion": "0.1.0-draft",
            "id": config.get("contextId") or subject_id + ":context", "version": at[:10] + ".1",
            "subject": dict({"id": subject_id}, **({"displayName": config["displayName"]}
                                                     if config.get("displayName") else {})),
            "holder": "subject", "created": at,
            "conformance": dict({"level": "L2", "modules": ["core", "governance", "binding.gum"]},
                                **({"subjectIsAdult": True} if config.get("subjectIsAdult") is True else {})),
            "parties": [], "policy": {"admission": "subject-only", "resolver": "returnDialog"},
            "collections": {},
        }
        if synthetic:
            manifest["synthetic"] = True
        package.create(manifest)
    else:
        if (package.manifest.get("subject") or {}).get("id") != subject_id:
            raise SystemExit("the previous package belongs to another subject")
        package.bump_version(at)
    package.ensure_module("binding.gum")
    package.ensure_party(dict(GUM_PARTY))
    package.unretracted = []
    package.refused = 0
    recorded_by = config.get("recordedBy", "subject")
    run = package.next_event_id()
    imported_from = {"importedAt": at, "run": run, "system": GUM_SYSTEM,
                     "systemVersion": str(snapshot.get("gumVersion") or GUM_VERSION)}
    if horizon:
        imported_from["derivedFields"] = ["horizon"]
    existing = package.ids()
    observer_party = {}
    for party in package.manifest.get("parties") or []:
        if re.match(r"^s-gum-\d+$", party.get("id", "")):
            observer_party[party.get("label")] = party["id"]
    new_ids = []
    source_of = {}
    kind_of_observation = {}
    for observation in sorted(snapshot.get("observations") or [], key=lambda o: o["id"]):
        sid = observation_id(instance, observation["id"])
        source_of[observation["id"]] = sid
        observer = observation.get("observer_name") or "observer"
        if observer not in observer_party:
            observer_party[observer] = "s-gum-%d" % (len(observer_party) + 1)
            package.ensure_party({"id": observer_party[observer], "partyKind": "software", "label": observer})
        kind_of_observation[observation["id"]] = source_kind(observer)
        if sid in existing:
            continue
        data, media_type, extension = observation_bytes(observation)
        if digest_only:
            content = {"locator": {"uri": "%s:obs:%s" % (instance, observation["id"])},
                       "mediaType": media_type, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
        else:
            rel, digest = package.store_vault(data, extension)
            content = {"locator": {"vaultPath": rel}, "mediaType": media_type, "sha256": digest, "size": len(data)}
        gum_ext = {"observationId": observation["id"]}
        if observation.get("updated_at") is not None:
            gum_ext["updatedAt"] = gum_time(observation["updated_at"])
        record = {
            "assertedBy": observer_party[observer], "authorship": {"author": observer_party[observer]},
            "content": content, "ext": {"gum.import": gum_ext},
            "id": sid, "importedFrom": dict(imported_from), "kind": "Source", "maxRelease": "index",
            "origin": "observed", "recordedAt": at, "recordedBy": recorded_by, "sourceKind": source_kind(observer),
        }
        if observation.get("created_at") is not None:
            record["formulatedAt"] = gum_time(observation["created_at"])
        if synthetic:
            record["synthetic"] = True
        package.add("Source", dict(sorted(record.items())))
        new_ids.append(sid)
    joins = {}
    for row in snapshot.get("observation_proposition") or []:
        joins.setdefault(row["proposition_id"], []).append(row["observation_id"])
    imported = [r for r in package.records("claims")
                if isinstance((r.get("ext") or {}).get("gum.import"), dict) and r.get("assertedBy") == "a-gum"]
    superseded = set(r.get("supersedes") for r in package.records() if r.get("supersedes"))
    snapshot_ids = set(p["id"] for p in snapshot.get("propositions") or [])
    by_group = {}
    for record in imported:
        gum = record["ext"]["gum.import"]
        if record["id"] not in superseded and gum.get("id") not in snapshot_ids:
            by_group.setdefault(gum.get("revisionGroup"), []).append(record)
    replaced = set()
    claim_ids = []
    for proposition in sorted(snapshot.get("propositions") or [], key=lambda p: p["id"]):
        cid = proposition_id(instance, proposition["id"])
        if cid in existing:
            continue
        joined_kinds = set(kind_of_observation.get(o) for o in joins.get(proposition["id"], []))
        if quarantined(proposition) and joined_kinds.intersection(spec.biometric_kinds):
            package.refused += 1  # R-X4: no affect value from behavioural signals, whatever the label says
            continue
        gum_ext = {"id": proposition["id"]}
        for column, key in (("created_at", "createdAt"), ("updated_at", "updatedAt")):
            if raw_time(proposition.get(column)) is not None:
                gum_ext[key] = raw_time(proposition.get(column))
        if proposition.get("decay") is not None:
            gum_ext["decay"] = proposition["decay"]
        if proposition.get("revision_group") is not None:
            gum_ext["revisionGroup"] = proposition["revision_group"]
        if proposition.get("version") is not None:
            gum_ext["version"] = proposition["version"]
        record = {
            "assertedBy": "a-gum", "epistemic": "hypothesis", "facet": "other",
            "generatedBy": {"software": GUM_SYSTEM, "version": imported_from["systemVersion"]},
            "id": cid, "importedFrom": dict(imported_from), "kind": "Claim", "origin": "inferred",
            "recordedAt": at, "recordedBy": recorded_by, "text": proposition.get("text") or "",
        }
        if proposition.get("confidence") is not None:
            raw = proposition["confidence"]
            record["confidence"] = {"method": CONFIDENCE_METHOD, "raw": raw, "scale": "gum:int-1-10",
                                    "semantics": "support-score", "value": round(raw / 10.0, 10)}
        evidence = [{"kind": "observation", "span": {"selector": {"type": "whole"}, "source": source_of[o]}}
                    for o in joins.get(proposition["id"], []) if o in source_of]
        if evidence:
            record["evidence"] = evidence
        if proposition.get("reasoning"):
            record["rationale"] = proposition["reasoning"]
        if proposition.get("created_at") is not None:
            record["formulatedAt"] = gum_time(proposition["created_at"])
        if proposition.get("updated_at") is not None:
            record["lastEvidenceAt"] = gum_time(proposition["updated_at"])
        if horizon and proposition.get("decay") is not None:
            for low, high, name in HORIZON_FROM_DECAY:
                if low <= proposition["decay"] <= high:
                    record["horizon"] = name
        group = proposition.get("revision_group")
        candidates = [r for r in by_group.get(group, []) if r["id"] not in replaced]
        if group is not None and candidates:
            old = sorted(candidates, key=lambda r: (r.get("recordedAt"), r["id"]))[-1]
            record["supersedes"] = old["id"]
            gum_ext["inferredLineage"] = True
            replaced.add(old["id"])
        record["ext"] = {"gum.import": dict(sorted(gum_ext.items()))}
        categories = []
        if quarantined(proposition):
            categories.append("mental-health")
            record["handling"] = ["no-infer", "person-only"]
            record["sensitivity"] = "special"
        elif THIRD_PARTY.search(record["text"]):
            categories.append("third-party")
        if categories:
            record["categories"] = categories
        if synthetic:
            record["synthetic"] = True
        package.add("Claim", dict(sorted(record.items())))
        claim_ids.append(cid)
    new_ids.extend(claim_ids)
    review_ids = []
    if previous is not None:
        retracted = set()
        for review in package.records("reviews"):
            if review.get("action") == "retract":
                retracted.update(model.review_targets(review))
        grant = gum_grant(package, at)
        for record in sorted(imported, key=lambda r: r["ext"]["gum.import"].get("id")):
            gum = record["ext"]["gum.import"]
            if gum.get("id") in snapshot_ids or record["id"] in replaced or record["id"] in superseded:
                continue
            if record["id"] in retracted:
                continue
            if not grant:
                # A Review by a Party needs underGrant (§11.1); without a grant to the GUM Party in force the
                # retraction is reported, not written.
                package.unretracted.append(record["id"])
                continue
            rid = next_numbered_id(package.ids(), "rv-")
            package.add("Review", {"action": "retract", "by": "a-gum", "id": rid, "kind": "Review", "recordedAt": at,
                                   "target": record["id"], "underGrant": grant})
            review_ids.append(rid)
    new_ids.extend(review_ids)
    package.append_event({"at": at, "eventType": "import-run", "actor": recorded_by, "records": new_ids}, seed=seed)
    package.save(at)
    return package


def gum_grant(package, at):
    """The newest grant to the GUM Party that is in force at ``at`` (cited by its lineage Reviews)."""
    best = None
    moment = model.parse_time(at)
    for grant in package.records("grants"):
        if grant.get("grantee") != "a-gum" or grant.get("effect") == "deny":
            continue
        start = model.parse_time(grant.get("recordedAt"))
        expires = model.parse_time((grant.get("constraints") or {}).get("expiresAt"))
        if start is not None and start <= moment and (expires is None or moment < expires):
            if best is None or start >= model.parse_time(best.get("recordedAt")):
                best = grant
    return best.get("id") if best else None


# ---------------------------------------------------------------------- export
def exportable(state, item, grant, moment):
    data = item.data
    status = state.status.get(item.id)
    if item.kind != "Claim" or status is None:
        return False
    if status.admission != "active" or status.retracted or status.endorsement == "rejected" or status.contested:
        return False
    if state.superseded(item.id):
        return False
    if state.tier(item.id) == "special":
        return False
    if set(state.handling(item.id)).intersection({"no-infer", "person-only", "no-forward"}):
        return False
    if status.epistemic == "frame-relative":
        return False
    if state.spec.layer("Claim") == "interpretation" and grant.get("interpretations") != "all":
        return False
    if data.get("valid") and data["valid"].get("until"):
        until = model.parse_time(data["valid"]["until"])
        if until is not None and until <= moment:
            return False
    return True


def run_export(package_dir, grant_id, mode, out, at=None, no_event=False, seed=None, holder_key=None):
    spec = vocab.Spec()
    ctx = model.Context(package_dir, spec)
    if holder_key is None and ctx.manifest.get("synthetic") is True:
        holder_key = grants.EXAMPLE_HOLDER_KEY
    grants.require_holder_key(ctx, holder_key)
    moment = model.parse_time(at) if at else ctx.latest_time()
    at = model.format_time(moment)
    state = model.State(ctx, moment)
    grant = ctx.record(grant_id)
    if grant is None or ctx.kind_of(grant_id) != "Grant" or "gum-export" not in (grant.get("purposes") or []):
        raise grants.Denied("no-grant")
    if state.grant_status(grant_id, moment) != "given":
        raise grants.Denied("grant-" + str(state.grant_status(grant_id, moment)))
    grantee = grant.get("grantee")
    alias = grants.subject_alias(holder_key, ctx.subject_id, grantee)
    served, _mode = grants.evaluate(state, grant, grantee, "gum-export", moment)
    servable = set(i.id for i in served)
    items = []
    for item in sorted(ctx.content, key=lambda i: (model.parse_time(i.data.get("recordedAt")), i.id)):
        if item.kind != "Claim" or not state.known(item) or item.id not in servable:
            continue
        if exportable(state, item, grant, moment):
            items.append(item)
    sidecar = []
    if mode == "B":
        propositions, declared = [], 0
        for item in items:
            data = item.data
            gum = (data.get("ext") or {}).get("gum.import")
            if isinstance(gum, dict) and data.get("assertedBy") == "a-gum":
                conf = (data.get("confidence") or {}).get("raw")
                row = {"id": gum["id"], "text": data.get("text"), "reasoning": data.get("rationale"),
                       "confidence": conf, "decay": gum.get("decay"),
                       "created_at": gum.get("createdAt") or data.get("formulatedAt"),
                       "updated_at": gum.get("updatedAt") or data.get("lastEvidenceAt"),
                       "revision_group": gum.get("revisionGroup"), "version": gum.get("version")}
            else:
                declared += 1
                created = data.get("formulatedAt") or data.get("recordedAt")
                value = (data.get("confidence") or {}).get("value")
                row = {"id": DECLARED_ID_BASE + declared, "text": data.get("text"),
                       "reasoning": "Declared by subject on %s; origin=%s; ohc:%s" % (created[:10], data.get("origin"), item.id),
                       "confidence": None if value is None else max(1, min(10, int(round(value * 10)))),
                       "decay": ((data.get("ext") or {}).get("gum.import") or {}).get("decay")
                       or HORIZON_DECAY.get(data.get("horizon")),
                       "created_at": created, "updated_at": created,
                       "revision_group": uuid.uuid5(uuid.NAMESPACE_URL, "%s#%s" % (ctx.manifest.get("id"), item.id)).hex,
                       "version": 1}
            propositions.append(row)
            sidecar.append({"exportedAt": at, "gumPropositionId": row["id"], "ohcClaimId": item.id,
                            "policyVersion": POLICY_VERSION})
        document = {"gumVersion": GUM_VERSION, "mode": "B", "exportedAt": at, "grant": grant_id}
        if ctx.manifest.get("synthetic") is True:
            document["synthetic"] = True
        document["propositions"] = propositions
        name = "propositions.json"
    else:
        observations = []
        for index, item in enumerate(items, start=1):
            data = item.data
            created = data.get("formulatedAt") or data.get("recordedAt")
            if data.get("origin") == "declared":
                text = "[ohc] %s states (declared %s): %s" % (alias, created[:10], data.get("text"))
            else:
                text = "[ohc] %s states (origin %s): %s" % (alias, data.get("origin"), data.get("text"))
            observations.append({"id": index, "observer_name": "ohc", "content": text, "content_type": "input_text",
                                 "created_at": created, "updated_at": created})
            sidecar.append({"exportedAt": at, "gumObservationId": index, "ohcClaimId": item.id,
                            "policyVersion": POLICY_VERSION})
        document = {"gumVersion": GUM_VERSION, "mode": "A", "exportedAt": at, "grant": grant_id}
        if ctx.manifest.get("synthetic") is True:
            document["synthetic"] = True
        document["observations"] = observations
        name = "observations.json"
    os.makedirs(out, exist_ok=True)
    jsonio.write_pretty(os.path.join(out, name), document)
    jsonio.write_jsonl(os.path.join(out, "sidecar.jsonl"), sidecar)
    if not no_event:
        package = Package(package_dir, spec)
        package.append_event({"at": at, "eventType": "export-run", "actor": "holder", "counterparty": grantee,
                              "grant": grant_id, "purpose": "gum-export", "records": [i.id for i in items],
                              "outcome": "served"}, seed=seed)
        package.save(at)
    return document, sidecar


def import_back(document, sidecar_lines):
    """OHC → GUM → OHC (GUM.md §4): restore claim id, text, origin and date from the sidecar and reasoning tag."""
    by_gum = dict((line["gumPropositionId"], line["ohcClaimId"]) for line in sidecar_lines if "gumPropositionId" in line)
    restored = []
    tag = re.compile(r"^Declared by subject on (\d{4}-\d{2}-\d{2}); origin=([a-z-]+); ohc:(\S+)$")
    for row in document.get("propositions") or []:
        match = tag.match(row.get("reasoning") or "")
        entry = {"id": by_gum.get(row["id"]), "text": row.get("text"), "created": row.get("created_at")}
        if match:
            entry["origin"] = match.group(2)
            entry["id"] = entry["id"] or match.group(3)
        else:
            entry["origin"] = "inferred"
        restored.append(entry)
    return restored


# ---------------------------------------------------------------------- gumcp
def _tokens(text):
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))


def get_user_context(ctx, caller=None, grant_id=None, query="", start_hh_mm_ago=None, end_hh_mm_ago=None,
                     now=None, holder_key=None):
    """The gumcp-compatible tool (MCP.md). Returns "" without an authenticated caller Party and a given grant, and
    gumcp's no-results sentence when the grant is valid and nothing matches.

    Blocks follow gumcp's layout: the proposition, ``Reasoning``, ``Confidence`` (only when served), ``Relevance
    Score`` and, only when excerpts are served, ``Supporting Observations`` with one ``- [ohc] <excerpt>`` line each.
    Everything printed comes from the records as the grant's mode serves them (§12.3), never from stored fields
    the mode withholds.
    """
    if holder_key is None and ctx.manifest.get("synthetic") is True:
        holder_key = grants.EXAMPLE_HOLDER_KEY
    spec = ctx.spec
    moment = now or ctx.latest_time()
    query = query or ""
    if not caller or caller not in ctx.parties or not grant_id:
        return ""
    grant = ctx.record(grant_id)
    if grant is None or grant.get("grantee") != caller:
        return ""
    purposes = set(grant.get("purposes") or []).intersection({"assist-personal", "gum-export"})
    if not purposes:
        return ""
    state = model.State(ctx, moment)
    if state.grant_status(grant_id, moment) != "given":
        return ""
    purpose = sorted(purposes)[0]
    try:
        served, mode = grants.evaluate(state, grant, caller, purpose, moment)
    except grants.Denied:
        return ""

    def window(text):
        if not text:
            return None
        hours, minutes = text.split(":")
        return moment - datetime.timedelta(hours=int(hours), minutes=int(minutes))

    earliest, latest = window(start_hh_mm_ago), window(end_hh_mm_ago)
    query_tokens = _tokens(query)
    ranked = []
    for item in served:
        if item.kind != "Claim":
            continue
        status = state.status.get(item.id)
        if status is None or status.admission != "active" or status.contested or status.endorsement == "rejected":
            continue
        if state.tier(item.id) == "special" or "person-only" in state.handling(item.id):
            continue
        if state.freshness(item.id, moment) in ("stale", "expired"):
            continue
        if spec.layer("Claim") == "interpretation":
            continue
        recorded = model.parse_time(item.data.get("recordedAt"))
        if earliest is not None and recorded < earliest:
            continue
        if latest is not None and recorded > latest:
            continue
        tokens = _tokens(item.data.get("text"))
        score = (len(query_tokens & tokens) / float(len(query_tokens))) if query_tokens else 0.0
        ranked.append((-score, -(recorded.timestamp() if recorded else 0), item.id, item, score))
    ranked.sort(key=lambda r: r[:3])
    if not ranked:
        return NO_RESULTS
    blocks = []
    for _neg, _rec, _rid, item, score in ranked[:3]:
        record = grants.transform(item, mode)
        lines = ["• %s" % record.get("text")]
        declared = item.data.get("origin") == "declared" and item.data.get("assertedBy") == "subject"
        if record.get("rationale"):
            lines.append("  Reasoning: %s" % record["rationale"])
        elif declared:
            lines.append("  Reasoning: Declared by the person.")
        elif "rationale" in item.data:
            lines.append("  Reasoning: [withheld]")
        else:
            lines.append("  Reasoning: Inferred; reasoning withheld.")
        confidence = record.get("confidence") or {}
        if confidence.get("raw") is not None:
            lines.append("  Confidence: %s" % confidence["raw"])
        elif confidence.get("value") is not None:
            lines.append("  Confidence: %s" % int(round(confidence["value"] * 10)))
        lines.append("  Relevance Score: %.2f" % score)
        if "cite-excerpt" in (grant.get("actions") or []):
            excerpts = []
            for ground in record.get("evidence") or []:
                selector = ((ground or {}).get("span") or {}).get("selector") or {}
                if selector.get("type") == "text-quote" and selector.get("exact"):
                    excerpts.append(selector["exact"])
            if excerpts:
                lines.append("  Supporting Observations:")
                lines.extend("    - [ohc] %s" % excerpt for excerpt in excerpts[:1])
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


# ---------------------------------------------------------------------- CLI
def main(argv=None):
    parser = argparse.ArgumentParser(description="GUM import and export for OHC packages.")
    sub = parser.add_subparsers(dest="command")
    imp = sub.add_parser("import")
    imp.add_argument("snapshot")
    imp.add_argument("--config", required=True)
    imp.add_argument("--out", required=True)
    imp.add_argument("--previous")
    imp.add_argument("--digest-only", action="store_true", default=None)
    imp.add_argument("--at")
    imp.add_argument("--seed")
    imp.add_argument("--horizon-heuristic", action="store_true")
    exp = sub.add_parser("export")
    exp.add_argument("package")
    exp.add_argument("--grant", required=True)
    exp.add_argument("--mode", choices=["A", "B"], required=True)
    exp.add_argument("--out", required=True)
    exp.add_argument("--at")
    exp.add_argument("--no-event", action="store_true")
    exp.add_argument("--seed")
    exp.add_argument("--holder-key-file", help="the holder's key (required unless the context is synthetic)")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    if args.command == "import":
        config = jsonio.load_json(args.config)
        package = run_import(args.snapshot, config, args.out, previous=args.previous, digest_only=args.digest_only,
                             at=args.at, seed=args.seed, horizon=args.horizon_heuristic)
        print("imported into %s" % args.out)
        if package.refused:
            print("refused %d affect proposition(s) resting on behavioural observations (R-X4)" % package.refused)
        for rid in package.unretracted:
            print("not retracted (no grant to the GUM Party in force): %s" % rid)
        return 0
    if args.command == "export":
        key = None
        if args.holder_key_file:
            with open(args.holder_key_file, "rb") as handle:
                key = handle.read().strip()
        try:
            document, sidecar = run_export(args.package, args.grant, args.mode, args.out, at=args.at,
                                           no_event=args.no_event, seed=args.seed, holder_key=key)
        except grants.Denied as denied:
            sys.stderr.write("export refused: %s\n" % denied.code)
            return 1
        except ValueError as error:
            sys.stderr.write("export refused: %s\n" % error)
            return 2
        print("exported %d item(s) to %s" % (len(sidecar), args.out))
        return 0
    parser.print_usage(sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
