#!/usr/bin/env python3
"""The person's window: a reference holder program in the terminal (INSTRUMENT-IMPORT.md §5; CONTEXT-03 0.2.0).

Usage:
    python3 tools/ohc_holder.py setup <context> --subject URN [--synthetic]
    python3 tools/ohc_holder.py template --instrument ID
    python3 tools/ohc_holder.py bring <context> (--draft FILE | --transcript FILE --instrument ID) [--report FILE]
    python3 tools/ohc_holder.py retake <context> (--draft FILE | --transcript FILE --instrument ID) [--report FILE]
    python3 tools/ohc_holder.py review <context> <result id>
    python3 tools/ohc_holder.py words <context> [--about ID]
    python3 tools/ohc_holder.py correct <context> <result id>
    python3 tools/ohc_holder.py agree <context> --grantee PARTY --purpose CODE [--operator employer|school]
        [--why-file FILE]
    python3 tools/ohc_holder.py preview <context> --grant ID --purpose CODE [--json]
    python3 tools/ohc_holder.py withdraw <context> <grant id>
    python3 tools/ohc_holder.py erase <context> <record id>
    python3 tools/ohc_holder.py playbooks <context> <lens id>
    python3 tools/ohc_holder.py serve <context> (--for PARTY | --grant ID) --purpose CODE [--render agent|json]
        [--now T] [--id ID] [--keep | --no-log]
    python3 tools/ohc_holder.py notices <context> [--for PARTY] [--ack MESSAGE]

Every command that decides something for the person (setup, bring, retake, review, words, correct, agree, preview,
withdraw, erase, playbooks) talks only to a controlling terminal (``/dev/tty``), never to an agent's pipes, and
refuses without one. It is not a lock: an agent that opens a terminal of its own could still type into it, which is
why the agent's procedure forbids it (CONTEXT-10, "Never"; C-8…C-10, H-17). ``template`` prints a blank draft for an agent to fill from a report the person handed over (IMA-1, IMA-2).
``serve`` is the session-start hook: it prints the agent rendering from outside the agent's reasoning and writes
nothing into the agent's workspace. ``notices`` is the per-prompt hook: pending ``revocation-notice`` and
``erasure-notice`` messages, and the runtime's acknowledgement. Common options: ``--at T`` (the time of the act;
default now), ``--registry DIR`` (extra registry documents), ``--outbox DIR`` (default ``<context>.outbox``),
``--holder-key-file FILE`` (``serve``, ``preview``; default ``<context>.holder-key``, which ``setup`` makes; the
published example key only for synthetic contexts), ``--seed S``
(reproducible Event salts and projection nonces, refused unless the context is synthetic; examples and tests only).

This is a terminal approximation of a holder's window, not a product: it shows the screen and records what the
person confirms. A passing run does not mean consent was informed, or that an agent behaves as agreed.
"""

import argparse
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import import_assessment  # noqa: E402
from ohclib import grants, jsonio, model, rendering, vocab, window  # noqa: E402
from ohclib.package import Package, next_numbered_id  # noqa: E402

NO_TERMINAL = 3
STANCE_MENU = "1 it fits · 2 parts fit · 3 not sure · 4 I dispute it · 5 it doesn't fit · 6 later"
STANCE_BY_KEY = dict(zip("123456", window.STANCES))


class NoTerminal(Exception):
    pass


class Terminal(object):
    """The person's controlling terminal (``/dev/tty``), never the agent's pipes."""

    def __init__(self, reader, writer=None):
        self.reader = reader
        self.writer = writer or reader

    @classmethod
    def open(cls):
        try:
            fd = os.open("/dev/tty", os.O_RDWR | getattr(os, "O_NOCTTY", 0))
        except OSError:
            raise NoTerminal()
        if not os.isatty(fd):
            os.close(fd)
            raise NoTerminal()
        # A terminal is not seekable, so it cannot be one read-write text stream: one reader, one writer.
        return cls(os.fdopen(fd, "r", encoding="utf-8"), os.fdopen(os.dup(fd), "w", buffering=1, encoding="utf-8"))

    def say(self, text=""):
        self.writer.write(text + ("" if text.endswith("\n") else "\n"))
        self.writer.flush()

    def ask(self, prompt):
        self.writer.write(prompt + " ")
        self.writer.flush()
        line = self.reader.readline()
        if not line:
            raise EOFError()
        return line.strip()


