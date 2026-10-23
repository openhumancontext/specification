"""RFC 8785 test vectors (shared by test_jcs.py and check.py --self-test, SELF-3).

``NUMBER_VECTORS`` are the IEEE 754 values of RFC 8785 Appendix B with their
expected serializations; ``None`` marks values that MUST be rejected (NaN and
Infinity).
"""

NUMBER_VECTORS = [
    ("0000000000000000", "0"),
    ("8000000000000000", "0"),
    ("0000000000000001", "5e-324"),
    ("8000000000000001", "-5e-324"),
    ("7fefffffffffffff", "1.7976931348623157e+308"),
    ("ffefffffffffffff", "-1.7976931348623157e+308"),
    ("4340000000000000", "9007199254740992"),
    ("c340000000000000", "-9007199254740992"),
    ("4430000000000000", "295147905179352830000"),
    ("7fffffffffffffff", None),
    ("7ff0000000000000", None),
    ("44b52d02c7e14af5", "9.999999999999997e+22"),
    ("44b52d02c7e14af6", "1e+23"),
    ("44b52d02c7e14af7", "1.0000000000000001e+23"),
    ("444b1ae4d6e2ef4e", "999999999999999700000"),
    ("444b1ae4d6e2ef4f", "999999999999999900000"),
    ("444b1ae4d6e2ef50", "1e+21"),
    ("3eb0c6f7a0b5ed8c", "9.999999999999997e-7"),
    ("3eb0c6f7a0b5ed8d", "0.000001"),
    ("41b3de4355555553", "333333333.3333332"),
    ("41b3de4355555554", "333333333.33333325"),
    ("41b3de4355555555", "333333333.3333333"),
    ("41b3de4355555556", "333333333.3333334"),
    ("41b3de4355555557", "333333333.33333343"),
    ("becbf647612f3696", "-0.0000033333333333333333"),
    ("43143ff3c1cb0959", "1424953923781206.2"),
]

# RFC 8785 section 3.2.3: input text and its canonical form.
STRUCTURE_INPUT = (
    '{\n  "numbers": [333333333.33333329, 1E30, 4.50, 2e-3, 0.000000000000000000000000001],\n'
    '  "string": "\\u20ac$\\u000F\\u000aA\'\\u0042\\u0022\\u005c\\\\\\"\\/",\n'
    '  "literals": [null, true, false]\n}'
)
STRUCTURE_OUTPUT = (
    '{"literals":[null,true,false],"numbers":[333333333.3333333,1e+30,4.5,0.002,1e-27],'
    '"string":"€$\\u000f\\nA\'B\\"\\\\\\\\\\"/"}'
)

# RFC 8785 section 3.2.3, sorting of object properties (UTF-16 code units).
SORTING_INPUT = (
    '{"\\u20ac": "Euro Sign", "\\r": "Carriage Return", "\\ufb33": "Hebrew Letter Dalet With Dagesh", '
    '"1": "One", "\\ud83d\\ude00": "Emoji: Grinning Face", "\\u0080": "Control", '
    '"\\u00f6": "Latin Small Letter O With Diaeresis"}'
)
SORTING_ORDER = ["\r", "1", "\u0080", "ö", "€", "\U0001f600", "דּ"]
