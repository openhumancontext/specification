# Kofi — a GUM import, an assessment import and an ODE employee

**Authored synthetic example.** Kofi, his work and every observation are fictional. The GUM tables, the scorer output
and the ODE fragment are synthetic files written for this example. No GUM instance, scorer, holder or digital
employee was run against a real person.

## The story

Kofi is a freelance translator. A General User Model (GUM) instance observed his screen and calendar for two weeks and
proposed a few statements about him. He imports them into his own context, keeps some, contests one and declines
another. A week later he imports a second snapshot: one proposition was revised, one disappeared, and a new one is
about stress, which the importer refuses. He also imports his own IPIP-NEO-120 self-report results. Finally he gives a scheduling digital employee,
"Planner" (an ODE package), a rule-only grant, and exports what he accepts back to GUM under a filter.

## What the example demonstrates

| Feature | Where |
|---|---|
| GUM observations become Sources; propositions become proposed, inferred Claims with their provenance | `context/records/sources.jsonl`, `context/records/claims.jsonl`, `importedFrom`, `ext["gum.import"]` |
| GUM's creation time is the formulation time, the import time is the knowledge time | `formulatedAt` vs `recordedAt` on every imported record; `capturedAt` is absent, because GUM does not keep it |
| A missing confidence stays missing | the "focus blocks" proposition has no `confidence` (never 0) |
| The person decides | Reviews `rv-01`…`rv-08`, `rv-10`, `rv-11`: admit, endorse, contest, decline |
| Lineage across snapshots | the revised proposition supersedes the old Claim (`inferredLineage: true`); the vanished one is retracted by GUM (`rv-09`); nothing is deleted |
| No affect from behavioural signals (R-X4) | the stress proposition rests on a screen observation, so it is refused on import and is not in the context |
| A psychological assessment imported as data, not as a verdict | `src-11`, `la-01` (route `imported`), `as-01`: special tier, prohibited purposes, `decisionUse: never` |
| A refinement offered by GUM and left unanswered | `c-04` in `prop-01`; it stays proposed and expires on its own (silence is not acceptance) |
| A rule-only projection for an ODE employee, and a binding that pins the grant | `context/projections/prj-0012.json` (run-time evidence) and `ode/planner-binding.json` (names `g-03`, never the projection) |
| A filtered export back to GUM | `gum-export/propositions.json` and `gum-export/sidecar.jsonl` (Mode B), selected by the grant evaluation under `g-04` |

## Inspect the files

- [fixtures/gum-snapshot-1.json](fixtures/gum-snapshot-1.json) and [fixtures/gum-snapshot-2.json](fixtures/gum-snapshot-2.json):
  synthetic GUM tables (`observations`, `propositions`, `observation_proposition`). GUM has no subject column, and
  neither do these files.
- [importer-config.json](importer-config.json): the person and the GUM instance are named here, by configuration,
  never guessed from the data.
- [fixtures/ipip-neo-120-results.json](fixtures/ipip-neo-120-results.json): synthetic scorer output, five domain and
  thirty facet raw means. It contains no item text, no item responses and no scoring key.
- [context/](context/): the L2 package after import and review: manifest, records, Events, the Planner's
  projection, the vault (the observation texts and the results file, named by sha256) and the lock.
- [ode/planner-binding.json](ode/planner-binding.json): the ODE package fragment that binds the Planner to Kofi's
  grant `g-03`.
- [gum-export/](gum-export/): the Mode B export and its sidecar.
- [expected-check.json](expected-check.json): the exact JSON output of the reference checker for `context/`.

## What the import keeps

The import follows the [GUM binding](../../spec/bindings/GUM.md):