def yes(term, prompt, default=False):
    answer = term.ask("%s [%s]" % (prompt, "Y/n" if default else "y/N")).lower()
    return default if answer == "" else answer in ("y", "yes", "д", "да")


def now_text(args):
    if getattr(args, "at", None):
        return model.format_time(model.parse_time(args.at))
    return model.format_time(datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))


def spec_for(args):
    return vocab.Spec(registries=getattr(args, "registry", None))


def outbox_for(args):
    return args.outbox or os.path.abspath(args.context).rstrip(os.sep) + ".outbox"


def open_package(args, spec):
    """The person's package; ``--seed`` makes Event salts reproducible, for a synthetic context only."""
    package = Package(args.context, spec)
    package.opaque = True  # the person's window issues opaque record ids (Annex B, "No existence oracles")
    seed = getattr(args, "seed", None)
    if seed:
        synthetic = package.manifest.get("synthetic") is True if package.exists() else \
            getattr(args, "synthetic", False)
        if not synthetic:
            raise import_assessment.Refused("--seed is for synthetic contexts only (examples and tests)")
        package.seed = seed
    return package


def key_path(context):
    return os.path.abspath(context).rstrip(os.sep) + ".holder-key"


def make_key(context):
    """The holder key (§12.3 step 11) next to the person's folder, readable by their user account only."""
    path = key_path(context)
    if not os.path.exists(path):
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as handle:
            handle.write(os.urandom(32).hex() + "\n")
    return path


def load_key(args, ctx):
    path = getattr(args, "holder_key_file", None) or (key_path(args.context) if os.path.isfile(key_path(args.context))
                                                       else None)
    if path:
        with open(path, "rb") as handle:
            return handle.read().strip()
    if ctx.manifest.get("synthetic") is True:
        return grants.EXAMPLE_HOLDER_KEY
    raise import_assessment.Refused("your holder key is missing: setup makes it at %s; give --holder-key-file if you "
                                    "keep it elsewhere" % key_path(args.context))


# ------------------------------------------------------------------ reading drafts back
def norm_groups(spec, draft):
    try:
        _doc, block, _lens = import_assessment.instrument_with_block(spec, draft.get("instrument"))
    except import_assessment.Refused:
        return []
    return [(g.get("id"), (g.get("label") or {}).get("en") or g.get("id")) for g in block.get("normGroups") or []]


def show_draft(term, spec, draft):
    doc = spec.instruments.get(draft.get("instrument")) or {}
    norm = draft.get("normGroup")
    label = dict(norm_groups(spec, draft)).get(norm, norm)
    term.say("%s · taken %s · norm group %s" % (doc.get("name") or draft.get("instrument"),
                                                 draft.get("administeredAt") or "(blank)", label or "(blank)"))
    for entry in draft.get("scores") or []:
        values = ["%s %s" % (k, entry[k]) for k in ("raw",) + import_assessment.STANDARDIZED
                  if k in entry and entry[k] is not None]
        term.say("   %-28s %s" % (entry.get("label") or entry.get("scale"), " · ".join(values) or "(blank)"))


def type_draft(term, draft, spec=None):
    """The person types or fixes the numbers; Enter keeps a value, '-' leaves it blank (IMA-2)."""
    answer = term.ask("Date you took it (YYYY-MM-DD) [%s]:" % (draft.get("administeredAt") or ""))
    if answer:
        draft["administeredAt"] = answer
    groups = norm_groups(spec, draft) if spec is not None else []
    if groups:
        menu = " · ".join("%d %s" % (n, label) for n, (_gid, label) in enumerate(groups, 1))
        answer = term.ask("Norm group on your report: %s (Enter keeps it, - leaves it blank):" % menu)
        if answer == "-":
            draft["normGroup"] = None
        elif answer.isdigit() and 0 < int(answer) <= len(groups):
            draft["normGroup"] = groups[int(answer) - 1][0]
    for entry in draft.get("scores") or []:
        for kind in ("raw",) + import_assessment.STANDARDIZED:
            if kind not in entry:
                continue
            answer = term.ask("%s, %s [%s]:" % (entry.get("label") or entry["scale"], kind,
                                                 "" if entry[kind] is None else entry[kind]))
            if answer == "-":
                entry[kind] = None
            elif answer:
                entry[kind] = import_assessment._number(answer)
    return draft


