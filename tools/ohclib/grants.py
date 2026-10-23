"""Grant evaluation and projection (SPECIFICATION.md §12.3), aliases and HMAC handles (§15.3).

``project()`` implements §12.3 step by step and returns a Projection document
(§14.1). The holder key ``K_holder`` is a secret of the holder; the reference tools
accept it on the command line. ``EXAMPLE_HOLDER_KEY`` exists only so that the
synthetic examples in this repository can be regenerated reproducibly.

The specification states these rules (§12.2, §12.3, §14.1); the summary here is for readers of the code:

- Records are also filtered by the request's ``select``: a record is served when it
  passes the grant and matches at least one requested selector (when ``select`` is
  given). A requested selector the grant does not cover yields a ``not-disclosed``
  absence, whether or not matching records exist (R-G5).
- A grant *covers* a requested selector when one of its include selectors subsumes
  it (every field of the include selector appears in the requested selector with a
  subset of its values) and no exclude selector subsumes it.
- Superseded records are not served in current views; with ``asOf`` the
  supersession is evaluated as known at ``asOf``.
- RecallCues are served only under a grant holding the ``recall`` action (RC-6).
- Served records never carry ``kind`` (the member implies it), nor ``underGrant``,
  ``recordedBy``, ``ext`` or ``importedFrom.run``.
- ``summary`` mode reduces Claims to ``id, facet, predicate, horizon, text, absence,
  valid, contexts``; Episode accounts keep only ``narrator, narratedAt, addedAt,
  accountKind, happened, didOrTried, lang, mediaType`` (never inner experience);
  every other kind loses evidence, grounds, counter-evidence, confidence, rationale,
  derivation, provenance and notes, and an AssessmentRecord its ``source`` (PJ-8).
- ``obligations.decisionUse`` is always present: the grant's ``decisionUse``, else
  ``deny`` (R-G14). A partly endorsed record's ``derived`` entry carries ``endorsedPart``
  (PJ-8).
- The proposer view (§12.5, ``own_proposals``) also serves the grantee's own proposed
  records and its records that expired undecided, under the same scope rules.
- ``rule-only`` serves only Claims with facets ``boundary``, ``preference`` and
  ``commitment`` and ``state`` claims with predicates ``availability`` or ``load``,
  reduced to ``id, facet, predicate, text``.
- Excerpts are generated only for ``text-position`` spans whose source text is
  readable; the excerpt ``selector`` is the text-quote selector generated at serve
  time.
"""

import base64
import datetime
import hashlib
import hmac
import os
import unicodedata

from . import jcs, model, vocab

EXAMPLE_HOLDER_KEY = b"ohc-example-holder-key-synthetic-only"
MODE_WIDTH = {"answer-only": 0, "rule-only": 1, "summary": 2, "full": 3}
SOURCE_ACTION_TIER = {"source-index": "index", "source-summary": "summary", "cite-excerpt": "excerpt",
                      "open-verbatim": "verbatim"}
CONTENT_ACTIONS = ("read", "suggest", "write")
RULE_ONLY_FACETS = ("boundary", "preference", "commitment")
RULE_ONLY_STATE = ("availability", "load")
SUMMARY_CLAIM_FIELDS = ("id", "facet", "predicate", "horizon", "text", "absence", "valid", "contexts")
# Episode accounts in summary mode keep what happened and what was done, never inner experience (§12.2).
SUMMARY_ACCOUNT_FIELDS = ("narrator", "narratedAt", "addedAt", "accountKind", "happened", "didOrTried", "lang")
SUPPORT_FIELDS = ("evidence", "grounds", "counterEvidence", "confidence", "rationale", "derivedFrom",
                  "generatedBy", "importedFrom", "note")
