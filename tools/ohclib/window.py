"""The person's window on the holder side (INSTRUMENT-IMPORT.md §5, IMH-1; SPECIFICATION.md §12.1, §15.5).

Pure functions over a context and the person's choices. The command-line window (``tools/ohc_holder.py``) asks the
person in their own terminal and calls these; an agent never calls the deciding ones for the person (C-8…C-10,
H-17). Nothing here decides anything by itself:

- ``record_stance`` and ``add_words``: the person's stance on a result and their own words (R-A1, PJ-8);
- ``screen`` / ``render_screen`` / ``build_grant`` / ``confirm_grant``: the agreement screen, everything ticked by
  default between the person and their own agent (W-12, W-13), nothing pre-ticked when the grantee's operator is
  the person's employer or school (§12.4); confirming the whole screen is the explicit consent (W-14);
- ``preview``: what the grantee would receive (the holder prints it as the agent's session-start text), and, for
  the person only, what it would not (H-15);
- ``withdraw``, ``erase_plan`` / ``erase``, ``mark_not_current``, ``choose_playbooks``: changing one's mind later.
"""

import copy
import datetime
import os
import re

from . import grants, jsonio, model
from .package import next_numbered_id  # message ids only; record ids come from Package.new_id

STANCES = ("fits", "parts", "not-sure", "dispute", "doesnt-fit", "later")
STANCE_ACTION = {"fits": "endorse", "parts": "partially-endorse", "not-sure": "admit", "dispute": "contest",
                 "doesnt-fit": "reject", "later": None}
EMPLOYER_OR_SCHOOL = ("employer", "school")
OTHER_WORD_FACETS = ["goal", "preference", "boundary"]
TERM_DAYS = 179  # within the 180 days of R-G10 for a grant with infer or special records
TOGGLES = ("hypotheses", "weighing", "notes")
TOGGLE_TEXT = {
    "hypotheses": ("Offer guesses about you from these results. For example: \"Planning review on Friday. You "
                   "said %s fits you. A guess: you will feel steadier with one decision and three checked risks. "
                   "Prepare it that way?\" Each is only a guess, with another way to see it; you keep or drop it, "
                   "and it keeps in its notes only what you kept. Unticked: it makes no guesses about you."),
    "weighing": ("Weigh results you accepted when it proposes something for you. For example: \"Two mornings "
                 "without meetings for the analysis (weighed: your result, %s).\" It names what it weighed; you "
                 "say yes or no to each proposal. A result you are not sure about is not weighed until you accept "
                 "it."),
    "notes": ("Keep notes between sessions, until %s. Either way it receives what you allow at the start of every "
              "session; this is about its own notes on your work together."),
}
NEVER_TEXT = ("Never, whatever you tick: put your results into anything others use to decide about you (hiring, "
              "allocating or evaluating your work, promotion, ranking you against others, credit or insurance); "
              "decide anything with a significant effect on you without a person; tailor persuasion or advertising "
              "to you; infer your political views; read your emotions at work or in study; sell your data or train "
              "models for others. You can share your own report yourself.")


class Refused(Exception):
    pass


def day_text(value):
    moment = model.parse_time(value) if isinstance(value, str) else value
    return "%d %s %d" % (moment.day, moment.strftime("%B"), moment.year) if moment else ""


# ------------------------------------------------------------------ stance and words
def endorsed_part_text(fits, not_fits, words=None):
    """PJ-8: "Fits: … Does not fit: …" from the scales the person marked, then their words; a scale in neither part
    is not decided (C-3, C-8)."""
    parts = []
    if fits:
        parts.append("Fits: %s." % ", ".join(fits))
    if not_fits:
        parts.append("Does not fit: %s." % ", ".join(not_fits))
    if words:
        parts.append("\"%s\"" % words.strip().strip("\""))
    return " ".join(parts)


def parse_endorsed(text):
    """(fits, does not fit, the person's words) from a PJ-8 text "Fits: A, B. Does not fit: C. \"words\"";
    anything else is all words."""
    text = (text or "").strip()
    fits, not_fits = [], []
    for head, out in (("Fits: ", fits), ("Does not fit: ", not_fits)):
        if text.startswith(head) and "." in text:
            part, text = text[len(head):].split(".", 1)
            out.extend(p.strip() for p in part.split(",") if p.strip())
            text = text.strip()
    return fits, not_fits, text


def scale_labels(record):
    return [r.get("label") or r.get("construct") for r in record.get("results") or []
            if isinstance(r, dict) and r.get("type") == "dimension-score"]


