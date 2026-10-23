"""Every example passes at its declared level, and the checker output equals expected-check.json."""

import os
import re
import unittest

import helpers

import check
from ohclib import jsonio

ROOT = helpers.repo_root()
EXAMPLES = [
    ("ilse-minimal", "examples/ilse-minimal", "L0"),
    ("noa-episode-first", "examples/noa-episode-first", "L2"),
    ("kofi-gum-ode", "examples/kofi-gum-ode/context", "L2"),
    ("mara-l1-agent", "examples/mara-l1-agent", "L1"),
    ("tove-bring-a-result", "examples/tove-bring-a-result/context", "L2"),
]


class Examples(unittest.TestCase):
    def test_examples_present(self):
        for name, target, _level in EXAMPLES:
            with self.subTest(example=name):
                self.assertTrue(os.path.isfile(os.path.join(ROOT, target, "context.json")), target)
                self.assertTrue(os.path.isfile(os.path.join(ROOT, "examples", name, "README.md")))
                self.assertTrue(os.path.isfile(os.path.join(ROOT, "examples", name, "expected-check.json")))

    def test_examples_pass_declared_level(self):
        for name, target, level in EXAMPLES:
            with self.subTest(example=name):
                report = check.run_context(os.path.join(ROOT, target), level=level, spec=helpers.spec())
                self.assertTrue(report["valid"], report["errors"])
                self.assertEqual(report["levelDeclared"], level)
                self.assertEqual(report["levelMet"], level)

    def test_expected_check_equality(self):
        for name, target, _level in EXAMPLES:
            with self.subTest(example=name):
                report = check.run_context(os.path.join(ROOT, target), spec=helpers.spec())
                expected = jsonio.load_json(os.path.join(ROOT, "examples", name, "expected-check.json"))
                self.assertEqual(report, expected)

    def test_checker_cli_json_output(self):
        import io
        import contextlib

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = check.main([os.path.join(ROOT, "examples", "ilse-minimal"), "--level", "L0", "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(jsonio.loads_strict(buffer.getvalue()),
                         jsonio.load_json(os.path.join(ROOT, "examples", "ilse-minimal", "expected-check.json")))

    def test_readme_example_matches(self):
        with open(os.path.join(ROOT, "README.md"), "r", encoding="utf-8") as handle:
            readme = handle.read()
        section = readme.split("## L0 in five minutes", 1)[1]
        block = re.search(r"```json\n(.*?)\n```", section, re.S).group(1)
        with open(os.path.join(ROOT, "examples", "ilse-minimal", "context.json"), "r", encoding="utf-8") as handle:
            self.assertEqual(block + "\n", handle.read())

    def test_every_example_record_is_synthetic(self):
        for name, target, _level in EXAMPLES:
            with self.subTest(example=name):
                report = check.run_context(os.path.join(ROOT, target), spec=helpers.spec())
                self.assertNotIn("X-1", [e["rule"] for e in report["errors"]])
                self.assertNotIn("CX-8", [e["rule"] for e in report["errors"]])


if __name__ == "__main__":
    unittest.main()