ALWAYS_DROP = ("kind", "underGrant", "recordedBy", "ext")
PSYCH_FACETS = ("state", "declared-value", "disposition", "belief")
MEMBERS = (
    ("statements", "claims", "Claim"), ("statements", "practices", "Practice"),
    ("statements", "lensAdoptions", "LensAdoption"), ("statements", "assessments", "AssessmentRecord"),
    ("statements", "healthRefs", "HealthRef"),
    ("experience", "episodes", "Episode"), ("experience", "sources", "Source"),
    ("interpretations", "interpretations", "Interpretation"), ("interpretations", "modelViews", "ModelView"),
    ("interpretations", "patterns", "Pattern"), ("interpretations", "tensions", "Tension"),
    ("interpretations", "parts", "Part"),
    ("recall", "recallCues", "RecallCue"), ("recall", "outcomes", "Outcome"),
    ("links", "relations", "Relation"),
)
KIND_MEMBER = dict((kind, (group, name)) for group, name, kind in MEMBERS)


class Denied(Exception):
    """§12.3 denial; ``code`` describes the grant or the request, never the data (H-5)."""

    def __init__(self, code):
        Exception.__init__(self, code)
        self.code = code


# ------------------------------------------------------------------ keys
def b64url(raw):
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def hkdf_sha256(key, info, length=32, salt=b""):
    """RFC 5869 HKDF with SHA-256."""
    prk = hmac.new(salt or b"\x00" * 32, key, hashlib.sha256).digest()
    out, block, counter = b"", b"", 1
    while len(out) < length:
        block = hmac.new(prk, block + info + bytes([counter]), hashlib.sha256).digest()
        out += block
        counter += 1
    return out[:length]


def subject_alias(holder_key, subject_id, grantee):
    """§12.3 step 11."""
    raw = hmac.new(holder_key, (subject_id + "|" + grantee).encode("utf-8"), hashlib.sha256).digest()
    return "urn:ohc:alias:" + base64.b32encode(raw).decode("ascii").lower()[0:26]


def grant_key(holder_key, grant_id):
    return hkdf_sha256(holder_key, ("ohc-grant|" + grant_id).encode("utf-8"))


def handle(holder_key, grant_id, source_id, selector=None):
    """§15.3: ``"hmac:" + base64url(HMAC-SHA256(K_g, sourceId + "|" + JCS(selector)))``."""
    selector = selector or {"type": "whole"}
    message = (source_id + "|" + jcs.canonicalize(selector)).encode("utf-8")
    return "hmac:" + b64url(hmac.new(grant_key(holder_key, grant_id), message, hashlib.sha256).digest())


def new_nonce(seed=None, label=""):
    if seed is None:
        return b64url(os.urandom(16))
    return b64url(hmac.new(seed, ("nonce|" + label).encode("utf-8"), hashlib.sha256).digest()[:16])


# ------------------------------------------------------------- selectors
def record_lens(item):
    data = item.data
    lens = model.lens_id_of(data)
    if lens:
        return lens
    if item.kind == "Practice":
        return (data.get("source") or {}).get("lens")
    return None


def record_facets(item):
    data = item.data
    if item.kind == "Claim":
        return [data.get("facet")] if data.get("facet") else []
    return list(data.get("facets") or [])


def matches(selector, item, state):
    """AND across fields, OR within a field (§12.1)."""
    data = item.data
    for field, values in selector.items():
        if field == "all":
            continue
        values = set(values)
        if field == "kinds" and item.kind not in values:
            return False
        if field == "facets" and not values.intersection(record_facets(item)):
            return False
        if field == "predicates" and data.get("predicate") not in values:
            return False
        if field == "horizons" and data.get("horizon") not in values:
            return False
        if field == "contexts" and not values.intersection(data.get("contexts") or []):
            return False
        if field == "categories" and not values.intersection(state.categories(item.id)):
            return False
        if field == "tiers" and state.tier(item.id) not in values:
            return False
        if field == "lenses" and record_lens(item) not in values:
            return False
        if field == "ids" and item.id not in values:
            return False
    return True