def record_stance(package, rid, stance, at, fits=None, words=None, not_fits=None):
    """Write the person's stance on a result as a Review by the subject (R-A1). ``parts`` takes the scale labels
    the person said fit and, separately, those they said do not; a scale in neither list stays not said (PJ-8).
    ``later`` writes nothing."""
    if stance not in STANCES:
        raise Refused("unknown stance %s" % stance)
    record = package.record(rid)
    if record is None or record.get("kind", "AssessmentRecord") != "AssessmentRecord" or "results" not in record:
        raise Refused("%s is not a result" % rid)
    action = STANCE_ACTION[stance]
    if action is None:
        return None
    review = {"action": action, "by": "subject", "id": package.new_id("rv-"), "kind": "Review",
              "recordedAt": at, "target": rid}
    if stance == "parts":
        labels = scale_labels(record)
        fits = [f for f in labels if f in (fits or [])]
        if not fits:
            raise Refused("parts fit: mark at least one scale that fits")
        not_fits = [f for f in labels if f in (not_fits or []) and f not in fits]
        review["endorsedPart"] = endorsed_part_text(fits, not_fits, words)
    package.add("Review", dict(sorted(review.items())))
    return review["id"]


def add_words(package, text, at, about=None, facet="preference", synthetic=False):
    """The person's own words to their agent, as a Claim they declare; ``about`` cites a result as its evidence
    (then the sentence is protected like the result, C3); without it the sentence stands on its own."""
    text = (text or "").strip()
    if not text:
        raise Refused("no words")
    claim = {"assertedBy": "subject", "facet": facet, "id": package.new_id("c-"), "kind": "Claim",
             "origin": "declared", "recordedAt": at, "text": text}
    if about:
        claim["evidence"] = [{"kind": "instrument", "ref": about}]
    if synthetic:
        claim["synthetic"] = True
    package.add("Claim", dict(sorted(claim.items())))
    return claim["id"]


def mark_not_current(package, rid, at):
    """After a retake: the earlier result stays as a dated reading and is marked not current by the person."""
    review = {"action": "mark-not-current", "by": "subject", "id": package.new_id("rv-"),
              "kind": "Review", "recordedAt": at, "target": rid}
    package.add("Review", review)
    return review["id"]


# ------------------------------------------------------------------ facts in plain words
def lens_name(doc, lang="en"):
    name = (doc or {}).get("name") or {}
    return name.get(lang) or name.get("en") if isinstance(name, dict) else str(name)


def instrument_short(spec, record):
    doc = spec.instruments.get((record.get("instrument") or {}).get("id")) or {}
    name = doc.get("name") or ""
    return name.split(" (")[0] if name else None


def category_label(spec, code):
    entry = None
    for item in (spec.catalogs.get("categories") or {}).get("codes") or []:
        if item.get("code") == code:
            entry = item
    label = (entry or {}).get("label") or {}
    return (label.get("en") if isinstance(label, dict) else label) or code


YOU_VERBS = {"is": "are", "has": "have", "does": "do", "chooses": "choose", "compares": "compare", "comes": "come",
             "declares": "declare", "states": "state", "tends": "tend", "says": "say", "wants": "want",
             "recognises": "recognise", "values": "value", "intends": "intend", "prefers": "prefer"}


def to_you(text):
    """The same fact, said to the person on their own screen ("you", not "the person")."""
    text = text.replace("the person's", "your").replace("the person", "you")
    return re.sub(r"\byou( then)? (%s)\b" % "|".join(YOU_VERBS),
                  lambda m: "you%s %s" % (m.group(1) or "", YOU_VERBS[m.group(2)]), text)


def plain_facts(spec, doc, constructs=(), you=False):
    """IMH-1 (2): what the lens supports and does not establish, its evidence, the publisher's own stated limits,
    and the special categories that protect a result (naming a construct only when it adds a category). Facts,
    never bans. ``you``: worded for the person's own screen."""
    if you:
        return [to_you(line) for line in plain_facts(spec, doc, constructs)]
    doc = doc or {}
    lines = []
    evidence = doc.get("evidence") or {}
    tier = evidence.get("measurementTier")
    status = evidence.get("ontologicalStatus")
    if status == "symbolic-frame" or tier == "T5":
        lines.append("A symbolic frame: its results are meaningful inside the frame, never empirical facts or "
                     "predictions.")
    elif tier in ("T1", "T2"):
        lines.append("Measured, with independent research behind it.")
    elif tier == "T3":
        lines.append("A published test with research behind it, most of it by the publisher.")
    elif tier == "T4":
        lines.append("Its core claims are contested in research.")
    if doc.get("supports"):
        lines.append("Can help with: %s." % "; ".join(doc["supports"]))
    if doc.get("doesNotEstablish"):
        lines.append("Does not show: %s." % "; ".join(doc["doesNotEstablish"]))
    stated = [r for r in (doc.get("ip") or {}).get("restrictions") or []
              if isinstance(r, str) and not r.lower().startswith(("never store", "internal draft"))]
    if stated:
        lines.append("Stated limits: %s." % "; ".join(stated))
    defaults = doc.get("defaults") or {}
    special = [c for c in defaults.get("categories") or [] if spec.categories_min.get(c) == "special"]
    named = set(special)
    if special:
        lines.append("Protected like %s data." % " and ".join(category_label(spec, c).lower() for c in special))
    labels = dict((c.get("id"), (c.get("label") or {}).get("en")) for c in doc.get("constructs") or []
                  if isinstance(c, dict))
    for construct, extra in sorted((defaults.get("perConstruct") or {}).items()):
        if constructs and construct not in constructs:
            continue
        cats = [c for c in extra.get("categories") or [] if spec.categories_min.get(c) == "special"]
        if cats and not set(cats) <= named:
            lines.append("One scale (%s) is protected like %s data." % (
                labels.get(construct) or construct.rsplit("/", 1)[-1],
                " and ".join(category_label(spec, c).lower() for c in cats)))
    return lines


