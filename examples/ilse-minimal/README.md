# Ilse — a minimal context, written by hand

**Authored synthetic example.** Ilse is fictional. No real person's data is included.

This is the smallest useful Open Human Context: one JSON file, written by hand in five minutes, with a subject and
five claims. It is conformance level **L0 Minimal** and needs no tools, no package and no grants.

## What it demonstrates

- **The required path is short.** The document has `format`, `specVersion`, `id`, `version` and `subject.id`. Each
  claim has the six required fields: `id`, `facet`, `text` (or `absence`), `origin`, `assertedBy` and `recordedAt`.
- **Four horizons of everyday context.** A goal with a validity window (`c-1`, `focus`), a boundary (`c-2`,
  `foundation`), a working preference (`c-3`) and a current state that expires on its own (`c-4`, `state`, valid
  until 13 October).
- **The right not to define.** `c-5` is an intentional absence: Ilse chose not to set a career goal. The choice is
  kept as `not-chosen` with `intentional: true`; it is never filled in, never read as zero and never read as consent.
- **Default deny.** There is no grant, so nothing is disclosed to anyone but Ilse herself.

## Inspect the files

- [context.json](context.json): the whole context. It is byte-identical to the "L0 in five minutes" block of the
  repository [README](../../README.md).
- [expected-check.json](expected-check.json): the exact JSON output of the reference checker for this file.

## Check and interpret

From the repository root, with Python 3.9+ and `jsonschema`:

```sh
python3 tools/check.py examples/ilse-minimal --level L0 --json
```

The checker reports `valid: true` and `levelMet: "L0"`. Because the file states so little, the checker also names
the defaults it applied:

| Default applied | What it means here |
|---|---|
| `conformance.level` | No level is declared, so L0 is assumed and reported (R-C1). |
| `sensitivity` | The claims carry no tier, so each gets the default for its kind and facet (`personal`). |
| `admission` | Ilse wrote the claims herself, so they are `active` without any review. |
| `endorsement` | Her own claims start as `endorsed`. |
| `epistemic` | Declared claims start as `as-reported`. |

The checker verifies structure and declared relationships only. Truth of content, consent and any runtime
behaviour remain unverified, and the report says so in its flags.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
