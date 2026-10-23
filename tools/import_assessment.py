#!/usr/bin/env python3
"""Bring a test result into a package as an AssessmentRecord (§10.6; module ``instrument-import``).

Two routes:

1. **Imported result** (INSTRUMENT-IMPORT.md, IMP-1…IMP-5). The person holds a report of an instrument whose entry
   has an ``import`` block. A blank draft is generated from the block (``template``); it is filled from the report
   (by the person, or by their agent from a report the person handed over) or read from a transcript of the score
   page (``Ambition: 88`` per line). ``import_result`` writes one AssessmentRecord per instrument, asserted by the
   scorer Party whose ``uri`` is the block's ``scoredBy.id`` (reused only by ``uri``), recorded by the subject,
   ``origin: imported``, ``formulatedAt`` at the first day of ``administeredAt`` (IMP-5), citing the report as a
   Source of kind ``instrument-report`` in the person's vault (IMP-4). The result stays proposed until the person
   decides on it (R-A1). Blank stays blank (IMA-2): an empty value is left out, never filled.

2. **Scorer output** (the earlier converter route; not an imported result). A scorer the person ran writes JSON::

    {"scorer": {"software", "version", "method"}, "instrument": {"id", "version", "form"},
     "administeredAt": "YYYY-MM-DD", "scoredAt": "...Z", "rawRange": [lo, hi], "normGroup": {...},
     "domains": [{"code", "label", "raw", "percentile"?}], "facets": [{"domain", "code", "label", "raw"}],
     "results": [...]?, "validityFlags": [...]?, "synthetic": true?}

   ``run_import`` writes it with ``origin`` by mode (AR-1).

Both routes refuse, naming the field and never its value: never-fields (AR-3: item text, responses, scoring keys,
report prose); any field outside the accepted list (so report text cannot reach the vault or a record); a mode that
is not an import or not in the catalog; a missing ``administeredAt``; an instrument result without an instrument id;
an instrument the lens does not list (AR-8); a type without the scores it was derived from and its rule (AR-6).
Neither writes use limits: what a grantee may do with a result is the person's grant (R-G14).

Usage:
    python3 tools/import_assessment.py template --instrument ID [--registry DIR]
    python3 tools/import_assessment.py draft --package P (--draft FILE | --transcript FILE --instrument ID)
        [--report FILE] [--at T] [--supersedes ID] [--registry DIR] [--seed S]
    python3 tools/import_assessment.py <results.json> --package P --lens ID [--lens-version V] [--variant ID]
        [--mode M] [--at T] [--adopt] [--scorer-label L] [--source-id ID] [--assessment-id ID] [--adoption-id ID]
        [--seed S]
"""

import argparse
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ohclib import jcs, jsonio, model, vocab  # noqa: E402
from ohclib.package import Package, next_numbered_id  # noqa: E402

TOOL = {"software": "ohc-import-assessment", "version": "0.1.0-draft"}
NEVER_FIELDS = ("items", "itemText", "item_text", "itemResponses", "item_responses", "responses", "answers",
                "scoringKey", "scoring_key", "key", "keys", "reportText", "report_text", "report", "narrative",
                "interpretation", "interpretations", "rawResponses", "raw_responses", "questions")
REFUSED_MODES = ("agent-inference", "cross-lens-estimate")
INSTRUMENT_MODES = ("self-report-instrument", "observer-report", "interview-scored", "vendor-report-import")
STANDARDIZED = ("T", "z", "percentile", "stanine", "sten")

# What the scorer route accepts, per object. Anything else is refused by path (R-026: no report text in the vault).
ACCEPTED = {
    "": ("scorer", "instrument", "administeredAt", "scoredAt", "rawRange", "normGroup", "domains", "facets",
         "results", "validityFlags", "synthetic", "note"),
    "scorer": ("software", "version", "method"),
    "instrument": ("id", "version", "form"),
    "normGroup": ("id", "country", "year", "n", "note"),
    "domains": ("code", "label", "raw", "percentile"),
    "facets": ("domain", "code", "label", "raw", "percentile"),
}
# What a filled draft accepts (route 1).
DRAFT_ACCEPTED = {
    "": ("format", "instrument", "instrumentVersion", "form", "mode", "administeredAt", "normGroup", "scores",
         "synthetic"),
    "scores": ("scale", "label") + ("raw",) + STANDARDIZED,
}
DRAFT_FORMAT = "ohc-import-draft"
MEDIA = {".pdf": "application/pdf", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
         ".txt": "text/plain", ".json": "application/json"}


