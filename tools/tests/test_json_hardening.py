"""Strict JSON: duplicate keys, NaN and Infinity, non-ASCII member names, BOM, JSON Lines (J-1…J-5)."""

import os
import shutil
import tempfile
import unittest

import helpers  # noqa: F401  (puts tools/ on sys.path)

from ohclib import jsonio


class JsonHardening(unittest.TestCase):
    def rule_of(self, text):
        with self.assertRaises(jsonio.JsonError) as caught:
            jsonio.loads_strict(text)
        return caught.exception.rule

    def test_duplicate_keys(self):
        self.assertEqual(self.rule_of('{"a": 1, "a": 2}'), "J-2")
        self.assertEqual(self.rule_of('{"x": {"b": 1, "b": 1}}'), "J-2")

    def test_nan_and_infinity(self):
        for literal in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(literal=literal):
                self.assertEqual(self.rule_of('{"a": %s}' % literal), "J-3")

    def test_non_ascii_member_names(self):
        self.assertEqual(self.rule_of('{"größe": 1}'), "J-5")

    def test_jscontact_card_keeps_its_member_names(self):
        # RFC 9553 cards may carry non-ASCII keys (for example `keywords`); J-5 exempts /subject/card only.
        card = '{"subject": {"id": "urn:ohc:example:x", "card": {"@type": "Card", "version": "1.0", "keywords": {"Bäcker": true}}}}'
        self.assertEqual(jsonio.loads_strict(card)["subject"]["card"]["keywords"], {"Bäcker": True})
        self.assertEqual(self.rule_of('{"subject": {"id": "urn:ohc:example:x", "größe": 1}}'), "J-5")
        self.assertEqual(self.rule_of('{"subject": {"card": {}}, "ext": {"a.b": {"größe": 1}}}'), "J-5")

    def test_non_ascii_values_allowed(self):
        self.assertEqual(jsonio.loads_strict('{"text": "Человек"}'),
                         {"text": "Человек"})

    def test_byte_order_mark_rejected(self):
        with self.assertRaises(jsonio.JsonError) as caught:
            jsonio.decode_utf8(b"\xef\xbb\xbf{}", "x.json")
        self.assertEqual(caught.exception.rule, "J-1")

    def test_invalid_utf8_rejected(self):
        with self.assertRaises(jsonio.JsonError) as caught:
            jsonio.decode_utf8(b'{"a": "\xff"}', "x.json")
        self.assertEqual(caught.exception.rule, "J-1")

    def test_jsonl_one_object_per_line(self):
        self.assertEqual(jsonio.parse_jsonl_text('{"a": 1}\n{"b": 2}\n', "x.jsonl"), [(1, {"a": 1}), (2, {"b": 2})])
        for text in ('{"a": 1}\n\n{"b": 2}\n', '{"a": 1}\r\n', '[1, 2]\n'):
            with self.subTest(text=text):
                with self.assertRaises(jsonio.JsonError) as caught:
                    jsonio.parse_jsonl_text(text, "x.jsonl")
                self.assertEqual(caught.exception.rule, "J-4")

    def test_checker_reports_duplicate_key(self):
        tmp = tempfile.mkdtemp(prefix="ohc-json-")
        try:
            fixture = helpers.load_fixture(os.path.join(helpers.FIXTURES, "negative", "j-2-duplicate-key.json"))
            report = helpers.run_fixture(fixture, os.path.join(tmp, "ctx"))
            self.assertEqual(helpers.error_rules(report), ["J-2"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
