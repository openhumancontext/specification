"""Documentation that must stay equal to its sources: the tagline, guide snippets, embedded examples, lens tables."""

import json
import os
import re
import shutil
import tempfile
import unittest

import helpers

import check
import lens_tables
from ohclib import jsonio

ROOT = helpers.repo_root()


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return handle.read()


class Docs(unittest.TestCase):
    def tagline(self, lang):
        glossary = jsonio.load_json(os.path.join(ROOT, "spec", "glossary.json"))
        term = next(t for t in glossary["terms"] if t["id"] == "tagline")
        return term["locales"][lang]["definition"]

    def test_one_canonical_english_tagline(self):
        english = self.tagline("en")
        self.assertIn("*%s*" % english, read("README.md"))
        self.assertIn("*%s*" % english, read("docs/OVERVIEW.md"))
        spec = read("spec/SPECIFICATION.md").split("### 2.1.", 1)[1].split("### 2.2.", 1)[0]
        clauses = [c.strip() + "." for c in english.rstrip(".").split(". ")]
        self.assertEqual(len(clauses), 5)
        for clause in clauses:
            self.assertIn("| %s |" % clause, spec)
        overview_rows = read("docs/OVERVIEW.md").split("## Five clauses", 1)[1]
        for clause in clauses:
            self.assertIn("| %s |" % clause, overview_rows)

    def test_russian_tagline_is_verbatim(self):
        russian = self.tagline("ru")
        self.assertIn(russian, read("README.md"))
        self.assertIn(russian, read("docs/OVERVIEW.ru.md"))
        self.assertIn(russian, read("spec/SPECIFICATION.md"))

    def test_quickstart_experience_snippet_is_l1(self):
        section = read("docs/guides/QUICKSTART.md").split("## Start from an experience", 1)[1]
        block = re.search(r"```json\n(.*?)\n```", section, re.S).group(1)
        tmp = tempfile.mkdtemp(prefix="ohc-docs-")
        try:
            path = os.path.join(tmp, "context.json")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(block)
            report = check.run_context(path, level="L1", spec=helpers.spec())
            self.assertTrue(report["valid"], report["errors"])
            self.assertEqual(report["levelMet"], "L1")
            self.assertNotIn("claims", json.loads(block))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_ode_binding_examples_are_the_published_fragment(self):
        fragment = jsonio.load_json(os.path.join(ROOT, "examples", "kofi-gum-ode", "ode", "planner-binding.json"))
        ode = read("spec/bindings/ODE.md").split("## 3.", 1)[1]
        self.assertEqual(json.loads(re.search(r"```json\n(.*?)\n```", ode, re.S).group(1)), fragment)
        procedure = read("docs/agents/procedures/CONTEXT-07.md")
        block = re.search(r"```json\n(.*?)\n\s*```", procedure, re.S).group(1)
        self.assertEqual(json.loads(block), fragment)
        binding = fragment["extensions"]["ohc.binding"]
        self.assertNotIn("projection", binding)
        self.assertTrue(fragment["externalDependencies"][0]["objectId"].endswith("#" + binding["grantRef"]["id"]))

    def test_procedure_versions_agree(self):
        directory = os.path.join(ROOT, "docs", "agents", "procedures")
        versions = {}
        for name in sorted(os.listdir(directory)):
            head = read("docs/agents/procedures/" + name).splitlines()[0]
            match = re.match(r"^# (CONTEXT-\d\d) / (\d+\.\d+\.\d+) ", head)
            self.assertIsNotNone(match, name)
            versions[match.group(1)] = match.group(2)
            self.assertIn("**Procedure · %s ·" % match.group(2), read("docs/agents/procedures/" + name))
        for rel in ("AGENTS.md", "docs/agents/README.md"):
            listed = dict(re.findall(r"\[(CONTEXT-\d\d) / (\d+\.\d+\.\d+)\]", read(rel)))
            self.assertEqual(listed, versions, rel)

    def test_lens_section_is_generated(self):
        text = read("spec/LENSES.md")
        self.assertEqual(lens_tables.replace(text, lens_tables.render(ROOT)), text)


if __name__ == "__main__":
    unittest.main()