class Refused(Exception):
    pass


# ------------------------------------------------------------------ shared checks
def find_never_fields(value, path=""):
    found = []
    if isinstance(value, dict):
        for key, inner in value.items():
            here = path + "/" + key
            if key in NEVER_FIELDS:
                found.append(here)
            else:
                found.extend(find_never_fields(inner, here))
    elif isinstance(value, list):
        for index, inner in enumerate(value):
            found.extend(find_never_fields(inner, "%s/%d" % (path, index)))
    return found


def unaccepted_fields(data, accepted):
    """Paths of members outside the accepted list (objects listed in ``accepted``; ``results`` go to the schema)."""
    found = []
    if not isinstance(data, dict):
        return ["/"]
    for key in data:
        if key not in accepted[""]:
            found.append("/" + key)
    for member, keys in accepted.items():
        if not member or member not in data:
            continue
        value = data[member]
        objects = value if isinstance(value, list) else [value]
        for index, obj in enumerate(objects):
            where = "/%s/%d" % (member, index) if isinstance(value, list) else "/" + member
            if not isinstance(obj, dict):
                found.append(where)
                continue
            found.extend(where + "/" + key for key in obj if key not in keys)
    return found


NOTE_MAX = 200  # a scorer's note about its file (one or two sentences), never report prose


def refuse_fields(data, accepted):
    never = find_never_fields(data)
    if never:
        raise Refused("never-fields present (AR-3): " + ", ".join(never))
    other = unaccepted_fields(data, accepted)
    note = data.get("note") if isinstance(data, dict) else None
    if note is not None and not (isinstance(note, str) and len(note) <= NOTE_MAX):
        other.append("/note")
    if other:
        raise Refused("fields outside the accepted list (nothing else is imported): " + ", ".join(other))


def partial_time(text):
    """``YYYY-MM-DD`` (or ``YYYY-MM``, ``YYYY``) as a PartialTime; anything else is refused."""
    if isinstance(text, dict):
        text = text.get("start")
    if not isinstance(text, str) or not re.match(r"^\d{4}(-\d{2}(-\d{2})?)?$", text):
        raise Refused("administeredAt is required as YYYY-MM-DD: the date the test was taken")
    precision = {4: "year", 7: "month", 10: "day"}[len(text)]
    return {"precision": precision, "start": text}


def lens_short(lens_id):
    return lens_id.rsplit(":", 1)[-1]


def score_entry(construct, label, raw=None, raw_range=None, standardized=None):
    """A ``dimension-score`` result: raw (with its range) and a standardized value in ``standardized`` (R-026)."""
    entry = {"construct": construct, "type": "dimension-score"}
    if label:
        entry["label"] = label
    if raw is not None:
        entry["raw"] = raw
        if raw_range:
            entry["rawRange"] = list(raw_range)
    if standardized is not None:
        entry["standardized"] = {"type": standardized[0], "value": standardized[1]}
    return dict(sorted(entry.items()))


def review_after(lens):
    """The lens default ``reviewAfter`` when it is a duration; ``on-change`` is not a record field (R-012)."""
    value = (lens.get("defaults") or {}).get("reviewAfter")
    if isinstance(value, str) and re.match(r"^P(?=[0-9T])", value):
        return value
    return None


def check_types(results, generated_by):
    """AR-6: a type assigned from continuous scores comes with those scores and the rule."""
    types = [r for r in results if r.get("type") == "type-assignment" and r.get("method") in ("instrument", "best-fit")]
    if types and not (any(r.get("type") == "dimension-score" for r in results) and (generated_by or {}).get("method")):
        raise Refused("a type derived from scores needs the scores and the scorer's method (AR-6)")


def trademark_notice(lens, instrument_doc):
    """The notice of the instrument's mark (nominative use), when the lens lists one for it."""
    name = (instrument_doc or {}).get("name") or ""
    for mark in (lens.get("ip") or {}).get("marks") or []:
        if not isinstance(mark, dict) or mark.get("status") == "unverified" or not mark.get("notice"):
            continue
        if mark.get("mark") and mark["mark"].lower() in name.lower():
            return mark["notice"]
    return None


