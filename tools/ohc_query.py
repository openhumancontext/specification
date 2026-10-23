#!/usr/bin/env python3
"""Temporal queries (SPECIFICATION.md §7.3) and grant projections (§12.3) for people and tests.

Usage:
    python3 tools/ohc_query.py <context> as-valid-at --at T [--now T|latest]
    python3 tools/ohc_query.py <context> as-known-at --at K
    python3 tools/ohc_query.py <context> as-understood-at --episode E --at K
    python3 tools/ohc_query.py <context> view-changes --episode E
    python3 tools/ohc_query.py <context> stopped-convincing
    python3 tools/ohc_query.py <context> actions-vs-explanations
    python3 tools/ohc_query.py <context> cross-domain-patterns
    python3 tools/ohc_query.py <context> project --grant G --purpose P [--select JSON] [--mode M]
                               [--as-of T] [--now T|latest] [--without-interpretations] [--own-proposals]
                               [--id prj-…] [--request msg-…] [--holder-key-file FILE] [--nonce N]
    python3 tools/ohc_query.py <context> preview (--grant G | --grant-file FILE) --purpose P [--now T|latest]
                               [--holder-key-file FILE] [--person]

A query about an episode includes the episodes it supersedes. "As understood at"
and the other self-model queries read the subject's own Interpretations; agents'
readings are never presented as the person's understanding. The tool shows
accounts and readings side by side and makes no judgement.

``project`` runs §12.3 and prints the Projection. ``--holder-key-file`` is required unless the context is marked
``synthetic``; only then is the published example key used, and the tool says so on stderr. ``--now`` defaults to
the current time; ``--now latest`` uses the newest time in the context (for reproducible examples). The time used is
echoed on stderr. A grant that fails its schema or the GR rules serves nothing. ``--own-proposals`` asks for the
proposer view (§12.5). Nothing here writes to the context.

``preview`` shows the grantee view of a stored grant or of a draft grant read from a file (H-15): exactly what
``project`` would serve, with the id ``prj-preview`` and the nonce ``preview``. What the grantee would not receive is
shown to the person only: with ``--person`` it is written to the person's own terminal, never to standard output.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ohclib import grants, jsonio, model, vocab  # noqa: E402


class Query(object):
    def __init__(self, ctx):
        self.ctx = ctx
        self.state = model.State(ctx)

    def header(self, name):
        return {"query": name, "context": {"id": self.ctx.manifest.get("id"), "version": self.ctx.manifest.get("version")}}

    def footer(self, out):
        if self.ctx.manifest.get("synthetic") is True:
            out["synthetic"] = True
        return out

    # -------------------------------------------------------------- helpers
    def chain(self, episode_id):
        out, cursor = [], episode_id
        while isinstance(cursor, str) and cursor not in out:
            out.append(cursor)
            cursor = (self.ctx.record(cursor) or {}).get("supersedes")
        return out

    def held_strings(self, rid):
        """heldDuring as strings: ``from`` as recorded, ``until`` as computed by I7 (absent when open)."""
        data = self.ctx.record(rid) or {}
        held = data.get("heldDuring") or {}
        out = {"from": held.get("from") or data.get("formulatedAt") or data.get("recordedAt")}
        if held.get("until"):
            out["until"] = held["until"]
            return out
        successor = self.state.successor.get(rid)
        if successor:
            succ = self.ctx.record(successor) or {}
            succ_held = succ.get("heldDuring") or {}
            out["until"] = succ_held.get("from") or succ.get("formulatedAt") or succ.get("recordedAt")
            return out
        status = self.state.status.get(rid)
        if status and status.not_current:
            latest = max(status.not_current)
            for review in self.ctx.reviews:
                if rid in model.review_targets(review.data) and review.data.get("action") == "mark-not-current" and \
                        model.parse_time(review.data.get("recordedAt")) == latest:
                    out["until"] = review.data.get("recordedAt")
        return out

    def subject_readings(self):
        out = []
        for item in self.ctx.items:
            if item.kind == "Interpretation" and item.data.get("assertedBy") == "subject":
                status = self.state.status.get(item.id)
                if status is not None and status.admission == "active":
                    out.append(item)
        return out

    def held_at(self, rid, moment):
        held = self.held_strings(rid)
        start = model.parse_time(held["from"])
        until = model.parse_time(held["until"]) if held.get("until") else None
        return start is not None and start <= moment and (until is None or moment < until)

    def about_ids(self, data):
        out = []
        for ref in data.get("about") or []:
            if isinstance(ref, str):
                out.append(ref)
        return out

    @staticmethod
    def by_from(entries):
        return sorted(entries, key=lambda e: (model.parse_time(e["heldDuring"]["from"]), e["id"]))

    # -------------------------------------------------------------- queries
    def as_valid_at(self, moment, now=None):
        out = self.header("as-valid-at")
        out["at"] = model.format_time(moment)
        records = []
        now = now or self.ctx.latest_time()
        for item in self.ctx.content:
            data = item.data
            span = None
            if item.kind == "Claim":
                valid = data.get("valid") or {}
                span = (valid.get("from"), valid.get("until"))
            elif item.kind == "Episode":
                occurred = data.get("occurred") or {}
                span = (occurred.get("start"), occurred.get("end") or occurred.get("start"))
            if span is None:
                continue
            start = model.parse_time(span[0]) if span[0] else None
            until = model.parse_time(span[1]) if span[1] else None
            if item.kind == "Episode" and until is not None and span[1] and len(span[1]) == 10:
                until = until.replace(hour=23, minute=59, second=59)
            if (start is None or start <= moment) and (until is None or moment < until or
                                                       (item.kind == "Episode" and moment <= until)):
                if item.kind == "Claim" and start is None and until is None:
                    pass
                records.append({"id": item.id, "kind": item.kind, "derived": self.state.derived(item.id, now)})
        out["records"] = records
        return self.footer(out)

    def as_known_at(self, moment):
        out = self.header("as-known-at")
        out["at"] = model.format_time(moment)
        state = model.State(self.ctx, moment)
        records = []
        for item in state.items:
            if item.kind not in model.CONTENT_KINDS or item.id in state.tombstoned:
                continue
            records.append({"id": item.id, "kind": item.kind, "derived": state.derived(item.id, moment),
                            "superseded": state.superseded(item.id)})
        out["records"] = records
        return self.footer(out)

    def as_understood_at(self, episode_id, moment):
        out = self.header("as-understood-at")
        chain = self.chain(episode_id)
        out["episode"] = episode_id
        out["at"] = model.format_time(moment)
        out["episodeChain"] = chain
        accounts = []
        head = self.ctx.record(episode_id) or {}
        for index, account in enumerate(head.get("accounts") or []):
            added = model.parse_time(account.get("addedAt"))
            if added is None or added > moment:
                continue
            entry = {"episode": episode_id, "index": index, "accountKind": account.get("accountKind"),
                     "narrator": account.get("narrator"), "narratedAt": account.get("narratedAt"),
                     "addedAt": account.get("addedAt")}
            if account.get("understandingThen"):
                entry["understandingThen"] = account["understandingThen"]
            accounts.append(entry)
        out["accounts"] = accounts
        readings = []
        for item in self.subject_readings():
            if not set(self.about_ids(item.data)).intersection(chain):
                continue
            if self.held_at(item.id, moment):
                readings.append({"id": item.id, "stance": item.data.get("stance"),
                                 "heldDuring": self.held_strings(item.id), "recordedAt": item.data.get("recordedAt")})
        out["interpretations"] = self.by_from(readings)
        return self.footer(out)

    def view_changes(self, episode_id):
        out = self.header("view-changes")
        chain = self.chain(episode_id)
        out["episode"] = episode_id
        out["episodeChain"] = chain
        about = [i for i in self.subject_readings() if set(self.about_ids(i.data)).intersection(chain)]
        ids = set(i.id for i in about)
        in_chain = set()
        for item in about:
            prior = item.data.get("supersedes")
            if isinstance(prior, str) and prior in ids:
                in_chain.update([item.id, prior])
        readings, changes = [], []
        for item in about:
            if item.id not in in_chain:
                continue
            entry = {"id": item.id, "stance": item.data.get("stance"), "heldDuring": self.held_strings(item.id)}
            if item.data.get("supersedes"):
                entry["supersedes"] = item.data["supersedes"]
                changes.append({"at": entry["heldDuring"]["from"], "from": item.data["supersedes"], "to": item.id})
            readings.append(entry)
        out["readings"] = self.by_from(readings)
        out["changes"] = sorted(changes, key=lambda c: (model.parse_time(c["at"]), c["to"]))
        return self.footer(out)

    def stopped_convincing(self):
        out = self.header("stopped-convincing")
        entries = []
        for item in self.subject_readings():
            status = self.state.status.get(item.id)
            held = self.held_strings(item.id)
            entry = {"id": item.id}
            successor = self.state.successor.get(item.id)
            if successor:
                entry["reason"] = "superseded"
            elif status is not None and status.endorsement == "rejected":
                entry["reason"] = "rejected"
            elif status is not None and status.not_current:
                entry["reason"] = "marked-not-current"
            elif held.get("until"):
                entry["reason"] = "held-until"
            else:
                continue
            entry["heldDuring"] = held
            if successor:
                entry["supersededBy"] = successor
            entries.append(entry)
        out["interpretations"] = self.by_from(entries)
        return self.footer(out)

    def actions_vs_explanations(self):
        out = self.header("actions-vs-explanations")
        episodes = []
        for item in self.ctx.items:
            if item.kind != "Episode":
                continue
            status = self.state.status.get(item.id)
            if status is None or status.admission != "active" or self.state.superseded(item.id):
                continue
            episodes.append(item)
        episodes.sort(key=lambda i: (model.parse_time((i.data.get("occurred") or {}).get("start")), i.id))
        readings = self.subject_readings()
        rows = []
        for item in episodes:
            data = item.data
            moment = model.parse_time((data.get("occurred") or {}).get("start"))
            did, understood = [], []
            for index, account in enumerate(data.get("accounts") or []):
                if account.get("didOrTried"):
                    did.append({"index": index, "narrator": account.get("narrator"),
                                "accountKind": account.get("accountKind"), "didOrTried": account["didOrTried"]})
                if account.get("understandingThen"):
                    understood.append({"index": index, "understandingThen": account["understandingThen"]})
            held = [r.id for r in readings if moment is not None and self.held_at(r.id, moment)]
            rows.append({"episode": item.id, "occurred": data.get("occurred"), "didOrTried": did,
                         "understoodThen": understood, "readingsHeldAtTheTime": held})
        out["episodes"] = rows
        out["note"] = "Shown side by side; the tool makes no judgement."
        return self.footer(out)

    def cross_domain_patterns(self):
        out = self.header("cross-domain-patterns")
        found = []
        for item in self.ctx.items:
            if item.kind != "Pattern":
                continue
            domains = set()
            for eid in item.data.get("episodes") or []:
                domains.update((self.ctx.record(eid) or {}).get("contexts") or [])
            if item.data.get("patternKind") == "cross-domain" or len(domains) > 1:
                found.append({"id": item.id, "patternKind": item.data.get("patternKind"),
                              "contexts": sorted(domains)})
        out["patterns"] = found
        return self.footer(out)


def load_key(path, ctx):
    """The holder key: from a file, or the published example key for a synthetic context only."""
    if path:
        with open(path, "rb") as handle:
            return handle.read().strip()
    if ctx.manifest.get("synthetic") is True:
        sys.stderr.write("holder key: the published example key (synthetic context)\n")
        return grants.EXAMPLE_HOLDER_KEY
    raise ValueError("--holder-key-file is required: this context is not marked synthetic")


def resolve_now(text, ctx):
    if text in (None, ""):
        import datetime

        moment = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    elif text == "latest":
        moment = ctx.latest_time()
    else:
        moment = model.parse_time(text)
    sys.stderr.write("now: %s\n" % model.format_time(moment))
    return moment


def grant_problems(ctx, grant_id):
    """Schema and GR-* errors of one grant (a grant that fails them serves nothing)."""
    import check

    item = ctx.by_id.get(grant_id)
    if item is None or item.kind != "Grant":
        return ["not-granted"]
    problems = [p for p, _d in ctx.spec.validate_detail("urn:ohc:schema:grant:0.1.0-draft", item.data)]
    checker = check.ContextChecker(ctx, ctx.dir, False)
    checker.check_grant(item)
    problems.extend(f["rule"] for f in checker.f.items if f["severity"] == "error")
    return problems


def preview(ctx, args):
    """The grantee view of a stored or draft grant; the "not included" part only in the person's own terminal."""
    from ohclib import window

    if not args.purpose or not (args.grant or args.grant_file):
        sys.stderr.write("preview needs --purpose and --grant or --grant-file\n")
        return 2
    grant = jsonio.load_json(args.grant_file) if args.grant_file else ctx.record(args.grant)
    if not isinstance(grant, dict) or (args.grant and ctx.kind_of(args.grant) != "Grant"):
        sys.stdout.write(json.dumps({"format": "ohc.experimental.denial", "code": "not-granted"}, indent=2) + "\n")
        return 1
    try:
        key = load_key(args.holder_key_file, ctx)
    except ValueError as error:
        sys.stderr.write("%s\n" % error)
        return 2
    try:
        result = window.preview(ctx, grant, args.purpose, resolve_now(args.now, ctx), key)
    except grants.Denied as denied:
        sys.stdout.write(json.dumps({"format": "ohc.experimental.denial", "code": denied.code}, indent=2) + "\n")
        return 1
    if args.person:
        import ohc_holder

        try:
            term = ohc_holder.Terminal.open()
        except ohc_holder.NoTerminal:
            sys.stderr.write("refused: what is not included is shown only in the person's own terminal\n")
            return ohc_holder.NO_TERMINAL
        term.say("Only you see this — not included: %s" % json.dumps(result["notIncluded"], ensure_ascii=False))
    sys.stdout.write(jsonio.dumps_pretty(result["receives"]))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Temporal queries and projections over an OHC context.")
    parser.add_argument("context")
    parser.add_argument("query", choices=["as-valid-at", "as-known-at", "as-understood-at", "view-changes",
                                          "stopped-convincing", "actions-vs-explanations", "cross-domain-patterns",
                                          "project", "preview"])
    parser.add_argument("--at")
    parser.add_argument("--episode")
    parser.add_argument("--grant")
    parser.add_argument("--purpose")
    parser.add_argument("--select", help="JSON array of GrantSelector objects")
    parser.add_argument("--mode")
    parser.add_argument("--as-of")
    parser.add_argument("--now")
    parser.add_argument("--without-interpretations", action="store_true")
    parser.add_argument("--own-proposals", action="store_true")
    parser.add_argument("--id", default="prj-0001")
    parser.add_argument("--request")
    parser.add_argument("--holder-key-file")
    parser.add_argument("--nonce")
    parser.add_argument("--grant-file")
    parser.add_argument("--person", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    ctx = model.Context(args.context, vocab.Spec())
    query = Query(ctx)
    try:
        if args.query == "as-valid-at":
            result = query.as_valid_at(model.parse_time(args.at), resolve_now(args.now or None, ctx))
        elif args.query == "as-known-at":
            result = query.as_known_at(model.parse_time(args.at))
        elif args.query == "as-understood-at":
            result = query.as_understood_at(args.episode, model.parse_time(args.at))
        elif args.query == "view-changes":
            result = query.view_changes(args.episode)
        elif args.query == "stopped-convincing":
            result = query.stopped_convincing()
        elif args.query == "actions-vs-explanations":
            result = query.actions_vs_explanations()
        elif args.query == "cross-domain-patterns":
            result = query.cross_domain_patterns()
        elif args.query == "preview":
            return preview(ctx, args)
        else:
            if not args.grant or not args.purpose:
                parser.print_usage(sys.stderr)
                return 2
            now = resolve_now(args.now, ctx)
            select = json.loads(args.select) if args.select else None
            try:
                key = load_key(args.holder_key_file, ctx)
            except ValueError as error:
                sys.stderr.write("%s\n" % error)
                return 2
            try:
                if grant_problems(ctx, args.grant):
                    raise grants.Denied("not-granted")
                result = grants.build_projection(
                    ctx, args.grant, args.purpose, now, args.id, holder_key=key,
                    select=select, mode=args.mode, as_of=model.parse_time(args.as_of) if args.as_of else None,
                    without_interpretations=args.without_interpretations, nonce=args.nonce, request=args.request,
                    own_proposals=args.own_proposals)
            except grants.Denied as denied:
                result = {"format": "ohc.experimental.denial", "code": denied.code}
                sys.stdout.write(json.dumps(result, indent=2) + "\n")
                return 1
    except (TypeError, ValueError):
        parser.print_usage(sys.stderr)
        return 2
    sys.stdout.write(jsonio.dumps_pretty(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
