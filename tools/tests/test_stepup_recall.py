"""Step-up for verbatim access (SU-1, SU-4) and recall (RC-2, RC-3, RC-4)."""

import os
import shutil
import tempfile
import unittest

import helpers

from ohclib import grants, model

VERBATIM = [
    {"op": "add", "target": "grants", "path": "/@g-01/actions", "value": "open-verbatim"},
    {"op": "set", "target": "grants", "path": "/@g-01/maxSourceTier", "value": "verbatim"},
    {"op": "set", "target": "grants", "path": "/@g-01/stepUp", "value": {"required": True, "maxDuration": "PT30M"}},
    {"op": "set", "target": "sources", "path": "/@src-01/maxRelease", "value": "verbatim"},
]


def step_up_events(outcome, opened_at="2026-10-08T13:05:00Z"):
    base = {"grant": "g-01", "purpose": "learning-support", "records": ["src-01"]}
    return [
        {"op": "add", "target": "events", "path": "", "value": dict(base, at="2026-10-08T13:00:00Z",
                                                                    eventType="source-access-requested",
                                                                    actor="a-01", counterparty="holder")},
        {"op": "add", "target": "events", "path": "", "value": dict(base, at="2026-10-08T13:01:00Z",
                                                                    eventType="step-up-confirmed", actor="subject",
                                                                    outcome=outcome,
                                                                    confirmationDigest="sha256:" + "1" * 64)},
        {"op": "add", "target": "events", "path": "", "value": dict(base, at=opened_at, eventType="source-opened",
                                                                    actor="holder", counterparty="a-01",
                                                                    tier="verbatim", outcome="served")},
    ]


def outcome(oid, result, at, response=None):
    record = helpers.subj({"id": oid, "about": {"recallCue": "rc-01"}, "result": result}, at)
    if response:
        record["delivery"] = {"at": at, "by": "a-01", "response": response}
    return {"op": "add", "target": "outcomes", "path": "", "value": record}


class StepUpAndRecall(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ohc-stepup-")
        self.n = 0

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_patches(self, patches, form="single"):
        self.n += 1
        return helpers.run_fixture({"form": form, "patches": patches}, os.path.join(self.tmp, str(self.n)))

    def test_step_up_max_one_hour(self):
        self.assertTrue(self.run_patches(VERBATIM)["valid"])
        for duration, ok in (("PT1H", True), ("PT61M", False), ("PT2H", False)):
            with self.subTest(duration=duration):
                patches = VERBATIM[:2] + VERBATIM[3:] + [{"op": "set", "target": "grants", "path": "/@g-01/stepUp",
                                                          "value": {"required": True, "maxDuration": duration}}]
                report = self.run_patches(patches)
                self.assertEqual(report["valid"], ok, report["errors"])
                if not ok:
                    self.assertIn("GR-3", helpers.error_rules(report))
        late = self.run_patches(VERBATIM + step_up_events("confirmed", "2026-10-08T13:45:00Z"), form="package")
        self.assertIn("EV-5", helpers.error_rules(late))

    def test_step_up_timeout_is_decline(self):
        confirmed = self.run_patches(VERBATIM + step_up_events("confirmed"), form="package")
        self.assertTrue(confirmed["valid"], confirmed["errors"])
        for silent in ("timeout", "declined"):
            with self.subTest(outcome=silent):
                report = self.run_patches(VERBATIM + step_up_events(silent), form="package")
                self.assertEqual(helpers.error_rules(report), ["EV-5"])

    def test_recall_autopause(self):
        dest = helpers.materialize(os.path.join(self.tmp, "pause"), form="single", patches=[
            outcome("oc-02", "no-effect", "2026-09-10T08:00:00Z"),
            outcome("oc-03", "worse", "2026-09-12T08:00:00Z"),
            outcome("oc-04", "no-effect", "2026-09-14T08:00:00Z")])
        ctx = model.Context(dest, helpers.spec())
        at = model.parse_time("2026-09-15T08:00:00Z")
        state = model.State(ctx, at)
        self.assertEqual(state.status["rc-01"].lifecycle, "paused")
        grant = dict(ctx.record("g-01"))
        grant["actions"] = list(grant["actions"]) + ["recall"]
        grant["purposes"] = ["learning-support", "recall-support"]
        grant["scope"] = {"include": [{"kinds": ["RecallCue", "Practice", "Episode"]}]}
        served, _mode = grants.evaluate(state, grant, "a-01", "recall-support", at)
        self.assertNotIn("rc-01", [i.id for i in served])
        two = model.State(ctx, model.parse_time("2026-09-13T08:00:00Z"))
        self.assertEqual(two.status["rc-01"].lifecycle, "active")
        resumed = helpers.materialize(os.path.join(self.tmp, "resume"), form="single", patches=[
            outcome("oc-02", "no-effect", "2026-09-10T08:00:00Z", "asked-to-stop"),
            {"op": "add", "target": "reviews", "path": "", "value": {"id": "rv-09", "target": "rc-01",
                                                                     "action": "resume", "by": "subject",
                                                                     "recordedAt": "2026-09-11T08:00:00Z"}}])
        ctx = model.Context(resumed, helpers.spec())
        self.assertEqual(model.State(ctx, model.parse_time("2026-09-10T12:00:00Z")).status["rc-01"].lifecycle, "paused")
        self.assertEqual(model.State(ctx, model.parse_time("2026-09-12T08:00:00Z")).status["rc-01"].lifecycle, "active")

    def test_recall_trauma_needs_subject_cue(self):
        fixture = helpers.load_fixture(os.path.join(helpers.FIXTURES, "negative", "rc-2-agent-cue-on-special-target.json"))
        report = helpers.run_fixture(fixture, os.path.join(self.tmp, "rc2"))
        self.assertEqual(helpers.error_rules(report), ["RC-2"])
        own = self.run_patches([{"op": "set", "target": "recallCues", "path": "/@rc-01/offer/targets",
                                 "value": ["pr-01", "part-01"]}])
        self.assertNotIn("RC-2", helpers.error_rules(own))

    def test_recall_alternatives_non_psychological(self):
        report = self.run_patches([{"op": "set", "target": "recallCues", "path": "/@rc-01/offer/alternativesNote",
                                    "value": "It may be avoidance or fear of failing."}])
        self.assertIn("RC-4", [w["rule"] for w in report["warnings"]])
        empty = self.run_patches([{"op": "set", "target": "recallCues", "path": "/@rc-01/offer/includeAlternatives",
                                   "value": False}])
        self.assertFalse(empty["valid"])
        fine = self.run_patches([])
        self.assertNotIn("RC-4", [w["rule"] for w in fine["warnings"]])


if __name__ == "__main__":
    unittest.main()