def read_back(term, spec, drafts):
    """Step 2 of the person's path: "yes, as on my report" once per report, or typing the numbers. The draft is
    checked first, so the person is never asked to confirm what the holder would then refuse."""
    for draft in drafts:
        while True:
            show_draft(term, spec, draft)
            try:
                import_assessment.check_draft(spec, draft)
                problem = None
            except import_assessment.Refused as refused:
                problem = str(refused)
            if problem:
                term.say("This draft cannot be brought as it is: %s. Ask your agent to fix the draft, or type the "
                         "numbers yourself." % problem)
                answer = term.ask("t type or fix the numbers · n stop").lower()
            else:
                answer = term.ask("As on your report? y yes · t type or fix the numbers · n stop").lower()
            if answer in ("y", "yes"):
                if problem:
                    continue
                break
            if answer == "t":
                type_draft(term, draft, spec)
                continue
            raise import_assessment.Refused("stopped by the person")
    return drafts


def drafts_from(args, spec):
    if args.transcript:
        if not args.instrument:
            raise import_assessment.Refused("--transcript needs --instrument")
        with open(args.transcript, "r", encoding="utf-8") as handle:
            return [import_assessment.parse_transcript(spec, args.instrument, handle.read())]
    if args.draft:
        return import_assessment.load_drafts(args.draft)
    if args.instrument:
        return [import_assessment.template(spec, args.instrument)]
    raise import_assessment.Refused("give --draft, --transcript or --instrument")


# ------------------------------------------------------------------ the person's stance and words
def ask_stance(term, package, rid, at):
    """Step 3: what fits; for parts, which scales; then the person's own words, with or without the result."""
    record = package.record(rid)
    labels = window.scale_labels(record)
    term.say("Result %s: %s" % (rid, ", ".join(labels)))
    while True:
        stance = STANCE_BY_KEY.get(term.ask(STANCE_MENU + ":"))
        if stance:
            break
    fits, not_fits, part_words = None, None, None
    if stance == "parts":
        for number, label in enumerate(labels, 1):
            term.say("   %d %s" % (number, label))
        fits = pick(labels, term.ask("Which scales fit? (numbers, comma-separated):"))
        not_fits = pick(labels, term.ask("Which do not fit? (numbers; Enter for none — the others stay not said):"))
        part_words = term.ask("Your words about it (optional):") or None
    window.record_stance(package, rid, stance, at, fits=fits, words=part_words, not_fits=not_fits)
    if stance not in ("doesnt-fit", "later"):
        ask_words(term, package, at, about=rid)
    return stance


def pick(labels, answer):
    return [labels[int(n) - 1] for n in answer.replace(" ", "").split(",") if n.isdigit() and
            0 < int(n) <= len(labels)]


def ask_words(term, package, at, about=None):
    text = term.ask("A sentence for your agent about how to work with you (optional):")
    if not text:
        return None
    link = about if about and yes(term, "Keep it with this result?", default=True) else None
    return window.add_words(package, text, at, about=link, synthetic=package.manifest.get("synthetic") is True)


