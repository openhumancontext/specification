"""The person's window (IMH-1; §12.1, §15.5): stance and words, the agreement screen with everything ticked by
default, confirmation as consent, preview of what the agent receives, and changing one's mind later (withdraw,
erase, correct, retake, playbooks). Synthetic people only."""

import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

import helpers
import importkit
from importkit import BIG_FIVE, HEXACO

import check
import import_assessment
import ohc_holder
import ohc_query
from ohclib import grants, jsonio, model, window
from ohclib.package import Package

AGREE_AT = "2026-10-12T09:18:00Z"
SERVE_AT = "2026-10-13T07:00:00Z"


class Holder(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ohc-holder-")
        self.spec = importkit.write_registry(self.tmp)
        self.pkg, self.ids = importkit.person_with_results(self.tmp, self.spec)
        self.outbox = os.path.join(self.tmp, "outbox")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def ctx(self):
        return model.Context(self.pkg, self.spec)

    def view(self, operator=None, at=AGREE_AT):
        return window.screen(self.ctx(), "a-01", "assist-personal", model.parse_time(at), operator=operator)

    def agree(self, gid="g-01", at=AGREE_AT, **choices):
        grant = window.build_grant(self.view(at=at), at, gid, **choices)
        package = Package(self.pkg, self.spec)
        window.confirm_grant(package, grant, seed="t")
        package.save(at)
        return grant

    def project(self, gid="g-01", at=SERVE_AT):
        return grants.build_projection(self.ctx(), gid, "assist-personal", model.parse_time(at), "prj-0001",
                                       holder_key=grants.EXAMPLE_HOLDER_KEY, nonce="n")

    def assertValid(self):
        report = check.run_context(self.pkg, spec=self.spec)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["levelMet"], "L2")
        return report

    # ------------------------------------------------------------ stance and words
    def test_stances_become_reviews(self):
        state = model.State(self.ctx())
        self.assertEqual(state.derived(self.ids["bfi"], model.parse_time(SERVE_AT))["label"], "partly-confirmed")
        self.assertEqual(state.status[self.ids["bfi"]].endorsed_part,
                         "Fits: Conscientiousness. Does not fit: Extraversion. "
                         "\"I am quieter than this says.\"")  # Openness: not said (PJ-8)
        self.assertEqual(state.derived(self.ids["hexaco"], model.parse_time(SERVE_AT))["label"], "hypothesis")
        expected = {"fits": ("endorse", "confirmed"), "dispute": ("contest", None),
                    "doesnt-fit": ("reject", None), "later": (None, "pending")}
        for stance, (action, label) in expected.items():
            pkg = importkit.new_package(os.path.join(self.tmp, stance), self.spec)
            import_assessment.import_result(pkg, [importkit.bfi_draft(self.spec)], importkit.AT, spec=self.spec,
                                            synthetic=True)
            package = Package(pkg, self.spec)
            review = window.record_stance(package, "as-01", stance, "2026-10-12T09:30:00Z")
            package.save("2026-10-12T09:30:00Z")
            self.assertEqual(package.record(review)["action"] if review else None, action, stance)
            derived = model.State(model.Context(pkg, self.spec)).derived("as-01", model.parse_time(SERVE_AT))
            if label:
                self.assertEqual(derived["label"], label, stance)
            self.assertTrue(check.run_context(pkg, spec=self.spec)["valid"], stance)
        with self.assertRaises(window.Refused):
            window.record_stance(Package(self.pkg, self.spec), self.ids["bfi"], "parts", AGREE_AT, fits=[])

    def test_words_with_and_without_the_result(self):
        state = model.State(self.ctx())
        self.assertEqual(state.tier(self.ids["words"]), "special")  # cites a special result (C3)
        self.assertEqual(state.tier("c-01"), "personal")
        self.assertValid()

    # ------------------------------------------------------------ the screen
    def test_screen_defaults(self):
        view = self.view()
        self.assertTrue(all(r["ticked"] for r in view["rows"]))
        self.assertTrue(all(w["ticked"] for w in view["otherWords"]))
        self.assertEqual(view["toggles"], {"hypotheses": True, "weighing": True, "notes": True})
        self.assertEqual(len(view["neverPurposes"]), 13)
        text = window.render_screen(view)
        self.assertEqual(text.count("ways of working: "), 2)
        self.assertIn("ways of working: basic (OHC editors) · change them", text)
        self.assertIn(" [x] a. ", text)
        self.assertIn("each is ticked; untick what you don't want", text)
        self.assertIn("you said parts fit: Conscientiousness fit; Extraversion does not;", text)
        self.assertIn("with your words: \"When you lay out options", text)
        self.assertIn("Protected like mental health data.", text)
        self.assertIn("Does not show:", text)
        self.assertIn(window.NEVER_TEXT, text)  # one plain sentence; the codes stay in the catalog (§8.10)
        self.assertNotIn("`", text)
        employer = self.view(operator="employer")
        self.assertFalse(any(r["ticked"] for r in employer["rows"]))
        self.assertFalse(any(w["ticked"] for w in employer["otherWords"]))
        self.assertEqual(employer["toggles"], {"hypotheses": False, "weighing": False, "notes": False})
        self.assertIn("run by your employer: nothing is ticked for you", window.render_screen(employer))

    def test_grant_from_the_default_screen(self):
        grant = self.agree()
        self.assertEqual(grant["scope"], {"include": [{"lenses": [BIG_FIVE, HEXACO]},
                                                      {"facets": ["goal", "preference", "boundary"]},
                                                      {"ids": [self.ids["words"]]}]})
        self.assertEqual(grant["actions"], ["read", "suggest", "infer"])
        self.assertEqual(grant["constraints"], {"expiresAt": "2027-04-09T09:18:00Z", "storage": "until-expiry",
                                                "forwarding": False, "crossContextUse": False,
                                                "decisionUse": "approval-required", "delegable": False})
        self.assertEqual(grant["basis"]["legal"], "explicit-consent")
        self.assertEqual(grant["expressedBy"], {"actor": "subject", "at": AGREE_AT, "channel": "holder-ui"})
        self.assertNotIn("HEXACO", grant["basis"]["note"])  # the disclosure names no lens
        events = Package(self.pkg, self.spec).events
        self.assertEqual(events[-1]["eventType"], "grant-given")
        self.assertEqual(events[-1]["counterparty"], "a-01")
        self.assertValid()
        projection = self.project()
        served = grants.served_id_set(projection)
        self.assertTrue({self.ids["bfi"], self.ids["hexaco"], self.ids["words"], "c-01"} <= served)
        self.assertEqual(projection["obligations"]["decisionUse"], "approval-required")

    def test_unticking(self):
        grant = self.agree(rows={self.ids["hexaco"]: False}, toggles={"hypotheses": False, "weighing": False,
                                                                       "notes": False})
        self.assertEqual(grant["actions"], ["read"])
        self.assertNotIn("decisionUse", grant["constraints"])
        self.assertEqual(grant["constraints"]["storage"], "session")
        self.assertEqual(grant["scope"]["include"][0], {"lenses": [BIG_FIVE]})
        self.assertValid()
        projection = self.project()
        self.assertNotIn(self.ids["hexaco"], grants.served_id_set(projection))
        self.assertEqual(projection["obligations"]["decisionUse"], "deny")
        with self.assertRaises(window.Refused):
            window.build_grant(self.view(), AGREE_AT, "g-09", rows={self.ids["bfi"]: False,
                                                                     self.ids["hexaco"]: False},
                               words={"c-01": False})

    def test_result_that_does_not_fit_is_not_on_offer(self):
        package = Package(self.pkg, self.spec)
        window.record_stance(package, self.ids["hexaco"], "doesnt-fit", "2026-10-12T09:15:00Z")
        package.save("2026-10-12T09:15:00Z")
        view = self.view()
        row = [r for r in view["rows"] if r["id"] == self.ids["hexaco"]][0]
        self.assertEqual((row["servable"], row["ticked"]), (False, False))
        self.assertIn("you said it doesn't fit — only you see it", window.render_screen(view))
        grant = window.build_grant(view, AGREE_AT, "g-01", rows={self.ids["hexaco"]: True})
        self.assertEqual(grant["scope"]["include"][0], {"lenses": [BIG_FIVE]})

    # ------------------------------------------------------------ preview (H-15)
    def test_preview_equals_project(self):
        grant = window.build_grant(self.view(), AGREE_AT, "g-01", rows={self.ids["hexaco"]: False})
        before = os.listdir(self.pkg)
        draft = window.preview(self.ctx(), grant, "assist-personal", model.parse_time(SERVE_AT),
                               grants.EXAMPLE_HOLDER_KEY)
        self.assertEqual(os.listdir(self.pkg), before)  # nothing written
        self.assertIsNone(self.ctx().record("g-01"))
        why = dict((e["id"], e["why"]) for e in draft["notIncluded"])
        self.assertEqual(why[self.ids["hexaco"]], "not in what you ticked")
        self.assertNotIn(self.ids["bfi"], why)
        package = Package(self.pkg, self.spec)
        window.confirm_grant(package, grant)
        package.save(AGREE_AT)
        stored = grants.build_projection(self.ctx(), "g-01", "assist-personal", model.parse_time(SERVE_AT),
                                         "prj-preview", holder_key=grants.EXAMPLE_HOLDER_KEY, nonce="preview")
        self.assertEqual(draft["receives"], stored)
        out = io.StringIO()
        with redirect_stdout(out), redirect_stderr(io.StringIO()):
            code = ohc_query.main([self.pkg, "preview", "--grant", "g-01", "--purpose", "assist-personal",
                                   "--now", SERVE_AT])
        self.assertEqual(code, 0)
        self.assertEqual(jsonio.loads_strict(out.getvalue(), "-"), stored)  # the grantee view only
        self.assertNotIn("notIncluded", out.getvalue())

    # ------------------------------------------------------------ changing one's mind
    def test_withdraw_then_narrower_grant(self):
        self.agree()
        package = Package(self.pkg, self.spec)
        notice = window.withdraw(package, "g-01", "2026-10-14T08:00:00Z", outbox=self.outbox, seed="t")
        package.save("2026-10-14T08:00:00Z")
        self.assertEqual(self.spec.validate("urn:ohc:schema:msg-revocation-notice:0.1.0-draft", notice), [])
        self.assertEqual(notice["purgeBy"], "2026-10-15T08:00:00Z")
        self.assertEqual([m["id"] for m in window.pending_notices(self.outbox, "a-01")], [notice["id"]])
        kinds = [e["eventType"] for e in Package(self.pkg, self.spec).events][-2:]
        self.assertEqual(kinds, ["grant-withdrawn", "revocation-notice-sent"])
        with self.assertRaises(grants.Denied):
            self.project(at="2026-10-14T09:00:00Z")
        self.agree(gid="g-02", at="2026-10-14T08:05:00Z", rows={self.ids["hexaco"]: False})
        projection = self.project(gid="g-02", at="2026-10-14T09:00:00Z")
        self.assertNotIn(self.ids["hexaco"], grants.served_id_set(projection))
        package = Package(self.pkg, self.spec)
        window.acknowledge(self.outbox, package, notice["id"], "2026-10-14T09:30:00Z", seed="t")
        package.save("2026-10-14T09:30:00Z")
        self.assertEqual(window.pending_notices(self.outbox), [])
        self.assertValid()

    def test_erasure_keeps_tier_of_kept_words(self):
        self.agree()
        out = io.StringIO()
        with redirect_stdout(out):  # the session-start hook serves it once, so the agent is a recipient
            ohc_holder.main(["serve", self.pkg, "--grant", "g-01", "--purpose", "assist-personal", "--now", SERVE_AT,
                             "--registry", os.path.join(self.tmp, "registry")])
        ctx = self.ctx()
        plan = window.erase_plan(ctx, self.ids["bfi"])
        self.assertEqual(plan, {"record": self.ids["bfi"], "words": [self.ids["words"]],
                                "report": self.ids["source"]})
        vault = ctx.record(self.ids["source"])["content"]["locator"]["vaultPath"]
        package = Package(self.pkg, self.spec)
        result = window.erase(package, ctx, self.ids["bfi"], "2026-10-15T08:00:00Z", erase_report=True,
                              outbox=self.outbox, seed="t")
        package.save("2026-10-15T08:00:00Z")
        self.assertEqual(result["erased"], [self.ids["bfi"], self.ids["source"]])
        self.assertFalse(os.path.exists(os.path.join(self.pkg, vault)))
        notice = result["notices"][0]
        self.assertEqual(notice["to"], "a-01")
        self.assertEqual(self.spec.validate("urn:ohc:schema:msg-erasure-notice:0.1.0-draft", notice), [])
        state = model.State(self.ctx())
        self.assertIn(self.ids["bfi"], state.tombstoned)
        self.assertEqual(state.tier(self.ids["words"]), "special")  # kept words keep their tier
        self.assertIn("mental-health", state.categories(self.ids["words"]))
        report = self.assertValid()
        self.assertEqual([w["rule"] for w in report["warnings"]], [])

    def test_correct_and_retake(self):
        fixed = importkit.bfi_draft(self.spec, **{"big-five/C": 4.4, "big-five/E": 2.9, "big-five/O": 3.6})
        import_assessment.import_result(self.pkg, [fixed], "2026-10-12T09:20:00Z", supersedes=self.ids["bfi"],
                                        spec=self.spec, synthetic=True)
        package = Package(self.pkg, self.spec)
        window.record_stance(package, "as-03", "fits", "2026-10-12T09:20:30Z")  # the correction, decided on
        package.save("2026-10-12T09:20:30Z")
        view = self.view(at="2026-10-12T09:21:00Z")
        self.assertEqual([r["id"] for r in view["rows"] if r["lens"] == BIG_FIVE], ["as-03"])
        retake = importkit.bfi_draft(self.spec, taken="2026-10-10", **{"big-five/C": 4.0})
        result = import_assessment.import_result(self.pkg, [retake], "2026-10-12T09:25:00Z", spec=self.spec,
                                                 synthetic=True)
        package = Package(self.pkg, self.spec)
        window.mark_not_current(package, "as-03", "2026-10-12T09:25:00Z")
        package.save("2026-10-12T09:25:00Z")
        self.assertEqual(result["assessments"], ["as-04"])
        self.assertValid()

    def test_playbooks_choice(self):
        ctx = self.ctx()
        package = Package(self.pkg, self.spec)
        window.choose_playbooks(package, ctx, HEXACO, [], "2026-10-12T09:12:00Z")
        package.save("2026-10-12T09:12:00Z")
        view = self.view()
        row = [r for r in view["rows"] if r["lens"] == HEXACO][0]
        self.assertEqual(row["playbooks"], [])
        self.assertIn("ways of working: none · change", window.render_screen(view))
        adoption = [i.data for i in self.ctx().items if i.kind == "LensAdoption"][0]
        self.assertEqual((adoption["agentInterpretation"], adoption["route"]), ("allowed", "self-chosen"))
        with self.assertRaises(window.Refused):  # PB-3
            window.choose_playbooks(Package(self.pkg, self.spec), self.ctx(), HEXACO,
                                    ["urn:ohc:playbook:big-five-basic"], "2026-10-12T09:13:00Z")
        self.assertValid()

    # ------------------------------------------------------------ the command line
    def test_holder_window_refuses_without_tty(self):
        script = os.path.join(helpers.repo_root(), "tools", "ohc_holder.py")
        lock = os.path.join(self.pkg, "context.lock.json")
        with open(lock, "rb") as handle:
            before = handle.read()
        for argv in (["agree", self.pkg, "--grantee", "a-01", "--purpose", "assist-personal"],
                     ["erase", self.pkg, self.ids["bfi"]], ["withdraw", self.pkg, "g-01"],
                     ["review", self.pkg, self.ids["hexaco"]]):
            run = subprocess.run([sys.executable, "-B", script] + argv, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True, timeout=60)
            self.assertEqual(run.returncode, ohc_holder.NO_TERMINAL, argv)
            self.assertIn(b"own terminal", run.stderr)
        with open(lock, "rb") as handle:
            self.assertEqual(handle.read(), before)

    def test_dialogue(self):
        registry = ["--registry", os.path.join(self.tmp, "registry")]
        term = importkit.ScriptedTerminal(["2", "ok"])  # untick result 2, then confirm the whole screen
        code = ohc_holder.main(["agree", self.pkg, "--grantee", "a-01", "--purpose", "assist-personal", "--at",
                                AGREE_AT] + registry, terminal=term)
        self.assertEqual(code, 0)
        grant = self.ctx().record("g-01")
        self.assertEqual(grant["scope"]["include"][0], {"lenses": [BIG_FIVE]})
        draft = os.path.join(self.tmp, "draft.json")
        jsonio.write_pretty(draft, importkit.bfi_draft(self.spec, taken="2026-10-11", **{"big-five/A": 3.3}))
        term = importkit.ScriptedTerminal(["y", "1", "Ask me before you plan my evenings.", "y", "y"])
        code = ohc_holder.main(["retake", self.pkg, "--draft", draft, "--at", "2026-10-12T10:00:00Z"] + registry,
                               terminal=term)
        self.assertEqual(code, 0)
        state = model.State(self.ctx())
        retaken = [i.id for i in self.ctx().items if i.kind == "AssessmentRecord" and
                   i.id not in (self.ids["bfi"], self.ids["hexaco"])]
        self.assertEqual(len(retaken), 1)
        self.assertNotRegex(retaken[0], r"^as-\d+$")  # the window issues opaque ids (no gap to read)
        self.assertEqual(state.status[retaken[0]].endorsement, "endorsed")
        self.assertTrue(state.status[self.ids["bfi"]].not_current)
        self.assertValid()
        term = importkit.ScriptedTerminal(["y"])  # stops at the second question: nothing more is decided
        with redirect_stderr(io.StringIO()):
            code = ohc_holder.main(["withdraw", self.pkg, "g-01", "--outbox", self.outbox, "--at",
                                    "2026-10-12T11:00:00Z"] + registry, terminal=term)
        self.assertEqual(code, 1)

    def test_setup_asks_first(self):
        target = os.path.join(self.tmp, "new")
        term = importkit.ScriptedTerminal(["n"])
        self.assertEqual(ohc_holder.main(["setup", target, "--subject", "urn:ohc:example:new-person"], terminal=term), 0)
        self.assertFalse(os.path.exists(target))  # nothing without a yes
        term = importkit.ScriptedTerminal(["y", "Bring me the decision first."])
        self.assertEqual(ohc_holder.main(["setup", target, "--subject", "urn:ohc:example:new-person", "--synthetic",
                                          "--at", importkit.AT], terminal=term), 0)
        self.assertTrue(any("serve" in line for line in term.said))
        report = check.run_context(target, spec=self.spec)
        self.assertTrue(report["valid"], report["errors"])

    def test_erase_dialogue_offers_to_relax_kept_words(self):
        term = importkit.ScriptedTerminal(["n", "n", "y", "y"])  # keep words, keep report, erase, relax
        code = ohc_holder.main(["erase", self.pkg, self.ids["bfi"], "--at", "2026-10-15T08:00:00Z", "--outbox",
                                self.outbox, "--registry", os.path.join(self.tmp, "registry")], terminal=term)
        self.assertEqual(code, 0)
        state = model.State(self.ctx())
        self.assertIn(self.ids["bfi"], state.tombstoned)
        self.assertNotIn(self.ids["source"], state.tombstoned)
        self.assertEqual(state.tier(self.ids["words"]), "personal")
        self.assertValid()

    def test_serve_and_notices_hooks(self):
        self.agree()
        out = io.StringIO()
        with redirect_stdout(out):
            code = ohc_holder.main(["serve", self.pkg, "--grant", "g-01", "--purpose", "assist-personal", "--now",
                                    SERVE_AT, "--registry", os.path.join(self.tmp, "registry")])
        self.assertEqual(code, 0)
        self.assertTrue(out.getvalue().startswith("OHC · Personal agent · grant g-01"))
        events = Package(self.pkg, self.spec).events
        self.assertEqual((events[-1]["eventType"], events[-1]["counterparty"]), ("projection-served", "a-01"))
        package = Package(self.pkg, self.spec)
        window.withdraw(package, "g-01", "2026-10-14T08:00:00Z", outbox=self.outbox, seed="t")
        package.save("2026-10-14T08:00:00Z")
        out = io.StringIO()
        with redirect_stdout(out):
            ohc_holder.main(["notices", self.pkg, "--for", "a-01", "--outbox", self.outbox])
        self.assertIn("ohc.experimental.revocation-notice", out.getvalue())
        out = io.StringIO()
        with redirect_stdout(out):
            code = ohc_holder.main(["serve", self.pkg, "--grant", "g-01", "--purpose", "assist-personal", "--now",
                                    "2026-10-14T09:00:00Z", "--registry", os.path.join(self.tmp, "registry")])
        self.assertEqual(code, 1)
        self.assertIn("ohc.experimental.denial", out.getvalue())
        self.assertValid()


if __name__ == "__main__":
    unittest.main()
