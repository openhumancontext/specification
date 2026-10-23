"""The import library (INSTRUMENT-IMPORT.md): a filled draft or a transcript becomes one imported result per
instrument that passes IMP-1...IMP-5 and cites the person's report in their vault; the scorer route keeps working with
the defects of R-026 fixed. Synthetic people and numbers only."""

import copy
import hashlib
import io
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout

import helpers
import importkit
from importkit import AT, BFI2, HEXACO_PI

import check
import import_assessment
from import_assessment import Refused
from ohclib import jsonio, model, vocab
from ohclib.package import Package


class ImportModule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ohc-import-")
        self.spec = importkit.write_registry(self.tmp)
        self.pkg = importkit.new_package(os.path.join(self.tmp, "ctx"), self.spec)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def check(self, path=None):
        return check.run_context(path or self.pkg, spec=self.spec)

    def bring(self, drafts, at=AT, **kw):
        return import_assessment.import_result(self.pkg, drafts, at, spec=self.spec, seed="t", synthetic=True, **kw)

    def record(self, rid):
        return Package(self.pkg, self.spec).record(rid)

    # ------------------------------------------------------------ the draft
    def test_template_follows_the_import_block(self):
        draft = import_assessment.template(self.spec, BFI2)
        self.assertEqual(draft["instrument"], BFI2)
        self.assertEqual(draft["instrumentVersion"], "0.2.0")
        self.assertEqual([s["scale"] for s in draft["scores"]], importkit.BLOCKS[BFI2]["scales"])
        self.assertEqual(draft["scores"][1], {"scale": "big-five/C", "label": "Conscientiousness", "raw": None})
        self.assertIsNone(draft["administeredAt"])
        hexaco = import_assessment.template(self.spec, HEXACO_PI)
        self.assertEqual(set(hexaco["scores"][0]), {"scale", "label", "percentile"})
        with self.assertRaises(Refused):
            import_assessment.template(self.spec, "urn:ohc:instrument:neo-pi-3")  # no import block (IMP-2)

    def test_template_on_the_command_line(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = import_assessment.main(["template", "--instrument", BFI2, "--registry",
                                           os.path.join(self.tmp, "registry")])
        self.assertEqual(code, 0)
        self.assertEqual(jsonio.loads_strict(out.getvalue(), "-")["instrument"], BFI2)

    # ------------------------------------------------------------ one imported result
    def test_imported_result_passes_the_module_rules(self):
        report = importkit.write_report(self.tmp)
        result = self.bring([importkit.bfi_draft(self.spec)], report_path=report)
        self.assertEqual(result["assessments"], ["as-01"])
        record = self.record("as-01")
        self.assertEqual(record["importedFrom"]["system"], BFI2)
        self.assertEqual(record["importedFrom"]["systemVersion"], "0.2.0")
        self.assertEqual(record["origin"], "imported")
        self.assertEqual(record["recordedBy"], "subject")
        self.assertEqual(record["assessedBy"], "subject")
        self.assertEqual(record["formulatedAt"], "2026-09-14T00:00:00Z")  # IMP-5
        self.assertEqual(record["sensitivity"], "special")  # AR-5
        self.assertNotIn("useLimits", record)
        self.assertEqual(record["results"][0], {"construct": "big-five/O", "label": "Openness", "raw": 3.6,
                                                "type": "dimension-score"})
        package = Package(self.pkg, self.spec)
        party = [p for p in package.manifest["parties"] if p["id"] == record["assertedBy"]][0]
        self.assertEqual(party, {"id": "o-01", "partyKind": "organization", "label": "Report scorer",
                                 "uri": "urn:ohc:scorer:bfi-2-report"})
        source = package.record(record["source"])
        self.assertEqual(source["sourceKind"], "instrument-report")
        self.assertEqual(source["content"]["mediaType"], "application/pdf")
        with open(report, "rb") as handle:
            body = handle.read()
        self.assertEqual(source["content"]["sha256"], hashlib.sha256(body).hexdigest())
        with open(os.path.join(self.pkg, source["content"]["locator"]["vaultPath"]), "rb") as handle:
            self.assertEqual(handle.read(), body)  # the report stays the person's, in their vault (V-0)
        self.assertTrue(set(record["categories"]) <= set(source["categories"]))  # IMP-4
        modules = package.manifest["conformance"]["modules"]
        self.assertIn("instrument-import", modules)  # IMP-1
        self.assertIn("lenses", modules)
        report_ = self.check()
        self.assertTrue(report_["valid"], report_["errors"])
        self.assertEqual(report_["warnings"], [])
        self.assertEqual(report_["levelMet"], "L2")
        state = model.State(model.Context(self.pkg, self.spec))
        self.assertEqual(state.status["as-01"].admission, "proposed")  # until the person decides (R-A1)

    def test_descriptor_and_playbooks_are_pinned(self):
        result = self.bring([importkit.bfi_draft(self.spec)])
        self.assertEqual(result["pinned"], ["lenses/big-five@0.2.0.lens.json",
                                            "lenses/big-five-basic@0.1.0.playbook.json"])
        manifest = jsonio.load_json(os.path.join(self.pkg, "context.json"))
        for member, rel in (("lenses", result["pinned"][0]), ("playbooks", result["pinned"][1])):
            with open(os.path.join(self.pkg, rel), "rb") as handle:
                digest = hashlib.sha256(handle.read()).hexdigest()
            self.assertIn(digest, [p.get("sha256") for p in manifest[member]])

    def test_scorer_party_is_reused_only_by_uri(self):
        package = Package(self.pkg, self.spec)
        package.ensure_party({"id": "o-01", "partyKind": "organization", "label": "Report scorer",
                              "uri": "urn:ohc:scorer:someone-else"})
        package.save("2026-09-15T09:06:00Z")
        self.bring([importkit.bfi_draft(self.spec)])
        self.assertEqual(self.record("as-01")["assertedBy"], "o-02")
        self.bring([importkit.bfi_draft(self.spec, taken="2026-10-01", **{"big-five/C": 4.0})], at="2026-10-12T10:00:00Z")
        self.assertEqual(self.record("as-02")["assertedBy"], "o-02")
        self.assertTrue(self.check()["valid"])

    def test_two_instruments_two_records_one_run(self):
        result = self.bring([importkit.bfi_draft(self.spec), importkit.hexaco_draft(self.spec)])
        self.assertEqual(result["assessments"], ["as-01", "as-02"])
        hexaco = self.record("as-02")
        self.assertEqual(hexaco["results"][0]["standardized"], {"type": "percentile", "value": 61})
        self.assertEqual(hexaco["normGroup"], {"id": "test-norms"})
        events = Package(self.pkg, self.spec).events
        self.assertEqual([e["eventType"] for e in events], ["import-run"])
        self.assertTrue(self.check()["valid"])
        with self.assertRaises(Refused):  # one report per scorer
            self.bring([importkit.bfi_draft(self.spec, taken="2026-10-02"), importkit.hexaco_draft(self.spec,
                                                                                                   taken="2026-10-02")],
                       report_path=importkit.write_report(self.tmp))

    def test_proprietary_scoring_is_flagged(self):
        path = os.path.join(self.tmp, "registry", "instruments", "hexaco-pi-r.instrument.json")
        doc = jsonio.load_json(path)
        doc["scoring"] = "proprietary"
        jsonio.write_pretty(path, doc)
        spec = vocab.Spec(registries=[os.path.join(self.tmp, "registry")])
        import_assessment.import_result(self.pkg, [importkit.hexaco_draft(spec)], AT, spec=spec, synthetic=True)
        self.assertEqual(self.record("as-01")["validityFlags"], ["vendor-algorithm-undisclosed"])
        self.assertTrue(check.run_context(self.pkg, spec=spec)["valid"])

    # ------------------------------------------------------------ refusals
    def test_blank_stays_blank(self):
        draft = importkit.bfi_draft(self.spec, **{"big-five/C": 4.2})
        self.bring([draft])
        self.assertEqual([r["construct"] for r in self.record("as-01")["results"]], ["big-five/C"])
        empty = import_assessment.template(self.spec, BFI2)
        empty["administeredAt"] = "2026-09-01"
        with self.assertRaises(Refused):
            self.bring([empty])

    def test_values_follow_the_block(self):
        cases = []
        draft = importkit.bfi_draft(self.spec, **{"big-five/C": 6})
        cases.append(draft)  # out of range
        draft = importkit.hexaco_draft(self.spec, **{"hexaco/C": 74.5})
        cases.append(draft)  # not an integer percentile
        draft = importkit.bfi_draft(self.spec)
        draft["scores"][0]["percentile"] = 50
        cases.append(draft)  # a kind the block does not list
        draft = importkit.bfi_draft(self.spec)
        draft["scores"].append({"scale": "big-five/C/order", "label": "Order", "raw": 3})
        cases.append(draft)  # a scale outside the block
        draft = importkit.hexaco_draft(self.spec)
        draft["normGroup"] = "other-norms"
        cases.append(draft)
        draft = importkit.bfi_draft(self.spec)
        draft["instrumentVersion"] = "0.1.0"
        cases.append(draft)  # made for another version (W-IMP2)
        for index, case in enumerate(cases):
            with self.assertRaises(Refused, msg=str(index)):
                self.bring([case])
        self.assertIsNone(self.record("as-01"))

    def test_report_text_and_unknown_fields_are_refused(self):
        for extra in ({"interpretation": "x"}, {"summary": "x"}):
            draft = importkit.bfi_draft(self.spec)
            draft.update(extra)
            with self.assertRaises(Refused) as caught:
                self.bring([draft])
            self.assertNotIn("x\"", str(caught.exception))  # names the field, never its value
        draft = importkit.bfi_draft(self.spec)
        draft["scores"][0]["note"] = "x"
        with self.assertRaises(Refused):
            self.bring([draft])

    def test_dates(self):
        draft = importkit.bfi_draft(self.spec)
        draft["administeredAt"] = None
        with self.assertRaises(Refused):
            self.bring([draft])
        with self.assertRaises(Refused):  # taken after it was recorded (IMP-5)
            self.bring([importkit.bfi_draft(self.spec, taken="2026-10-13")])

    def test_duplicate_is_refused_and_correction_supersedes(self):
        self.bring([importkit.bfi_draft(self.spec)])
        with self.assertRaises(Refused):  # W-IMP6
            self.bring([importkit.bfi_draft(self.spec)], at="2026-10-12T09:30:00Z")
        fixed = importkit.bfi_draft(self.spec, **{"big-five/C": 4.4, "big-five/E": 2.9, "big-five/O": 3.6})
        self.bring([fixed], at="2026-10-12T09:30:00Z", supersedes="as-01")
        record = self.record("as-02")
        self.assertEqual(record["supersedes"], "as-01")
        self.assertEqual(record["assertedBy"], self.record("as-01")["assertedBy"])  # R-V2
        report = self.check()
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["warnings"], [])
        with self.assertRaises(Refused):
            self.bring([importkit.hexaco_draft(self.spec)], at="2026-10-12T09:40:00Z", supersedes="as-02")

    # ------------------------------------------------------------ transcript
    def test_transcript(self):
        text = "\n".join(["# read from a screenshot of the score page", "Taken: 2026-09-20", "Norms: Test norms",
                          "Честность-скромность: 61", "Conscientiousness: 74", "hexaco/X: 30", "Openness to Experience: -"])
        draft = import_assessment.parse_transcript(self.spec, HEXACO_PI, text)
        self.assertEqual(draft["administeredAt"], "2026-09-20")
        self.assertEqual(draft["normGroup"], "test-norms")
        values = dict((s["scale"], s["percentile"]) for s in draft["scores"])
        self.assertEqual((values["hexaco/H"], values["hexaco/C"], values["hexaco/X"], values["hexaco/O"]),
                         (61, 74, 30, None))
        self.bring([draft])
        self.assertEqual(len(self.record("as-01")["results"]), 3)
        with self.assertRaises(Refused) as caught:
            import_assessment.parse_transcript(self.spec, HEXACO_PI, "Taken: 2026-09-20\nCharisma: 80\nC 74")
        self.assertIn("2, 3", str(caught.exception))
        self.assertNotIn("80", str(caught.exception))

    def test_draft_on_the_command_line(self):
        path = os.path.join(self.tmp, "draft.json")
        jsonio.write_pretty(path, importkit.bfi_draft(self.spec))
        with redirect_stdout(io.StringIO()):
            code = import_assessment.main(["draft", "--package", self.pkg, "--draft", path, "--at", AT, "--registry",
                                           os.path.join(self.tmp, "registry"), "--report",
                                           importkit.write_report(self.tmp)])
        self.assertEqual(code, 0)
        self.assertEqual(self.record("as-01")["source"], "src-01")


