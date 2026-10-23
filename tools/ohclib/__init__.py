"""Shared library for the Open Human Context reference tools.

The modules here are used by the command-line tools in ``tools/``. They have no
command-line interface of their own. Only the standard library and ``jsonschema``
(with its ``referencing`` dependency) are used.

Privacy rule for every module (§5.8): never echo field values in messages or
logs; name the record id, the field path and the rule id only.
"""

SPEC_VERSION = "0.1.0-draft"
RELEASE_VERSION = "0.1.0-draft.2"