# ------------------------------------------------------------------ commands
def cmd_setup(args, term):
    term.say("Your agent asks to set up two things, once: a folder for your context, kept private to your user "
             "account, with its holder key next to it (%s), and one step in its own settings so that it starts every "
             "session with what you allow. Keep the folder and the key out of your agent's file tools."
             % os.path.abspath(args.context))
    if not yes(term, "Set them up?", default=True):
        term.say("Nothing was set up.")
        return 0
    package = open_package(args, spec_for(args))
    if not package.exists():
        first = term.ask("To start, one sentence your agent should know about how to work with you:")
        if not first:
            term.say("Nothing was set up: a context starts from something you say (§4.2).")
            return 0
        at = now_text(args)
        manifest = {"format": "ohc.context", "specVersion": "0.1.0-draft", "id": args.subject + ":context",
                    "version": at[:10] + ".1", "subject": {"id": args.subject}, "holder": "subject",
                    "created": at, "conformance": {"level": "L2", "modules": ["core", "governance"],
                                                   "subjectIsAdult": True},
                    "parties": [{"id": args.agent, "partyKind": "agent", "label": args.agent_label}],
                    "policy": {"admission": "subject-only", "resolver": "returnDialog"}}
        if args.synthetic:
            manifest["synthetic"] = True
        package.create(manifest, private=not args.synthetic)
        cid = window.add_words(package, first, at, synthetic=args.synthetic)
        package.append_event({"at": at, "eventType": "record-written", "actor": "subject", "records": [cid]})
        package.save(at)
    if not (package.manifest or {}).get("synthetic"):
        term.say("Your holder key: %s" % make_key(args.context))
    here = os.path.abspath(__file__)
    registries = "".join(" --registry %s" % os.path.abspath(r) for r in args.registry or [])
    term.say("Session start:  python3 %s serve %s --for %s --purpose assist-personal --render agent%s"
             % (here, os.path.abspath(args.context), args.agent, registries))
    term.say("Each prompt:    python3 %s notices %s --for %s" % (here, os.path.abspath(args.context), args.agent))
    return 0


def cmd_bring(args, term, retake=False):
    spec = spec_for(args)
    at = now_text(args)
    drafts = read_back(term, spec, drafts_from(args, spec))
    before = open_package(args, spec)
    earlier = [r for r in import_assessment.current_imported(before)
               if (r.get("instrument") or {}).get("id") in [d.get("instrument") for d in drafts]]
    result = import_assessment.import_result(args.context, drafts, at, report_path=args.report, spec=spec,
                                             seed=args.seed, opaque=True,
                                             synthetic=before.manifest.get("synthetic") is True)
    package = open_package(args, spec)
    for rid in result["assessments"]:
        ask_stance(term, package, rid, at)
    if retake:
        for record in earlier:
            if yes(term, "Mark your earlier result of %s as not current?" %
                   (record.get("administeredAt") or {}).get("start"), default=True):
                window.mark_not_current(package, record["id"], at)
    package.save(at)
    term.say("Brought: %s" % ", ".join(result["assessments"]))
    return 0


def cmd_review(args, term):
    spec = spec_for(args)
    at = now_text(args)
    package = open_package(args, spec)
    ask_stance(term, package, args.record, at)
    package.save(at)
    return 0


def cmd_words(args, term):
    at = now_text(args)
    package = open_package(args, spec_for(args))
    if ask_words(term, package, at, about=args.about):
        package.save(at)
    return 0


def draft_from_record(spec, record):
    draft = import_assessment.template(spec, (record.get("instrument") or {}).get("id"))
    draft["administeredAt"] = (record.get("administeredAt") or {}).get("start")
    draft["normGroup"] = (record.get("normGroup") or {}).get("id")
    draft["form"] = (record.get("instrument") or {}).get("form")
    draft["mode"] = record.get("mode")
    values = dict((r.get("construct"), r) for r in record.get("results") or [])
    for entry in draft["scores"]:
        result = values.get(entry["scale"]) or {}
        if "raw" in entry:
            entry["raw"] = result.get("raw")
        standardized = result.get("standardized") or {}
        if standardized.get("type") in entry:
            entry[standardized["type"]] = standardized.get("value")
    return draft


def cmd_correct(args, term):
    """Fix a number: a new result that supersedes the old one with the same scorer (R-V2), then the stance."""
    spec = spec_for(args)
    at = now_text(args)
    record = open_package(args, spec).record(args.record)
    if record is None or not model.is_imported_result("AssessmentRecord", record):
        raise import_assessment.Refused("%s is not an imported result" % args.record)
    draft = type_draft(term, draft_from_record(spec, record), spec)
    drafts = read_back(term, spec, [draft])
    result = import_assessment.import_result(args.context, drafts, at, supersedes=args.record, spec=spec,
                                             seed=args.seed, opaque=True,
                                             synthetic=record.get("synthetic") is True)
    package = open_package(args, spec)
    for rid in result["assessments"]:
        ask_stance(term, package, rid, at)
    package.save(at)
    return 0


