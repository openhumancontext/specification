"""Erasure: notices to recipients, the Event chain across redaction, tombstones on restore, vault in exports."""

import copy
import hashlib
import os
import shutil
import tempfile
import unittest

import helpers

import convert_gum
from ohclib import events as ev
from ohclib import grants, jsonio, model

ROOT = helpers.repo_root()
NOA = os.path.join(ROOT, "examples", "noa-episode-first")
KOFI = os.path.join(ROOT, "examples", "kofi-gum-ode")


class Erasure(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ohc-erasure-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_erasure_notice_required(self):
        fixture = helpers.load_fixture(os.path.join(helpers.FIXTURES, "negative", "ev-6-erasure-without-notice.json"))
        report = helpers.run_fixture(fixture, os.path.join(self.tmp, "ev6"))
        self.assertEqual(helpers.error_rules(report), ["EV-6"])
        events = [e for _n, e in jsonio.load_jsonl(os.path.join(NOA, "events.jsonl"))]
        erased = [e for e in events if e.get("eventType") == "record-erased"]
        self.assertTrue(erased)
        self.assertTrue([e for e in events if e.get("eventType") == "erasure-notice-sent"])

    def test_chain_survives_erasure(self):
        events = [e for _n, e in jsonio.load_jsonl(os.path.join(NOA, "events.jsonl"))]
        self.assertTrue([e for e in events if e.get("redacted") is True])
        self.assertEqual(ev.verify_chain(events), [])
        redacted = copy.deepcopy(events)
        index = next(i for i, e in enumerate(redacted) if e.get("eventType") == "review-written")
        redacted[index] = ev.make_stub(redacted[index])
        self.assertEqual(ev.verify_chain(redacted), [])
        tampered = copy.deepcopy(events)
        tampered[index]["at"] = "2026-01-01T00:00:00Z"
        self.assertNotEqual(ev.verify_chain(tampered), [])

    def test_restore_reapplies_tombstones(self):
        tombstone = {"kind": "Tombstone", "id": "in-01", "erasedKind": "Interpretation",
                     "erasedAt": "2026-09-07T08:00:00Z", "erasedBy": "subject", "reason": "subject-request"}
        restored_reading = helpers.subj({"id": "in-01", "about": ["ep-01"], "stance": "retrospective",
                                         "text": "I skip when I have not eaten before class."}, "2026-09-06T08:00:00Z")
        report = helpers.run_fixture({"form": "single", "patches": [
            {"op": "set", "target": "interpretations", "path": "/@in-01", "value": tombstone},
            {"op": "add", "target": "interpretations", "path": "", "value": restored_reading}]},
            os.path.join(self.tmp, "restore"))
        self.assertIn("ID-2", helpers.error_rules(report))
        ctx = model.Context(os.path.join(self.tmp, "restore"), helpers.spec())
        state = model.State(ctx, model.parse_time("2026-09-06T12:00:00Z"))
        self.assertIn("in-01", state.tombstoned)
        grant = copy.deepcopy(ctx.record("g-01"))
        grant["interpretations"] = "all"
        grant["scope"]["include"].append({"kinds": ["Interpretation"]})
        served, _mode = grants.evaluate(state, grant, "a-01", "learning-support",
                                        model.parse_time("2026-09-06T12:00:00Z"))
        self.assertNotIn("in-01", [i.id for i in served])

    def test_export_includes_vault(self):
        out = os.path.join(self.tmp, "export")
        convert_gum.run_import(os.path.join(KOFI, "fixtures", "gum-snapshot-1.json"),
                               jsonio.load_json(os.path.join(KOFI, "importer-config.json")), out,
                               at="2026-09-28T10:05:00Z", seed="t")
        copy_dir = os.path.join(self.tmp, "copy")
        convert_gum.run_import(os.path.join(KOFI, "fixtures", "gum-snapshot-2.json"),
                               jsonio.load_json(os.path.join(KOFI, "importer-config.json")), copy_dir,
                               previous=out, at="2026-10-05T10:05:00Z", seed="t")
        ctx = model.Context(copy_dir, helpers.spec())
        sources = [i for i in ctx.items if i.kind == "Source"]
        self.assertTrue(sources)
        for item in sources:
            content = item.data["content"]
            path = os.path.join(copy_dir, content["locator"]["vaultPath"])
            self.assertTrue(os.path.isfile(path), path)
            with open(path, "rb") as handle:
                self.assertEqual(hashlib.sha256(handle.read()).hexdigest(), content["sha256"])
        lock = jsonio.load_json(os.path.join(copy_dir, "context.lock.json"))
        self.assertFalse([p for p in lock["files"] if p.startswith("vault/")])


if __name__ == "__main__":
    unittest.main()
