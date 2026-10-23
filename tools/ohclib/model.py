"""Loading contexts and computing effective status (§3.3, §6, §7, §11.1).

``Context`` loads a single document (``context.json`` with record arrays) or a
package (manifest with ``collections``, JSON Lines files, ``events.jsonl``,
``projections/``, ``lenses/``, ``vault/`` and ``context.lock.json``).

``State`` replays Reviews at a time ``at`` (as known at ``at``) and computes, for
every record: admission, endorsement, contested, locked, epistemic status,
disclosure (effective tier by C3, categories, handling, audience, recall),
freshness, lifecycle status, held-during interval and the derived label.

Nothing here reads vault content; only file presence is recorded.
"""

import datetime
import os
import re

from . import jsonio, vocab

ZERO_DIGEST = "sha256:" + "0" * 64
UTC = datetime.timezone.utc

CONTENT_KINDS = (
    "Source", "Episode", "Claim", "AssessmentRecord", "LensAdoption", "Practice", "HealthRef",
    "Interpretation", "ModelView", "Tension", "Pattern", "Part", "RecallCue", "Outcome", "Relation",
)
GOVERNANCE_KINDS = ("Review", "Proposal", "Grant", "Event", "Tombstone")
INTERPRETATION_LAYER = ("Interpretation", "ModelView", "Pattern", "Tension", "Part")
FRESHNESS_KINDS = ("Claim", "AssessmentRecord", "LensAdoption", "Practice")
HISTORICAL_KINDS = ("Episode", "Outcome")
EMOTION_PREDICATES = ("mood", "emotion", "stress", "affect")
COLLECTION_ORDER = (
    "claims", "relations", "sources", "episodes", "interpretations", "tensions", "reviews", "proposals",
    "grants", "lensAdoptions", "assessments", "modelViews", "practices", "outcomes", "patterns",
    "recallCues", "parts", "healthRefs", "events",
)


# ------------------------------------------------------------------- time
def parse_time(value):
    """Parse a Date or an RFC 3339 DateTime into an aware UTC datetime (None if absent)."""
    if value is None:
        return None
    if isinstance(value, dict):
        return parse_time(value.get("start"))
    text = str(value)
    if len(text) == 10:
        return datetime.datetime.strptime(text, "%Y-%m-%d").replace(tzinfo=UTC)
    text = text.replace("z", "Z")
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    match = re.match(r"^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})(\.\d+)?([+-]\d{2}:\d{2})?$", text)
    if not match:
        raise ValueError("not a date-time")
    date_part, time_part, frac, offset = match.groups()
    base = datetime.datetime.strptime(date_part + "T" + time_part, "%Y-%m-%dT%H:%M:%S")
    if frac:
        base = base.replace(microsecond=int((frac[1:] + "000000")[:6]))
    if offset:
        sign = 1 if offset[0] == "+" else -1
        hours, minutes = int(offset[1:3]), int(offset[4:6])
        tz = datetime.timezone(sign * datetime.timedelta(hours=hours, minutes=minutes))
    else:
        tz = UTC
    return base.replace(tzinfo=tz).astimezone(UTC)


def format_time(moment):
    """Format an aware datetime as RFC 3339 in UTC with a ``Z`` suffix."""
    moment = moment.astimezone(UTC)
    if moment.microsecond:
        return moment.strftime("%Y-%m-%dT%H:%M:%S.%f").rstrip("0") + "Z"
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


_DURATION = re.compile(
    r"^P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)W)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?$")


def parse_duration(text):
    """Return ``(years, months, timedelta)`` for an ISO 8601 duration, or None."""
    if not isinstance(text, str):
        return None
    match = _DURATION.match(text)
    if not match or text in ("P", "PT"):
        return None
    years, months, weeks, days, hours, minutes, seconds = match.groups()
    delta = datetime.timedelta(
        weeks=int(weeks or 0), days=int(days or 0), hours=int(hours or 0), minutes=int(minutes or 0),
        seconds=float(seconds or 0))
    return int(years or 0), int(months or 0), delta


def add_duration(moment, text):
    parsed = parse_duration(text)
    if parsed is None:
        return None
    years, months, delta = parsed
    if years or months:
        month_index = moment.month - 1 + months + 12 * years
        year = moment.year + month_index // 12
        month = month_index % 12 + 1
        day = moment.day
        while True:
            try:
                moment = moment.replace(year=year, month=month, day=day)
                break
            except ValueError:
                day -= 1
    return moment + delta


def duration_upper_bound(text):
    """An upper bound of a duration as a timedelta (years count as 366 days, months as 31)."""
    parsed = parse_duration(text)
    if parsed is None:
        return None
    years, months, delta = parsed
    return datetime.timedelta(days=366 * years + 31 * months) + delta


# --------------------------------------------------------------- loading
class LoadError(Exception):
    def __init__(self, rule, path, record_id=None):
        Exception.__init__(self, rule)
        self.rule = rule
        self.path = path
        self.record_id = record_id


PATH_RE = re.compile(r"^(?!/)(?!.*\\)(?!.*(?:^|/)\.\.(?:/|$))(?!.*:)[^\x00]+$")


class Item(object):
    """One stored record with its location."""

    __slots__ = ("kind", "data", "collection", "file", "loc", "order")

    def __init__(self, kind, data, collection, file, loc, order):
        self.kind = kind
        self.data = data
        self.collection = collection
        self.file = file
        self.loc = loc
        self.order = order

    @property
    def id(self):
        return self.data.get("id")

    def path(self, field=""):
        if self.loc.startswith("L"):
            return "%s#%s%s" % (self.file, self.loc, field)
        return "%s#%s%s" % (self.file, self.loc, field)