def names_special(selector, item=None, state=None):
    """R-G3(b): a special record is reached only by a selector that names its id, its lens, or one of its
    categories whose minimum tier is special. Without a record, a static test of the selector."""
    if item is None or state is None:
        if selector.get("ids") or selector.get("lenses"):
            return True
        spec = state.spec if state is not None else None
        cats = selector.get("categories") or []
        if spec is None:
            return bool(cats)
        return any(spec.categories_min.get(c) == "special" for c in cats)
    if item.id in (selector.get("ids") or []):
        return True
    lens = record_lens(item)
    if lens and lens in (selector.get("lenses") or []):
        return True
    special_cats = set(c for c in state.categories(item.id) if state.spec.categories_min.get(c) == "special")
    return bool(special_cats.intersection(selector.get("categories") or []))


def names_sensitive(selector):
    return bool(selector.get("ids") or selector.get("categories") or selector.get("lenses") or
                selector.get("kinds") or selector.get("facets"))


def subsumes(general, specific):
    """True when every record matching ``specific`` also matches ``general``."""
    fields = [f for f in general if f != "all"]
    if not fields:
        return bool(general.get("all"))
    for field in fields:
        if field not in specific:
            return False
        if not set(specific[field]).issubset(set(general[field])):
            return False
    return True


def covers(grant, selector):
    scope = grant.get("scope") or {}
    for exclude in scope.get("exclude") or []:
        if subsumes(exclude, selector):
            return False
    for include in scope.get("include") or []:
        if subsumes(include, selector):
            return True
    return False


# ------------------------------------------------------------- §12.3
def check_grant(state, grant, requester, purpose, now, action="read"):
    """§12.3 steps 1-2. Raises Denied."""
    if grant is None or grant.get("grantee") != requester:
        raise Denied("not-granted")
    if grant.get("effect", "allow") == "deny":
        raise Denied("not-granted")
    status = state.grant_status(grant.get("id"), now)
    if status == "expired":
        raise Denied("expired-grant")
    if status != "given":
        raise Denied("not-granted")
    constraints = grant.get("constraints") or {}
    not_before = model.parse_time(constraints.get("notBefore")) if constraints.get("notBefore") else None
    if not_before is not None and now < not_before:
        raise Denied("not-granted")
    if purpose not in (grant.get("purposes") or []) or purpose in state.spec.prohibited_purposes:
        raise Denied("purpose-mismatch")
    actions = set(grant.get("actions") or [])
    if action == "read" and not actions.intersection(CONTENT_ACTIONS):
        raise Denied("not-granted")
    if action != "read" and action not in actions:
        raise Denied("not-granted")


def deny_grants_for(state, requester, now):
    out = []
    for item in state.ctx.grants:
        data = item.data
        if data.get("effect") == "deny" and data.get("grantee") == requester and \
                state.grant_status(item.id, now) == "given":
            out.append(data)
    return out


def source_tier(state, grant, item):
    """§15.3: min(grant source action, grant.maxSourceTier, source.maxRelease, custody ceiling)."""
    data = item.data
    granted = "none"
    for action in grant.get("actions") or []:
        tier = SOURCE_ACTION_TIER.get(action)
        if tier and vocab.release_rank(tier) > vocab.release_rank(granted):
            granted = tier
    ceiling = default_max_release(data)
    custody = data.get("custody") or {}
    confidentiality = custody.get("confidentiality", "none")
    custody_ceiling = None
    if confidentiality != "none":
        info = state.spec.custody.get(confidentiality) or {}
        custody_ceiling = info.get("ceilingWithRelease") if custody.get("releaseRef") else info.get("ceilingWithoutRelease")
    tier = vocab.min_release(granted, grant.get("maxSourceTier", "none"), ceiling, custody_ceiling)
    if tier == "verbatim":
        tier = "excerpt"  # verbatim never travels inside a projection (§12.3 step 10)
    return tier


def default_max_release(data):
    if data.get("maxRelease"):
        return data["maxRelease"]
    custody = data.get("custody") or {}
    if custody.get("confidentiality", "none") != "none" or data.get("containsThirdParty"):
        return "index"
    if ((data.get("ext") or {}).get("gum.import") is not None) or \
            (data.get("importedFrom") or {}).get("system") == "gum-ai":
        return "index"
    return "summary"


