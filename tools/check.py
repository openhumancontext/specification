#!/usr/bin/env python3
"""Open Human Context reference checker.

Usage:
    python3 tools/check.py <file-or-dir> [--level L0|L1|L2] [--json] [--strict] [--registry DIR]
    python3 tools/check.py --self-test
    python3 tools/check.py --release [<repo-root>]
    python3 tools/check.py --gen-enums

The checker is read-only (``--gen-enums`` is the one generator: it rewrites the
vocabulary ``$defs`` of ``spec/schema/common.schema.json`` from the catalogs). It
never follows external locators, never reads vault content (it only hashes
present vault files) and never prints field values: every finding is
``{rule, id, path}`` plus the rule's own text (``message``), where it is defined (``see``) and, for schema
findings, the failing keyword and schema property name (``detail``) - never a value (SPECIFICATION.md §5.1).

Exit codes: 0 valid, 1 invalid, 2 usage error.
"""

import argparse
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ohclib import affect  # noqa: E402
from ohclib import ode  # noqa: E402
from ohclib import events as ev  # noqa: E402
from ohclib import grants, jcs, jsonio, model, vocab  # noqa: E402

LEVELS = ("L0", "L1", "L2")

# --------------------------------------------------------------------------- rules
# Every rule id the specification cites, with how the checker treats it.
#   level: the lowest conformance level at which a violation is an error.
#   how:   "check" (machine-checked here), "warning" (heuristic warning),
#          "schema" (enforced by the JSON Schemas, reported as S-2/S-3),
#          "computed" (applied when computing status, tiers or projections),
#          "alias:<id>" (reported under another id),
#          "normative" (normative only; not machine-checkable from files).
RULES = {}


def _rules(level, how, ids):
    for rule in ids.split():
        RULES[rule] = (level, how)


_rules("L0", "check", "J-1 J-2 J-3 J-4 J-5 J-6 S-1 S-2 S-3 S-5 CX-1 CX-2 CX-3 CX-5 CX-6 CX-7 CX-8 R-C4")
_rules("L0", "check", "SJ-1 SJ-2 SJ-3 PA-1 PA-2 ID-1 ID-2 ID-3 CL-1 CL-2 CL-3 CL-4 CL-6 CL-7 CL-8 CL-9 ENV-2 ENV-3")
_rules("L0", "check", "ENV-5 X-1 X-2 X-3 LV-0 TP-2 P-1")
_rules("L0", "alias:CL-2", "R-B1")
_rules("L0", "alias:CL-4", "R-X4")
_rules("L0", "warning", "W-ID1 W-CL5 PA-3 W-CL4")
_rules("L0", "alias:ID-1", "CX-4")
_rules("L0", "alias:X-1", "ENV-6")
_rules("L0", "alias:S-3", "ENV-1 EP-4 LA-2 PC-3 PC-4 MV-2 P-4 EV-3 AR-3 TB-1 HR-1")
_rules("L0", "alias:CL-6", "TP-1")
_rules("L0", "alias:W-CL5", "CL-5")
_rules("L0", "alias:S-1", "R-V0")
_rules("L0", "alias:S-5", "R-M1 PT-4")
_rules("L0", "alias:RL-3", "P-5")
_rules("L1", "check", "ENV-4 G4 INF-1 RA-1 RL-1 RL-2 RL-3 RL-4 SR-1 SR-2 SR-3 SR-5 SR-6 SR-7 RF-1")
_rules("L1", "check", "EP-1 EP-2 EP-3 EP-6 I1 I2 I4 I5 I6 I7 I8 I10 T1 T2 T4 RV-1 RV-2 RV-4 RV-5")
_rules("L1", "check", "PR-1 PR-2 PR-4 GR-1 GR-2 GR-3 GR-4 GR-5 GR-6 GR-7 GR-8 GR-9 LA-1 LA-3 LA-6")
_rules("L1", "check", "AR-1 AR-2 AR-4 AR-6 AR-7 AR-8 MV-1 MV-3 PC-1 PC-2 O-1 O-3 PT-1 PT-2 PT-3")
_rules("L1", "check", "RC-1 RC-2 RC-6 RC-7 P-2 HR-2 HR-4 LV-1 TB-3 TB-5")
_rules("L1", "warning", "W-SR1 TP-3 EP-5 SR-4 RC-4 W-LA6 W-HO1")
_rules("L1", "alias:RA-1", "R-A1")
_rules("L1", "alias:ENV-4", "R-V2")
_rules("L1", "alias:ENV-3", "R-T5b")
_rules("L1", "alias:EV-5", "SU-2 SU-3")
_rules("L1", "alias:T1", "RV-6")
_rules("L1", "alias:EP-2", "R-E1")
_rules("L1", "normative", "I3")
_rules("L1", "computed", "I9 T3 RV-3 PR-3 LA-4 LA-5 AR-5 MV-4 O-2 RC-3 P-3 EP-7 TB-2 R-O1 R-O3 R-T3")
_rules("L2", "check", "LV-2 LK-1 LK-2 LK-3 EV-1 EV-2 EV-4 EV-5 EV-6 EV-7 PJ-1 PJ-2 PJ-3 PJ-4 PJ-5 PJ-6 PJ-7 TB-4")
_rules("L2", "check", "RL-5 HR-3 V-6")
_rules("L2", "alias:EV-7", "R-G1 H-1")
_rules("L0", "check", "LN-1 LN-3 LN-4 LN-5 LN-6 LN-7 LN-8 LN-9 LN-11 LN-13 M-1 M-2 M-3 M-6")
# Playbooks (LENSES.md §2.2) and instrument import (INSTRUMENT-IMPORT.md).
_rules("L0", "check", "PB-1 PB-2 INS-1 IMP-1")
_rules("L1", "check", "PB-3 IMP-2 IMP-3 IMP-4 IMP-5")
_rules("L0", "warning", "W-PB5")
_rules("L1", "warning", "W-IMP2 W-IMP6")
_rules("L0", "normative", "PB-4 PB-5 IMA-1 IMA-2 IMH-1")
_rules("L2", "computed", "PJ-8")
_rules("L0", "normative", "M-4 M-5 M-7 M-8")
_rules("L0", "check", "S-4 SELF-1 SELF-2 SELF-3 SELF-4")
_rules("L0", "check", "REL-1 REL-2 REL-3 REL-4 REL-5 REL-6 REL-7")
_rules("L0", "check", "OB-1 OB-2 OB-3 OB-4")
_rules("L0", "warning", "W-OB1")
_rules("L0", "alias:EP-1", "G1")
_rules("L0", "schema", "G2 G3 R-N1")
_rules("L0", "normative", "R-S1 R-S2 R-S3 R-S4 R-S5 R-C1 R-C2 R-C3 R-I1 R-P2 R-O2 R-N2 R-T2 R-T4 R-T5")
_rules("L0", "normative", "R-T6 R-V1 R-X3 R-L0 C3 ST-1")
_rules("L0", "normative", " ".join("R-G%d" % n for n in range(2, 15)))
_rules("L0", "normative", " ".join("C-%d" % n for n in range(1, 13)))
_rules("L0", "normative", " ".join("H-%d" % n for n in range(2, 18)))
_rules("L0", "normative", "V-0 V-1 V-2 V-3 V-4 V-5 SU-1 SU-4 SU-5 SU-6 SU-7 RC-5")
_rules("L0", "normative", " ".join("IB-%d" % n for n in range(1, 7)))
# Rules the specification states as computed or normative, with the check that realises them:
ALIASES_EXPLAINED = {
    "ENV-6": "X-1", "CX-4": "ID-1", "TP-1": "CL-6, TP-2, RF-1", "RV-6": "T1", "R-E1": "EP-2", "P-5": "RL-3",
    "R-M1": "S-5", "PT-4": "S-5", "CL-5": "W-CL5", "R-V0": "S-1", "G1": "EP-1, SR-6, I6", "R-B1": "CL-2",
    "R-A1": "RA-1", "R-V2": "ENV-4", "R-T5b": "ENV-3", "R-X4": "CL-4", "R-N1": "S-3", "R-G1": "EV-7, PJ-2",
    "H-1": "EV-7", "SU-2": "EV-5", "SU-3": "EV-5",
}
# Tokens that look like rule ids in the specification text but are not rules.
NOT_RULES = {"UTF-8", "T5"}

DEFAULTS_ORDER = ("conformance.level", "sensitivity", "admission", "endorsement", "epistemic")
REPORT_FLAGS = {
    "truthVerified": False, "consentVerified": False, "consentAuthenticated": False,
    "endorsementAuthenticated": False, "behaviorTested": False, "runtimeTested": False,
    "vaultContentRead": False, "externalLocatorsFollowed": 0, "realPersonData": "not-detectable-by-check",
}
NON_PSYCH_ALTERNATIVES = ("situational", "physiological", "informational", "external")
PERSONAL_NAME_DENY = (
    "Alice", "Bob", "Charlie", "John", "Jane", "Smith", "Johnson", "Michael", "David", "Sarah", "Emily",
    "Jennifer", "Robert", "William", "Muhammad", "Mohammed", "Maria", "Ivan", "Ivanov", "Olga", "Natalia",
    "Dmitry", "Sergey", "Elena", "Svetlana", "Tatiana", "Petrov", "Smirnov", "Mueller", "Garcia", "Rodriguez",
)
INNER_STATE_WORDS = ("felt", "feels", "angry", "anxious", "afraid", "ashamed", "jealous", "depressed",
                     "thinks that", "believes that", "was upset", "wanted to")
NON_PSYCH_WORDS = ("tired", "fatigue", "sleep", "load", "busy", "full week", "workload", "health", "ill",
                   "sick", "circumstance", "time", "schedule", "deadline", "weather", "travel", "money",
                   "information", "external", "situation", "situational", "physical", "hungry", "noise")


class Findings(object):
    def __init__(self):
        self.items = []

    def add(self, rule, rid, path, level=None, detail=None):
        lvl, how = RULES.get(rule, ("L0", "check"))
        severity = "warning" if how == "warning" else "error"
        finding = {"rule": rule, "id": rid, "path": path, "level": level or lvl, "severity": severity}
        if detail:
            finding["detail"] = detail
        self.items.append(finding)

    def rules_for(self, rid):
        return set(f["rule"] for f in self.items if f["id"] == rid)


# ------------------------------------------------------------------ rule texts
# A finding carries the rule's own sentence from the specification and where it is defined, so that a writer can
# fix it without searching. Only specification text is printed, never a value from the checked file.
_RULE_TEXT = None
_RULE_DEF = re.compile(r"^- \*\*([A-Z][A-Za-z0-9-]*)(?: \(([A-Z][A-Za-z0-9-]*)\))?\.\*\*\s+(.*)$")
_HEADING = re.compile(r"^#{2,4}\s+(Annex [A-Z]|[A-Z]\.\d+|\d+(?:\.\d+)*)\.?\s")
RULE_DOCS = ("spec/SPECIFICATION.md", "spec/EXCHANGE.md", "spec/LENSES.md", "spec/INSTRUMENT-IMPORT.md",
             "spec/bindings/ODE.md")


def _first_sentence(text):
    text = re.sub(r"\s+", " ", text).strip()
    match = re.search(r"(?<![A-Z][a-z])(?<!e\.g)(?<!i\.e)(?<!\bvs)\.(?:\s|$)", text)
    sentence = text[:match.start() + 1] if match else text
    return sentence if len(sentence) <= 300 else sentence[:297].rstrip() + "..."


def rule_texts():
    """{rule id: (first sentence, "file §section")} from the rule definitions in the specification documents."""
    global _RULE_TEXT
    if _RULE_TEXT is not None:
        return _RULE_TEXT
    _RULE_TEXT = {}
    root = vocab.default_root()
    for rel in RULE_DOCS:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as handle:
            lines = handle.read().split("\n")
        section = ""
        index = 0
        while index < len(lines):
            line = lines[index]
            heading = _HEADING.match(line)
            if heading:
                section = heading.group(1)
            match = _RULE_DEF.match(line)
            if match and match.group(1) not in _RULE_TEXT:
                text = [match.group(3)]
                cursor = index + 1
                while cursor < len(lines) and lines[cursor].startswith("  ") and lines[cursor].strip():
                    text.append(lines[cursor].strip())
                    cursor += 1
                where = "%s §%s" % (rel, section) if section else rel
                entry = (_first_sentence(" ".join(text)), where)
                _RULE_TEXT[match.group(1)] = entry
                if match.group(2):  # "**EP-2 (R-E1).**": the second id is the same rule's other name
                    _RULE_TEXT.setdefault(match.group(2), entry)
            index += 1
    return _RULE_TEXT


def undefined_rules():
    """SELF-4: every rule id in RULES is defined (``- **ID.**``) in a specification document, so that every finding
    can carry its rule's sentence and a place to look."""
    texts = rule_texts()
    return sorted(rule for rule in RULES if rule not in texts)


def explain(rule):
    """(message, see) for a rule id, following aliases to the rule that defines the text."""
    texts = rule_texts()
    if rule in texts:
        return texts[rule]
    return ("", "spec/SPECIFICATION.md Annex A")

def rel_path(item, field=""):
    return item.path(field)


