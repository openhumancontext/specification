"""Test helpers: a deterministic synthetic base context and a small patch language.

``base_records()`` returns a valid synthetic context about Ilse (fictional), used by the negative fixtures in
``fixtures/negative/`` and by several suites. It is materialised either as a single document (declared L1) or as
a package (declared L2, with an Event chain, one stored projection built by §12.3, and a lock).

A negative fixture is a JSON file::

    {"description": "...", "expect": ["RULE-ID", ...],        # exactly the error rule ids the checker must report
     "form": "single" | "package", "level": "L0" | "L1" | "L2",
     "patches": [...],          # applied to the base before files are written
     "postPatches": [...],      # applied after the Event chain and projections are built (package)
     "lockPatches": [...],      # applied to the lock before it is written (package)
     "finalize": {"chain": true, "digest": true, "lock": true, "projections": "rebuild" | "keep"},
     "raw": {"<relative path>": "<file text>"},          # written before the lock
     "rawAfterLock": {"<relative path>": "<file text>"}, # written after the lock
     "documentFrom": "<repository path>" | "document": {...},  # a standalone document instead of a context
     "registry": {"<kind dir>/<file>": {...} | {"documentFrom": "<repository path>", "patches": [...]}}}
                                # extra registry documents (lenses/, instruments/, playbooks/) for this fixture only

A patch is ``{"op": "set" | "remove" | "add", "target": <collection> | "manifest" | "events" | "lock" |
"projection:<id>", "path": "/@<record id>/field/..." or "/<index>/...", "value": ...}``. ``add`` appends to a
list; ``"path": ""`` appends a record to a collection.
"""

import copy
import hashlib
import json
import os
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from ohclib import events as ev  # noqa: E402
from ohclib import grants, jsonio, model, vocab  # noqa: E402

SEED = b"ohc-test-seed"
VAULT_TEXT = ("Calendar export (synthetic). Tuesday 18:00 Dutch class B1, unit 4. "
              "Thursday 18:00 Dutch class B1, unit 5.\n").encode("utf-8")
VAULT_SHA = hashlib.sha256(VAULT_TEXT).hexdigest()
VAULT_PATH = "vault/%s/%s.txt" % (VAULT_SHA[:2], VAULT_SHA)
FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
_SPEC = None


def spec():
    global _SPEC
    if _SPEC is None:
        _SPEC = vocab.Spec()
    return _SPEC


def repo_root():
    return os.path.dirname(TOOLS)


def base_manifest(form):
    manifest = {
        "format": "ohc.context", "specVersion": "0.1.0-draft", "id": "urn:ohc:example:fixture-ilse:context",
        "version": "2026-10-08.1",
        "subject": {"id": "urn:ohc:example:fixture-ilse", "displayName": "Ilse (fictional)"},
        "holder": "subject", "lang": "en", "created": "2026-09-01T08:00:00Z",
        "conformance": {"level": "L2" if form == "package" else "L1",
                        "modules": ["core", "governance", "lenses", "practices", "patterns", "recall",
                                    "inner-system", "health-ref"], "subjectIsAdult": True},
        "parties": [
            {"id": "a-01", "partyKind": "agent", "label": "Study assistant"},
            {"id": "p-01", "partyKind": "person", "label": "Tutor", "role": "teacher"},
            {"id": "o-01", "partyKind": "organization", "label": "Physiotherapy practice"},
            {"id": "s-01", "partyKind": "software", "label": "Calendar export"},
        ],
        "policy": {"admission": "subject-only", "resolver": "returnDialog"},
        "lenses": [{"id": "urn:ohc:lens:cbt", "version": "0.1.0"}],
        "synthetic": True,
    }
    return manifest


def subj(rec, at):
    rec.update({"origin": "declared", "assertedBy": "subject", "recordedAt": at, "synthetic": True})
    return rec


