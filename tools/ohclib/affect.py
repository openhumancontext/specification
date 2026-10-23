"""Affect content (R-X3, R-X4): the lexical classifier, affect predicates and the quarantine mark.

The classifier is deliberately broad: when unsure, it says "affect". It is used by the GUM importer to quarantine
or refuse propositions, and by the checker for the W-CL4 warning. It never decides what a person feels.
"""

import re

EMOTION_PREDICATES = ("mood", "emotion", "stress", "affect")
# Non-affect state predicates that may rest on behavioural signals (R-X4, CL-4).
NON_AFFECT_STATE_PREDICATES = ("availability", "load")
QUARANTINE = re.compile(
    r"(?i)\b(stress\w*|mood\w*|emotion\w*|affect\w*|anxi\w*|mental\w*|depress\w*|burn-?out|panic\w*|"
    r"sad(?:ness)?|ang(?:er|ry)|upset|worr\w*|fear\w*|lonel\w*|overwhelm\w*|frustrat\w*|nervous\w*|"
    r"grie(?:f|ving)|trauma\w*|distress\w*|unhapp\w*|happ(?:y|iness)|cry(?:ing)?|tearful)\b")
QUARANTINE_HANDLING = ("no-infer", "person-only")


def affect_text(*texts):
    """True when any text speaks of affect, mood, stress, emotion, anxiety or a mental condition."""
    return bool(QUARANTINE.search(" ".join(t for t in texts if isinstance(t, str))))


def predicate_is_affect(predicate, vocabulary=None):
    """An affect predicate, or a local ``x-`` code whose ``broader`` chain in ``vocabulary`` reaches one."""
    seen = set()
    vocabulary = vocabulary or {}
    while isinstance(predicate, str) and predicate not in seen:
        if predicate in EMOTION_PREDICATES:
            return True
        seen.add(predicate)
        entry = vocabulary.get(predicate)
        predicate = entry.get("broader") if isinstance(entry, dict) else None
    return False


def quarantine_marked(data):
    """The R-X3 quarantine: special, mental-health, no-infer and person-only."""
    return set(QUARANTINE_HANDLING) <= set(data.get("handling") or []) and \
        "mental-health" in set(data.get("categories") or []) and data.get("sensitivity") == "special"