# ====================================================================== contexts
class ContextChecker(object):
    def __init__(self, ctx, display_root, example_mode):
        self.ctx = ctx
        self.spec = ctx.spec
        self.f = Findings()
        self.example_mode = example_mode
        self.display_root = display_root
        self.now = ctx.latest_time()
        self.state = model.State(ctx)
        self._state_at = {}

    def state_at(self, moment):
        key = model.format_time(moment)
        if key not in self._state_at:
            self._state_at[key] = model.State(self.ctx, moment)
        return self._state_at[key]

    def add(self, rule, rid, path, level=None, detail=None):
        self.f.add(rule, rid, path, level, detail)

    # --------------------------------------------------------------- driver
    def run(self):
        for rule, rid, path in self.ctx.findings:
            self.add({"J-0": "J-4"}.get(rule, rule), rid, path)
        self.check_manifest()
        self.check_schemas()
        self.check_ids()
        self.check_parties()
        self.check_modules()
        for item in self.ctx.items:
            kind = item.kind
            if kind in model.CONTENT_KINDS:
                self.check_envelope(item)
                method = getattr(self, "check_" + kind.lower(), None)
                if method:
                    method(item)
                self.check_references(item)
            elif kind == "Review":
                self.check_review(item)
            elif kind == "Proposal":
                self.check_proposal(item)
            elif kind == "Grant":
                self.check_grant(item)
            elif kind == "Tombstone":
                self.check_tombstone(item)
        self.check_events()
        self.check_projections()
        self.check_lock()
        self.check_vault()
        self.check_levels()
        self.check_examples()
        for doc_path, doc in list(self.ctx.pinned_lenses.items()) + list(self.ctx.inline_lenses().items()):
            check_lens_doc(doc, doc_path, self.f, self.spec, ctx=self.ctx)
        for doc_path, doc in list(self.ctx.pinned_playbooks.items()) + list(self.ctx.inline_playbooks().items()):
            check_playbook_doc(doc, doc_path, self.f, self.spec, ctx=self.ctx)
        self.check_playbook_pins()
        self.check_imported_duplicates()
        return self.f

    def check_playbook_pins(self):
        """W-PB5: a pin in Context.playbooks that resolves to no playbook."""
        for index, pin in enumerate(self.ctx.manifest.get("playbooks") or []):
            if not isinstance(pin, dict):
                continue
            if self.ctx.playbook_doc(pin.get("id"), pin.get("version")) is None:
                self.add("W-PB5", None, self.ctx.manifest_rel + "#/playbooks/%d" % index)

    def check_imported_duplicates(self):
        """W-IMP6: two active, non-superseded imported results with the same instrument, time and results."""
        superseded = set(i.data.get("supersedes") for i in self.ctx.content if isinstance(i.data, dict))
        seen = {}
        for item in self.ctx.content:
            data = item.data
            if not model.is_imported_result(item.kind, data) or item.id in superseded:
                continue
            status = self.state.status.get(item.id)
            if status is None or status.admission not in ("active", "proposed"):
                continue
            key = (str((data.get("instrument") or {}).get("id")), jcs.canonicalize(data.get("administeredAt")),
                   jcs.canonicalize(data.get("results")))
            if key in seen:
                self.add("W-IMP6", item.id, rel_path(item, "/results"))
            else:
                seen[key] = item.id

    # ------------------------------------------------------------- manifest
    def check_manifest(self):
        m = self.ctx.manifest
        path = self.ctx.manifest_rel
        if m.get("format") != "ohc.context" or m.get("specVersion") != "0.1.0-draft":
            self.add("CX-1", None, path + "#/format")
        has_arrays = any(isinstance(m.get(c), list) for c in model.COLLECTION_ORDER)
        if "collections" in m and has_arrays:
            self.add("CX-2", None, path + "#/collections")
        if m.get("version") == "":
            self.add("CX-6", None, path + "#/version")
        for index, steward in enumerate(m.get("stewards") or []):
            if isinstance(steward, dict) and steward.get("basis") == "guardianship":
                self.add("CX-7", None, path + "#/stewards/%d/basis" % index)
        conformance = m.get("conformance") if isinstance(m.get("conformance"), dict) else {}
        if conformance.get("level") and conformance.get("subjectIsAdult") is not True:
            self.add("R-C4", None, path + "#/conformance/subjectIsAdult")
        holder = m.get("holder")
        if isinstance(holder, str) and holder not in ("subject", "holder"):
            for item in self.ctx.grants:
                if item.data.get("grantee") == holder and item.data.get("effect", "allow") == "allow":
                    self.add("W-HO1", item.id, rel_path(item, "/grantee"))
        subject = m.get("subject") or {}
        if not isinstance(subject, dict) or not subject.get("id"):
            self.add("SJ-1", None, path + "#/subject/id")
        card = subject.get("card") if isinstance(subject, dict) else None
        if card is not None and (not isinstance(card, dict) or card.get("@type") != "Card" or "version" not in card):
            self.add("SJ-2", None, path + "#/subject/card")
        seen = set()
        for index, alias in enumerate(subject.get("aliases") or [] if isinstance(subject, dict) else []):
            grantee = (alias or {}).get("grantee")
            if grantee in seen:
                self.add("SJ-3", None, path + "#/subject/aliases/%d" % index)
            seen.add(grantee)

    def check_schemas(self):
        m = self.ctx.manifest
        path = self.ctx.manifest_rel
        manifest = dict((k, v) for k, v in m.items() if k not in model.COLLECTION_ORDER)
        errors = self.spec.validate_detail("urn:ohc:schema:context:0.1.0-draft", manifest)
        manifest_rules = set(f["rule"] for f in self.f.items if f["path"].startswith(path + "#/") and f["id"] is None)
        if errors and not manifest_rules.intersection({"CX-1", "CX-2", "CX-6", "CX-7", "SJ-1", "SJ-2", "J-6"}):
            self.add("S-2", None, path + "#" + errors[0][0], detail=errors[0][1])
        self._record_schema_errors = {}
        for item in self.ctx.items:
            kind = item.kind
            schema_id = self.spec.by_kind.get(kind)
            if schema_id is None or not isinstance(item.data, dict):
                self.add("S-3", item.id if isinstance(item.data, dict) else None, rel_path(item))
                continue
            data = item.data
            if "kind" in data and kind != "Tombstone" and data.get("kind") != kind:
                self._record_schema_errors[item.order] = [("/kind", "const: expects %s" % kind)]
                continue
            errs = self.spec.validate_detail(schema_id, data)
            if errs:
                self._record_schema_errors[item.order] = errs

    def flush_schema_errors(self, target_level="L2"):
        """Report each record's schema errors (S-3). A schema error is left out only when a more specific rule
        reported the same field at or below the requested level; a missing or unknown property is never left out."""
        target = LEVELS.index(target_level) if target_level in LEVELS else 2
        for item in self.ctx.items:
            errors = getattr(self, "_record_schema_errors", {}).get(item.order)
            if not errors:
                continue
            for pointer, detail in errors:
                keyword = detail.split(":")[0]
                where = rel_path(item, pointer)
                if keyword not in ("required", "additionalProperties"):
                    specific = [f for f in self.f.items if f["id"] == item.id and f["path"] == where and
                                f["rule"] != "S-3" and f["severity"] == "error" and
                                LEVELS.index(f["level"]) <= target]
                    if specific:
                        continue
                self.add("S-3", item.id, where, detail=detail)

    def check_ids(self):
        tombstoned = set(i.id for i in self.ctx.tombstones)
        for item in self.ctx.duplicates:
            first = self.ctx.by_id.get(item.id)
            if item.kind == "Tombstone" or (first is not None and first.kind == "Tombstone") or item.id in tombstoned:
                self.add("ID-2", item.id, rel_path(item, "/id"))
            else:
                self.add("ID-1", item.id, rel_path(item, "/id"))
        for item in self.ctx.content:
            for field, ref in model.refs_of(item.kind, item.data):
                if ref in self.ctx.by_id or ref in tombstoned or ref in self.ctx.parties:
                    continue
                self.add("ID-3", item.id, rel_path(item, field))
            rid = item.id
            if isinstance(rid, str) and self.state.tier(rid) in ("sensitive", "special"):
                match = re.match(r"^[a-z]{1,5}-(.*)$", rid)
                rest = match.group(1) if match else rid
                if re.search(r"[A-Za-z]{5,}", rest):
                    self.add("W-ID1", rid, rel_path(item, "/id"))

    def check_parties(self):
        path = self.ctx.manifest_rel
        prefixes = {"person": "p-", "agent": "a-", "software": "s-", "organization": "o-"}
        part_ids = set(i.id for i in self.ctx.items if i.kind == "Part")
        for index, party in enumerate(self.ctx.manifest.get("parties") or []):
            if not isinstance(party, dict):
                continue
            pid = party.get("id") or ""
            prefix = prefixes.get(party.get("partyKind"))
            if prefix and not pid.startswith(prefix):
                self.add("PA-1", pid, path + "#/parties/%d/id" % index)
            if pid in part_ids:
                self.add("PA-2", pid, path + "#/parties/%d/id" % index)
            if self.example_mode:
                label = party.get("label") or ""
                if any(re.search(r"\b%s\b" % re.escape(n), label) for n in PERSONAL_NAME_DENY):
                    self.add("PA-3", pid, path + "#/parties/%d/label" % index)
        known = set(self.ctx.parties) | {"subject", "holder"}
        refs = []
        holder = self.ctx.manifest.get("holder")
        if holder:
            refs.append((None, path + "#/holder", holder))
        for index, steward in enumerate(self.ctx.manifest.get("stewards") or []):
            refs.append((None, path + "#/stewards/%d/party" % index, (steward or {}).get("party")))
        for index, alias in enumerate((self.ctx.manifest.get("subject") or {}).get("aliases") or []):
            refs.append((None, path + "#/subject/aliases/%d/grantee" % index, (alias or {}).get("grantee")))
        for item in self.ctx.items:
            if not isinstance(item.data, dict):
                continue
            for field, actor in model.party_refs(item.kind, item.data):
                if item.kind == "Claim" and field == "/about":
                    continue
                refs.append((item.id, rel_path(item, field), actor))
        for rid, where, actor in refs:
            if not isinstance(actor, str):
                continue
            if actor in part_ids:
                self.add("P-1", rid, where)
            elif actor not in known:
                self.add("CX-3", rid, where)

    def check_modules(self):
        declared = set(((self.ctx.manifest.get("conformance") or {}).get("modules")) or ["core"])
        declared.add("core")
        for item in self.ctx.items:
            kind = item.kind
            if kind in ("Tombstone",):
                continue
            module = self.spec.module_of(kind)
            if module and module not in declared:
                maturity = self.spec.maturity(kind)
                self.add("S-5" if maturity == "experimental" else "CX-5", item.id, rel_path(item, "/kind"))

    # --------------------------------------------------------------- envelope
    def writer(self, data):
        return data.get("recordedBy") or data.get("assertedBy")

    def is_agent(self, actor):
        party = self.ctx.parties.get(actor)
        return bool(party) and party.get("partyKind") == "agent"

    def check_envelope(self, item):
        data = item.data
        rid = item.id
        if not isinstance(data, dict):
            return
        if data.get("origin") == "declared" and self.is_agent(data.get("assertedBy")) and "text" not in data:
            self.add("ENV-2", rid, rel_path(item, "/origin"))
        imported = data.get("importedFrom")
        if isinstance(imported, dict) and imported.get("importedAt") and data.get("recordedAt"):
            try:
                if model.parse_time(imported["importedAt"]) != model.parse_time(data["recordedAt"]):
                    self.add("ENV-3", rid, rel_path(item, "/importedFrom/importedAt"))
                if data.get("formulatedAt") and model.parse_time(data["formulatedAt"]) > model.parse_time(data["recordedAt"]):
                    self.add("ENV-3", rid, rel_path(item, "/formulatedAt"))
            except ValueError:
                pass
        stored = data.get("sensitivity")
        if stored and data.get("assertedBy") != "subject":
            default = self.state.kind_default_tier(item)
            if default and vocab.tier_rank(stored) < vocab.tier_rank(default):
                self.add("ENV-5", rid, rel_path(item, "/sensitivity"))
        self.check_supersession(item)
        self.check_layers(item)
        self.check_inf1(item)
        self.check_affect(item)
        self.check_frame_inference(item)
        if data.get("origin") in ("inferred", "derived"):
            grounded = bool(data.get("evidence") or data.get("grounds") or data.get("derivedFrom"))
            if item.kind == "AssessmentRecord" and data.get("source"):
                grounded = True
            if not grounded:
                self.add("LV-1", rid, rel_path(item, "/origin"), level="L1")

    def check_supersession(self, item):
        data = item.data
        target = data.get("supersedes")
        if not isinstance(target, str):
            return
        prior = self.ctx.by_id.get(target)
        if prior is None:
            return
        if prior.kind != item.kind:
            self.add("ENV-4", item.id, rel_path(item, "/supersedes"))
            return
        seen = {item.id}
        cursor = target
        while isinstance(cursor, str):
            if cursor in seen:
                self.add("ENV-4", item.id, rel_path(item, "/supersedes"))
                break
            seen.add(cursor)
            nxt = self.ctx.by_id.get(cursor)
            cursor = nxt.data.get("supersedes") if nxt and isinstance(nxt.data, dict) else None
        at = model.parse_time(data.get("recordedAt"))
        if at is not None:
            prior_status = self.state_at(at).status.get(target)
            if prior_status is not None and prior_status.locked and data.get("assertedBy") != "subject":
                self.add("ENV-4", item.id, rel_path(item, "/supersedes"))

    def check_layers(self, item):
        layer = self.spec.layer(item.kind)
        data = item.data
        for field, ref in model.refs_of(item.kind, data):
            target_kind = self.ctx.kind_of(ref)
            if target_kind is None or target_kind == "Tombstone":
                continue  # TB-2: a reference to an erased record is allowed and renders as [erased]
            if layer in ("evidence", "experience", "assertion") and target_kind in ("Outcome", "RecallCue"):
                self.add("G4", item.id, rel_path(item, field))
                continue
            if item.kind == "Source":
                if target_kind == "Interpretation":
                    self.add("I6", item.id, rel_path(item, field))
                elif target_kind != "Source":
                    self.add("SR-6", item.id, rel_path(item, field))
            elif item.kind == "Episode":
                if target_kind == "Interpretation":
                    self.add("I6", item.id, rel_path(item, field))
                elif target_kind not in ("Source", "Episode"):
                    self.add("EP-1", item.id, rel_path(item, field))
            if field.endswith("/ref") or "/grounds/" in field or "/evidence/" in field or "/derivedFrom/" in field:
                if target_kind == "HealthRef":
                    self.add("HR-4", item.id, rel_path(item, field))
        if item.kind in model.INTERPRETATION_LAYER:
            for field, ref in model.refs_of(item.kind, data):
                if item.kind == "Interpretation" and field.startswith("/about/"):
                    continue  # I8
                if ref in self.ctx.parties:
                    self.add("TP-2", item.id, rel_path(item, field))

    @staticmethod
    def reference_code(kind, field):
        """The reference-targets catalog code for a field path from ``model.refs_of`` (None: governed elsewhere)."""
        parts = field.strip("/").split("/")
        head = parts[0]
        if head in ("supersedes",) or (kind == "Relation" and head in ("from", "to")):
            return None
        if head in ("grounds", "counterEvidence", "evidence") and len(parts) >= 3:
            return "%s.%s.%s" % (kind, head, "span" if parts[2] == "span" else "ref")
        if head == "derivedFrom":
            return "%s.derivedFrom" % kind
        if kind == "Interpretation" and head == "about":
            return "Interpretation.about.span" if parts[-1] == "source" else "Interpretation.about"
        if kind == "Outcome" and head == "about":
            return "Outcome.about.%s" % parts[1]
        if kind == "Episode" and head == "accounts":
            return "Episode.accounts.evidence"
        if kind == "Episode" and head == "externalConfirmation":
            return "Episode.externalConfirmation.basis"
        if kind == "ModelView" and head == "scope":
            return "ModelView.scope.%s" % parts[1]
        if head in ("offer", "delivery", "custody", "practice", "valueAddress"):
            return "%s.%s.%s" % (kind, head, parts[1])
        return "%s.%s" % (kind, head)

    def check_references(self, item):
        """RF-1: every reference field points only at the kinds the allowed-reference matrix lists
        (spec/catalogs/reference-targets.json). Tombstoned targets are always allowed (TB-2)."""
        if not isinstance(item.data, dict):
            return
        reported = set(f["path"] for f in self.f.items if f["id"] == item.id)
        for field, ref in model.refs_of(item.kind, item.data):
            code = self.reference_code(item.kind, field)
            if code is None:
                continue
            target_kind = self.ctx.kind_of(ref)
            if target_kind is None and ref not in self.ctx.parties:
                continue  # dangling: ID-3
            if target_kind == "Tombstone":
                continue
            allowed = self.spec.reference_targets.get(code, set())
            where = rel_path(item, field)
            if (target_kind or "Party") not in allowed and where not in reported:
                self.add("RF-1", item.id, where)

    def grant_matches_record(self, grant, item, state):
        explicit = (grant.get("basis") or {}).get("legal") == "explicit-consent"
        scope = grant.get("scope") or {}
        if any(grants.matches(s, item, state) for s in scope.get("exclude") or []):
            return False
        tier = state.tier(item.id)
        named = state.audience(item.id) == "named"
        for selector in scope.get("include") or []:
            if not grants.matches(selector, item, state):
                continue
            if tier == "special":
                if grants.names_special(selector, item, state) and explicit:
                    return True
            elif tier == "sensitive" or named:
                if grants.names_sensitive(selector):
                    return True
            else:
                return True
        return False

    def steward_may_write(self, steward, item, data):
        """INF-1: a steward writes within scope when its scope holds ``write`` (and ``infer`` for an inference),
        matches the record's kind and facet, and is valid at ``recordedAt``."""
        scope = steward.get("scope") or {}
        actions = set(scope.get("actions") or [])
        if "write" not in actions or (data.get("origin") == "inferred" and "infer" not in actions):
            return False
        if scope.get("kinds") and item.kind not in scope["kinds"]:
            return False
        if scope.get("facets") and data.get("facet") not in scope["facets"]:
            return False
        if item.kind == "Part" or self.state.tier(item.id) == "special":
            return False
        at = model.parse_time(data.get("recordedAt"))
        start, end = model.parse_time(steward.get("validFrom")), model.parse_time(steward.get("validUntil"))
        return at is not None and start is not None and end is not None and start <= at < end

    def check_inf1(self, item):
        data = item.data
        writer = self.writer(data)
        if writer == "subject":
            return
        if writer == "holder":
            # The holder may write what it is given (imports, copies, derived scoring) but never its own
            # inference: an inference about the person is made by a Party under an infer grant.
            if data.get("origin") == "inferred":
                self.add("INF-1", item.id, rel_path(item, "/origin"))
            return
        steward = self.ctx.stewards.get(writer)
        if steward is not None and not data.get("underGrant"):
            if not self.steward_may_write(steward, item, data):
                self.add("INF-1", item.id, rel_path(item, "/recordedBy" if data.get("recordedBy") else "/assertedBy"))
            return
        gid = data.get("underGrant")
        if not gid:
            self.add("INF-1", item.id, rel_path(item, "/underGrant"))
            return
        grant_item = self.ctx.by_id.get(gid)
        if grant_item is None or grant_item.kind != "Grant":
            self.add("INF-1", item.id, rel_path(item, "/underGrant"))
            return
        grant = grant_item.data
        at = model.parse_time(data.get("recordedAt"))
        actions = set(grant.get("actions") or [])
        ok = grant.get("grantee") == writer and grant.get("effect", "allow") == "allow"
        ok = ok and at is not None and self.state.grant_status(gid, at) == "given"
        ok = ok and bool(actions.intersection({"suggest", "write"}))
        if data.get("origin") == "inferred":
            ok = ok and "infer" in actions
        ok = ok and data.get("purpose") in (grant.get("purposes") or [])
        ok = ok and self.grant_matches_record(grant, item, self.state)
        if not ok:
            self.add("INF-1", item.id, rel_path(item, "/underGrant"))

    # ------------------------------------------------------------- per kind
    def check_claim(self, item):
        data = item.data
        rid = item.id
        has_text, has_absence = "text" in data, "absence" in data
        if has_text == has_absence:
            self.add("CL-1", rid, rel_path(item, "/text"))
        if has_absence and "value" in data:
            self.add("CL-2", rid, rel_path(item, "/value"))
        if has_absence and "valueAddress" in data:
            self.add("CL-2", rid, rel_path(item, "/valueAddress"))
        if "value" in data:
            value = data["value"]
            stand_in = value is None or value is False or value == "" or value == {} or value == [] or \
                (value == 0 and not isinstance(value, bool) and "unit" not in data)
            if stand_in:
                self.add("CL-2", rid, rel_path(item, "/value"))
        absence = data.get("absence")
        if isinstance(absence, dict) and absence.get("intentional"):
            if absence.get("code") != "not-chosen":
                self.add("CL-9", rid, rel_path(item, "/absence/code"))
            elif data.get("assertedBy") != "subject":
                self.add("CL-9", rid, rel_path(item, "/absence/intentional"))
        facet = data.get("facet")
        if facet == "disposition":
            ok = data.get("origin") == "declared" and data.get("assertedBy") == "subject"
            if data.get("origin") == "derived":
                kinds = [self.ctx.kind_of(r) for r in data.get("derivedFrom") or [] if isinstance(r, str)]
                ok = "AssessmentRecord" in kinds
                if "Pattern" in kinds:
                    self.add("PT-3", rid, rel_path(item, "/derivedFrom"), level="L1")
            if not ok:
                self.add("CL-3", rid, rel_path(item, "/origin"))
        if data.get("horizon") == "state" and not (
                (data.get("valid") or {}).get("until") or data.get("valueAddress") or data.get("reviewAfter")):
            self.add("W-CL5", rid, rel_path(item, "/horizon"))
        if "about" in data:
            if facet not in ("relationship", "commitment", "boundary", "preference", "goal"):
                self.add("CL-6", rid, rel_path(item, "/about"))
            elif data["about"] not in self.ctx.parties:
                self.add("ID-3", rid, rel_path(item, "/about"))
        if "value" in data and "valueAddress" in data:
            self.add("CL-7", rid, rel_path(item, "/valueAddress"))
        predicate = data.get("predicate")
        if predicate is not None and not str(predicate).startswith("x-") and facet in self.spec.facet_predicates:
            if predicate not in self.spec.facet_predicates.get(facet, set()):
                self.add("CL-8", rid, rel_path(item, "/predicate"))
        sources = self.grounding_sources(data)
        if sources and all((self.ctx.record(s) or {}).get("inbound") for s in sources):
            only_spans = all(isinstance(g, dict) and "span" in g for g in data.get("evidence") or [])
            if only_spans:
                self.add("W-SR1", rid, rel_path(item, "/evidence"))

    def affect_bearing(self, item):
        """R-X3/R-X4: is this record about affect, whatever its labels say?"""
        data = item.data
        vocabulary = self.ctx.manifest.get("vocabulary") or {}
        if affect.predicate_is_affect(data.get("predicate"), vocabulary):
            return True
        if affect.quarantine_marked(data):
            return True
        return False

    def behavioural_grounds(self, rid, seen=None):
        """Every biometric or behavioural Source a record rests on, followed transitively through evidence, grounds,
        derivedFrom and Episode account evidence (R-X4)."""
        seen = seen if seen is not None else set()
        if not isinstance(rid, str) or rid in seen:
            return []
        seen.add(rid)
        item = self.ctx.by_id.get(rid)
        if item is None or not isinstance(item.data, dict):
            return []
        data = item.data
        if item.kind == "Source":
            return [rid] if data.get("sourceKind") in self.spec.biometric_kinds else []
        refs = []
        for field in ("evidence", "grounds"):
            for ground in data.get(field) or []:
                if not isinstance(ground, dict):
                    continue
                if isinstance(ground.get("span"), dict):
                    refs.append(ground["span"].get("source"))
                if isinstance(ground.get("ref"), str):
                    refs.append(ground["ref"])
        refs.extend(r for r in data.get("derivedFrom") or [] if isinstance(r, str))
        if item.kind == "Episode":
            for account in data.get("accounts") or []:
                for span in (account or {}).get("evidence") or []:
                    if isinstance(span, dict):
                        refs.append(span.get("source"))
        if item.kind == "AssessmentRecord" and isinstance(data.get("source"), str):
            refs.append(data["source"])
        out = []
        for ref in refs:
            for found in self.behavioural_grounds(ref, seen):
                if found not in out:
                    out.append(found)
        return out

    def check_affect(self, item):
        """CL-4 (R-X3, R-X4), independent of facet and method labels.

        - An affect record (affect predicate, an x- predicate whose ``broader`` chain reaches one, or the R-X3
          quarantine mark) that the subject did not declare must carry the quarantine.
        - Nothing observed, inferred or derived that rests on a biometric or behavioural Source, directly or through
          Episodes, Claims or grounds, may be about affect; the lexical classifier decides when the labels do not,
          and when unsure it says affect (fail closed). A ``state`` resting on such signals needs a closed
          non-affect predicate (availability, load).
        - Elsewhere the classifier only warns (W-CL4): an unquarantined record that reads as affect.
        """
        data = item.data
        rid = item.id
        declared_by_subject = data.get("origin") == "declared" and data.get("assertedBy") == "subject"
        affective = self.affect_bearing(item)
        if item.kind == "Claim" and affective and not (declared_by_subject or affect.quarantine_marked(data)):
            self.add("CL-4", rid, rel_path(item, "/predicate" if data.get("predicate") else "/handling"))
        if declared_by_subject:
            return
        reads_as_affect = affect.affect_text(data.get("text"), data.get("rationale"))
        behavioural = self.behavioural_grounds(rid) if data.get("origin") in ("observed", "inferred", "derived") \
            else []
        if behavioural:
            field = "/evidence" if "evidence" in data else "/grounds" if "grounds" in data else "/derivedFrom"
            if affective or reads_as_affect:
                self.add("CL-4", rid, rel_path(item, field))
            elif item.kind == "Claim" and data.get("facet") == "state" and \
                    data.get("predicate") not in affect.NON_AFFECT_STATE_PREDICATES:
                self.add("CL-4", rid, rel_path(item, "/predicate"))
        elif reads_as_affect and not affect.quarantine_marked(data):
            self.add("W-CL4", rid, rel_path(item, "/text"))

    def grounding_sources(self, data):
        out = []
        for field in ("evidence", "grounds"):
            for ground in data.get(field) or []:
                if not isinstance(ground, dict):
                    continue
                if isinstance(ground.get("span"), dict):
                    out.append(ground["span"].get("source"))
                elif isinstance(ground.get("ref"), str) and self.ctx.kind_of(ground["ref"]) == "Source":
                    out.append(ground["ref"])
        for ref in data.get("derivedFrom") or []:
            if isinstance(ref, str) and self.ctx.kind_of(ref) == "Source":
                out.append(ref)
        return [s for s in out if isinstance(s, str)]

    def check_relation(self, item):
        data = item.data
        rid = item.id
        rel = data.get("rel")
        src, dst = data.get("from"), data.get("to")
        if isinstance(src, str) and isinstance(dst, str) and src == dst:
            self.add("RL-4", rid, rel_path(item, "/to"))
        info = self.spec.relation_codes.get(rel) or {}
        if info.get("module"):
            declared = set(((self.ctx.manifest.get("conformance") or {}).get("modules")) or [])
            if info["module"] not in declared:
                self.add("RL-3", rid, rel_path(item, "/rel"))
        from_kind = self.ctx.kind_of(src) if isinstance(src, str) else None
        to_kind = self.ctx.kind_of(dst) if isinstance(dst, str) else None
        tombstoned = set(i.id for i in self.ctx.tombstones)
        for end, end_kind, field in ((src, from_kind, "/from"), (dst, to_kind, "/to")):
            if isinstance(end, str) and end_kind is None and end not in tombstoned:
                self.add("RL-1", rid, rel_path(item, field))
        if from_kind in (None, "Tombstone") or to_kind in (None, "Tombstone"):
            return
        allowed = False
        for pair in info.get("endpoints") or []:
            froms, tos = pair.get("from", []), pair.get("to", [])
            ok_from = from_kind in froms or ("content" in froms and from_kind in model.CONTENT_KINDS)
            ok_to = to_kind in tos or ("content" in tos and to_kind in model.CONTENT_KINDS) or \
                ("same-kind" in tos and to_kind == from_kind)
            if ok_from and ok_to:
                allowed = True
        if allowed and rel == "practice-for" and to_kind == "Claim":
            allowed = (self.ctx.record(dst) or {}).get("facet") in ("goal", "need", "state")
        if allowed and rel == "competes-for-resource":
            allowed = all((self.ctx.record(x) or {}).get("facet") in ("goal", "commitment") for x in (src, dst))
        if not allowed:
            self.add("RL-2", rid, rel_path(item, "/rel"))

    def check_source(self, item):
        data = item.data
        rid = item.id
        content = data.get("content") or {}
        sha = content.get("sha256")
        if data.get("sourceKind") != "live-feed" and not sha:
            self.add("SR-1", rid, rel_path(item, "/content/sha256"))
        locator = content.get("locator") or {}
        vault_path = locator.get("vaultPath") if isinstance(locator, dict) else None
        if vault_path:
            match = re.match(r"^vault/([0-9a-f]{2})/([0-9a-f]{64})\.[A-Za-z0-9]+$", vault_path)
            if not match or not sha or match.group(2) != sha or match.group(1) != sha[:2]:
                self.add("SR-3", rid, rel_path(item, "/content/locator/vaultPath"))
            elif not model.PATH_RE.match(vault_path):
                self.add("J-6", rid, rel_path(item, "/content/locator/vaultPath"))
            else:
                full = os.path.join(self.ctx.dir, vault_path)
                if os.path.isfile(full):
                    digest = hashlib.sha256()
                    with open(full, "rb") as handle:
                        for block in iter(lambda: handle.read(65536), b""):
                            digest.update(block)
                    if digest.hexdigest() != sha:
                        self.add("SR-2", rid, rel_path(item, "/content/sha256"))
        for field in ("note",):
            if isinstance(data.get(field), str) and len(data[field]) > 280:
                self.add("SR-4", rid, rel_path(item, "/" + field))
        custody = data.get("custody") or {}
        confidentiality = custody.get("confidentiality", "none")
        if confidentiality != "none":
            info = self.spec.custody.get(confidentiality) or {}
            ceiling = info.get("ceilingWithRelease") if custody.get("releaseRef") else info.get("ceilingWithoutRelease")
            max_release = data.get("maxRelease", "index")
            if ceiling and vocab.release_rank(max_release) > vocab.release_rank(ceiling):
                self.add("SR-5", rid, rel_path(item, "/maxRelease"))
            if not custody.get("releaseRef") and data.get("maxRelease", "index") != "index":
                self.add("SR-7", rid, rel_path(item, "/custody/releaseRef"))

    def check_episode(self, item):
        data = item.data
        rid = item.id
        for index, account in enumerate(data.get("accounts") or []):
            if not isinstance(account, dict):
                continue
            if account.get("narrator") != "subject" and ("experienced" in account or "affectTags" in account):
                self.add("EP-3", rid, rel_path(item, "/accounts/%d" % index))
            if account.get("accountKind") == "observer-account":
                if account.get("narrator") not in self.ctx.parties:
                    self.add("EP-5", rid, rel_path(item, "/accounts/%d/narrator" % index))
                text = " ".join(str(account.get(k, "")) for k in ("happened", "text", "didOrTried")).lower()
                if any(word in text for word in INNER_STATE_WORDS):
                    self.add("TP-3", rid, rel_path(item, "/accounts/%d" % index))
        if data.get("recall", "not-permitted") != "not-permitted" and data.get("assertedBy") != "subject":
            self.add("EP-6", rid, rel_path(item, "/recall"))
        prior_id = data.get("supersedes")
        prior = self.ctx.record(prior_id) if isinstance(prior_id, str) else None
        if prior is not None and self.ctx.kind_of(prior_id) == "Episode":
            old = prior.get("accounts") or []
            new = data.get("accounts") or []
            if len(new) < len(old) or any(not jcs.equal(a, b) for a, b in zip(old, new)):
                self.add("EP-2", rid, rel_path(item, "/accounts"))

    def adoption_ok(self, item, data, rule):
        """I5 / MV-3 / PT-2: who may read through a lens.

        An agent or software author writes under an ``infer`` grant whose scope names the lens; any other non-subject
        author is listed in ``interpretationAuthors`` of the active adoption that ``adoption`` names. An active
        adoption of the lens with ``agentInterpretation`` ``off`` (or none) stops agent and software authors; with
        ``ask-first``, at L2, a confirmed ``ask-first`` Event precedes the record.
        """
        author = data.get("assertedBy")
        lens_id = model.lens_id_of(data)
        if author == "subject" or not lens_id:
            return
        at = model.parse_time(data.get("recordedAt"))
        state = self.state_at(at) if at else self.state
        adoption_id = data.get("adoption")
        named = self.ctx.by_id.get(adoption_id) if isinstance(adoption_id, str) else None
        if named is not None and named.kind == "LensAdoption" and \
                (named.data.get("lens") or {}).get("id") != lens_id:
            self.add(rule, item.id, rel_path(item, "/lens"))
            return
        party = self.ctx.parties.get(author) or {}
        if party.get("partyKind") in ("agent", "software"):
            if not self.infer_grant_names_lens(data, lens_id):
                self.add(rule, item.id, rel_path(item, "/underGrant"))
                return
            for adoption_item in self.active_adoptions(lens_id, state):
                mode = adoption_item.data.get("agentInterpretation", "off")
                if mode == "off":
                    self.add(rule, item.id, rel_path(item, "/lens"))
                    return
                if mode == "ask-first" and not self.ask_first_confirmed(author, adoption_item.id, at):
                    self.add(rule, item.id, rel_path(item, "/adoption"), level="L2")
                    return
            return
        if named is None or named.kind != "LensAdoption":
            self.add(rule, item.id, rel_path(item, "/adoption"))
            return
        status = state.status.get(adoption_id)
        active = status is not None and status.admission == "active" and status.lifecycle == "active"
        if not active or author not in (named.data.get("interpretationAuthors") or ["subject"]):
            self.add(rule, item.id, rel_path(item, "/adoption"))

    def infer_grant_names_lens(self, data, lens_id):
        """I5: the record's ``underGrant`` holds ``infer`` and an include selector that names the lens."""
        grant_item = self.ctx.by_id.get(data.get("underGrant")) if isinstance(data.get("underGrant"), str) else None
        if grant_item is None or grant_item.kind != "Grant":
            return False
        grant = grant_item.data
        if "infer" not in (grant.get("actions") or []):
            return False
        return any(isinstance(s, dict) and lens_id in (s.get("lenses") or [])
                   for s in (grant.get("scope") or {}).get("include") or [])

    def active_adoptions(self, lens_id, state):
        """The person's current, active adoptions of a lens (not superseded) as known in ``state``."""
        superseded = set(i.data.get("supersedes") for i in self.ctx.content
                         if i.kind == "LensAdoption" and isinstance(i.data, dict) and state.known(i))
        out = []
        for adoption_item in self.ctx.content:
            if adoption_item.kind != "LensAdoption" or adoption_item.id in superseded or \
                    (adoption_item.data.get("lens") or {}).get("id") != lens_id or not state.known(adoption_item):
                continue
            status = state.status.get(adoption_item.id)
            if status is not None and status.admission == "active" and status.lifecycle == "active":
                out.append(adoption_item)
        return out

    def ask_first_confirmed(self, author, adoption_id, at):
        for event in self.ctx.events:
            e = event.data
            if e.get("eventType") == "ask-first" and e.get("outcome") == "confirmed" and \
                    e.get("counterparty") == author and adoption_id in (e.get("records") or []):
                when = model.parse_time(e.get("at"))
                if when is not None and at is not None and when <= at:
                    return True
        return False

    def check_interpretation(self, item):
        data = item.data
        rid = item.id
        subject = data.get("assertedBy") == "subject"
        if not subject:
            if self.effective_epistemic(data) not in ("hypothesis", "frame-relative"):
                self.add("I1", rid, rel_path(item, "/epistemic"))
        self.check_reading_origin(item)
        grounds = data.get("grounds") or []
        if data.get("causal") == "asserted":
            if not subject or not any(isinstance(g, dict) and g.get("kind") != "sequence" for g in grounds):
                self.add("I2", rid, rel_path(item, "/causal"))
        if not subject:
            alternatives = data.get("alternatives") or []
            if len(grounds) < 1 or len(alternatives) < 2 or not data.get("limits") or not any(
                    isinstance(a, dict) and a.get("kind") in NON_PSYCH_ALTERNATIVES for a in alternatives):
                self.add("I4", rid, rel_path(item, "/alternatives"))
        self.adoption_ok(item, data, "I5")
        held = data.get("heldDuring") or {}
        if held.get("from") and held.get("until"):
            try:
                if model.parse_time(held["until"]) <= model.parse_time(held["from"]):
                    self.add("I7", rid, rel_path(item, "/heldDuring"))
            except ValueError:
                pass
        for index, ref in enumerate(data.get("about") or []):
            if isinstance(ref, str) and ref in self.ctx.parties:
                self.add("I8", rid, rel_path(item, "/about/%d" % index))

    def effective_epistemic(self, data):
        """The stored epistemic status, else the default of the record's origin (§6.1)."""
        if data.get("epistemic"):
            return data["epistemic"]
        origins = dict((c["code"], c) for c in self.spec.catalogs["origin"]["codes"])
        return (origins.get(data.get("origin")) or {}).get("defaultEpistemic", "as-reported")

    def check_reading_origin(self, item):
        """I10: a reading written by an agent or by software is an inference, never a declaration."""
        data = item.data
        author = data.get("assertedBy")
        party = self.ctx.parties.get(author) or {}
        if party.get("partyKind") not in ("agent", "software"):
            return
        origin = data.get("origin")
        if origin == "inferred" or (origin == "derived" and (data.get("generatedBy") or {}).get("method")):
            return
        self.add("I10", item.id, rel_path(item, "/origin"))

    def check_tension(self, item):
        data = item.data
        rid = item.id
        if data.get("whoDecides") == "holder-policy" and data.get("tensionKind") not in (
                "source-divergence", "holder-divergence"):
            self.add("T2", rid, rel_path(item, "/whoDecides"))
        between = [b for b in data.get("between") or [] if isinstance(b, str)]
        if len(set(between)) != len(between):
            self.add("T4", rid, rel_path(item, "/between"))
        for index, ref in enumerate(between):
            kind = self.ctx.kind_of(ref)
            if kind is None:
                continue
            if kind == "Source" and data.get("tensionKind") != "source-divergence":
                self.add("T4", rid, rel_path(item, "/between/%d" % index))
            elif kind not in ("Claim", "Interpretation", "AssessmentRecord", "Source", "Tombstone"):
                self.add("T4", rid, rel_path(item, "/between/%d" % index))

    def check_lensadoption(self, item):
        data = item.data
        rid = item.id
        lens_ref = data.get("lens") or {}
        lens_id = lens_ref.get("id")
        doc = self.ctx.lens_doc(lens_id, lens_ref.get("version"))
        pins = [p for p in self.ctx.manifest.get("lenses") or [] if isinstance(p, dict)]
        pinned = any(p.get("id") == lens_id and p.get("version") == lens_ref.get("version") for p in pins)
        if not (pinned or self.spec.lens(lens_id)):
            self.add("LA-6", rid, rel_path(item, "/lens"))
        if doc is None:
            # No resolvable descriptor: fail closed and treat the lens as a stub (LA-6).
            self.add("W-LA6", rid, rel_path(item, "/lens"))
            doc = STUB_DESCRIPTOR
        if data.get("route") == "agent-suggested":
            for review in self.ctx.reviews:
                r = review.data
                if rid in model.review_targets(r) and r.get("action") in ("admit", "endorse", "partially-endorse",
                                                                           "contest") and r.get("by") != "subject":
                    self.add("LA-1", rid, rel_path(item, "/route"))
        for index, playbook_id in enumerate(data.get("playbooks") or []):
            playbook = self.ctx.playbook_doc(playbook_id, self.pinned_playbook_version(playbook_id))
            if playbook is None or lens_id not in (playbook.get("lenses") or []):
                self.add("PB-3", rid, rel_path(item, "/playbooks/%d" % index))
        practice = data.get("practice") or {}
        if data.get("route") == "inherited-from-practice":
            practitioner = practice.get("practitioner")
            stored = any(i.kind == "Source" and ((i.data.get("custody") or {}).get("custodian") == practitioner or
                                                 (i.data.get("authorship") or {}).get("author") == practitioner)
                         for i in self.ctx.content)
            if not practice or (stored and not practice.get("releaseRef")):
                self.add("LA-3", rid, rel_path(item, "/practice"))

    def check_imported_result(self, item):
        """IMP-1...IMP-5 and W-IMP2 for an AssessmentRecord whose importedFrom.system is an instrument id."""
        data = item.data
        rid = item.id
        imported = data.get("importedFrom") or {}
        system = imported.get("system")
        declared = set(((self.ctx.manifest.get("conformance") or {}).get("modules")) or [])
        if not {"lenses", "instrument-import"} <= declared:
            self.add("IMP-1", rid, rel_path(item, "/importedFrom/system"))
        instrument = self.spec.instruments.get(system) or {}
        block = instrument.get("import") if isinstance(instrument.get("import"), dict) else None
        if block is None:
            self.add("IMP-2", rid, rel_path(item, "/importedFrom/system"))
        else:
            if (data.get("instrument") or {}).get("id") != system:
                self.add("IMP-2", rid, rel_path(item, "/instrument/id"))
            if (data.get("lens") or {}).get("id") != instrument.get("lens"):
                self.add("IMP-2", rid, rel_path(item, "/lens/id"))
            if instrument.get("scoring") == "proprietary" and \
                    "vendor-algorithm-undisclosed" not in (data.get("validityFlags") or []):
                self.add("IMP-2", rid, rel_path(item, "/validityFlags"))
            if instrument.get("version") != imported.get("systemVersion"):
                self.add("W-IMP2", rid, rel_path(item, "/importedFrom/systemVersion"))
            else:
                self.check_imported_values(item, block)
        party = self.ctx.parties.get(data.get("assertedBy")) or {}
        scorer = (block or {}).get("scoredBy") or {}
        if data.get("assertedBy") == "subject" or party.get("partyKind") != "organization" or \
                (block is not None and party.get("uri") != scorer.get("id")):
            self.add("IMP-3", rid, rel_path(item, "/assertedBy"))
        if data.get("recordedBy") != "subject":
            self.add("IMP-3", rid, rel_path(item, "/recordedBy"))
        if data.get("origin") != "imported":
            self.add("IMP-3", rid, rel_path(item, "/origin"))
        source_id = data.get("source")
        if isinstance(source_id, str):
            source = self.ctx.by_id.get(source_id)
            sdata = source.data if source is not None and source.kind == "Source" else None
            if sdata is None or sdata.get("sourceKind") != "instrument-report" or \
                    vocab.tier_rank(sdata.get("sensitivity")) < vocab.tier_rank(self.state.tier(rid)) or \
                    not set(self.state.categories(rid)) <= set(sdata.get("categories") or []):
                self.add("IMP-4", rid, rel_path(item, "/source"))
        day = model.administered_day(data)
        try:
            formulated = model.parse_time(data.get("formulatedAt"))
            recorded = model.parse_time(data.get("recordedAt"))
        except ValueError:
            formulated = recorded = None
        if day is None or formulated != day:
            self.add("IMP-5", rid, rel_path(item, "/formulatedAt"))
        elif recorded is not None and day > recorded:
            self.add("IMP-5", rid, rel_path(item, "/administeredAt"))

    def check_imported_values(self, item, block):
        """IMP-2: scales, kinds, ranges and norm groups against the instrument's import block."""
        data = item.data
        rid = item.id
        scales = set(s for s in block.get("scales") or [] if isinstance(s, str))
        kinds = dict((s.get("kind"), s) for s in block.get("scores") or [] if isinstance(s, dict))
        seen = set()
        for index, result in enumerate(data.get("results") or []):
            where = rel_path(item, "/results/%d" % index)
            if not isinstance(result, dict) or result.get("type") != "dimension-score" or \
                    result.get("construct") not in scales or result.get("construct") in seen:
                self.add("IMP-2", rid, where)
                continue
            seen.add(result.get("construct"))
            values = []
            if "raw" in result:
                values.append(("raw", result.get("raw")))
            if isinstance(result.get("standardized"), dict):
                values.append((result["standardized"].get("type"), result["standardized"].get("value")))
            for kind, value in values:
                score = kinds.get(kind)
                rng = (score or {}).get("range") or []
                ok = score is not None and isinstance(value, (int, float)) and len(rng) == 2 and \
                    rng[0] <= value <= rng[1]
                if ok and score.get("integer") and not float(value).is_integer():
                    ok = False
                if not ok:
                    self.add("IMP-2", rid, where)
                    break
        norm = (data.get("normGroup") or {}).get("id")
        if norm is not None and norm not in [g.get("id") for g in block.get("normGroups") or [] if isinstance(g, dict)]:
            self.add("IMP-2", rid, rel_path(item, "/normGroup/id"))

    def check_frame_inference(self, item):
        """AR-4: a record inferred from a result of a symbolic-frame or T5 lens is frame-relative too."""
        data = item.data
        if data.get("origin") != "inferred":
            return
        refs = []
        for field in ("evidence", "grounds"):
            for ground in data.get(field) or []:
                if isinstance(ground, dict) and isinstance(ground.get("ref"), str):
                    refs.append(ground["ref"])
        refs.extend(r for r in data.get("derivedFrom") or [] if isinstance(r, str))
        if item.kind == "Interpretation":
            refs.extend(r for r in data.get("about") or [] if isinstance(r, str))
        for ref in refs:
            target = self.ctx.by_id.get(ref)
            if target is None or target.kind != "AssessmentRecord" or not self.state.frame_relative(target.data):
                continue
            status = self.state.status.get(item.id)
            epistemic = status.epistemic if status is not None else data.get("epistemic")
            if epistemic != "frame-relative":
                self.add("AR-4", item.id, rel_path(item, "/epistemic"))
            return

    def pinned_playbook_version(self, playbook_id):
        for pin in self.ctx.manifest.get("playbooks") or []:
            if isinstance(pin, dict) and pin.get("id") == playbook_id:
                return pin.get("version")
        return None

    def check_assessmentrecord(self, item):
        data = item.data
        rid = item.id
        mode = data.get("mode")
        expected = (self.spec.assessment_modes.get(mode) or {}).get("expectedOrigin")
        if expected and data.get("origin") not in expected:
            self.add("AR-1", rid, rel_path(item, "/origin"))
        lens_ref = data.get("lens") or {}
        doc = self.ctx.lens_doc(lens_ref.get("id"), lens_ref.get("version")) or {}
        if mode in ("agent-inference", "cross-lens-estimate"):
            marks = set(m.get("mark") for m in (doc.get("ip") or {}).get("marks") or [] if isinstance(m, dict))
            labels = set(r.get("label") for r in data.get("results") or [] if isinstance(r, dict))
            ok = "person-only" in set(data.get("handling") or [])
            ok = ok and "agent-estimate-not-validated" in set(data.get("validityFlags") or [])
            ceiling = "agent-estimate-not-validated" if mode == "agent-inference" else "cross-lens-population-estimate"
            ok = ok and data.get("validityCeiling") == ceiling
            ok = ok and not (marks & labels) and "trademarkNotice" not in data
            if not ok:
                self.add("AR-2", rid, rel_path(item, "/mode"))
        test_data = (data.get("ext") or {}).get("ohc.test-data")
        if test_data is not None and not ("person-only" in set(data.get("handling") or []) and
                                          "test-data-personal-only" in set(data.get("validityFlags") or [])):
            self.add("AR-2", rid, rel_path(item, "/ext"))
        evidence = doc.get("evidence") or {}
        if evidence.get("ontologicalStatus") == "symbolic-frame" or evidence.get("measurementTier") == "T5":
            if data.get("epistemic") not in (None, "frame-relative"):
                self.add("AR-4", rid, rel_path(item, "/epistemic"))
        results = [r for r in data.get("results") or [] if isinstance(r, dict)]
        types = [r for r in results if r.get("type") == "type-assignment" and r.get("method") in ("instrument", "best-fit")]
        if types and not (any(r.get("type") == "dimension-score" for r in results) and
                          (data.get("generatedBy") or {}).get("method")):
            self.add("AR-6", rid, rel_path(item, "/results"))
        if mode == "cross-lens-estimate":
            mapping = self.spec.mappings.get(data.get("mapping"))
            ok = mapping is not None and mapping.get("chainable") is False
            ok = ok and mapping.get("rowStatus") in ("accepted", "accepted-with-loss") and not mapping.get("forbiddenUse")
            ok = ok and (mapping.get("to") or {}).get("lens") == lens_ref.get("id")
            if ok:
                for end in ("from", "to"):
                    end_doc = self.ctx.lens_doc((mapping.get(end) or {}).get("lens")) or {}
                    if (end_doc.get("useLimits") or {}).get("crossLensMapping") != "population-level-only":
                        ok = False
            if not ok:
                self.add("AR-7", rid, rel_path(item, "/mapping"))
        instrument = (data.get("instrument") or {}).get("id")
        if instrument and doc and instrument not in (doc.get("instruments") or []):
            self.add("AR-8", rid, rel_path(item, "/instrument/id"))
        if model.is_imported_result(item.kind, data):
            self.check_imported_result(item)

    def check_modelview(self, item):
        data = item.data
        rid = item.id
        scope = data.get("scope") or {}
        episodes = set(scope.get("episodes") or [])
        sources = set(scope.get("sources") or [])
        for index, hid in enumerate(data.get("hypotheses") or []):
            hyp = self.ctx.by_id.get(hid)
            if hyp is None:
                continue
            if hyp.kind != "Interpretation":
                self.add("MV-1", rid, rel_path(item, "/hypotheses/%d" % index))
                continue
            for about in hyp.data.get("about") or []:
                if isinstance(about, dict) and "source" in about:
                    if about["source"] not in sources:
                        self.add("MV-1", rid, rel_path(item, "/hypotheses/%d" % index))
                elif isinstance(about, str) and self.ctx.kind_of(about) == "Episode" and about not in episodes:
                    self.add("MV-1", rid, rel_path(item, "/hypotheses/%d" % index))
        self.check_reading_origin(item)
        self.adoption_ok(item, data, "MV-3")

    def check_practice(self, item):
        data = item.data
        source = data.get("source") or {}
        template = source.get("templateId")
        from_agent = source.get("route") == "from-agent" or self.is_agent(source.get("by")) or \
            self.is_agent(data.get("assertedBy"))
        if template and from_agent:
            lens = self.ctx.lens_doc(source.get("lens")) if source.get("lens") else None
            docs = [lens] if lens else list(self.spec.lenses.values())
            for doc in docs:
                for tool in doc.get("toolkit") or []:
                    if tool.get("id") == template and (tool.get("requiresPractitioner") or not tool.get("agentMayOffer")):
                        self.add("PC-2", item.id, rel_path(item, "/source/templateId"))
        if source.get("route") == "from-agent" and data.get("assertedBy") == "subject":
            status = self.state.status.get(item.id)
            if status is not None and status.admitted_by not in (None, "subject"):
                self.add("PC-1", item.id, rel_path(item, "/source/route"))

    def check_outcome(self, item):
        data = item.data
        rid = item.id
        if data.get("assertedBy") != "subject" and data.get("epistemic") not in (None, "hypothesis"):
            self.add("O-1", rid, rel_path(item, "/epistemic"))
        expected = {"practice": "Practice", "recallCue": "RecallCue", "proposal": "Proposal",
                    "interpretation": "Interpretation", "modelView": "ModelView"}
        for key, value in (data.get("about") or {}).items():
            kind = self.ctx.kind_of(value)
            if kind is not None and kind not in (expected.get(key), "Tombstone"):
                self.add("O-3", rid, rel_path(item, "/about/" + key))
        cue = (data.get("about") or {}).get("recallCue")
        delivery = data.get("delivery") or {}
        if cue and delivery.get("by") and delivery.get("by") not in ("subject", "holder"):
            if not self.recall_grant(delivery["by"], delivery.get("at")):
                self.add("RC-6", rid, rel_path(item, "/delivery/by"))

    def recall_grant(self, agent, when):
        at = model.parse_time(when) if when else self.now
        for grant_item in self.ctx.grants:
            g = grant_item.data
            if g.get("grantee") == agent and "recall" in (g.get("actions") or []) and \
                    "recall-support" in (g.get("purposes") or []) and g.get("effect", "allow") == "allow" and \
                    self.state.grant_status(grant_item.id, at) == "given":
                return True
        return False

    def check_pattern(self, item):
        data = item.data
        rid = item.id
        roots = set()
        for eid in data.get("episodes") or []:
            cursor, seen = eid, set()
            while isinstance(cursor, str) and cursor not in seen:
                seen.add(cursor)
                nxt = (self.ctx.record(cursor) or {}).get("supersedes")
                if not isinstance(nxt, str):
                    break
                cursor = nxt
            roots.add(self.chain_root(eid))
        if len(roots) < 2:
            self.add("PT-1", rid, rel_path(item, "/episodes"))
        if data.get("assertedBy") != "subject":
            alternatives = data.get("alternatives") or []
            if not data.get("grounds") or len(alternatives) < 2 or not data.get("limits") or not any(
                    isinstance(a, dict) and a.get("kind") in NON_PSYCH_ALTERNATIVES for a in alternatives):
                self.add("PT-2", rid, rel_path(item, "/alternatives"))
            if data.get("epistemic") not in (None, "hypothesis", "frame-relative"):
                self.add("PT-2", rid, rel_path(item, "/epistemic"))
        self.check_reading_origin(item)
        self.adoption_ok(item, data, "PT-2")

    def chain_root(self, rid):
        """Collapse supersession chains (both directions) to one representative."""
        members = set([rid])
        changed = True
        while changed:
            changed = False
            for item in self.ctx.items:
                if item.kind != "Episode":
                    continue
                prior = item.data.get("supersedes")
                if item.id in members and isinstance(prior, str) and prior not in members:
                    members.add(prior)
                    changed = True
                if prior in members and item.id not in members:
                    members.add(item.id)
                    changed = True
        return min(members)

    def check_recallcue(self, item):
        data = item.data
        rid = item.id
        for review in self.ctx.reviews:
            r = review.data
            if rid in model.review_targets(r) and r.get("action") in ("admit", "endorse", "partially-endorse",
                                                                       "contest", "resume") and r.get("by") != "subject":
                self.add("RC-1", rid, rel_path(review, "/by"))
        offer = data.get("offer") or {}
        for index, target in enumerate(offer.get("targets") or []):
            cats = self.state.categories(target)
            if ("mental-health" in cats or "trauma-adjacent" in cats or self.state.tier(target) == "special") and \
                    data.get("assertedBy") != "subject":
                self.add("RC-2", rid, rel_path(item, "/offer/targets/%d" % index))
            if self.ctx.kind_of(target) == "Episode" and self.state.recall(target) not in ("ask-each-time", "permitted"):
                self.add("RC-7", rid, rel_path(item, "/offer/targets/%d" % index))
        note = str(offer.get("alternativesNote") or "").lower()
        if offer.get("includeAlternatives") is not True or not note or not any(w in note for w in NON_PSYCH_WORDS):
            self.add("RC-4", rid, rel_path(item, "/offer/alternativesNote"))

    def check_part(self, item):
        if item.data.get("assertedBy") != "subject":
            self.add("P-2", item.id, rel_path(item, "/assertedBy"))

    def check_healthref(self, item):
        data = item.data
        if not set(data.get("categories") or []).intersection({"health", "mental-health"}) or \
                data.get("audience", "named") != "named":
            self.add("HR-2", item.id, rel_path(item, "/categories"))

    # ------------------------------------------------------------ governance
    def check_review(self, item):
        data = item.data
        rid = item.id
        targets = model.review_targets(data)
        tombstoned = dict((i.id, i.data) for i in self.ctx.tombstones)
        action = data.get("action")
        info = self.spec.review_actions.get(action) or {}
        kinds = set()
        at = model.parse_time(data.get("recordedAt"))
        state = self.state_at(at) if at else self.state
        for target in targets:
            if target in tombstoned:
                erased_at = model.parse_time(tombstoned[target].get("erasedAt"))
                if at is None or erased_at is None or at >= erased_at:
                    self.add("RV-4", rid, rel_path(item, "/target"))
                continue
            target_item = self.ctx.by_id.get(target)
            if target_item is None:
                self.add("RV-1", rid, rel_path(item, "/target"))
                continue
            kinds.add(target_item.kind)
            allowed_targets = info.get("targets") or []
            kind_ok = target_item.kind in allowed_targets or (
                target_item.kind in model.CONTENT_KINDS and
                any(t in ("content", "contested", "proposed") for t in allowed_targets))
            if target_item.kind in ("Review", "Event", "Proposal") or not kind_ok:
                self.add("RV-1", rid, rel_path(item, "/target"))
                continue
            if target_item.kind == "Grant":
                if not state.grant_review_allowed(data, target_item):
                    self.add("RV-2", rid, rel_path(item, "/by"))
                continue
            if action == "resolve":
                by = data.get("by")
                who = target_item.data.get("whoDecides")
                if not (by == "subject" or (by == "holder" and who == "holder-policy")):
                    self.add("T1", rid, rel_path(item, "/by"))
                    continue
            if not state.review_allowed(data, target_item):
                admission = action in ("admit", "decline") or (
                    action in ("endorse", "partially-endorse", "contest") and
                    (state.status.get(target) or model.Status()).admission == "proposed")
                by = data.get("by")
                if admission and (by == "holder" or by in self.ctx.stewards):
                    self.add("RA-1", rid, rel_path(item, "/by"))
                else:
                    self.add("RV-2", rid, rel_path(item, "/by"))
            elif action in ("endorse", "partially-endorse", "contest", "admit") and data.get("by") != "subject":
                target_status = state.status.get(target)
                if target_status and target_status.admission == "proposed" and state.subject_only_admission(target_item):
                    self.add("RA-1", rid, rel_path(item, "/by"))
        if len(kinds) > 1:
            self.add("RV-1", rid, rel_path(item, "/target"))
        by = data.get("by")
        if by in self.ctx.stewards and data.get("basis") != "steward-scope":
            self.add("RV-2", rid, rel_path(item, "/basis"))
        if by in self.ctx.parties and by not in self.ctx.stewards and not data.get("underGrant"):
            self.add("RV-2", rid, rel_path(item, "/underGrant"))
        if action == "admit":
            for target in targets:
                for other in self.ctx.reviews:
                    o = other.data
                    if target in model.review_targets(o) and o.get("action") == "retract":
                        t_retract = model.parse_time(o.get("recordedAt"))
                        if t_retract is not None and at is not None and t_retract <= at:
                            self.add("RV-5", rid, rel_path(item, "/action"))

    def check_proposal(self, item):
        data = item.data
        rid = item.id
        gid = data.get("underGrant")
        grant_item = self.ctx.by_id.get(gid) if isinstance(gid, str) else None
        inferred = False
        for index, iid in enumerate(data.get("items") or []):
            target = self.ctx.by_id.get(iid)
            if target is None:
                if iid not in set(i.id for i in self.ctx.tombstones):
                    self.add("PR-1", rid, rel_path(item, "/items/%d" % index))
                continue
            if target.kind == "Tombstone":
                continue
            if target.data.get("assertedBy") != data.get("proposer") or target.data.get("underGrant") != gid:
                self.add("PR-1", rid, rel_path(item, "/items/%d" % index))
            if target.data.get("origin") == "inferred":
                inferred = True
        at = model.parse_time(data.get("recordedAt"))
        ok = grant_item is not None and grant_item.kind == "Grant"
        if ok:
            grant = grant_item.data
            actions = set(grant.get("actions") or [])
            ok = at is not None and self.state.grant_status(gid, at) == "given"
            ok = ok and data.get("purpose") in (grant.get("purposes") or [])
            ok = ok and bool(actions.intersection({"suggest", "write"}))
            ok = ok and grant.get("grantee") == data.get("proposer")
            if inferred:
                ok = ok and "infer" in actions
        if not ok:
            self.add("PR-2", rid, rel_path(item, "/underGrant"))
        for index, request in enumerate(data.get("requests") or []):
            if (request or {}).get("target") not in self.ctx.by_id:
                self.add("PR-4", rid, rel_path(item, "/requests/%d/target" % index))

    def grant_reaches_special(self, grant):
        """GR-1, GR-4, GR-6: a grant reaches special material when a selector names a special category, lens, tier
        or id, or when an include selector matches a record that is special now and names it (R-G3)."""
        includes = (grant.get("scope") or {}).get("include") or []
        for selector in includes:
            if "special" in (selector.get("tiers") or []):
                return True
            for category in selector.get("categories") or []:
                if self.spec.categories_min.get(category) == "special":
                    return True
            for lens_id in selector.get("lenses") or []:
                doc = self.ctx.lens_doc(lens_id)
                if doc is None or (doc.get("defaults") or {}).get("sensitivity") == "special":
                    return True
            for rid in selector.get("ids") or []:
                if self.state.tier(rid) == "special":
                    return True
        for item in self.ctx.content:
            if not isinstance(item.data, dict) or self.state.tier(item.id) != "special":
                continue
            for selector in includes:
                if grants.matches(selector, item, self.state) and grants.names_special(selector, item, self.state):
                    return True
        return False

    def check_grant(self, item):
        data = item.data
        rid = item.id
        constraints = data.get("constraints") or {}
        actions = set(data.get("actions") or [])
        allow = data.get("effect", "allow") == "allow"
        recorded = model.parse_time(data.get("recordedAt"))
        expires = model.parse_time(constraints.get("expiresAt")) if constraints.get("expiresAt") else None
        if expires is None or recorded is None or expires <= recorded:
            self.add("GR-1", rid, rel_path(item, "/constraints/expiresAt"))
        elif allow:
            # R-G10 caps apply to permissions; a refusal (effect deny) may run as long as the person wants.
            limit = "P180D" if ("infer" in actions or self.grant_reaches_special(data)) else "P1Y"
            if expires > model.add_duration(recorded, limit):
                self.add("GR-1", rid, rel_path(item, "/constraints/expiresAt"))
        if "grant" in actions:
            self.add("GR-9", rid, rel_path(item, "/actions"))
        if constraints.get("decisionUse", "deny") not in ("deny", "approval-required"):
            self.add("GR-2", rid, rel_path(item, "/constraints/decisionUse"))
        for key in ("forwarding", "crossContextUse", "delegable"):
            if constraints.get(key, False) is not False:
                self.add("GR-2", rid, rel_path(item, "/constraints/" + key))
        if "open-verbatim" in actions:
            step = data.get("stepUp") or {}
            bound = model.duration_upper_bound(step.get("maxDuration", "PT30M"))
            if step.get("required") is not True or bound is None or bound.total_seconds() > 3600 or \
                    data.get("maxSourceTier") != "verbatim":
                self.add("GR-3", rid, rel_path(item, "/stepUp"))
        legal = (data.get("basis") or {}).get("legal")
        if allow and ("infer" in actions or self.grant_reaches_special(data)):
            if not data.get("purposes") or legal != "explicit-consent":
                self.add("GR-4", rid, rel_path(item, "/basis/legal"))
        grantee = data.get("grantee")
        if grantee not in self.ctx.parties:
            self.add("GR-5", rid, rel_path(item, "/grantee"))
        if allow:
            for index, selector in enumerate((data.get("scope") or {}).get("include") or []):
                if "special" in (selector.get("tiers") or []) and not (
                        selector.get("ids") or selector.get("categories") or selector.get("lenses")):
                    self.add("GR-6", rid, rel_path(item, "/scope/include/%d/tiers" % index))
        else:
            if "actions" in data or "mode" in data:
                self.add("GR-7", rid, rel_path(item, "/effect"))
        grantor = data.get("grantor")
        if grantor not in ("subject", None):
            steward = self.ctx.stewards.get(grantor)
            ok = steward is not None and "grant" in ((steward.get("scope") or {}).get("actions") or [])
            if ok and recorded is not None:
                start, end = model.parse_time(steward.get("validFrom")), model.parse_time(steward.get("validUntil"))
                ok = start is not None and end is not None and start <= recorded < end
            if not ok:
                self.add("GR-8", rid, rel_path(item, "/grantor"))

    def check_tombstone(self, item):
        data = item.data
        allowed = {"kind", "id", "erasedKind", "erasedAt", "erasedBy", "reason"}
        extra = sorted(set(data) - allowed)
        if extra:
            self.add("TB-1", item.id, rel_path(item, "/" + extra[0]))
        erased_at = model.parse_time(data.get("erasedAt")) if isinstance(data.get("erasedAt"), str) else None
        by = data.get("erasedBy")
        if by not in ("subject", "holder"):
            steward = self.ctx.stewards.get(by)
            start = model.parse_time((steward or {}).get("validFrom"))
            end = model.parse_time((steward or {}).get("validUntil"))
            if steward is None or erased_at is None or start is None or end is None or not (start <= erased_at < end):
                self.add("TB-5", item.id, rel_path(item, "/erasedBy"))
        expected_kind = self.spec.collection_kind.get(item.collection)
        if expected_kind and data.get("erasedKind") != expected_kind:
            self.add("TB-5", item.id, rel_path(item, "/erasedKind"))
        if self.ctx.form == "package":
            events = [e.data for e in self.ctx.events if e.data.get("eventType") == "record-erased" and
                      item.id in (e.data.get("records") or [])]
            if not events:
                self.add("TB-4", item.id, rel_path(item, "/id"))
            elif not any(e.get("actor") == by and erased_at is not None and model.parse_time(e.get("at")) is not None
                         and model.parse_time(e.get("at")) <= erased_at for e in events):
                self.add("TB-5", item.id, rel_path(item, "/erasedAt"), level="L2")

    # ---------------------------------------------------------------- events
    def check_events(self):
        events = [e.data for e in self.ctx.events]
        if not events:
            return
        for rule, index in ev.verify_chain(events):
            item = self.ctx.events[index]
            self.add(rule, item.id, rel_path(item, "/seq" if rule == "EV-1" else "/prev"))
        self.check_step_ups()
        self.check_disclosures()
        served = []
        for item in self.ctx.events:
            e = item.data
            if e.get("eventType") in DISCLOSURE_EVENTS:
                served.append(item)
            if e.get("eventType") == "record-erased":
                erased = set(e.get("records") or [])
                recipients = set()
                for prior in served:
                    if prior.order < item.order and erased.intersection(prior.data.get("records") or []):
                        recipients.add(prior.data.get("counterparty"))
                for recipient in sorted(r for r in recipients if r):
                    notified = any(n.data.get("eventType") == "erasure-notice-sent" and
                                   n.data.get("counterparty") == recipient and n.order > item.order and
                                   erased.intersection(n.data.get("records") or [])
                                   for n in self.ctx.events)
                    if not notified:
                        self.add("EV-6", item.id, rel_path(item, "/records"))

    def check_step_ups(self):
        """EV-5 (with SU-1…SU-3): every source-opened is preceded, within the grant's step-up window, by a
        step-up-confirmed for the same grant that covers the opened Sources and was confirmed by the subject (or a
        steward with open-verbatim in scope, never for special material); a special Source is opened at most once
        per step-up; and the grant allows verbatim (open-verbatim, maxSourceTier verbatim, stepUp.required)."""
        grants_by_id = dict((g.id, g.data) for g in self.ctx.grants)
        step_ups = [e for e in self.ctx.events if e.data.get("eventType") == "step-up-confirmed"]
        used = {}
        for item in self.ctx.events:
            e = item.data
            if e.get("eventType") != "source-opened":
                continue
            when = model.parse_time(e.get("at"))
            grant = grants_by_id.get(e.get("grant")) or {}
            step = grant.get("stepUp") or {}
            ok = "open-verbatim" in (grant.get("actions") or []) and grant.get("maxSourceTier") == "verbatim" and \
                step.get("required") is True and e.get("tier") == "verbatim"
            window = model.duration_upper_bound(step.get("maxDuration", "PT30M"))
            opened = set(e.get("records") or [])
            state = self.state_at(when) if when is not None else self.state
            special = set(r for r in opened if state.tier(r) == "special")
            match = None
            for candidate in step_ups:
                s = candidate.data
                at = model.parse_time(s.get("at"))
                if s.get("grant") != e.get("grant") or s.get("outcome", "confirmed") != "confirmed" or \
                        at is None or when is None or at > when or candidate.order > item.order:
                    continue
                if window is not None and when - at > window:
                    continue
                if not opened <= set(s.get("records") or []):
                    continue
                confirmer = s.get("actor")
                if confirmer != "subject":
                    steward = self.ctx.stewards.get(confirmer)
                    in_scope = steward is not None and "open-verbatim" in ((steward.get("scope") or {}).get("actions")
                                                                           or [])
                    if not in_scope or special:
                        continue
                match = candidate
            if match is None:
                ok = False
            elif special:
                key = match.id
                if used.get(key):
                    ok = False
                used[key] = True
            if not ok:
                self.add("EV-5", item.id, rel_path(item, "/eventType"))

    def check_disclosures(self):
        """EV-7 (R-G1, H-1): every disclosure Event names a grant whose grantee is the counterparty, whose status was
        given at ``at`` and whose purposes hold the Event's purpose; every record it names was servable under §12.3
        at ``at``; a stored projection's Event names exactly the records the projection serves."""
        for item in self.ctx.events:
            e = item.data
            kind = e.get("eventType")
            if kind not in DISCLOSURE_EVENTS + ("step-up-confirmed",):
                continue
            if e.get("outcome") not in (None, "served", "confirmed") or e.get("redacted"):
                continue
            when = model.parse_time(e.get("at"))
            grant_item = self.ctx.by_id.get(e.get("grant")) if isinstance(e.get("grant"), str) else None
            grant = grant_item.data if grant_item is not None and grant_item.kind == "Grant" else None
            counterparty = e.get("counterparty") if kind != "step-up-confirmed" else \
                (grant or {}).get("grantee")
            if grant is None or when is None or grant.get("grantee") != counterparty or \
                    e.get("purpose") not in (grant.get("purposes") or []) or \
                    self.state.grant_status(grant_item.id, when) != "given":
                self.add("EV-7", item.id, rel_path(item, "/grant"))
                continue
            state = self.state_at(when)
            tombstones = dict((t.id, model.parse_time(t.data.get("erasedAt"))) for t in self.ctx.tombstones)
            # A record erased after the disclosure can no longer be re-evaluated; EV-6 follows it instead.
            records = [r for r in e.get("records") or [] if isinstance(r, str) and not (
                r in tombstones and tombstones[r] is not None and tombstones[r] > when)]
            if kind in ("source-opened", "step-up-confirmed"):
                for index, rid in enumerate(records):
                    if grants.verbatim_refusal(state, grant, state.by_id.get(rid), counterparty, e.get("purpose"),
                                               when):
                        self.add("EV-7", item.id, rel_path(item, "/records/%d" % index))
                continue
            try:
                served, _mode = grants.evaluate(state, grant, counterparty, e.get("purpose"), when,
                                                own_proposals=True)
            except grants.Denied:
                self.add("EV-7", item.id, rel_path(item, "/grant"))
                continue
            servable = set(i.id for i in served)
            listed = [r for r in e.get("records") or [] if isinstance(r, str)]
            for rid in records:
                if rid not in servable:
                    self.add("EV-7", item.id, rel_path(item, "/records/%d" % listed.index(rid)))
            if kind == "projection-served":
                stored = [doc for doc in self.ctx.projections.values()
                          if isinstance(doc, dict) and doc.get("id") == e.get("message")]
                if stored and sorted(grants.served_id_set(stored[0])) != sorted(listed):
                    self.add("EV-7", item.id, rel_path(item, "/records"))

    # ----------------------------------------------------------- projections
    def check_projections(self):
        for rel, doc in sorted(self.ctx.projections.items()):
            self.check_projection(rel, doc)

    def check_projection(self, rel, doc):
        pid = doc.get("id") if isinstance(doc, dict) else None
        if not isinstance(doc, dict):
            self.add("S-2", None, rel)
            return
        if doc.get("format") != "ohc.projection" or doc.get("specVersion") != "0.1.0-draft":
            self.add("S-1", pid, rel + "#/format")
            return
        detailed = self.spec.validate_detail("urn:ohc:schema:projection:0.1.0-draft", doc)
        errors = [pointer for pointer, _detail in detailed]
        if detailed:
            self.add("S-2", pid, rel + "#" + detailed[0][0], detail=detailed[0][1])
        if doc.get("digest") != grants.projection_digest(doc):
            self.add("PJ-1", pid, rel + "#/digest")
        if self.ctx.form == "package" and not any(
                e.data.get("eventType") == "projection-served" and e.data.get("message") == pid for e in self.ctx.events):
            self.add("EV-4", pid, rel + "#/id")
        if _has_count_key(doc):
            self.add("PJ-3", pid, rel)
        if doc.get("subjectAlias") == self.ctx.subject_id:
            self.add("PJ-6", pid, rel + "#/subjectAlias")
        if errors:
            return
        grant_item = self.ctx.by_id.get(doc.get("grant"))
        grant = grant_item.data if grant_item is not None and grant_item.kind == "Grant" else None
        now = model.parse_time(doc.get("generatedAt"))
        as_of = model.parse_time(doc.get("asOf")) if doc.get("asOf") else None
        ids_by_member = grants.served_ids(doc)
        all_ids = [i for ids in ids_by_member.values() for i in ids]
        if grant is None or now is None:
            self.add("PJ-2", pid, rel + "#/grant")
            return
        state = model.State(self.ctx, as_of or now)
        grant_state = self.state_at(now)
        try:
            grants.check_grant(grant_state, grant, doc.get("grantee"), doc.get("purpose"), now)
        except grants.Denied:
            self.add("PJ-2", pid, rel + "#/grant")
            return
        if grants.MODE_WIDTH.get(doc.get("mode"), 3) > grants.MODE_WIDTH.get(grant.get("mode", "summary"), 2):
            self.add("PJ-2", pid, rel + "#/mode")
            return
        variants = []
        own = doc.get("ownProposals") is True
        for without in (False, True):
            try:
                served, mode = grants.evaluate(state, grant, doc.get("grantee"), doc.get("purpose"), now,
                                               mode=doc.get("mode"), without_interpretations=without,
                                               own_proposals=own)
            except grants.Denied:
                served, mode = [], doc.get("mode")
            variants.append((without, dict((i.id, i) for i in served), mode))
        servable = variants[0][1]
        for member, ids in ids_by_member.items():
            for index, rid in enumerate(ids):
                if rid not in servable:
                    self.add("PJ-2", rid, rel + "#/%s" % member)
        policy = grant.get("interpretations", "subject-endorsed")
        for rid in all_ids:
            item = self.ctx.by_id.get(rid)
            if item is None or item.kind != "Claim":
                continue
            data = item.data
            psych = data.get("facet") in ("state", "declared-value", "disposition", "belief") or \
                "mental-health" in state.categories(rid)
            status = state.status.get(rid) or model.Status()
            if data.get("origin") == "inferred" and psych and policy != "all" and not status.endorsed_by_subject:
                self.add("PJ-4", rid, rel + "#/statements/claims")
        for record in (doc.get("interpretations") or {}).get("tensions") or []:
            tid = record.get("id")
            derived = (doc.get("derived") or {}).get(tid) or {}
            members = (self.ctx.record(tid) or {}).get("between") or []
            if derived.get("contested") or any(m not in servable for m in members):
                self.add("PJ-5", tid, rel + "#/interpretations/tensions")
        for record in (doc.get("links") or {}).get("relations") or []:
            if record.get("from") not in all_ids or record.get("to") not in all_ids:
                self.add("RL-5", record.get("id"), rel + "#/links/relations")
        for record in (doc.get("statements") or {}).get("healthRefs") or []:
            hid = record.get("id")
            names = any(hid in (s.get("ids") or []) for s in (grant.get("scope") or {}).get("include") or [])
            if doc.get("purpose") != "health-coordination" or not names:
                self.add("HR-3", hid, rel + "#/statements/healthRefs")
        if any(f["rule"] in ("PJ-2",) and f["path"].startswith(rel) for f in self.f.items):
            return
        if not self.projection_reproduces(doc, state, grant, variants, now, as_of):
            self.add("PJ-7", pid, rel)

    def projection_reproduces(self, doc, state, grant, variants, now, as_of):
        for absence in doc.get("absences") or []:
            if grants.covers(grant, absence.get("selector") or {}):
                return False
        if doc.get("validUntil") != model.format_time(grants.valid_until(grant, now)):
            stored = model.parse_time(doc.get("validUntil")) if doc.get("validUntil") else None
            if stored != grants.valid_until(grant, now):
                return False
        constraints = grant.get("constraints") or {}
        if (doc.get("obligations") or {}).get("storage") != constraints.get("storage", "session"):
            return False
        if (doc.get("obligations") or {}).get("decisionUse") != constraints.get("decisionUse", "deny"):
            return False  # R-G14: always present, copied from the grant
        served_now = grants.served_ids(doc)
        stored_ids = [i for ids in served_now.values() for i in ids]
        for without, servable, mode in variants:
            if doc.get("interpretations") is not None and without:
                continue
            ok = True
            transformed = []
            for member, ids in served_now.items():
                stored_records = dict((r.get("id"), r) for g, n, _k in grants.MEMBERS if n == member
                                      for r in (doc.get(g) or {}).get(n) or [])
                for rid in ids:
                    item = servable.get(rid)
                    if item is None:
                        ok = False
                        break
                    if item.kind == "Source":
                        expected = grants.serve_source(state, grant, item, b"", [], read_vault=False)
                    else:
                        expected = grants.transform(item, mode)
                    transformed.append((item.kind, expected))
                    if not jcs.equal(grants.strip_holder_keyed(expected), grants.strip_holder_keyed(stored_records[rid])):
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                continue
            expected_ids = [i for i in servable if i in stored_ids]
            if sorted(expected_ids) != sorted(stored_ids):
                continue
            for rid in stored_ids:
                if not jcs.equal(state.derived(rid, as_of or now), (doc.get("derived") or {}).get(rid)):
                    ok = False
            if set((doc.get("derived") or {}).keys()) != set(stored_ids):
                ok = False
            handling = dict((rid, sorted(state.handling(rid))) for rid in stored_ids if state.handling(rid))
            if not jcs.equal(handling, (doc.get("obligations") or {}).get("handling") or {}):
                ok = False
            parties = grants.referenced_parties(self.ctx, transformed)
            if not jcs.equal(parties, doc.get("parties") or []):
                ok = False
            if ok:
                return True
        return False

    # ------------------------------------------------------------------- lock
    def check_lock(self):
        if self.ctx.form != "package":
            return
        lock = self.ctx.lock
        if lock is None:
            return
        errors = self.spec.validate("urn:ohc:schema:lock:0.1.0-draft", lock)
        if errors:
            self.add("S-2", None, "context.lock.json#" + errors[0])
            return
        files = lock.get("files") or {}
        for rel, digest in sorted(files.items()):
            if not model.PATH_RE.match(rel):
                self.add("J-6", None, "context.lock.json#/files")
                continue
            full = os.path.join(self.ctx.dir, rel)
            if not os.path.isfile(full):
                self.add("LK-1", None, "context.lock.json#/files/" + rel.replace("/", "~1"))
                continue
            with open(full, "rb") as handle:
                actual = "sha256:" + hashlib.sha256(handle.read()).hexdigest()
            if actual != digest:
                self.add("LK-1", None, "context.lock.json#/files/" + rel.replace("/", "~1"))
        for rel in self.ctx.package_files():
            if rel == "context.lock.json" or rel.startswith("vault/") or rel.startswith("ext/"):
                continue
            if os.path.basename(rel) in ("README.md", "expected-check.json"):
                continue
            if rel not in files:
                self.add("LK-2", None, rel)
        context = lock.get("context") or {}
        if context.get("id") != self.ctx.manifest.get("id") or context.get("version") != self.ctx.manifest.get("version"):
            self.add("LK-3", None, "context.lock.json#/context")

    # ------------------------------------------------------------------ vault
    def check_vault(self):
        """V-6: after erasure no primary material stays behind. Every vault object is referenced, by file name, from
        the content.sha256 of a Source that is not tombstoned. The checker never opens these files for this."""
        if self.ctx.form != "package" or not self.ctx.vault_files:
            return
        live = set()
        for item in self.ctx.items:
            if item.kind == "Source" and isinstance(item.data, dict):
                sha = (item.data.get("content") or {}).get("sha256")
                if isinstance(sha, str):
                    live.add(sha)
        for rel in self.ctx.vault_files:
            name = os.path.basename(rel).split(".")[0]
            if name not in live:
                self.add("V-6", None, rel)

    # ----------------------------------------------------------------- levels
    def check_levels(self):
        """LV-0: at least one content record, a Claim or an Episode with at least one account (§4.2)."""
        starts = [i for i in self.ctx.items if i.kind == "Claim" or (
            i.kind == "Episode" and isinstance(i.data, dict) and i.data.get("accounts"))]
        if not starts:
            self.add("LV-0", None, self.ctx.manifest_rel + "#/claims")
        if self.ctx.form != "package":
            self.add("LV-2", None, self.ctx.manifest_rel + "#/collections", level="L2")
        else:
            if self.ctx.lock is None:
                self.add("LV-2", None, "context.lock.json", level="L2")
            if not self.ctx.events:
                self.add("LV-2", None, "events.jsonl", level="L2")

    # ----------------------------------------------------------------- examples
    def check_examples(self):
        if not self.example_mode:
            return
        if self.ctx.manifest.get("synthetic") is not True:
            self.add("CX-8", None, self.ctx.manifest_rel + "#/synthetic")
        for item in self.ctx.content:
            if item.data.get("synthetic") is not True:
                self.add("X-1", item.id, rel_path(item, "/synthetic"))
        pattern = re.compile(r"\b(%s)\b" % "|".join(re.escape(n) for n in PERSONAL_NAME_DENY))
        for item in self.ctx.items:
            for pointer in _string_pointers(item.data):
                value = _get_pointer(item.data, pointer)
                if isinstance(value, str) and pattern.search(value):
                    self.add("X-2", item.id, rel_path(item, pointer))
                    break