# ------------------------------------------------------------------ the agreement screen (IMH-1)
def stance_of(status):
    if status is None:
        return "later"
    if status.endorsement == "rejected" or status.admission == "declined":
        return "doesnt-fit"
    if status.contested:
        return "dispute"
    if status.endorsement == "endorsed":
        return "fits"
    if status.endorsement == "partial":
        return "parts"
    if status.admission == "active":
        return "not-sure"
    return "later"


STANCE_TEXT = {
    "fits": "you said it fits",
    "parts": "you said parts fit",
    "not-sure": "you are not sure it fits",
    "dispute": "you dispute it — your agent sees that you dispute it and may only ask you about it",
    "doesnt-fit": "you said it doesn't fit — only you see it",
    "later": "you have not decided yet — your agent does not see it until you do",
}


def adoption_guesses(ctx, state, lens_id):
    """``agentInterpretation`` of the person's active adoption of a lens when it is not ``allowed`` (absent counts
    as ``off``, I5); None when there is no adoption or it allows."""
    for item in ctx.items:
        if item.kind == "LensAdoption" and model.lens_id_of(item.data) == lens_id and not state.superseded(item.id):
            status = state.status.get(item.id)
            if status is not None and status.admission == "active":
                mode = item.data.get("agentInterpretation") or "off"
                return None if mode == "allowed" else mode
    return None


def playbook_choice(ctx, state, lens_id):
    """The person's playbooks for a lens (LENSES.md §2.2): their active adoption's ``playbooks`` when given (``[]``
    is none), otherwise the descriptor's list."""
    for item in ctx.items:
        if item.kind == "LensAdoption" and model.lens_id_of(item.data) == lens_id and \
                isinstance(item.data.get("playbooks"), list):
            status = state.status.get(item.id)
            if status is not None and status.admission == "active" and not state.superseded(item.id):
                return list(item.data["playbooks"])
    doc = ctx.lens_doc(lens_id) or {}
    return list(doc.get("playbooks") or [])


def playbook_label(doc, lens_doc=None):
    """A playbook's name and author; next to its lens, without repeating the lens's name."""
    name = (doc.get("name") or {}).get("en") or doc.get("id")
    if lens_doc and len(doc.get("lenses") or []) == 1 and ": " in name:
        name = name.rsplit(": ", 1)[1]  # "Big Five: basic ways of working" next to Big Five is "basic"
        if name.endswith(" ways of working"):
            name = name[:-len(" ways of working")]
    return "%s (%s)" % (name, doc.get("author") or "unknown author")


def parts_text(endorsed_part):
    fits, not_fits, words = parse_endorsed(endorsed_part)
    out = ["%s fit" % ", ".join(fits)] if fits else []
    if not_fits:
        out.append("%s %s not" % (", ".join(not_fits), "does" if len(not_fits) == 1 else "do"))
    if words:
        out.append(words)
    return "; ".join(out)


def cited(data):
    """The record ids a Claim cites as its evidence."""
    return [g.get("ref") for g in data.get("evidence") or [] if isinstance(g, dict) and isinstance(g.get("ref"), str)]


def words_about(ctx, state, rid):
    out = []
    for item in ctx.items:
        if item.kind != "Claim" or rid not in cited(item.data):
            continue
        status = state.status.get(item.id)
        if status is not None and status.admission == "active" and status.endorsement != "rejected":
            out.append({"id": item.id, "text": item.data.get("text")})
    return out


