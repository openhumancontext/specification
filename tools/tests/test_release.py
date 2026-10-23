"""Release manifest and REL checks, the private denylist and the export tree."""

import json
import os
import shutil
import tempfile
import unittest

import helpers

import build_release_manifest as brm
import check

ROOT = helpers.repo_root()


class Release(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = brm.load_plan(ROOT)
        cls.manifest = brm.build_manifest(ROOT, cls.plan)
        cls.findings = brm.release_findings(ROOT, check.Findings).items

    def rules(self, rule):
        return [f for f in self.findings if f["rule"] == rule]

    def test_licensing_map_identical(self):
        rules, default = brm.licensing_md_rules(ROOT)
        self.assertEqual(rules, self.plan["licensing"]["rules"])
        self.assertEqual(default, self.plan["licensing"]["default"])
        expected = ["README.md", "STATUS.md", "CONTRIBUTING.md", "CHANGELOG.md", "LICENSING.md", "CONTRIBUTORS.md",
                    "AGENTS.md", "spec/COMPOSITION.md", "spec/glossary.json", "docs/**"]
        self.assertEqual([r["glob"] for r in rules], expected)
        self.assertEqual(set(r["license"] for r in rules), {"CC-BY-4.0"})
        self.assertEqual(self.manifest["files"]["README.md"]["license"], "CC-BY-4.0")
        self.assertEqual(self.manifest["files"]["spec/SPECIFICATION.md"]["license"], "Apache-2.0")
        self.assertEqual(self.rules("REL-3"), [])

    def test_internal_excluded(self):
        tree = brm.PRIVATE_TREE
        self.assertIn(tree + "/**", self.plan["exclude"])
        self.assertFalse([p for p in self.manifest["files"] if p.split("/")[0] == tree])
        self.assertTrue(self.manifest["flags"]["internalExcluded"])
        self.assertEqual(self.rules("REL-2"), [])

    def test_banned_strings(self):
        denylist = brm.load_denylist(ROOT)
        if denylist is None:
            # Fail closed: without the private list the release is never reported clean.
            self.assertTrue([f for f in self.rules("REL-5") if "denylist" in f["path"]])
            self.assertFalse(self.manifest["flags"]["privateMarkersAndCredentialPatternScan"])
        else:
            self.assertEqual(self.rules("REL-5"), [])
            self.assertTrue(self.manifest["flags"]["privateMarkersAndCredentialPatternScan"])
        samples = ["/Us" + "ers/someone", "local" + "host:8080", "write to someone" + "@" + "example.org",
                   "AKIA" + "ABCDEFGHIJKLMNOP", "-----BEGIN " + "PRIVATE KEY-----"]
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertTrue(brm.scan_text("x.md", sample))
        for clean in ("Taras Pustovoy and contributors", "lenses/cbt" + "@0.1.0.lens.json", "Setting up", "Tarot"):
            with self.subTest(clean=clean):
                self.assertEqual(brm.scan_text("x.md", clean, denylist), [])
        self.assertEqual(brm.scan_text("release-plan.json", brm.PRIVATE_TREE + "/**"), [])
        self.assertTrue(brm.scan_text("README.md", brm.PRIVATE_TREE + "/**"))
        self.assertTrue(brm.scan_text("tools/x.py", "see " + "F" + ".3 for the algorithm"))
        self.assertEqual(brm.scan_text("tools/x.py", "see §12.3 and version 0.1.0"), [])

    def test_private_markers_are_not_in_the_release(self):
        """The marker list lives outside the repository; a synthetic list shows how it is applied."""
        tmp = tempfile.mkdtemp(prefix="ohc-deny-")
        try:
            path = os.path.join(tmp, "deny.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump({"format": brm.DENYLIST_FORMAT, "patterns": [
                    {"group": "test", "regex": "Zorb" + "lax", "ignoreCase": True}]}, handle)
            previous = os.environ.get(brm.DENYLIST_ENV)
            os.environ[brm.DENYLIST_ENV] = path
            try:
                denylist = brm.load_denylist(ROOT)
            finally:
                if previous is None:
                    del os.environ[brm.DENYLIST_ENV]
                else:
                    os.environ[brm.DENYLIST_ENV] = previous
            self.assertTrue(brm.scan_text("x.md", "the zorb" + "lax project", denylist))
            self.assertEqual(brm.scan_text("x.md", "the zorb" + "lax project"), [])
            self.assertEqual(sorted(set(group for group, _p in brm.FORBIDDEN)), ["paths-and-hosts", "personal"])
            self.assertIn(brm.DENYLIST_FILE, self.plan["exclude"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_export_tree_has_no_private_tree(self):
        tmp = tempfile.mkdtemp(prefix="ohc-export-")
        try:
            out = os.path.join(tmp, "tree")
            os.makedirs(os.path.join(out, brm.PRIVATE_TREE))
            with open(os.path.join(out, brm.PRIVATE_TREE, "x.md"), "w") as handle:
                handle.write("x")
            self.assertEqual([f["rule"] for f in brm.export_findings(out, check.Findings()).items], ["REL-7"])
            clean = os.path.join(tmp, "clean")
            os.makedirs(clean)
            self.assertEqual(brm.export_findings(clean, check.Findings()).items, [])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_footer_present(self):
        self.assertEqual(self.rules("REL-4"), [])
        cc = "# Title\n\nText.\n\n---\n" + brm.FOOTERS["CC-BY-4.0"] + "\n"
        self.assertTrue(brm.footer_ok(cc, "CC-BY-4.0"))
        self.assertFalse(brm.footer_ok(cc, "Apache-2.0"))
        self.assertFalse(brm.footer_ok("# Title\n", "CC-BY-4.0"))

    def test_manifest_shape_and_determinism(self):
        spec = helpers.spec()
        self.assertEqual(spec.validate("urn:ohc:schema:release-manifest:0.1.0-draft", self.manifest), [])
        self.assertEqual(spec.validate("urn:ohc:schema:release-plan:0.1.0-draft", self.plan), [])
        self.assertEqual(brm.build_manifest(ROOT, self.plan), self.manifest)
        self.assertEqual(self.manifest["format"], "ohc.public-export/1")
        self.assertEqual(self.manifest["rightsHolder"], "Taras Pustovoy and contributors")
        self.assertEqual(self.manifest["licenseStatus"], "approved-by-owner")
        flags = self.manifest["flags"]
        self.assertFalse(flags["realPersonDataIncluded"])
        self.assertFalse(flags["liveRuntimeTested"])
        self.assertTrue(flags["referenceToolsDistributed"])
        self.assertNotIn(brm.MANIFEST, self.manifest["files"])
        self.assertIn(brm.PLAN, self.manifest["files"])

    def test_only_the_release_step_is_pending(self):
        findings = self.findings
        if brm.load_denylist(ROOT) is None:
            findings = [f for f in findings if not (f["rule"] == "REL-5" and "denylist" in f["path"])]
            findings = [f for f in findings if not (f["rule"] == "REL-6" and f["path"].endswith(
                "privateMarkersAndCredentialPatternScan"))]
        pending = [f for f in findings if not (f["rule"] == "REL-1" and f["path"] == brm.MANIFEST)]
        if os.path.isfile(os.path.join(ROOT, brm.MANIFEST)):
            self.assertEqual(findings, [])
        else:
            self.assertEqual(pending, [])

    def test_playbooks_in_the_release_and_the_private_tree_out(self):
        files = self.manifest["files"]
        self.assertTrue([p for p in files if p.startswith("spec/playbooks/") and p.endswith(".playbook.json")])
        self.assertEqual([p for p in files if p.startswith(brm.PRIVATE_TREE + "/")], [])

    def test_tests_that_read_the_private_tree_skip_without_it(self):
        """A released copy has no private tree: every test that reads it checks first and skips otherwise."""
        here = os.path.join(ROOT, "tools", "tests")
        for name in sorted(os.listdir(here)):
            if not (name.startswith("test_") and name.endswith(".py")):
                continue
            with open(os.path.join(here, name), "r", encoding="utf-8") as handle:
                text = handle.read()
            if "PRIVATE_TREE" in text.replace("brm.PRIVATE_TREE + \"/\"", "") or "\"inter\" + \"nal\"" in text:
                with self.subTest(test=name):
                    self.assertTrue("isdir" in text or "isfile" in text, name)
                    self.assertTrue("skip" in text.lower(), name)

    def test_glob_semantics(self):
        self.assertTrue(brm.glob_match("docs/**", "docs/agents/x.md"))
        self.assertFalse(brm.glob_match("README.md", "examples/noa/README.md"))
        self.assertTrue(brm.glob_match("**/*.pyc", "a.pyc"))
        self.assertTrue(brm.glob_match("**/__pycache__/**", "tools/__pycache__/x.pyc"))
        self.assertFalse(brm.glob_match("spec/*.md", "spec/bindings/GUM.md"))


if __name__ == "__main__":
    unittest.main()