def base_records():
    """Records by collection name (single-document array names)."""
    t = "2026-09-0%dT08:00:00Z"
    records = {
        "claims": [
            subj({"id": "c-01", "facet": "goal", "text": "Pass the Dutch B1 exam in June 2027.", "horizon": "focus",
                  "valid": {"until": "2027-07-01"}, "contexts": ["learning"]}, t % 2),
            subj({"id": "c-02", "facet": "boundary", "predicate": "time-window",
                  "text": "No study messages after 21:00.", "horizon": "foundation"}, t % 2),
            subj({"id": "c-03", "facet": "preference", "predicate": "format",
                  "text": "Short written exercises, not audio.", "horizon": "focus"}, t % 2),
            subj({"id": "c-04", "facet": "state", "predicate": "availability", "text": "Travelling this week.",
                  "horizon": "state", "valid": {"from": "2026-09-02", "until": "2026-09-09"}}, t % 2),
            {"id": "c-05", "facet": "preference", "predicate": "timing", "text": "Studies best on weekday evenings.",
             "origin": "inferred", "assertedBy": "a-01", "recordedAt": "2026-09-05T10:00:00Z", "underGrant": "g-01",
             "purpose": "learning-support", "epistemic": "hypothesis",
             "confidence": {"value": 0.5, "semantics": "support-score"},
             "evidence": [{"span": {"source": "src-01", "selector": {"type": "whole"}}, "kind": "observation"}],
             "synthetic": True},
            subj({"id": "c-06", "facet": "goal", "text": "Keep evenings free for family.", "horizon": "foundation",
                  "contexts": ["family"]}, t % 2),
        ],
        "sources": [
            subj({"id": "src-01", "sourceKind": "calendar",
                  "content": {"locator": {"vaultPath": VAULT_PATH}, "sha256": VAULT_SHA, "mediaType": "text/plain",
                              "size": len(VAULT_TEXT)},
                  "capturedAt": "2026-09-01T07:00:00Z", "authorship": {"author": "s-01"},
                  "contemporaneity": "contemporaneous", "maxRelease": "summary",
                  "summary": {"text": "Two evening classes per week.", "authoredBy": "subject",
                              "recordedAt": "2026-09-01T08:00:00Z", "method": "subject-written"},
                  "retention": {"eraseOnRequest": True}}, t % 1),
        ],
        "episodes": [
            subj({"id": "ep-01", "occurred": {"start": "2026-09-03", "precision": "day"}, "contexts": ["learning"],
                  "accounts": [{"narrator": "subject", "narratedAt": "2026-09-03T20:00:00Z",
                                "addedAt": "2026-09-03T20:05:00Z", "accountKind": "in-the-moment",
                                "happened": "Skipped the evening class.", "experienced": "Tired.",
                                "evidence": [{"source": "src-01", "selector": {"type": "whole"}}]}],
                  "recall": "permitted"}, "2026-09-03T20:05:00Z"),
            subj({"id": "ep-02", "occurred": {"start": "2026-09-05", "precision": "day"}, "contexts": ["learning"],
                  "accounts": [{"narrator": "subject", "narratedAt": "2026-09-05T20:00:00Z",
                                "addedAt": "2026-09-05T20:05:00Z", "accountKind": "in-the-moment",
                                "happened": "Went to class after a short walk."}],
                  "recall": "permitted"}, "2026-09-05T20:05:00Z"),
        ],
        "interpretations": [
            subj({"id": "in-01", "about": ["ep-01"], "stance": "retrospective",
                  "text": "I skip when I have not eaten before class."}, "2026-09-06T08:00:00Z"),
        ],
        "tensions": [
            subj({"id": "t-01", "between": ["c-01", "c-06"], "tensionKind": "resource-competition",
                  "whoDecides": "subject"}, "2026-09-06T08:10:00Z"),
        ],
        "relations": [
            subj({"id": "r-01", "rel": "practice-for", "from": "pr-01", "to": "c-01"}, "2026-09-06T08:20:00Z"),
        ],
        "practices": [
            subj({"id": "pr-01", "name": "Short walk before class", "practiceKind": "movement",
                  "source": {"route": "self-discovered"}, "initialStatus": "in-use", "nonClinical": True,
                  "contexts": ["learning"]}, "2026-09-06T08:15:00Z"),
        ],
        "outcomes": [
            subj({"id": "oc-01", "about": {"practice": "pr-01"}, "episode": "ep-02", "result": "helped"},
                 "2026-09-06T08:30:00Z"),
        ],
        "patterns": [
            subj({"id": "pat-01", "text": "Class attendance follows whether I moved before it.",
                  "patternKind": "recurring-situation", "episodes": ["ep-01", "ep-02"]}, "2026-09-06T08:40:00Z"),
        ],
        "recallCues": [
            subj({"id": "rc-01", "trigger": {"description": "I say I want to skip class.",
                                             "signals": ["keyword-in-subject-message"]},
                  "offer": {"targets": ["pr-01", "ep-02"], "framing": "A walk helped last time.",
                            "includeAlternatives": True,
                            "alternativesNote": "It may also be plain tiredness or a full week.", "maxTier": "summary"},
                  "timing": {"askBeforeReminding": True, "cooldown": "P1D", "maxPerWeek": 2},
                  "safety": {"nonClinical": True}}, "2026-09-06T08:50:00Z"),
        ],
        "parts": [
            subj({"id": "part-01", "name": "The planner", "authoredWith": "alone"}, "2026-09-06T09:00:00Z"),
        ],
        "healthRefs": [
            subj({"id": "hr-01", "system": "fhir", "fhirVersion": "R5", "resourceType": "CarePlan",
                  "reference": "urn:uuid:0b6f7f3e-2a51-4d0f-9b8e-4f5e6a7b8c9d", "custodian": "o-01",
                  "sensitivity": "special", "categories": ["health"], "audience": "named"},
                 "2026-09-06T09:10:00Z"),
        ],
        "lensAdoptions": [
            subj({"id": "la-01", "lens": {"id": "urn:ohc:lens:cbt", "version": "0.1.0"}, "route": "self-chosen",
                  "uses": ["speak-in-lens"], "agentInterpretation": "off"}, "2026-09-06T09:20:00Z"),
        ],
        "assessments": [],
        "modelViews": [],
        "reviews": [
            {"id": "rv-01", "target": "c-05", "action": "endorse", "by": "subject",
             "recordedAt": "2026-09-05T18:00:00Z"},
        ],
        "proposals": [
            {"id": "prop-01", "proposer": "a-01", "recordedAt": "2026-09-05T10:00:00Z", "underGrant": "g-01",
             "purpose": "learning-support", "items": ["c-05"], "rationale": "Calendar shows evening classes."},
        ],
        "grants": [
            {"id": "g-01", "recordedAt": "2026-09-01T09:00:00Z", "grantor": "subject", "grantee": "a-01",
             "purposes": ["learning-support"],
             "scope": {"include": [{"facets": ["goal", "preference", "boundary"]}, {"kinds": ["Source"]}]},
             "actions": ["read", "suggest", "infer", "source-index"], "mode": "summary", "interpretations": "none",
             "maxSourceTier": "index",
             "constraints": {"expiresAt": "2026-11-30T00:00:00Z", "storage": "session", "forwarding": False,
                             "crossContextUse": False, "delegable": False},
             "basis": {"legal": "explicit-consent"},
             "expressedBy": {"actor": "subject", "at": "2026-09-01T09:00:00Z", "channel": "holder-ui"}},
        ],
    }
    return records


