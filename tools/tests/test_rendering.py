"""The session-start rendering for a persistent agent (CONTEXT-03 0.2.0, PB-5) and the MCP read that stays as it
was (``get_user_context``). Synthetic people only."""

import os
import shutil
import tempfile
import unittest

import importkit
from importkit import HEXACO

import convert_gum
from ohclib import grants, jsonio, model, rendering, window
from ohclib.package import Package

AGREE_AT = "2026-10-12T09:18:00Z"
SERVE_AT = "2026-10-13T07:00:00Z"


class Rendering(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ohc-render-")
        self.spec = importkit.write_registry(self.tmp)
        self.pkg, self.ids = importkit.person_with_results(self.tmp, self.spec)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def ctx(self):
        return model.Context(self.pkg, self.spec)

    def agree(self, gid="g-01", **choices):
        view = window.screen(self.ctx(), "a-01", "assist-personal", model.parse_time(AGREE_AT))
        grant = window.build_grant(view, AGREE_AT, gid, **choices)
        package = Package(self.pkg, self.spec)
        window.confirm_grant(package, grant)
        package.save(AGREE_AT)
        return grant

    def render(self, gid="g-01"):
        ctx = self.ctx()
        projection = grants.build_projection(ctx, gid, "assist-personal", model.parse_time(SERVE_AT), "prj-0001",
                                             holder_key=grants.EXAMPLE_HOLDER_KEY, nonce="n")
        return projection, rendering.render_agent(ctx, projection, ctx.record(gid))

    @staticmethod
    def block(text, start, end):
        return text[text.index(start):text.index(end)]

    def test_rendering_sections_in_order(self):
        grant = self.agree()
        _projection, text = self.render()
        heads = ["OHC · Personal agent · grant g-01 · personal assistance · 13 Oct 2026 07:00 UTC · notes until "
                 "9 Apr 2027", "What the person said — act on these", "Their results", "How to speak about them",
                 "Ways of working", "Your agreement with the person"]
        positions = [text.index(h) for h in heads]
        self.assertEqual(positions, sorted(positions))
        words = self.block(text, heads[1], heads[2])
        self.assertIn("✓ \"Give me the decision first, in one paragraph.\"", words)
        self.assertIn("✓ \"When you lay out options, show me the evidence behind each one.\"", words)
        results = self.block(text, heads[2], heads[3])
        self.assertIn("◐ BFI-2 · Big Five (Five-Factor Model) · the person said parts fit", results)
        self.assertIn("Fits: Conscientiousness. Does not fit: Extraversion.", results)
        self.assertIn("     ✓ Conscientiousness 4.2", results)
        self.assertIn("     ✗ Extraversion", results)
        self.assertIn("     ? Openness", results)  # not said (PJ-8)
        self.assertIn("~ HEXACO-PI-R", results)
        self.assertIn("ask before relying on any scale", results)
        self.assertIn("norm group Test norms", results)
        self.assertIn("Honesty-Humility percentile 61", results)
        self.assertIn("The test: Measured, with independent research", results)
        speaking = self.block(text, heads[3], heads[4])
        self.assertIn("Tools you may offer: Fit check — ", speaking)
        self.assertIn("Never: present a score as evidence of fit for a job or role", speaking)
        agreement = text[text.index(heads[5]):]
        self.assertIn("\"%s\"" % grant["basis"]["note"], agreement)  # the disclosure, verbatim
        self.assertIn("may weigh: BFI-2 Conscientiousness.", agreement)
        self.assertIn("Ask them first before weighing: BFI-2 Openness; HEXACO-PI-R.", agreement)
        self.assertIn("Do not weigh or ask again: BFI-2 Extraversion (they said it does not fit", agreement)
        self.assertIn("Keep your notes until 9 Apr 2027", agreement)

    def test_rendering_playbooks(self):
        self.agree()
        _projection, text = self.render()
        block = self.block(text, "Ways of working", "Your agreement with the person")
        self.assertIn("Your agreement: guesses — yes · weighing accepted results — yes", block)
        self.assertIn("their words above come first", block)
        self.assertIn("Your own crisis protocol comes before any step.", block)
        self.assertEqual(block.count("  Planning a week\n"), 1)  # grouped by situation across lenses
        self.assertEqual(block.count("  Looking back at an episode\n"), 1)
        self.assertIn("    HEXACO: basic ways of working (OHC editors) · the person is not sure it fits: ask first",
                      block)
        self.assertIn("Watch for: A score is a dated reading", block)
        self.assertIn("Draws on: Conscientiousness, Extraversion (they said it does not fit).", block)
        self.assertLess(block.index("Big Five: basic"), block.index("HEXACO: basic"))

    def test_rendering_grant_line(self):
        self.agree()
        _p, full = self.render()
        self.agree(gid="g-02", toggles={"hypotheses": False, "weighing": False})
        _p, narrow = self.render("g-02")
        self.assertIn("guesses — no · weighing accepted results — no", narrow)
        steps = lambda text: self.block(text, "  Planning a week", "Your agreement with the person")  # noqa: E731
        self.assertEqual(steps(full), steps(narrow))  # the playbook text does not change
        self.assertIn("No guesses about them", narrow)
        self.assertIn("none grounds a choice you make or propose for them", narrow)

    def test_unticked_lens_brings_no_playbook(self):
        self.agree(rows={self.ids["hexaco"]: False})
        projection, text = self.render()
        self.assertNotIn("HEXACO", text)
        self.assertIn("Big Five: basic ways of working", text)
        self.assertNotIn(self.ids["hexaco"], grants.served_id_set(projection))

    def test_adoption_with_no_playbooks_renders_none_for_that_lens(self):
        package = Package(self.pkg, self.spec)
        window.choose_playbooks(package, self.ctx(), HEXACO, [], "2026-10-12T09:12:00Z")
        package.save("2026-10-12T09:12:00Z")
        self.agree()
        _p, text = self.render()
        self.assertNotIn("HEXACO: basic ways of working", text)
        self.assertIn("Big Five: basic ways of working", text)

    def test_unpinned_playbook_is_left_out(self):
        manifest_path = os.path.join(self.pkg, "context.json")
        manifest = jsonio.load_json(manifest_path)
        manifest["playbooks"] = [p for p in manifest["playbooks"] if "hexaco" not in p["id"]]
        jsonio.write_pretty(manifest_path, manifest)
        self.agree()
        _p, text = self.render()
        self.assertNotIn("HEXACO: basic ways of working", text)

    def test_playbooks_never_enter_a_projection(self):
        self.agree()
        with_pins, _text = self.render()
        manifest_path = os.path.join(self.pkg, "context.json")
        manifest = jsonio.load_json(manifest_path)
        manifest.pop("playbooks")
        jsonio.write_pretty(manifest_path, manifest)
        without, text = self.render()
        self.assertEqual(with_pins, without)
        self.assertNotIn("Ways of working", text)

    def test_rendering_is_a_pure_function(self):
        self.agree()
        before = sorted(os.listdir(self.pkg))
        first = self.render()
        self.assertEqual(first, self.render())
        self.assertEqual(sorted(os.listdir(self.pkg)), before)

    def test_get_user_context_stays_compatible(self):
        """The MCP read serves no special records: results and the words that cite them never leave by it."""
        self.agree()
        ctx = self.ctx()
        out = convert_gum.get_user_context(ctx, caller="a-01", grant_id="g-01", query="decision first",
                                           now=model.parse_time(SERVE_AT))
        self.assertIn("• Give me the decision first, in one paragraph.", out)
        self.assertIn("Reasoning: Declared by the person.", out)
        for leak in ("evidence behind each one", "Conscientiousness", "4.2", "percentile"):
            self.assertNotIn(leak, out)
        self.assertEqual(convert_gum.get_user_context(ctx, caller=None, grant_id="g-01"), "")


if __name__ == "__main__":
    unittest.main()