| GUM | OHC |
|---|---|
| each snapshot | one `import-run` Event; every imported record cites it in `importedFrom.run` |
| `observations` row | a Source asserted by the observer Party (`s-gum-1` "Screen", `s-gum-2` "Calendar"), origin `observed`, the content in the vault, `maxRelease: index` |
| `observations.created_at` / `updated_at` | `formulatedAt` / `ext["gum.import"].updatedAt` |
| `propositions` row | a Claim asserted by `a-gum`, recorded by Kofi, origin `inferred`, `facet: other`, the text verbatim, `epistemic: hypothesis` |
| `reasoning` | `rationale` |
| `confidence` 1–10 | `{"value": raw/10, "raw": raw, "scale": "gum:int-1-10", "semantics": "support-score"}`, absent when null |
| `decay`, `revision_group`, `version`, raw ids | `ext["gum.import"]`, so that a Mode B export reproduces every column |
| `observation_proposition` | `evidence`: whole-source spans of the joined observations |

Conventions this example fixes, so that the reference converter can reproduce `context/records`:

- record ids are `src-` or `c-` plus a UUIDv5 in the URL namespace over `<gumInstanceId>:obs:<id>` (observations) or
  `<gumInstanceId>:<id>` (propositions);
- observers are numbered `s-gum-<n>` in order of first appearance; `Screen` maps to `screen-observation` and
  `Calendar` to `calendar`;
- the optional horizon heuristic is not applied, and null values are omitted rather than written as 0;
- a proposition whose text speaks of stress, mood, emotion, affect, anxiety or mental condition is refused when it
  rests on a screen observation (R-X4), and quarantined otherwise (R-X3);
- every imported record carries `synthetic: true`, because this is a published example.

## Why the stress proposition is refused

The second snapshot proposes that Kofi is under heavy stress in deadline weeks. GUM drew it from a screen
observation, which is a behavioural signal. No record may hold a stress, mood, emotion or affect value derived from
such signals, whatever its facet or label (R-X4), so the importer does not import it at all and reports only that one
proposition was refused. A quarantine would not be enough: it would still keep a value inferred from behaviour.

If Kofi wants to say how deadline weeks feel to him, he says it himself, as a `declared` Claim in his own words. Other
affect propositions that do not rest on behavioural signals would be quarantined on import (tier `special`, category
`mental-health`, handling `no-infer` and `person-only`), visible to him alone.

## Why the Planner never sees the IPIP results

The Planner's grant `g-03` is rule-only: it covers boundaries, preferences and the `availability` and `load` states,
rendered as their text. The assessment `as-01` is treated as special category. A special record is served only to a
selector that names it by id, category or lens, under explicit consent, and `g-03` names none of these. Its use limits
also forbid personnel selection, task allocation, performance evaluation and every other decision use. So
`prj-0012` holds exactly three claims, "No calls on Fridays.", "Deadlines in writing." and the current availability,
and the Planner's request for commitments comes back as `not-disclosed`.

The ODE fragment carries no context values and no projection. It declares Kofi's grant `g-03` as an external
dependency (`urn:ohc:example:kofi:context#g-03`, version = the grant's `recordedAt`), lists `ohc.binding` in
`requiredExtensions`, names all thirteen prohibited purposes and requires a check at use. `prj-0012` is what the
Planner fetched at run time under that grant; its id and digest belong in a `use-report`, not in the package. The ODE
Party reference in the fragment is not identity and grants nothing.

## The export back to GUM

The export is made under `g-04`, whose grantee is the GUM instance. Records are selected by the grant evaluation
under `g-04` and then by the export filter. Only active records pass, and never declined,
retracted, rejected or contested ones, special records, records with `no-infer`, `person-only` or `no-forward`
handling, frame-relative records or readings. Five propositions leave: two imported ones Kofi endorsed (with their
original GUM columns), his two own statements (`Declared by subject on …; origin=declared; ohc:<id>`), and the
revised proposition he endorsed. The contested, declined and retracted propositions stay home, and the refused one
was never imported.

## Check and interpret

From the repository root, with Python 3.9+ and `jsonschema`:

```sh
python3 tools/check.py examples/kofi-gum-ode/context --level L2 --json
```

The checker verifies structure, provenance, review rules, the Event chain, the lock and that `prj-0012` is what the
evaluation algorithm would serve. It does not establish that GUM's propositions or the scores are true, that Kofi's
consent was given as recorded, or how the Planner behaves at runtime.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