class Context(object):
    """A loaded context in either serialization."""

    def __init__(self, target, spec=None):
        self.spec = spec or vocab.Spec()
        self.findings = []
        target = os.path.abspath(target)
        if os.path.isdir(target):
            self.dir = target
            self.manifest_file = os.path.join(target, "context.json")
        else:
            self.dir = os.path.dirname(target)
            self.manifest_file = target
        self.manifest_rel = os.path.basename(self.manifest_file)
        self.manifest = jsonio.load_json(self.manifest_file)
        self.items = []
        self.projections = {}
        self.lock = None
        self.pinned_lenses = {}
        self.pinned_playbooks = {}
        self.vault_files = []
        self.collection_files = {}
        self.form = "package" if "collections" in self.manifest else "single"
        if self.form == "package":
            self._load_package()
        else:
            self._load_single()
        self._index()

    # ----------------------------------------------------------- serializations
    def _add(self, kind, data, collection, file, loc):
        if isinstance(data, dict) and data.get("kind") == "Tombstone":
            kind = "Tombstone"
        self.items.append(Item(kind, data, collection, file, loc, len(self.items)))

    def _load_single(self):
        for collection in COLLECTION_ORDER:
            records = self.manifest.get(collection)
            if not isinstance(records, list):
                continue
            kind = self.spec.collection_kind.get(collection, "Event" if collection == "events" else None)
            for index, record in enumerate(records):
                if isinstance(record, dict):
                    self._add(kind, record, collection, self.manifest_rel, "/%s/%d" % (collection, index))

    def _load_package(self):
        collections = self.manifest.get("collections") or {}
        listed = set()
        for collection in COLLECTION_ORDER:
            paths = collections.get(collection)
            if paths is None:
                continue
            if isinstance(paths, str):
                paths = [paths]
            kind = self.spec.collection_kind.get(collection, "Event" if collection == "events" else None)
            for rel in paths:
                listed.add(rel)
                self.collection_files.setdefault(collection, []).append(rel)
                if not PATH_RE.match(rel):
                    self.findings.append(("J-6", None, "context.json#/collections/" + collection))
                    continue
                full = os.path.join(self.dir, rel)
                if not os.path.isfile(full):
                    self.findings.append(("CX-2", None, "context.json#/collections/" + collection))
                    continue
                try:
                    lines = jsonio.load_jsonl(full)
                except jsonio.JsonError as error:
                    self.findings.append((error.rule, None, rel + (("#" + error.where) if error.where else "")))
                    continue
                for number, record in lines:
                    self._add(kind, record, collection, rel, "L%d" % number)
        events_path = os.path.join(self.dir, "events.jsonl")
        if "events.jsonl" not in listed and os.path.isfile(events_path):
            self.collection_files.setdefault("events", []).append("events.jsonl")
            try:
                for number, record in jsonio.load_jsonl(events_path):
                    self._add("Event", record, "events", "events.jsonl", "L%d" % number)
            except jsonio.JsonError as error:
                self.findings.append((error.rule, None, "events.jsonl"))
        proj_dir = os.path.join(self.dir, "projections")
        if os.path.isdir(proj_dir):
            for name in sorted(os.listdir(proj_dir)):
                if name.endswith(".json"):
                    rel = "projections/" + name
                    try:
                        self.projections[rel] = jsonio.load_json(os.path.join(proj_dir, name))
                    except jsonio.JsonError as error:
                        self.findings.append((error.rule, None, rel))
        lens_dir = os.path.join(self.dir, "lenses")
        if os.path.isdir(lens_dir):
            for name in sorted(os.listdir(lens_dir)):
                if name.endswith(".json"):
                    rel = "lenses/" + name
                    target = self.pinned_playbooks if name.endswith(".playbook.json") else self.pinned_lenses
                    try:
                        target[rel] = jsonio.load_json(os.path.join(lens_dir, name))
                    except jsonio.JsonError as error:
                        self.findings.append((error.rule, None, rel))
        lock_path = os.path.join(self.dir, "context.lock.json")
        if os.path.isfile(lock_path):
            try:
                self.lock = jsonio.load_json(lock_path)
            except jsonio.JsonError as error:
                self.findings.append((error.rule, None, "context.lock.json"))
        vault_dir = os.path.join(self.dir, "vault")
        if os.path.isdir(vault_dir):
            for base, _dirs, files in os.walk(vault_dir):
                for name in files:
                    full = os.path.join(base, name)
                    self.vault_files.append(os.path.relpath(full, self.dir).replace(os.sep, "/"))
            self.vault_files.sort()

    def package_files(self):
        """Every file of a package except the vault and the lock, as relative paths."""
        out = []
        for base, dirs, files in os.walk(self.dir):
            dirs.sort()
            for name in sorted(files):
                rel = os.path.relpath(os.path.join(base, name), self.dir).replace(os.sep, "/")
                out.append(rel)
        return out

    # ------------------------------------------------------------- indexing
    def _index(self):
        self.by_id = {}
        self.duplicates = []
        for item in self.items:
            rid = item.id
            if not isinstance(rid, str):
                continue
            if rid in self.by_id:
                self.duplicates.append(item)
            else:
                self.by_id[rid] = item
        self.parties = {}
        for party in self.manifest.get("parties") or []:
            if isinstance(party, dict) and isinstance(party.get("id"), str):
                self.parties[party["id"]] = party
        self.stewards = {}
        for steward in self.manifest.get("stewards") or []:
            if isinstance(steward, dict):
                self.stewards[steward.get("party")] = steward
        self.events = [i for i in self.items if i.kind == "Event"]
        self.reviews = [i for i in self.items if i.kind == "Review"]
        self.grants = [i for i in self.items if i.kind == "Grant"]
        self.proposals = [i for i in self.items if i.kind == "Proposal"]
        self.tombstones = [i for i in self.items if i.kind == "Tombstone"]
        self.content = [i for i in self.items if i.kind in CONTENT_KINDS]

    @property
    def subject_id(self):
        subject = self.manifest.get("subject") or {}
        return subject.get("id")

    @property
    def holder(self):
        return self.manifest.get("holder", "subject")

    def kind_of(self, rid):
        item = self.by_id.get(rid)
        return item.kind if item else None

    def record(self, rid):
        item = self.by_id.get(rid)
        return item.data if item else None

    def lens_doc(self, lens_id, version=None):
        """The descriptor for a lens: shipped in the package (``lenses/``), inline in a pin, or in the catalog."""
        for doc in self.pinned_lenses.values():
            if doc.get("id") == lens_id and (version is None or doc.get("version") == version):
                return doc
        for pin in self.manifest.get("lenses") or []:
            if isinstance(pin, dict) and pin.get("id") == lens_id and isinstance(pin.get("descriptor"), dict) and \
                    (version is None or pin.get("version") == version):
                return pin["descriptor"]
        return self.spec.lens(lens_id)

    def inline_lenses(self):
        """Inline local lens descriptors of a single document, as {pointer: descriptor}."""
        out = {}
        for index, pin in enumerate(self.manifest.get("lenses") or []):
            if isinstance(pin, dict) and isinstance(pin.get("descriptor"), dict):
                out["%s#/lenses/%d/descriptor" % (self.manifest_rel, index)] = pin["descriptor"]
        return out

    def playbook_doc(self, playbook_id, version=None):
        """A playbook: shipped in the package (``lenses/``), inline in a pin, or in the registry (LENSES.md §2.2)."""
        for doc in self.pinned_playbooks.values():
            if isinstance(doc, dict) and doc.get("id") == playbook_id and \
                    (version is None or doc.get("version") == version):
                return doc
        for pin in self.manifest.get("playbooks") or []:
            if isinstance(pin, dict) and pin.get("id") == playbook_id and isinstance(pin.get("playbook"), dict) and \
                    (version is None or pin.get("version") == version):
                return pin["playbook"]
        doc = self.spec.playbook(playbook_id)
        if doc is not None and (version is None or doc.get("version") == version):
            return doc
        return None

    def inline_playbooks(self):
        """Inline local playbooks of a single document, as {pointer: playbook}."""
        out = {}
        for index, pin in enumerate(self.manifest.get("playbooks") or []):
            if isinstance(pin, dict) and isinstance(pin.get("playbook"), dict):
                out["%s#/playbooks/%d/playbook" % (self.manifest_rel, index)] = pin["playbook"]
        return out

    def latest_time(self):
        """The newest knowledge time in the context; used as a deterministic "now"."""
        best = parse_time(self.manifest.get("created")) if self.manifest.get("created") else None
        for item in self.items:
            data = item.data
            for key in ("recordedAt", "at", "erasedAt"):
                value = data.get(key)
                if isinstance(value, str):
                    try:
                        moment = parse_time(value)
                    except ValueError:
                        continue
                    if best is None or moment > best:
                        best = moment
        for doc in self.projections.values():
            try:
                moment = parse_time(doc.get("generatedAt"))
            except (ValueError, TypeError):
                continue
            if moment and (best is None or moment > best):
                best = moment
        return best or datetime.datetime(2026, 1, 1, tzinfo=UTC)