def own_proposal(state, item, requester):
    """§12.5 proposer view: the requester's own proposed record, or one that expired undecided."""
    status = state.status.get(item.id)
    if status is None or item.data.get("assertedBy") != requester:
        return False
    return status.admission == "proposed" or (status.admission == "declined" and status.declined_reason == "expired")


def scope_passes(state, grant, item, requester, now, denies=None, own_proposals=False):
    """§12.3 steps 3-7 for one record: admission, erasure and supersession, person-only, deny grants, exclude,
    include and the R-G3 naming rule. Shared by projections, answers and the verbatim step-up (§15.4)."""
    rid = item.id
    status = state.status.get(rid)
    if status is None:
        return False
    own = own_proposals and own_proposal(state, item, requester)
    if status.admission != "active" and not own:
        return False
    if rid in state.tombstoned or state.superseded(rid):
        return False
    if status.endorsement == "rejected":
        return False
    if "person-only" in state.handling(rid):
        return False
    if denies is None:
        denies = deny_grants_for(state, requester, now)
    for deny in denies:
        for selector in (deny.get("scope") or {}).get("include") or []:
            if matches(selector, item, state):
                return False
    scope = grant.get("scope") or {}
    if any(matches(selector, item, state) for selector in scope.get("exclude") or []):
        return False
    explicit = (grant.get("basis") or {}).get("legal") == "explicit-consent"
    tier = state.tier(rid)
    named = state.audience(rid) == "named"
    for selector in scope.get("include") or []:
        if not matches(selector, item, state):
            continue
        if tier == "special":
            if explicit and names_special(selector, item, state):
                return True
        elif tier == "sensitive" or named:
            if names_sensitive(selector):
                return True
        else:
            return True
    return False


def verbatim_refusal(state, grant, item, requester, purpose, now):
    """§15.4 holder checks for one Source before a verbatim step-up: the grant is in force for the purpose, the
    Source passes §12.3 steps 3-7, and the verbatim tier is allowed by the grant, the Source and its custody.
    Returns None when allowed, or a denial code."""
    try:
        check_grant(state, grant, requester, purpose, now, action="open-verbatim")
    except Denied as denied:
        return denied.code
    if item is None or item.kind != "Source":
        return "not-granted"
    if not scope_passes(state, grant, item, requester, now):
        return "not-granted"
    step = grant.get("stepUp") or {}
    if grant.get("maxSourceTier") != "verbatim" or step.get("required") is not True:
        return "not-granted"
    data = item.data
    custody = data.get("custody") or {}
    confidentiality = custody.get("confidentiality", "none")
    ceiling = None
    if confidentiality != "none":
        info = state.spec.custody.get(confidentiality) or {}
        ceiling = info.get("ceilingWithRelease") if custody.get("releaseRef") else info.get("ceilingWithoutRelease")
    if vocab.min_release("verbatim", default_max_release(data), ceiling or "verbatim") != "verbatim":
        return "not-granted"
    return None