# ------------------------------------------------------------------ route 2: scorer output
def build_results(data, lens_id):
    if isinstance(data.get("results"), list):
        return data["results"]
    short = lens_short(lens_id)
    raw_range = data.get("rawRange")
    out = []
    for domain in data.get("domains") or []:
        pct = domain.get("percentile")
        out.append(score_entry("%s/%s" % (short, domain["code"]), domain.get("label"), domain.get("raw"), raw_range,
                               ("percentile", pct) if pct is not None else None))
    for facet in data.get("facets") or []:
        pct = facet.get("percentile")
        out.append(score_entry("%s/%s/%s" % (short, facet["domain"], facet["code"]), facet.get("label"),
                               facet.get("raw"), raw_range, ("percentile", pct) if pct is not None else None))
    return out


def run_import(results_path, package_dir, lens_id, lens_version=None, variant=None, mode="self-report-instrument",
               at=None, adopt=False, scorer_label="Assessment scorer", source_id=None, assessment_id=None,
               adoption_id=None, seed=None, spec=None):
    """The scorer route: the person ran a scorer; the record is ``derived`` (``declared`` when self-identified)."""
    spec = spec or vocab.Spec()
    with open(results_path, "rb") as handle:
        raw_bytes = handle.read()
    data = jsonio.loads_strict(jsonio.decode_utf8(raw_bytes, results_path), results_path)
    refuse_fields(data, ACCEPTED)
    if mode in REFUSED_MODES:
        raise Refused("mode %s is not an import" % mode)
    if mode not in spec.assessment_modes or mode == "vendor-report-import":
        raise Refused("mode %s is not a scorer mode of the catalog (a vendor report is brought with a draft)" % mode)
    lens = spec.lens(lens_id)
    if lens is None:
        raise Refused("unknown lens %s" % lens_id)
    lens_version = lens_version or lens.get("version")
    instrument = data.get("instrument") or {}
    if mode != "self-identified" and mode != "computed-from-birth-data" and not instrument.get("id"):
        raise Refused("an instrument result needs instrument.id")
    if instrument.get("id") and instrument["id"] not in (lens.get("instruments") or []):
        raise Refused("instrument %s is not listed by the lens (AR-8)" % instrument["id"])
    scorer = data.get("scorer") or {}
    if mode != "self-identified" and not (scorer.get("software") and scorer.get("version")):
        raise Refused("scored results need scorer.software and scorer.version")
    administered = partial_time(data.get("administeredAt"))
    results = build_results(data, lens_id)
    if not results:
        raise Refused("no results")
    generated_by = dict((k, scorer[k]) for k in ("method", "software", "version") if k in scorer)
    check_types(results, generated_by)
    package = Package(package_dir, spec)
    if not package.exists():
        raise Refused("no package at %s" % package_dir)
    origin = (spec.assessment_modes[mode].get("expectedOrigin") or ["derived"])[0]
    synthetic = data.get("synthetic") is True
    at = at or model.format_time(model.parse_time(data.get("scoredAt")))
    package.bump_version(at)
    scorer_party = None
    for party in package.manifest.get("parties") or []:
        if party.get("label") == scorer_label and party.get("partyKind") == "software":
            scorer_party = party["id"]
    if scorer_party is None:
        scorer_party = next_numbered_id(package.party_ids(), "s-")
        package.ensure_party({"id": scorer_party, "partyKind": "software", "label": scorer_label})
    ids = package.ids()
    source_id = source_id or next_numbered_id(ids, "src-")
    assessment_id = assessment_id or next_numbered_id(ids, "as-")
    adoption_id = adoption_id or next_numbered_id(ids, "la-")
    run = package.next_event_id()
    imported_from = {"importedAt": at, "run": run, "system": scorer.get("software", "self-identified"),
                     "systemVersion": str(scorer.get("version", "0"))}
    defaults = lens.get("defaults") or {}
    categories = list(defaults.get("categories") or ["mental-health"])
    vault_path, digest = package.store_vault(raw_bytes, "json")
    source = {"assertedBy": "subject", "authorship": {"author": scorer_party}, "categories": categories,
              "contemporaneity": "contemporaneous",
              "content": {"locator": {"vaultPath": vault_path}, "mediaType": "application/json", "sha256": digest,
                          "size": len(raw_bytes)},
              "id": source_id, "importedFrom": dict(imported_from), "kind": "Source", "maxRelease": "index",
              "origin": "imported", "recordedAt": at, "retention": {"eraseOnRequest": True},
              "sensitivity": "special", "sourceKind": "instrument-report"}
    if data.get("scoredAt"):
        source["capturedAt"] = data["scoredAt"]
        source["formulatedAt"] = data["scoredAt"]
    if synthetic:
        source["synthetic"] = True
    package.add("Source", dict(sorted(source.items())))
    lens_ref = {"id": lens_id, "version": lens_version}
    new_ids = [source_id]
    if adopt:
        adoption = {"agentInterpretation": "off", "assertedBy": "subject", "categories": categories,
                    "derivedFrom": [source_id],
                    "generatedBy": dict(TOOL, method="adopt the lens of the imported instrument"),
                    "id": adoption_id, "importedFrom": dict(imported_from), "interpretationAuthors": ["subject"],
                    "kind": "LensAdoption", "lens": dict(lens_ref), "origin": "derived", "recordedAt": at,
                    "route": "imported", "sensitivity": "special", "uses": ["store-results"]}
        if synthetic:
            adoption["synthetic"] = True
        package.add("LensAdoption", dict(sorted(adoption.items())))
        new_ids.append(adoption_id)
    flags = list(data.get("validityFlags") or [])
    if mode == "self-identified" and "self-identified-only" not in flags:
        flags.append("self-identified-only")
    record = {"administeredAt": administered, "assertedBy": "subject",
              "assessedBy": "subject", "categories": categories, "derivedFrom": [source_id],
              "id": assessment_id, "importedFrom": dict(imported_from), "kind": "AssessmentRecord",
              "lens": dict(lens_ref), "mode": mode, "origin": origin, "recordedAt": at,
              "results": results, "sensitivity": "special", "source": source_id, "validityFlags": flags}
    if generated_by:
        record["generatedBy"] = generated_by
    if instrument:
        record["instrument"] = dict(sorted(instrument.items()))
        notice = trademark_notice(lens, spec.instruments.get(instrument.get("id")))
        if notice:
            record["trademarkNotice"] = notice
    if variant:
        record["lensVariant"] = variant
    if data.get("normGroup"):
        record["normGroup"] = data["normGroup"]
    if data.get("scoredAt"):
        record["formulatedAt"] = data["scoredAt"]
    if review_after(lens):
        record["reviewAfter"] = review_after(lens)
    if synthetic:
        record["synthetic"] = True
    package.add("AssessmentRecord", dict(sorted(record.items())))
    new_ids.append(assessment_id)
    package.ensure_module("lenses")
    package.append_event({"at": at, "eventType": "import-run", "actor": "subject", "records": new_ids}, seed=seed)
    package.save(at)
    return {"source": source_id, "assessment": assessment_id, "adoption": adoption_id if adopt else None}


