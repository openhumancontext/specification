"""RFC 8785 test vectors and the R-S1 single-document / package round-trip."""

import json
import os
import shutil
import tempfile
import unittest

import helpers
from jcs_vectors import NUMBER_VECTORS, SORTING_INPUT, SORTING_ORDER, STRUCTURE_INPUT, STRUCTURE_OUTPUT

from ohclib import jcs, model


class Rfc8785(unittest.TestCase):
    def test_number_vectors(self):
        for hex_value, expected in NUMBER_VECTORS:
            with self.subTest(ieee=hex_value):
                number = jcs.number_from_ieee_hex(hex_value)
                if expected is None:
                    with self.assertRaises(jcs.JcsError):
                        jcs.format_number(number)
                else:
                    self.assertEqual(jcs.format_number(number), expected)

    def test_structure_example(self):
        self.assertEqual(jcs.canonicalize(json.loads(STRUCTURE_INPUT)), STRUCTURE_OUTPUT)

    def test_property_sorting_by_utf16(self):
        canonical = jcs.canonicalize(json.loads(SORTING_INPUT))
        self.assertEqual(list(json.loads(canonical).keys()), SORTING_ORDER)

    def test_digest_prefix(self):
        self.assertTrue(jcs.digest({"a": 1}).startswith("sha256:"))
        self.assertEqual(len(jcs.digest({"a": 1})), 7 + 64)


def records_by_id(ctx):
    out = {}
    for item in ctx.items:
        if item.kind == "Event":
            continue
        record = dict((k, v) for k, v in item.data.items() if k != "kind")
        out[item.id] = jcs.canonicalize(record)
    return out


class SinglePackageRoundTrip(unittest.TestCase):
    """R-S1: the two serializations carry the same records."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ohc-rs1-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_single_to_package_and_back(self):
        spec = helpers.spec()
        single_dir = helpers.materialize(os.path.join(self.tmp, "single"), form="single")
        single = model.Context(single_dir, spec)
        # single -> package
        state = {"manifest": dict((k, v) for k, v in single.manifest.items() if k not in spec.collection_kind),
                 "records": {}, "events": helpers.chain(helpers.BASE_EVENTS), "projections": {}}
        for item in single.items:
            state["records"].setdefault(item.collection, []).append(item.data)
        package_dir = os.path.join(self.tmp, "package")
        helpers.write_files(package_dir, helpers.package_files(state))
        helpers.write_files(package_dir, {helpers.VAULT_PATH: helpers.VAULT_TEXT})
        package = model.Context(package_dir, spec)
        self.assertEqual(records_by_id(single), records_by_id(package))
        # package -> single
        back = dict(package.manifest)
        back.pop("collections")
        for item in package.items:
            if item.kind != "Event":
                back.setdefault(item.collection, []).append(item.data)
        again_dir = os.path.join(self.tmp, "again")
        helpers.write_files(again_dir, {"context.json": back, helpers.VAULT_PATH: helpers.VAULT_TEXT})
        again = model.Context(again_dir, spec)
        self.assertEqual(records_by_id(again), records_by_id(single))
        self.assertTrue(helpers.run_check(again_dir)["valid"])


if __name__ == "__main__":
    unittest.main()
