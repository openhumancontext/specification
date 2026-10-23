"""Writing packages (§3.3) for the reference converters.

``Package`` opens an existing package directory (or starts a new one), keeps the
existing JSON Lines exactly as they are, appends new records as RFC 8785 lines,
orders each collection by ``recordedAt`` then ``id`` (§3.3), extends the Event
chain (§13.2) and rewrites the lock. Nothing is ever deleted.
"""

import copy
import hashlib
import hmac
import json
import os
import re
import shutil

from . import events as ev
from . import jcs, jsonio, model

LOCK_EXCLUDED_NAMES = ("README.md", "expected-check.json")


def lock_document(directory, manifest, created_at):
    files = {}
    for base, dirs, names in os.walk(directory):
        dirs.sort()
        for name in sorted(names):
            rel = os.path.relpath(os.path.join(base, name), directory).replace(os.sep, "/")
            if rel == "context.lock.json" or rel.startswith("vault/") or rel.startswith("ext/"):
                continue
            if name in LOCK_EXCLUDED_NAMES:
                continue
            with open(os.path.join(base, name), "rb") as handle:
                files[rel] = "sha256:" + hashlib.sha256(handle.read()).hexdigest()
    return {"format": "ohc.lock", "specVersion": manifest.get("specVersion", "0.1.0-draft"),
            "context": {"id": manifest.get("id"), "version": manifest.get("version")},
            "algorithm": "sha256", "files": dict(sorted(files.items())), "createdAt": created_at}


def _sort_key(record):
    return (model.parse_time(record.get("recordedAt") or record.get("erasedAt") or "") or model.parse_time("1970-01-01"),
            record.get("id") or "")


def next_numbered_id(existing_ids, prefix, width=2):
    """Next ``<prefix><n>`` after the highest numbered id with that prefix (e.g. rv-09 after rv-08)."""
    pattern = re.compile("^" + re.escape(prefix) + r"(\d+)$")
    top = 0
    for rid in existing_ids:
        match = pattern.match(rid or "")
        if match:
            top = max(top, int(match.group(1)))
    return "%s%0*d" % (prefix, width, top + 1)


OPAQUE_ALPHABET = "23456789abcdefghjkmnpqrstvwxyz"


def opaque_id(existing_ids, prefix, seed=None):
    """A new ``<prefix><4 characters>`` id that says nothing about other records: no sequence, so a projection that
    leaves a record out shows no gap (Annex B, "No existence oracles"). With ``seed`` (synthetic
    contexts only: examples and tests) the ids are reproducible; otherwise they are random."""
    taken = set(existing_ids)
    width, attempt = 4, 0
    while True:
        attempt += 1
        if seed:
            raw = hmac.new(seed.encode("utf-8"), ("%s%d" % (prefix, attempt)).encode("utf-8"),
                           hashlib.sha256).digest()
        else:
            raw = os.urandom(8)
        token = "".join(OPAQUE_ALPHABET[b % len(OPAQUE_ALPHABET)] for b in raw[:width])
        if prefix + token not in taken:
            return prefix + token
        if attempt % 64 == 0:
            width += 1


