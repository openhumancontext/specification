"""Strict JSON and JSON Lines loading (§5.1, checker group J).

- J-1: files are UTF-8.
- J-2: duplicate member names are rejected.
- J-3: NaN and Infinity are rejected.
- J-4: JSON Lines hold exactly one JSON object per line.
- J-5: member names are ASCII.

Errors never carry field values: only the rule id, the file and a location.
"""

import json
import os


class JsonError(Exception):
    """A strictness violation. ``rule`` is a J-* rule id; ``where`` is a location."""

    def __init__(self, rule, path, where=""):
        Exception.__init__(self, "%s %s%s" % (rule, path, (" " + where) if where else ""))
        self.rule = rule
        self.path = path
        self.where = where


class _DuplicateKey(ValueError):
    pass


class _BadConstant(ValueError):
    pass


def _pairs_hook(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise _DuplicateKey("duplicate member name")
        obj[key] = value
    return obj


def _bad_constant(name):
    raise _BadConstant("non-finite number")


# Subtrees exempt from J-5: an embedded JSContact card keeps its own member names, which RFC 9553 lets carry
# non-ASCII text (for example vendor properties and `keywords` keys). SPECIFICATION.md §5.1.
NON_ASCII_EXEMPT = ("/subject/card",)


def _non_ascii_member(value, pointer=""):
    """Return the JSON pointer of the first non-ASCII member name, or None."""
    if pointer in NON_ASCII_EXEMPT:
        return None
    if isinstance(value, dict):
        for key, item in value.items():
            if any(ord(ch) > 127 for ch in key):
                return pointer + "/" + _escape_pointer_token(key.encode("ascii", "replace").decode("ascii"))
            found = _non_ascii_member(item, pointer + "/" + _escape_pointer_token(key))
            if found is not None:
                return found
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found = _non_ascii_member(item, pointer + "/" + str(index))
            if found is not None:
                return found
    return None


def _escape_pointer_token(token):
    return token.replace("~", "~0").replace("/", "~1")


def loads_strict(text, path="<string>", where=""):
    """Parse one JSON text with the J-2, J-3 and J-5 rules."""
    try:
        value = json.loads(text, object_pairs_hook=_pairs_hook, parse_constant=_bad_constant)
    except _DuplicateKey:
        raise JsonError("J-2", path, where)
    except _BadConstant:
        raise JsonError("J-3", path, where)
    except ValueError:
        raise JsonError("J-0", path, where)
    bad = _non_ascii_member(value)
    if bad is not None:
        raise JsonError("J-5", path, (where + " " if where else "") + bad)
    return value


def decode_utf8(data, path):
    """Decode bytes as UTF-8 (J-1). A UTF-8 byte order mark is rejected too."""
    if data.startswith(b"\xef\xbb\xbf"):
        raise JsonError("J-1", path, "byte order mark")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        raise JsonError("J-1", path)


def load_json(path):
    """Load one JSON document strictly."""
    with open(path, "rb") as handle:
        data = handle.read()
    return loads_strict(decode_utf8(data, path), path)


def parse_jsonl_text(text, path):
    """Parse JSON Lines text: exactly one JSON object per line (J-4).

    A final newline is allowed; blank lines inside the file are not.
    Returns a list of ``(line_number, object)``.
    """
    records = []
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    for number, line in enumerate(lines, 1):
        if line.endswith("\r"):
            raise JsonError("J-4", path, "line %d" % number)
        if not line.strip():
            raise JsonError("J-4", path, "line %d" % number)
        value = loads_strict(line, path, "line %d" % number)
        if not isinstance(value, dict):
            raise JsonError("J-4", path, "line %d" % number)
        records.append((number, value))
    return records


def load_jsonl(path):
    """Load a JSON Lines file strictly. Returns a list of ``(line_number, object)``."""
    with open(path, "rb") as handle:
        data = handle.read()
    return parse_jsonl_text(decode_utf8(data, path), path)


def dumps_pretty(value):
    """The JSON file style of this repository: 2-space indent, UTF-8, final newline."""
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def write_pretty(path, value):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(dumps_pretty(value))


def write_jsonl(path, records):
    """Write records as JSON Lines in JCS form, one per line (§3.3)."""
    from . import jcs

    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(jcs.canonicalize(record))
            handle.write("\n")
