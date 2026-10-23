"""Examples built by running the person's window (``session.json``): each rebuilds byte for byte, every package in
it passes at L2 with the registries its session names, and its agent rendering follows PB-5.

The public example is ``examples/tove-bring-a-result``. An example of the same path kept outside the release (with its
variant in which the person unticks one result) is checked the same way when it is present, and skipped otherwise."""

import json
import os
import shutil
import tempfile
import unittest

import helpers
import tove_session

import build_release_manifest as brm
import check
from ohclib import jsonio, model, rendering, vocab

ROOT = helpers.repo_root()
PUBLIC = os.path.join(ROOT, "examples", "tove-bring-a-result")
KEPT_OUT = os.path.join(ROOT, brm.PRIVATE_TREE, "examples", "tove-hogan-import")


def session_of(example):
    with open(os.path.join(example, "session.json"), "r", encoding="utf-8") as handle:
        return json.load(handle)


def packages(example):
    """The packages of a built example: ``context`` and every ``variants/<name>``."""
    out = [os.path.join(example, "context")]
    variants = os.path.join(example, "variants")
    if os.path.isdir(variants):
        out.extend(os.path.join(variants, name) for name in sorted(os.listdir(variants)))
    return out


class BuiltExamples(unittest.TestCase):
    def examples(self):
        out = [PUBLIC]
        if os.path.isdir(KEPT_OUT):
            out.append(KEPT_OUT)
        return out

    def spec_for(self, example):
        registries = [os.path.join(ROOT, r) for r in session_of(example).get("registries") or []]
        return vocab.Spec(registries=registries or None)

    def test_rebuilds_byte_for_byte(self):
        for example in self.examples():
            with self.subTest(example=os.path.basename(example)):
                tmp = tempfile.mkdtemp(prefix="ohc-tove-")
                try:
                    built = tove_session.build(example, os.path.join(tmp, "example"))
                    self.assertEqual(sorted(tove_session.built_files(built)),
                                     sorted(tove_session.built_files(example)))
                    for rel, data in tove_session.built_files(built).items():
                        self.assertEqual(data, tove_session.built_files(example)[rel], rel)
                finally:
                    shutil.rmtree(tmp, ignore_errors=True)

    def test_packages_pass_at_l2(self):
        for example in self.examples():
            spec = self.spec_for(example)
            for package in packages(example):
                with self.subTest(package=os.path.relpath(package, ROOT).split(os.sep, 1)[-1]):
                    report = check.run_context(package, spec=spec)
                    self.assertTrue(report["valid"], report["errors"])
                    self.assertEqual(report["levelMet"], "L2")
                    self.assertEqual(report["warnings"], [])

    def test_report_is_a_vault_source_and_the_result_cites_it(self):
        for example in self.examples():
            ctx = model.Context(os.path.join(example, "context"), self.spec_for(example))
            results = [i.data for i in ctx.items if i.kind == "AssessmentRecord"]
            self.assertTrue(results)
            for record in results:
                with self.subTest(result=record["id"]):
                    source = ctx.record(record["source"])
                    self.assertEqual(source["sourceKind"], "instrument-report")
                    self.assertTrue(source["content"]["locator"]["vaultPath"].startswith("vault/"))
                    self.assertEqual(record["origin"], "imported")
                    self.assertTrue(record.get("synthetic"))

    def test_everything_ticked_and_one_grant(self):
        for example in self.examples():
            ctx = model.Context(os.path.join(example, "context"), self.spec_for(example))
            grants = [i.data for i in ctx.items if i.kind == "Grant"]
            self.assertEqual(len(grants), 1)
            grant = grants[0]
            self.assertEqual(grant["actions"], ["read", "suggest", "infer"])
            self.assertEqual(grant["constraints"]["decisionUse"], "approval-required")
            self.assertEqual(grant["constraints"]["storage"], "until-expiry")
            given = [e for e in ctx.events if e.data.get("eventType") == "grant-given"]
            self.assertEqual([e.data["grant"] for e in given], [grant["id"]])

    def test_rendering_is_the_stored_projection_and_pb5(self):
        """The rendering is served from the stored projection; a lens with nothing served brings no playbook, and
        the grant line says what the agreement allows."""
        for example in self.examples():
            spec = self.spec_for(example)
            expected = os.path.join(example, "expected")
            renderings = {"context": os.path.join(expected, "session-start.txt")}
            if not os.path.isfile(renderings["context"]):
                renderings["context"] = os.path.join(expected, "default", "session-start.txt")
            for package in packages(example)[1:]:
                renderings[package] = os.path.join(expected, os.path.basename(package), "session-start.txt")
            for package in packages(example):
                key = "context" if package.endswith(os.sep + "context") else package
                with self.subTest(package=os.path.basename(package)):
                    ctx = model.Context(package, spec)
                    projection = jsonio.load_json(os.path.join(package, "projections", "prj-0001.json"))
                    with open(renderings[key], "r", encoding="utf-8") as handle:
                        text = handle.read()
                    self.assertEqual(rendering.render_agent(ctx, projection, ctx.record(projection["grant"])), text)
                    self.assertIn("guesses — yes · weighing accepted results — yes", text)
                    served = set(a["lens"]["id"] for a in projection["statements"]["assessments"])
                    for doc in ctx.pinned_playbooks.values():
                        name = doc["name"]["en"]
                        if set(doc["lenses"]) & served:
                            self.assertIn(name, text)
                        else:
                            self.assertNotIn(name, text)
                    for record in projection["statements"]["claims"]:
                        self.assertIn(record["text"], text)


class RealTerminal(unittest.TestCase):
    @unittest.skipUnless(os.name == "posix", "needs a pseudo-terminal")
    def test_the_window_runs_on_a_real_terminal(self):
        """The window reads and writes the person's own terminal (a terminal is not seekable: one reader, one
        writer); the same command without a terminal is refused with exit 3."""
        import pty
        import select
        import subprocess
        import sys

        tmp = tempfile.mkdtemp(prefix="ohc-tty-")
        try:
            holder = os.path.join(ROOT, "tools", "ohc_holder.py")
            argv = [sys.executable, "-B", holder, "setup", os.path.join(tmp, "ctx"), "--subject",
                    "urn:ohc:example:tove", "--synthetic", "--at", "2026-09-15T09:05:00Z"]
            pid, fd = pty.fork()
            if pid == 0:  # the child: its /dev/tty is the pseudo-terminal
                os.execv(sys.executable, argv)
            answers, seen = ["y", "Give me the decision first, in one paragraph."], b""
            while True:
                try:
                    ready = select.select([fd], [], [], 0.3)[0]
                    if ready:
                        data = os.read(fd, 4096)
                        if not data:
                            break
                        seen += data
                    elif answers:
                        os.write(fd, (answers.pop(0) + "\n").encode("utf-8"))
                except OSError:
                    break
            _pid, status = os.waitpid(pid, 0)
            self.assertEqual(os.WEXITSTATUS(status), 0, seen.decode("utf-8", "replace")[-400:])
            self.assertTrue(os.path.isfile(os.path.join(tmp, "ctx", "context.json")))
            refused = subprocess.run(argv[:4] + [os.path.join(tmp, "other")] + argv[5:], stdin=subprocess.DEVNULL,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
            self.assertEqual(refused.returncode, 3)
            self.assertFalse(os.path.exists(os.path.join(tmp, "other")))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