# ------------------------------------------------------------ reference walking
def refs_of(kind, data):
    """Every (field_path, referenced_id) a record cites, for G1-G4, ID-3 and C3."""
    out = []

    def add(path, value):
        if isinstance(value, str):
            out.append((path, value))
        elif isinstance(value, dict) and isinstance(value.get("id"), str) and "context" in value:
            pass  # cross-context reference: never followed

    def grounds(field):
        for index, ground in enumerate(data.get(field) or []):
            if not isinstance(ground, dict):
                continue
            if "ref" in ground:
                add("/%s/%d/ref" % (field, index), ground["ref"])
            if isinstance(ground.get("span"), dict):
                add("/%s/%d/span/source" % (field, index), ground["span"].get("source"))

    grounds("grounds")
    grounds("counterEvidence")
    if kind == "Claim":
        grounds("evidence")
    for index, value in enumerate(data.get("derivedFrom") or []):
        add("/derivedFrom/%d" % index, value)
    if isinstance(data.get("supersedes"), str):
        add("/supersedes", data["supersedes"])
    if kind == "Interpretation":
        for index, value in enumerate(data.get("about") or []):
            if isinstance(value, dict) and "source" in value and "selector" in value:
                add("/about/%d/source" % index, value["source"])
            else:
                add("/about/%d" % index, value)
        if data.get("adoption"):
            add("/adoption", data["adoption"])
    if kind in ("ModelView", "Pattern", "Part") and data.get("adoption"):
        add("/adoption", data["adoption"])
    if kind == "Tension":
        for index, value in enumerate(data.get("between") or []):
            add("/between/%d" % index, value)
    if kind == "Relation":
        add("/from", data.get("from"))
        add("/to", data.get("to"))
    if kind == "Pattern":
        for index, value in enumerate(data.get("episodes") or []):
            add("/episodes/%d" % index, value)
    if kind == "ModelView":
        for index, value in enumerate(data.get("hypotheses") or []):
            add("/hypotheses/%d" % index, value)
        scope = data.get("scope") or {}
        for field in ("episodes", "sources"):
            for index, value in enumerate(scope.get(field) or []):
                add("/scope/%s/%d" % (field, index), value)
        for index, value in enumerate(data.get("alternatives") or []):
            if isinstance(value, str) and not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value):
                add("/alternatives/%d" % index, value)
    if kind == "RecallCue":
        for index, value in enumerate((data.get("offer") or {}).get("targets") or []):
            add("/offer/targets/%d" % index, value)
    if kind == "Outcome":
        about = data.get("about") or {}
        for key, value in about.items():
            add("/about/" + key, value)
        if data.get("episode"):
            add("/episode", data["episode"])
        for index, value in enumerate((data.get("delivery") or {}).get("presented") or []):
            add("/delivery/presented/%d" % index, value)
    if kind == "Episode":
        for a_index, account in enumerate(data.get("accounts") or []):
            for e_index, span in enumerate((account or {}).get("evidence") or []):
                if isinstance(span, dict):
                    add("/accounts/%d/evidence/%d/source" % (a_index, e_index), span.get("source"))
        for index, value in enumerate((data.get("externalConfirmation") or {}).get("basis") or []):
            add("/externalConfirmation/basis/%d" % index, value)
    if kind == "Source":
        custody = data.get("custody") or {}
        if custody.get("releaseRef"):
            add("/custody/releaseRef", custody["releaseRef"])
    if kind == "AssessmentRecord" and data.get("source"):
        add("/source", data["source"])
    if kind == "LensAdoption":
        practice = data.get("practice") or {}
        if practice.get("releaseRef"):
            add("/practice/releaseRef", practice["releaseRef"])
    if kind == "Claim" and isinstance(data.get("valueAddress"), dict):
        src = data["valueAddress"].get("source")
        if isinstance(src, str) and not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", src):
            add("/valueAddress/source", src)
    return out