def screen(ctx, grantee, purpose, now, operator=None):
    """The agreement screen as data. Every row, word and term is ticked, unless the grantee's operator is the
    person's employer or school (then nothing is; §12.4). A row the person said does not fit, or has not decided
    on, is shown without a tick and cannot be ticked (it is not served, §12.3)."""
    state = model.State(ctx, now)
    spec = ctx.spec
    open_default = operator not in EMPLOYER_OR_SCHOOL
    rows, about_results, example = [], set(), None
    for item in ctx.items:
        if item.kind != "AssessmentRecord" or item.id in state.tombstoned:
            continue
        data = item.data
        status = state.status.get(item.id)
        if state.superseded(item.id):
            continue
        stance = stance_of(status)
        servable = stance not in ("doesnt-fit", "later")
        lens_id = model.lens_id_of(data)
        doc = ctx.lens_doc(lens_id, (data.get("lens") or {}).get("version")) or {}
        constructs = [r.get("construct") for r in data.get("results") or [] if isinstance(r, dict)]
        words = words_about(ctx, state, item.id)
        about_results.update(w["id"] for w in words)
        playbooks = []
        for pid in playbook_choice(ctx, state, lens_id):
            pdoc = ctx.playbook_doc(pid)
            if pdoc is not None:
                playbooks.append(playbook_label(pdoc, doc))
        stance_text = STANCE_TEXT[stance]
        if stance == "parts" and status is not None and status.endorsed_part:
            stance_text += ": " + parts_text(status.endorsed_part)
        if example is None and servable and open_default:
            accepted = parse_endorsed(status.endorsed_part)[0] if stance == "parts" and status is not None else (
                scale_labels(data) if stance == "fits" else [])
            example = accepted[0] if accepted else None
        rows.append({"id": item.id, "lens": lens_id, "lensName": lens_name(doc), "version": (data.get("lens") or
                                                                                              {}).get("version"),
                     "instrument": instrument_short(spec, data), "scales": len(constructs), "stance": stance,
                     "stanceText": stance_text, "servable": servable, "ticked": servable and open_default,
                     "words": words, "facts": plain_facts(spec, doc, constructs, you=True), "playbooks": playbooks,
                     "taken": (data.get("administeredAt") or {}).get("start"),
                     "guesses": adoption_guesses(ctx, state, lens_id)})
    others = []
    for item in ctx.items:
        if item.kind != "Claim" or item.id in about_results or item.data.get("assertedBy") != "subject":
            continue
        if item.data.get("facet") not in OTHER_WORD_FACETS or any(
                ctx.kind_of(r) == "AssessmentRecord" for r in cited(item.data)):
            continue
        status = state.status.get(item.id)
        if status is None or status.admission != "active" or status.endorsement == "rejected" or \
                state.superseded(item.id):
            continue
        others.append({"id": item.id, "text": item.data.get("text"), "ticked": open_default,
                       "special": state.tier(item.id) == "special"})
    expires = now + datetime.timedelta(days=TERM_DAYS)
    party = ctx.parties.get(grantee) or {}
    purposes = []
    for code in (spec.catalogs.get("prohibited-purposes") or {}).get("codes") or []:
        purposes.append({"code": code["code"], "label": code["label"]["en"],
                         "definition": (code.get("definition") or {}).get("en")})
    purpose_entry = next((c for c in spec.catalogs["purposes"]["codes"] if c["code"] == purpose), {})
    return {"grantee": grantee, "granteeLabel": party.get("label") or grantee, "purpose": purpose,
            "purposeLabel": (purpose_entry.get("label") or {}).get("en", purpose), "operator": operator,
            "generatedAt": model.format_time(now), "expiresAt": model.format_time(expires), "rows": rows,
            "otherWords": others, "toggles": dict((t, open_default) for t in TOGGLES), "neverPurposes": purposes,
            "example": example}


