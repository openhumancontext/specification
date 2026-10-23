# Lens recipe: Schwartz theory of basic human values

**Recipe · lens `urn:ohc:lens:schwartz-values` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe shows, step by step, how a person's value priorities (from a values questionnaire they took, from their coach, teacher or therapist, or in their own words) become OHC records that the person controls, while a measured profile and the values the person declares are kept apart.

The lens descriptor is [spec/lenses/schwartz-values.lens.json](../../spec/lenses/schwartz-values.lens.json): `descriptorStatus: draft`, kind `values-circular`, measurement tier `T2` (validated with caveats), ontological status `measured-construct`. Values form a circle: neighbouring values are compatible, opposite values trade off, and scores are centred on the person's own mean. The lens supports self-reflection on value trade-offs and language for priorities the person chose. It does not establish which values are right, political or religious views, or comparisons between people.

Two rules shape every step:

- **A measured profile is not a declared value.** The questionnaire result is an AssessmentRecord. What the person says matters to them is a Claim with facet `declared-value`, in their words. Neither is ever turned into the other (the descriptor's `ip.restrictions` and `helperMustNot`).
- **Values can reveal beliefs and politics.** Every record of this lens is treated as special category, with the categories `belief` and `political`, and nothing in it is ever used to infer views or to tailor persuasion.

The record shapes are in [SPECIFICATION.md](../../spec/SPECIFICATION.md) §10.5 (LensAdoption), §10.6 (AssessmentRecord), §10.3 (Interpretation), §10.4 (Tension), §13 (Event), §17 (Practice, Outcome) and §12 (Grant); the schemas are in [spec/schema/](../../spec/schema/). The lens rules are in [LENSES.md](../../spec/LENSES.md).

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them.

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:schwartz-values-basic`](../../spec/playbooks/schwartz-values-basic.playbook.json) (Schwartz values: basic ways of working, by the OHC editors), for these situations: choosing between options; planning the week ahead; preparing a hard conversation; after a setback. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

**Bringing a report through the person's window.** When an instrument's catalog entry carries an `import` block, a person can bring its result through their own window ([guide](../guides/BRING-A-RESULT.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). No entry of this lens has one yet, so the steps below record the report by hand.

## 1. What you may have

| Input | Use it? | Where it goes |
|---|---|---|
| The person's own words about what matters to them ("choosing my own way of working matters to me") | Yes | Claims with facet `declared-value` (step 4); never an AssessmentRecord |
| A PVQ-RR result the person took: scored by a scoring tool, or by hand with the public scoring instructions. PVQ-RR is the only values instrument in the 0.1 catalog; its licence was not found **[U]** | Yes | Source (step 2) and AssessmentRecord with `mode: self-report-instrument` (step 3); scored by hand: the variant "scored by hand" in steps 1–4 |
| A result from another values questionnaire (a shorter or older form, or another questionnaire) | Only the report, as a Source | Source (step 2, variant "another questionnaire"): `sourceKind: "instrument-report"`, `authorship.author` a software Party for that questionnaire, `sensitivity: "special"`, `categories: ["belief", "political"]`, `maxRelease: "index"`. No AssessmentRecord: the checker rejects an instrument the lens does not list (AR-8). The person's own conclusions go into declared-value Claims |
| Notes from a coach, teacher or therapist who works with values | Yes, with the practitioner's written release | Route `inherited-from-practice` with `practice.releaseRef` (step 1, variant), release and notes Sources (step 2, variant) |
| The person's accounts of decisions and their own reading of which values pulled against each other | Yes | Episode and Interpretation (step 5); a Tension between declared values (step 4) |
| An agent's reading ("your messages suggest you value tradition") | **Only under the person's Grant** | An Interpretation by the agent needs `suggest` and `infer` naming the lens, and the person's active adoption not set to `off` (I5). No grant ever licenses inferring political or religious views (C-7, §8.10; `helperMustNot`). In the example the person allows none. |

**[U]** is an evidence grade: unverified, or a known gap ([LENSES.md](../../spec/LENSES.md) §7.3; the citation is listed there).

## 2. Before you start

### 2.1 Route of adoption

Choose one route with the person. It decides who writes the LensAdoption and when it becomes active. Step 1 has a complete record for each route that the worked examples use.

| Route | When | What it changes |
|---|---|---|
| `self-chosen` | The person picks the lens themselves; also when they scored the questionnaire by hand. | The person writes the adoption: `assertedBy: "subject"`, `origin: "declared"`. It is active at once. Record: step 1, variant "scored by hand". |
| `agent-suggested` | The person asked an agent for ways of looking at what matters to them (the descriptor's `adoption.suggestionRequires`), and accepted the lens the agent offered. | First the person gives the agent a grant with the action `suggest` whose scope names the lens (the grant `g-0` of step 6, variant, has this shape). The agent then writes the adoption under that grant: `suggestedBy` and `assertedBy` are its own Party id, `origin: "observed"` (`declared` is refused by ENV-2), `underGrant` is the grant's id and `purpose` is one of the grant's `purposes`. It stays `proposed` until the person writes a Review `admit` (LA-1). The [enneagram recipe](enneagram.md), step 1, shows the three records in full. |
| `inherited-from-practice` | The lens comes from the person's coach, teacher or therapist (the descriptor's `adoption.inheritanceRoles`). | The practitioner is a Party with `role: "practitioner"`; the adoption carries a `practice` block. If session material is stored, the practitioner's release is stored first as a Source of kind `practitioner-release`, and the same id goes in the adoption's `practice.releaseRef` (LA-3) and in the notes Source's `custody.releaseRef` (SR-7). Set `confidentiality` to `practitioner-scope`, or for a therapist `therapy-confidential` if the person chooses it; LA-4 then makes the adoption `person-only`, but it does not reach the person's own records in the lens, so also add `"person-only"` to their `handling` (section 6). Leave `onEnd` at `ask`. The adoption gives the practitioner no access (LA-2). Records: step 1 and step 2, variant "coach's notes". |
| `imported` | A scoring tool writes the adoption together with the result. This is the route of the worked example. | `origin: "derived"`, `derivedFrom` naming the result Source, `generatedBy` naming the tool, and `importedFrom` with a `run` id shared by every record of the same import; each record's `importedFrom.importedAt` equals its own `recordedAt` (ENV-3). The adoption and the AssessmentRecord with that `run` stay `proposed` until the person admits them (LA-5). |

In the example `agentInterpretation` is `"off"` on every route, the default the person keeps: only the person writes readings through this lens (I5). The person may change it.

### 2.2 Consent

- An agent speaks in the lens's language once the person adopted it, in the person's own words; it never compares the person's values with other people (`agentPosture`).
- Nothing leaves the context without a Grant (R-G1). Results in this lens are treated as special category: a grant needs `basis.legal: "explicit-consent"`, must name the records by id, by the lens or by the category `belief` or `political` (R-G3), and lasts at most 180 days (GR-1).
- An imported result counts only after the person has looked at it: until their Review, it is `proposed` and served to nobody.

### 2.3 Defaults for this lens

| Setting | Value | Why |
|---|---|---|
| `sensitivity` | `"special"` on every record that names the lens (LensAdoption, AssessmentRecord, Interpretation with `lens`, Practice with `source.lens`), on every Source of a result, report, release or notes, and on every Claim that cites such a Source | The descriptor's `defaults.sensitivity`; AR-5; I9; propagation rule C3 |
| `categories` | `["belief", "political"]` on the same records | The descriptor's `defaults.categories` |
| Declared-value Claims and their Tensions | `"sensitive"` (the kind default), raised to `special` only when the person's words touch a special category | §8.3; they do not name the lens |
| `handling` on results | `["no-infer", "no-leverage"]` | `no-infer`: the person keeps the profile from every inference and mapping (M-7; the lens also sets `crossLensMapping: not-allowed`). `no-leverage`: never used to persuade or steer the person (`persuasion-targeting` is prohibited). |
| `reviewAfter` | `"P3Y"` | The descriptor's `defaults.reviewAfter` |
| Source `maxRelease` | `"index"` | A grantee never receives the result file |

### 2.4 What is never stored

- PVQ-RR item text (the instrument entry's `neverStore`). The person's own item responses may be kept only in their own test data: `ext["ohc.test-data"]` with handling `person-only` and the validity flag `test-data-personal-only` (AR-3). The recipe recommends not keeping them at all.
- The scoring key (which item belongs to which value) inside any record.
- A declared value derived from the profile, and a profile built from declared values.
- Any comparison with other people: norm groups, "higher than most", group averages (M-5).
- Any guess about the person's political or religious views, and any judgement that a value is right or wrong.

## 3. Steps

Snippets are records from the worked examples (section 5) and validate against the named schemas. They carry `"synthetic": true` because they are examples. Use opaque ids (`as-1`, never `as-tradition`; W-ID1). Times are RFC 3339 with an offset.

**Set up the context once.** Create a directory for the context (the *context directory*) and save this skeleton in it as `context.json`. Each step below names the array its record goes in; inside an array, the order of records does not matter.

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:ohc:example:odile:context", "version": "2026-10-10.1",
 "subject": {"id": "urn:ohc:example:odile", "displayName": "Odile (fictional)"},
 "holder": "subject", "lang": "en", "created": "2026-09-15T08:00:00Z",
 "conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
 "parties": [
   {"id": "s-01", "partyKind": "software", "label": "Values questionnaire scorer"},
   {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}],
 "policy": {"admission": "subject-only", "resolver": "returnDialog"},
 "lenses": [{"id": "urn:ohc:lens:schwartz-values", "version": "0.2.0",
             "sha256": "3d794f1201ae2f22a719f0e44644deaa7829626f650700ede0df9c76786f9bb2"}],
 "events": [], "sources": [], "lensAdoptions": [], "assessments": [], "reviews": [], "claims": [], "tensions": [],
 "episodes": [], "interpretations": [], "practices": [], "outcomes": [], "grants": [],
 "synthetic": true}
```

- `format`, `specVersion`, `id`, `version` and `subject` are required (`context.schema.json`). `holder`, `lang`, `created` and `policy` are optional; keep them as shown. Arrays you do not use may be left out.
- `"synthetic": true` marks an example. In an example it MUST be on the context root and on every content record, or the check fails with CX-8. **For a real person**, give `id` and `subject.id` the form `urn:uuid:<a new UUID>`, and leave out `synthetic` at the root and on every record.
- `lenses[].sha256` is the SHA-256 of the descriptor file's bytes: `shasum -a 256 spec/lenses/schwartz-values.lens.json`.
- `governance` is needed for Events and Grants (steps 1, 6 and 7), `practices` for Practice and Outcome (step 6).
- Every Party you reference goes in `parties` (CX-3). The main path uses the scoring tool `s-01` and the companion `a-01`. The variant "another questionnaire" adds `{"id": "s-02", "partyKind": "software", "label": "Short values survey site"}`; the variant "coach's notes" needs `{"id": "p-01", "partyKind": "person", "label": "Coach", "role": "practitioner"}`.
- The check passes only once the context holds a Claim or an Episode with an account (LV-0); before step 4 it reports LV-0.

### Step 1. The import adopts the lens: LensAdoption and the import-run Event

The person scored their questionnaire with a tool, and the tool's import writes the adoption, the Source and the result in one run. First record the run as an Event (schema `event.schema.json`, array `events`):

```json
{"id": "e-1", "seq": 1, "at": "2026-09-15T08:00:00Z", "eventType": "import-run", "actor": "subject",
 "records": ["la-1", "src-1", "as-1"], "salt": "q7Hc2mVd9KxTzR4bWn8sLg",
 "prev": "sha256:0000000000000000000000000000000000000000000000000000000000000000"}
```

- `seq` is 1 for the first Event of the context; `at` is the time of the import; `records` lists the ids the import writes; `salt` is at least 16 random bytes in base64url, for example from `python3 -c "import secrets; print(secrets.token_urlsafe(16))"`; `prev` is `"sha256:"` followed by 64 zeros for the first Event (a later Event uses the previous Event's digest, §13.2). Events hold no free text (EV-3).

Then write the LensAdoption (schema `lens-adoption.schema.json`, array `lensAdoptions`):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:schwartz-values", "version": "0.2.0"}, "route": "imported",
 "uses": ["store-results", "speak-in-lens", "interpret", "offer-practices"], "interpretationAuthors": ["subject"],
 "agentInterpretation": "off", "representationPreference": "schwartz-values.circular-chart", "origin": "derived",
 "derivedFrom": ["src-1"],
 "generatedBy": {"software": "values-scorer", "version": "1.2.0", "method": "adopt the lens of the imported instrument"},
 "importedFrom": {"system": "values-scorer", "systemVersion": "1.2.0", "importedAt": "2026-09-15T08:00:00Z", "run": "e-1"},
 "assertedBy": "subject", "recordedAt": "2026-09-15T08:00:00Z", "sensitivity": "special",
 "categories": ["belief", "political"], "synthetic": true}
```

- Give every record of the import the same `importedFrom.run`: the id of the import-run Event. The checker does not yet resolve `run` against the Event (section 6); step 8 checks it by hand.
- Each record's `importedFrom.importedAt` equals its own `recordedAt` (ENV-3).
- `uses` are confirmed with the person when they admit the adoption (step 4): `speak-in-lens`, `store-results`, `interpret` (the person's own readings), `offer-practices` (an agent may offer `schwartz-values.values-in-tension`, the only toolkit item with `agentMayOffer: true`), `recall`.

**Variant "scored by hand": the person chose the lens and scored it themselves.** No Event and no `importedFrom`. The adoption is the person's own and active at once. From [examples/schwartz-values/variants/by-hand/context.json](examples/schwartz-values/variants/by-hand/context.json):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:schwartz-values", "version": "0.2.0"}, "route": "self-chosen",
 "uses": ["store-results", "speak-in-lens", "interpret", "offer-practices"], "interpretationAuthors": ["subject"],
 "agentInterpretation": "off", "representationPreference": "schwartz-values.circular-chart", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-09-15T08:00:00Z", "sensitivity": "special",
 "categories": ["belief", "political"], "synthetic": true}
```

**Variant "coach's notes": the lens comes from a coach, and session notes are stored.** Add `p-01` to `parties`, write the release Source (step 2, variant), then this adoption, then the notes Source. All are in [examples/schwartz-values/variants/coach-notes/context.json](examples/schwartz-values/variants/coach-notes/context.json):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:schwartz-values", "version": "0.2.0"}, "route": "inherited-from-practice",
 "practice": {"role": "coach", "practitioner": "p-01", "relationship": "active", "since": "2026-07-01", "releaseRef": "src-3"},
 "confidentiality": "practitioner-scope", "uses": ["store-results", "speak-in-lens", "interpret", "offer-practices"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off", "representationPreference": "schwartz-values.circular-chart",
 "onEnd": "ask", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:00:00Z",
 "sensitivity": "special", "categories": ["belief", "political"], "synthetic": true}
```

- `practice.role` is `coach`, `teacher` or `therapist` (the descriptor's `adoption.inheritanceRoles`). Without `practice.releaseRef`, LA-3 fails as soon as notes are stored.

**Who sees it by default:** only the person. An imported adoption stays `proposed`, and is served to no one, until the person admits it; a self-chosen or inherited one is active at once.

### Step 2. Keep the original: Source

The result file (scores only, never items):

1. compute its SHA-256: `shasum -a 256 <file>`;
2. copy it into the context directory as `vault/<first two hex characters of the hash>/<hash>.<extension>`;
3. write a Source (schema `source.schema.json`, array `sources`) whose `content.locator.vaultPath` is that same path, relative to the context directory and starting with `vault/`.

```json
{"id": "src-1", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/66/66fdb027b998d9f5d1ef3b3750aa1fa51515c0a68b47f2d175d31df65f749b3c.json"}, "sha256": "66fdb027b998d9f5d1ef3b3750aa1fa51515c0a68b47f2d175d31df65f749b3c", "mediaType": "application/json"},
 "capturedAt": "2026-09-14T20:30:00Z", "authorship": {"author": "s-01"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index", "retention": {"eraseOnRequest": true}, "origin": "imported",
 "importedFrom": {"system": "values-scorer", "systemVersion": "1.2.0", "importedAt": "2026-09-15T08:00:00Z", "run": "e-1"},
 "formulatedAt": "2026-09-14T20:30:00Z", "assertedBy": "subject", "recordedAt": "2026-09-15T08:00:00Z",
 "sensitivity": "special", "categories": ["belief", "political"], "synthetic": true}
```

- `formulatedAt` is when the scores were produced; `recordedAt` is when they entered the context (R-T5b).
- When the file is present, the checker reads it and compares its hash with `sha256`; a mismatch fails SR-2. `"vaultContentRead": false` in the checker's report means that the content was not interpreted; the hash is still checked. When the file is absent, as in the worked examples, only the record is checked.

**Variant "scored by hand".** The person's own score sheet: `authorship.author` is `"subject"`, `origin: "declared"`, no `importedFrom`, no `inbound`:

```json
{"id": "src-1", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/74/7413c6d945343591439cd39fb46c6652a27d388981eed96109ba1292e36eeec6.json"}, "sha256": "7413c6d945343591439cd39fb46c6652a27d388981eed96109ba1292e36eeec6", "mediaType": "application/json"},
 "capturedAt": "2026-09-14T21:00:00Z", "authorship": {"author": "subject"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index", "retention": {"eraseOnRequest": true}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-15T08:02:00Z", "sensitivity": "special", "categories": ["belief", "political"], "synthetic": true}
```

**Variant "another questionnaire": a report from a values questionnaire that is not in the catalog.** Keep it as a Source only, and write no AssessmentRecord. `authorship.author` is a software Party for that questionnaire, such as `s-02`; never name the questionnaire in `title`. From the by-hand file:

```json
{"id": "src-2", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/05/051af99e6b54400e6b66867e556a1738e3c9880e91a661d87a3e8f220e1965b0.pdf"}, "sha256": "051af99e6b54400e6b66867e556a1738e3c9880e91a661d87a3e8f220e1965b0", "mediaType": "application/pdf"},
 "capturedAt": "2026-08-30T12:00:00Z", "authorship": {"author": "s-02"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-15T08:03:00Z", "sensitivity": "special",
 "categories": ["belief", "political"], "synthetic": true}
```

**Variant "coach's notes": the release, then the notes.** The release is the practitioner's written permission to keep the notes. Store it first:

```json
{"id": "src-3", "sourceKind": "practitioner-release",
 "content": {"locator": {"vaultPath": "vault/3a/3a3c1eed46da5f6f71ed0840f339a3aefd617bea0943b7cf1a43c7859600d321.pdf"}, "sha256": "3a3c1eed46da5f6f71ed0840f339a3aefd617bea0943b7cf1a43c7859600d321", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-19T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T17:50:00Z", "sensitivity": "special",
 "categories": ["belief", "political"], "synthetic": true}
```

Then the notes, citing the same release id:

```json
{"id": "src-4", "sourceKind": "practitioner-notes",
 "content": {"locator": {"vaultPath": "vault/5e/5e7349978e8051c7fa4556498824f14bc93c733ce5d9288c39c0c5a463695b02.pdf"}, "sha256": "5e7349978e8051c7fa4556498824f14bc93c733ce5d9288c39c0c5a463695b02", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-19T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "custody": {"custodian": "p-01", "confidentiality": "coaching", "releaseRef": "src-3"},
 "maxRelease": "index", "retention": {"eraseOnRequest": true}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-20T18:01:00Z", "sensitivity": "special", "categories": ["belief", "political"], "synthetic": true}
```

- The release id `src-3` appears twice: in `custody.releaseRef` here (SR-7) and in the adoption's `practice.releaseRef` (step 1; LA-3). For a therapist, use `"confidentiality": "therapy"` in `custody`.

**Who sees it by default:** only the person, at every tier (V-0). A grantee can receive at most the `index` tier.

### Step 3. Record the profile: AssessmentRecord

Write one AssessmentRecord for the profile (schema `assessment-record.schema.json`, array `assessments`):

```json
{"id": "as-1", "lens": {"id": "urn:ohc:lens:schwartz-values", "version": "0.2.0"}, "lensVariant": "19",
 "instrument": {"id": "urn:ohc:instrument:pvq-rr", "form": "57"}, "mode": "self-report-instrument",
 "assessedBy": "subject", "administeredAt": {"start": "2026-09-14", "precision": "day"},
 "results": [
   {"type": "values-profile", "scores": [
     {"construct": "schwartz-values/self-direction-thought", "raw": 5.67, "centered": 1.61},
     {"construct": "schwartz-values/self-direction-action", "raw": 5.33, "centered": 1.28},
     {"construct": "schwartz-values/stimulation", "raw": 4, "centered": -0.05},
     {"construct": "schwartz-values/hedonism", "raw": 4.33, "centered": 0.28},
     {"construct": "schwartz-values/achievement", "raw": 3.67, "centered": -0.39},
     {"construct": "schwartz-values/power-dominance", "raw": 2, "centered": -2.05},
     {"construct": "schwartz-values/power-resources", "raw": 2.33, "centered": -1.72},
     {"construct": "schwartz-values/face", "raw": 3.33, "centered": -0.72},
     {"construct": "schwartz-values/security-personal", "raw": 4.67, "centered": 0.61},
     {"construct": "schwartz-values/security-societal", "raw": 4, "centered": -0.05},
     {"construct": "schwartz-values/tradition", "raw": 2.67, "centered": -1.39},
     {"construct": "schwartz-values/conformity-rules", "raw": 3, "centered": -1.05},
     {"construct": "schwartz-values/conformity-interpersonal", "raw": 3.67, "centered": -0.39},
     {"construct": "schwartz-values/humility", "raw": 4, "centered": -0.05},
     {"construct": "schwartz-values/benevolence-caring", "raw": 5.33, "centered": 1.28},
     {"construct": "schwartz-values/benevolence-dependability", "raw": 5, "centered": 0.95},
     {"construct": "schwartz-values/universalism-concern", "raw": 4.67, "centered": 0.61},
     {"construct": "schwartz-values/universalism-nature", "raw": 5, "centered": 0.95},
     {"construct": "schwartz-values/universalism-tolerance", "raw": 4.33, "centered": 0.28}]}],
 "validityFlags": [], "source": "src-1",
 "origin": "derived", "derivedFrom": ["src-1"],
 "generatedBy": {"software": "values-scorer", "version": "1.2.0", "method": "public PVQ-RR scoring: mean of the three items of each of the 19 values; centred by subtracting the person's mean over all 57 items"},
 "importedFrom": {"system": "values-scorer", "systemVersion": "1.2.0", "importedAt": "2026-09-15T08:00:00Z", "run": "e-1"},
 "formulatedAt": "2026-09-14T20:30:00Z", "reviewAfter": "P3Y", "assertedBy": "subject",
 "recordedAt": "2026-09-15T08:00:00Z", "sensitivity": "special", "categories": ["belief", "political"],
 "handling": ["no-infer", "no-leverage"], "synthetic": true}
```

- `instrument.id` MUST be `urn:ohc:instrument:pvq-rr` (AR-8); `form` is `"57"`; `lensVariant` is `"19"`.
- **The 19 construct ids** are the descriptor's own: `self-direction-thought`, `self-direction-action`, `stimulation`, `hedonism`, `achievement`, `power-dominance`, `power-resources`, `face`, `security-personal`, `security-societal`, `tradition`, `conformity-rules`, `conformity-interpersonal`, `humility`, `benevolence-caring`, `benevolence-dependability`, `universalism-concern`, `universalism-nature`, `universalism-tolerance`, each prefixed with `schwartz-values/`. Store all 19; if items were skipped, keep the values that could be scored and add the validity flag `incomplete`.
- **The two numbers.** `raw` is the person's mean rating for the value on the 1-to-6 scale (the mean of its three items). The person's mean is the mean of all 57 ratings; because every value has three items, it equals the mean of the 19 unrounded `raw` values. `centered` is the unrounded `raw` minus the unrounded person's mean. Round both numbers to two decimals only at the end. (In the example, the person's mean is 4.0526…, so `raw` 5.67 has `centered` 1.61.)
- Higher-order scores (`schwartz-values/openness-to-change` and the other three) are added only if the scoring tool computes them, with the rule named in `generatedBy.method`.
- `mode: "self-report-instrument"` requires `origin: "derived"` (or `imported` for a copied report), with `derivedFrom` and `generatedBy.method` (AR-1, §6.1).
- Give no `normGroup` and no `trademarkNotice`: centred scores are within one person (M-5), and the lens lists no marks.
- `validityFlags`: add `incomplete` if items were skipped, `translated-form` for a translated version.

**Variant "scored by hand".** The same record as `as-1` above, with these changes only:

- leave out `importedFrom`;
- `"generatedBy": {"software": "by hand", "method": "<the same rule as above>"}`;
- `formulatedAt` is when the person finished scoring; `recordedAt` is when they entered it.

Everything else stays: `lensVariant`, `instrument`, `mode`, `assessedBy`, `administeredAt`, `results`, `validityFlags`, `source`, `origin: "derived"`, `derivedFrom`, `reviewAfter`, `assertedBy`, `sensitivity`, `categories`, `handling`. The full record is `as-1` in the by-hand file. It is active at once.

**Who sees it by default:** only the person. An imported profile stays `proposed`, and is served to no one, until the person's Review (step 4a); a profile scored by hand is active at once. Tier `special`, audience `named`.

### Step 4. What the person accepts: Reviews, declared-value Claims and Tension

**4a. The person decides on the import.** Show the profile with its meaning: centred scores, and which values are neighbours or opposites. The person then writes Reviews (schema `review.schema.json`, array `reviews`):

```json
{"id": "rv-1", "target": "la-1", "action": "admit", "by": "subject", "recordedAt": "2026-09-15T20:00:00Z"}
```

```json
{"id": "rv-2", "target": "as-1", "action": "partially-endorse", "by": "subject",
 "recordedAt": "2026-09-15T20:05:00Z",
 "endorsedPart": "Self-direction and caring for the people close to me come first. I do not see myself as low on tradition."}
```

- `endorse` accepts the whole profile and `partially-endorse` accepts part of it in the person's words (`endorsedPart`); both also admit the record (RV-3). `reject` says it does not fit: on a proposed record it also declines it, and it is never served. `decline` leaves it not admitted. Only the person may decide, because the record is special (R-A1).

**Variant "scored by hand".** Nothing needs admitting. A Review is optional: `endorse` or `partially-endorse` with `endorsedPart` if the person wants to say what fits.

**4b. The person says what matters to them.** Separately, and in their own words, write Claims with facet `declared-value` (schema `claim.schema.json`, array `claims`):

```json
{"id": "c-1", "facet": "declared-value", "predicate": "priority",
 "text": "Choosing my own way of working matters to me.", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-21T09:00:00Z", "horizon": "foundation", "contexts": ["work"], "sensitivity": "sensitive",
 "synthetic": true}
```

```json
{"id": "c-2", "facet": "declared-value", "predicate": "priority",
 "text": "A steady income matters to me; I do not want to count every month.", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-09-21T09:02:00Z", "horizon": "foundation", "contexts": ["money"],
 "sensitivity": "sensitive", "synthetic": true}
```

- `origin` is always `"declared"` and `assertedBy` is always `"subject"`. Never `derivedFrom` or `evidence` pointing at the AssessmentRecord, and never a value name copied from the profile as the person's declaration.
- A declared value that rests on a coach's notes may cite them: `{"ref": "src-4", "kind": "practitioner"}`, and then it is `special` with `["belief", "political"]`, like the notes (the Claim `c-3` in the coach-notes file).
- Raise `sensitivity` to `"special"` and add the category `belief` or `political` when the person's words touch religion, philosophy or politics.

**4c. Values that pull against each other** are a Tension between declared values (schema `tension.schema.json`, array `tensions`). The person decides it, or holds it as it is:

```json
{"id": "t-1", "between": ["c-1", "c-2"], "tensionKind": "value-conflict", "whoDecides": "subject",
 "text": "Freedom in how I work pulls against a steady income.", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-21T09:05:00Z", "sensitivity": "sensitive", "synthetic": true}
```

**Who sees it by default:** only the person. The declared values are `sensitive` with audience `named`: a grant must name them by id, kind, facet or category.

### Step 5. Values in a decision: Episode and Interpretation

This is the toolkit item `schwartz-values.values-in-tension`: the person takes a recent decision and notes which two values pulled against each other and what they chose. The decision is an Episode (schema `episode.schema.json`, array `episodes`); the reading is an Interpretation (schema `interpretation.schema.json`, array `interpretations`):

```json
{"id": "ep-1", "occurred": {"start": "2026-09-18", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-18T21:00:00Z", "addedAt": "2026-09-18T21:05:00Z", "accountKind": "in-the-moment", "happened": "I turned down a permanent position in another city and stayed freelance.", "didOrTried": "Called back the same day and asked to stay in touch for project work.", "understandingThen": "The timing is wrong while I am helping my father move to a new flat."}],
 "selection": {"selectedBy": "subject", "reason": "subject-chose"}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-18T21:05:00Z", "contexts": ["work", "family"], "sensitivity": "sensitive",
 "synthetic": true}
```

```json
{"id": "in-1", "about": ["ep-1"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:schwartz-values", "version": "0.2.0"},
 "text": "Security pulled against self-direction. I chose self-direction; being close to my family tipped it.",
 "alternatives": [{"text": "The salary offered was below what I earned freelance this year.", "kind": "external"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-21T09:10:00Z",
 "heldDuring": {"from": "2026-09-21"}, "contexts": ["work", "family"], "sensitivity": "special",
 "categories": ["belief", "political"], "synthetic": true}
```

- Only the person writes the reading here (`assertedBy: "subject"`). An agent may offer the exercise and ask the descriptor's questions ("Which values pulled against each other here?", "Which value would you not give up in this situation?"), but an agent's reading through this lens fails I5 while the person's adoption has `agentInterpretation: off`.
- The two values are named in `text`; there is no structured field for them yet (section 6).
- Describe only the person. The Episode may mention other people as participants, never their inner states, traits or beliefs (TP-1).
- Ask for at least one alternative that is not psychological (`situational`, `physiological`, `informational` or `external`), so that a decision is not explained by values alone.

**Who sees it by default:** only the person. The Interpretation is `special` because it names a lens (I9).

### Step 6. Practices and outcomes: Practice and Outcome

The exercise can become a habit, which is a Practice (schema `practice.schema.json`, array `practices`); how it went is an Outcome (schema `outcome.schema.json`, array `outcomes`):

```json
{"id": "pr-1", "name": "Name the two values before deciding",
 "description": "Before a bigger decision, write which two values pull against each other and what I give up with each choice.",
 "practiceKind": "writing",
 "source": {"route": "from-lens", "lens": "urn:ohc:lens:schwartz-values", "templateId": "schwartz-values.values-in-tension"},
 "steps": ["Write the decision in one line", "Name the two values pulling against each other", "Write what I choose and what I give up"],
 "duration": "PT15M", "limits": "Not for small daily choices.", "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-21T09:20:00Z", "sensitivity": "special",
 "categories": ["belief", "political"], "synthetic": true}
```

```json
{"id": "oc-1", "about": {"practice": "pr-1"}, "result": "helped", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-10-06T19:00:00Z", "note": "Used it before answering a second offer; the choice felt clear.",
 "synthetic": true}
```

- An Outcome written by anyone other than the person is only an "agent's estimate" (O-1).

**Variant "agent-offered": the agent offers the exercise.** An agent may offer only `schwartz-values.values-in-tension` (`agentMayOffer: true`). Three records, all in the by-hand file. (1) The person gives the agent a grant to suggest, whose scope names the lens and excludes the profile, so that the agent that offers exercises never sees it (array `grants`):

```json
{"id": "g-0", "recordedAt": "2026-09-16T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:schwartz-values"]}], "exclude": [{"ids": ["as-1"]}]},
 "actions": ["suggest"], "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2027-03-14T00:00:00Z", "storage": "session", "forwarding": false, "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-16T09:00:00Z", "channel": "holder-ui"},
 "note": "The companion may suggest the values-in-tension exercise; it never sees my profile."}
```

(2) The agent writes the Practice under that grant:

```json
{"id": "pr-2", "name": "Two values before a bigger choice",
 "description": "Before a bigger decision, name the two values that pull against each other.",
 "practiceKind": "writing",
 "source": {"route": "from-agent", "lens": "urn:ohc:lens:schwartz-values", "templateId": "schwartz-values.values-in-tension", "by": "a-01"},
 "steps": ["Write the decision in one line", "Name the two values pulling against each other"],
 "limits": "Not for small daily choices.", "initialStatus": "candidate", "nonClinical": true,
 "origin": "observed", "assertedBy": "a-01", "underGrant": "g-0", "purpose": "self-reflection",
 "recordedAt": "2026-09-16T09:10:00Z", "sensitivity": "special", "categories": ["belief", "political"], "synthetic": true}
```

(3) The person admits it:

```json
{"id": "rv-2", "target": "pr-2", "action": "admit", "by": "subject", "recordedAt": "2026-09-16T09:40:00Z"}
```

- `purpose` on the Practice MUST be one of the grant's `purposes` (INF-1). The scope MUST name the lens with `{"lenses": [...]}`; a wildcard such as `{"all": true}` does not count, and INF-1 fails. The grant needs only `suggest`.
- `initialStatus` is `"candidate"`: the person has not tried it yet. `origin` is `"observed"` and `assertedBy` and `source.by` are the agent (`"declared"` fails ENV-2).
- Until the person's `admit`, the Practice and its Outcomes are withheld from every grantee (PC-1; verified with the projection tool). After it, grantees see the Practice labelled `observed` (section 6).
- An agent never offers `schwartz-values.record-result` (PC-2).

**Who sees it by default:** only the person.

### Step 7. Who may see what: Grant

The person lets a reflection companion read their values records (schema `grant.schema.json`, array `grants`):

```json
{"id": "g-1", "recordedAt": "2026-09-22T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:schwartz-values"]}, {"ids": ["c-1", "c-2", "t-1", "oc-1"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2027-03-20T00:00:00Z", "storage": "session", "forwarding": false, "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-22T09:00:00Z", "channel": "holder-ui"},
 "note": "For reflection on my own decisions; never to persuade me."}
```

- The selector `{"lenses": [...]}` reaches the adoption, the profile, the reading and the Practice. The declared values, the Tension and the Outcome do not name a lens; add them by `ids`.
- `actions: ["read"]` only: the companion may not propose records (no `suggest`), and could not infer through this lens anyway.
- `basis.legal` MUST be `explicit-consent`; `expiresAt` is at most 180 days after `recordedAt` (GR-1). `purposes` never include a prohibited purpose (section 4).
- Handling travels with each record: the grantee receives `no-infer` and `no-leverage` in `obligations.handling` and must keep them (C-4, C-6).
- The grantee sees the profile labelled "partly confirmed", but not the person's `endorsedPart` (section 6). If that matters, the person can repeat it in their own words as a declared-value Claim.

**What this grantee receives.** Run the projection the grantee would get:

```sh
python3 -B tools/ohc_query.py <your context directory> project --grant g-1 --purpose self-reflection --now latest
```

`--purpose` is one of the grant's `purposes`; `--now latest` evaluates at the newest time in the context. **For a real person's context** (no `synthetic`), also pass `--holder-key-file <file>`, a file holding the holder's secret key (K_holder, §12.3 step 11); without it the tool stops with "--holder-key-file is required: this context is not marked synthetic". For the worked example it serves `la-1`, `as-1`, `c-1`, `c-2` and `pr-1` under `statements`, `in-1` and `t-1` under `interpretations`, and `oc-1` under `recall`; not `ep-1`, `src-1`, `e-1` or the Reviews.

### Step 8. Check

```sh
python3 -B tools/check.py <your context directory> --level L1 --json
```

Expect `"valid": true` and `"levelMet": "L1"`, then run the projection command of step 7 for each grant. The checker does not verify everything this recipe asks for. Check these by hand:

- every construct id is one of the descriptor's `constructs`, and a 19-value profile has all 19 or the flag `incomplete`;
- `centered` equals `raw` minus the person's mean for every value, allowing a difference of 0.01 from rounding (in the example, 4.67 − 0.61 = 4.06 while the mean is 4.05);
- every `declared-value` Claim is `declared` by the subject and does not cite the AssessmentRecord;
- every record of one import has the same `importedFrom.run`, that id is the import-run Event, and the Event's `records` list them;
- no record holds item text, a norm group or a guess about the person's views.

## 4. Never

- **Prohibited purposes.** Never use any record of this lens for `personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting`, `political-profiling` or any other prohibited purpose (§8.10), under any grant. A result grounds a choice you propose for the person only under `decisionUse: approval-required`, only when the person accepted it, naming what you weighed (R-G14).
- **No inference of views.** Never infer or suggest political or religious views from values, from the profile or from anything the person wrote.
- **No persuasion.** Never use values to tailor a message, an offer or an argument to the person; value profiles are a known input for psychological targeting.
- **No conversion.** Never turn the measured profile into declared values, or declared values into a profile.
- **No comparisons.** Never compare the person's values with other people's or with a population, and never map them to another lens (`crossLensMapping: not-allowed`).
- **No agent inference unless the person allows it.** An estimate of the profile or a reading through the lens exists only under the person's Grant (`suggest` and `infer` naming the lens; I5 for readings), as a person-only proposal (AR-2); and never political or religious views.
- **No judgement.** Speak of priorities and trade-offs, never of right or wrong values.

## 5. Worked example

[examples/schwartz-values/context.json](examples/schwartz-values/context.json) is a single-document context about Odile, who is fictional. It contains exactly the records of the main path of section 3: `e-1`, `la-1`, `src-1`, `as-1`, `rv-1`, `rv-2`, `c-1`, `c-2`, `t-1`, `ep-1`, `in-1`, `pr-1`, `oc-1` and `g-1`, with two Parties and the pinned descriptor. Odile scored her questionnaire with a tool; the import is proposed until she admits the adoption and partly endorses the profile; she then says in her own words what matters to her, notes the tension between two of her values, reads a recent decision through the lens, and lets a reflection companion read these records, never to persuade her.

```sh
python3 -B tools/check.py docs/lenses/examples/schwartz-values --level L1 --json
```

It reports `"valid": true`, `"levelMet": "L1"`, no errors and no warnings. Its output equals [examples/schwartz-values/expected-check.json](examples/schwartz-values/expected-check.json).

The variants of section 3 are in two more contexts about the same fictional Odile. Each passes the same way (`"valid": true`, `"levelMet": "L1"`, no errors, no warnings):

| Variant | File | Records |
|---|---|---|
| scored by hand, another questionnaire, agent-offered practice | [variants/by-hand/context.json](examples/schwartz-values/variants/by-hand/context.json) | `g-0`, `la-1`, `src-1`, `src-2`, `as-1`, `c-1`, `pr-2`, `rv-2` |
| coach's notes | [variants/coach-notes/context.json](examples/schwartz-values/variants/coach-notes/context.json) | `src-3`, `la-1`, `src-4`, `c-3` |

```sh
python3 -B tools/check.py docs/lenses/examples/schwartz-values/variants/by-hand --level L1 --json
python3 -B tools/check.py docs/lenses/examples/schwartz-values/variants/coach-notes --level L1 --json
```

No result, report, release or notes file is shipped; with the file absent, the checker checks only the Source record (step 2).

## 6. What does not fit yet

These are gaps in OHC 0.1 for this lens. They are collected for the next pass of the standard.

1. **The profile has no scale.** A `values-profile` score has `raw` and `centered` but no range, so the 1-to-6 scale lives only in the instrument entry's free-text note. Proposal: an optional `rawRange` on `values-profile` results.
2. **Only one instrument, and none for the 10-value variant.** The descriptor has variants `10` and `19`, but only PVQ-RR is listed; results of shorter or older value questionnaires fail AR-8 and can be kept only as Sources. Proposal: instrument entries for the other published forms after a licence review, or a general way to record an unlisted instrument with a validity flag.
3. **"A measured profile is not a declared value" is not checked.** A `declared-value` Claim with `origin: derived` and `derivedFrom` pointing at the profile passes the checker (verified). Proposal: a rule like CL-3 for `declared-value`: `origin: declared`, asserted by the subject, with no `derivedFrom` or `evidence` that reaches an AssessmentRecord.
4. **A partial endorsement does not travel.** The person's `endorsedPart` stays in the Review (G3); a grantee receives the whole profile labelled "partly confirmed" without knowing which part the person rejects (verified with the projection tool). Proposal: serve the subject's `endorsedPart` in `derived` for that record, or let a Review endorse or reject single results.
5. **A reading cannot name the values it is about.** An Interpretation from the values-in-tension exercise names its two values only in `text`, and a `value-conflict` Tension links Claims, not lens constructs. Proposal: an optional `constructs` list (construct ids of the cited lens) on Interpretation and Practice.
6. **`importedFrom.run` is never resolved.** LA-5 links an `imported` adoption and its results through `importedFrom.run`. A single document may carry the import-run Event in `events` (as the worked example does), yet a `run` pointing at a missing Event (`e-9`) or at an Event of another type (`backup-created`) passes the checker (verified); LA-5 grouping therefore rests on an unchecked string, and without a `run` LA-5 silently does not apply and the result is active at once. Proposal: when `events` is present, `importedFrom.run` MUST resolve to an Event with `eventType: import-run` whose `records` include the record; when `events` is absent, a warning; and a warning when an `imported` adoption has no `run`.
7. **Record use limits are not checked against the lens.** *Resolved in 0.1.0-draft.2:* records carry no `useLimits`; the prohibited purposes bind every grantee (§8.10), and no grant licenses deriving political views (C-7).
8. **The default categories leave no room to choose.** Every record carries `belief` and `political`, so excluding `political` from a grant removes everything, including a practice that reveals nothing political. Proposal: keep `special` for the lens, and move `belief` and `political` to `perConstruct` for the values the descriptor's risk notes name (Tradition, Universalism, Conformity), with per-result categories as proposed for other ranked lenses.
9. **`therapy-confidential` does not reach the person's own records.** LA-4 propagates only to records that cite the adoption, and the profile, readings and practices do not cite it. Proposal: apply LA-4 to every record whose `lens` or `source.lens` is the adopted lens.
10. **The origin of what an agent writes on the person's behalf is not stated.** An agent-written `agent-suggested` adoption and a Practice with `source.route: from-agent` cannot be `declared` (ENV-2); `observed` passes but is documented nowhere. Proposal: state it in §10.5, §17.1 and CONTEXT-08.
11. **A LensAdoption gates nothing.** A context with lens results, lens readings and from-lens Practices but no LensAdoption passes L1; results pass when the adoption's `uses` lack `store-results`, and when they were recorded before the adoption; while an `agent-suggested` or `imported` adoption is still `proposed`, a lens selector already serves the person's results, readings and Practices in that lens (verified). `uses` has no normative effect; §10.5 gives `uses` no rule. Proposal: a rule LA-8: a record with `lens` or `source.lens` by a non-subject author requires an adoption of that lens that is active at its `recordedAt` and whose `uses` include the matching use (`store-results`, `interpret`, `offer-practices`); a warning for the subject's own lens records with no active adoption; and a projection that withholds lens records while the adoption is `proposed` or `paused`.
12. **An agent-offered Practice reaches grantees labelled "observed".** After the person's `admit`, a Practice with `source.route: from-agent` is served with the derived `label: observed` and `endorsement: not-asked` (verified with the projection tool); the same holds for an admitted `agent-suggested` adoption. The grantee sees the agent's suggestion presented as an observation about the person, and cannot see that the person admitted it. Proposal: derive `label: suggested` for these records, and `endorsement: admitted` once a subject `admit` Review exists; or add an origin `suggested` instead of reusing `observed`.
13. **`lensVariant` and profile completeness are not checked.** An AssessmentRecord with `lensVariant: "10"` and 19 values-profile constructs passes, and so does a 19-variant profile with only 10 of 19 scores and no `incomplete` flag (verified). Scores centred on a partial profile mean something different, yet nothing tells the reader. Proposal: let descriptor variants list their construct sets; add a checker rule: result constructs ⊆ the variant's set, and a values-profile with fewer constructs than the variant requires has `validityFlags` ⊇ `["incomplete"]`.
14. **The centring rule has no stored anchor and no tolerance.** `centered` is `raw` minus the person's mean, but the mean is stored nowhere; with two-decimal rounding a correct profile is inconsistent by up to 0.01 (4.67 − 0.61 = 4.06 against a mean of 4.05 in the worked example), and any `centered` value passes the checker (`centered` 3.0 against `raw` 4.67 passes; verified). Proposal: an optional `personMean` on values-profile results; define centring on unrounded values with an equality tolerance of 0.01; a checker rule comparing `centered` with `raw − personMean`.
15. **A Source cannot name the lens it belongs to.** The recipe keeps a non-catalog values questionnaire "only as a Source", but a Source has no `lens` field, so lens selectors, the lens defaults (`special`, `belief`, `political`) and the propagation proposed in item 9 never reach it, and the person cannot tie it to the lens. Proposal: an optional `lens` (LensRef) on Source; lens selectors then reach it at its `maxRelease` tier, and lens default categories apply to it.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