# ------------------------------------------------------------------ route 1: imported results
def instrument_with_block(spec, instrument_id):
    doc = spec.instruments.get(instrument_id)
    if doc is None:
        raise Refused("unknown instrument %s" % instrument_id)
    block = doc.get("import")
    if not isinstance(block, dict):
        raise Refused("instrument %s has no import block (IMP-2)" % instrument_id)
    lens = spec.lens(doc.get("lens"))
    if lens is None:
        raise Refused("the lens of instrument %s does not resolve" % instrument_id)
    return doc, block, lens


def construct_labels(lens, lang="en"):
    out = {}
    for construct in lens.get("constructs") or []:
        if isinstance(construct, dict) and construct.get("id"):
            label = construct.get("label") or {}
            out[construct["id"]] = label.get(lang) or label.get("en") if isinstance(label, dict) else label
    return out


def template(spec, instrument_id):
    """The blank draft for one instrument, generated from its import block (not a document of the standard)."""
    doc, block, lens = instrument_with_block(spec, instrument_id)
    labels = construct_labels(lens)
    kinds = [s.get("kind") for s in block.get("scores") or []]
    scores = []
    for scale in block.get("scales") or []:
        entry = {"scale": scale, "label": labels.get(scale) or scale.rsplit("/", 1)[-1]}
        entry.update((kind, None) for kind in kinds)
        scores.append(entry)
    return {"format": DRAFT_FORMAT, "instrument": instrument_id, "instrumentVersion": doc.get("version"),
            "form": None, "mode": "self-report-instrument", "administeredAt": None, "normGroup": None,
            "scores": scores}


