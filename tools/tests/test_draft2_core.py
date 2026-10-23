"""0.1.0-draft.2 core: instrument import (IMP, INS), decisions on results and readings (R-G14, GR-2), the person's
words on a partly endorsed record (PJ-8), reading through a lens under the agreement (I5, LA-1, AR-4) and playbooks
(PB-1...PB-3, W-PB5). Positive cases here; each negative case is also a fixture in fixtures/negative/."""

import copy
import os
import shutil
import tempfile
import unittest

import helpers

import check
from ohclib import grants, jsonio, model

T = "2026-09-07T08:00:00Z"
MODULES = ["core", "governance", "lenses", "instrument-import", "practices", "patterns", "recall", "inner-system",
           "health-ref"]


def op(kind, target, path, value=None):
    patch = {"op": kind, "target": target, "path": path}
    if kind != "remove":
        patch["value"] = value
    return patch


def imported_fixture():
    """A valid imported result: the IMP-1 fixture with the module declared."""
    fixture = helpers.load_fixture(os.path.join(helpers.FIXTURES, "negative", "imp-1-module-not-declared.json"))
    fixture["patches"][0]["value"] = list(MODULES)
    fixture.pop("expect")
    return fixture


def playbook_fixture(name):
    return helpers.load_fixture(os.path.join(helpers.FIXTURES, "negative", name + ".json"))


