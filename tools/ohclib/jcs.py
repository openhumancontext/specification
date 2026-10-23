"""RFC 8785 JSON Canonicalization Scheme (JCS).

Used for every JSON digest OHC defines (§5.1): the projection digest, the Event
``entryDigest`` and ``prev`` chain, ``confirmationDigest``, R-S1 equality and the
pins in the ODE binding. Numbers are serialized per RFC 8785 section 3.2.2.3
(ECMAScript ``Number.prototype.toString``); the RFC's test vectors are in
``tools/tests/test_jcs.py``.
"""

import decimal
import hashlib
import math
import struct


class JcsError(ValueError):
    pass


def _format_number(value):
    if isinstance(value, bool):
        raise JcsError("boolean is not a number")
    if isinstance(value, int):
        number = float(value)
        if abs(value) < 2 ** 53:
            return str(value)
    else:
        number = float(value)
    if math.isnan(number) or math.isinf(number):
        raise JcsError("non-finite number")
    if number == 0:
        return "0"
    if number < 0:
        return "-" + _format_positive(-number)
    return _format_positive(number)


def _format_positive(number):
    # repr() gives the shortest decimal string that round-trips (as ECMAScript does).
    digits_tuple = decimal.Decimal(repr(number)).as_tuple()
    digits = "".join(str(d) for d in digits_tuple.digits)
    exponent = digits_tuple.exponent
    stripped = digits.rstrip("0")
    exponent += len(digits) - len(stripped)
    digits = stripped.lstrip("0") or "0"
    k = len(digits)
    n = exponent + k
    if k <= n <= 21:
        return digits + "0" * (n - k)
    if 0 < n <= 21:
        return digits[:n] + "." + digits[n:]
    if -6 < n <= 0:
        return "0." + "0" * (-n) + digits
    e = n - 1
    sign = "+" if e >= 0 else "-"
    if k == 1:
        return digits + "e" + sign + str(abs(e))
    return digits[0] + "." + digits[1:] + "e" + sign + str(abs(e))


_ESCAPES = {
    '"': '\\"',
    "\\": "\\\\",
    "\b": "\\b",
    "\f": "\\f",
    "\n": "\\n",
    "\r": "\\r",
    "\t": "\\t",
}


def _format_string(text):
    out = ['"']
    for ch in text:
        if ch in _ESCAPES:
            out.append(_ESCAPES[ch])
        elif ord(ch) < 0x20:
            out.append("\\u%04x" % ord(ch))
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _utf16_key(text):
    return text.encode("utf-16-be")


def _serialize(value, out):
    if value is None:
        out.append("null")
    elif value is True:
        out.append("true")
    elif value is False:
        out.append("false")
    elif isinstance(value, (int, float)):
        out.append(_format_number(value))
    elif isinstance(value, str):
        out.append(_format_string(value))
    elif isinstance(value, (list, tuple)):
        out.append("[")
        for index, item in enumerate(value):
            if index:
                out.append(",")
            _serialize(item, out)
        out.append("]")
    elif isinstance(value, dict):
        out.append("{")
        for index, key in enumerate(sorted(value, key=_utf16_key)):
            if not isinstance(key, str):
                raise JcsError("member names must be strings")
            if index:
                out.append(",")
            out.append(_format_string(key))
            out.append(":")
            _serialize(value[key], out)
        out.append("}")
    else:
        raise JcsError("value is not JSON")


def canonicalize(value):
    """Return the JCS serialization of a JSON value as a str."""
    out = []
    _serialize(value, out)
    return "".join(out)


def canonical_bytes(value):
    return canonicalize(value).encode("utf-8")


def sha256_hex(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest(value):
    """``"sha256:" + hex(sha256(JCS(value)))``."""
    return "sha256:" + sha256_hex(value)


def equal(a, b):
    """JCS equality (R-S1, EP-2)."""
    return canonicalize(a) == canonicalize(b)


def number_from_ieee_hex(hex_text):
    """Helper for the RFC 8785 Appendix B vectors: a double from 16 hex digits."""
    return struct.unpack(">d", bytes.fromhex(hex_text))[0]


def format_number(value):
    """Public access to the number serializer (used by tests)."""
    return _format_number(value)