# Events that disclose record content to a party (§13.1): erasure notices follow them (EV-6), grants cover them (EV-7).
DISCLOSURE_EVENTS = ("projection-served", "answer-served", "export-run", "source-opened")

# A lens with no resolvable descriptor behaves as a stub (LA-6): its results are frame-relative.
STUB_DESCRIPTOR = {"descriptorStatus": "stub", "useLimits": {"crossLensMapping": "not-allowed"}}

COUNT_KEY = re.compile(r"^(?:count|counts|total|totals|withheld|omitted|numberOf[A-Za-z]*)$|(?:Count|Counts|Total)$")


def _has_count_key(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if COUNT_KEY.search(key):
                return True
            if _has_count_key(item):
                return True
    elif isinstance(value, list):
        return any(_has_count_key(v) for v in value)
    return False


def _string_pointers(value, pointer=""):
    out = []
    if isinstance(value, dict):
        for key, item in value.items():
            out.extend(_string_pointers(item, pointer + "/" + key.replace("~", "~0").replace("/", "~1")))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            out.extend(_string_pointers(item, pointer + "/" + str(index)))
    elif isinstance(value, str):
        out.append(pointer)
    return out


def _get_pointer(value, pointer):
    for part in pointer.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


# =================================================================== registry docs
def is_local_lens(lens_id):
    return isinstance(lens_id, str) and lens_id.startswith("urn:ohc:lens:x-")


def is_local_playbook(playbook_id):
    return isinstance(playbook_id, str) and playbook_id.startswith("urn:ohc:playbook:x-")


def check_lens_doc(doc, path, findings, spec, ctx=None):
    rid = doc.get("id")
    errors = spec.validate_detail("urn:ohc:schema:lens:0.1.0-draft", doc)
    if errors:
        findings.add("S-2", rid, path + "#" + errors[0][0], detail=errors[0][1])
    for index, playbook_id in enumerate(doc.get("playbooks") or []):
        # PB-2: a registry descriptor lists registry playbooks; a local one may also list playbooks pinned with it.
        if is_local_lens(rid) and ctx is not None:
            playbook = ctx.playbook_doc(playbook_id)
        else:
            playbook = None if is_local_playbook(playbook_id) else spec.playbook(playbook_id)
        if playbook is None or rid not in (playbook.get("lenses") or []):
            findings.add("PB-2", rid, path + "#/playbooks/%d" % index)
    toolkit = doc.get("toolkit") or []
    for index, tool in enumerate(toolkit):
        if isinstance(tool, dict) and tool.get("requiresPractitioner") and tool.get("agentMayOffer"):
            findings.add("LN-1", rid, path + "#/toolkit/%d" % index)
    if is_local_lens(rid):
        # A local descriptor (LENSES.md §5.1) is always a stub: the registry rules below do not apply, and the
        # stub rules (LN-10, LA-1) hold for every adoption of it.
        for pointer in _string_pointers(doc):
            value = _get_pointer(doc, pointer)
            if isinstance(value, str) and len(value) > 1500:
                findings.add("LN-5", rid, path + "#" + pointer)
        return
    evidence = doc.get("evidence") or {}
    limits = doc.get("useLimits") or {}
    if evidence.get("measurementTier") == "T5" or evidence.get("ontologicalStatus") == "symbolic-frame":
        if limits.get("crossLensMapping") != "not-allowed":
            findings.add("LN-3", rid, path + "#/useLimits/crossLensMapping")
    defaults = doc.get("defaults") or {}
    if doc.get("kind") != "representation" and defaults.get("sensitivity") != "special":
        findings.add("LN-4", rid, path + "#/defaults/sensitivity")
    for pointer in _string_pointers(doc):
        value = _get_pointer(doc, pointer)
        if isinstance(value, str) and len(value) > 1500:
            findings.add("LN-5", rid, path + "#" + pointer)
    if (evidence.get("practiceTier") or {}).get("agentOffered") != "not-assessed":
        findings.add("LN-6", rid, path + "#/evidence/practiceTier/agentOffered")
    if ("constructs" in doc) == ("constructsByReference" in doc):
        findings.add("LN-7", rid, path + "#/constructs")
    marks = (doc.get("ip") or {}).get("marks") or []
    registered = set()
    for index, mark in enumerate(marks):
        if not isinstance(mark, dict):
            continue
        if mark.get("status") == "registered":
            registered.add(mark.get("mark"))
            if mark.get("use") != "avoid" and not mark.get("notice"):
                findings.add("LN-8", rid, path + "#/ip/marks/%d" % index)
    for index, construct in enumerate(doc.get("constructs") or []):
        label = ((construct or {}).get("label") or {}).get("en")
        if label in registered:
            findings.add("LN-8", rid, path + "#/constructs/%d/label" % index)
    for index, mapping_id in enumerate(doc.get("mappings") or []):
        if mapping_id not in spec.mappings:
            findings.add("LN-9", rid, path + "#/mappings/%d" % index)
    if evidence.get("ontologicalStatus") == "contemplative-tradition" and \
            ((doc.get("ip") or {}).get("lineageConsent") or {}).get("status") != "obtained":
        findings.add("LN-11", rid, path + "#/ip/lineageConsent")


def is_construct_of(lens_doc, construct_id):
    """A construct id of a lens: listed in ``constructs`` or matching ``constructsByReference.idPattern``."""
    if not isinstance(lens_doc, dict) or not isinstance(construct_id, str):
        return False
    if any(isinstance(c, dict) and c.get("id") == construct_id for c in lens_doc.get("constructs") or []):
        return True
    pattern = (lens_doc.get("constructsByReference") or {}).get("idPattern")
    if isinstance(pattern, str):
        try:
            return re.fullmatch(pattern, construct_id) is not None
        except re.error:
            return False
    return False


def check_playbook_doc(doc, path, findings, spec, ctx=None):
    """S-2 and PB-1 for a playbook (LENSES.md §2.2): registry, or local (x-) and pinned in a context."""
    rid = doc.get("id") if isinstance(doc, dict) else None
    errors = spec.validate_detail("urn:ohc:schema:playbook:0.1.0-draft", doc)
    if errors:
        findings.add("S-2", rid, path + "#" + errors[0][0], detail=errors[0][1])
        return
    local = is_local_playbook(rid)
    situations = doc.get("situations") or []
    if not local:
        if "ru" not in doc["name"]:
            findings.add("PB-1", rid, path + "#/name")
        if "licence" not in doc:
            findings.add("PB-1", rid, path + "#/licence")
        if doc.get("author") != "OHC editors" and not doc.get("sources"):
            findings.add("PB-1", rid, path + "#/sources")
        for index, situation in enumerate(situations):
            for key in ("when", "use", "watchFor"):
                if key in situation and "ru" not in situation[key]:
                    findings.add("PB-1", rid, path + "#/situations/%d/%s" % (index, key))
    lens_docs = []
    for index, lens_id in enumerate(doc.get("lenses") or []):
        if local and ctx is not None:
            lens_doc = ctx.lens_doc(lens_id)
        else:
            lens_doc = None if is_local_lens(lens_id) else spec.lens(lens_id)
        if lens_doc is None:
            findings.add("PB-1", rid, path + "#/lenses/%d" % index)
        else:
            lens_docs.append(lens_doc)
    offerable = set(t.get("id") for d in lens_docs for t in d.get("toolkit") or []
                    if isinstance(t, dict) and t.get("agentMayOffer") is True)
    seen = set()
    for index, situation in enumerate(situations):
        where = path + "#/situations/%d" % index
        if situation.get("id") in seen:
            findings.add("PB-1", rid, where + "/id")
        seen.add(situation.get("id"))
        use = situation.get("use") or {}
        if "ru" in use and len(use["ru"]) != len(use.get("en") or []):
            findings.add("PB-1", rid, where + "/use")
        for tool_index, tool_id in enumerate(situation.get("toolkit") or []):
            if tool_id not in offerable:
                findings.add("PB-1", rid, where + "/toolkit/%d" % tool_index)
        for result_index, construct_id in enumerate(situation.get("results") or []):
            if not any(is_construct_of(d, construct_id) for d in lens_docs):
                findings.add("PB-1", rid, where + "/results/%d" % result_index)


def check_instrument_doc(doc, path, findings, spec):
    """S-2 and INS-1 for an instrument entry (LENSES.md §3, INSTRUMENT-IMPORT.md §2)."""
    rid = doc.get("id") if isinstance(doc, dict) else None
    errors = spec.validate_detail("urn:ohc:schema:instrument:0.1.0-draft", doc)
    if errors:
        findings.add("S-2", rid, path + "#" + errors[0][0], detail=errors[0][1])
        return
    block = doc.get("import")
    if not isinstance(block, dict):
        return
    lens_doc = spec.lens(doc.get("lens"))
    if lens_doc is None:
        findings.add("INS-1", rid, path + "#/lens")
    seen = set()
    for index, scale in enumerate(block.get("scales") or []):
        if scale in seen or (lens_doc is not None and not is_construct_of(lens_doc, scale)):
            findings.add("INS-1", rid, path + "#/import/scales/%d" % index)
        seen.add(scale)
    kinds = []
    for index, score in enumerate(block.get("scores") or []):
        rng = score.get("range") or []
        if score.get("kind") in kinds or (len(rng) == 2 and not rng[0] < rng[1]):
            findings.add("INS-1", rid, path + "#/import/scores/%d" % index)
        kinds.append(score.get("kind"))
    if len([k for k in kinds if k != "raw"]) > 1:
        findings.add("INS-1", rid, path + "#/import/scores")
    groups = set()
    for index, group in enumerate(block.get("normGroups") or []):
        if group.get("id") in groups or group.get("id") == "unknown":
            findings.add("INS-1", rid, path + "#/import/normGroups/%d/id" % index)
        groups.add(group.get("id"))


def check_lens_markers(spec, findings):
    """LN-13: every F2, U or verify citation is surfaced in LENSES.md with its marker."""
    lenses_md = os.path.join(spec.root, "spec", "LENSES.md")
    if not os.path.isfile(lenses_md):
        findings.add("LN-13", None, "spec/LENSES.md")
        return
    with open(lenses_md, encoding="utf-8") as handle:
        lines = handle.read().splitlines()
    for lens_id, doc in sorted(spec.lenses.items()):
        name = lens_id.rsplit(":", 1)[-1]
        for index, citation in enumerate((doc.get("evidence") or {}).get("citations") or []):
            grade = citation.get("grade")
            if grade not in ("F2", "U", "verify"):
                continue
            marker = "[%s]" % grade
            if not any(("`%s`" % name) in line and marker in line for line in lines):
                findings.add("LN-13", lens_id, "spec/lenses/%s.lens.json#/evidence/citations/%d" % (name, index))


def check_mapping_doc(doc, path, findings, spec):
    rid = doc.get("id")
    errors = spec.validate_detail("urn:ohc:schema:mapping:0.1.0-draft", doc)
    if errors:
        findings.add("S-2", rid, path + "#" + errors[0][0], detail=errors[0][1])
    if doc.get("notIdentity") is not True:
        findings.add("M-1", rid, path + "#/notIdentity")
    if doc.get("chainable") is not False:
        findings.add("M-3", rid, path + "#/chainable")
    if doc.get("bridgeKind") == "lens-lens":
        if doc.get("scope") != "population-level only; never for converting one person's result":
            findings.add("M-2", rid, path + "#/scope")
        statistic = doc.get("statistic") or {}
        if doc.get("relation") == "correlates" and not doc.get("source"):
            findings.add("M-2", rid, path + "#/source")
        elif doc.get("relation") == "correlates" and doc.get("rowStatus") != "unresolved" and not (
                isinstance(statistic.get("r"), (int, float)) and isinstance(statistic.get("n"), int)):
            findings.add("M-2", rid, path + "#/statistic")
        elif doc.get("relation") == "correlates" and doc.get("rowStatus") == "unresolved" and not doc.get("forbiddenUse"):
            findings.add("M-2", rid, path + "#/forbiddenUse")
        for end in ("from", "to"):
            lens = spec.lens((doc.get(end) or {}).get("lens"))
            evidence = (lens or {}).get("evidence") or {}
            if (evidence.get("ontologicalStatus") == "symbolic-frame" or evidence.get("measurementTier") == "T5") \
                    and doc.get("relation") != "no-relation":
                findings.add("M-6", rid, path + "#/relation")


def check_document(path, display, spec):
    """Check one non-context document by its format."""
    findings = Findings()
    try:
        doc = jsonio.load_json(path)
    except jsonio.JsonError as error:
        findings.add({"J-0": "S-2"}.get(error.rule, error.rule), None, display)
        return findings, doc_format(None)
    fmt = doc.get("format") if isinstance(doc, dict) else None
    if fmt == "ohc.lens":
        check_lens_doc(doc, display, findings, spec)
    elif fmt == "ohc.playbook":
        check_playbook_doc(doc, display, findings, spec)
    elif fmt == "ohc.instrument":
        check_instrument_doc(doc, display, findings, spec)
    elif fmt == "ohc.mapping":
        check_mapping_doc(doc, display, findings, spec)
    elif fmt in spec.by_format:
        errors = spec.validate_detail(spec.by_format[fmt], doc)
        if errors:
            findings.add("S-2", doc.get("id") if isinstance(doc, dict) else None, display + "#" + errors[0][0],
                         detail=errors[0][1])
    elif ode.is_binding(doc):
        ode.check_binding(doc, display, spec, findings)
    else:
        findings.add("S-1", None, display + "#/format")
    return findings, doc_format(fmt)


def doc_format(fmt):
    return fmt


# ===================================================================== self-test
def self_test(spec):
    findings = Findings()
    regenerated = spec.regenerate_common()
    if jsonio.dumps_pretty(regenerated) != jsonio.dumps_pretty(spec.common):
        findings.add("S-4", None, "spec/schema/common.schema.json#/$defs")
    for schema_id, schema in spec.schemas.items():
        keys = list(schema.keys())[:4]
        if keys != ["$schema", "$id", "title", "description"] or schema.get("$schema") != \
                "https://json-schema.org/draft/2020-12/schema":
            findings.add("S-2", None, os.path.relpath(spec.schema_paths[schema_id], spec.root))
    for collision in enum_field_collisions(spec):
        findings.add("SELF-1", None, collision)
    for missing in uncited_rules(spec):
        findings.add("SELF-2", missing, "spec/SPECIFICATION.md")
    if not jcs_vectors_pass():
        findings.add("SELF-3", None, "tools/ohclib/jcs.py")
    for undefined in undefined_rules():
        findings.add("SELF-4", undefined, "tools/check.py#RULES")
    for lens_id, doc in sorted(spec.lenses.items()):
        check_lens_doc(doc, os.path.relpath(spec.lens_paths[lens_id], spec.root), findings, spec)
    check_lens_markers(spec, findings)
    for path in sorted(_glob(os.path.join(spec.root, "spec", "mappings", "*", "*.mapping.json"))):
        doc = jsonio.load_json(path)
        check_mapping_doc(doc, os.path.relpath(path, spec.root), findings, spec)
    for path in sorted(_glob(os.path.join(spec.root, "spec", "instruments", "*.instrument.json"))):
        check_instrument_doc(jsonio.load_json(path), os.path.relpath(path, spec.root), findings, spec)
    for path in sorted(_glob(os.path.join(spec.root, "spec", "playbooks", "*.playbook.json"))):
        check_playbook_doc(jsonio.load_json(path), os.path.relpath(path, spec.root), findings, spec)
    for name, catalog in sorted(spec.catalogs.items()):
        errors = spec.validate("urn:ohc:schema:catalog:0.1.0-draft", catalog)
        if errors:
            findings.add("S-2", None, "spec/catalogs/%s.json#%s" % (name, errors[0]))
    glossary_path = os.path.join(spec.root, "spec", "glossary.json")
    if os.path.isfile(glossary_path):
        errors = spec.validate("urn:ohc:schema:glossary:0.1.0-draft", jsonio.load_json(glossary_path))
        if errors:
            findings.add("S-2", None, "spec/glossary.json#" + errors[0])
    return findings


def _glob(pattern):
    import glob

    return glob.glob(pattern)


# Enum values that collide with a sibling field name by design (the field tables of §10.1 and §14.1, and EXCHANGE.md),
# as (schema name, field, value). ``state`` is allow-listed everywhere (D intro).
SELF1_ALLOW = {
    ("source", "sourceKind", "note"), ("source", "maxRelease", "summary"),
    ("projection", "sourceKind", "note"), ("projection", "maxRelease", "summary"),
    ("projection", "tier", "summary"), ("msg-feedback", "feedbackKind", "outcome"),
    ("event", "eventType", "redacted"),
}


def enum_field_collisions(spec):
    """SELF-1: no enum value equals the name of a different field of the same object."""
    out = []

    def resolve(ref, base):
        if ref.startswith("#"):
            ref = base + ref
        doc_id, _sep, fragment = ref.partition("#")
        node = spec.schemas.get(doc_id)
        for part in [p for p in fragment.split("/") if p]:
            if node is None:
                return None
            node = node.get(part) if isinstance(node, dict) else None
        return node

    def values(node, base, depth=0):
        found = set()
        if depth > 8 or not isinstance(node, dict):
            return found
        for v in node.get("enum") or []:
            if isinstance(v, str):
                found.add(v)
        if isinstance(node.get("const"), str):
            found.add(node["const"])
        if "$ref" in node:
            target = resolve(node["$ref"], base)
            ref_base = node["$ref"].partition("#")[0] or base
            found |= values(target, ref_base, depth + 1)
        for key in ("anyOf", "oneOf", "allOf"):
            for sub in node.get(key) or []:
                found |= values(sub, base, depth + 1)
        if node.get("type") == "array":
            found |= values(node.get("items"), base, depth + 1)
        return found

    def walk(node, base, name):
        if isinstance(node, dict):
            props = node.get("properties")
            if isinstance(props, dict):
                for field, sub in props.items():
                    if field in ("format", "kind", "type", "specVersion"):
                        continue
                    for value in sorted(values(sub, base) & set(props)):
                        if value == field or value == "state" or (name, field, value) in SELF1_ALLOW:
                            continue
                        out.append("spec/schema/%s.schema.json#%s=%s" % (name, field, value))
            for value in node.values():
                walk(value, base, name)
        elif isinstance(node, list):
            for value in node:
                walk(value, base, name)

    for schema_id, schema in sorted(spec.schemas.items()):
        name = schema_id.split(":")[3]
        walk(schema, schema_id, name)
    return out


RULE_TOKEN = re.compile(
    r"(?<![A-Za-z0-9-])((?:R-[A-Z]{1,2}\d*[a-z]?)|(?:W-[A-Z]{2,3}\d+)|(?:[A-Z]{1,4}-\d{1,2}[a-z]?)|(?:[IGT]\d)|(?:C3))"
    r"(?![A-Za-z0-9-])")


def uncited_rules(spec):
    """SELF-2: every rule id cited in SPECIFICATION.md is known to the checker."""
    path = os.path.join(spec.root, "spec", "SPECIFICATION.md")
    if not os.path.isfile(path):
        return ["spec/SPECIFICATION.md"]
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    missing = []
    for token in sorted(set(RULE_TOKEN.findall(text))):
        if token in NOT_RULES or token in RULES:
            continue
        missing.append(token)
    return missing


def jcs_vectors_pass():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests"))
    try:
        from jcs_vectors import NUMBER_VECTORS
    except ImportError:
        return False
    for hex_text, expected in NUMBER_VECTORS:
        try:
            if jcs.format_number(jcs.number_from_ieee_hex(hex_text)) != expected:
                return False
        except jcs.JcsError:
            if expected is not None:
                return False
    return True


# ===================================================================== driver
def find_context_target(target):
    if os.path.isdir(target):
        manifest = os.path.join(target, "context.json")
        return manifest if os.path.isfile(manifest) else None
    try:
        doc = jsonio.load_json(target)
    except Exception:
        return None
    return target if isinstance(doc, dict) and doc.get("format") == "ohc.context" else None


def example_dir_for(target):
    """The example directory (``examples/<name>/``) that holds ``expected-check.json`` for a target."""
    base = os.path.abspath(target if os.path.isdir(target) else os.path.dirname(target))
    if os.path.basename(os.path.dirname(base)) == "examples":
        return base
    parent = os.path.dirname(base)
    if os.path.basename(os.path.dirname(parent)) == "examples":
        return parent
    return None


def run_context(target, level=None, strict=False, spec=None):
    spec = spec or vocab.Spec()
    manifest = find_context_target(target)
    try:
        ctx = model.Context(manifest or target, spec)
    except jsonio.JsonError as error:
        findings = Findings()
        findings.add({"J-0": "S-2"}.get(error.rule, error.rule), None, os.path.basename(error.path))
        return build_report(None, findings, level or "L0", strict, [], {"records": 0})
    example_mode = "examples" in os.path.abspath(target).split(os.sep) or \
        str(ctx.manifest.get("id", "")).startswith("urn:ohc:example:")
    checker = ContextChecker(ctx, target, example_mode)
    findings = checker.run()
    declared = (ctx.manifest.get("conformance") or {}).get("level")
    checker.flush_schema_errors(level or declared or "L0")
    defaults = []
    if not declared:
        defaults.append("conformance.level")
    content = [i for i in ctx.content if isinstance(i.data, dict)]
    if any("sensitivity" not in i.data for i in content):
        defaults.append("sensitivity")
    if content:
        defaults.extend(["admission", "endorsement"])
    if any("epistemic" not in i.data for i in content):
        defaults.append("epistemic")
    counts = {"records": len(ctx.items)}
    report = build_report(ctx, findings, level or declared or "L0", strict, defaults, counts)
    report["levelDeclared"] = declared or "L0"
    example_dir = example_dir_for(target)
    if example_dir and not strict and (level is None or level == (declared or "L0")):
        expected_path = os.path.join(example_dir, "expected-check.json")
        try:
            expected = jsonio.load_json(expected_path)
        except Exception:
            expected = None
        if expected is None or not jcs.equal(expected, report):
            findings.add("X-3", None, "expected-check.json")
            report = build_report(ctx, findings, level or declared or "L0", strict, defaults, counts)
            report["levelDeclared"] = declared or "L0"
    return report


def build_report(ctx, findings, target_level, strict, defaults, counts):
    target_index = LEVELS.index(target_level) if target_level in LEVELS else 0
    errors, warnings = [], []
    met = None
    for index, level in enumerate(LEVELS):
        if index > target_index:
            break
        blocking = [f for f in findings.items if f["severity"] == "error" and LEVELS.index(f["level"]) <= index]
        if blocking:
            break
        met = level
    for finding in findings.items:
        if LEVELS.index(finding["level"]) > target_index:
            continue
        entry = {"rule": finding["rule"], "id": finding["id"], "path": finding["path"]}
        if finding.get("detail"):
            entry["detail"] = finding["detail"]
        message, see = explain(finding["rule"])
        if message:
            entry["message"] = message
        entry["see"] = see
        (warnings if finding["severity"] == "warning" else errors).append(entry)
    key = lambda f: (f["rule"], f["id"] or "", f["path"])  # noqa: E731
    errors = _unique(sorted(errors, key=key))
    warnings = _unique(sorted(warnings, key=key))
    modules = ["core"]
    if ctx is not None:
        declared = (ctx.manifest.get("conformance") or {}).get("modules")
        if declared:
            modules = list(declared) if "core" in declared else ["core"] + list(declared)
    valid = not errors and met == target_level and not (strict and warnings)
    report = {
        "valid": valid, "levelDeclared": target_level, "levelMet": met, "modules": modules,
        "errors": errors, "warnings": warnings, "defaultsApplied": [d for d in DEFAULTS_ORDER if d in defaults],
        "counts": counts,
    }
    report.update(REPORT_FLAGS)
    return report


def _unique(items):
    out, seen = [], set()
    for item in items:
        key = (item["rule"], item["id"], item["path"], item.get("detail"))
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def report_for_findings(findings, strict=False):
    report = build_report(None, findings, "L0", strict, [], {"records": 0})
    report["modules"] = []
    return report


def print_human(report, stream):
    status = "VALID" if report["valid"] else "INVALID"
    stream.write("%s · level declared %s · level met %s\n" % (status, report.get("levelDeclared"),
                                                            report.get("levelMet")))
    for label, group in (("ERROR  ", report["errors"]), ("WARNING", report["warnings"])):
        for finding in group:
            stream.write("%s %-8s %-12s %s\n" % (label, finding["rule"], finding["id"] or "-", finding["path"]))
            if finding.get("detail"):
                stream.write("        %s\n" % finding["detail"])
            if finding.get("message"):
                stream.write("        %s\n" % finding["message"])
            if finding.get("see"):
                stream.write("        see %s\n" % finding["see"])
    stream.write("Not established by this check: truth of content, consent, endorsement authenticity, runtime behaviour.\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check Open Human Context files (read-only).")
    parser.add_argument("target", nargs="?")
    parser.add_argument("--level", choices=LEVELS)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--release", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--gen-enums", action="store_true")
    parser.add_argument("--registry", action="append", default=[],
                        help="an extra registry directory with lenses/, instruments/, playbooks/ or mappings/ "
                             "(repeatable); its documents resolve like catalog entries")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    spec = vocab.Spec(registries=args.registry)
    if args.gen_enums:
        regenerated = spec.regenerate_common()
        path = spec.schema_paths[vocab.COMMON_ID]
        if jsonio.dumps_pretty(regenerated) != jsonio.dumps_pretty(spec.common):
            jsonio.write_pretty(path, regenerated)
            sys.stdout.write("regenerated vocabulary $defs in spec/schema/common.schema.json\n")
        else:
            sys.stdout.write("vocabulary $defs already match the catalogs\n")
        return 0
    if args.self_test:
        report = report_for_findings(self_test(spec), args.strict)
    elif args.release:
        import build_release_manifest

        root = os.path.abspath(args.target or spec.root)
        report = report_for_findings(build_release_manifest.release_findings(root, Findings), args.strict)
    else:
        if not args.target or not os.path.exists(args.target):
            parser.print_usage(sys.stderr)
            return 2
        if find_context_target(args.target):
            report = run_context(args.target, args.level, args.strict, spec)
        elif os.path.isdir(args.target):
            findings = Findings()
            for name in sorted(os.listdir(args.target)):
                if name.endswith(".json"):
                    sub, _fmt = check_document(os.path.join(args.target, name), name, spec)
                    findings.items.extend(sub.items)
            report = report_for_findings(findings, args.strict)
        else:
            findings, _fmt = check_document(args.target, os.path.basename(args.target), spec)
            report = report_for_findings(findings, args.strict)
    if args.json:
        sys.stdout.write(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    else:
        print_human(report, sys.stdout)
        if args.self_test:
            normative = sorted(r for r, (_lvl, how) in RULES.items()
                               if how == "normative" and r not in ALIASES_EXPLAINED)
            sys.stdout.write("Not machine-checkable (normative only): %s\n" % ", ".join(normative))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