def show_preview(term, result, as_json=False):
    """What the agent would receive, as it receives it (its session-start text), then, for the person only, what
    it would not."""
    if as_json:
        term.say(jsonio.dumps_pretty(result["receives"]))
    else:
        term.say("Your agent would receive this at the start of a session:")
        term.say(rendering.render_agent(result["context"], result["receives"], result["grant"]))
    if result["notIncluded"]:
        term.say("Only you see this — not included:")
        for entry in result["notIncluded"]:
            term.say("  - %s%s: %s" % (entry["kind"], " \"%s\"" % entry["label"] if entry.get("label") else "",
                                        entry["why"]))


def run_screen(term, ctx, args, at, start=None):
    """The agreement screen. ``start``: the ticks and the agent's words of a withdrawn grant (a narrower one)."""
    view = window.screen(ctx, args.grantee, args.purpose, model.parse_time(at), operator=args.operator)
    rows = dict((r["id"], r["ticked"]) for r in view["rows"])
    words = dict((w["id"], w["ticked"]) for w in view["otherWords"])
    toggles = dict(view["toggles"])
    note = None
    if start is not None:
        rows, words, toggles = window.ticks_from(view, start)
        note = window.own_note(start)
    if args.why_file:
        with open(args.why_file, "r", encoding="utf-8") as handle:
            note = handle.read().strip()
    while True:
        shown = dict(view)
        shown["rows"] = [dict(r, ticked=rows[r["id"]]) for r in view["rows"]]
        shown["otherWords"] = [dict(w, ticked=words[w["id"]]) for w in view["otherWords"]]
        shown["toggles"] = toggles
        shown["note"] = note
        term.say(window.render_screen(shown))
        answer = term.ask("Untick or tick: a result number, w<number> for your words, a/b/c for what it may do; "
                          "p preview; ok confirm the whole screen; q quit:").lower()
        if answer == "q":
            return None
        if answer in ("a", "b", "c"):
            key = window.TOGGLES["abc".index(answer)]
            toggles[key] = not toggles[key]
        elif answer.isdigit() and 0 < int(answer) <= len(view["rows"]):
            row = view["rows"][int(answer) - 1]
            if row["servable"]:
                rows[row["id"]] = not rows[row["id"]]
        elif answer.startswith("w") and answer[1:].isdigit() and 0 < int(answer[1:]) <= len(view["otherWords"]):
            wid = view["otherWords"][int(answer[1:]) - 1]["id"]
            words[wid] = not words[wid]
        elif answer in ("p", "ok"):
            gid = next_numbered_id(set(i.id for i in ctx.items if i.id), "g-")
            grant = window.build_grant(view, at, gid, rows=rows, words=words, toggles=toggles, note=note)
            if answer == "p":
                try:
                    show_preview(term, window.preview(ctx, grant, args.purpose, model.parse_time(at),
                                                      load_key(args, ctx)))
                except (import_assessment.Refused, window.Refused) as refused:
                    term.say("No preview: %s. Your screen is unchanged." % refused)
                except grants.Denied as denied:
                    term.say("No preview: this agreement would serve nothing (%s)." % denied.code)
                continue
            return grant


def cmd_agree(args, term, start=None):
    """Step 4: the agreement screen; confirming the whole screen in this window is the explicit consent."""
    spec = spec_for(args)
    at = now_text(args)
    ctx = model.Context(args.context, spec)
    grant = run_screen(term, ctx, args, at, start=start)
    if grant is None:
        term.say("Nothing was agreed.")
        return 0
    package = open_package(args, spec)
    window.confirm_grant(package, grant)
    package.save(at)
    term.say("Agreed: %s, until %s." % (grant["id"], window.day_text(grant["constraints"]["expiresAt"])))
    return 0


