"""The eight episode-first checks (Annex C), shown on the Noa example and on mutations of the base fixture."""

import copy
import hashlib
import os
import shutil
import tempfile
import unittest

import helpers

import ohc_query
from ohclib import grants, model

NOA = os.path.join(helpers.repo_root(), "examples", "noa-episode-first")
ACCOUNT_FIELDS = {"narrator", "narratedAt", "addedAt", "accountKind", "happened", "experienced", "didOrTried",
                  "understandingThen", "evidence", "affectTags", "mediaType", "lang", "note"}


class EpisodeFirst(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ctx = model.Context(NOA, helpers.spec())
        cls.now = cls.ctx.latest_time()
        cls.state = model.State(cls.ctx, cls.now)

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ohc-episode-first-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_retrospective_reading_not_in_episode(self):
        episodes = [i for i in self.ctx.items if i.kind == "Episode"]
        readings = [i for i in self.ctx.items if i.kind == "Interpretation"]
        self.assertTrue(episodes and readings)
        for episode in episodes:
            for account in episode.data.get("accounts") or []:
                self.assertTrue(set(account).issubset(ACCOUNT_FIELDS), sorted(set(account) - ACCOUNT_FIELDS))
        for reading in readings:
            self.assertTrue(all(self.ctx.kind_of(ref) in ("Episode", "Pattern", "Claim", "Relation", None)
                                for ref in reading.data.get("about") or [] if isinstance(ref, str)))
        # A reading written into an episode is rejected by the schema.
        report = helpers.run_fixture({"form": "single", "patches": [
            {"op": "set", "target": "episodes", "path": "/@ep-01/accounts/0/interpretation",
             "value": "I skipped because I avoid being evaluated."}]}, os.path.join(self.tmp, "x"))
        self.assertIn("S-3", helpers.error_rules(report))

    def test_two_interpretations_coexist(self):
        for rid in ("in-02", "in-03"):
            status = self.state.status[rid]
            self.assertEqual(status.admission, "active")
            self.assertFalse(self.state.superseded(rid))
        relation = self.ctx.record("r-03")
        self.assertEqual((relation["rel"], relation["from"], relation["to"]), ("alternative-to", "in-02", "in-03"))

    def test_temporal_self_model_query(self):
        query = ohc_query.Query(self.ctx)
        changes = query.view_changes("ep-04")["changes"]
        self.assertEqual([(c["from"], c["to"]) for c in changes], [("in-01", "in-03")])
        self.assertEqual(self.state.successor.get("c-11"), "c-12")
        self.assertEqual([r["id"] for r in query.stopped_convincing()["interpretations"]], ["in-01"])

    def test_pattern_needs_two_episodes(self):
        pattern = self.ctx.record("pat-01")
        self.assertGreaterEqual(len(set(pattern["episodes"])), 2)
        fixture = helpers.load_fixture(os.path.join(helpers.FIXTURES, "negative", "pt-1-one-episode.json"))
        self.assertEqual(helpers.error_rules(helpers.run_fixture(fixture, os.path.join(self.tmp, "pt"))), ["PT-1"])

    def test_independent_agent_does_not_inherit_interpretations(self):
        projection = grants.build_projection(self.ctx, "g-01", "scheduling", self.now, "prj-test",
                                             holder_key=grants.EXAMPLE_HOLDER_KEY)
        self.assertNotIn("interpretations", projection)
        served = grants.served_id_set(projection)
        for rid in served:
            self.assertNotEqual(helpers.spec().layer(self.ctx.kind_of(rid)), "interpretation", rid)
        companion = grants.build_projection(self.ctx, "g-02", "self-reflection", model.parse_time("2026-09-22T12:00:00Z"),
                                            "prj-test-2", holder_key=grants.EXAMPLE_HOLDER_KEY)
        self.assertIn("interpretations", companion)

    def test_contest_keeps_evidence(self):
        status = self.state.status["c-09"]
        self.assertTrue(status.contested)
        self.assertEqual(self.state.label("c-09", self.now), "disputed")
        source = self.ctx.record("src-02")
        self.assertIsNotNone(source)
        cited = [g["span"]["source"] for g in self.ctx.record("c-09")["evidence"] if "span" in g]
        self.assertIn("src-02", cited)
        with open(os.path.join(NOA, source["content"]["locator"]["vaultPath"]), "rb") as handle:
            self.assertEqual(hashlib.sha256(handle.read()).hexdigest(), source["content"]["sha256"])

    def test_recall_requires_grant_action(self):
        at = model.parse_time("2026-09-24T07:30:00Z")
        state = model.State(self.ctx, at)
        grant = self.ctx.record("g-02")
        served, _mode = grants.evaluate(state, grant, "a-02", "recall-support", at)
        self.assertIn("rc-01", [i.id for i in served])
        without = copy.deepcopy(grant)
        without["actions"] = [a for a in without["actions"] if a != "recall"]
        served, _mode = grants.evaluate(state, without, "a-02", "recall-support", at)
        self.assertNotIn("RecallCue", [i.kind for i in served])

    def test_outcome_recorded_by_subject(self):
        outcome = self.ctx.record("oc-02")
        self.assertEqual(outcome["assertedBy"], "subject")
        self.assertEqual(outcome["about"], {"recallCue": "rc-01"})
        self.assertEqual(outcome["result"], "helped")
        fixture = helpers.load_fixture(os.path.join(helpers.FIXTURES, "negative", "o-1-agent-outcome-not-hypothesis.json"))
        self.assertEqual(helpers.error_rules(helpers.run_fixture(fixture, os.path.join(self.tmp, "o1"))), ["O-1"])


if __name__ == "__main__":
    unittest.main()