def render_screen(view):
    """The screen as text, in the person's window (§A.1 of the build contract, with the 12.10 defaults)."""
    lines = ["What \"%s\" may see and do · for %s · until %s" % (view["granteeLabel"], view["purposeLabel"].lower(),
                                                                 day_text(view["expiresAt"]))]
    if view["operator"] in EMPLOYER_OR_SCHOOL:
        lines.append("This agent is run by your %s: nothing is ticked for you. Tick only what you want it to have; "
                     "your agreement is never a condition of your %s." % (
                         view["operator"], "work" if view["operator"] == "employer" else "studies"))
    lines.append("Sees — each result is ticked; untick what you don't want" if view["operator"] not in
                 EMPLOYER_OR_SCHOOL else "Sees — tick what you want")
    for number, row in enumerate(view["rows"], 1):
        mark = "[x]" if row["ticked"] else ("[ ]" if row["servable"] else " - ")
        title = " · ".join(x for x in (row["instrument"], row["lensName"]) if x)
        lines.append(" %s %d. %s · %d scales · %s" % (mark, number, title, row["scales"], row["stanceText"]))
        for word in row["words"]:
            lines.append("       with your words: \"%s\"%s" % (word["text"], "" if row["ticked"] or not row["servable"]
                                                               else " (not given either while this is unticked)"))
        if row["servable"]:
            lines.append("       ways of working: %s · change them with the playbooks command" % (
                ", ".join(row["playbooks"]) or "none"))
            if row.get("guesses"):
                lines.append("       guesses through this lens: %s — your choice when you adopted the lens" % (
                    "ask you first" if row["guesses"] == "ask-first" else "off"))
    for word in view["otherWords"]:
        lines.append("     %s Also seen, not about a test: \"%s\"" % ("[x]" if word["ticked"] else "[ ]", word["text"]))
    lines.append("     Your agent may use what it sees in how it works with you. Untick a result to keep it from "
                 "your agent.")
    lines.append("May do — each is ticked; untick what you don't want" if view["operator"] not in EMPLOYER_OR_SCHOOL
                 else "May do — tick what you want")
    example = view.get("example") or "a tendency"
    for letter, toggle in zip("abc", TOGGLES):
        text = TOGGLE_TEXT[toggle] % (day_text(view["expiresAt"]) if toggle == "notes" else example)
        lines.append(" [%s] %s. %s" % ("x" if view["toggles"][toggle] else " ", letter, text))
    lines.append(NEVER_TEXT)
    lines.append("About the tests")
    for number, row in enumerate(view["rows"], 1):
        lines.append(" %d. %s" % (number, row["instrument"] or row["lensName"]))
        for fact in row["facts"]:
            lines.append("    %s" % fact)
    if view.get("note"):
        lines.append("What your agent says it will do, in its own words: \"%s\"" % view["note"])
    else:
        lines.append("What your agent will be told you agreed to (written by this program; your agent gave no words "
                     "of its own): \"%s\"" % default_note(view["toggles"]["hypotheses"], view["toggles"]["weighing"]))
    lines.append("[ p: show what my agent will receive ]   [ ok: confirm ]")
    return "\n".join(lines) + "\n"


def default_note(hypotheses, weighing):
    """The disclosure written when the agent gave no ``why`` of its own (W-9, W-15). It names no lens, so unticking
    a row never needs a rewrite."""
    parts = []
    if hypotheses:
        parts.append("Which: guesses about how the tendencies in the results you let me see may show in a situation "
                     "you bring up, read from those results and your words about them. Why: to help you notice your "
                     "patterns and choose. How: I say each as a guess, with at least one other way to see it; you "
                     "keep or drop it; I keep in my notes only what you kept, and none is used as a fact about you.")
    else:
        parts.append("I read what you let me see and use it in how I work with you; I write no guesses about you.")
    if weighing:
        parts.append("When I propose something for you, I may weigh a result you accepted; I name what I weighed, "
                     "and you say yes or no.")
    return " ".join(parts)


def build_grant(view, at, grant_id, rows=None, words=None, toggles=None, note=None):
    """One grant from the screen and the person's unticks (``rows``/``words``: {id: bool}; ``toggles``: {name:
    bool}); anything not given keeps the screen's default. One screen records one grant (§12.1)."""
    rows = dict((r["id"], (rows or {}).get(r["id"], r["ticked"]) and r["servable"]) for r in view["rows"])
    words = dict((w["id"], (words or {}).get(w["id"], w["ticked"])) for w in view["otherWords"])
    toggles = dict((t, (toggles or {}).get(t, view["toggles"][t])) for t in TOGGLES)
    lenses, exclude, ids = [], [], []
    for row in view["rows"]:
        if rows[row["id"]]:
            if row["lens"] not in lenses:
                lenses.append(row["lens"])
            ids.extend(w["id"] for w in row["words"])
    # words that stayed special (kept after their result was erased) are reached only by naming them (R-G3(b))
    ids.extend(w["id"] for w in view["otherWords"] if words[w["id"]] and w.get("special"))
    for row in view["rows"]:
        if not rows[row["id"]] and row["lens"] in lenses:
            exclude.append(row["id"])
    include = []
    if lenses:
        include.append({"lenses": lenses})
    if any(words.values()):
        include.append({"facets": list(OTHER_WORD_FACETS)})
        exclude.extend(w for w, ticked in words.items() if not ticked)
    if ids:
        include.append({"ids": ids})
    if not include:
        raise Refused("nothing is ticked: there is nothing to agree to")
    scope = {"include": include}
    if exclude:
        scope["exclude"] = [{"ids": exclude}]
    actions = ["read"] + (["suggest", "infer"] if toggles["hypotheses"] else [])
    constraints = {"expiresAt": view["expiresAt"], "storage": "until-expiry" if toggles["notes"] else "session",
                   "forwarding": False, "crossContextUse": False}
    if toggles["weighing"]:
        constraints["decisionUse"] = "approval-required"
    constraints["delegable"] = False
    grant = {"id": grant_id, "recordedAt": at, "grantor": "subject", "grantee": view["grantee"],
             "purposes": [view["purpose"]], "scope": scope, "actions": actions, "mode": "summary",
             "interpretations": "subject-endorsed", "maxSourceTier": "none", "constraints": constraints,
             "basis": {"legal": "explicit-consent", "note": note or default_note(toggles["hypotheses"],
                                                                                 toggles["weighing"])},
             "expressedBy": {"actor": "subject", "at": at, "channel": "holder-ui"}}
    return grant


