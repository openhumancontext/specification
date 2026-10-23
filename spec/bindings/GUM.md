# GUM binding

Module `binding.gum` · format `0.1.0-draft` · **normative-draft for anyone claiming GUM compatibility**.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as described in BCP 14 (RFC 2119,
RFC 8174) when, and only when, they appear in all capitals.

This binding defines how a General User Model (GUM) store is imported into an OHC context, how an OHC context is
exported for a GUM store, and which round trips are lossless. Import reads all three GUM tables. Export writes the
`propositions` columns through an OHC JSON interchange file, and observations and the join table are one-way: there
is no writer into a gum-ai SQLite database. The reference implementation is
`tools/convert_gum.py`; the synthetic example is `examples/kofi-gum-ode/`.

## 1. Scope

**Source.** General User Models: the `gum-ai` package, version 0.1.11 (MIT licence), described in the UIST '25 paper
"Creating General User Models from Computer Use" (doi:10.1145/3746059.3747722).

**Tables.**

| Table | Columns |
|---|---|
| `observations` | `id`, `observer_name`, `content`, `content_type`, `created_at`, `updated_at` |
| `propositions` | `id`, `text`, `reasoning`, `confidence` (1–10, nullable), `decay` (1–10, nullable), `created_at`, `updated_at`, `revision_group`, `version` |
| `observation_proposition` | the join table between observations and propositions |

**What GUM does not keep.** These facts shape the import rules:

- GUM has no subject column. The user's name is a constructor argument substituted into prompts.
- GUM loses the capture time: `observations.created_at` is the time a batch was processed, not the time of capture.
- Since 2025-08-13, GUM deletes and recreates propositions on revision; `version` is always 1, and a new
  `revision_group` is minted on each revision. Revision lineage is therefore not kept at the source.

## 2. Import (GUM → OHC)

### 2.1 Field by field