def evaluate(state, grant, requester, purpose, now, select=None, mode=None, without_interpretations=False,
             own_proposals=False):
    """§12.3 steps 1-9. Returns ``(served_items, mode)`` in storage order. Raises Denied."""
    check_grant(state, grant, requester, purpose, now)
    effective_mode = grant.get("mode", "summary")
    if mode:
        if MODE_WIDTH.get(mode, 3) > MODE_WIDTH.get(effective_mode, 2):
            raise Denied("not-granted")
        effective_mode = mode
    scope = grant.get("scope") or {}
    includes = scope.get("include") or []
    denies = deny_grants_for(state, requester, now)
    actions = set(grant.get("actions") or [])

    def passes(item):
        rid = item.id
        if not scope_passes(state, grant, item, requester, now, denies, own_proposals):
            return False
        status = state.status.get(rid)
        own = own_proposals and own_proposal(state, item, requester)
        if item.kind == "HealthRef":
            if purpose != "health-coordination" or not any(
                    rid in (s.get("ids") or []) for s in includes if matches(s, item, state)):
                return False
        if item.kind in model.INTERPRETATION_LAYER and not own:
            policy = grant.get("interpretations", "subject-endorsed")
            if policy == "none" or without_interpretations:
                return False
            if policy == "subject-endorsed":
                if not (item.data.get("assertedBy") == "subject" or status.endorsed_by_subject and
                        status.endorsement in ("endorsed", "partial")):
                    return False
        if item.kind in model.INTERPRETATION_LAYER and own and without_interpretations:
            return False
        if item.kind == "Claim" and item.data.get("origin") == "inferred" and not own:
            psych = item.data.get("facet") in PSYCH_FACETS or "mental-health" in state.categories(rid)
            if psych and grant.get("interpretations", "subject-endorsed") != "all" and not status.endorsed_by_subject:
                return False  # PJ-4
        if status.epistemic == "frame-relative":
            lens = record_lens(item)
            if not any(lens in (s.get("lenses") or []) for s in includes if matches(s, item, state)):
                return False
        if item.kind == "RecallCue" and ("recall" not in actions or status.lifecycle in ("paused", "retired")):
            return False
        if item.kind == "Source" and source_tier(state, grant, item) == "none":
            return False
        if purpose == "recall-support" and item.kind == "Episode":
            if state.recall(rid) not in ("ask-each-time", "permitted"):
                return False
        if select:
            if not any(matches(selector, item, state) for selector in select):
                return False
        if effective_mode == "answer-only":
            return False
        if effective_mode == "rule-only":
            if item.kind != "Claim":
                return False
            facet = item.data.get("facet")
            if facet not in RULE_ONLY_FACETS and not (
                    facet == "state" and item.data.get("predicate") in RULE_ONLY_STATE):
                return False
        return True

    first = dict((i.id, i) for i in state.items if i.kind in model.CONTENT_KINDS and passes(i))

    def dependent_ok(item):
        data = item.data
        if item.kind == "Tension":
            return all(ref in first for ref in data.get("between") or [])
        if item.kind == "Relation":
            return data.get("from") in first and data.get("to") in first
        if item.kind == "Outcome":
            return all(v in first for v in (data.get("about") or {}).values())
        if item.kind == "RecallCue":
            return all(t in first for t in (data.get("offer") or {}).get("targets") or [])
        return True

    served = []
    for item in state.items:
        if item.id in first and dependent_ok(item):
            served.append(item)
    return served, effective_mode


# ---------------------------------------------------------- transforms
def _strip(record):
    out = dict((k, v) for k, v in record.items() if k not in ALWAYS_DROP)
    if isinstance(out.get("importedFrom"), dict) and "run" in out["importedFrom"]:
        out["importedFrom"] = dict((k, v) for k, v in out["importedFrom"].items() if k != "run")
    return out


def transform(item, mode):
    """§12.3 step 10 for non-Source records."""
    record = _strip(item.data)
    if mode == "rule-only":
        return dict((k, record[k]) for k in ("id", "facet", "predicate", "text") if k in record)
    if mode == "summary":
        if item.kind == "Claim":
            return dict((k, record[k]) for k in SUMMARY_CLAIM_FIELDS if k in record)
        out = dict((k, v) for k, v in record.items() if k not in SUPPORT_FIELDS)
        if item.kind == "AssessmentRecord":
            out.pop("source", None)  # PJ-8: summary mode serves no pointer to the report
        if item.kind == "Episode" and isinstance(out.get("accounts"), list):
            out["accounts"] = [dict((k, v) for k, v in a.items() if k in SUMMARY_ACCOUNT_FIELDS)
                               for a in out["accounts"]]
        return out
    return record


def coarse_day(value):
    """Index tier: capturedAt coarsened to the day, as a PartialTime."""
    if isinstance(value, str):
        return {"start": value[:10], "precision": "day"}
    if isinstance(value, dict):
        out = dict(value)
        if isinstance(out.get("start"), str):
            out["start"] = out["start"][:10]
        if isinstance(out.get("end"), str):
            out["end"] = out["end"][:10]
        if out.get("precision") == "exact":
            out["precision"] = "day"
        return out
    return value


