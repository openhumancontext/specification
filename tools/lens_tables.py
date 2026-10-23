#!/usr/bin/env python3
"""Generate the "How each lens works with a person" section of spec/LENSES.md from the lens descriptors.

Usage:
    python3 tools/lens_tables.py           # rewrite the generated section in spec/LENSES.md
    python3 tools/lens_tables.py --check   # exit 1 when the section differs from the descriptors

The section sits between ``<!-- lens-how:start -->`` and ``<!-- lens-how:end -->``. Every value comes from the
descriptor's ``mentalModel``, ``toolkit``, ``representations`` and ``playbooks`` (the playbook documents in
``spec/playbooks/``); nothing is written by hand.
"""

import argparse
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ohclib import jsonio, vocab  # noqa: E402

START = "<!-- lens-how:start -->"
END = "<!-- lens-how:end -->"


def _cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def _list(items):
    return "; ".join(_cell(i) for i in items or []) or "—"


def _tool(tool):
    who = "practitioner required" if tool.get("requiresPractitioner") else "no practitioner required"
    agent = "an agent may offer it" if tool.get("agentMayOffer") else "an agent never offers it"
    return "%s (%s; facilitation `%s`; %s; %s)" % (_cell(tool.get("name", tool.get("id"))), tool.get("kind"),
                                                   tool.get("facilitation"), who, agent)


def _playbook(playbook_id, playbooks):
    doc = playbooks.get(playbook_id)
    short = playbook_id.rsplit(":", 1)[-1]
    if doc is None:
        return "`%s` (not found)" % short
    situations = []
    for situation in doc.get("situations") or []:
        text = _cell(((situation.get("when") or {}).get("en") or situation.get("id", "")).rstrip("."))
        tools = ", ".join("`%s`" % tool for tool in situation.get("toolkit") or [])
        situations.append("%s (%s)" % (text, tools) if tools else text)
    return "`%s` by %s: %s" % (short, _cell(doc.get("author", "—")), "; ".join(situations) or "—")


def lens_block(doc, playbooks=None):
    name = doc.get("name") or {}
    short = doc["id"].rsplit(":", 1)[-1]
    mental = doc.get("mentalModel") or {}
    posture = mental.get("agentPosture") or {}
    stub = doc.get("descriptorStatus") == "stub"
    rows = [
        ("Mental model", _cell(mental.get("summary", "—"))),
        ("Attends to", _list(mental.get("attendsTo"))),
        ("Stance", _cell(mental.get("stance", "—"))),
        ("How change happens", _cell(mental.get("howChangeHappens", "—"))),
        ("Agent posture", "Do: %s. Don't: %s." % (_list(posture.get("do")), _list(posture.get("dont")))),
        ("A helper must not", _list(mental.get("helperMustNot"))),
    ]
    toolkit = doc.get("toolkit") or []
    representations = doc.get("representations") or []
    if stub:
        rows.append(("Toolkit", "Not described yet (stub)."))
        rows.append(("Representations", "Not described yet (stub)."))
    else:
        rows.append(("Toolkit", "; ".join(_tool(t) for t in toolkit) or "—"))
        rows.append(("Representations", "; ".join("`%s` (%s)" % (r.get("id"), r.get("kind"))
                                                  for r in representations) or "—"))
    rows.append(("Playbooks", " · ".join(_playbook(i, playbooks or {}) for i in doc.get("playbooks") or []) or "—"))
    lines = ["#### `%s`: %s" % (short, _cell(name.get("en", short) if isinstance(name, dict) else name)), "",
             "| | |", "|---|---|"]
    lines += ["| %s | %s |" % (label, value) for label, value in rows]
    return "\n".join(lines)


def counts(docs):
    descriptors = [d for d in docs if d.get("descriptorStatus") != "stub"]
    stubs = [d for d in docs if d.get("descriptorStatus") == "stub"]
    tools = sum(len(d.get("toolkit") or []) for d in descriptors)
    return len(docs), len(descriptors), len(stubs), tools


def render(root=None):
    root = root or vocab.default_root()
    docs = [jsonio.load_json(p) for p in sorted(glob.glob(os.path.join(root, "spec", "lenses", "*.lens.json")))]
    playbooks = {}
    for path in sorted(glob.glob(os.path.join(root, "spec", "playbooks", "*.playbook.json"))):
        playbook = jsonio.load_json(path)
        playbooks[playbook.get("id")] = playbook
    total, descriptors, stubs, tools = counts(docs)
    head = ("Generated from the descriptors and their playbooks by `tools/lens_tables.py`. %d entries: %d "
            "descriptors, which together carry %d toolkit items and at least one representation each, and %d stubs, "
            "whose mental model is sketched but whose toolkit and representations are not described yet. Every "
            "entry lists its playbooks, with the situations each covers and the tools it offers (§2.2)."
            % (total, descriptors, tools, stubs))
    return "\n\n".join([START, head] + [lens_block(d, playbooks) for d in docs] + [END])


def replace(text, section):
    if START not in text or END not in text:
        raise ValueError("markers missing")
    before = text.split(START, 1)[0]
    after = text.split(END, 1)[1]
    return before + section + after


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate the per-lens section of LENSES.md.")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    root = vocab.default_root()
    path = os.path.join(root, "spec", "LENSES.md")
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    new = replace(text, render(root))
    if args.check:
        if new != text:
            print("LENSES.md: the per-lens section is out of date; run tools/lens_tables.py")
            return 1
        print("LENSES.md per-lens section up to date")
        return 0
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(new)
    print("wrote the per-lens section of spec/LENSES.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