def confirm_grant(package, grant, seed=None):
    """The person confirmed the whole screen in their window: that confirmation is the explicit consent (§12.1;
    the ticks are not). Records the Grant and a ``grant-given`` Event."""
    record = dict(grant, kind="Grant")
    package.add("Grant", record)
    package.append_event({"at": grant["recordedAt"], "eventType": "grant-given", "actor": "subject",
                          "counterparty": grant["grantee"], "grant": grant["id"], "records": [grant["id"]]},
                         seed=seed)
    return grant["id"]


# ------------------------------------------------------------------ preview (H-15)
def with_grant(ctx, grant):
    """A shallow copy of ``ctx`` that also holds a draft grant (nothing is written)."""
    draft = copy.copy(ctx)
    draft.items = list(ctx.items)
    draft._add("Grant", dict(grant, kind="Grant"), "grants", "(draft)", "/draft")
    draft._index()
    return draft


def preview(ctx, grant, purpose, now, holder_key):
    """What the grantee would receive under ``grant`` (stored, or a draft), and, for the person only, what it would
    not. The projection is the one ``ohc_query.py project`` would serve, with a preview id and a fixed nonce."""
    if ctx.by_id.get(grant["id"]) is None:
        if ctx.spec.validate("urn:ohc:schema:grant:0.1.0-draft", dict(grant, kind="Grant")):
            raise grants.Denied("not-granted")  # a draft that fails its schema serves nothing, as a stored one
        ctx = with_grant(ctx, grant)
    projection = grants.build_projection(ctx, grant["id"], purpose, now, "prj-preview", holder_key=holder_key,
                                         nonce="preview")
    served = grants.served_id_set(projection)
    state = model.State(ctx, now)
    not_included = []
    for item in ctx.content:
        if item.id in served or item.id in state.tombstoned:
            continue
        status = state.status.get(item.id)
        stance = stance_of(status) if item.kind == "AssessmentRecord" else None
        if stance == "doesnt-fit":
            why = "you said it doesn't fit"
        elif status is not None and status.admission == "proposed":
            why = "you have not decided on it yet"
        elif status is not None and status.endorsement == "rejected":
            why = "you rejected it"
        elif item.kind == "Source":
            why = "your report stays in your vault; this screen never gives it to your agent"
        else:
            why = "not in what you ticked"
        label = item.data.get("text") if item.kind == "Claim" else (
            lens_name(ctx.lens_doc(model.lens_id_of(item.data))) if item.kind == "AssessmentRecord" else None)
        entry = {"id": item.id, "kind": item.kind, "why": why}
        if label:
            entry["label"] = label
        not_included.append(entry)
    return {"receives": projection, "notIncluded": not_included, "context": ctx, "grant": grant}


# ------------------------------------------------------------------ later changes
def write_notice(outbox, message):
    if outbox:
        jsonio.write_pretty(os.path.join(outbox, message["id"] + ".json"), message)
    return message


def next_message_id(outbox, package):
    taken = set(e.get("message") for e in package.events if e.get("message"))
    for folder in (outbox, os.path.join(outbox, "acknowledged") if outbox else None):
        if folder and os.path.isdir(folder):
            taken.update(name[:-5] for name in os.listdir(folder) if name.endswith(".json"))
    return next_numbered_id(taken, "msg-", 4)


