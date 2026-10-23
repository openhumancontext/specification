"""Every JSON example in SPECIFICATION.md is taken from a published example and stays equal to it (§1.5)."""

import json
import os
import re
import unittest

import helpers

from ohclib import jsonio

ROOT = helpers.repo_root()
SPEC = os.path.join(ROOT, "spec", "SPECIFICATION.md")
NOA = os.path.join(ROOT, "examples", "noa-episode-first")
KOFI = os.path.join(ROOT, "examples", "kofi-gum-ode", "context")


def _jsonl(path):
    return [record for _n, record in jsonio.load_jsonl(path)]


class SpecExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(SPEC, encoding="utf-8") as handle:
            text = handle.read()
        cls.blocks = [json.loads(m.group(1)) for m in re.finditer(r"```json\n(.*?)\n```", text, re.S)]
        cls.records = {}
        for name in sorted(os.listdir(os.path.join(NOA, "records"))):
            for record in _jsonl(os.path.join(NOA, "records", name)):
                cls.records[record["id"]] = record
        cls.events = _jsonl(os.path.join(NOA, "events.jsonl"))
        for record in cls.events:
            cls.records[record["id"]] = record
        for name in sorted(os.listdir(os.path.join(NOA, "projections"))):
            projection = jsonio.load_json(os.path.join(NOA, "projections", name))
            cls.records[projection["id"]] = projection
        cls.manifest = jsonio.load_json(os.path.join(NOA, "context.json"))
        cls.lock = jsonio.load_json(os.path.join(NOA, "context.lock.json"))
        cls.kofi_manifest = jsonio.load_json(os.path.join(KOFI, "context.json"))
        cls.kofi_assessments = dict((r["id"], r) for r in _jsonl(os.path.join(KOFI, "records", "assessments.jsonl")))

    def expected(self, block):
        """The published object this example shows, or None."""
        if block.get("format") == "ohc.context":
            return None  # checked separately: an illustration built from the Noa manifest
        if block.get("format") == "ohc.lock":
            return dict(dict((k, v) for k, v in self.lock.items() if k != "files"),
                        files=dict((k, self.lock["files"][k]) for k in block.get("files", {})))
        if str(block.get("id", "")).startswith("urn:") and "aliases" in block:
            return self.manifest["subject"]
        if block.get("partyKind"):
            return next((p for p in self.kofi_manifest["parties"] if p["id"] == block.get("id")), None)
        if block.get("id") == "as-01":
            record = dict(self.kofi_assessments["as-01"])
            record.pop("kind")
            shown = [r["construct"] for r in block.get("results", [])]
            record["results"] = [r for r in record["results"] if r["construct"] in shown]
            return record
        record = self.records.get(block.get("id"))
        if record is None:
            return None
        record = dict(record)
        if record.get("kind") != "Tombstone":
            record.pop("kind", None)
        return record

    def test_every_example_is_published(self):
        self.assertGreaterEqual(len(self.blocks), 25)
        for block in self.blocks:
            if block.get("format") == "ohc.context":
                continue
            with self.subTest(example=block.get("id") or block.get("format")):
                self.assertEqual(block, self.expected(block))

    def test_context_example_is_the_noa_manifest(self):
        contexts = [b for b in self.blocks if b.get("format") == "ohc.context"]
        self.assertEqual(len(contexts), 1)
        block = contexts[0]
        for key in ("id", "version", "parties", "policy", "lenses", "holder", "lang", "created"):
            self.assertEqual(block[key], self.manifest[key], key)
        self.assertEqual(block["subject"]["id"], self.manifest["subject"]["id"])
        self.assertTrue(block["conformance"]["subjectIsAdult"])
        errors = helpers.spec().validate("urn:ohc:schema:context:0.1.0-draft", block)
        self.assertEqual(errors, [])

    def test_assessment_example_is_abridged_only_in_results(self):
        block = next(b for b in self.blocks if b.get("id") == "as-01")
        published = self.kofi_assessments["as-01"]["results"]
        for result in block["results"]:
            self.assertIn(result, published)


if __name__ == "__main__":
    unittest.main()
