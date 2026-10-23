"""The catalog's basic playbooks (LENSES.md §2.2, PB-1, PB-2, PB-4): one per registry lens, in its lens's terms."""

import glob
import json
import os
import unittest

import helpers

ROOT = helpers.repo_root()
SLUGS = {"plan-week", "hard-conversation", "choose-between-options", "after-setback", "under-strain",
         "give-feedback", "look-back-at-an-episode"}


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def registry(folder, suffix):
    docs = [load(p) for p in sorted(glob.glob(os.path.join(ROOT, "spec", folder, "*.%s.json" % suffix)))]
    return {doc["id"]: doc for doc in docs}


class Playbooks(unittest.TestCase):
    def setUp(self):
        self.lenses = registry("lenses", "lens")
        self.playbooks = registry("playbooks", "playbook")

    def test_one_basic_playbook_per_lens(self):
        self.assertEqual(len(self.lenses), 16)
        self.assertEqual(len(self.playbooks), len(self.lenses))
        for lens_id, lens in self.lenses.items():
            name = lens_id.rsplit(":", 1)[-1]
            self.assertEqual(lens.get("playbooks"), ["urn:ohc:playbook:%s-basic" % name], lens_id)
            playbook = self.playbooks["urn:ohc:playbook:%s-basic" % name]
            self.assertEqual(playbook["lenses"], [lens_id])
            self.assertEqual(playbook["author"], "OHC editors")
            self.assertEqual(playbook["sources"], lens.get("sources") or [])

    def test_shared_situations_and_step_counts(self):
        for playbook_id, playbook in self.playbooks.items():
            situations = playbook["situations"]
            self.assertTrue(3 <= len(situations) <= 6, playbook_id)
            for situation in situations:
                self.assertIn(situation["id"], SLUGS, playbook_id)
                self.assertEqual(len(situation["use"]["en"]), len(situation["use"]["ru"]), playbook_id)
                self.assertTrue(2 <= len(situation["use"]["en"]) <= 5, playbook_id)

    def test_frames_never_present_content_as_fact(self):
        # PB-4: a playbook of a symbolic frame or a T5 lens says so in a watchFor of every situation.
        for lens_id, lens in self.lenses.items():
            evidence = lens.get("evidence") or {}
            if evidence.get("ontologicalStatus") != "symbolic-frame" and evidence.get("measurementTier") != "T5":
                continue
            playbook = self.playbooks[lens["playbooks"][0]]
            for situation in playbook["situations"]:
                self.assertIn("watchFor", situation, lens_id)


if __name__ == "__main__":
    unittest.main()
