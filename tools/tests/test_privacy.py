"""Privacy properties of §12.3 projections: no existence oracle, no guessable digests, no conflict flags outside the
grant, separation of statements and readings, the derived block, pairwise aliases."""

import os
import re
import shutil
import tempfile
import unittest

import helpers

from ohclib import grants, jcs, model

NOA = os.path.join(helpers.repo_root(), "examples", "noa-episode-first")
NOW = model.parse_time("2026-10-08T12:00:00Z")
KEY = grants.EXAMPLE_HOLDER_KEY
SPECIAL_EXTRAS = [
    {"op": "add", "target": "claims", "path": "", "value": helpers.subj({
        "id": "c-07", "facet": "state", "predicate": "stress", "text": "Exam stress in June.", "horizon": "state",
        "sensitivity": "special", "categories": ["mental-health"], "valid": {"until": "2026-06-30"}},
        "2026-09-02T08:00:00Z")},
    {"op": "add", "target": "claims", "path": "", "value": helpers.subj({
        "id": "c-08", "facet": "preference", "predicate": "format", "text": "Large print for health letters.",
        "sensitivity": "special", "categories": ["health"]}, "2026-09-02T08:00:00Z")},
]
SELECT = [{"facets": ["goal"]}, {"categories": ["health"]}, {"categories": ["mental-health"]}]


def walk_keys(value, out):
    if isinstance(value, dict):
        for key, inner in value.items():
            out.append((key, inner))
            walk_keys(inner, out)
    elif isinstance(value, list):
        for inner in value:
            walk_keys(inner, out)
    return out


class Privacy(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ohc-privacy-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def project(self, patches, grant="g-01", select=SELECT, name="x"):
        dest = helpers.materialize(os.path.join(self.tmp, name), form="single", patches=patches)
        ctx = model.Context(dest, helpers.spec())
        return grants.build_projection(ctx, grant, "learning-support", NOW, "prj-0001", select=select,
                                       holder_key=KEY, nonce="AAAAAAAAAAAAAAAAAAAAAA")

    def test_no_existence_oracle(self):
        without = self.project([], name="without")
        with_special = self.project(SPECIAL_EXTRAS, name="with")
        self.assertEqual(jcs.canonicalize(without), jcs.canonicalize(with_special))
        self.assertEqual(sorted(a["code"] for a in without["absences"]), ["not-disclosed", "not-disclosed"])

    def test_no_guessable_digest(self):
        projection = self.project([], select=None)
        keys = walk_keys(projection, [])
        self.assertFalse([k for k, _v in keys if k in ("sha256", "contentDigest", "vaultPath", "locator")])
        handles = [v for k, v in keys if k == "handle"]
        self.assertTrue(handles)
        for handle in handles:
            self.assertTrue(handle.startswith("hmac:"))
            self.assertNotIn(helpers.VAULT_SHA, handle)
        text = jcs.canonicalize(projection)
        self.assertNotIn(helpers.VAULT_SHA, text)
        self.assertNotIn("urn:ohc:example:fixture-ilse\"", text)

    def test_handles_differ_per_grant(self):
        first = grants.handle(grants.EXAMPLE_HOLDER_KEY, "g-01", "src-01")
        second = grants.handle(grants.EXAMPLE_HOLDER_KEY, "g-02", "src-01")
        self.assertNotEqual(first, second)

    def test_no_conflict_flag_outside_grant(self):
        patches = [{"op": "set", "target": "grants", "path": "/@g-01/scope/include",
                    "value": [{"ids": ["c-01"]}, {"kinds": ["Tension"]}]}]
        projection = self.project(patches, select=None, name="conflict")
        served = grants.served_id_set(projection)
        self.assertIn("c-01", served)
        self.assertNotIn("t-01", served)
        self.assertNotIn("c-06", served)
        self.assertFalse(projection["derived"]["c-01"]["contested"])
        self.assertNotIn("t-01", jcs.canonicalize(projection))

    def test_naive_consumer_separation(self):
        ctx = model.Context(NOA, helpers.spec())
        spec = helpers.spec()
        companion = grants.build_projection(ctx, "g-02", "self-reflection", model.parse_time("2026-09-22T12:00:00Z"),
                                            "prj-t", holder_key=KEY)
        for group, members in ((g, companion.get(g) or {}) for g in ("statements", "experience", "interpretations",
                                                                       "recall", "links")):
            for name, records in members.items():
                kind = dict((n, k) for _g, n, k in grants.MEMBERS)[name]
                layer = spec.layer(kind)
                if group == "interpretations":
                    self.assertEqual(layer, "interpretation", kind)
                else:
                    self.assertNotEqual(layer, "interpretation", kind)
        assistant = grants.build_projection(ctx, "g-01", "scheduling", ctx.latest_time(), "prj-u", holder_key=KEY)
        self.assertNotIn("interpretations", assistant)

    def test_projection_derived_block(self):
        projection = self.project([], select=None)
        served = grants.served_id_set(projection)
        self.assertEqual(set(projection["derived"]), served)
        for rid, entry in projection["derived"].items():
            for key in ("label", "freshness", "endorsement", "contested", "locked", "admission", "computedAt"):
                self.assertIn(key, entry, rid)
            self.assertEqual(entry["computedAt"], projection["generatedAt"])
        self.assertEqual(projection["completeness"], "partial")
        self.assertEqual(projection["omissions"], "hidden")
        self.assertEqual(projection["digest"], grants.projection_digest(projection))

    def test_aliases_pairwise(self):
        subject = "urn:ohc:example:fixture-ilse"
        first = grants.subject_alias(grants.EXAMPLE_HOLDER_KEY, subject, "a-01")
        again = grants.subject_alias(grants.EXAMPLE_HOLDER_KEY, subject, "a-01")
        other = grants.subject_alias(grants.EXAMPLE_HOLDER_KEY, subject, "a-02")
        self.assertEqual(first, again)
        self.assertNotEqual(first, other)
        for alias in (first, other):
            self.assertRegex(alias, r"^urn:ohc:alias:[a-z2-7]{26}$")
            self.assertNotIn("ilse", alias)
        self.assertNotEqual(first, grants.subject_alias(b"another-holder-key", subject, "a-01"))


if __name__ == "__main__":
    unittest.main()