def read_vault_text(ctx, data):
    locator = ((data.get("content") or {}).get("locator") or {})
    rel = locator.get("vaultPath")
    if not rel:
        return None
    path = os.path.join(ctx.dir, rel)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "rb") as handle_:
            return unicodedata.normalize("NFC", handle_.read().decode("utf-8"))
    except (OSError, UnicodeDecodeError):
        return None


def cited_spans(served_records, source_id):
    spans = []

    def visit(value):
        if isinstance(value, dict):
            if value.get("source") == source_id and isinstance(value.get("selector"), dict):
                spans.append(value["selector"])
            for item in value.values():
                visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    for record in served_records:
        visit(record)
    unique = []
    for span in spans:
        if not any(jcs.equal(span, other) for other in unique):
            unique.append(span)
    return unique


def serve_source(state, grant, item, holder_key, served_records, read_vault=True):
    data = item.data
    tier = source_tier(state, grant, item)
    out = {"id": data["id"], "sourceKind": data.get("sourceKind")}
    content = data.get("content") or {}
    if content.get("mediaType"):
        out["content"] = {"mediaType": content["mediaType"]}
    if "capturedAt" in data:
        out["capturedAt"] = coarse_day(data["capturedAt"])
    if "contemporaneity" in data:
        out["contemporaneity"] = data["contemporaneity"]
    if "authorship" in data:
        out["authorship"] = {"author": (data.get("authorship") or {}).get("author")}
    if vocab.release_rank(tier) >= vocab.release_rank("summary"):
        if "title" in data:
            out["title"] = data["title"]
        if "summary" in data:
            out["summary"] = data["summary"]
    out["tier"] = tier
    out["handle"] = handle(holder_key, grant["id"], data["id"])
    if tier == "excerpt" and read_vault:
        text = read_vault_text(state.ctx, data)
        excerpts = []
        if text is not None:
            redactions = [r.get("selector") for r in data.get("redactions") or []]
            for selector in cited_spans(served_records, data["id"]):
                if selector.get("type") != "text-position":
                    continue
                start, end = selector.get("start", 0), selector.get("end", 0)
                chars = list(text[start:end])
                for red in redactions:
                    if isinstance(red, dict) and red.get("type") == "text-position":
                        for pos in range(max(start, red["start"]), min(end, red["end"])):
                            chars[pos - start] = "█"
                excerpt = "".join(chars).strip()
                if excerpt:
                    excerpts.append({"handle": handle(holder_key, grant["id"], data["id"], selector),
                                     "selector": {"type": "text-quote", "exact": excerpt}, "text": excerpt})
        if excerpts:
            out["excerpts"] = excerpts
    return out


def referenced_parties(ctx, records):
    found = set()
    for kind, record in records:
        for _path, actor in model.party_refs(kind, record):
            if actor in ctx.parties:
                found.add(actor)
    out = []
    for party in ctx.manifest.get("parties") or []:
        if party.get("id") in found:
            served = {"id": party["id"], "partyKind": party.get("partyKind"), "label": party.get("label")}
            if party.get("role"):
                served["role"] = party["role"]
            out.append(served)
    return out


def valid_until(grant, generated_at):
    constraints = grant.get("constraints") or {}
    expires = model.parse_time(constraints.get("expiresAt"))
    storage = constraints.get("storage", "session")
    if storage == "none":
        limit = generated_at
    elif storage == "until-expiry":
        limit = expires
    else:
        limit = generated_at + datetime.timedelta(hours=12)
    return min(expires, limit) if expires else limit


def require_holder_key(ctx, holder_key):
    """The published example key is accepted only for contexts marked ``synthetic`` (privacy of aliases)."""
    if not holder_key:
        raise ValueError("a holder key is required")
    if holder_key == EXAMPLE_HOLDER_KEY and ctx.manifest.get("synthetic") is not True:
        raise ValueError("the example holder key is only for synthetic contexts; pass the holder's own key")
    return holder_key