def _number(text):
    text = text.strip().replace(",", ".")
    if text in ("", "-", "—", "?"):
        return None
    try:
        value = float(text)
    except ValueError:
        raise Refused("not a number")
    return int(value) if value.is_integer() and "." not in text else value


def parse_transcript(spec, instrument_id, text):
    """A draft from a transcript of the score page: one ``<scale>: <value>[ / <value>]`` per line, values in the
    order of the block's ``scores``; ``taken: YYYY-MM-DD``, ``norms: <norm group>``, ``form: <form>``. A scale the
    page does not show is simply absent; a line that names no scale is refused by line number (IMA-2)."""
    draft = template(spec, instrument_id)
    _doc, block, lens = instrument_with_block(spec, instrument_id)
    kinds = [s.get("kind") for s in block.get("scores") or []]
    by_name = {}
    for construct, label in construct_labels(lens).items():
        if construct in (block.get("scales") or []):
            by_name[construct.lower()] = construct
            for other in (lens_label for c in lens.get("constructs") or [] if c.get("id") == construct
                          for lens_label in (c.get("label") or {}).values()):
                by_name[other.lower()] = construct
            by_name[(label or "").lower()] = construct
    groups = dict((g.get("label", {}).get("en", "").lower(), g.get("id")) for g in block.get("normGroups") or [])
    scores = dict((s["scale"], s) for s in draft["scores"])
    unmatched = []
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            unmatched.append(number)
            continue
        name, value = [part.strip() for part in line.split(":", 1)]
        key = name.lower()
        if key in ("taken", "date", "administered", "administeredat"):
            draft["administeredAt"] = value or None
        elif key in ("norms", "norm group", "normgroup"):
            draft["normGroup"] = groups.get(value.lower(), value) or None
        elif key == "form":
            draft["form"] = value or None
        elif key in by_name:
            parts = [p for p in value.split("/")]
            if len(parts) > len(kinds):
                unmatched.append(number)
                continue
            try:
                for kind, part in zip(kinds, parts):
                    scores[by_name[key]][kind] = _number(part)
            except Refused:
                unmatched.append(number)
        else:
            unmatched.append(number)
    if unmatched:
        raise Refused("transcript lines that name no scale of the instrument or carry no number: %s" %
                      ", ".join(str(n) for n in unmatched))
    return draft


def norm_group_labels(block):
    return [(g.get("label") or {}).get("en") or g.get("id") for g in block.get("normGroups") or []]


def norm_group_id(block, value):
    """A norm group as the report prints it (its label, in any language) or by id: the id (IMA-2: copy what the
    report shows)."""
    if not isinstance(value, str):
        return value
    for group in block.get("normGroups") or []:
        labels = [l.lower() for l in (group.get("label") or {}).values() if isinstance(l, str)]
        if value.strip().lower() in labels:
            return group.get("id")
    return value


