"""The session-start rendering for a persistent agent (CONTEXT-03 0.2.0; PB-5).

A pure function of the projection, the grant (``basis.note`` and constraints) and the documents pinned in the
person's context: the descriptors of the served lenses and the playbooks of §2.2 of LENSES.md. It reads no record
the projection does not carry and never widens the grant: the playbook steps are guidance, and the grant line above
them says what the agreement allows (PB-4). The holder prints it into the session from outside the agent's
reasoning (H-17); nothing here is written anywhere.
"""

from . import model, window

MARK = {"stated": "✓", "confirmed": "✓", "partly-confirmed": "◐", "hypothesis": "~", "pending": "~"}
STANCE = {
    "confirmed": "the person said it fits — a dated reading they recognise, not a fact about them",
    "partly-confirmed": "the person said parts fit",
    "hypothesis": "the person is not sure it fits — ask before relying on any scale",
    "pending": "not decided yet — ask first",
}
PLAYBOOK_STANCE = {"hypothesis": "the person is not sure it fits: ask first",
                   "pending": "not decided yet: ask first", "contested": "the person disputes it: only ask"}


def _day(text):
    moment = model.parse_time(text)
    return "%d %s %d" % (moment.day, moment.strftime("%b"), moment.year) if moment else "?"


def _en(value):
    if isinstance(value, dict):
        return value.get("en") or next(iter(value.values()), "")
    return value or ""


def _lower_first(text):
    return text[:1].lower() + text[1:] if text[1:2].islower() else text


def pinned_playbook(ctx, playbook_id):
    """A playbook only when the context pins it (PB-5: the rendering uses pinned documents; W-PB5 otherwise)."""
    for pin in ctx.manifest.get("playbooks") or []:
        if isinstance(pin, dict) and pin.get("id") == playbook_id:
            return ctx.playbook_doc(playbook_id, pin.get("version"))
    return None


def fitting_scales(endorsed_part):
    """The scale labels named as fitting in a PJ-8 text ("Fits: A, B. Does not fit: …")."""
    return window.parse_endorsed(endorsed_part)[0]


def scale_stances(record, derived):
    """{scale label: "fits" | "does-not-fit" | "not-said"} for a partly confirmed result (PJ-8); {} otherwise."""
    if derived.get("label") != "partly-confirmed":
        return {}
    fits, not_fits, _words = window.parse_endorsed(derived.get("endorsedPart"))
    out = {}
    for result in record.get("results") or []:
        label = result.get("label") or result.get("construct")
        out[label] = "fits" if label in fits else ("does-not-fit" if label in not_fits else "not-said")
    return out


SCALE_MARK = {"fits": "✓ ", "does-not-fit": "✗ ", "not-said": "? "}
SCALE_NOTE = {"does-not-fit": "they said it does not fit", "not-said": "not said: ask first"}


def _stance_key(derived):
    if derived.get("contested"):
        return "contested"
    return derived.get("label")


