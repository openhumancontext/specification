"""Temporal queries (§7.3): as-valid-at, as-known-at, as-understood-at; and the stored query outputs."""

import contextlib
import io
import os
import unittest

import helpers

import ohc_query
from ohclib import jsonio, model

NOA = os.path.join(helpers.repo_root(), "examples", "noa-episode-first")


def query(*argv):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = ohc_query.main(list(argv))
    return code, buffer.getvalue()


class Queries(unittest.TestCase):
    def setUp(self):
        self.ctx = model.Context(NOA, helpers.spec())
        self.query = ohc_query.Query(self.ctx)

    def test_as_understood_at_july_gives_in_01(self):
        result = self.query.as_understood_at("ep-04", model.parse_time("2026-07-01T00:00:00Z"))
        self.assertEqual([r["id"] for r in result["interpretations"]], ["in-01"])
        self.assertEqual(result["episodeChain"], ["ep-04", "ep-01"])

    def test_as_understood_at_october_gives_in_03(self):
        result = self.query.as_understood_at("ep-04", model.parse_time("2026-10-01T00:00:00Z"))
        ids = [r["id"] for r in result["interpretations"]]
        self.assertIn("in-03", ids)
        self.assertNotIn("in-01", ids)

    def test_as_known_at_hides_later_records(self):
        result = self.query.as_known_at(model.parse_time("2026-07-01T00:00:00Z"))
        ids = set(r["id"] for r in result["records"])
        self.assertIn("in-01", ids)
        self.assertNotIn("in-03", ids)
        self.assertNotIn("c-12", ids)
        later = set(r["id"] for r in self.query.as_known_at(model.parse_time("2026-10-01T00:00:00Z"))["records"])
        self.assertIn("in-03", later)

    def test_as_valid_at(self):
        before = set(r["id"] for r in self.query.as_valid_at(model.parse_time("2026-03-12T12:00:00Z"))["records"])
        self.assertIn("ep-01", before)
        self.assertNotIn("ep-03", before)
        after = set(r["id"] for r in self.query.as_valid_at(model.parse_time("2026-09-18T12:00:00Z"))["records"])
        self.assertIn("ep-03", after)

    def test_stored_query_outputs_reproduce(self):
        cases = [
            ("as-understood-at-2026-07-01--ep-04.json", ["as-understood-at", "--episode", "ep-04", "--at",
                                                          "2026-07-01T00:00:00Z"]),
            ("view-changes--ep-04.json", ["view-changes", "--episode", "ep-04"]),
            ("stopped-convincing.json", ["stopped-convincing"]),
            ("actions-vs-explanations.json", ["actions-vs-explanations"]),
        ]
        for name, argv in cases:
            with self.subTest(query=name):
                code, out = query(NOA, *argv)
                self.assertEqual(code, 0)
                with open(os.path.join(NOA, "queries", name), "r", encoding="utf-8") as handle:
                    self.assertEqual(out, handle.read())

    def test_project_reproduces_stored_projection(self):
        stored = jsonio.load_json(os.path.join(NOA, "projections", "prj-0007.json"))
        code, out = query(NOA, "project", "--grant", "g-02", "--purpose", "recall-support", "--now",
                          stored["generatedAt"], "--id", "prj-0007", "--request", stored["request"], "--nonce",
                          stored["nonce"], "--mode", "summary", "--select",
                          '[{"kinds": ["Practice", "Outcome"]}, {"kinds": ["Episode"], "contexts": ["work"]},'
                          ' {"facets": ["relationship"]}]')
        self.assertEqual(code, 0)
        self.assertEqual(jsonio.loads_strict(out), stored)

    def test_project_denied_without_grant(self):
        code, out = query(NOA, "project", "--grant", "g-99", "--purpose", "scheduling")
        self.assertEqual(code, 1)
        self.assertIn("not-granted", out)


if __name__ == "__main__":
    unittest.main()
