# Write a minimal context in five minutes

**Guide · informative · 0.1.0-draft.** A minimal OHC context (level **L0**) is one JSON file with a subject and a few claims. This guide writes one with a fictional person, Ilse. If you are an agent writing with a person, follow [CONTEXT-01](../agents/procedures/CONTEXT-01.md); it adds the steps for asking and confirming.

## 1. Start the file

Create `context.json` with the five manifest fields:

```json
{
  "format": "ohc.context",
  "specVersion": "0.1.0-draft",
  "id": "urn:ohc:example:ilse:context",
  "version": "1",
  "subject": {"id": "urn:ohc:example:ilse", "displayName": "Ilse (fictional)"},
  "synthetic": true,
  "claims": []
}
```

- `format` and `specVersion` are fixed for this version of the format.
- `id` is a URI you control. Real holders SHOULD use `urn:uuid:…`; the `urn:ohc:example:` form is for examples only.
- `version` is yours to choose. Change it with every change set.
- `subject.id` identifies the person. It is never sent to anyone the person shares the context with; they get a pairwise alias instead.
- `synthetic: true` marks example data. Leave it out for a real person.

## 2. Add claims in the person's words

Each claim needs six fields: `id`, `facet`, `text` (or `absence`), `origin`, `assertedBy` and `recordedAt`.

```json
{"id": "c-1", "facet": "goal", "text": "Finish the Dutch B1 course by June 2027.", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-09T08:00:00Z", "horizon": "focus", "valid": {"until": "2027-07-01"}, "synthetic": true}
```

