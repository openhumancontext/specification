"""Schemas: valid draft 2020-12, the $id scheme, header order, enums equal the catalogs (S-4), self-test."""

import glob
import os
import unittest

import helpers
from jsonschema import Draft202012Validator

import check
from ohclib import jsonio

SCHEMA_DIR = os.path.join(helpers.repo_root(), "spec", "schema")


class Schemas(unittest.TestCase):
    def schema_files(self):
        files = sorted(glob.glob(os.path.join(SCHEMA_DIR, "*.schema.json")))
        self.assertTrue(files)
        return files

    def test_every_schema_is_valid_2020_12(self):
        for path in self.schema_files():
            with self.subTest(schema=os.path.basename(path)):
                Draft202012Validator.check_schema(jsonio.load_json(path))

    def test_id_scheme(self):
        for path in self.schema_files():
            name = os.path.basename(path)[:-len(".schema.json")]
            with self.subTest(schema=name):
                self.assertEqual(jsonio.load_json(path)["$id"], "urn:ohc:schema:%s:0.1.0-draft" % name)

    def test_header_order(self):
        for path in self.schema_files():
            with self.subTest(schema=os.path.basename(path)):
                keys = list(jsonio.load_json(path).keys())[:4]
                self.assertEqual(keys, ["$schema", "$id", "title", "description"])

    def test_index_lists_every_schema(self):
        spec = helpers.spec()
        listed = set(os.path.normpath(p) for p in spec.schema_paths.values())
        for path in self.schema_files():
            self.assertIn(os.path.normpath(path), listed)

    def test_enums_equal_catalogs(self):
        spec = helpers.spec()
        self.assertEqual(jsonio.dumps_pretty(spec.regenerate_common()), jsonio.dumps_pretty(spec.common))

    def test_self_test_passes(self):
        report = check.report_for_findings(check.self_test(helpers.spec()))
        self.assertEqual(report["errors"], [])
        self.assertTrue(report["valid"])


if __name__ == "__main__":
    unittest.main()
