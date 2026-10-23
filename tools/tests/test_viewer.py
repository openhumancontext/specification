"""The static viewer: renders, readable without scripts, "view as" pages show exactly what §12.3 serves."""

import html.parser
import os
import re
import unittest

import helpers

import render_viewer
from ohclib import grants


class Page(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.h1 = 0
        self.ids = []
        self.data_ids = []
        self.external = []
        self.lang = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "h1":
            self.h1 += 1
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if "data-id" in attrs:
            self.data_ids.append(attrs["data-id"])
        for key in ("src", "href"):
            value = attrs.get(key) or ""
            if tag in ("script", "img", "link", "iframe") and value.startswith(("http:", "https:", "//")):
                self.external.append(value)


def parse(text):
    page = Page()
    page.feed(text)
    return page


class Viewer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = render_viewer.render_all(helpers.repo_root(), helpers.spec())
        cls.examples = render_viewer.load_examples(helpers.repo_root(), helpers.spec())

    def test_renders(self):
        self.assertIn("index.html", self.files)
        for example in self.examples:
            self.assertIn("%s/index.html" % example.person, self.files)
            for grantee in render_viewer.grantee_pages(example):
                self.assertIn("%s/as-%s/index.html" % (example.person, grantee), self.files)
        for name, text in self.files.items():
            with self.subTest(page=name):
                page = parse(text)
                self.assertEqual(page.h1, 1)
                self.assertEqual(len(page.ids), len(set(page.ids)))
                self.assertEqual(page.lang, "en")
                self.assertIn('content="noindex,nofollow"', text)
                self.assertEqual(page.external, [])
                self.assertNotIn("@import", text)

    def test_pinned_playbooks_are_shown(self):
        """A context that pins playbooks shows them by situation, readable without scripts (LENSES.md §2.2)."""
        for example in self.examples:
            pins = [p for p in example.ctx.manifest.get("playbooks") or [] if isinstance(p, dict)]
            text = re.sub(r"<script>.*?</script>", "", self.files["%s/index.html" % example.person], flags=re.S)
            with self.subTest(person=example.person):
                self.assertEqual("Ways of working (playbooks)" in text, bool(pins))
                for pin in pins:
                    self.assertIn(pin["id"], text)

    def test_content_present_with_scripts_stripped(self):
        for example in self.examples:
            text = re.sub(r"<script>.*?</script>", "", self.files["%s/index.html" % example.person], flags=re.S)
            with self.subTest(person=example.person):
                for heading in ("Needs grid", "Statements", "Episodes", "Then and now", "Tensions", "Lenses",
                                "Practices, outcomes and recall", "Grants", "Event log", "Legend"):
                    self.assertIn(">%s</h2>" % heading, text)
                for item in example.ctx.items:
                    if item.kind == "Claim" and item.data.get("text"):
                        self.assertIn(render_viewer.esc(item.data["text"]), text)
                self.assertIn("fictional", text)

    def test_controls_hidden_without_script(self):
        text = self.files["index.html"]
        self.assertIn('id="controls" hidden', text)

    def test_viewer_view_as_matches_projection(self):
        for example in self.examples:
            for grantee, grant_ids in render_viewer.grantee_pages(example).items():
                with self.subTest(person=example.person, grantee=grantee):
                    expected = set()
                    for grant_id in grant_ids:
                        projection, _denied = render_viewer.projection_for(example, grant_id)
                        if projection is not None:
                            expected |= grants.served_id_set(projection)
                    page = parse(self.files["%s/as-%s/index.html" % (example.person, grantee)])
                    self.assertEqual(set(page.data_ids), expected)
                    self.assertEqual(len(page.data_ids), len(set(page.data_ids)))
                    text = self.files["%s/as-%s/index.html" % (example.person, grantee)]
                    hidden = set(i.id for i in example.ctx.items if i.kind in ("Claim", "Interpretation", "Episode"))
                    for rid in hidden - expected:
                        self.assertIsNone(re.search(r"\b%s\b" % re.escape(rid), text), rid)
                    self.assertNotIn(example.ctx.subject_id, text)

    def test_view_as_withdrawn_grant_serves_nothing(self):
        noa = [e for e in self.examples if e.person == "noa"]
        if not noa:
            self.skipTest("Noa example missing")
        text = self.files["noa/as-s-02/index.html"]
        self.assertIn("Nothing is served", text)
        self.assertEqual(parse(text).data_ids, [])

    def test_viewer_deterministic(self):
        again = render_viewer.render_all(helpers.repo_root(), helpers.spec())
        self.assertEqual(again, self.files)


if __name__ == "__main__":
    unittest.main()