def check_draft(spec, draft):
    """Validate a filled draft against the import block; return (instrument doc, lens, results, record fields)."""
    refuse_fields(draft, DRAFT_ACCEPTED)
    if draft.get("format") not in (None, DRAFT_FORMAT):
        raise Refused("not an import draft")
    doc, block, lens = instrument_with_block(spec, draft.get("instrument"))
    if draft.get("instrumentVersion") != doc.get("version"):
        raise Refused("the draft was made for instrument version %s; the entry is %s: make a new draft (W-IMP2)" %
                      (draft.get("instrumentVersion"), doc.get("version")))
    mode = draft.get("mode") or "self-report-instrument"
    if mode not in INSTRUMENT_MODES or mode not in spec.assessment_modes:
        raise Refused("mode %s is not an instrument import" % mode)
    administered = partial_time(draft.get("administeredAt"))
    kinds = dict((s.get("kind"), s) for s in block.get("scores") or [])
    scales = list(block.get("scales") or [])
    seen = set()
    results = []
    for index, entry in enumerate(draft.get("scores") or []):
        scale = entry.get("scale")
        if scale not in scales or scale in seen:
            raise Refused("/scores/%d: not a scale of the import block, or listed twice (IMP-2)" % index)
        seen.add(scale)
        raw, standardized = None, None
        for kind, score in kinds.items():
            value = entry.get(kind)
            if value is None or value == "":
                continue  # blank stays blank (IMA-2)
            rng = score.get("range") or [None, None]
            ok = isinstance(value, (int, float)) and not isinstance(value, bool) and rng[0] <= value <= rng[1]
            if ok and score.get("integer") and not float(value).is_integer():
                ok = False
            if not ok:
                raise Refused("/scores/%d/%s: outside the range or kind of the import block (IMP-2)" % (index, kind))
            if kind == "raw":
                raw = value
            else:
                standardized = (kind, int(value) if score.get("integer") else value)
        for kind in STANDARDIZED + ("raw",):
            if entry.get(kind) not in (None, "") and kind not in kinds:
                raise Refused("/scores/%d/%s: a kind the import block does not list (IMP-2)" % (index, kind))
        if raw is None and standardized is None:
            continue
        results.append(score_entry(scale, entry.get("label"), raw, None, standardized))
    if not results:
        raise Refused("no values in the draft: nothing to bring")
    fields = {"administeredAt": administered, "mode": mode}
    norm = norm_group_id(block, draft.get("normGroup"))
    if norm not in (None, ""):
        if norm not in [g.get("id") for g in block.get("normGroups") or []]:
            raise Refused("the norm group \"%s\" is not one of: %s (IMP-2)" % (
                norm, "; ".join(norm_group_labels(block)) or "none listed"))
        fields["normGroup"] = {"id": norm}
    if draft.get("form"):
        fields["form"] = str(draft["form"])
    return doc, block, lens, results, fields


def result_categories(lens, constructs):
    """Lens default categories plus the per-construct categories of the scales present (§8.3, C3)."""
    defaults = lens.get("defaults") or {}
    cats = set(defaults.get("categories") or [])
    for construct in constructs:
        cats.update(((defaults.get("perConstruct") or {}).get(construct) or {}).get("categories") or [])
    return sorted(cats)


def current_imported(package):
    """Imported results that are not superseded, declined or retracted (W-IMP6)."""
    records = [r for r in package.records("assessments") if model.is_imported_result("AssessmentRecord", r)]
    superseded = set(r.get("supersedes") for r in records if r.get("supersedes"))
    gone = set()
    for review in package.records("reviews"):
        if review.get("action") in ("decline", "retract", "reject") and review.get("by") == "subject":
            gone.add(review.get("target"))
    return [r for r in records if r.get("id") not in superseded and r.get("id") not in gone]


def scorer_party(package, block):
    """The scorer Party, reused only when its ``uri`` equals the block's ``scoredBy.id`` (IMP-3)."""
    scorer = block.get("scoredBy") or {}
    for party in package.manifest.get("parties") or []:
        if party.get("uri") == scorer.get("id") and party.get("partyKind") == "organization":
            return party["id"]
    pid = next_numbered_id(package.party_ids(), "o-")
    package.ensure_party({"id": pid, "partyKind": "organization", "label": scorer.get("label") or "Report scorer",
                          "uri": scorer.get("id")})
    return pid