BASE_EVENTS = [
    {"at": "2026-09-01T09:00:00Z", "eventType": "grant-given", "actor": "subject", "counterparty": "a-01",
     "grant": "g-01"},
    {"at": "2026-09-05T10:00:00Z", "eventType": "proposal-received", "actor": "holder", "counterparty": "a-01",
     "grant": "g-01", "purpose": "learning-support", "records": ["c-05"]},
    {"at": "2026-09-05T18:00:00Z", "eventType": "review-written", "actor": "subject", "records": ["c-05"]},
    {"at": "2026-10-08T12:00:00Z", "eventType": "projection-served", "actor": "holder", "counterparty": "a-01",
     "grant": "g-01", "purpose": "learning-support", "records": ["c-01", "c-02", "c-03", "c-05", "c-06", "src-01"],
     "message": "prj-0001", "outcome": "served"},
]
BASE_PROJECTIONS = [{"id": "prj-0001", "grant": "g-01", "purpose": "learning-support",
                     "now": "2026-10-08T12:00:00Z", "select": None}]


# --------------------------------------------------------------------- patches
def _resolve(container, path, create=False):
    parts = [p for p in path.split("/")][1:] if path else []
    node = container
    for part in parts[:-1]:
        node = _step(node, part)
    return node, (parts[-1] if parts else None)