# Fields along which C3 propagates (§8.4).
C3_FIELDS = ("about", "grounds", "counterEvidence", "evidence", "derivedFrom", "between", "episodes",
             "hypotheses", "targets", "scope")


def c3_refs(kind, data):
    out = []
    for path, rid in refs_of(kind, data):
        head = path.split("/")[1]
        if head == "offer":
            head = "targets"
        if head == "accounts":
            head = "evidence"
        if kind == "Relation" and head in ("from", "to"):
            out.append(rid)
        elif head in C3_FIELDS:
            out.append(rid)
    return out


def party_refs(kind, data):
    """Every (field_path, actor) naming a Party or actor."""
    out = []

    def add(path, value):
        if isinstance(value, str):
            out.append((path, value))

    for field in ("assertedBy", "recordedBy", "by", "grantor", "grantee", "proposer", "actor", "counterparty",
                  "suggestedBy", "assessedBy", "custodian", "erasedBy"):
        add("/" + field, data.get(field))
    if kind == "Claim":
        add("/about", data.get("about"))
    for index, value in enumerate(data.get("participants") or []):
        add("/participants/%d" % index, value)
    for index, account in enumerate(data.get("accounts") or []):
        if isinstance(account, dict):
            add("/accounts/%d/narrator" % index, account.get("narrator"))
    authorship = data.get("authorship") or {}
    if isinstance(authorship, dict):
        add("/authorship/author", authorship.get("author"))
        for index, value in enumerate(authorship.get("coAuthors") or []):
            add("/authorship/coAuthors/%d" % index, value)
    custody = data.get("custody") or {}
    if isinstance(custody, dict):
        add("/custody/custodian", custody.get("custodian"))
    summary = data.get("summary")
    if isinstance(summary, dict):
        add("/summary/authoredBy", summary.get("authoredBy"))
    for index, redaction in enumerate(data.get("redactions") or []):
        if isinstance(redaction, dict):
            add("/redactions/%d/by" % index, redaction.get("by"))
    practice = data.get("practice")
    if isinstance(practice, dict):
        add("/practice/practitioner", practice.get("practitioner"))
    for index, value in enumerate(data.get("interpretationAuthors") or []):
        add("/interpretationAuthors/%d" % index, value)
    source = data.get("source")
    if isinstance(source, dict):
        add("/source/by", source.get("by"))
    delivery = data.get("delivery")
    if isinstance(delivery, dict):
        add("/delivery/by", delivery.get("by"))
    selection = data.get("selection")
    if isinstance(selection, dict):
        add("/selection/selectedBy", selection.get("selectedBy"))
    confirmation = data.get("externalConfirmation")
    if isinstance(confirmation, dict):
        add("/externalConfirmation/by", confirmation.get("by"))
    expressed = data.get("expressedBy")
    if isinstance(expressed, dict):
        add("/expressedBy/actor", expressed.get("actor"))
    return out


def review_targets(data):
    target = data.get("target")
    if isinstance(target, list):
        return [t for t in target if isinstance(t, str)]
    if isinstance(target, str):
        return [target]
    return []


INSTRUMENT_PREFIX = "urn:ohc:instrument:"


def is_imported_result(kind, data):
    """An imported result (INSTRUMENT-IMPORT.md): an AssessmentRecord whose importedFrom.system is an instrument id."""
    if kind != "AssessmentRecord" or not isinstance(data, dict):
        return False
    system = (data.get("importedFrom") or {}).get("system") if isinstance(data.get("importedFrom"), dict) else None
    return isinstance(system, str) and system.startswith(INSTRUMENT_PREFIX)


def administered_day(data):
    """IMP-5: the first day of administeredAt (its end, else its start) at 00:00:00Z, or None."""
    when = data.get("administeredAt") if isinstance(data, dict) else None
    if not isinstance(when, dict):
        return None
    value = when.get("end") or when.get("start")
    if not isinstance(value, str) or len(value) < 4:
        return None
    day = value[:10]
    if len(day) == 4:
        day += "-01-01"
    elif len(day) == 7:
        day += "-01"
    try:
        return datetime.datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=UTC)
    except ValueError:
        return None


def lens_id_of(data):
    lens = data.get("lens")
    if isinstance(lens, dict):
        return lens.get("id")
    if isinstance(lens, str):
        return lens
    return None


# ------------------------------------------------------------------ state
class Status(object):
    """Computed status of one content record."""

    def __init__(self):
        self.admission = "active"
        self.endorsement = "not-asked"
        self.endorsed_by_subject = False
        self.contested = False
        self.locked = False
        self.epistemic = "as-reported"
        self.confirmed = []
        self.not_current = []
        self.relaxed_to = None
        self.raised_to = None
        self.audience = None
        self.add_handling = set()
        self.remove_handling = set()
        self.add_categories = set()
        self.recall = None
        self.lifecycle = None
        self.tension = "open"
        self.retracted = False
        self.declined_reason = None
        self.admitted_by = None
        self.endorsed_part = None


