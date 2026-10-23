"""Rules and behaviours added in the 0.1.0-draft.1 review: positive and negative cases beside the fixtures."""

import contextlib
import io
import json
import os
import shutil
import tempfile
import unittest

import helpers

import check
import ohc_query
from ohclib import grants, jsonio, model

ROOT = helpers.repo_root()
MARA = os.path.join(ROOT, "examples", "mara-l1-agent")

VERBATIM = [
    {"op": "add", "target": "grants", "path": "/@g-01/actions", "value": "open-verbatim"},
    {"op": "set", "target": "grants", "path": "/@g-01/maxSourceTier", "value": "verbatim"},
    {"op": "set", "target": "grants", "path": "/@g-01/stepUp", "value": {"required": True, "maxDuration": "PT30M"}},
    {"op": "set", "target": "sources", "path": "/@src-01/maxRelease", "value": "verbatim"},
]


def event(**fields):
    return {"op": "add", "target": "events", "path": "", "value": fields}


def step_up(actor="subject", opens=1, records=("src-01",), source="src-01"):
    base = {"grant": "g-01", "purpose": "learning-support"}
    patches = [event(at="2026-10-08T13:00:00Z", eventType="step-up-confirmed", actor=actor, outcome="confirmed",
                     records=list(records), confirmationDigest="sha256:" + "1" * 64, **base)]
    for n in range(opens):
        patches.append(event(at="2026-10-08T13:0%d:00Z" % (n + 1), eventType="source-opened", actor="holder",
                             counterparty="a-01", records=[source], tier="verbatim", outcome="served", **base))
    return patches


def tombstone(rid, kind, at):
    return {"kind": "Tombstone", "id": rid, "erasedKind": kind, "erasedAt": at, "erasedBy": "subject",
            "reason": "subject-request"}