class Draft2Core(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ohc-draft2-")
        self.n = 0

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_fixture(self, fixture):
        self.n += 1
        return helpers.run_fixture(fixture, os.path.join(self.tmp, str(self.n)))

    def run_patches(self, patches, form="single", **rest):
        fixture = dict({"form": form, "patches": patches}, **rest)
        return self.run_fixture(fixture)

    def warnings(self, report):
        return sorted(set(w["rule"] for w in report["warnings"]))

    def assertValid(self, report):
        self.assertTrue(report["valid"], report["errors"])

    # ------------------------------------------------------------ rules table
    def test_rule_ids_of_draft2(self):
        for rule in ("LN-2", "LN-10", "LN-12", "LA-7"):
            self.assertNotIn(rule, check.RULES)
        expected = {"IMP-1": "check", "IMP-2": "check", "IMP-3": "check", "IMP-4": "check", "IMP-5": "check",
                    "INS-1": "check", "W-IMP2": "warning", "W-IMP6": "warning", "PB-1": "check", "PB-2": "check",
                    "PB-3": "check", "W-PB5": "warning", "PB-4": "normative", "PB-5": "normative",
                    "IMA-1": "normative", "IMA-2": "normative", "IMH-1": "normative", "R-G14": "normative",
                    "PJ-8": "computed"}
        for rule, how in expected.items():
            self.assertEqual(check.RULES[rule][1], how, rule)
        for rule, where in (("IMP-2", "INSTRUMENT-IMPORT.md"), ("INS-1", "INSTRUMENT-IMPORT.md"),
                            ("IMH-1", "INSTRUMENT-IMPORT.md"), ("PB-1", "LENSES.md"), ("W-PB5", "LENSES.md"),
                            ("R-G14", "SPECIFICATION.md"), ("PJ-8", "SPECIFICATION.md")):
            message, see = check.explain(rule)
            self.assertTrue(message, rule)
            self.assertIn(where, see, rule)

    # ------------------------------------------------------------ instrument import
    def test_imported_result_is_valid_and_proposed(self):
        fixture = imported_fixture()
        report = self.run_fixture(fixture)
        self.assertValid(report)
        self.assertEqual(self.warnings(report), [])
        dest = os.path.join(self.tmp, "ctx")
        spec = helpers.write_registry(dest + "-registry", fixture["registry"])
        helpers.materialize_fixture(fixture, dest)
        state = model.State(model.Context(dest, spec))
        self.assertEqual(state.status["as-01"].admission, "proposed")  # IMP-3: proposed until the subject decides

    def test_instrument_version_change_warns(self):
        fixture = imported_fixture()
        fixture["patches"][3]["value"]["importedFrom"]["systemVersion"] = "0.0.9"
        report = self.run_fixture(fixture)
        self.assertValid(report)
        self.assertEqual(self.warnings(report), ["W-IMP2"])

    def test_duplicate_import_warns(self):
        fixture = imported_fixture()
        twin = copy.deepcopy(fixture["patches"][3]["value"])
        twin["id"] = "as-02"
        fixture["patches"].append(op("add", "assessments", "", twin))
        report = self.run_fixture(fixture)
        self.assertValid(report)
        self.assertEqual(self.warnings(report), ["W-IMP6"])

    def test_draft1_records_are_not_imported_results(self):
        for name in ("noa-episode-first", "kofi-gum-ode/context", "mara-l1-agent", "ilse-minimal"):
            ctx = model.Context(os.path.join(helpers.repo_root(), "examples", name), helpers.spec())
            self.assertFalse(any(model.is_imported_result(i.kind, i.data) for i in ctx.items), name)

    def test_import_block_is_checked(self):
        fixture = playbook_fixture("ins-1-scale-not-of-the-lens")
        fixture["patches"][0]["value"]["scales"] = ["big-five/E", "big-five/C"]
        fixture.pop("expect")
        report = self.run_fixture(fixture)
        self.assertEqual(report["errors"], [])

    def test_imported_result_freshness_anchor_is_administered_at(self):
        fixture = imported_fixture()
        result = fixture["patches"][3]["value"]
        result.update({"administeredAt": {"start": "2023-05-02", "precision": "day"},
                       "formulatedAt": "2023-05-02T00:00:00Z", "reviewAfter": "P3Y"})
        dest = os.path.join(self.tmp, "anchor")
        spec = helpers.write_registry(dest + "-registry", fixture["registry"])
        helpers.materialize_fixture(fixture, dest)
        state = model.State(model.Context(dest, spec))
        self.assertEqual(state.freshness("as-01", model.parse_time("2026-09-08T00:00:00Z")), "review-due")
        self.assertValid(self.run_fixture(fixture))

    # ------------------------------------------------------------ R-G14, GR-2, PJ-8
    def test_decision_use_codes(self):
        self.assertValid(self.run_patches([op("set", "grants", "/@g-01/constraints/decisionUse", "approval-required")]))
        report = self.run_patches([op("set", "grants", "/@g-01/constraints/automatedDecisionUse", False)])
        self.assertIn("S-3", helpers.error_rules(report))

    def test_obligations_carry_decision_use(self):
        for value, expected in ((None, "deny"), ("approval-required", "approval-required")):
            patches = [] if value is None else [op("set", "grants", "/@g-01/constraints/decisionUse", value)]
            dest = helpers.materialize(os.path.join(self.tmp, expected), form="package", patches=patches)
            ctx = model.Context(dest, helpers.spec())
            projection = grants.build_projection(ctx, "g-01", "learning-support",
                                                 model.parse_time("2026-10-08T12:00:00Z"), "prj-t",
                                                 holder_key=grants.EXAMPLE_HOLDER_KEY)
            self.assertEqual(projection["obligations"]["decisionUse"], expected)
            self.assertValid(helpers.run_check(dest))

    def test_endorsed_part_and_summary_source(self):
        fixture = imported_fixture()
        grant = {"id": "g-02", "recordedAt": "2026-09-07T09:00:00Z", "grantor": "subject", "grantee": "a-01",
                 "purposes": ["assist-personal"], "scope": {"include": [{"lenses": ["urn:ohc:lens:big-five"]}]},
                 "actions": ["read"], "mode": "summary", "maxSourceTier": "none",
                 "constraints": {"expiresAt": "2027-03-01T00:00:00Z", "storage": "until-expiry", "forwarding": False,
                                 "crossContextUse": False, "decisionUse": "approval-required", "delegable": False},
                 "basis": {"legal": "explicit-consent"},
                 "expressedBy": {"actor": "subject", "at": "2026-09-07T09:00:00Z", "channel": "holder-ui"}}
        words = "Fits: Conscientiousness. Does not fit: Extraversion. \"I am quieter than this says.\""
        fixture["patches"] += [
            op("add", "grants", "", grant),
            op("add", "reviews", "", {"id": "rv-02", "target": "as-01", "action": "partially-endorse", "by": "subject",
                                      "endorsedPart": words, "recordedAt": "2026-09-07T08:30:00Z"})]
        self.assertValid(self.run_fixture(fixture))
        dest = os.path.join(self.tmp, "pj8")
        spec = helpers.write_registry(dest + "-registry", fixture["registry"])
        helpers.materialize_fixture(fixture, dest)
        ctx = model.Context(dest, spec)
        projection = grants.build_projection(ctx, "g-02", "assist-personal", model.parse_time("2026-09-08T07:00:00Z"),
                                             "prj-t", holder_key=grants.EXAMPLE_HOLDER_KEY)
        record = projection["statements"]["assessments"][0]
        self.assertNotIn("source", record)
        self.assertNotIn("importedFrom", record)
        self.assertEqual(projection["derived"]["as-01"]["label"], "partly-confirmed")
        self.assertEqual(projection["derived"]["as-01"]["endorsedPart"], words)
        self.assertEqual(projection["obligations"]["decisionUse"], "approval-required")
        self.assertEqual(helpers.spec().validate("urn:ohc:schema:projection:0.1.0-draft", projection), [])

    # ------------------------------------------------------------ I5, LA-1, AR-4
    def reading_patches(self, mode, include):
        fixture = playbook_fixture("i-5-adoption-off")
        patches = fixture["patches"]
        patches[0]["value"]["scope"]["include"] = include
        patches.append(op("set", "lensAdoptions", "/@la-01/agentInterpretation", mode))
        return patches

    def test_agent_reads_through_lens_under_grant_and_adoption(self):
        named = [{"lenses": ["urn:ohc:lens:cbt"]}]
        self.assertValid(self.run_patches(self.reading_patches("allowed", named)))
        # ask-first needs a confirmed ask-first Event, checked at L2 only
        self.assertValid(self.run_patches(self.reading_patches("ask-first", named)))

    def test_agent_reads_lens_without_adoption(self):
        patches = self.reading_patches("off", [{"lenses": ["urn:ohc:lens:cbt"]}])
        patches.append(op("remove", "lensAdoptions", "/@la-01"))
        self.assertValid(self.run_patches(patches))

    def test_agent_suggested_adoption_of_a_frame(self):
        adoption = helpers.subj({"id": "la-02", "lens": {"id": "urn:ohc:lens:astrology", "version": "0.1.0"},
                                 "route": "agent-suggested", "suggestedBy": "a-01", "uses": ["speak-in-lens"]}, T)
        self.assertValid(self.run_patches([op("add", "lensAdoptions", "", adoption)]))

    def test_record_inferred_from_frame_is_frame_relative(self):
        fixture = playbook_fixture("ar-4-inferred-from-frame")
        fixture["patches"][2]["value"]["epistemic"] = "frame-relative"
        fixture.pop("expect")
        self.assertValid(self.run_fixture(fixture))

    # ------------------------------------------------------------ playbooks
    def test_registry_playbook_passes(self):
        fixture = playbook_fixture("pb-1-tool-not-of-the-lens")
        fixture["patches"] = []
        report = self.run_fixture(fixture)
        self.assertEqual(report["errors"], [])

    def test_local_playbook_pinned_and_chosen(self):
        fixture = playbook_fixture("pb-3-playbook-not-for-this-lens")
        playbook = fixture["patches"][0]["value"][0]["playbook"]
        playbook["lenses"] = ["urn:ohc:lens:cbt"]
        playbook["situations"][0]["toolkit"] = ["cbt.thought-record"]
        fixture.pop("expect")
        self.assertValid(self.run_fixture(fixture))
        fixture["patches"][1]["value"] = []
        self.assertValid(self.run_fixture(fixture))

    def test_local_playbook_in_a_package(self):
        fixture = playbook_fixture("pb-3-playbook-not-for-this-lens")
        playbook = fixture["patches"][0]["value"][0].pop("playbook")
        playbook["lenses"] = ["urn:ohc:lens:cbt"]
        playbook["situations"][0]["toolkit"] = ["cbt.thought-record"]
        fixture.update({"form": "package", "raw": {"lenses/week-review@0.1.0.playbook.json":
                                                   jsonio.dumps_pretty(playbook)}})
        fixture.pop("expect")
        report = self.run_fixture(fixture)
        self.assertValid(report)
        self.assertEqual(report["levelMet"], "L2")
        dest = os.path.join(self.tmp, str(self.n))
        lock = jsonio.load_json(os.path.join(dest, "context.lock.json"))
        self.assertIn("lenses/week-review@0.1.0.playbook.json", lock["files"])

    def test_unresolved_pin_warns(self):
        report = self.run_patches([op("set", "manifest", "/playbooks",
                                      [{"id": "urn:ohc:playbook:x-coach-a:gone", "version": "0.1.0"}])])
        self.assertValid(report)
        self.assertEqual(self.warnings(report), ["W-PB5"])

    def test_local_descriptor_lists_its_pinned_playbook(self):
        lens = playbook_fixture("pb-2-unresolved-playbook")["document"]
        playbook = playbook_fixture("pb-3-playbook-not-for-this-lens")["patches"][0]["value"][0]["playbook"]
        playbook["lenses"] = [lens["id"]]
        playbook["situations"][0]["toolkit"] = []
        lens["playbooks"] = [playbook["id"]]
        report = self.run_patches([
            op("add", "manifest", "/lenses", {"id": lens["id"], "version": lens["version"], "descriptor": lens}),
            op("set", "manifest", "/playbooks", [{"id": playbook["id"], "version": "0.1.0", "playbook": playbook}])])
        self.assertValid(report)


if __name__ == "__main__":
    unittest.main()