def _step(node, part):
    if isinstance(node, list):
        if part.startswith("@"):
            for item in node:
                if isinstance(item, dict) and item.get("id") == part[1:]:
                    return item
            raise KeyError(part)
        return node[int(part)]
    return node[part.replace("~1", "/").replace("~0", "~")]


def apply_patch(doc, patch):
    op = patch["op"]
    path = patch.get("path", "")
    if op == "add" and path == "":
        doc.append(copy.deepcopy(patch["value"]))
        return
    parent, last = _resolve(doc, path)
    if isinstance(parent, list) and last is not None and last.startswith("@"):
        index = [i for i, x in enumerate(parent) if isinstance(x, dict) and x.get("id") == last[1:]][0]
        last = str(index)
    if op == "set":
        if isinstance(parent, list):
            parent[int(last)] = copy.deepcopy(patch["value"])
        else:
            parent[last] = copy.deepcopy(patch["value"])
    elif op == "remove":
        if isinstance(parent, list):
            del parent[int(last)]
        else:
            del parent[last]
    elif op == "add":
        target = _step(parent, last) if last is not None else parent
        target.append(copy.deepcopy(patch["value"]))
    else:
        raise ValueError(op)


def _target(state, name):
    if name == "manifest":
        return state["manifest"]
    if name == "events":
        return state["events"]
    if name.startswith("projection:"):
        return state["projections"][name.split(":", 1)[1]]
    if name == "lock":
        return state["lock"]
    return state["records"].setdefault(name, [])


def _patch_all(state, patches):
    for patch in patches or []:
        target = _target(state, patch["target"])
        apply_patch(target, patch)


# ----------------------------------------------------------------- materialise
def write_single(dest, state):
    os.makedirs(dest, exist_ok=True)
    manifest = dict(state["manifest"])
    for name, records in state["records"].items():
        if records:
            manifest[name] = records
    jsonio.write_pretty(os.path.join(dest, "context.json"), manifest)
    return dest


def package_files(state):
    sp = spec()
    files = {}
    collections = {}
    for name, records in state["records"].items():
        if not records:
            continue
        kind = sp.collection_kind[name]
        rel = sp.kind_file[kind]
        collections[name] = rel
        files[rel] = records
    collections["events"] = "events.jsonl"
    manifest = dict(state["manifest"])
    collections.update(manifest.get("collections") or {})
    manifest["collections"] = collections
    files["context.json"] = manifest
    files["events.jsonl"] = state["events"]
    for pid, doc in state["projections"].items():
        files["projections/%s.json" % pid] = doc
    return files


