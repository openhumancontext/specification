"""Named rule tests: each rule is shown failing on a minimal mutation of the base fixture."""

import os
import shutil
import tempfile
import unittest

import helpers

from ohclib import grants, model

ROOT = helpers.repo_root()
T = "2026-09-07T08:00:00Z"
STEWARD = {"party": "p-01", "scope": {"actions": ["confirm-current"], "facets": ["goal"]},
           "basis": "delegated-by-subject", "validFrom": "2026-09-01T00:00:00Z", "validUntil": "2026-12-01T00:00:00Z",
           "expressedBy": {"actor": "subject", "at": "2026-09-01T00:00:00Z", "channel": "in-person"}}


def op(kind, target, path, value=None):
    patch = {"op": kind, "target": target, "path": path}
    if kind != "remove":
        patch["value"] = value
    return patch


class Rules(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ohc-rules-")
        self.n = 0

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_patches(self, patches, form="single"):
        self.n += 1
        return helpers.run_fixture({"form": form, "patches": patches}, os.path.join(self.tmp, str(self.n)))

    def fixture(self, name):
        self.n += 1
        fixture = helpers.load_fixture(os.path.join(helpers.FIXTURES, "negative", name + ".json"))
        return helpers.run_fixture(fixture, os.path.join(self.tmp, str(self.n)))

    def assertRule(self, report, rule):
        self.assertFalse(report["valid"])
        self.assertIn(rule, helpers.error_rules(report))

    def test_silence_is_not_acceptance(self):
        ctx = model.Context(os.path.join(ROOT, "examples", "kofi-gum-ode", "context"), helpers.spec())
        before = model.State(ctx, model.parse_time("2026-10-09T12:00:00Z"))
        self.assertEqual(before.status["c-04"].admission, "proposed")
        after = model.State(ctx, model.parse_time("2026-11-07T00:00:00Z"))
        self.assertEqual(after.status["c-04"].admission, "declined")
        self.assertEqual(after.label("c-04", model.parse_time("2026-11-07T00:00:00Z")), "not-accepted")

    def test_absence_is_not_zero(self):
        self.assertRule(self.fixture("cl-2-absence-with-value"), "CL-2")
        report = self.run_patches([op("add", "claims", "", helpers.subj(
            {"id": "c-07", "facet": "resource", "predicate": "money", "absence": {"code": "not-disclosed"}}, T))])
        self.assertTrue(report["valid"], report["errors"])

    def test_part_cannot_grant(self):
        report = self.run_patches([op("set", "grants", "/@g-01/grantor", "part-01")])
        self.assertRule(report, "P-1")
        self.assertRule(self.fixture("p-1-part-as-actor"), "P-1")

    def test_frame_result_stays_in_the_frame(self):
        self.assertRule(self.fixture("ln-3-frame-allows-cross-lens-mapping"), "LN-3")
        self.assertRule(self.fixture("ar-4-inferred-from-frame"), "AR-4")
        report = self.run_patches([
            op("set", "manifest", "/lenses", [{"id": "urn:ohc:lens:cbt", "version": "0.1.0"},
                                             {"id": "urn:ohc:lens:astrology", "version": "0.1.0"}]),
            op("add", "assessments", "", helpers.subj({
                "id": "as-01", "lens": {"id": "urn:ohc:lens:astrology", "version": "0.1.0"},
                "mode": "self-identified", "administeredAt": {"start": "2026-09-01", "precision": "day"},
                "results": [{"type": "type-assignment", "construct": "astrology/placement", "method": "self-identified"}],
                "epistemic": "hypothesis"}, T))])
        self.assertRule(report, "AR-4")

    def test_tombstone_has_no_content(self):
        self.assertRule(self.fixture("tb-1-tombstone-with-content"), "TB-1")

    def test_verbatim_requires_step_up(self):
        self.assertRule(self.fixture("gr-3-verbatim-without-step-up"), "GR-3")
        self.assertRule(self.fixture("ev-5-verbatim-without-step-up"), "EV-5")

    def test_mapping_is_not_identity(self):
        self.assertRule(self.fixture("m-6-frame-correlates"), "M-6")
        spec = helpers.spec()
        self.assertTrue(spec.mappings)
        for mapping in spec.mappings.values():
            self.assertNotIn(mapping.get("relation"), ("identity", "same-as", "equivalent"))
            self.assertIs(mapping.get("notIdentity"), True)
            self.assertIs(mapping.get("chainable"), False)

    def test_infer_requires_grant(self):
        self.assertRule(self.fixture("inf-1-no-grant"), "INF-1")

    def test_proposal_without_infer_not_stored(self):
        report = self.run_patches([op("set", "grants", "/@g-01/actions", ["read", "suggest", "source-index"])])
        self.assertRule(report, "INF-1")

    def test_special_default_for_psych(self):
        ctx = model.Context(os.path.join(ROOT, "examples", "kofi-gum-ode", "context"), helpers.spec())
        state = model.State(ctx)
        self.assertEqual(state.tier("as-01"), "special")
        self.assertEqual(state.tier("src-11"), "special")
        assessment = [i for i in ctx.items if i.id == "as-01"][0]
        self.assertEqual(state.kind_default_tier(assessment), "special")
        dest = helpers.materialize(os.path.join(self.tmp, "psych"), form="single", patches=[
            op("set", "claims", "/@c-03/categories", ["mental-health"]),
            op("set", "claims", "/@c-03/sensitivity", "personal")])
        base = model.State(model.Context(dest, helpers.spec()))
        self.assertEqual(base.tier("c-03"), "special")
        self.assertRule(self.fixture("env-5-agent-lowers-tier"), "ENV-5")

    def test_agent_estimate_person_only(self):
        self.assertRule(self.fixture("ar-2-agent-estimate-not-person-only"), "AR-2")

    def test_emotion_from_biometric_rejected(self):
        self.assertRule(self.fixture("cl-4-emotion-from-screen"), "CL-4")
        report = self.run_patches([
            op("add", "sources", "", helpers.subj({
                "id": "src-02", "sourceKind": "biometric",
                "content": {"locator": {"uri": "urn:uuid:3f1b1a52-9a77-4b0c-8a1e-2d3c4b5a6f71"}, "sha256": "3" * 64,
                            "mediaType": "application/json"},
                "authorship": {"author": "s-01"}, "maxRelease": "index", "retention": {"eraseOnRequest": True}}, T)),
            op("add", "claims", "", dict(helpers.subj({
                "id": "c-07", "facet": "state", "predicate": "stress", "text": "High stress.", "horizon": "state",
                "valid": {"until": "2026-09-08"}, "sensitivity": "special", "categories": ["mental-health"],
                "evidence": [{"span": {"source": "src-02", "selector": {"type": "whole"}}, "kind": "observation"}]}, T),
                origin="derived"))])
        report_rules = helpers.error_rules(report)
        self.assertIn("CL-4", report_rules)

    def test_third_party_inner_state_rejected(self):
        self.assertRule(self.fixture("i-8-reading-about-party"), "I8")
        self.assertRule(self.fixture("cl-6-about-on-state"), "CL-6")
        report = self.run_patches([
            {"op": "add", "target": "episodes", "path": "/@ep-02/accounts", "value": {
                "narrator": "p-01", "narratedAt": "2026-09-05T21:00:00Z", "addedAt": "2026-09-06T08:00:00Z",
                "accountKind": "observer-account", "happened": "Arrived late and felt ashamed."}}])
        self.assertIn("TP-3", [w["rule"] for w in report["warnings"]])

    def test_grant_must_expire(self):
        report = self.run_patches([op("remove", "grants", "/@g-01/constraints/expiresAt")])
        self.assertRule(report, "GR-1")
        self.assertRule(self.fixture("gr-1-infer-grant-too-long"), "GR-1")

    def test_steward_scope(self):
        report = self.run_patches([
            op("set", "manifest", "/stewards", [STEWARD]),
            op("add", "reviews", "", {"id": "rv-09", "target": "c-05", "action": "endorse", "by": "p-01",
                                      "basis": "steward-scope", "recordedAt": "2026-09-08T08:00:00Z"})])
        self.assertEqual(helpers.error_rules(report), ["RV-2"])
        within = self.run_patches([
            op("set", "manifest", "/stewards", [STEWARD]),
            op("add", "reviews", "", {"id": "rv-09", "target": "c-01", "action": "confirm-current", "by": "p-01",
                                      "basis": "steward-scope", "recordedAt": "2026-09-08T08:00:00Z"})])
        self.assertTrue(within["valid"], within["errors"])

    def test_ids_opaque_warning(self):
        report = self.run_patches([op("set", "parts", "/@part-01/id", "part-planner")])
        self.assertTrue(report["valid"], report["errors"])
        self.assertIn("W-ID1", [w["rule"] for w in report["warnings"]])

    def test_served_absence_code_is_only_not_disclosed(self):
        ctx = model.Context(os.path.join(ROOT, "examples", "noa-episode-first"), helpers.spec())
        projection = grants.build_projection(ctx, "g-01", "scheduling", ctx.latest_time(), "prj-t",
                                             holder_key=grants.EXAMPLE_HOLDER_KEY,
                                             select=[{"facets": ["state"]}, {"facets": ["boundary"]}])
        self.assertEqual([a["code"] for a in projection["absences"]], ["not-disclosed"])


if __name__ == "__main__":
    unittest.main()
