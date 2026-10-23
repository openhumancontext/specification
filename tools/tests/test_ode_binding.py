"""Packaged OHC references must agree; schema validity never verifies live consent."""

import copy
import json
from pathlib import Path
import tempfile
import unittest

import helpers
import check
from ohclib import ode

ROOT = Path(helpers.repo_root())


class ODEBinding(unittest.TestCase):
    def setUp(self):
        self.fragment = json.loads((ROOT / "examples/kofi-gum-ode/ode/planner-binding.json").read_text())
        self.package = json.loads((ROOT / "examples/ohc-ode-tara/package/manifest.json").read_text())

    def findings(self, doc):
        result = check.Findings()
        ode.check_binding(doc, "binding.json", helpers.spec(), result)
        return {item["rule"] for item in result.items}

    def test_fragment_and_full_manifest(self):
        self.assertEqual(self.findings(self.fragment), set())
        self.assertEqual(self.findings(self.package), set())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(self.package))
            findings, _ = check.check_document(str(path), "manifest.json", helpers.spec())
            self.assertEqual(findings.items, [])

    def test_id_and_version_must_match(self):
        for key, value in (("objectId", "urn:ohc:example:kofi:context#g-other"), ("version", "2026-10-02T09:00:00Z")):
            with self.subTest(key=key):
                doc = copy.deepcopy(self.fragment)
                doc["externalDependencies"][0][key] = value
                self.assertIn("OB-2", self.findings(doc))

    def test_duplicate_target_even_at_another_version(self):
        dep = copy.deepcopy(self.fragment["externalDependencies"][0])
        dep["version"] = "2026-10-02T09:00:00Z"
        self.fragment["externalDependencies"].append(dep)
        self.assertIn("OB-2", self.findings(self.fragment))

    def test_context_cannot_be_absent_or_fragmented(self):
        for value in (None, "urn:ohc:example:kofi:context#other"):
            doc = copy.deepcopy(self.fragment)
            ref = doc["extensions"]["ohc.binding"]["grantRef"]
            if value is None:
                del ref["context"]
            else:
                ref["context"] = value
            self.assertIn("OB-1", self.findings(doc))

    def test_standard_declaration_must_be_unambiguous(self):
        for values in ([], self.package["standards"] * 2,
                       [{"id": "ohc", "url": "urn:ohc:specification", "revision": "other", "required": False}]):
            doc = copy.deepcopy(self.package)
            doc["standards"] = values
            self.assertTrue(self.findings(doc) & {"OB-3", "S-2"})

    def test_runtime_check_and_prohibitions_cannot_be_removed(self):
        for key, value in (("checkAtUse", False), ("prohibitedPurposes", ["advertising"])):
            doc = copy.deepcopy(self.package)
            doc["extensions"]["ohc.binding"][key] = value
            self.assertIn("S-2", self.findings(doc))
        self.package["requiredExtensions"] = []
        self.assertIn("S-2", self.findings(self.package))

    def test_standalone_value_is_not_a_verified_package(self):
        self.assertEqual(self.findings(self.fragment["extensions"]["ohc.binding"]), {"W-OB1"})

    def test_other_dependencies_and_extensions_can_coexist(self):
        self.package["externalDependencies"].append({"objectId": "urn:example:tool", "version": "1", "reason": "Synthetic dependency"})
        self.package["extensions"]["example.other"] = {"enabled": True}
        self.assertEqual(self.findings(self.package), set())

    def test_unsupported_ode_version_is_rejected(self):
        self.package["specVersion"] = "0.2.0-draft"
        self.assertIn("OB-4", self.findings(self.package))

    def test_current_crosswalk_does_not_turn_admission_into_agreement(self):
        rows = list((ROOT / "spec/mappings/ode").glob("*--ode-0.4.0-draft.2.mapping.json"))
        self.assertEqual(len(rows), 11)
        admission = json.loads((ROOT / "spec/catalogs/admission.json").read_text())
        self.assertNotIn('"ode"', json.dumps(admission))
        row = json.loads(next(p for p in rows if p.name.startswith("ohc.admission--")).read_text())
        self.assertIn("not-permitted", json.dumps(row))


if __name__ == "__main__":
    unittest.main()
