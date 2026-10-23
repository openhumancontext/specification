"""The Event log: a salted hash chain that survives erasure (§13.1, §13.2).

    entryDigest(e) = "sha256:" + hex(sha256(JCS(e minus {"entryDigest", "redacted"})))
    e[1].prev      = "sha256:" + "0" * 64
    e[n].prev      = entryDigest(e[n-1])

A redacted stub keeps ``id``, ``seq``, ``at``, ``prev`` and the original
``entryDigest`` with ``eventType: "redacted"`` and ``redacted: true``; verification
uses the stored digest. A ``chain-resealed`` Event starts a new segment.
"""

import base64
import hashlib
import hmac
import os

from . import jcs

ZERO = "sha256:" + "0" * 64


def entry_digest(event):
    body = dict((k, v) for k, v in event.items() if k not in ("entryDigest", "redacted"))
    return jcs.digest(body)


def stored_or_computed_digest(event):
    if event.get("redacted") is True and isinstance(event.get("entryDigest"), str):
        return event["entryDigest"]
    return entry_digest(event)


def verify_chain(events):
    """Check EV-1 (contiguous seq) and EV-2 (chain). Returns ``[(rule, index)]``."""
    problems = []
    previous = None
    for index, event in enumerate(events):
        expected_seq = index + 1
        if event.get("seq") != expected_seq:
            problems.append(("EV-1", index))
        if previous is None:
            if event.get("prev") != ZERO:
                problems.append(("EV-2", index))
        else:
            if event.get("prev") != previous:
                resealed = event.get("eventType") == "chain-resealed" and event.get("prev") == ZERO
                if not resealed:
                    problems.append(("EV-2", index))
        previous = stored_or_computed_digest(event)
    return problems


def make_stub(event):
    """Replace an Event by its redacted stub (§13.2)."""
    return {
        "id": event["id"],
        "seq": event["seq"],
        "at": event["at"],
        "eventType": "redacted",
        "prev": event["prev"],
        "entryDigest": entry_digest(event),
        "redacted": True,
    }


def new_salt(seed=None, label=""):
    """16 bytes, base64url without padding. A ``seed`` makes salts reproducible (examples and tests only)."""
    if seed is None:
        raw = os.urandom(16)
    else:
        raw = hmac.new(seed if isinstance(seed, bytes) else seed.encode("utf-8"),
                       ("salt|" + label).encode("utf-8"), hashlib.sha256).digest()[:16]
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def next_event(events, fields, salt=None, seed=None, id_width=4):
    """Build the next Event after ``events`` with ``fields`` (eventType, at, actor, ...)."""
    seq = len(events) + 1
    prev = stored_or_computed_digest(events[-1]) if events else ZERO
    event = {"id": "e-%0*d" % (id_width, seq), "seq": seq}
    event.update(fields)
    event["salt"] = salt or new_salt(seed, "%d|%s" % (seq, fields.get("eventType", "")))
    event["prev"] = prev
    ordered = {}
    for key in ("kind", "id", "seq", "at", "eventType", "actor", "counterparty", "grant", "purpose", "records",
                "message", "outcome", "reason", "tier", "confirmationDigest", "salt", "prev"):
        if key in event:
            ordered[key] = event[key]
    for key, value in event.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def confirmation_digest(request, grant, purpose, targets, why, expires_at, confirmed_by, at, nonce):
    """SU-5: covers request parameters only, never content."""
    return jcs.digest({
        "request": request, "grant": grant, "purpose": purpose, "targets": targets, "why": why,
        "expiresAt": expires_at, "confirmedBy": confirmed_by, "at": at, "nonce": nonce,
    })


def content_digest_fields():
    """Event members that may never carry content digests (G3); only these digests are allowed."""
    return ("prev", "entryDigest", "confirmationDigest")