def import_result(package_dir, drafts, at, report_path=None, supersedes=None, seed=None, spec=None, pin=True,
                  synthetic=False, opaque=False):
    """Write one imported result per draft (one per instrument), all citing the person's report when given.

    Returns ``{"assessments": [ids], "source": id or None, "parties": [ids], "pinned": [rel paths]}``. Refuses a
    draft that repeats a current imported result (W-IMP6) unless it ``supersedes`` that result (a correction, R-V2).
    """
    spec = spec or vocab.Spec()
    if isinstance(drafts, dict):
        drafts = [drafts]
    if not drafts:
        raise Refused("no draft")
    if supersedes and len(drafts) != 1:
        raise Refused("a correction supersedes one result with one draft")
    checked = [check_draft(spec, draft) for draft in drafts]
    if len(set(c[0]["id"] for c in checked)) != len(checked):
        raise Refused("one draft per instrument")
    package = Package(package_dir, spec)
    if not package.exists():
        raise Refused("no package at %s" % package_dir)
    if opaque:  # the person's window: opaque record ids (Annex B, "No existence oracles")
        package.opaque, package.seed = True, seed if synthetic else None
    moment = model.parse_time(at)
    current = current_imported(package)
    prior = None
    if supersedes:
        prior = package.record(supersedes)
        if prior is None or not model.is_imported_result("AssessmentRecord", prior) or \
                (prior.get("instrument") or {}).get("id") != checked[0][0]["id"]:
            raise Refused("%s is not an imported result of this instrument" % supersedes)
    for doc, _block, _lens, results, fields in checked:
        day = model.administered_day(fields)
        if day is None or day > moment:
            raise Refused("administeredAt is later than the time of recording (IMP-5)")
        for record in current:
            if record.get("id") != supersedes and (record.get("instrument") or {}).get("id") == doc["id"] and \
                    record.get("administeredAt") == fields["administeredAt"] and \
                    jcs.canonicalize(record.get("results")) == jcs.canonicalize(results):
                raise Refused("this result is already in the context as %s (W-IMP6)" % record.get("id"))
    package.bump_version(at)
    run = package.next_event_id()
    new_ids, parties, pinned = [], [], []
    all_categories = set()
    for _doc, _block, lens, results, _fields in checked:
        all_categories.update(result_categories(lens, [r["construct"] for r in results]))
    source_id = None
    if report_path:
        with open(report_path, "rb") as handle:
            report = handle.read()
        extension = os.path.splitext(report_path)[1].lower()
        vault_path, digest = package.store_vault(report, extension.lstrip(".") or "bin")
        scorers = set((c[1].get("scoredBy") or {}).get("id") for c in checked)
        if len(scorers) != 1:
            raise Refused("one report per scorer: bring each report with its own drafts")
        source_id = package.new_id("src-")
        author = scorer_party(package, checked[0][1])
        source = {"assertedBy": "subject", "categories": sorted(all_categories), "contemporaneity": "retrospective",
                  "content": {"locator": {"vaultPath": vault_path}, "mediaType": MEDIA.get(extension,
                                                                                         "application/octet-stream"),
                              "sha256": digest, "size": len(report)},
                  "id": source_id, "kind": "Source", "maxRelease": "index", "origin": "declared",
                  "recordedAt": at, "retention": {"eraseOnRequest": True}, "sensitivity": "special",
                  "sourceKind": "instrument-report", "authorship": {"author": author}}
        if synthetic:
            source["synthetic"] = True
        package.add("Source", dict(sorted(source.items())))
        new_ids.append(source_id)
    for doc, block, lens, results, fields in checked:
        party = scorer_party(package, block)
        parties.append(party)
        assessment_id = package.new_id("as-")
        day = model.administered_day(fields)
        instrument = {"id": doc["id"]}
        if fields.get("form"):
            instrument["form"] = fields["form"]
        record = {"administeredAt": fields["administeredAt"], "assertedBy": party, "assessedBy": "subject",
                  "categories": result_categories(lens, [r["construct"] for r in results]),
                  "formulatedAt": model.format_time(day), "id": assessment_id,
                  "importedFrom": {"importedAt": at, "run": run, "system": doc["id"],
                                   "systemVersion": doc.get("version")},
                  "instrument": instrument, "kind": "AssessmentRecord",
                  "lens": {"id": lens["id"], "version": lens.get("version")}, "mode": fields["mode"],
                  "origin": "imported", "recordedAt": at, "recordedBy": "subject", "results": results,
                  "sensitivity": "special", "validityFlags": []}
        if doc.get("scoring") == "proprietary":
            record["validityFlags"].append("vendor-algorithm-undisclosed")
        if fields.get("normGroup"):
            record["normGroup"] = fields["normGroup"]
        if source_id:
            record["source"] = source_id
        notice = trademark_notice(lens, doc)
        if notice:
            record["trademarkNotice"] = notice
        if review_after(lens):
            record["reviewAfter"] = review_after(lens)
        if prior is not None:
            if prior.get("assertedBy") != party:
                raise Refused("a correction keeps the scorer of the result it corrects (R-V2)")
            record["supersedes"] = prior["id"]
        if synthetic:
            record["synthetic"] = True
        package.add("AssessmentRecord", dict(sorted(record.items())))
        new_ids.append(assessment_id)
        if pin:
            pinned.extend(pin_lens(package, spec, lens))
    package.ensure_module("lenses")
    package.ensure_module("instrument-import")
    package.append_event({"at": at, "eventType": "import-run", "actor": "subject", "records": new_ids}, seed=seed)
    package.save(at)
    return {"assessments": [i for i in new_ids if i.startswith("as-")], "source": source_id,
            "parties": sorted(set(parties)), "pinned": pinned}