class ScorerRoute(unittest.TestCase):
    """The earlier converter route (not an imported result) with the defects of R-026 fixed."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ohc-scorer-")
        self.spec = importkit.write_registry(self.tmp)
        self.pkg = importkit.new_package(os.path.join(self.tmp, "ctx"), self.spec)
        kofi = os.path.join(helpers.repo_root(), "examples", "kofi-gum-ode", "fixtures", "ipip-neo-120-results.json")
        self.data = jsonio.load_json(kofi)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_with(self, data, **kw):
        path = os.path.join(self.tmp, "results.json")
        jsonio.write_pretty(path, data)
        return import_assessment.run_import(path, self.pkg, importkit.BIG_FIVE, spec=self.spec, seed="t", **kw)

    def test_percentile_goes_into_standardized(self):
        data = copy.deepcopy(self.data)
        data["domains"][0]["percentile"] = 40
        self.run_with(data, at="2026-09-29T19:00:00Z")
        record = Package(self.pkg, self.spec).record("as-01")
        self.assertEqual(record["results"][0]["standardized"], {"type": "percentile", "value": 40})
        self.assertNotIn("percentile", record["results"][0])
        self.assertFalse(model.is_imported_result("AssessmentRecord", record))
        report = check.run_context(self.pkg, spec=self.spec)
        self.assertTrue(report["valid"], report["errors"])

    def test_refusals(self):
        cases = []
        data = copy.deepcopy(self.data)
        del data["administeredAt"]
        cases.append((data, {}))
        data = copy.deepcopy(self.data)
        del data["instrument"]
        cases.append((data, {}))
        data = copy.deepcopy(self.data)
        del data["scorer"]
        cases.append((data, {}))
        data = copy.deepcopy(self.data)
        data["reportSummary"] = "x"
        cases.append((data, {}))
        data = copy.deepcopy(self.data)
        data["note"] = "x" * 500
        cases.append((data, {}))
        cases.append((copy.deepcopy(self.data), {"mode": "observer-report-instrument"}))  # not a catalog code
        cases.append((copy.deepcopy(self.data), {"mode": "vendor-report-import"}))  # a report comes as a draft
        cases.append((copy.deepcopy(self.data), {"mode": "agent-inference"}))
        data = copy.deepcopy(self.data)
        data.pop("domains"), data.pop("facets")
        data["results"] = [{"type": "type-assignment", "construct": "big-five/E", "method": "instrument"}]
        del data["scorer"]["method"]
        cases.append((data, {}))  # AR-6
        for index, (data, kw) in enumerate(cases):
            with self.assertRaises(Refused, msg=str(index)):
                self.run_with(data, **kw)

    def test_review_after_is_a_duration_or_absent(self):
        self.assertEqual(import_assessment.review_after({"defaults": {"reviewAfter": "P3Y"}}), "P3Y")
        self.assertIsNone(import_assessment.review_after({"defaults": {"reviewAfter": "on-change"}}))

    def test_self_identified_is_flagged(self):
        data = copy.deepcopy(self.data)
        for key in ("scorer", "instrument", "rawRange", "normGroup", "facets", "scoredAt"):
            data.pop(key)
        self.run_with(data, mode="self-identified", at="2026-09-29T19:00:00Z")
        record = Package(self.pkg, self.spec).record("as-01")
        self.assertEqual(record["origin"], "declared")
        self.assertIn("self-identified-only", record["validityFlags"])


if __name__ == "__main__":
    unittest.main()