def cmd_preview(args, term):
    spec = spec_for(args)
    ctx = model.Context(args.context, spec)
    grant = ctx.record(args.grant)
    if grant is None or ctx.kind_of(args.grant) != "Grant":
        raise import_assessment.Refused("%s is not a grant" % args.grant)
    result = window.preview(ctx, grant, args.purpose, model.parse_time(now_text(args)), load_key(args, ctx))
    show_preview(term, result, as_json=args.json)
    return 0


def cmd_withdraw(args, term):
    """Step 5: untick later. The grant is withdrawn and the agent told to purge; a narrower one is a new screen."""
    spec = spec_for(args)
    at = now_text(args)
    package = open_package(args, spec)
    grant = package.record(args.grant)
    if grant is None or grant.get("kind") != "Grant":
        raise import_assessment.Refused("%s is not a grant" % args.grant)
    if not yes(term, "Withdraw your agreement %s with %s? Your agent is told to delete what it kept." %
               (args.grant, grant.get("grantee"))):
        return 0
    notice = window.withdraw(package, args.grant, at, outbox=outbox_for(args))
    package.save(at)
    term.say("Withdrawn; your agent must delete what it kept by %s." % notice["purgeBy"])
    if yes(term, "Make a new, narrower agreement now? It starts as you had it; untick what you want.", default=True):
        args.grantee, args.purpose = grant["grantee"], grant["purposes"][0]
        args.operator, args.why_file = getattr(args, "operator", None), None
        return cmd_agree(args, term, start=grant)
    return 0


def cmd_erase(args, term):
    spec = spec_for(args)
    at = now_text(args)
    ctx = model.Context(args.context, spec)
    plan = window.erase_plan(ctx, args.record)
    erase_words = []
    for wid in plan["words"]:
        if yes(term, "Your words \"%s\" cite it. Erase them too? (Kept, they stay protected as now.)" %
               (ctx.record(wid) or {}).get("text")):
            erase_words.append(wid)
    erase_report = bool(plan["report"]) and yes(term, "Erase the report you added as well?")
    if not yes(term, "Erase %s now? This cannot be undone." % args.record):
        return 0
    package = open_package(args, spec)
    result = window.erase(package, ctx, args.record, at, erase_words=erase_words, erase_report=erase_report,
                          outbox=outbox_for(args))
    kept = [w for w in plan["words"] if w not in erase_words]
    if kept and yes(term, "Your kept words stay protected like the result was. Treat them as ordinary words from now on? "
                          "(Your own agent gets them either way when you tick them.)"):
        for wid in kept:
            window.relax(package, wid, at)
    package.save(at)
    term.say("Erased: %s. Agents that received it are told to delete it." % ", ".join(result["erased"]))
    return 0


def cmd_playbooks(args, term):
    """The ways of working your agent receives with a lens: the descriptor's, others pinned or in the registry that
    name the lens, or none (LensAdoption.playbooks)."""
    spec = spec_for(args)
    at = now_text(args)
    ctx = model.Context(args.context, spec)
    lens = ctx.lens_doc(args.lens)
    if lens is None:
        raise import_assessment.Refused("unknown lens %s" % args.lens)
    options = list(lens.get("playbooks") or [])
    for pid, doc in sorted(spec.playbooks.items()):
        if args.lens in (doc.get("lenses") or []) and pid not in options:
            options.append(pid)
    for doc in ctx.pinned_playbooks.values():
        if args.lens in (doc.get("lenses") or []) and doc.get("id") not in options:
            options.append(doc["id"])
    for number, pid in enumerate(options, 1):
        doc = ctx.playbook_doc(pid) or {"id": pid}
        term.say("  %d %s" % (number, window.playbook_label(doc)))
    picked = term.ask("Which ones? (numbers; 0 for none; Enter keeps the lens's own):")
    if picked == "":
        chosen = list(lens.get("playbooks") or [])
    elif picked.strip() == "0":
        chosen = []
    else:
        chosen = [options[int(n) - 1] for n in picked.replace(" ", "").split(",") if n.isdigit() and
                  0 < int(n) <= len(options)]
    package = open_package(args, spec)
    window.choose_playbooks(package, ctx, args.lens, chosen, at)
    package.save(at)
    return 0