def withdraw(package, grant_id, at, purge_by=None, outbox=None, seed=None):
    """Untick later: withdraw the grant (``withdraw-grant``), send ``revocation-notice`` with ``purgeBy`` (C-12).
    A narrower grant is then a new screen the person confirms."""
    grant = package.record(grant_id)
    if grant is None or grant.get("kind") != "Grant":
        raise Refused("%s is not a grant" % grant_id)
    purge_by = purge_by or model.format_time(model.parse_time(at) + datetime.timedelta(days=1))
    review = {"action": "withdraw-grant", "by": "subject", "id": package.new_id("rv-"),
              "kind": "Review", "recordedAt": at, "target": grant_id}
    package.add("Review", review)
    package.append_event({"at": at, "eventType": "grant-withdrawn", "actor": "subject",
                          "counterparty": grant["grantee"], "grant": grant_id, "records": [review["id"]]}, seed=seed)
    message_id = next_message_id(outbox, package)
    package.append_event({"at": at, "eventType": "revocation-notice-sent", "actor": "holder",
                          "counterparty": grant["grantee"], "grant": grant_id, "message": message_id}, seed=seed)
    notice = {"format": "ohc.experimental.revocation-notice", "specVersion": "0.1.0-draft", "id": message_id,
              "from": "holder", "to": grant["grantee"], "at": at, "grant": grant_id, "status": "withdrawn",
              "purgeBy": purge_by}
    return write_notice(outbox, notice)


def erase_plan(ctx, rid):
    """What the person decides on before a result goes (§B.3): the words that cite it and the report Source."""
    record = ctx.record(rid)
    if record is None:
        raise Refused("%s is not in the context" % rid)
    words = [item.id for item in ctx.items if item.kind == "Claim" and rid in cited(item.data)]
    report = record.get("source") if isinstance(record.get("source"), str) and ctx.record(record["source"]) else None
    return {"record": rid, "words": words, "report": report}


def erase(package, ctx, rid, at, erase_words=(), erase_report=False, outbox=None, purge_by=None, seed=None):
    """Erase a result and what the person chose with it. Words they keep keep their tier: a ``restrict`` Review
    records it, because only the person lowers a tier (C3) and the record that raised it is gone. Recipients that
    were served any erased record get an ``erasure-notice`` (§15.5, EV-6)."""
    plan = erase_plan(ctx, rid)
    state = model.State(ctx, model.parse_time(at))
    targets = [rid] + [w for w in plan["words"] if w in set(erase_words)]
    if erase_report and plan["report"]:
        targets.append(plan["report"])
    for word in plan["words"]:
        if word in targets:
            continue
        disclosure = {"sensitivity": state.tier(word)}
        categories = sorted(state.categories(word) - set((ctx.record(word) or {}).get("categories") or []))
        if categories:
            disclosure["addCategories"] = categories
        package.add("Review", {"action": "restrict", "by": "subject", "disclosure": disclosure,
                               "id": package.new_id("rv-"), "kind": "Review", "recordedAt": at,
                               "target": word})
    for target in targets:
        item = ctx.by_id[target]
        if item.kind == "Source":
            package.remove_vault(((item.data.get("content") or {}).get("locator") or {}).get("vaultPath") or "")
        package.replace(target, {"erasedAt": at, "erasedBy": "subject", "erasedKind": item.kind, "id": target,
                                 "kind": "Tombstone", "reason": "subject-request"})
    package.append_event({"at": at, "eventType": "record-erased", "actor": "subject", "records": targets}, seed=seed)
    purge_by = purge_by or model.format_time(model.parse_time(at) + datetime.timedelta(days=1))
    recipients = {}
    for event in package.events:
        if event.get("eventType") in ("projection-served", "answer-served", "export-run", "source-opened") and \
                event.get("counterparty"):
            hit = [t for t in targets if t in (event.get("records") or [])]
            if hit:
                recipients.setdefault(event["counterparty"], set()).update(hit)
    notices = []
    for recipient in sorted(recipients):
        message_id = next_message_id(outbox, package)
        records = sorted(recipients[recipient])
        package.append_event({"at": at, "eventType": "erasure-notice-sent", "actor": "holder",
                              "counterparty": recipient, "records": records, "message": message_id}, seed=seed)
        notices.append(write_notice(outbox, {
            "format": "ohc.experimental.erasure-notice", "specVersion": "0.1.0-draft", "id": message_id,
            "from": "holder", "to": recipient, "at": at, "records": records, "erasedAt": at,
            "purgeBy": purge_by}))
    return {"erased": targets, "notices": notices}


def relax(package, rid, at, sensitivity="personal"):
    """The person lowers the protection of words they kept after erasing the result they cited (C3: only the
    person lowers a tier)."""
    review = {"action": "relax", "by": "subject", "disclosure": {"sensitivity": sensitivity},
              "id": package.new_id("rv-"), "kind": "Review", "recordedAt": at, "target": rid}
    package.add("Review", review)
    return review["id"]


def pending_notices(outbox, grantee=None):
    """Notices not yet acknowledged (the per-prompt hook prints them; the agent purges, its runtime acknowledges)."""
    out = []
    if not outbox or not os.path.isdir(outbox):
        return out
    for name in sorted(os.listdir(outbox)):
        if name.endswith(".json"):
            message = jsonio.load_json(os.path.join(outbox, name))
            if grantee is None or message.get("to") == grantee:
                out.append(message)
    return out