def build_projection(ctx, grant_id, purpose, now, projection_id, holder_key=None, select=None,
                     mode=None, as_of=None, without_interpretations=False, nonce=None, request=None,
                     read_vault=True, state=None, own_proposals=False):
    """§12.3 in full: returns a Projection document (§14.1) with its digest."""
    require_holder_key(ctx, holder_key)
    grant_item = ctx.by_id.get(grant_id)
    grant = grant_item.data if grant_item and grant_item.kind == "Grant" else None
    if grant is None:
        raise Denied("not-granted")
    requester = grant.get("grantee")
    state = state or model.State(ctx, as_of or now)
    grant_state = state if as_of is None else model.State(ctx, now)
    check_grant(grant_state, grant, requester, purpose, now)
    served, effective_mode = evaluate(state, grant, requester, purpose, now, select=select, mode=mode,
                                      without_interpretations=without_interpretations, own_proposals=own_proposals)
    sections = {}
    transformed = []
    for item in served:
        if item.kind == "Source":
            continue
        record = transform(item, effective_mode)
        transformed.append((item.kind, record))
    for item in served:
        if item.kind == "Source":
            record = serve_source(state, grant, item, holder_key, [r for _k, r in transformed], read_vault)
            transformed.append((item.kind, record))
    order = dict((item.id, index) for index, item in enumerate(served))
    transformed.sort(key=lambda pair: order.get(pair[1]["id"], 0))
    for kind, record in transformed:
        group, name = KIND_MEMBER[kind]
        sections.setdefault(group, {}).setdefault(name, []).append(record)
    projection = {
        "format": "ohc.projection",
        "specVersion": "0.1.0-draft",
        "id": projection_id,
        "context": {"id": ctx.manifest.get("id"), "version": ctx.manifest.get("version")},
        "subjectAlias": subject_alias(holder_key, ctx.subject_id or "", requester),
        "grantee": requester,
        "grant": grant_id,
    }
    if request:
        projection["request"] = request
    projection["purpose"] = purpose
    projection["mode"] = effective_mode
    if as_of is not None:
        projection["asOf"] = model.format_time(as_of)
    if own_proposals:
        projection["ownProposals"] = True
    projection["generatedAt"] = model.format_time(now)
    projection["validUntil"] = model.format_time(valid_until(grant, now))
    projection["nonce"] = nonce or new_nonce()
    parties = referenced_parties(ctx, transformed)
    if parties:
        projection["parties"] = parties
    for group in ("statements", "experience", "interpretations", "recall", "links"):
        if group in sections:
            projection[group] = dict((name, sections[group][name]) for g, name, _k in MEMBERS
                                     if g == group and name in sections[group])
    projection["derived"] = dict((item.id, state.derived(item.id, as_of or now)) for item in served)
    absences = []
    for selector in select or []:
        if not covers(grant, selector):
            absences.append({"selector": selector, "code": "not-disclosed"})
    if absences:
        projection["absences"] = absences
    projection["completeness"] = "partial"
    projection["omissions"] = "hidden"
    handling = {}
    for item in served:
        codes = sorted(state.handling(item.id))
        if codes:
            handling[item.id] = codes
    constraints = grant.get("constraints") or {}
    projection["obligations"] = {
        "storage": constraints.get("storage", "session"), "forwarding": False, "crossContextUse": False,
        "decisionUse": constraints.get("decisionUse", "deny"), "delegable": False, "handling": handling,
    }
    projection["digest"] = projection_digest(projection)
    return projection


def projection_digest(projection):
    body = dict((k, v) for k, v in projection.items() if k != "digest")
    return jcs.digest(body)


def served_ids(projection):
    """Every served record id of a Projection, by member."""
    out = {}
    for group, name, _kind in MEMBERS:
        for record in (projection.get(group) or {}).get(name) or []:
            if isinstance(record, dict):
                out.setdefault(name, []).append(record.get("id"))
    return out


def served_id_set(projection):
    """Every served record id of a Projection, as a set."""
    return set(rid for ids in served_ids(projection).values() for rid in ids)


def strip_holder_keyed(record):
    """Remove the fields that only the holder key can reproduce (handles)."""
    out = dict((k, v) for k, v in record.items() if k not in ("handle", "excerpts"))
    return out