def cmd_serve(args):
    """The session-start hook: the projection under the grant, rendered for the agent (CONTEXT-03 0.2.0)."""
    spec = spec_for(args)
    ctx = model.Context(args.context, spec)
    moment = model.parse_time(args.now) if args.now else model.parse_time(now_text(args))
    import ohc_query

    if getattr(args, "for") and not args.grant:
        # the one current grant of this grantee for this purpose: the agent's hook survives any change of mind
        state = model.State(ctx, moment)
        current = [i.id for i in ctx.items if i.kind == "Grant" and i.data.get("grantee") == getattr(args, "for")
                   and args.purpose in (i.data.get("purposes") or []) and state.grant_status(i.id, moment) == "given"
                   and not ohc_query.grant_problems(ctx, i.id)]
        if len(current) > 1:
            raise import_assessment.Refused("more than one current agreement with %s for %s: name one with --grant"
                                            % (getattr(args, "for"), args.purpose))
        args.grant = current[0] if current else None
    if not args.grant:
        raise grants.Denied("not-granted")
    grant = ctx.record(args.grant)
    if ctx.kind_of(args.grant) != "Grant" or ohc_query.grant_problems(ctx, args.grant):
        raise grants.Denied("not-granted")
    nonce = None
    if args.seed:
        if ctx.manifest.get("synthetic") is not True:
            raise import_assessment.Refused("--seed is for synthetic contexts only (examples and tests)")
        nonce = grants.new_nonce(args.seed.encode("utf-8"), args.id)
    projection = grants.build_projection(ctx, args.grant, args.purpose, moment, args.id, holder_key=load_key(args, ctx),
                                         nonce=nonce)
    if args.keep and args.no_log:
        raise import_assessment.Refused("--keep needs the projection-served Event: drop --no-log (EV-4)")
    if not args.no_log:
        package = open_package(args, spec)
        package.append_event({"at": model.format_time(moment), "eventType": "projection-served", "actor": "holder",
                              "counterparty": grant["grantee"], "grant": args.grant, "purpose": args.purpose,
                              "records": sorted(grants.served_id_set(projection)), "message": projection["id"],
                              "outcome": "served"})
        if args.keep:
            jsonio.write_pretty(os.path.join(args.context, "projections", "%s.json" % args.id), projection)
        package.save(model.format_time(moment))
    if args.render == "json":
        sys.stdout.write(jsonio.dumps_pretty(projection))
    else:
        sys.stdout.write(rendering.render_agent(ctx, projection, grant))
    return 0


def cmd_notices(args):
    outbox = outbox_for(args)
    if args.ack:
        package = open_package(args, spec_for(args))
        window.acknowledge(outbox, package, args.ack, now_text(args))
        package.save(now_text(args))
        return 0
    for message in window.pending_notices(outbox, getattr(args, "for")):
        sys.stdout.write(json.dumps(message, ensure_ascii=False) + "\n")
    return 0


HELP = {
    "setup": "start your context and holder key; print the two steps for your agent's settings",
    "template": "print a blank draft of a test's scores, for your agent to fill from your report",
    "bring": "bring a test result: check the numbers, then say what fits",
    "retake": "bring a new result of a test you took again",
    "review": "change what you said about a result (fits, parts fit, not sure, dispute, doesn't fit)",
    "words": "add a sentence for your agent about how to work with you",
    "correct": "fix a number in a result you brought",
    "agree": "the agreement screen: what your agent may see and do",
    "preview": "show what your agent receives under an agreement",
    "withdraw": "withdraw an agreement; your agent is told to delete what it kept",
    "erase": "erase a result, and the words and report that go with it",
    "playbooks": "choose the ways of working your agent gets with a lens",
    "serve": "(your agent's session-start step) print what it receives",
    "notices": "(your agent's per-prompt step) print withdrawals and erasures it must act on",
}