class Rendering(object):
    def __init__(self, ctx, projection, grant):
        self.ctx = ctx
        self.spec = ctx.spec
        self.p = projection
        self.grant = grant
        self.derived = projection.get("derived") or {}
        self.statements = projection.get("statements") or {}
        self.constraints = grant.get("constraints") or {}
        self.infer = "infer" in (grant.get("actions") or [])
        self.weigh = (projection.get("obligations") or {}).get("decisionUse") == "approval-required"
        self.lines = []

    def out(self, text=""):
        self.lines.append(text)

    # ---------------------------------------------------------------- pieces
    def lens_doc(self, ref):
        return self.ctx.lens_doc(ref.get("id"), ref.get("version")) or {}

    def instrument_name(self, record):
        doc = self.spec.instruments.get((record.get("instrument") or {}).get("id")) or {}
        name = doc.get("name") or ""
        return name.split(" (")[0] if name else None

    def result_title(self, record):
        doc = self.lens_doc(record.get("lens") or {})
        return " · ".join(x for x in (self.instrument_name(record), _en(doc.get("name"))) if x)

    def header(self):
        party = dict((p.get("id"), p) for p in self.ctx.manifest.get("parties") or []).get(self.p.get("grantee")) or {}
        purpose = next((c for c in self.spec.catalogs["purposes"]["codes"] if c["code"] == self.p.get("purpose")), {})
        storage = (self.p.get("obligations") or {}).get("storage")
        notes = {"until-expiry": "notes until %s" % _day(self.constraints.get("expiresAt")),
                 "session": "notes for this session only", "none": "no notes"}.get(storage, "notes: %s" % storage)
        self.out("OHC · %s · grant %s · %s · %s %s UTC · %s" % (
            party.get("label") or self.p.get("grantee"), self.p.get("grant"),
            _en(purpose.get("label")).lower() or self.p.get("purpose"), _day(self.p.get("generatedAt")),
            (self.p.get("generatedAt") or "")[11:16], notes))

    def words(self):
        claims = self.statements.get("claims") or []
        if not claims:
            return
        self.out("What the person said — act on these")
        for claim in claims:
            derived = self.derived.get(claim.get("id")) or {}
            if derived.get("contested"):
                self.out("  ✗ \"%s\" — disputed: only ask" % claim.get("text"))
            elif derived.get("label") in ("stated", "confirmed"):
                self.out("  ✓ \"%s\"" % claim.get("text"))
            else:
                self.out("  ~ \"%s\" — not confirmed: ask before acting on it" % claim.get("text"))

    def results(self):
        records = self.statements.get("assessments") or []
        if not records:
            return
        self.out("Their results — dated readings by an instrument they brought")
        for record in records:
            derived = self.derived.get(record.get("id")) or {}
            key = _stance_key(derived)
            mark = "✗" if key == "contested" else MARK.get(derived.get("label"), "~")
            stance = "the person disputes it — only ask about it" if key == "contested" else STANCE.get(
                derived.get("label"), "ask first")
            taken = (record.get("administeredAt") or {}).get("start")
            self.out("  %s %s · %s" % (mark, self.result_title(record), stance))
            details = ["taken %s" % _day(taken)] if taken else []
            norm = (record.get("normGroup") or {}).get("id")
            if norm:
                details.append("norm group %s" % self.norm_label(record, norm))
            if details:
                self.out("     " + " · ".join(details))
            if derived.get("endorsedPart"):
                self.out("     %s" % derived["endorsedPart"])
            stances = scale_stances(record, derived)
            if stances:
                self.out("     ✓ fits · ✗ they said it does not fit · ? not said: ask first")
            ranges = self.raw_ranges(record)
            doc = self.lens_doc(record.get("lens") or {})
            descriptions = dict((c.get("id"), c.get("description")) for c in doc.get("constructs") or []
                                if isinstance(c, dict))
            for result in record.get("results") or []:
                if result.get("type") != "dimension-score":
                    continue
                values = []
                if "raw" in result:
                    values.append(str(result["raw"]) + (" on %s–%s" % tuple(ranges) if ranges else ""))
                if result.get("standardized"):
                    values.append("%s %s" % (result["standardized"].get("type"), result["standardized"].get("value")))
                label = result.get("label") or result.get("construct")
                line = "     %s%s %s" % (SCALE_MARK.get(stances.get(label), ""), label, " · ".join(values))
                if descriptions.get(result.get("construct")):
                    line += " — %s" % descriptions[result["construct"]].rstrip(".")
                self.out(line)
            facts = window.plain_facts(self.spec, doc, [r.get("construct") for r in record.get("results") or []])
            if facts:
                self.out("     The test: %s" % " ".join(facts))

    def raw_ranges(self, record):
        """The raw-score range of the instrument's import block, so a bare number has its scale."""
        doc = self.spec.instruments.get((record.get("instrument") or {}).get("id")) or {}
        for score in (doc.get("import") or {}).get("scores") or []:
            if score.get("kind") == "raw" and isinstance(score.get("range"), list) and len(score["range"]) == 2:
                return [("%g" % v) for v in score["range"]]
        return None

    def norm_label(self, record, norm):
        doc = self.spec.instruments.get((record.get("instrument") or {}).get("id")) or {}
        for group in (doc.get("import") or {}).get("normGroups") or []:
            if group.get("id") == norm:
                return _en(group.get("label"))
        return norm

    def served_lenses(self):
        """Lens refs named by served AssessmentRecords, Interpretations and LensAdoptions, in order (PB-5)."""
        out = []
        groups = ((self.statements, "assessments"), (self.p.get("interpretations") or {}, "interpretations"),
                  (self.statements, "lensAdoptions"))
        for group, name in groups:
            for record in group.get(name) or []:
                lens = record.get("lens")
                ref = lens if isinstance(lens, dict) else ({"id": lens} if isinstance(lens, str) else None)
                if ref and ref.get("id") and ref["id"] not in [r["id"] for r in out]:
                    out.append(ref)
        return out

    def speaking(self):
        lenses = [r for r in self.served_lenses() if self.lens_doc(r)]
        if not lenses:
            return
        self.out("How to speak about them")
        for ref in lenses:
            doc = self.lens_doc(ref)
            model_ = doc.get("mentalModel") or {}
            name = _en(doc.get("name"))
            if model_.get("languageGuidance"):
                self.out("  · %s: %s" % (name, model_["languageGuidance"]))
            never = []
            for item in list(model_.get("helperMustNot") or []) + list((model_.get("agentPosture") or {}).get("dont")
                                                                         or []):
                if item not in never:  # a descriptor may say the same thing in both lists
                    never.append(item)
            do = (model_.get("agentPosture") or {}).get("do") or []
            if do:
                self.out("    Do: %s." % "; ".join(item.rstrip(".") for item in do))
            if never:
                self.out("    Never: %s." % "; ".join(item.rstrip(".") for item in never))
            tools = [t for t in doc.get("toolkit") or [] if isinstance(t, dict) and t.get("agentMayOffer") is True]
            if tools:
                self.out("    Tools you may offer: %s." % "; ".join(
                    "%s — %s" % (t.get("name") or t.get("id"), _lower_first(_en(t.get("description")).rstrip(".")))
                    if t.get("description") else (t.get("name") or t.get("id")) for t in tools))

    def lens_stance(self, lens_id):
        """The weakest stance among the served results of a lens (for the playbook qualifier)."""
        keys = []
        for record in self.statements.get("assessments") or []:
            if (record.get("lens") or {}).get("id") == lens_id:
                keys.append(_stance_key(self.derived.get(record.get("id")) or {}))
        for key in ("contested", "pending", "hypothesis"):
            if key in keys:
                return key
        return keys[0] if keys else None

    def adoption_choice(self, lens_id):
        for record in self.statements.get("lensAdoptions") or []:
            if (record.get("lens") or {}).get("id") == lens_id and isinstance(record.get("playbooks"), list):
                return list(record["playbooks"])
        return None

    def construct_label(self, lens_id, construct):
        doc = self.ctx.lens_doc(lens_id) or {}
        for c in doc.get("constructs") or []:
            if isinstance(c, dict) and c.get("id") == construct:
                return _en(c.get("label")) or construct
        return construct.rsplit("/", 1)[-1]

    def playbooks(self):
        """PB-5: for each served lens, the person's playbooks (their adoption's choice, else the descriptor's list)
        that resolve to pinned documents, grouped by situation, with the grant line above them."""
        by_situation, order = {}, []
        for ref in self.served_lenses():
            doc = self.lens_doc(ref)
            chosen = self.adoption_choice(ref["id"])
            ids = chosen if chosen is not None else list(doc.get("playbooks") or [])
            stance = self.lens_stance(ref["id"])
            for pid in ids:
                playbook = pinned_playbook(self.ctx, pid)
                if playbook is None:
                    continue
                for situation in playbook.get("situations") or []:
                    sid = situation.get("id")
                    if sid not in by_situation:
                        by_situation[sid] = {"when": _en(situation.get("when")), "entries": []}
                        order.append(sid)
                    by_situation[sid]["entries"].append((ref, doc, playbook, situation, stance))
        if not order:
            return
        self.out("Ways of working — playbooks of their lenses, by situation. Guidance, not rules about the person: "
                 "their words above come first, and skip a step they have already answered.")
        self.out("Your own crisis protocol comes before any step. Take how they feel from what they tell you; do not "
                 "name a feeling they did not name.")
        self.out("Your agreement: guesses — %s · weighing accepted results — %s" % (
            "yes" if self.infer else "no", "yes" if self.weigh else "no"))
        for sid in order:
            self.out("  %s" % by_situation[sid]["when"])
            for ref, doc, playbook, situation, stance in by_situation[sid]["entries"]:
                name = _en(playbook.get("name"))
                if len(playbook.get("lenses") or []) != 1:  # a single-lens playbook's name already names its lens
                    name = "%s · %s" % (_en(doc.get("name")) or ref["id"], name)
                title = "%s (%s)" % (name, playbook.get("author") or "unknown author")
                if stance in PLAYBOOK_STANCE:
                    title += " · " + PLAYBOOK_STANCE[stance]
                self.out("    " + title)
                for number, step in enumerate((situation.get("use") or {}).get("en") or [], 1):
                    self.out("      %d. %s" % (number, step))
                tools = [self.tool_name(doc, t) for t in situation.get("toolkit") or []]
                if tools:
                    self.out("      Tools: %s." % ", ".join(tools))
                results = [self.draws_on(ref["id"], c) for c in situation.get("results") or []]
                if results:
                    self.out("      Draws on: %s." % ", ".join(results))
                if situation.get("watchFor"):
                    self.out("      Watch for: %s" % _en(situation["watchFor"]))

    def draws_on(self, lens_id, construct):
        """A scale a step draws on, with the person's stance when it is not "fits" (delta §3.5)."""
        label = self.construct_label(lens_id, construct)
        for record in self.statements.get("assessments") or []:
            if (record.get("lens") or {}).get("id") != lens_id:
                continue
            stances = scale_stances(record, self.derived.get(record.get("id")) or {})
            for result in record.get("results") or []:
                if result.get("construct") == construct:
                    note = SCALE_NOTE.get(stances.get(result.get("label") or construct))
                    if note:
                        return "%s (%s)" % (label, note)
        return label

    @staticmethod
    def tool_name(doc, tool_id):
        for tool in doc.get("toolkit") or []:
            if isinstance(tool, dict) and tool.get("id") == tool_id:
                return tool.get("name") or tool_id
        return tool_id

    def agreement(self):
        self.out("Your agreement with the person")
        note = (self.grant.get("basis") or {}).get("note")
        if note and window.own_note(self.grant):
            self.out("  · Your disclosure, as they confirmed it: \"%s\"" % note)
        elif note:
            self.out("  · What they confirmed (their window's words; you gave none of your own): \"%s\"" % note)
        if self.infer:
            self.out("  · Guesses: say each as a guess, with another way to see it; they keep or drop it; keep in "
                     "your notes only what they kept, and do not use a dropped guess again.")
        else:
            self.out("  · No guesses about them: the agreement does not include them.")
        if self.weigh:
            accepted, ask, rejected = [], [], []
            for record in self.statements.get("assessments") or []:
                derived = self.derived.get(record.get("id")) or {}
                title = self.instrument_name(record) or _en(self.lens_doc(record.get("lens") or {}).get("name"))
                if derived.get("contested"):
                    ask.append(title)
                elif derived.get("label") == "confirmed":
                    accepted.append(title)
                elif derived.get("label") == "partly-confirmed":
                    stances = scale_stances(record, derived)
                    for state, out in (("fits", accepted), ("not-said", ask), ("does-not-fit", rejected)):
                        names = [k for k, v in stances.items() if v == state]
                        if names:
                            out.append("%s %s" % (title, ", ".join(names)))
                else:
                    ask.append(title)
            if accepted:
                self.out("  · What you propose for them may weigh: %s. Name what you weighed; they say yes or no to "
                         "each proposal." % "; ".join(accepted))
            if ask:
                self.out("    Ask them first before weighing: %s." % "; ".join(ask))
            if rejected:
                self.out("    Do not weigh or ask again: %s (they said it does not fit; use their words instead)."
                         % "; ".join(rejected))
        else:
            self.out("  · Results and readings inform how you work with them; none grounds a choice you make or "
                     "propose for them.")
        storage = (self.p.get("obligations") or {}).get("storage")
        if storage == "until-expiry":
            self.out("  · Keep your notes until %s; purge on notice." % _day(self.constraints.get("expiresAt")))
        elif storage == "session":
            self.out("  · Keep nothing beyond this session, your runtime's transcripts and caches included.")
        else:
            self.out("  · Keep nothing of what you received.")
        self.out("  · Never put their results into anything others use to decide about them.")

    def render(self):
        self.header()
        self.words()
        self.results()
        self.speaking()
        self.playbooks()
        self.agreement()
        return "\n".join(self.lines) + "\n"


def render_agent(ctx, projection, grant):
    """The session-start text for a persistent agent: a pure function of its inputs."""
    return Rendering(ctx, projection, grant).render()