def pin_lens(package, spec, lens):
    """Pin the lens descriptor and the playbooks it lists that resolve, so the agent rendering is a pure function
    of pinned documents (CONTEXT-03; LENSES.md §2.2)."""
    out = []
    pins = [(p.get("id"), p.get("version")) for p in package.manifest.get("lenses") or [] if isinstance(p, dict)]
    if (lens["id"], lens.get("version")) not in pins:
        out.append(package.pin("lenses", lens))
    have = [(p.get("id"), p.get("version")) for p in package.manifest.get("playbooks") or [] if isinstance(p, dict)]
    for playbook_id in lens.get("playbooks") or []:
        doc = spec.playbook(playbook_id)
        if doc is not None and (doc["id"], doc.get("version")) not in have:
            out.append(package.pin("playbooks", doc))
    return out


def load_drafts(path):
    data = jsonio.load_json(path)
    return data if isinstance(data, list) else [data]


# ------------------------------------------------------------------ command line
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        if argv[:1] == ["template"]:
            parser = argparse.ArgumentParser(prog="import_assessment.py template")
            parser.add_argument("--instrument", required=True)
            parser.add_argument("--registry", action="append")
            args = parser.parse_args(argv[1:])
            sys.stdout.write(jsonio.dumps_pretty(template(vocab.Spec(registries=args.registry), args.instrument)))
            return 0
        if argv[:1] == ["draft"]:
            parser = argparse.ArgumentParser(prog="import_assessment.py draft")
            parser.add_argument("--package", required=True)
            parser.add_argument("--draft")
            parser.add_argument("--transcript")
            parser.add_argument("--instrument")
            parser.add_argument("--report")
            parser.add_argument("--at")
            parser.add_argument("--supersedes")
            parser.add_argument("--registry", action="append")
            parser.add_argument("--seed")
            args = parser.parse_args(argv[1:])
            spec = vocab.Spec(registries=args.registry)
            if args.transcript:
                if not args.instrument:
                    raise Refused("--transcript needs --instrument")
                with open(args.transcript, "r", encoding="utf-8") as handle:
                    drafts = [parse_transcript(spec, args.instrument, handle.read())]
            elif args.draft:
                drafts = load_drafts(args.draft)
            else:
                raise Refused("give --draft or --transcript")
            at = args.at or model.format_time(datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))
            result = import_result(args.package, drafts, at, report_path=args.report, supersedes=args.supersedes,
                                   seed=args.seed, spec=spec)
            print(json.dumps(result))
            return 0
        parser = argparse.ArgumentParser(description="Import a scorer's output as an AssessmentRecord.")
        parser.add_argument("results")
        parser.add_argument("--package", required=True)
        parser.add_argument("--lens", required=True)
        parser.add_argument("--lens-version")
        parser.add_argument("--variant")
        parser.add_argument("--mode", default="self-report-instrument")
        parser.add_argument("--at")
        parser.add_argument("--adopt", action="store_true")
        parser.add_argument("--scorer-label", default="Assessment scorer")
        parser.add_argument("--source-id")
        parser.add_argument("--assessment-id")
        parser.add_argument("--adoption-id")
        parser.add_argument("--seed")
        args = parser.parse_args(argv)
        result = run_import(args.results, args.package, args.lens, lens_version=args.lens_version,
                            variant=args.variant, mode=args.mode, at=args.at, adopt=args.adopt,
                            scorer_label=args.scorer_label, source_id=args.source_id,
                            assessment_id=args.assessment_id, adoption_id=args.adoption_id, seed=args.seed)
    except SystemExit:
        return 2
    except Refused as refused:
        sys.stderr.write("refused: %s\n" % refused)
        return 1
    except jsonio.JsonError as error:
        sys.stderr.write("refused: %s at %s\n" % (error.rule, error.path))
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