DECIDING = {"setup": cmd_setup, "bring": cmd_bring, "retake": lambda a, t: cmd_bring(a, t, retake=True),
            "review": cmd_review, "words": cmd_words, "correct": cmd_correct, "agree": cmd_agree,
            "preview": cmd_preview, "withdraw": cmd_withdraw, "erase": cmd_erase, "playbooks": cmd_playbooks}


def parser():
    top = argparse.ArgumentParser(description="The person's window (reference holder program).")
    sub = top.add_subparsers(dest="command")
    sub.required = True
    commands = {}
    for name in ("setup", "bring", "retake", "review", "words", "correct", "agree", "preview", "withdraw", "erase",
                 "playbooks", "serve", "notices", "template"):
        cmd = sub.add_parser(name, help=HELP[name], description=HELP[name])
        if name != "template":
            cmd.add_argument("context")
        cmd.add_argument("--at")
        cmd.add_argument("--registry", action="append")
        cmd.add_argument("--outbox")
        cmd.add_argument("--holder-key-file")
        cmd.add_argument("--seed", help="reproducible Event salts; synthetic contexts only (examples, tests)")
        commands[name] = cmd
    commands["setup"].add_argument("--subject", required=True, help="who the context is about, e.g. urn:ohc:person:ines")
    commands["setup"].add_argument("--agent", default="a-01")
    commands["setup"].add_argument("--agent-label", default="Personal agent")
    commands["setup"].add_argument("--synthetic", action="store_true", help="a fictional person (examples, tests)")
    for name in ("bring", "retake"):
        commands[name].add_argument("--draft")
        commands[name].add_argument("--transcript")
        commands[name].add_argument("--instrument")
        commands[name].add_argument("--report")
    for name in ("review", "correct", "erase"):
        commands[name].add_argument("record")
    commands["words"].add_argument("--about")
    for name in ("agree",):
        commands[name].add_argument("--grantee", required=True)
        commands[name].add_argument("--purpose", required=True)
        commands[name].add_argument("--operator", choices=["employer", "school"])
        commands[name].add_argument("--why-file")
    commands["preview"].add_argument("--grant", required=True)
    commands["preview"].add_argument("--purpose", required=True)
    commands["preview"].add_argument("--json", action="store_true", help="the projection itself, not its text")
    commands["withdraw"].add_argument("grant")
    commands["playbooks"].add_argument("lens")
    commands["serve"].add_argument("--grant", help="a named agreement (default: the current one of --for)")
    commands["serve"].add_argument("--for", help="the agent: serve its one current agreement for --purpose")
    commands["serve"].add_argument("--purpose", required=True)
    commands["serve"].add_argument("--render", choices=["agent", "json"], default="agent")
    commands["serve"].add_argument("--now")
    commands["serve"].add_argument("--id", default="prj-session")
    commands["serve"].add_argument("--no-log", action="store_true")
    commands["serve"].add_argument("--keep", action="store_true",
                                   help="keep the holder's copy of the served projection in projections/<id>.json")
    commands["notices"].add_argument("--for")
    commands["notices"].add_argument("--ack")
    commands["template"].add_argument("--instrument", required=True)
    return top


def main(argv=None, terminal=None):
    """``terminal`` is for tests of the window's dialogue only; the command line always opens ``/dev/tty``."""
    try:
        args = parser().parse_args(argv)
    except SystemExit:
        return 2
    try:
        if args.command == "template":
            sys.stdout.write(jsonio.dumps_pretty(import_assessment.template(spec_for(args), args.instrument)))
            return 0
        if args.command == "serve":
            return cmd_serve(args)
        if args.command == "notices":
            return cmd_notices(args)
        try:
            term = terminal or Terminal.open()
        except NoTerminal:
            sys.stderr.write("refused: the person's window needs the person's own terminal; nothing was decided\n")
            return NO_TERMINAL
        return DECIDING[args.command](args, term)
    except (import_assessment.Refused, window.Refused) as refused:
        sys.stderr.write("refused: %s\n" % refused)
        return 1
    except grants.Denied as denied:
        sys.stdout.write(json.dumps({"format": "ohc.experimental.denial", "code": denied.code}) + "\n")
        return 1
    except EOFError:
        sys.stderr.write("stopped: no answer; nothing more was decided\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