class ReviewFixes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ohc-review-")
        self.n = 0

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_patches(self, patches, form="single", **extra):
        self.n += 1
        fixture = dict({"form": form, "patches": patches}, **extra)
        return helpers.run_fixture(fixture, os.path.join(self.tmp, str(self.n)))

    def warnings(self, report):
        return sorted(set(w["rule"] for w in report["warnings"]))

    # ------------------------------------------------------------- findings
    def test_findings_explain_themselves_without_values(self):
        report = self.run_patches([{"op": "remove", "target": "claims", "path": "/@c-02/assertedBy"}])
        finding = next(e for e in report["errors"] if e["rule"] == "S-3")
        self.assertEqual(finding["detail"], "required: assertedBy")
        self.assertTrue(finding["message"])
        self.assertIn("SPECIFICATION.md", finding["see"])
        self.assertNotIn("No study messages", json.dumps(report))

    def test_missing_facet_is_reported_at_the_facet(self):
        report = self.run_patches([{"op": "remove", "target": "claims", "path": "/@c-02/facet"}])
        paths = [e["path"] for e in report["errors"]]
        self.assertTrue(any(p.endswith("/facet") for p in paths), paths)
        self.assertNotIn("CL-8", helpers.error_rules(report))

    def test_every_checker_rule_is_defined(self):
        self.assertEqual(check.undefined_rules(), [])
        check.RULES["ZZ-1"] = ("L0", "check")
        try:
            self.assertEqual(check.undefined_rules(), ["ZZ-1"])
        finally:
            del check.RULES["ZZ-1"]

    # ------------------------------------------------------------- warnings
    def test_lens_without_descriptor_is_a_stub(self):
        adoption = helpers.subj({"id": "la-02", "lens": {"id": "urn:ohc:lens:x-coach:three-rooms", "version": "0.1.0"},
                                 "route": "self-chosen", "uses": ["speak-in-lens"]}, "2026-09-06T09:30:00Z")
        report = self.run_patches([{"op": "add", "target": "lensAdoptions", "path": "", "value": adoption}])
        self.assertIn("W-LA6", self.warnings(report))
        # A stub only makes results frame-relative (LA-6); agent reading is the person's agreement (I5).
        allowed = dict(adoption, agentInterpretation="allowed")
        report = self.run_patches([{"op": "add", "target": "lensAdoptions", "path": "", "value": allowed}])
        self.assertEqual(helpers.error_rules(report), ["LA-6"])  # unpinned; no stub rule on agentInterpretation

    def test_local_lens_descriptor_inline(self):
        with open(os.path.join(ROOT, "spec", "LENSES.md"), encoding="utf-8") as handle:
            text = handle.read()
        block = text.split("### 5.1 Local lenses", 1)[1].split("```json\n", 1)[1].split("\n```", 1)[0]
        descriptor = json.loads(block)
        self.assertEqual(helpers.spec().validate("urn:ohc:schema:lens:0.1.0-draft", descriptor), [])
        pin = {"id": descriptor["id"], "version": descriptor["version"], "descriptor": descriptor}
        adoption = helpers.subj({"id": "la-02", "lens": {"id": descriptor["id"], "version": "0.1.0"},
                                 "route": "self-chosen", "uses": ["speak-in-lens"]}, "2026-09-06T09:30:00Z")
        report = self.run_patches([{"op": "add", "target": "manifest", "path": "/lenses", "value": pin},
                                   {"op": "add", "target": "lensAdoptions", "path": "", "value": adoption}])
        self.assertTrue(report["valid"], report["errors"])
        self.assertNotIn("W-LA6", self.warnings(report))

    def test_agent_holder_with_its_own_grant_warns(self):
        report = self.run_patches([{"op": "set", "target": "manifest", "path": "/holder", "value": "a-01"}])
        self.assertIn("W-HO1", self.warnings(report))

    def test_affect_reading_without_quarantine_warns(self):
        claim = {"id": "c-07", "facet": "preference", "text": "Seems anxious before exams.", "origin": "inferred",
                 "assertedBy": "a-01", "recordedAt": "2026-09-05T10:00:00Z", "underGrant": "g-01",
                 "purpose": "learning-support", "evidence": [{"ref": "ep-02", "kind": "observation"}],
                 "synthetic": True}
        report = self.run_patches([{"op": "add", "target": "claims", "path": "", "value": claim}])
        self.assertIn("W-CL4", self.warnings(report))
        self.assertNotIn("CL-4", helpers.error_rules(report))

    # ------------------------------------------------------------- step-up (EV-5)
    def test_step_up_confirmed_by_the_subject(self):
        report = self.run_patches(VERBATIM + step_up(), form="package")
        self.assertTrue(report["valid"], report["errors"])

    def test_agent_never_confirms_a_step_up(self):
        report = self.run_patches(VERBATIM + step_up(actor="a-01"), form="package")
        self.assertIn("EV-5", helpers.error_rules(report))

    def test_step_up_covers_only_the_confirmed_sources(self):
        report = self.run_patches(VERBATIM + step_up(records=("ep-01",)), form="package")
        self.assertIn("EV-5", helpers.error_rules(report))

    def test_special_source_opened_once_per_step_up(self):
        note = helpers.subj({"id": "src-02", "sourceKind": "note", "categories": ["health"],
                             "content": {"locator": {"vaultPath": "vault/ab/" + "ab" * 32 + ".txt"},
                                         "sha256": "ab" * 32, "mediaType": "text/plain"},
                             "authorship": {"author": "subject"}, "maxRelease": "verbatim",
                             "retention": {"eraseOnRequest": True}}, "2026-09-01T08:00:00Z")
        special = VERBATIM + [
            {"op": "add", "target": "sources", "path": "", "value": note},
            {"op": "add", "target": "grants", "path": "/@g-01/scope/include", "value": {"ids": ["src-02"]}},
            # the stored projection of 8 October now serves src-02 at the index tier, so its Event lists it (EV-7)
            {"op": "add", "target": "events", "path": "/3/records", "value": "src-02"}]
        once = self.run_patches(special + step_up(records=("src-02",), source="src-02"), form="package")
        self.assertTrue(once["valid"], once["errors"])
        twice = self.run_patches(special + step_up(opens=2, records=("src-02",), source="src-02"), form="package")
        self.assertEqual(helpers.error_rules(twice), ["EV-5"])

    # ------------------------------------------------------------- erasure
    def test_erase_a_reviewed_claim(self):
        erased = [{"op": "set", "target": "claims", "path": "/@c-05", "value": tombstone("c-05", "Claim",
                                                                                          "2026-09-20T08:00:00Z")}]
        self.assertTrue(self.run_patches(erased)["valid"])
        cascade = erased + [
            {"op": "set", "target": "reviews", "path": "/@rv-01",
             "value": tombstone("rv-01", "Review", "2026-09-20T08:00:00Z")},
            {"op": "set", "target": "proposals", "path": "/@prop-01",
             "value": tombstone("prop-01", "Proposal", "2026-09-20T08:00:00Z")}]
        report = self.run_patches(cascade)
        self.assertTrue(report["valid"], report["errors"])
        late = erased + [{"op": "add", "target": "reviews", "path": "",
                          "value": {"id": "rv-09", "target": "c-05", "action": "lock", "by": "subject",
                                    "recordedAt": "2026-09-21T08:00:00Z"}}]
        self.assertIn("RV-4", helpers.error_rules(self.run_patches(late)))

    def test_erase_a_cited_source_and_its_vault_object(self):
        at = "2026-10-09T08:00:00Z"
        patches = [
            {"op": "set", "target": "sources", "path": "/@src-01", "value": tombstone("src-01", "Source", at)},
            event(at=at, eventType="record-erased", actor="subject", records=["src-01"]),
            event(at="2026-10-09T08:01:00Z", eventType="erasure-notice-sent", actor="holder", counterparty="a-01",
                  records=["src-01"])]
        self.n += 1
        dest = os.path.join(self.tmp, str(self.n))
        helpers.materialize(dest, form="package", patches=patches, finalize={"projections": "keep"})
        with_object = helpers.run_check(dest)
        self.assertEqual(helpers.error_rules(with_object), ["V-6"])
        os.remove(os.path.join(dest, helpers.VAULT_PATH))
        report = helpers.run_check(dest)
        self.assertTrue(report["valid"], report["errors"])

    # ------------------------------------------------------------- tiers and freshness
    def test_wildcard_never_reaches_primary_material(self):
        self.n += 1
        dest = helpers.materialize(os.path.join(self.tmp, str(self.n)), form="single", patches=[
            {"op": "set", "target": "grants", "path": "/@g-01/scope/include", "value": [{"all": True}]}])
        ctx = model.Context(dest, helpers.spec())
        now = model.parse_time("2026-10-08T12:00:00Z")
        state = model.State(ctx, now)
        self.assertEqual(state.tier("src-01"), "sensitive")
        served, _mode = grants.evaluate(state, ctx.record("g-01"), "a-01", "learning-support", now)
        self.assertNotIn("src-01", [i.id for i in served])
        self.assertIn("c-01", [i.id for i in served])

    def test_state_claim_current_inside_its_window(self):
        self.n += 1
        dest = helpers.materialize(os.path.join(self.tmp, str(self.n)), form="single")
        ctx = model.Context(dest, helpers.spec())
        inside = model.parse_time("2026-09-06T12:00:00Z")
        after = model.parse_time("2026-09-10T12:00:00Z")
        self.assertEqual(model.State(ctx, inside).freshness("c-04", inside), "current")
        self.assertEqual(model.State(ctx, after).freshness("c-04", after), "expired")

    # ------------------------------------------------------------- Mara: proposer view, renewal, no-quote-back
    def test_proposer_view_and_renewal(self):
        ctx = model.Context(MARA, helpers.spec())
        before = model.parse_time("2026-09-13T08:00:00Z")
        plain = grants.build_projection(ctx, "g-01", "learning-support", before, "prj-t1",
                                        holder_key=grants.EXAMPLE_HOLDER_KEY)
        own = grants.build_projection(ctx, "g-01", "learning-support", before, "prj-t2",
                                      holder_key=grants.EXAMPLE_HOLDER_KEY, own_proposals=True)
        self.assertNotIn("in-02", grants.served_id_set(plain))
        self.assertTrue(own["ownProposals"])
        for rid in ("ep-02", "in-02", "c-03"):
            self.assertEqual(own["derived"][rid]["label"], "pending")
        later = model.parse_time("2026-12-02T08:00:00Z")
        state = model.State(ctx, later)
        self.assertEqual(state.grant_status("g-01", later), "expired")
        renewed = grants.build_projection(ctx, "g-02", "learning-support", later, "prj-t3",
                                          holder_key=grants.EXAMPLE_HOLDER_KEY)
        self.assertEqual(renewed["obligations"]["handling"].get("in-03"), ["no-quote-back"])
        self.assertNotIn("c-03", grants.served_id_set(renewed))

    # ------------------------------------------------------------- ohc_query keys and time
    def query(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = ohc_query.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_query_needs_a_key_for_real_contexts(self):
        self.n += 1
        dest = helpers.materialize(os.path.join(self.tmp, str(self.n)), form="single",
                                   patches=[{"op": "remove", "target": "manifest", "path": "/synthetic"}])
        code, _out, err = self.query(dest, "project", "--grant", "g-01", "--purpose", "learning-support",
                                     "--now", "2026-10-08T12:00:00Z")
        self.assertEqual(code, 2)
        self.assertIn("--holder-key-file", err)
        key = os.path.join(self.tmp, "holder.key")
        with open(key, "wb") as handle:
            handle.write(b"a-real-holder-key-kept-secret")
        code, out, err = self.query(dest, "project", "--grant", "g-01", "--purpose", "learning-support",
                                    "--now", "2026-10-08T12:00:00Z", "--holder-key-file", key)
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["format"], "ohc.projection")
        self.assertIn("now: 2026-10-08T12:00:00Z", err)

    def test_query_now_defaults_to_the_clock(self):
        code, _out, err = self.query(MARA, "project", "--grant", "g-02", "--purpose", "learning-support")
        self.assertIn("now: ", err)
        self.assertNotIn("now: 2026-11-28T10:00:00Z", err)
        code, _out, err = self.query(MARA, "project", "--grant", "g-02", "--purpose", "learning-support",
                                     "--now", "latest")
        self.assertEqual(code, 0, err)
        self.assertIn("now: 2026-11-28T10:00:00Z", err)


if __name__ == "__main__":
    unittest.main()