class State(object):
    """Effective status of a context, as known at ``at`` (§7.3, §11.1)."""

    def __init__(self, ctx, at=None):
        self.ctx = ctx
        self.spec = ctx.spec
        self.at = at
        self.items = [i for i in ctx.items if self.known(i)]
        self.by_id = {}
        for item in self.items:
            if isinstance(item.id, str) and item.id not in self.by_id:
                self.by_id[item.id] = item
        self.tombstoned = set(i.id for i in ctx.items if i.kind == "Tombstone")
        self.status = {}
        self.grant_events = {}
        self._tier_cache = {}
        self._cat_cache = {}
        self._replay()
        self._supersession()

    def known(self, item):
        if self.at is None:
            return True
        data = item.data
        stamp = data.get("recordedAt") or data.get("at")
        if item.kind == "Tombstone":
            return True  # tombstones apply retroactively (§7.3)
        if not isinstance(stamp, str):
            return True
        try:
            return parse_time(stamp) <= self.at
        except ValueError:
            return True

    # ------------------------------------------------------------- replay
    def initial(self, item):
        data = item.data
        status = Status()
        subject_asserted = data.get("assertedBy") == "subject"
        status.admission = "active" if subject_asserted else "proposed"
        if item.kind == "LensAdoption" and data.get("route") in ("agent-suggested", "imported"):
            status.admission = "proposed"
        if item.kind == "Practice" and (data.get("source") or {}).get("route") == "from-agent":
            status.admission = "proposed"
        if item.kind == "AssessmentRecord" and self._imported_adoption_run(data):
            status.admission = "proposed"
        status.endorsement = "endorsed" if subject_asserted else "not-asked"
        status.endorsed_by_subject = subject_asserted
        origin_codes = {c["code"]: c for c in self.spec.catalogs["origin"]["codes"]}
        default_epistemic = (origin_codes.get(data.get("origin")) or {}).get("defaultEpistemic", "as-reported")
        status.epistemic = data.get("epistemic") or default_epistemic
        if item.kind in INTERPRETATION_LAYER and not subject_asserted and not data.get("epistemic"):
            status.epistemic = "hypothesis"
        if self._frame_relative(data):
            status.epistemic = "frame-relative"
        if item.kind == "Practice":
            status.lifecycle = data.get("initialStatus", "candidate")
        elif item.kind in ("LensAdoption", "RecallCue"):
            status.lifecycle = "active"
            if item.kind == "LensAdoption":
                practice = data.get("practice") or {}
                if practice.get("relationship") == "ended" and data.get("onEnd", "ask") == "ask":
                    status.lifecycle = "paused"
        return status

    def _imported_adoption_run(self, data):
        run = (data.get("importedFrom") or {}).get("run")
        if not run:
            return False
        for item in self.ctx.items:
            if item.kind == "LensAdoption" and item.data.get("route") == "imported" and \
                    (item.data.get("importedFrom") or {}).get("run") == run:
                return True
        return False

    def frame_relative(self, data):
        """AR-4 / LA-6: results of a symbolic-frame or T5 lens, or of a lens with no descriptor."""
        return self._frame_relative(data)

    def _frame_relative(self, data):
        lens_id = lens_id_of(data)
        if not lens_id:
            return False
        doc = self.ctx.lens_doc(lens_id)
        if not doc:
            return True  # no resolvable descriptor: treated as a stub, results are frame-relative (LA-6)
        evidence = doc.get("evidence") or {}
        return evidence.get("measurementTier") == "T5" or evidence.get("ontologicalStatus") == "symbolic-frame"

    def actor_class(self, actor, target_data=None):
        """Classify an actor: subject, holder, steward, asserter or party."""
        if actor == "subject":
            return "subject"
        if actor == "holder":
            return "holder"
        return "party"

    def review_allowed(self, review, target_item):
        """§11.1 allowed actors, steward scope and R-A1 (also used by checker rule RV-2)."""
        action = review.get("action")
        info = self.spec.review_actions.get(action)
        if info is None or target_item is None:
            return False
        by = review.get("by")
        allowed = info.get("allowedActors", [])
        target = target_item.data
        if by == "subject":
            return "subject" in allowed
        if by == "holder":
            if "holder" not in allowed:
                return False
            if action == "admit":
                return self.holder_may_admit(target_item)
            if action == "decline":
                return True  # protective: the holder may always decline a proposed record (§11.1, IB-4, IB-5)
            if action == "resolve":
                return target.get("whoDecides") == "holder-policy"
            return True
        if "asserter" in allowed and by == target.get("assertedBy"):
            return True
        steward = self.ctx.stewards.get(by)
        if steward and "steward" in allowed:
            return self.steward_in_scope(steward, review, target_item)
        return False

    def holder_may_admit(self, target_item):
        policy = (self.ctx.manifest.get("policy") or {}).get("admission", "subject-only")
        if policy != "holder-may-admit-ordinary":
            return False
        if self.subject_only_admission(target_item):
            return False
        return self.tier(target_item.id) in ("ordinary", "personal")

    def subject_only_admission(self, target_item):
        """R-A1: records that only the subject in person may admit."""
        data = target_item.data
        kind = target_item.kind
        if kind in ("Part", "RecallCue"):
            return True
        if kind in ("Interpretation", "Pattern", "ModelView") and data.get("origin") == "inferred":
            return True
        if kind == "AssessmentRecord" and data.get("mode") in ("agent-inference", "cross-lens-estimate"):
            return True
        return self.tier(target_item.id) == "special"

    def steward_in_scope(self, steward, review, target_item):
        scope = steward.get("scope") or {}
        if review.get("action") not in (scope.get("actions") or []):
            return False
        if scope.get("kinds") and target_item.kind not in scope["kinds"]:
            return False
        if scope.get("facets") and target_item.data.get("facet") not in scope["facets"]:
            return False
        if target_item.kind == "Part" or self.tier(target_item.id) == "special":
            return False
        at = parse_time(review.get("recordedAt"))
        start = parse_time(steward.get("validFrom"))
        end = parse_time(steward.get("validUntil"))
        if at is None or start is None or end is None or not (start <= at < end):
            return False
        return True

    def _replay(self):
        for item in self.items:
            if item.kind in CONTENT_KINDS:
                self.status[item.id] = self.initial(item)
        reviews = [i for i in self.items if i.kind == "Review"]
        reviews.sort(key=lambda i: (parse_time(i.data.get("recordedAt")) or datetime.datetime.min.replace(tzinfo=UTC), i.order))
        self.grant_reviews = {}
        for review_item in reviews:
            review = review_item.data
            for target in review_targets(review):
                target_item = self.by_id.get(target)
                if target_item is None or target in self.tombstoned:
                    continue
                if target_item.kind == "Grant":
                    if self.grant_review_allowed(review, target_item):
                        self.grant_reviews.setdefault(target, []).append(review)
                    continue
                status = self.status.get(target)
                if status is None:
                    continue
                if not self.review_allowed(review, target_item):
                    continue
                self.apply(status, review, target_item)
        self._expire_proposals()
        self._auto_pause()

    def _auto_pause(self):
        """RC-3: a RecallCue is computed paused after 3 consecutive Outcomes about it with result ``no-effect`` or
        ``worse``, or after one with response ``asked-to-stop``; only a subject ``resume`` reactivates it."""
        for cue in [i for i in self.items if i.kind == "RecallCue"]:
            status = self.status.get(cue.id)
            if status is None:
                continue
            timeline = []
            for item in self.items:
                if item.kind == "Outcome" and (item.data.get("about") or {}).get("recallCue") == cue.id:
                    timeline.append((parse_time(item.data.get("recordedAt")), 1, item.order, "outcome", item.data))
                elif item.kind == "Review" and cue.id in review_targets(item.data) and \
                        item.data.get("action") == "resume" and item.data.get("by") == "subject":
                    timeline.append((parse_time(item.data.get("recordedAt")), 0, item.order, "resume", item.data))
            timeline.sort(key=lambda t: (t[0], t[1], t[2]))
            streak, paused = 0, False
            for _at, _rank, _order, what, data in timeline:
                if what == "resume":
                    streak, paused = 0, False
                    continue
                if (data.get("delivery") or {}).get("response") == "asked-to-stop":
                    paused = True
                elif data.get("result") in ("no-effect", "worse"):
                    streak += 1
                    if streak >= 3:
                        paused = True
                else:
                    streak = 0
            if paused and status.lifecycle != "retired":
                status.lifecycle = "paused"

    def grant_review_allowed(self, review, grant_item):
        action = review.get("action")
        by = review.get("by")
        if action == "withdraw-grant":
            if by == "subject":
                return True
            steward = self.ctx.stewards.get(by)
            return bool(steward) and grant_item.data.get("grantor") == by
        if action == "revoke-grant":
            return by == "holder"
        return False

    def apply(self, status, review, target_item):
        action = review.get("action")
        at = parse_time(review.get("recordedAt"))
        by = review.get("by")
        if status.retracted:
            return
        if action in ("endorse", "partially-endorse", "contest"):
            if action == "endorse":
                status.endorsement = "endorsed"
                status.endorsed_by_subject = by == "subject"
            elif action == "partially-endorse":
                status.endorsement = "partial"
                status.endorsed_by_subject = by == "subject"
                status.endorsed_part = review.get("endorsedPart")  # PJ-8: the latest one's words
            else:
                status.contested = True
            if status.admission == "proposed":
                status.admission = "active"
                status.admitted_by = by
        elif action == "reject":
            status.endorsement = "rejected"
            status.endorsed_by_subject = False
            if status.admission == "proposed":
                status.admission = "declined"
        elif action in ("withdraw-contest", "resolve-contest"):
            status.contested = False
        elif action == "lock":
            status.locked = True
        elif action == "unlock":
            status.locked = False
        elif action == "confirm-current":
            status.confirmed.append(at)
        elif action == "mark-not-current":
            status.not_current.append(at)
        elif action == "admit":
            status.admission = "active"
            status.admitted_by = by
            status.declined_reason = None
        elif action == "decline":
            status.admission = "declined"
        elif action == "retract":
            status.admission = "retracted"
            status.retracted = True
        elif action == "reassess":
            if review.get("epistemic"):
                status.epistemic = review["epistemic"]
        elif action in ("restrict", "relax"):
            disclosure = review.get("disclosure") or {}
            if action == "relax":
                if disclosure.get("sensitivity"):
                    status.relaxed_to = disclosure["sensitivity"]
                    status.raised_to = None
                for code in disclosure.get("removeHandling") or []:
                    status.remove_handling.add(code)
                    status.add_handling.discard(code)
                status.audience = "grantees" if disclosure.get("audience") in (None, "grantees") else status.audience
            else:
                if disclosure.get("sensitivity"):
                    status.raised_to = vocab.max_tier(status.raised_to, disclosure["sensitivity"])
                for code in disclosure.get("addHandling") or []:
                    status.add_handling.add(code)
                    status.remove_handling.discard(code)
                for code in disclosure.get("addCategories") or []:
                    status.add_categories.add(code)
                if disclosure.get("audience"):
                    status.audience = disclosure["audience"]
            if disclosure.get("recall"):
                status.recall = disclosure["recall"]
        elif action in ("pause", "resume", "retire"):
            status.lifecycle = {"pause": "paused", "resume": "in-use" if target_item.kind == "Practice" else "active",
                                "retire": "retired"}[action]
        elif action in ("acknowledge", "explore", "hold-as-is", "resolve"):
            status.tension = {"acknowledge": "acknowledged", "explore": "exploring", "hold-as-is": "held-as-is",
                              "resolve": "resolved"}[action]
        if target_item.kind == "Practice" and action == "reject":
            status.lifecycle = "not-for-me"

    def _expire_proposals(self):
        now = self.at
        for item in self.items:
            if item.kind != "Proposal":
                continue
            data = item.data
            expires = parse_time(data.get("expiresAt")) if data.get("expiresAt") else None
            if expires is None:
                recorded = parse_time(data.get("recordedAt"))
                expires = recorded + datetime.timedelta(days=30) if recorded else None
            if expires is None or now is None or now < expires:
                continue
            for rid in data.get("items") or []:
                status = self.status.get(rid)
                if status is not None and status.admission == "proposed":
                    status.admission = "declined"
                    status.declined_reason = "expired"

    def _supersession(self):
        self.successor = {}
        for item in self.items:
            target = item.data.get("supersedes") if item.kind in CONTENT_KINDS else None
            if isinstance(target, str):
                status = self.status.get(item.id)
                if status is not None and status.admission == "active":
                    self.successor.setdefault(target, item.id)

    def superseded(self, rid):
        return rid in self.successor

    # -------------------------------------------------------------- disclosure
    def kind_default_tier(self, item):
        data = item.data
        kind = item.kind
        base = self.spec.default_tier(kind)
        defaults = self.spec.kind_defaults.get(kind) or {}
        facet = data.get("facet")
        if kind == "Claim":
            base = (defaults.get("facetDefaults") or {}).get(facet, base or "personal")
            if facet == "belief":
                base = "special"
            if facet == "state" and data.get("predicate") in EMOTION_PREDICATES:
                base = "special"
        elif kind == "Source":
            base = vocab.max_tier(base, self.spec.source_kind_tier.get(data.get("sourceKind")) or "sensitive")
            custody = data.get("custody") or {}
            if custody.get("confidentiality", "none") != "none":
                base = "special"
            elif data.get("containsThirdParty"):
                base = vocab.max_tier(base, "sensitive")
        elif kind == "Interpretation":
            if lens_id_of(data):
                base = "special"
            for ref in data.get("about") or []:
                if isinstance(ref, str) and self.kind_of(ref) == "Part":
                    base = "special"
            adoption = self.record(data.get("adoption"))
            if adoption and adoption.get("confidentiality", "none") != "none":
                base = "special"
        elif kind == "Pattern":
            if lens_id_of(data):
                base = "special"
        elif kind == "LensAdoption":
            if data.get("route") == "inherited-from-practice" or data.get("confidentiality", "none") != "none":
                base = "special"
        return base

    def kind_of(self, rid):
        item = self.ctx.by_id.get(rid)
        return item.kind if item else None

    def record(self, rid):
        if not isinstance(rid, str):
            return None
        item = self.ctx.by_id.get(rid)
        return item.data if item else None

    def lens_default(self, data):
        lens_id = lens_id_of(data)
        if not lens_id:
            return None, []
        doc = self.ctx.lens_doc(lens_id)
        if not doc:
            return None, []
        defaults = doc.get("defaults") or {}
        return defaults.get("sensitivity"), list(defaults.get("categories") or [])

    def categories(self, rid, _stack=None):
        """Effective categories: own + added + lens defaults + union along C3 edges."""
        if rid in self._cat_cache:
            return self._cat_cache[rid]
        item = self.ctx.by_id.get(rid)
        if item is None or item.kind not in CONTENT_KINDS:
            return set()
        stack = _stack or set()
        if rid in stack:
            return set()
        stack = stack | {rid}
        data = item.data
        cats = set(data.get("categories") or [])
        status = self.status.get(rid)
        if status:
            cats |= status.add_categories
        if item.kind == "Source" and data.get("containsThirdParty"):
            cats.add("third-party")
        _tier, lens_cats = self.lens_default(data)
        cats |= set(lens_cats)
        for ref in c3_refs(item.kind, data):
            cats |= self.categories(ref, stack)
        self._cat_cache[rid] = cats
        return cats

    def tier(self, rid, _stack=None):
        """Effective sensitivity tier by C3 (§8.4), with restrict and relax Reviews applied."""
        if rid in self._tier_cache:
            return self._tier_cache[rid]
        item = self.ctx.by_id.get(rid)
        if item is None or item.kind not in CONTENT_KINDS:
            return None
        stack = _stack or set()
        if rid in stack:
            return item.data.get("sensitivity") or self.kind_default_tier(item) or "personal"
        stack = stack | {rid}
        data = item.data
        tiers = [data.get("sensitivity"), self.kind_default_tier(item)]
        for category in self.categories(rid):
            tiers.append(self.spec.categories_min.get(category, "personal"))
        lens_tier, _cats = self.lens_default(data)
        tiers.append(lens_tier)
        adoption = self.record(data.get("adoption"))
        if adoption and adoption.get("confidentiality") == "therapy-confidential":
            tiers.append("special")
        if item.kind == "LensAdoption" and data.get("confidentiality") == "therapy-confidential":
            tiers.append("special")
        for ref in c3_refs(item.kind, data):
            tiers.append(self.tier(ref, stack))
        computed = vocab.max_tier(*tiers) or "personal"
        status = self.status.get(rid)
        if status is not None and status.relaxed_to:
            computed = status.relaxed_to
        if status is not None and status.raised_to:
            computed = vocab.max_tier(computed, status.raised_to)
        self._tier_cache[rid] = computed
        return computed

    def stored_tier_or_default(self, item):
        """The tier before propagation (for ENV-5)."""
        return vocab.max_tier(item.data.get("sensitivity"), self.kind_default_tier(item)) or "personal"

    def handling(self, rid):
        item = self.ctx.by_id.get(rid)
        if item is None:
            return set()
        data = item.data
        codes = set(data.get("handling") or [])
        if item.kind == "Part" and "handling" not in data:
            codes.add("person-only")
        adoption = self.record(data.get("adoption"))
        if adoption and adoption.get("confidentiality") == "therapy-confidential":
            codes.add("person-only")
        if item.kind == "LensAdoption" and data.get("confidentiality") == "therapy-confidential":
            codes.add("person-only")
        status = self.status.get(rid)
        if status:
            codes |= status.add_handling
            codes -= status.remove_handling
        return codes

    def audience(self, rid):
        item = self.ctx.by_id.get(rid)
        status = self.status.get(rid)
        if status is not None and status.audience:
            return status.audience
        if item is not None and item.data.get("audience"):
            return item.data["audience"]
        return "named" if self.tier(rid) in ("sensitive", "special") else "grantees"

    def recall(self, rid):
        item = self.ctx.by_id.get(rid)
        status = self.status.get(rid)
        if status is not None and status.recall:
            return status.recall
        if item is not None:
            return item.data.get("recall", "not-permitted")
        return "not-permitted"

    # -------------------------------------------------------------- freshness
    def freshness(self, rid, now):
        return self.freshness_detail(rid, now)[0]

    def stale_since(self, rid, now):
        """When a stale record became stale (review due, expiry or not-current mark); None otherwise."""
        return self.freshness_detail(rid, now)[1]

    def freshness_detail(self, rid, now):
        """§7.2: (freshness, since) where ``since`` is the moment it became review-due or expired."""
        item = self.ctx.by_id.get(rid)
        if item is None:
            return "not-applicable", None
        if item.kind in HISTORICAL_KINDS:
            return "historical", None
        if item.kind not in FRESHNESS_KINDS:
            return "not-applicable", None
        data = item.data
        status = self.status.get(rid) or Status()
        last_confirmed = max(status.confirmed) if status.confirmed else None
        if status.not_current and (last_confirmed is None or max(status.not_current) > last_confirmed):
            return "expired", max(status.not_current)
        if data.get("valueAddress"):
            return "unknown", None
        valid = data.get("valid") or {}
        if valid.get("until") and now >= parse_time(valid["until"]):
            return "expired", parse_time(valid["until"])
        if valid.get("until") and not data.get("reviewAfter") and data.get("horizon") == "state":
            return "current", None  # §7.2 step 4: valid.until replaces the state interval
        anchors = [parse_time(data.get("recordedAt"))]
        if is_imported_result(item.kind, data) and administered_day(data) is not None:
            anchors = [administered_day(data)]  # IMP-5: an imported result is anchored at administeredAt
        if last_confirmed:
            anchors.append(last_confirmed)
        if data.get("lastEvidenceAt"):
            anchors.append(parse_time(data["lastEvidenceAt"]))
        anchor = max(a for a in anchors if a is not None)
        review_after = data.get("reviewAfter")
        if item.kind == "AssessmentRecord" and not review_after:
            doc = self.ctx.lens_doc(lens_id_of(data)) if lens_id_of(data) else None
            review_after = ((doc or {}).get("defaults") or {}).get("reviewAfter")
        if review_after == "on-change":
            return "current", None
        if review_after:
            if parse_duration(review_after) is not None:
                due = add_duration(anchor, review_after)
            else:
                try:
                    due = parse_time(review_after)
                except ValueError:
                    due = None
            if due is None:
                return "unknown", None
            return ("review-due", due) if now >= due else ("current", None)
        horizon = data.get("horizon") or "none"
        interval = self.spec.default_intervals.get(horizon, "P1Y")
        due = add_duration(anchor, interval)
        return ("review-due", due) if now >= due else ("current", None)

    # ----------------------------------------------------------- held during
    def held_from(self, rid):
        data = self.record(rid) or {}
        held = data.get("heldDuring") or {}
        return parse_time(held.get("from") or data.get("formulatedAt") or data.get("recordedAt"))

    def held_until(self, rid):
        """I7: stored until; else successor's from; else mark-not-current; else open (None)."""
        data = self.record(rid) or {}
        held = data.get("heldDuring") or {}
        if held.get("until"):
            return parse_time(held["until"])
        successor = self.successor.get(rid)
        if successor:
            return self.held_from(successor)
        status = self.status.get(rid)
        if status and status.not_current:
            return max(status.not_current)
        return None

    def held_now(self, rid, now):
        until = self.held_until(rid)
        return until is None or until > now

    # ------------------------------------------------------------------ labels
    def label(self, rid, now):
        """§6.6: the first matching rule wins."""
        item = self.ctx.by_id.get(rid)
        data = item.data if item else {}
        status = self.status.get(rid) or Status()
        if status.admission in ("declined", "retracted"):
            return "not-accepted"
        if status.endorsement == "rejected" or status.contested:
            return "disputed"
        if self.freshness(rid, now) in ("review-due", "expired", "unknown"):
            return "stale"
        if status.admission == "proposed":
            return "pending"
        if status.epistemic == "frame-relative":
            return "frame"
        if data.get("origin") == "declared" and data.get("assertedBy") == "subject":
            return "stated"
        if status.endorsement == "endorsed":
            return "confirmed"
        if status.endorsement == "partial":
            return "partly-confirmed"
        if data.get("origin") == "attested":
            return "attested"
        if data.get("origin") in ("observed", "derived") and status.endorsement == "not-asked":
            return "observed"
        return "hypothesis"

    def derived(self, rid, now):
        status = self.status.get(rid) or Status()
        entry = {
            "label": self.label(rid, now),
            "freshness": self.freshness(rid, now),
            "endorsement": status.endorsement,
            "contested": bool(status.contested),
            "locked": bool(status.locked),
            "admission": status.admission,
        }
        if self.kind_of(rid) == "Interpretation":
            entry["heldNow"] = self.held_now(rid, now)
        if status.endorsement == "partial" and status.endorsed_part:
            entry["endorsedPart"] = status.endorsed_part  # PJ-8
        entry["computedAt"] = format_time(now)
        return entry

    # ---------------------------------------------------------------- grants
    def grant_status(self, gid, now):
        """§12.1 computed status at ``now``: given, withdrawn, revoked, expired, invalidated (None if unknown)."""
        item = self.ctx.by_id.get(gid)
        if item is None or item.kind != "Grant":
            return None
        data = item.data
        recorded = parse_time(data.get("recordedAt"))
        if recorded is None or now < recorded:
            return None
        for review in self.grant_reviews.get(gid, []):
            at = parse_time(review.get("recordedAt"))
            if at is not None and at <= now:
                return "withdrawn" if review.get("action") == "withdraw-grant" else "revoked"
        constraints = data.get("constraints") or {}
        expires = parse_time(constraints.get("expiresAt")) if constraints.get("expiresAt") else None
        if expires is not None and now >= expires:
            return "expired"
        for other in self.ctx.grants:
            # A renewal replaces the grant it renews from the moment it is given (§12.1), so a narrower renewal is
            # never undercut by the broader grant it replaced.
            if other.id != gid and other.data.get("renews") == gid and \
                    other.data.get("grantee") == data.get("grantee"):
                given = parse_time(other.data.get("recordedAt"))
                if given is not None and given <= now:
                    return "expired"
        max_uses = constraints.get("maxUses")
        if isinstance(max_uses, int):
            used = 0
            for event in self.ctx.events:
                ev = event.data
                if ev.get("grant") == gid and ev.get("eventType") in ("projection-served", "answer-served"):
                    at = parse_time(ev.get("at"))
                    if at is not None and at < now:
                        used += 1
            if used >= max_uses:
                return "expired"
        grantor = data.get("grantor")
        if grantor not in ("subject", None):
            steward = self.ctx.stewards.get(grantor)
            if not steward or "grant" not in ((steward.get("scope") or {}).get("actions") or []):
                return "invalidated"
            end = parse_time(steward.get("validUntil"))
            if end is not None and now >= end:
                return "invalidated"
        if data.get("grantee") not in self.ctx.parties:
            return "invalidated"
        return "given"


def content_items(ctx):
    return [i for i in ctx.items if i.kind in CONTENT_KINDS]
