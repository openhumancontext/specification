"""Tove (fictional) brings her test reports to her agent: an example built by running the person's window.

An example directory with a ``session.json`` is built, not written by hand. Every record in it is written by
``tools/ohc_holder.py`` itself (``setup``, ``bring``, ``review``, ``agree``, ``serve``); this module only types the
person's answers into her window, as she would, through the window's ``terminal`` hook, and keeps what the window
showed her and what her agent received. Her reports (``inputs/``) are synthetic stand-ins with no publisher text,
and her numbers are invented.

``session.json``::

    {"seed": "...", "registries": ["dir", ...],          # optional extra registries, relative to the repository
     "steps": [{"run": [command, option, ...], "context": "context", "answers": [...],
                "window": "expected/...txt", "stdout": "expected/...txt"},
               {"copy": "context", "to": "variants/..."}]}

``context`` (default ``context``) is the package the command works on; ``window`` keeps the window's text,
``stdout`` what the command printed (the agent rendering, or the projection). Paths are relative to the example.

    python3 -B tools/tests/tove_session.py examples/tove-bring-a-result --write   # rebuild in place
    python3 -B tools/tests/tove_session.py examples/tove-bring-a-result --out DIR # build into DIR
"""

import argparse
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import ohc_holder  # noqa: E402

BUILT = ("context", "variants", "expected")  # what a build writes; inputs/, session.json and README.md are kept


class ScriptedTerminal(object):
    """The person at her own window: each ``ask`` takes her next answer; everything the window says is kept."""

    def __init__(self, answers):
        self.answers = list(answers)
        self.out = []

    def say(self, text=""):
        self.out.append(text + ("" if text.endswith("\n") else "\n"))

    def ask(self, prompt):
        if not self.answers:
            raise EOFError()
        answer = self.answers.pop(0)
        self.out.append("%s %s\n" % (prompt, answer))
        return answer

    def text(self):
        return "".join(self.out)


class SessionError(Exception):
    pass


def standin_pdf(title):
    """A one-page PDF that says what it is: a synthetic stand-in for a score report, with no publisher content."""
    lines = [title, "Synthetic stand-in for a score report of a fictional person.",
             "It carries no publisher text, items, scoring keys or report prose."]
    stream = "BT /F1 11 Tf 56 760 Td 14 TL " + " ".join("(%s) '" % line.replace("(", "[").replace(")", "]")
                                                        for line in lines) + " ET"
    objects = ["<< /Type /Catalog /Pages 2 0 R >>", "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
               "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R "
               "/Resources << /Font << /F1 5 0 R >> >> >>",
               "<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream),
               "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    out = "%PDF-1.4\n"
    offsets = []
    for number, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += "%d 0 obj\n%s\nendobj\n" % (number, body)
    xref = len(out)
    out += "xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    out += "".join("%010d 00000 n \n" % offset for offset in offsets)
    out += "trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, xref)
    return out.encode("ascii")


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def run_step(out, step, session):
    """One command in the person's window. Option values that name a file of the example are made absolute."""
    command, rest = step["run"][0], step["run"][1:]
    argv = [command]
    if command != "template":
        argv.append(os.path.join(out, step.get("context", "context")))
    for value in rest:
        argv.append(os.path.join(out, value) if value.startswith("inputs/") else value)
    for registry in session.get("registries") or []:
        argv += ["--registry", os.path.join(ROOT, registry)]
    if session.get("seed") and command != "template":
        argv += ["--seed", session["seed"]]
    terminal = ScriptedTerminal(step.get("answers") or [])
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = ohc_holder.main(argv, terminal=terminal)
    if code != 0 or terminal.answers:
        raise SessionError("%s: exit %s, %d answers left; %s" % (" ".join(step["run"]), code, len(terminal.answers),
                                                                 stderr.getvalue().strip()))
    if step.get("window"):
        _write(os.path.join(out, step["window"]), terminal.text())
    if step.get("stdout"):
        _write(os.path.join(out, step["stdout"]), stdout.getvalue())


def build(example, out):
    """Build ``example`` into ``out``: copy its inputs and session, then run the session's steps in order."""
    with open(os.path.join(example, "session.json"), "r", encoding="utf-8") as handle:
        session = json.load(handle)
    os.makedirs(out, exist_ok=True)
    shutil.copyfile(os.path.join(example, "session.json"), os.path.join(out, "session.json"))
    if os.path.abspath(example) != os.path.abspath(out):
        shutil.copytree(os.path.join(example, "inputs"), os.path.join(out, "inputs"))
    for step in session["steps"]:
        if "copy" in step:
            shutil.copytree(os.path.join(out, step["copy"]), os.path.join(out, step["to"]))
        else:
            run_step(out, step, session)
    return out


def built_files(directory):
    """{relative path: bytes} of everything a build writes."""
    out = {}
    for top in BUILT:
        for base, dirs, names in os.walk(os.path.join(directory, top)):
            dirs.sort()
            for name in sorted(names):
                full = os.path.join(base, name)
                with open(full, "rb") as handle:
                    out[os.path.relpath(full, directory).replace(os.sep, "/")] = handle.read()
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build an example by running the person's window.")
    parser.add_argument("example")
    parser.add_argument("--write", action="store_true", help="replace the built parts of the example in place")
    parser.add_argument("--out", help="build into this directory instead")
    args = parser.parse_args(argv)
    example = os.path.abspath(args.example)
    out = args.out or tempfile.mkdtemp(prefix="ohc-session-")
    target = os.path.join(out, "example")
    build(example, target)
    if args.write:
        for top in BUILT:
            if os.path.exists(os.path.join(example, top)):
                shutil.rmtree(os.path.join(example, top))
            if os.path.exists(os.path.join(target, top)):
                shutil.copytree(os.path.join(target, top), os.path.join(example, top))
        print("rebuilt %s" % args.example)
    else:
        print(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