| GUM | OHC | Notes |
|---|---|---|
| (instance) | Event `import-run`. `importedFrom` `{"system": "gum-ai", "systemVersion": "0.1.11", "importedAt", "run": <event id>}` on every record. | One run per snapshot. |
| `user_name` (configuration) | `Context.subject`, **from the importer configuration only, never guessed** | |
| `observations.id` | `Source.id` = `src-` + UUIDv5(ns, gumInstanceId + ":obs:" + id). The raw id is kept in `ext["gum.import"].observationId`. | Opaque ids (R-I1). |
| `observations.observer_name` | `Source.sourceKind`: `screen-observation` (screen observers), `calendar`, or `x-gum:<observer>`. `authorship.author` = a Party `s-gum-<n>` labelled with the observer name. | `screen-observation` triggers R-X4. |
| `observations.content` | A vault object plus `content.sha256`. With `--digest-only`: no vault object, and `maxRelease: index`. | The default is `maxRelease: index` for every GUM stream. |
| `observations.content_type` | `input_text` → `text/markdown`; `input_image` → `image/png` or `image/jpeg` (sniffed) | |
| `observations.created_at` | `formulatedAt` (R-T5b). `capturedAt` is **absent**: it was lost at the source. | |
| `observations.updated_at` | `ext["gum.import"].updatedAt` | |
| `propositions.id` | `Claim.id` = `c-` + UUIDv5(ns, gumInstanceId + ":" + id). The raw id is kept in `ext["gum.import"].id`. | |
| `text` | `Claim.text`, verbatim. `facet: other`. | A classifier MAY *propose* a separate, refining Claim. It never rewrites the import. |
| `reasoning` | `Claim.rationale` | |
| `confidence` (1–10) | `confidence` `{"value": raw/10, "raw": raw, "scale": "gum:int-1-10", "semantics": "support-score", "method": "gum-ai 0.1.11 PROPOSE/REVISE"}` | `null` → the field is absent, **never 0** (R-N2). |
| `decay` (1–10) | `ext["gum.import"].decay`. An optional horizon heuristic (1–4 `state`, 5–7 `focus`, 8–10 `foundation`), listed in `importedFrom.derivedFields: ["horizon"]`. | |
| `created_at` | `formulatedAt`, normalised to RFC 3339 UTC. When the stored string differs (SQLite's naive form with fractional seconds), the raw string is kept in `ext["gum.import"].createdAt`. | |
| `updated_at` | `lastEvidenceAt`, normalised; the raw string, when different, in `ext["gum.import"].updatedAt` | |
| `revision_group`, `version` | `ext["gum.import"].revisionGroup`, `ext["gum.import"].version` | |
| `observation_proposition` | `Claim.evidence`: `[{"span": {"source": <src id>, "selector": {"type": "whole"}}, "kind": "observation"}]` | |

### 2.2 Values implied on every imported proposition

- `origin: inferred`, and `assertedBy: "a-gum"` (a Party: the agent "GUM").
- `recordedBy`: the actor running the import. When that actor is the subject, no grant is needed. When it is anyone
  else, INF-1 applies: the importer needs a grant with `infer` for a named purpose.
- `generatedBy` `{"software": "gum-ai", "version": "0.1.11"}`.
- `epistemic: hypothesis`; admission `proposed`. The subject admits, declines, endorses or rejects each imported
  proposition through Reviews.
- Category `third-party` when other people are named (an importer heuristic, applied conservatively).

### 2.3 Refusal (R-X4) and quarantine (R-X3)

- A proposition about affect, mood, stress, emotion or mental condition that rests on a behavioural observation
  (`screen-observation` and every other kind flagged `biometricOrBehavioural`, `SPECIFICATION.md` §8.8) MUST be
  **refused**: it is not imported, whatever its wording or confidence, and the importer reports only how many were
  refused, never their text. GUM's screen observations are behavioural signals, so this covers most affect
  propositions GUM makes.
- Any other proposition about affect, mood, stress or mental condition MUST be quarantined: tier `special`,
  categories ⊇ `["mental-health"]`, handling ⊇ `["no-infer", "person-only"]`. Quarantined propositions are shown only
  to the subject.
- The classifier is lexical and broad. When it is uncertain, it says "affect": it refuses or quarantines.
- The person's own words about how they feel are recorded by the person, as `declared` Claims, never by import.

### 2.4 Lineage across snapshots

GUM no longer keeps revision lineage, so the importer reconstructs it from successive snapshots:

- a proposition missing from a later snapshot gets a Review `retract` by `a-gum`;
- a new proposition in the same `revision_group` supersedes the old one, with
  `ext["gum.import"].inferredLineage: true`;
- nothing is deleted.

### 2.5 Informative notes on GUM semantics

- GUM's prompt describes `decay` as "1 (short-lived) to 10 (long-lasting insight or pattern)", while its retrieval
  code uses the raw value as a decay *rate*. OHC therefore keeps the raw value and never converts it silently; the
  horizon heuristic is optional and declared in `derivedFields`.
- GUM's confidence is a verbalised evidence-support score, not a calibrated probability. That is why its
  `semantics` is `support-score`.
- GUM propositions can be about other people named in observations. The `third-party` category and the third-party
  rule TP-1 keep such content from becoming statements about another person's inner life.

## 3. Export (OHC → GUM)

### 3.1 Mandatory filter

- An export MUST be made under a grant with purpose `gum-export`, whose grantee is the GUM instance as a Party.
- Records are selected by the grant evaluation (`SPECIFICATION.md` §12.3) under that grant, then by this filter.
- Only records with admission `active` are exported.
- The following are **never** exported:
  - declined, retracted, rejected or contested records;
  - `special` records;
  - records with handling `no-infer`, `person-only` or `no-forward`;
  - `frame-relative` records;
  - interpretation-layer records, unless the grant says `interpretations: all`.

GUM has no access control: anything in its store can be surfaced to any client that can read it. The filter exists
for that reason.

**Erasure.** An export is a disclosure (`export-run`). When a record that was exported is later erased, the holder
sends the GUM instance an erasure notice (`SPECIFICATION.md` §15.5), and the GUM side is expected to delete the
matching proposition, found through the sidecar, and acknowledge.

### 3.2 Mode A — seed as observations

- Each Claim becomes one observation: `observer_name = "ohc"`, and
  `content = "[ohc] <subject alias> states (declared <formulatedAt date>): <text>"` for text claims, or
  `"… (origin <origin>) …"` for claims that are not declared.
- GUM then proposes its own propositions from these observations.

Mode A is the recommended mode for declared claims: GUM's revision step deletes and rewrites similar propositions,
so a declared claim inserted directly as a proposition would not stay authoritative.

### 3.3 Mode B — direct insert

One proposition per Claim:

| GUM column | Value |
|---|---|
| `text` | `text` |
| `reasoning` | `"Declared by subject on <date>; origin=<origin>; ohc:<id>"` |
| `confidence` | `clamp(round(value × 10), 1, 10)` if a confidence is present, else `null` |
| `decay` | from `ext["gum.import"].decay` if present, else by horizon (`state` 2, `focus` 6, `foundation` 9; no horizon: `null`) |
| `created_at` | the raw `ext["gum.import"].createdAt` if present, else `formulatedAt`, or `recordedAt` |
| `updated_at` | the raw `ext["gum.import"].updatedAt` if present, else `lastEvidenceAt` |

### 3.4 Sidecar

The exporter writes `ext/gum/sidecar.jsonl` in the package, one line per exported proposition:

```text
{"gumPropositionId", "ohcClaimId", "exportedAt", "policyVersion"}
```

and an Event `export-run`. Origin, endorsement, consent, sensitivity, validity and lineage have no slot in GUM; they
stay on the OHC side and are never encoded only in `reasoning` text.

## 4. Lossless round trips

What is tested is the `propositions` table, through the OHC JSON interchange file; observations and the join table
are one-way.

- **GUM → OHC → GUM (Mode B, with the same grant).** Every column of each proposition that the person admitted and
  that passes the export filter is reproduced exactly, including the raw timestamp strings; ids come back from
  `ext["gum.import"]`. Refused (R-X4), quarantined, special, `no-infer`, `person-only`, rejected, contested and
  retracted propositions do not return. (Tests: `test_gum_roundtrip_admitted_lossless`,
  `test_gum_roundtrip_does_not_return_refused_or_withheld`, `test_sqlite_naive_timestamps_roundtrip`.)
- **OHC → GUM → OHC.** Claim ids, text, origin and dates are restored through the sidecar and the reasoning tag; the
  other status axes stay on the OHC side. Records excluded by the filter are reported only in **the subject's**
  export report, never to GUM.

## 5. The gumcp-compatible tool

A holder MAY expose the tool `get_user_context` with the same name, parameters and block layout as GUM's MCP server,
so that clients built for GUM work unchanged, with consent and purpose filtering behind the tool. The signature, behaviour
and output format are defined in [MCP.md](MCP.md).

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