def acknowledge(outbox, package, message_id, at, seed=None):
    """The grantee's runtime acknowledges a notice: the holder records it and files the notice away."""
    path = os.path.join(outbox, message_id + ".json")
    message = jsonio.load_json(path)
    event = {"at": at, "actor": message["to"], "message": message_id}
    if message["format"].endswith("erasure-notice"):
        event.update({"eventType": "erasure-notice-acknowledged", "records": message["records"]})
    else:
        event.update({"eventType": "purge-receipt-received", "grant": message["grant"]})
    package.append_event(event, seed=seed)
    os.makedirs(os.path.join(outbox, "acknowledged"), exist_ok=True)
    os.replace(path, os.path.join(outbox, "acknowledged", message_id + ".json"))
    return event


def choose_playbooks(package, ctx, lens_id, playbooks, at, agent_interpretation=None):
    """The person picks the ways of working for a lens: writes (or supersedes) their adoption of it with
    ``playbooks`` (``[]`` is none). Choosing ways of working does not change whether the agent may read through
    the lens: an adoption keeps its ``agentInterpretation``; a new one starts ``allowed``, as pre-selected in
    CONTEXT-08 0.3.0, unless ``agent_interpretation`` is given. Registry playbooks the person picks are pinned
    (LENSES.md §2.2)."""
    state = model.State(ctx, model.parse_time(at))
    for pid in playbooks:
        doc = ctx.playbook_doc(pid)
        if doc is None or lens_id not in (doc.get("lenses") or []):
            raise Refused("%s is not a playbook of %s (PB-3)" % (pid, lens_id))
    current = None
    for item in ctx.items:
        if item.kind == "LensAdoption" and model.lens_id_of(item.data) == lens_id and not state.superseded(item.id):
            status = state.status.get(item.id)
            if status is not None and status.admission == "active":
                current = item.data
    doc = ctx.lens_doc(lens_id) or {}
    if current is not None:
        adoption = dict((k, v) for k, v in current.items() if k not in ("id", "recordedAt", "supersedes"))
        adoption["supersedes"] = current["id"]
    else:
        adoption = {"assertedBy": "subject", "interpretationAuthors": ["subject"], "kind": "LensAdoption",
                    "lens": {"id": lens_id, "version": doc.get("version")}, "origin": "declared",
                    "route": "self-chosen", "uses": ["store-results"]}
    adoption.update({"id": package.new_id("la-"), "recordedAt": at, "playbooks": list(playbooks),
                     "assertedBy": "subject", "origin": "declared"})
    if agent_interpretation or current is None:
        adoption["agentInterpretation"] = agent_interpretation or "allowed"
    if ctx.manifest.get("synthetic") is True:
        adoption["synthetic"] = True
    package.add("LensAdoption", dict(sorted(adoption.items())))
    have = [(p.get("id"), p.get("version")) for p in package.manifest.get("playbooks") or [] if isinstance(p, dict)]
    for pid in playbooks:
        pdoc = ctx.playbook_doc(pid)
        if (pid, pdoc.get("version")) not in have and ctx.spec.playbook(pid) is pdoc:
            package.pin("playbooks", pdoc)
    return adoption["id"]


def ticks_from(view, grant):
    """The ticks of an earlier grant, laid on a new screen: the person withdrew it to untick one thing, so the rest
    starts as they had it (``rows``, ``words``, ``toggles`` for ``build_grant``)."""
    scope = grant.get("scope") or {}
    lenses, ids, facets = set(), set(), False
    for selector in scope.get("include") or []:
        lenses.update(selector.get("lenses") or [])
        ids.update(selector.get("ids") or [])
        facets = facets or bool(selector.get("facets"))
    excluded = set(i for selector in scope.get("exclude") or [] for i in selector.get("ids") or [])
    rows = dict((r["id"], r["servable"] and r["lens"] in lenses and r["id"] not in excluded) for r in view["rows"])
    words = dict((w["id"], (w["id"] in ids or facets) and w["id"] not in excluded) for w in view["otherWords"])
    constraints = grant.get("constraints") or {}
    toggles = {"hypotheses": "infer" in (grant.get("actions") or []),
               "weighing": constraints.get("decisionUse") == "approval-required",
               "notes": constraints.get("storage") == "until-expiry"}
    return rows, words, toggles


def own_note(grant):
    """The agent's own disclosure on a grant, or None when the note is this program's default (W-15)."""
    note = (grant.get("basis") or {}).get("note")
    actions = grant.get("actions") or []
    weighing = (grant.get("constraints") or {}).get("decisionUse") == "approval-required"
    return None if note in (None, default_note("infer" in actions, weighing)) else note