- **`facet`** says what kind of statement it is: `goal`, `boundary`, `preference`, `state`, `need`, `declared-value` and so on ([the list](../../spec/SPECIFICATION.md#942-facets-families-and-predicates)). An optional `predicate` narrows it, for example `time-window` for a boundary. Predicates are a **closed list per facet** (or an `x-` code you define in `vocabulary`); when unsure, leave `predicate` out. The common ones:

  | Facet | Predicates |
  |---|---|
  | `goal` | `outcome`, `habit`, `career`, `learning`, `relationship` |
  | `boundary` | `never`, `only-if`, `ask-first`, `time-window` |
  | `preference` | `channel`, `timing`, `tone`, `detail-level`, `format`, `decision-brief`, `pushback` |
  | `state` | `energy`, `attention`, `availability`, `load`, `location-status` (and the affect predicates, which only the person may declare) |
- **`text`** keeps the person's own words. Do not rephrase them into a profile.
- **`origin`** is `declared` when the person said it. Anything you concluded yourself is `inferred`, never `declared` (R-O2).
- **`assertedBy`** is `"subject"` when it is the person's own statement.
- **`recordedAt`** is when the claim entered this file, with a time zone offset.
- **`horizon`** is optional: `foundation` (changes over years), `focus` (months) or `state` (hours or days). A `state` claim should say until when it holds (`valid.until`): inside that window it is current, and after it, expired. Without `valid.until` it is due for review after one day.

## 3. Keep a gap as a gap

When the person chooses not to define something, say so instead of leaving it out or filling it in:

```json
{"id": "c-5", "facet": "goal", "predicate": "career", "absence": {"code": "not-chosen", "intentional": true}, "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-09T08:00:00Z", "synthetic": true}
```

An absence is never zero, false, a default or consent (R-B1). `intentional: true` marks a protected choice: the right not to set a goal.

## 4. The whole file

This is Ilse's complete context, [examples/ilse-minimal/context.json](../../examples/ilse-minimal/context.json):

```json
{
  "format": "ohc.context",
  "specVersion": "0.1.0-draft",
  "id": "urn:ohc:example:ilse:context",
  "version": "1",
  "subject": {"id": "urn:ohc:example:ilse", "displayName": "Ilse (fictional)"},
  "synthetic": true,
  "claims": [
    {"id": "c-1", "facet": "goal", "text": "Finish the Dutch B1 course by June 2027.", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-09T08:00:00Z", "horizon": "focus", "valid": {"until": "2027-07-01"}, "synthetic": true},
    {"id": "c-2", "facet": "boundary", "predicate": "time-window", "text": "No work messages after 19:00 on weekdays.", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-09T08:00:00Z", "horizon": "foundation", "synthetic": true},
    {"id": "c-3", "facet": "preference", "predicate": "format", "text": "Short written summaries before calls.", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-09T08:00:00Z", "synthetic": true},
    {"id": "c-4", "facet": "state", "predicate": "availability", "text": "Travelling; slow replies.", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-09T08:00:00Z", "horizon": "state", "valid": {"from": "2026-10-09", "until": "2026-10-13"}, "synthetic": true},
    {"id": "c-5", "facet": "goal", "predicate": "career", "absence": {"code": "not-chosen", "intentional": true}, "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-09T08:00:00Z", "synthetic": true}
  ]
}
```

## 5. Check it

From the specification repository, with Python 3.9+ and `jsonschema` installed:

```sh
python3 tools/check.py examples/ilse-minimal --level L0 --json
```

The checker is read-only and never prints your values. For Ilse it reports `"valid": true` and `"levelMet": "L0"`, and it lists the defaults it applied in `defaultsApplied`:

- `conformance.level`: no level was declared, so L0 was assumed;
- `sensitivity`: claims default to the `personal` tier;
- `admission`: the subject's own claims are active;
- `endorsement`: the subject's own claims count as endorsed;
- `epistemic`: declared claims are recorded "as reported".

It also says what it did not verify: that the content is true, or that anyone consented to anything.

## 6. What this file allows

Nothing leaves this file. **With no grant, nothing is disclosed to anyone but the subject.** To let an agent read part of it, the person adds a Grant: a named recipient, a purpose, a scope and an expiry ([§12 of the specification](../../spec/SPECIFICATION.md#12-grant-and-grant-evaluation)). Two things go with the first grant:

- Grants belong to the `governance` module, so the file declares it: `"conformance": {"level": "L0", "modules": ["core", "governance"], "subjectIsAdult": true}`. A file that declares a level also attests that its subject is an adult (R-C4).
- The recipient is a Party: list it in `parties`, for example `{"id": "a-1", "partyKind": "agent", "label": "Calendar assistant"}`, and name it as `grantee`.

A grant is usable at any level, and required for any disclosure at L2.

## Start from an experience

A person does not have to begin with statements about themselves. A context may start from something that happened, and from how the person understood it then and later (LV-0). This file is a complete context at level L1, about Lio, who is fictional:

```json
{
  "format": "ohc.context",
  "specVersion": "0.1.0-draft",
  "id": "urn:ohc:example:lio:context",
  "version": "1",
  "subject": {"id": "urn:ohc:example:lio", "displayName": "Lio (fictional)"},
  "conformance": {"level": "L1", "subjectIsAdult": true},
  "synthetic": true,
  "episodes": [
    {"id": "ep-1", "occurred": {"start": "2026-10-03", "precision": "day"}, "accounts": [{"narrator": "subject", "narratedAt": "2026-10-03T21:00:00Z", "addedAt": "2026-10-03T21:00:00Z", "accountKind": "in-the-moment", "happened": "I left the climbing gym after one route instead of three.", "understandingThen": "My shoulder was not right."}], "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-03T21:00:00Z", "synthetic": true}
  ],
  "interpretations": [
    {"id": "in-1", "about": ["ep-1"], "stance": "retrospective", "text": "I left because of my shoulder.", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T08:00:00Z", "synthetic": true},
    {"id": "in-2", "supersedes": "in-1", "about": ["ep-1"], "stance": "revision", "text": "I left because the people I usually climb with were not there.", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-10T08:00:00Z", "synthetic": true}
  ]
}
```

- The **Episode** keeps what happened and how Lio understood it at the time (`understandingThen`). Later readings never go into the Episode.
- Each later reading is a separate **Interpretation**. `in-2` supersedes `in-1`, so both stay: "how did I understand this then?" remains answerable (§7.3).
- An agent working with Lio would add its own readings as proposals under a grant with `infer`. See [Mara's example](../../examples/mara-l1-agent/) for a persistent companion doing exactly that.

## Choose a lens (optional)

If the person already describes themselves through a framework, from a test they took, their therapy, coaching or a practice, record that relation as a LensAdoption ([§10.5](../../spec/SPECIFICATION.md#105-lensadoption)).

- Pick a lens by how it works with a person: what it attends to, its stance, how change happens in it, what a helper must not do, and its toolkit. [LENSES.md §7.6](../../spec/LENSES.md#76-how-each-lens-works-with-a-person) shows this for every catalog entry.
- An agent interprets through a lens only under the person's grant (`infer` naming the lens) and adoption (`agentInterpretation`, I5). A descriptor carries facts and guidance, never a permission.
- A framework that is not in the catalog can be described with a short local descriptor ([LENSES.md §5.1](../../spec/LENSES.md#51-local-lenses)). Without any descriptor, the lens is treated as a stub: its results are `frame-relative` (LA-6).

## Next steps

- **L1 Grounded:** cite grounds for every inferred claim, hash your sources, and record every status change as a Review. See [Mara's example](../../examples/mara-l1-agent/): one file, an episode-first context, and a persistent study companion whose readings are proposals that Mara reviews in batches.
- **L2 Governed:** move to the package form, with an event log, grants, projections and a lock. See [Noa's example](../../examples/noa-episode-first/).
- [The overview](../OVERVIEW.md) explains why the format is built this way.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