class Package(object):
    def __init__(self, directory, spec, previous=None):
        """Open ``directory``; when ``previous`` is given and differs, copy it there first."""
        self.dir = directory
        self.spec = spec
        if previous and os.path.abspath(previous) != os.path.abspath(directory):
            if os.path.exists(directory):
                shutil.rmtree(directory)
            shutil.copytree(previous, directory)
        self.manifest = None
        self.lines = {}      # collection -> list of (record, raw line or None)
        self.events = []
        self.dirty = set()
        # a folder made private at setup stays so: its new vault files are 0600 too
        self.private = os.path.isdir(directory) and (os.stat(directory).st_mode & 0o077) == 0
        self.kept_keys = {}  # id -> sort key of a record replaced in place (a Tombstone keeps its position)
        self.seed = None     # reproducible Event salts, for synthetic contexts only (examples and tests)
        self.opaque = False  # the person's window issues opaque record ids (new_id); converters keep numbers
        manifest_path = os.path.join(directory, "context.json")
        if os.path.isfile(manifest_path):
            self.manifest = jsonio.load_json(manifest_path)
            for collection, rel in (self.manifest.get("collections") or {}).items():
                full = os.path.join(directory, rel)
                if collection == "events":
                    if os.path.isfile(full):
                        self.events = [obj for _n, obj in jsonio.load_jsonl(full)]
                    continue
                entries = []
                if os.path.isfile(full):
                    with open(full, "r", encoding="utf-8") as handle:
                        for line in handle.read().split("\n"):
                            if line:
                                entries.append((json.loads(line), line))
                self.lines[collection] = entries

    # ----------------------------------------------------------------- state
    def exists(self):
        return self.manifest is not None

    def create(self, manifest, private=False):
        """Start a new package. ``private``: the folder is readable by the person's user account only (0700, its
        vault files 0600); an agent that runs as that user can still read it, so a holder keeps it out of reach."""
        self.manifest = copy.deepcopy(manifest)
        self.manifest.setdefault("collections", {})
        self.private = private
        self.dirty.add("context.json")

    def records(self, collection=None):
        out = []
        for name, entries in self.lines.items():
            if collection is None or name == collection:
                out.extend(record for record, _raw in entries)
        return out

    def ids(self):
        out = set(r.get("id") for r in self.records())
        out.update(e.get("id") for e in self.events)
        return out

    def new_id(self, prefix):
        """A new record id: opaque in the person's window (``opaque``), numbered otherwise. Reviews stay numbered:
        they are never served, and Reviews made at the same instant replay in id order (§3.3, §11.1)."""
        if self.opaque and prefix != "rv-":
            return opaque_id(self.ids(), prefix, self.seed)
        return next_numbered_id(self.ids(), prefix)

    def record(self, rid):
        for record in self.records():
            if record.get("id") == rid:
                return record
        return None

    def party_ids(self):
        return [p.get("id") for p in self.manifest.get("parties") or []]

    def ensure_party(self, party):
        if party["id"] not in self.party_ids():
            self.manifest.setdefault("parties", []).append(party)
            self.dirty.add("context.json")

    def ensure_module(self, module):
        conformance = self.manifest.setdefault("conformance", {"level": "L2", "modules": ["core"]})
        modules = conformance.setdefault("modules", ["core"])
        if module not in modules:
            modules.append(module)
            self.dirty.add("context.json")

    def add(self, kind, record):
        """Append a record of ``kind`` to its collection (JCS line)."""
        collection = self.spec.kind_collection[kind]
        rel = self.spec.kind_file[kind]
        collections = self.manifest.setdefault("collections", {})
        if collection not in collections:
            collections[collection] = rel
            self.dirty.add("context.json")
        self.lines.setdefault(collection, []).append((record, None))
        self.dirty.add(collection)
        return record

    def replace(self, rid, record):
        """Replace the record ``rid`` in its collection, in place (a Tombstone keeps its position, §14.3)."""
        for collection, entries in self.lines.items():
            for index, (old, _raw) in enumerate(entries):
                if old.get("id") == rid:
                    self.kept_keys[rid] = _sort_key(old)
                    entries[index] = (record, None)
                    self.dirty.add(collection)
                    return old
        return None

    def remove_vault(self, rel):
        """Delete a vault object (erasure, §15.5). Only paths under ``vault/`` are touched."""
        if not rel.startswith("vault/") or ".." in rel.split("/"):
            return False
        full = os.path.join(self.dir, rel)
        if os.path.isfile(full):
            os.remove(full)
            return True
        return False

    def pin(self, member, doc):
        """Pin a registry document in the package: ``lenses/<name>@<version>.<lens|playbook>.json`` and a
        ``{id, version, sha256}`` entry in the manifest's ``lenses`` or ``playbooks`` (§9.1, LENSES.md §2.2)."""
        suffix = {"lenses": "lens", "playbooks": "playbook"}[member]
        name = doc["id"].rsplit(":", 1)[-1]
        rel = "lenses/%s@%s.%s.json" % (name, doc["version"], suffix)
        text = jsonio.dumps_pretty(doc).encode("utf-8")
        full = os.path.join(self.dir, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as handle:
            handle.write(text)
        entry = {"id": doc["id"], "version": doc["version"], "sha256": hashlib.sha256(text).hexdigest()}
        pins = [p for p in self.manifest.get(member) or []
                if not (isinstance(p, dict) and p.get("id") == doc["id"] and p.get("version") == doc["version"])]
        pins.append(entry)
        self.manifest[member] = pins
        self.dirty.add("context.json")
        return rel

    def store_vault(self, data, extension):
        digest = hashlib.sha256(data).hexdigest()
        rel = "vault/%s/%s.%s" % (digest[:2], digest, extension)
        full = os.path.join(self.dir, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as handle:
            handle.write(data)
        if self.private:
            os.chmod(full, 0o600)
        return rel, digest

    def next_event_id(self):
        return "e-%04d" % (len(self.events) + 1)

    def append_event(self, fields, seed=None):
        collections = self.manifest.setdefault("collections", {})
        if "events" not in collections:
            collections["events"] = "events.jsonl"
            self.dirty.add("context.json")
        event = ev.next_event(self.events, fields, seed=seed if seed is not None else self.seed)
        self.events.append(event)
        self.dirty.add("events")
        return event

    def bump_version(self, at):
        day = at[:10]
        version = self.manifest.get("version") or ""
        match = re.match(r"^(\d{4}-\d{2}-\d{2})\.(\d+)$", version)
        if match and match.group(1) == day:
            self.manifest["version"] = "%s.%d" % (day, int(match.group(2)) + 1)
        else:
            self.manifest["version"] = day + ".1"
        self.dirty.add("context.json")

    # ------------------------------------------------------------------ save
    def save(self, created_at, lock=True):
        os.makedirs(self.dir, exist_ok=True)
        if self.private:
            os.chmod(self.dir, 0o700)
        collections = self.manifest.get("collections") or {}
        for collection in sorted(self.dirty):
            if collection in ("context.json", "events"):
                continue
            rel = collections[collection]
            entries = sorted(self.lines[collection],
                             key=lambda e: self.kept_keys.get(e[0].get("id")) or _sort_key(e[0]))
            full = os.path.join(self.dir, rel)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8", newline="\n") as handle:
                for record, raw in entries:
                    handle.write((raw if raw is not None else jcs.canonicalize(record)) + "\n")
        if "events" in self.dirty:
            jsonio.write_jsonl(os.path.join(self.dir, collections.get("events", "events.jsonl")), self.events)
        jsonio.write_pretty(os.path.join(self.dir, "context.json"), self.manifest)
        if lock:
            jsonio.write_pretty(os.path.join(self.dir, "context.lock.json"),
                                lock_document(self.dir, self.manifest, created_at))
        self.dirty = set()
