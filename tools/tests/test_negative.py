"""Every negative fixture fails with exactly its expected rule ids; one fixture or more per rule group."""

import glob
import os
import re
import shutil
import tempfile
import unittest

import helpers

import check

FIXTURES = sorted(glob.glob(os.path.join(helpers.FIXTURES, "negative", "*.json")))
# Rule groups covered elsewhere: SELF (test_schemas), REL (test_release), W- warnings (test_rules).
NOT_FIXTURE_GROUPS = {"SELF", "REL", "W"}


def group_of(rule):
    match = re.match(r"^(R-[A-Z]|W|[A-Z]+)", rule)
    return match.group(1)


class NegativeFixtures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ohc-negative-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_each_fixture_fails_with_expected_rules(self):
        self.assertTrue(FIXTURES, "no negative fixtures found")
        for path in FIXTURES:
            name = os.path.basename(path)
            with self.subTest(fixture=name):
                fixture = helpers.load_fixture(path)
                report = helpers.run_fixture(fixture, os.path.join(self.tmp, name[:-5]))
                self.assertFalse(report["valid"], name)
                self.assertEqual(helpers.error_rules(report), sorted(fixture["expect"]), name)

    def test_at_least_one_fixture_per_rule_group(self):
        covered = set()
        for path in FIXTURES:
            for rule in helpers.load_fixture(path)["expect"]:
                covered.add(group_of(rule))
        required = set()
        for rule, (_level, how) in check.RULES.items():
            if how == "check" and group_of(rule) not in NOT_FIXTURE_GROUPS:
                required.add(group_of(rule))
        self.assertEqual(sorted(required - covered), [])

    def test_base_contexts_are_valid(self):
        for form, level in (("single", "L1"), ("package", "L2")):
            with self.subTest(form=form):
                dest = helpers.materialize(os.path.join(self.tmp, form), form=form)
                report = helpers.run_check(dest)
                self.assertTrue(report["valid"], report["errors"])
                self.assertEqual(report["levelMet"], level)


if __name__ == "__main__":
    unittest.main()