def write_files(dest, files):
    for rel, content in files.items():
        full = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(full) or dest, exist_ok=True)
        if isinstance(content, list):
            jsonio.write_jsonl(full, content)
        elif isinstance(content, dict):
            jsonio.write_pretty(full, content)
        elif isinstance(content, bytes):
            with open(full, "wb") as handle:
                handle.write(content)
        else:
            with open(full, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(content)


def compute_lock(dest, manifest):
    files = {}
    for base, dirs, names in os.walk(dest):
        dirs.sort()
        for name in sorted(names):
            rel = os.path.relpath(os.path.join(base, name), dest).replace(os.sep, "/")
            if rel == "context.lock.json" or rel.startswith("vault/") or rel.startswith("ext/"):
                continue
            with open(os.path.join(base, name), "rb") as handle:
                files[rel] = "sha256:" + hashlib.sha256(handle.read()).hexdigest()
    return {"format": "ohc.lock", "specVersion": "0.1.0-draft",
            "context": {"id": manifest["id"], "version": manifest["version"]},
            "algorithm": "sha256", "files": files, "createdAt": "2026-10-08T12:05:00Z"}


def chain(raw_events):
    out = []
    for event in raw_events:
        fields = dict((k, v) for k, v in event.items() if k not in ("id", "seq", "salt", "prev"))
        out.append(ev.next_event(out, fields, seed=SEED))
    return out


def build_state(form):
    return {"manifest": base_manifest(form), "records": base_records(), "events": copy.deepcopy(BASE_EVENTS),
            "projections": {}, "lock": None}


def materialize(dest, form="package", patches=None, post_patches=None, finalize=None, raw=None,
                raw_after_lock=None, lock_patches=None):
    finalize = dict({"chain": True, "digest": True, "lock": True, "projections": "rebuild"}, **(finalize or {}))
    state = build_state(form)
    _patch_all(state, patches)
    os.makedirs(dest, exist_ok=True)
    write_files(dest, {VAULT_PATH: VAULT_TEXT})
    if form == "single":
        _patch_all(state, post_patches)
        write_single(dest, state)
    else:
        if finalize["chain"]:
            state["events"] = chain(state["events"])
        write_files(dest, package_files(state))
        if finalize["projections"] == "rebuild":
            ctx = model.Context(dest, spec())
            for item in BASE_PROJECTIONS:
                if any(e.get("message") == item["id"] for e in state["events"]):
                    try:
                        doc = grants.build_projection(
                            ctx, item["grant"], item["purpose"], model.parse_time(item["now"]), item["id"],
                            select=item["select"], holder_key=grants.EXAMPLE_HOLDER_KEY,
                            nonce=grants.new_nonce(SEED, item["id"]))
                    except grants.Denied:
                        continue
                    state["projections"][item["id"]] = doc
        _patch_all(state, post_patches)
        if finalize["digest"]:
            for doc in state["projections"].values():
                doc["digest"] = grants.projection_digest(doc)
        write_files(dest, package_files(state))
        for rel, text in (raw or {}).items():
            write_files(dest, {rel: text})
        raw = None
        if finalize["lock"]:
            state["lock"] = compute_lock(dest, state["manifest"])
            _patch_all(state, lock_patches)
            write_files(dest, {"context.lock.json": state["lock"]})
    for rel, text in (raw or {}).items():
        write_files(dest, {rel: text})
    for rel, text in (raw_after_lock or {}).items():
        write_files(dest, {rel: text})
    return dest


def run_check(dest, level=None, registry_spec=None):
    import check

    return check.run_context(dest, level=level, spec=registry_spec or spec())


def write_registry(dest, registry):
    """Materialise a fixture's extra registry documents and return a Spec that resolves them (or None)."""
    if not registry:
        return None
    root = os.path.join(dest, "_registry")
    for rel, entry in sorted(registry.items()):
        if isinstance(entry, dict) and "documentFrom" in entry:
            doc = jsonio.load_json(os.path.join(repo_root(), entry["documentFrom"]))
            for patch in entry.get("patches") or []:
                apply_patch(doc, patch)
        else:
            doc = copy.deepcopy(entry)
        full = os.path.join(root, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        jsonio.write_pretty(full, doc)
    return vocab.Spec(registries=[root])


def error_rules(report):
    return sorted(set(e["rule"] for e in report["errors"]))


def load_fixture(path):
    return jsonio.load_json(path)


def materialize_fixture(fixture, dest):
    return materialize(dest, form=fixture.get("form", "single"), patches=fixture.get("patches"),
                       post_patches=fixture.get("postPatches"), finalize=fixture.get("finalize"),
                       raw=fixture.get("raw"), raw_after_lock=fixture.get("rawAfterLock"),
                       lock_patches=fixture.get("lockPatches"))


def run_fixture(fixture, dest):
    """Materialise a negative fixture and return the checker's report (context or document)."""
    import check

    if "documentFrom" in fixture or "document" in fixture:
        if "documentFrom" in fixture:
            doc = jsonio.load_json(os.path.join(repo_root(), fixture["documentFrom"]))
        else:
            doc = copy.deepcopy(fixture["document"])
        state = {"document": doc}
        for patch in fixture.get("patches") or []:
            apply_patch(state["document"], patch)
        os.makedirs(dest, exist_ok=True)
        path = os.path.join(dest, "document.json")
        jsonio.write_pretty(path, state["document"])
        findings, _fmt = check.check_document(path, "document.json", spec())
        return check.report_for_findings(findings)
    registry_spec = write_registry(dest + "-registry", fixture.get("registry"))
    materialize_fixture(fixture, dest)
    return run_check(dest, level=fixture.get("level"), registry_spec=registry_spec)


def dumps(value):
    return json.dumps(value, indent=2, ensure_ascii=False)
