"""GUM binding (bindings/GUM.md, bindings/MCP.md) and the assessment import, against the Kofi example."""

import copy
import json
import os
import re
import shutil
import sqlite3
import tempfile
import unittest

import helpers

import convert_gum
import import_assessment
from ohclib import jsonio, model
from ohclib.package import Package

KOFI = os.path.join(helpers.repo_root(), "examples", "kofi-gum-ode")
SNAP1 = os.path.join(KOFI, "fixtures", "gum-snapshot-1.json")
SNAP2 = os.path.join(KOFI, "fixtures", "gum-snapshot-2.json")
AT1 = "2026-09-28T10:05:00Z"
AT2 = "2026-10-05T10:05:00Z"


def records(directory, files=("claims", "sources", "reviews", "assessments", "lens-adoptions", "grants")):
    out = {}
    for name in files:
        path = os.path.join(directory, "records", name + ".jsonl")
        if os.path.isfile(path):
            for _n, record in jsonio.load_jsonl(path):
                out[record["id"]] = record
    return out


def without_run(record):
    record = copy.deepcopy(record)
    (record.get("importedFrom") or {}).pop("run", None)
    return record


class Gum(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = jsonio.load_json(os.path.join(KOFI, "importer-config.json"))
        cls.kofi = records(os.path.join(KOFI, "context"))

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ohc-gum-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def import1(self, name="one"):
        out = os.path.join(self.tmp, name)
        convert_gum.run_import(SNAP1, self.config, out, at=AT1, seed="test")
        return out

    def add_gum_grant(self, directory):
        package = Package(directory, helpers.spec())
        grant = dict(self.kofi["g-04"])
        package.add("Grant", grant)
        package.append_event({"at": grant["recordedAt"], "eventType": "grant-given", "actor": "subject",
                              "counterparty": "a-gum", "grant": "g-04", "records": ["g-04"]}, seed="test")
        package.save(grant["recordedAt"])

    def test_import_field_by_field(self):
        out = self.import1()
        imported = records(out)
        self.assertEqual(len([r for r in imported.values() if r["kind"] == "Source"]), 6)
        self.assertEqual(len([r for r in imported.values() if r["kind"] == "Claim"]), 5)
        for rid, record in imported.items():
            with self.subTest(record=rid):
                self.assertEqual(without_run(record), without_run(self.kofi[rid]))
        focus = [r for r in imported.values() if r.get("text") == "Kofi plans his week around long focus blocks."][0]
        self.assertNotIn("confidence", focus)
        for record in imported.values():
            self.assertNotIn("capturedAt", record)
            self.assertEqual(record["recordedAt"], AT1)
        manifest = jsonio.load_json(os.path.join(out, "context.json"))
        self.assertEqual(manifest["subject"]["id"], self.config["subjectId"])
        report = helpers.run_check(out)
        self.assertTrue(report["valid"], report["errors"])

    def test_digest_only_keeps_no_vault(self):
        out = os.path.join(self.tmp, "digest")
        convert_gum.run_import(SNAP1, dict(self.config, digestOnly=True), out, at=AT1, seed="test")
        self.assertFalse(os.path.isdir(os.path.join(out, "vault")))
        for record in records(out).values():
            if record["kind"] == "Source":
                self.assertIn("uri", record["content"]["locator"])
                self.assertEqual(record["maxRelease"], "index")

    def test_affect_from_screen_is_refused(self):
        """R-X4: an affect proposition resting on screen observations is never imported, whatever its label."""
        first = self.import1()
        out = os.path.join(self.tmp, "two")
        package = convert_gum.run_import(SNAP2, self.config, out, previous=first, at=AT2, seed="test")
        self.assertEqual(package.refused, 1)
        self.assertFalse([r for r in records(out).values() if "stress" in (r.get("text") or "")])
        self.assertNotIn(convert_gum.proposition_id(self.config["gumInstanceId"], 7), set(self.kofi))
        report = helpers.run_check(out)
        self.assertTrue(report["valid"], report["errors"])

    def test_quarantine(self):
        """R-X3: an affect proposition that does not rest on behavioural signals is quarantined on import."""
        snapshot = jsonio.load_json(SNAP2)
        snapshot["observation_proposition"] = [row for row in snapshot["observation_proposition"]
                                               if row["proposition_id"] != 7] + [{"observation_id": 6,
                                                                                  "proposition_id": 7}]
        path = os.path.join(self.tmp, "snap2-calendar.json")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(snapshot))
        first = self.import1()
        out = os.path.join(self.tmp, "two")
        package = convert_gum.run_import(path, self.config, out, previous=first, at=AT2, seed="test")
        self.assertEqual(package.refused, 0)
        stress = [r for r in records(out).values() if "stress" in (r.get("text") or "")][0]
        self.assertEqual(stress["sensitivity"], "special")
        self.assertEqual(stress["categories"], ["mental-health"])
        self.assertEqual(stress["handling"], ["no-infer", "person-only"])
        self.assertTrue(convert_gum.quarantined({"text": "Feels anxious before calls."}))
        self.assertFalse(convert_gum.quarantined({"text": "Avoids calls on Fridays."}))
        report = helpers.run_check(out)
        self.assertTrue(report["valid"], report["errors"])

    def test_lineage(self):
        first = self.import1()
        self.add_gum_grant(first)
        out = os.path.join(self.tmp, "two")
        convert_gum.run_import(SNAP2, self.config, out, previous=first, at=AT2, seed="test")
        before, after = records(first), records(out)
        self.assertTrue(set(before).issubset(after), "nothing is deleted")
        revised = [r for r in after.values() if r.get("supersedes")][0]
        self.assertEqual(without_run(revised), without_run(self.kofi[revised["id"]]))
        self.assertTrue(revised["ext"]["gum.import"]["inferredLineage"])
        retracts = [r for r in after.values() if r.get("kind") == "Review" and r.get("action") == "retract"]
        self.assertEqual([(r["target"], r["by"], r["underGrant"]) for r in retracts],
                         [(self.kofi["rv-09"]["target"], "a-gum", "g-04")])
        report = helpers.run_check(out)
        self.assertTrue(report["valid"], report["errors"])
        events = [e for _n, e in jsonio.load_jsonl(os.path.join(out, "events.jsonl"))]
        self.assertEqual([e["eventType"] for e in events], ["import-run", "grant-given", "import-run"])
        for record in after.values():
            if record.get("importedFrom", {}).get("importedAt") == AT2:
                self.assertEqual(record["importedFrom"]["run"], events[-1]["id"])

    def test_gum_roundtrip_admitted_lossless(self):
        """GUM -> OHC -> GUM (Mode B) returns every column of each admitted proposition that passes the export
        filter; OHC -> GUM -> OHC restores ids, text, origin and dates."""
        out = self.import1()
        self.add_gum_grant(out)
        package = Package(out, helpers.spec())
        for index, record in enumerate(sorted(package.records("claims"), key=lambda r: r["id"]), start=1):
            package.add("Review", {"action": "endorse", "by": "subject", "id": "rv-%02d" % index, "kind": "Review",
                                   "recordedAt": "2026-10-02T08:00:00Z", "target": record["id"]})
        package.save("2026-10-02T08:00:00Z")
        export_dir = os.path.join(self.tmp, "export")
        document, sidecar = convert_gum.run_export(out, "g-04", "B", export_dir, at="2026-10-03T08:00:00Z",
                                                   no_event=True)
        original = dict((p["id"], p) for p in jsonio.load_json(SNAP1)["propositions"])
        exported = dict((p["id"], p) for p in document["propositions"])
        self.assertEqual(exported, original)
        self.assertEqual(sorted(line["gumPropositionId"] for line in sidecar), sorted(original))
        # OHC -> GUM -> OHC, with the example's export
        kofi_doc = jsonio.load_json(os.path.join(KOFI, "gum-export", "propositions.json"))
        kofi_sidecar = [obj for _n, obj in jsonio.load_jsonl(os.path.join(KOFI, "gum-export", "sidecar.jsonl"))]
        restored = dict((r["id"], r) for r in convert_gum.import_back(kofi_doc, kofi_sidecar))
        for rid in ("c-01", "c-02"):
            claim = self.kofi[rid]
            self.assertEqual(restored[rid]["text"], claim["text"])
            self.assertEqual(restored[rid]["origin"], claim["origin"])
            self.assertEqual(restored[rid]["created"], claim["recordedAt"])

    def test_gum_roundtrip_does_not_return_refused_or_withheld(self):
        """The second snapshot's affect proposition (7) never comes back: refused on import (R-X4)."""
        first = self.import1()
        self.add_gum_grant(first)
        out = os.path.join(self.tmp, "two")
        convert_gum.run_import(SNAP2, self.config, out, previous=first, at=AT2, seed="test")
        package = Package(out, helpers.spec())
        for index, record in enumerate(sorted(package.records("claims"), key=lambda r: r["id"]), start=1):
            package.add("Review", {"action": "endorse", "by": "subject", "id": "rv-%02d" % (50 + index),
                                   "kind": "Review", "recordedAt": "2026-10-06T08:00:00Z", "target": record["id"]})
        package.save("2026-10-06T08:00:00Z")
        document, _sidecar = convert_gum.run_export(out, "g-04", "B", os.path.join(self.tmp, "export"),
                                                    at="2026-10-07T08:00:00Z", no_event=True)
        exported = set(p["id"] for p in document["propositions"])
        self.assertNotIn(7, exported)
        self.assertIn(6, exported)

    def test_sqlite_naive_timestamps_roundtrip(self):
        """A GUM SQLite store keeps naive timestamps with fractional seconds; Mode B returns them verbatim."""
        snapshot = jsonio.load_json(SNAP1)
        path = os.path.join(self.tmp, "gum.sqlite")
        connection = sqlite3.connect(path)
        try:
            connection.execute("CREATE TABLE observations (id INTEGER PRIMARY KEY, observer_name TEXT, content TEXT, "
                               "content_type TEXT, created_at TEXT, updated_at TEXT)")
            connection.execute("CREATE TABLE propositions (id INTEGER PRIMARY KEY, text TEXT, reasoning TEXT, "
                               "confidence INTEGER, decay INTEGER, created_at TEXT, updated_at TEXT, "
                               "revision_group TEXT, version INTEGER)")
            connection.execute("CREATE TABLE observation_proposition (observation_id INTEGER, proposition_id INTEGER)")

            def naive(value):
                return value.replace("T", " ").replace("Z", ".123456") if value else value

            for o in snapshot["observations"]:
                connection.execute("INSERT INTO observations VALUES (?, ?, ?, ?, ?, ?)", (
                    o["id"], o["observer_name"], o["content"], o["content_type"], naive(o.get("created_at")),
                    naive(o.get("updated_at"))))
            for p in snapshot["propositions"]:
                connection.execute("INSERT INTO propositions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                    p["id"], p["text"], p.get("reasoning"), p.get("confidence"), p.get("decay"),
                    naive(p.get("created_at")), naive(p.get("updated_at")), p.get("revision_group"), p.get("version")))
            for row in snapshot["observation_proposition"]:
                connection.execute("INSERT INTO observation_proposition VALUES (?, ?)",
                                   (row["observation_id"], row["proposition_id"]))
            connection.commit()
        finally:
            connection.close()
        out = os.path.join(self.tmp, "sqlite")
        convert_gum.run_import(path, self.config, out, at=AT1, seed="test")
        self.add_gum_grant(out)
        package = Package(out, helpers.spec())
        for index, record in enumerate(sorted(package.records("claims"), key=lambda r: r["id"]), start=1):
            package.add("Review", {"action": "endorse", "by": "subject", "id": "rv-%02d" % index, "kind": "Review",
                                   "recordedAt": "2026-10-02T08:00:00Z", "target": record["id"]})
        package.save("2026-10-02T08:00:00Z")
        document, _sidecar = convert_gum.run_export(out, "g-04", "B", os.path.join(self.tmp, "export"),
                                                    at="2026-10-03T08:00:00Z", no_event=True,
                                                    holder_key=b"a-test-holder-key")
        self.assertTrue(document["propositions"])
        stored = dict((p["id"], p) for p in snapshot["propositions"])
        for row in document["propositions"]:
            self.assertEqual(row["created_at"], naive(stored[row["id"]]["created_at"]))
            self.assertEqual(row["updated_at"], naive(stored[row["id"]]["updated_at"]))

    def test_mode_b_export_matches_example(self):
        work = os.path.join(self.tmp, "kofi")
        shutil.copytree(os.path.join(KOFI, "context"), work)
        out = os.path.join(self.tmp, "export")
        convert_gum.run_export(work, "g-04", "B", out, at="2026-10-08T12:00:00Z", no_event=True)
        for name in ("propositions.json", "sidecar.jsonl"):
            with open(os.path.join(out, name), "rb") as mine, open(os.path.join(KOFI, "gum-export", name), "rb") as ex:
                self.assertEqual(mine.read(), ex.read(), name)
        exported = jsonio.load_json(os.path.join(out, "propositions.json"))["propositions"]
        texts = [p["text"] for p in exported]
        self.assertNotIn("Kofi is under heavy stress in deadline weeks.", texts)
        self.assertNotIn("Kofi often works late at night.", texts)

    def test_gumcp_output_format(self):
        """gumcp's block layout (MCP.md): Confidence only when served; Supporting Observations only with excerpts;
        gumcp's no-results sentence when a valid grant matches nothing; "" without a caller Party or grant."""
        ctx = model.Context(os.path.join(KOFI, "context"), helpers.spec())
        self.assertEqual(convert_gum.get_user_context(ctx, caller=None, grant_id="g-04"), "")
        self.assertEqual(convert_gum.get_user_context(ctx, caller="a-gum", grant_id=None), "")
        self.assertEqual(convert_gum.get_user_context(ctx, caller="a-01", grant_id="g-03", query="calls"), "")
        output = convert_gum.get_user_context(ctx, caller="a-gum", grant_id="g-04", query="calls on Fridays")
        blocks = output.split("\n\n")
        self.assertTrue(1 <= len(blocks) <= 3)
        for block in blocks:
            lines = block.split("\n")
            self.assertTrue(lines[0].startswith("• "))
            self.assertTrue(lines[1].startswith("  Reasoning: "), lines[1])
            score = [line for line in lines if line.startswith("  Relevance Score: ")]
            self.assertEqual(len(score), 1)
            self.assertRegex(score[0], r"^  Relevance Score: (0|1)\.\d\d$")
            self.assertFalse([line for line in lines if "n/a" in line])
            self.assertFalse([line for line in lines if line.startswith("  Supporting Observations")])
            for line in lines:
                if line.startswith("  Confidence: "):
                    self.assertRegex(line, r"^  Confidence: \d+$")
        declared = [b for b in blocks if "Declared by the person." in b]
        for block in declared:
            self.assertFalse(block.startswith("• Kofi "), block)
        self.assertNotIn(ctx.subject_id, output)
        self.assertIsNone(re.search(r"\b(?:c|src|as|la|rv|e)-[0-9a-f]{2}", output))
        self.assertNotIn("stress", output)
        nothing = convert_gum.get_user_context(ctx, caller="a-gum", grant_id="g-04", query="x",
                                               start_hh_mm_ago="00:01")
        self.assertEqual(nothing, convert_gum.NO_RESULTS)

    def test_gumcp_summary_mode_withholds_reasoning(self):
        """privacy: in summary mode the tool prints no reasoning and no confidence."""
        work = os.path.join(self.tmp, "kofi")
        shutil.copytree(os.path.join(KOFI, "context"), work)
        path = os.path.join(work, "records", "grants.jsonl")
        lines = []
        for _n, grant in jsonio.load_jsonl(path):
            if grant["id"] == "g-04":
                grant["mode"] = "summary"
            lines.append(grant)
        jsonio.write_jsonl(path, lines)
        ctx = model.Context(work, helpers.spec())
        output = convert_gum.get_user_context(ctx, caller="a-gum", grant_id="g-04", query="calls on Fridays")
        self.assertNotIn("Confidence:", output)
        for block in output.split("\n\n"):
            reasoning = block.split("\n")[1]
            self.assertIn(reasoning, ("  Reasoning: [withheld]", "  Reasoning: Declared by the person."))

    def test_import_assessment_reproduces_example(self):
        out = self.import1()
        result = import_assessment.run_import(
            os.path.join(KOFI, "fixtures", "ipip-neo-120-results.json"), out, "urn:ohc:lens:big-five",
            variant="5-domain-30-facet", at="2026-09-29T19:00:00Z", adopt=True, source_id="src-11",
            assessment_id="as-01", adoption_id="la-01", seed="test")
        self.assertEqual(result, {"source": "src-11", "assessment": "as-01", "adoption": "la-01"})
        mine = records(out)
        for rid in ("src-11", "as-01", "la-01"):
            self.assertEqual(without_run(mine[rid]), without_run(self.kofi[rid]), rid)
        self.assertTrue(helpers.run_check(out)["valid"])

    def test_import_assessment_refuses_never_fields(self):
        out = self.import1()
        data = jsonio.load_json(os.path.join(KOFI, "fixtures", "ipip-neo-120-results.json"))
        data["itemResponses"] = [3, 4, 5]
        path = os.path.join(self.tmp, "results.json")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(data))
        with self.assertRaises(import_assessment.Refused):
            import_assessment.run_import(path, out, "urn:ohc:lens:big-five")
        with self.assertRaises(import_assessment.Refused):
            import_assessment.run_import(os.path.join(KOFI, "fixtures", "ipip-neo-120-results.json"), out,
                                         "urn:ohc:lens:big-five", mode="agent-inference")
        self.assertNotIn("as-01", records(out))


if __name__ == "__main__":
    unittest.main()
