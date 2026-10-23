# Lens recipe: Enneagram (nine motivational patterns)

**Recipe · lens `urn:ohc:lens:enneagram` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe shows, step by step, how what a person knows about their own Enneagram pattern (their own recognition, a test report they own, or a typing interview) becomes OHC records that the person controls.

The lens descriptor is [spec/lenses/enneagram.lens.json](../../spec/lenses/enneagram.lens.json): `descriptorStatus: draft`, kind `type-categorical`, measurement tier `T4` (contested), ontological status `theoretical-model`. The lens supports self-reflection on recurring motivations and a shared vocabulary the person chose. It does not establish that nine distinct types exist, any diagnosis, or job fit. Read the descriptor's `mentalModel` before you start: the person's own recognition matters more than any score.

The record shapes are in [SPECIFICATION.md](../../spec/SPECIFICATION.md) §10.5 (LensAdoption), §10.6 (AssessmentRecord), §10.3 (Interpretation), §17 (Practice, Outcome) and §12 (Grant); the schemas are in [spec/schema/](../../spec/schema/). The lens rules are in [LENSES.md](../../spec/LENSES.md).

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them.

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:enneagram-basic`](../../spec/playbooks/enneagram-basic.playbook.json) (Enneagram: basic ways of working, by the OHC editors), for these situations: under strain: tired, pressed or overloaded; looking back at something that happened; preparing a hard conversation; choosing between options. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

**Bringing a report through the person's window.** When an instrument's catalog entry carries an `import` block, a person can bring its result through their own window ([guide](../guides/BRING-A-RESULT.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). No entry of this lens has one yet, so the steps below record the report by hand.

## 1. What you may have

| Input | Use it? | Where it goes |
|---|---|---|
| The person's own recognition, said in conversation ("I see myself in pattern 4, mostly under pressure") | Yes | AssessmentRecord with `mode: self-identified` (step 3a), a Claim in their words (step 4) |
| A report from an instrument the person took and owns. RHETI® v2.5 is the only Enneagram instrument in the 0.1 catalog | Yes | Source (step 2) and AssessmentRecord with `mode: vendor-report-import` (step 3b) |
| A result from any other Enneagram test (free online tests, questionnaires of other schools) | Only as the person's own identification | Source (step 2, variant "unlisted test") and AssessmentRecord with `mode: self-identified` (step 3a, variant); never as an instrument result, because the checker rejects an instrument the lens does not list (AR-8) |
| Notes or a result from a typing interview with a coach, teacher or facilitator | Yes, with the practitioner's written release | Route `inherited-from-practice` (step 1, variant), release and notes Sources (step 2, variant) and AssessmentRecord with `mode: practitioner-facilitated` (step 3c) |
| The person's own accounts of episodes and their own readings of them through the lens | Yes | Episode and Interpretation (step 5) |
| An agent's reading ("from the way you write, you seem to be a type 8") | **Only under the person's Grant** | An Interpretation by the agent needs `suggest` and `infer` naming the lens, and the person's active adoption not set to `off` (I5). The descriptor's guidance: never type the person, and never present type descriptions as facts about them. In the example the person allows none. |

## 2. Before you start

### 2.1 Route of adoption

Choose one route with the person. It decides who writes the LensAdoption and when it becomes active. Step 1 has a complete record for each route that the worked examples use.

| Route | When | What it changes |
|---|---|---|
| `self-chosen` | The person picks the lens themselves. | The person writes the adoption: `assertedBy: "subject"`, `origin: "declared"`. It is active at once. This is the route of the worked example. |
| `agent-suggested` | The person asked an agent for ways of looking at recurring motivations (the descriptor's `suggestionRequires`), and accepted the lens the agent offered. | First the person gives the agent a grant with the action `suggest` whose scope names the lens. The agent then writes the adoption under that grant: `suggestedBy` and `assertedBy` are its own Party id, `origin: "observed"` (the agent records that the person accepted; `declared` is refused by ENV-2), `underGrant` is the grant's id and `purpose` is one of the grant's `purposes`. It stays `proposed` until the person writes a Review `admit`. The agent never admits it (LA-1). Records: step 1, variant "agent-suggested". |
| `inherited-from-practice` | The lens comes from the person's coach, teacher or facilitator (the descriptor's `inheritanceRoles`). Use it whenever a typing interview is part of the work. | The coach is a Party with `role: "practitioner"`. The adoption carries a `practice` block. If session material such as typing-interview notes is stored, the practitioner's release is stored first as a Source of kind `practitioner-release`, and its id goes both in the adoption's `practice.releaseRef` (LA-3) and in the notes Source's `custody.releaseRef` (SR-7). `confidentiality: "practitioner-scope"`, `onEnd: "ask"`. The adoption gives the practitioner no access (LA-2); access needs a Grant (step 7). Records: step 1, variant "with a coach". |
| `imported` | An importer tool creates the adoption from an instrument report. | `origin: "derived"`, `derivedFrom` naming the report Source, `generatedBy` naming the tool, and `importedFrom` with a `run` id; each record's `importedFrom.importedAt` equals its own `recordedAt` (ENV-3). The adoption and every AssessmentRecord with the same `importedFrom.run` stay `proposed` until the person admits them (LA-5). The [schwartz-values recipe](schwartz-values.md) shows this route in full. |

In the example `agentInterpretation` is `"off"` on every route, the default the person keeps: only the person writes readings through this lens (I5). The person may change it.

### 2.2 Consent

- An agent speaks in the lens's language once the person adopted it, in the person's own words; it never types the person (`agentPosture`).
- Nothing leaves the context without a Grant (R-G1). Every result in this lens is treated as special category, so a grant that shares it needs `basis.legal: "explicit-consent"`, must name the records by id, by the lens or by the category `mental-health` (R-G3), and lasts at most 180 days (GR-1).
- A practitioner's notes enter the context only with the practitioner's release, stored as its own Source.

### 2.3 Defaults for this lens

| Setting | Value | Why |
|---|---|---|
| `sensitivity` | `"special"` on every record that names the lens (LensAdoption, AssessmentRecord, Interpretation with `lens`, Practice with `source.lens`), on every Source of a report, screenshot, release or notes, and on every Claim or Tension that cites a result | The descriptor's `defaults.sensitivity`; AR-5; I9; propagation rule C3 |
| `categories` | `["mental-health"]` on the same records | The descriptor's `defaults.categories` |
| `handling` on results | `["no-infer", "no-quote-back"]` | `no-infer`: the person keeps the result from every inference and mapping (M-7). `no-quote-back`: nobody presents the type back to the person as a fact about them ("as a 4, you…"). |
| `reviewAfter` | leave it out | The descriptor's default is `on-change`, which the AssessmentRecord field cannot hold (section 6) |
| Source `maxRelease` | `"index"` | A grantee never receives the report's bytes, title or text |

### 2.4 What is never stored

- RHETI® item text, item responses, scoring keys and report prose (AR-3; the instrument entry's `neverStore`). The report file may sit in the person's own vault; no record quotes it.
- The descriptive type names that a school or a vendor gives each type. Construct labels are `Type 1` … `Type 9` only (the descriptor's `ip.restrictions`).
- The name of an unlisted test, in any field.
- A type label produced from another lens's result, for example from Big Five scores (M-4).
- Descriptions of "core fears" or of what a type "needs", written as facts about the person.
- A score or a type as a judgement of the person ("she is a 9"). A result is a dated, within-person description with its method.

## 3. Steps

Snippets are records from the worked examples (section 5) and validate against the named schemas. They carry `"synthetic": true` because they are examples. Use opaque ids (`as-1`, never `as-type4`; W-ID1). Times are RFC 3339 with an offset.

**Set up the context once.** Create a directory for the context (the *context directory*) and save this skeleton in it as `context.json`. Each step below names the array its record goes in; inside an array, the order of records does not matter.

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:ohc:example:linnea:context", "version": "2026-10-10.1",
 "subject": {"id": "urn:ohc:example:linnea", "displayName": "Linnea (fictional)"},
 "holder": "subject", "lang": "en", "created": "2026-09-24T22:05:00Z",
 "conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
 "parties": [
   {"id": "s-01", "partyKind": "software", "label": "Online test report"},
   {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}],
 "policy": {"admission": "subject-only", "resolver": "returnDialog"},
 "lenses": [{"id": "urn:ohc:lens:enneagram", "version": "0.2.0",
             "sha256": "1c22298a0fb2bc26f272a35d5382eefb026585597aa3020279ea1078e2c99a3b"}],
 "lensAdoptions": [], "sources": [], "assessments": [], "tensions": [], "claims": [], "reviews": [],
 "episodes": [], "interpretations": [], "practices": [], "outcomes": [], "grants": [],
 "synthetic": true}
```

- `format`, `specVersion`, `id`, `version` and `subject` are required (`context.schema.json`). `holder`, `lang`, `created` and `policy` are optional; keep them as shown. Arrays you do not use may be left out.
- `"synthetic": true` marks an example. In an example it MUST be on the context root and on every content record, or the check fails with CX-8. **For a real person**, give `id` and `subject.id` the form `urn:uuid:<a new UUID>`, and leave out `synthetic` at the root and on every record.
- `lenses[].sha256` is the SHA-256 of the descriptor file's bytes: `shasum -a 256 spec/lenses/enneagram.lens.json`.
- `governance` is needed for Grants (steps 1 and 7), `practices` for Practice and Outcome (step 6).
- Every Party you reference goes in `parties` (CX-3). The main path uses `s-01` and `a-01`. The variant "unlisted test" adds `{"id": "s-02", "partyKind": "software", "label": "Online test site"}`; the variant "with a coach" needs `{"id": "p-01", "partyKind": "person", "label": "Coach", "role": "practitioner"}`.
- The check passes only once the context holds a Claim or an Episode with an account (LV-0); before step 4 it reports LV-0.

### Step 1. The person adopts the lens: LensAdoption

The person says they want to look at themselves through the Enneagram. Write one LensAdoption (schema `lens-adoption.schema.json`, array `lensAdoptions`):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"}, "route": "self-chosen",
 "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"], "interpretationAuthors": ["subject"],
 "agentInterpretation": "off", "representationPreference": "enneagram.type-label", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-10-01T19:00:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- Choose `uses` with the person: `speak-in-lens` (an agent may use pattern words), `store-results`, `interpret` (the person's own readings), `offer-practices` (an agent may offer `enneagram.recognition`, the only toolkit item with `agentMayOffer: true`), `recall`.
- If a typing interview with a practitioner is part of the work, use the route `inherited-from-practice` now (variant "with a coach" below). This is recommended; the checker does not require it (section 6).

**Variant "agent-suggested": the agent offered the lens.** Write three records in this order. All three are in [examples/enneagram/variants/with-agent/context.json](examples/enneagram/variants/with-agent/context.json).

(1) The person gives the agent a grant to suggest (array `grants`):

```json
{"id": "g-0", "recordedAt": "2026-09-29T10:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:enneagram"]}], "exclude": [{"ids": ["as-4"]}]},
 "actions": ["suggest"], "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2027-03-27T00:00:00Z", "storage": "session", "forwarding": false, "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-29T10:00:00Z", "channel": "holder-ui"},
 "note": "The companion may suggest this lens and its recognition exercise; it never sees my results."}
```

(2) The agent writes the adoption under that grant (array `lensAdoptions`):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"}, "route": "agent-suggested",
 "suggestedBy": "a-01", "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "representationPreference": "enneagram.type-label", "origin": "observed", "assertedBy": "a-01",
 "underGrant": "g-0", "purpose": "self-reflection", "recordedAt": "2026-09-29T10:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

(3) The person admits it (array `reviews`):

```json
{"id": "rv-1", "target": "la-1", "action": "admit", "by": "subject", "recordedAt": "2026-09-29T10:10:00Z"}
```

- `purpose` on the adoption MUST be one of the grant's `purposes`; otherwise INF-1 fails.
- The grant's scope MUST name the lens with `{"lenses": [...]}`. A wildcard such as `{"all": true}` does not count, and INF-1 fails.
- The grant needs only the action `suggest`. Its `exclude` lists the ids of the person's results (here `as-4`, step 3a), so that the suggesting agent never sees them; an id may be listed before its record exists.
- `origin` is `"observed"`: the agent records that the person accepted. `"declared"` fails ENV-2 (section 6).
- Until the person's `admit`, the adoption is `proposed` and no grantee receives it. Only the person writes the `admit` (LA-1).
- The same grant also covers the agent's offer of a practice (step 6, variant).

**Variant "with a coach": the lens comes from a practitioner.** Add the coach's Party `p-01` to `parties`, write the release Source (step 2, variant), then this adoption, then the notes Source. All are in [examples/enneagram/variants/with-coach/context.json](examples/enneagram/variants/with-coach/context.json).

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"}, "route": "inherited-from-practice",
 "practice": {"role": "coach", "practitioner": "p-01", "relationship": "active", "since": "2026-08-01", "releaseRef": "src-2"},
 "confidentiality": "practitioner-scope", "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off", "representationPreference": "enneagram.type-label",
 "onEnd": "ask", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-01T19:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- `practice.releaseRef` is the id of the release Source. Put the same id in `custody.releaseRef` of the notes Source (step 2). Without `practice.releaseRef`, LA-3 fails as soon as notes are stored.
- `practice.role` is `coach`, `teacher` or `facilitator` (the descriptor's `adoption.inheritanceRoles`).
- `confidentiality: "practitioner-scope"` and `onEnd: "ask"`: when the relationship ends, the person decides what happens to the adoption.

**Who sees it by default:** only the person. An `agent-suggested` adoption is not served to anyone until the person admits it.

### Step 2. Keep the original: Source

If the person has a report file, a screenshot or a practitioner's notes:

1. compute the file's SHA-256: `shasum -a 256 <file>`;
2. copy the file into the context directory as `vault/<first two hex characters of the hash>/<hash>.<extension>`;
3. write a Source (schema `source.schema.json`, array `sources`) whose `content.locator.vaultPath` is that same path, relative to the context directory and starting with `vault/`.

```json
{"id": "src-1", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/64/64d90261deb72a4b6bf2c0220a75433793731f33d7555598b864f5d6013c1ec9.pdf"}, "sha256": "64d90261deb72a4b6bf2c0220a75433793731f33d7555598b864f5d6013c1ec9", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-28T20:00:00Z", "authorship": {"author": "s-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-01T19:02:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- `authorship.author` is a software Party for a vendor report.
- Give no `title` and no `summary` that repeats report prose.
- When the file is present, the checker reads it and compares its hash with `sha256`; a mismatch fails SR-2. `"vaultContentRead": false` in the checker's report means that the content was not interpreted; the hash is still checked. When the file is absent, as in the worked examples, only the record is checked.

**Variant "unlisted test": a free online test.** Use `sourceKind` `instrument-report` for a downloaded report, or `image` for a screenshot. `authorship.author` is a software Party such as `s-02` ("Online test site"). Never name the test, in `title` or anywhere else.

```json
{"id": "src-4", "sourceKind": "image",
 "content": {"locator": {"vaultPath": "vault/fc/fc16c529b1a721d09ee4596d5d6d92dd0d2fb22ed664fdcb6fef01d0082203d9.png"}, "sha256": "fc16c529b1a721d09ee4596d5d6d92dd0d2fb22ed664fdcb6fef01d0082203d9", "mediaType": "image/png"},
 "capturedAt": "2026-09-30T20:00:00Z", "authorship": {"author": "s-02"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-30T20:05:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

**Variant "with a coach": the release, then the notes.** The release is the practitioner's written permission to keep the notes. Store it first:

```json
{"id": "src-2", "sourceKind": "practitioner-release",
 "content": {"locator": {"vaultPath": "vault/22/22f766eb7183cf2ec7f3e20f0bc59eb224e2f66fdc07a867805208b880b83f74.pdf"}, "sha256": "22f766eb7183cf2ec7f3e20f0bc59eb224e2f66fdc07a867805208b880b83f74", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-30T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-01T18:50:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

Then the typing-interview notes, citing the same release id:

```json
{"id": "src-3", "sourceKind": "practitioner-notes",
 "content": {"locator": {"vaultPath": "vault/b9/b9212fcb20d7a5360968d7106f6030f5f296ce526a63f4eb1afd4450b15d4776.pdf"}, "sha256": "b9212fcb20d7a5360968d7106f6030f5f296ce526a63f4eb1afd4450b15d4776", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-30T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "custody": {"custodian": "p-01", "confidentiality": "coaching", "releaseRef": "src-2"},
 "maxRelease": "index", "retention": {"eraseOnRequest": true}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-10-01T19:02:00Z", "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- The release id `src-2` appears twice: in `custody.releaseRef` here (SR-7) and in the adoption's `practice.releaseRef` (step 1; LA-3).

**Who sees it by default:** only the person, at every tier (V-0). A grantee can receive at most the `index` tier: kind, media type and day, never the bytes or a title.

### Step 3. Record the results: AssessmentRecord

Write one AssessmentRecord per way the result was reached (schema `assessment-record.schema.json`, array `assessments`). Construct ids come from the descriptor's `constructs`: `enneagram/type-1` … `enneagram/type-9`, `enneagram/wing`, `enneagram/instinctual-variant`.

**3a. The person's own recognition** (the toolkit item `enneagram.recognition`: the person reads neutral descriptions of the nine patterns and says which ones they recognise, and when):

```json
{"id": "as-1", "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"}, "mode": "self-identified",
 "assessedBy": "subject", "administeredAt": {"start": "2026-10-01", "precision": "day"},
 "results": [
   {"type": "type-assignment", "construct": "enneagram/type-4", "label": "Type 4", "method": "self-identified", "alternatives": ["enneagram/type-9"]},
   {"type": "type-assignment", "construct": "enneagram/wing", "label": "Wing: type 5", "method": "self-identified"}],
 "validityFlags": ["self-identified-only"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-01T19:05:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "handling": ["no-infer", "no-quote-back"], "synthetic": true}
```

- `origin` is `declared` for `self-identified` (AR-1). There is no `instrument`.
- `alternatives` lists other patterns the person also recognises.
- A wing goes in a second `type-assignment` with `construct: "enneagram/wing"`; the neighbouring type can only be named in `label` (section 6). Leave instinctual variants out, or name them only in a Claim in the person's words (section 6).

**Variant "unlisted test".** A result of a free online test is written exactly like 3a, with `"source"` naming its Source (step 2, variant) and no `instrument`:

```json
{"id": "as-4", "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"}, "mode": "self-identified",
 "assessedBy": "subject", "administeredAt": {"start": "2026-09-30", "precision": "day"},
 "results": [{"type": "type-assignment", "construct": "enneagram/type-4", "label": "Type 4", "method": "self-identified"}],
 "validityFlags": ["self-identified-only"], "source": "src-4",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-30T20:10:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "handling": ["no-infer", "no-quote-back"], "synthetic": true}
```

**3b. A RHETI® v2.5 report the person owns:**

```json
{"id": "as-2", "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"},
 "instrument": {"id": "urn:ohc:instrument:rheti-2.5", "version": "2.5", "form": "2.5"},
 "mode": "vendor-report-import", "assessedBy": "subject",
 "administeredAt": {"start": "2026-09-28", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "enneagram/type-1", "label": "Type 1", "raw": 14},
   {"type": "dimension-score", "construct": "enneagram/type-2", "label": "Type 2", "raw": 12},
   {"type": "dimension-score", "construct": "enneagram/type-3", "label": "Type 3", "raw": 9},
   {"type": "dimension-score", "construct": "enneagram/type-4", "label": "Type 4", "raw": 19},
   {"type": "dimension-score", "construct": "enneagram/type-5", "label": "Type 5", "raw": 17},
   {"type": "dimension-score", "construct": "enneagram/type-6", "label": "Type 6", "raw": 13},
   {"type": "dimension-score", "construct": "enneagram/type-7", "label": "Type 7", "raw": 8},
   {"type": "dimension-score", "construct": "enneagram/type-8", "label": "Type 8", "raw": 6},
   {"type": "dimension-score", "construct": "enneagram/type-9", "label": "Type 9", "raw": 21},
   {"type": "type-assignment", "construct": "enneagram/type-9", "label": "Type 9", "method": "instrument"}],
 "validityFlags": ["vendor-algorithm-undisclosed"], "source": "src-1",
 "trademarkNotice": "RHETI® (US Reg. No. 5584848) is a registered mark of Enneagram Personality Types, Inc. (dba The Enneagram Institute). Enneathought and Enneagram Institute are names it uses; their status is not verified here. All are used only to name its products.",
 "origin": "imported",
 "importedFrom": {"system": "vendor report (PDF), scores copied by the person", "importedAt": "2026-10-01T19:10:00Z"},
 "generatedBy": {"software": "vendor scoring (not disclosed)", "method": "main type as stated in the vendor report; the vendor's rule is not disclosed"},
 "formulatedAt": "2026-09-28T20:00:00Z", "assertedBy": "subject", "recordedAt": "2026-10-01T19:10:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-infer", "no-quote-back"],
 "synthetic": true}
```

- `instrument.id` MUST be `urn:ohc:instrument:rheti-2.5` (AR-8).
- `mode: "vendor-report-import"` requires `origin: "imported"` and `importedFrom` (AR-1). `formulatedAt` is when the report was produced; `recordedAt` is when it entered the context (R-T5b).
- `importedFrom.importedAt` equals `recordedAt` (ENV-3). Do not set it to the moment the file was copied.
- Copy the nine type scores as printed in the report into `raw`. Add `rawRange` only if the report states the range. Give no `normGroup`: the scores describe one person and are not normative.
- If the report names a main type, add one `type-assignment` with `method: "instrument"`. `generatedBy.method` is then REQUIRED (AR-6).
- `trademarkNotice` is copied word for word from the `notice` of the `RHETI` mark in [spec/instruments/rheti-2.5.instrument.json](../../spec/instruments/rheti-2.5.instrument.json).
- If the person ran an importer tool instead of copying by hand, keep `assertedBy: "subject"`; if the tool also wrote an `imported` adoption, both stay `proposed` until the person admits them (LA-5).

**3c. Variant "with a coach": a typing interview** (the toolkit item `enneagram.typing-interview`, which requires a practitioner; an agent never offers it). Use the route `inherited-from-practice` (step 1, variant) and the notes Source `src-3` (step 2, variant). The full record:

```json
{"id": "as-3", "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"}, "mode": "practitioner-facilitated",
 "assessedBy": "p-01", "administeredAt": {"start": "2026-09-30", "precision": "day"},
 "results": [{"type": "type-assignment", "construct": "enneagram/type-4", "label": "Type 4", "method": "interview"}],
 "source": "src-3",
 "origin": "declared", "assertedBy": "p-01", "recordedBy": "subject", "recordedAt": "2026-10-01T19:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-infer", "no-quote-back"], "synthetic": true}
```

- No `validityFlags`. `assessedBy` and `assertedBy` are the practitioner; `recordedBy: "subject"`, because the person writes the record into their own context (INF-1 then does not apply).
- Because the asserter is not the person, the record is `proposed`, and no grantee receives it, until the person writes a Review `endorse`, `partially-endorse` or `admit` (R-A1) in `reviews`:

```json
{"id": "rv-3", "target": "as-3", "action": "endorse", "by": "subject", "recordedAt": "2026-10-01T19:20:00Z"}
```

**Who sees results by default:** only the person. Tier `special`, audience `named`.

### Step 4. What the person accepts: Claim, and Tension when results differ

Ask the person what fits, and write only what they say, in their words, as a Claim (schema `claim.schema.json`, array `claims`). Never copy a type description into `text`. Cite the result in `evidence`. The Ground `kind` follows the cited result: `subject-statement` for a 3a result, `instrument` for a 3b result, `practitioner` for a 3c result.

```json
{"id": "c-1", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "Under pressure I go quiet and wait to be noticed instead of asking for what I want.",
 "evidence": [{"ref": "as-1", "kind": "subject-statement"}], "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-10-02T08:00:00Z", "horizon": "foundation", "sensitivity": "special",
 "categories": ["mental-health"], "handling": ["no-quote-back"], "synthetic": true}
```

- In the variant "with a coach", the Claim `c-2` cites `{"ref": "as-3", "kind": "practitioner"}`; see the with-coach file.
- Facet `disposition` requires `origin: "declared"` by the person, or `derived` from an AssessmentRecord (CL-3). Prefer the person's own words (`declared`). A mechanical copy of a result (`origin: "derived"`) needs `derivedFrom` and `generatedBy.method`, and adds nothing the AssessmentRecord does not already hold.
- If the person's recognition and the instrument disagree, keep both records and link them with a Tension (schema `tension.schema.json`, array `tensions`); the disagreement is data (M-8):

```json
{"id": "t-1", "between": ["as-1", "as-2"], "tensionKind": "source-divergence", "whoDecides": "subject",
 "text": "I recognise pattern 4; the test put pattern 9 first. I keep both.", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-10-01T19:15:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- If the person does not recognise a result at all, they write a Review (schema `review.schema.json`, array `reviews`) `{"id": "rv-4", "target": "as-2", "action": "reject", "by": "subject", "recordedAt": "<now>", "reasonCode": "not-true"}`. The record and its evidence stay; grantees stop receiving it. `contest` instead keeps it open for discussion.

**Who sees it by default:** only the person.

### Step 5. Readings of episodes through the lens: Episode and Interpretation

The person tells what happened (an Episode, schema `episode.schema.json`, array `episodes`) and, separately, how they read it through the lens (an Interpretation, schema `interpretation.schema.json`, array `interpretations`):

```json
{"id": "ep-1", "occurred": {"start": "2026-09-24", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-24T22:00:00Z", "addedAt": "2026-09-24T22:05:00Z", "accountKind": "in-the-moment", "happened": "At choir rehearsal the solo I had prepared went to another singer.", "experienced": "Hot face, then flat.", "didOrTried": "Said nothing and left before the last song.", "understandingThen": "My voice was not good enough this week."}],
 "selection": {"selectedBy": "subject", "reason": "subject-chose"}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-24T22:05:00Z", "contexts": ["community"], "sensitivity": "sensitive", "synthetic": true}
```

```json
{"id": "in-1", "about": ["ep-1"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:enneagram", "version": "0.2.0"},
 "text": "This is the pattern I recognise as my 4: I pulled back and waited to be seen instead of asking for the solo.",
 "alternatives": [
   {"text": "I had a cold that week and my voice was weak.", "kind": "physiological"},
   {"text": "The solo list may have been set before the rehearsal.", "kind": "situational"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-02T08:10:00Z",
 "heldDuring": {"from": "2026-10-02"}, "contexts": ["community"], "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- Only the person writes lens readings here. `assertedBy` is `"subject"`; an agent's reading through this lens fails I5 while the person's adoption has `agentInterpretation: off`.
- Readings never go into the Episode (EP-4). A later change of mind is a new Interpretation with `stance: "revision"` and `supersedes`.
- Ask the person for at least one alternative that is not psychological (`situational`, `physiological`, `informational` or `external`). It is required only for non-subject authors (I4), but it keeps the pattern from becoming the only explanation.
- After the adoption, an agent may ask the descriptor's exploratory questions ("Which pattern do you recognise under stress?", "What helps when that pattern is strong?"). The answer is the person's record, not the agent's.

**Who sees it by default:** only the person. The Interpretation is `special` because it names a lens (I9).

### Step 6. Practices and outcomes: Practice and Outcome

A way of acting that the person takes from the lens is a Practice (schema `practice.schema.json`, array `practices`); how it went is an Outcome (schema `outcome.schema.json`, array `outcomes`):

```json
{"id": "pr-1", "name": "Say one sentence before I go quiet",
 "description": "When I notice the pull to withdraw, I name the pattern to myself and say one sentence about what I want.",
 "practiceKind": "reflection",
 "source": {"route": "from-lens", "lens": "urn:ohc:lens:enneagram", "templateId": "enneagram.recognition"},
 "steps": ["Notice the pull to go quiet", "Name it to myself as the pattern", "Say one sentence about what I want"],
 "limits": "Not a rule for every silence; sometimes quiet is what I want.", "initialStatus": "in-use",
 "nonClinical": true, "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-02T08:20:00Z",
 "contexts": ["community"], "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "oc-1", "about": {"practice": "pr-1"}, "result": "partly", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-10-09T21:00:00Z", "note": "Said it once at rehearsal; the second time I still went quiet.",
 "contexts": ["community"], "synthetic": true}
```

- `templateId` is a toolkit item id of the descriptor.
- An Outcome written by anyone other than the person is only an "agent's estimate" (O-1).

**Variant "agent-suggested": the agent offers the recognition exercise.** An agent may offer only `enneagram.recognition` (`agentMayOffer: true`). It needs a grant with `suggest` whose scope names the lens: the grant `g-0` of step 1 (write it now, as shown there, if the adoption took another route). The agent writes the Practice; the person admits it. Both are in the with-agent file.

```json
{"id": "pr-2", "name": "Notice the pattern once a day",
 "description": "Once a day, notice whether the pull to go quiet showed up, without judging it.",
 "practiceKind": "reflection",
 "source": {"route": "from-agent", "lens": "urn:ohc:lens:enneagram", "templateId": "enneagram.recognition", "by": "a-01"},
 "steps": ["At the end of the day, recall one moment", "Note whether the pull to go quiet was there"],
 "limits": "Only while it feels useful; skip any day.", "initialStatus": "candidate", "nonClinical": true,
 "origin": "observed", "assertedBy": "a-01", "underGrant": "g-0", "purpose": "self-reflection",
 "recordedAt": "2026-10-02T09:00:00Z", "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "rv-2", "target": "pr-2", "action": "admit", "by": "subject", "recordedAt": "2026-10-02T09:30:00Z"}
```

- `underGrant` is `g-0`; `purpose` MUST be one of g-0's `purposes` (INF-1). The scope MUST name the lens; a wildcard does not count.
- `initialStatus` is `"candidate"`: the person has not tried it yet. `origin` is `"observed"` and `assertedBy` and `source.by` are the agent (`"declared"` fails ENV-2).
- Until the person's `admit`, the Practice and its Outcomes are withheld from every grantee (PC-1; verified with the projection tool). After it, grantees see the Practice labelled `observed` (section 6).
- An agent never offers `enneagram.typing-interview` or `enneagram.record-instrument-result` (PC-2).

**Who sees it by default:** only the person. The Practice is `special` here because it names the lens; the Outcome takes the tier of its Practice.

### Step 7. Who may see what: Grant

The person decides who receives what. Write a Grant (schema `grant.schema.json`, array `grants`); without one, nothing leaves the context:

```json
{"id": "g-1", "recordedAt": "2026-10-03T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [
    {"lenses": ["urn:ohc:lens:enneagram"]},
    {"ids": ["c-1", "oc-1"]}], "exclude": [{"ids": ["as-2"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2027-03-31T00:00:00Z", "storage": "session", "forwarding": false, "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-10-03T09:00:00Z", "channel": "holder-ui"},
 "note": "Pattern language for reflection; the test scores stay with me."}
```

- The selector `{"lenses": [...]}` reaches every record that names the lens: the adoption, results, readings, and Practices whose `source.lens` names it. Claims and Outcomes do not name a lens; add them by `ids`.
- `exclude` keeps the instrument scores with the person. The Tension `t-1` is then withheld too, without any flag, because one of its members is not served (T3).
- `basis.legal` MUST be `explicit-consent` (special records); `expiresAt` is at most 180 days after `recordedAt` (GR-1). `purposes` never include a prohibited purpose (section 4).
- Handling travels with each record: the grantee receives `no-infer` and `no-quote-back` in `obligations.handling` and must keep them (C-4, C-6). A Grant has no handling field of its own.
- `expressedBy.actor` is `"subject"`. An agent's statement that the person agreed is never consent.

**What this grantee receives.** Run the projection the grantee would get:

```sh
python3 -B tools/ohc_query.py <your context directory> project --grant g-1 --purpose self-reflection --now latest
```

`--purpose` is one of the grant's `purposes`; `--now latest` evaluates at the newest time in the context. **For a real person's context** (no `synthetic`), also pass `--holder-key-file <file>`, a file holding the holder's secret key (K_holder, §12.3 step 11); without it the tool stops with "--holder-key-file is required: this context is not marked synthetic". For the worked example it serves `la-1`, `as-1`, `c-1` and `pr-1` under `statements`, `in-1` under `interpretations`, and `oc-1` under `recall`; not `as-2`, `t-1`, `ep-1` or `src-1`.

### Step 8. Check

```sh
python3 -B tools/check.py <your context directory> --level L1 --json
```

Expect `"valid": true` and `"levelMet": "L1"`, then run the projection command of step 7 for each grant. The checker does not verify everything this recipe asks for. Check these by hand:

- every construct id is one of the descriptor's `constructs`;
- `trademarkNotice` is present on a RHETI® result and absent elsewhere;
- every Ground `kind` matches the cited result (step 4);
- a `practitioner-facilitated` result sits under an `inherited-from-practice` adoption;
- no record contains item text, report prose, a school's type names or the name of an unlisted test;
- no record was written by an agent through the lens beyond what the person's grant and adoption allow.

## 4. Never

- **Prohibited purposes.** Never use any record of this lens for `personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting` or any other prohibited purpose (§8.10), under any grant. A result grounds a choice you propose for the person only under `decisionUse: approval-required`, only when the person accepted it, naming what you weighed (R-G14).
- **No agent typing.** An agent never assigns a type to the person, and never derives one from another lens's scores (M-4). An agent's estimate or reading through the lens exists only under the person's Grant (`suggest` and `infer` naming the lens; I5 for readings), as a person-only proposal (AR-2), never as a type. The mapping to the Big Five is population-level and `unresolved`; it never converts one person's result.
- **No school names as labels.** School-specific type names are vendor labels only, never construct labels, never generic words.
- **RHETI® only for RHETI® results.** Use the mark only to name the genuine instrument, nominatively, with its notice. Never call another test RHETI®.
- **No clinical language.** Never speak about core fears unless the person brings them up; never present a type description as a fact about the person; never present the pattern as a diagnosis.
- **No roles or teams.** Never use a type to suggest roles, tasks or team composition.
- **No typing interview by an agent.** A typing interview belongs with a practitioner; deeper work touching personal history belongs there too.

## 5. Worked example

[examples/enneagram/context.json](examples/enneagram/context.json) is a single-document context about Linnea, who is fictional. It contains exactly the records of the main path of section 3: `la-1`, `src-1`, `as-1`, `as-2`, `t-1`, `c-1`, `ep-1`, `in-1`, `pr-1`, `oc-1` and `g-1`, with two Parties and the pinned descriptor. Linnea recognises pattern 4 with a 5 wing; her RHETI® report puts type 9 first; she keeps both, writes a Tension, and shares the pattern language, but not the scores, with her reflection companion.

```sh
python3 -B tools/check.py docs/lenses/examples/enneagram --level L1 --json
```

It reports `"valid": true`, `"levelMet": "L1"`, no errors and no warnings. Its output equals [examples/enneagram/expected-check.json](examples/enneagram/expected-check.json).

The variants of section 3 are in two more contexts about the same fictional Linnea. Each passes the same way (`"valid": true`, `"levelMet": "L1"`, no errors, no warnings):

| Variant | File | Records |
|---|---|---|
| agent-suggested, unlisted test, agent-offered practice | [variants/with-agent/context.json](examples/enneagram/variants/with-agent/context.json) | `g-0`, `la-1`, `rv-1`, `src-4`, `as-4`, `c-1`, `pr-2`, `rv-2` |
| with a coach | [variants/with-coach/context.json](examples/enneagram/variants/with-coach/context.json) | `la-1`, `src-2`, `src-3`, `as-3`, `rv-3`, `c-2` |

```sh
python3 -B tools/check.py docs/lenses/examples/enneagram/variants/with-agent --level L1 --json
python3 -B tools/check.py docs/lenses/examples/enneagram/variants/with-coach --level L1 --json
```

No report, screenshot or notes file is shipped; with the file absent, the checker checks only the Source record (step 2).

## 6. What does not fit yet

These are gaps in OHC 0.1 for this lens. They are collected for the next pass of the standard.

1. **Wings and instinctual variants have no structured form.** `enneagram/wing` is one construct without a value, so the neighbouring type survives only in the free `label`; instinctual variants have no codes at all. Proposal: a `role` field (`main`, `wing`, `instinctual-variant`) on `type-assignment` results, and OHC-worded constructs `enneagram/instinct/self-preservation`, `enneagram/instinct/social` and `enneagram/instinct/one-to-one` under `enneagram/instinctual-variant`.
2. **"Under stress" and "at ease" cannot be recorded.** The descriptor attends to patterns under stress and at ease, but a result has no condition. Proposal: an optional `condition` on `type-assignment` results (`under-stress`, `at-ease`, or free text).
3. **`reviewAfter: on-change` cannot be stored.** AssessmentRecord `reviewAfter` accepts only a duration, and §7.2 does not define `on-change`. Proposal: allow `on-change` and define it as "current until superseded or marked not current".
4. **A practitioner's reading through the lens cannot be stored.** *Resolved in 0.1.0-draft.2:* LA-7 is retired and I5 applies `agentInterpretation` to agent and software authors only; a coach's reading needs the coach in `interpretationAuthors` of the active adoption.
5. **Unlisted tests have no honest mode.** Most people bring a free online test, which AR-8 rejects as an instrument; `self-identified` hides that a test was used. Proposal: allow a local instrument id `urn:ohc:instrument:x-<namespace>:<name>` with a validity flag `unlisted-instrument`, never with a `trademarkNotice`.
6. **The trademark notice rule is ambiguous.** `trademarkNotice` is required when the lens's marks require a notice and the result is genuine; for a self-identified result that uses no instrument, the rule reads as required. The checker does not test it. Proposal: require the notice exactly when `instrument` is present and that instrument's `marks` carry a notice; forbid it otherwise; add a checker rule.
7. **AR-6 asks for a rule the vendor does not disclose.** A vendor-assigned main type forces a placeholder in `generatedBy.method`. Proposal: let `mode: vendor-report-import` with `validityFlags` ⊇ `vendor-algorithm-undisclosed` satisfy AR-6.
8. **The instrument entry has no result scale.** Without it, an importer cannot fill `rawRange`. Proposal: `forms[].resultScale` (`min`, `max`, `unit`) in instrument entries, from public documentation only.
9. **The origin of what an agent writes on the person's behalf is not stated.** An agent-written `agent-suggested` LensAdoption and a Practice with `source.route: from-agent` have no `text`, so `origin: declared` fails ENV-2; `observed` passes but is documented nowhere, and `inferred` needs grounds these records do not have (verified). Proposal: state in §10.5, §17.1 and CONTEXT-08 that such records use `origin: observed` ("the agent records that the person accepted").
10. **An agent-offered Practice reaches grantees labelled "observed".** After the person's `admit`, a Practice with `source.route: from-agent`, `origin: observed` and the agent as asserter is served with the derived `label: observed` and `endorsement: not-asked`; the same holds for an admitted `agent-suggested` adoption (verified with the projection tool). The grantee sees the agent's suggestion presented as an observation about the person, and cannot see that the person admitted it. Proposal: derive `label: suggested` for Practices with `source.route: from-agent` and for `agent-suggested` adoptions, and `endorsement: admitted` once a subject `admit` Review exists; or add an origin `suggested` instead of reusing `observed`.
11. **A LensAdoption gates nothing.** A context with lens results, lens readings and from-lens Practices but no LensAdoption passes L1; results pass when the adoption's `uses` lack `store-results`, and when they were recorded before the adoption; while an `agent-suggested` or `imported` adoption is still `proposed`, a lens selector already serves the person's results, readings and Practices in that lens (verified). `uses` has no normative effect; §10.5 gives `uses` no rule. Proposal: a rule LA-8: a record with `lens` or `source.lens` by a non-subject author requires an adoption of that lens that is active at its `recordedAt` and whose `uses` include the matching use (`store-results`, `interpret`, `offer-practices`); a warning for the subject's own lens records with no active adoption; and a projection that withholds lens records while the adoption is `proposed` or `paused`.
12. **The route does not have to match the mode.** A `self-chosen` adoption with a `practitioner-facilitated` result passes the check (verified), so a typing interview can enter without the practitioner relationship and its release being recorded. Proposal: a warning when a `practitioner-facilitated` AssessmentRecord exists and no active adoption of its lens is `inherited-from-practice` with `practice.practitioner` equal to its `assessedBy`.
13. **Ground `kind` is not tied to the cited record.** A Claim can cite a self-identified or practitioner result with `kind: instrument`; the checker accepts any Ground kind for any target, and an earlier version of this recipe did exactly that. A grantee then reads a self-recognition as instrument evidence. Proposal: when a Ground's `ref` is an AssessmentRecord, `kind` matches its `mode` (`self-identified` → `subject-statement`; `practitioner-facilitated` or interview modes → `practitioner`; instrument modes → `instrument`), or the projection derives the kind from the mode.
14. **A Source cannot name the lens it belongs to.** A screenshot of a free test kept without a self-identified record has no `lens` field, so lens selectors, lens defaults (`special`, `mental-health`) and grants by lens never reach it, and the person cannot tie it to the lens. Proposal: an optional `lens` (LensRef) on Source; lens selectors then reach it at its `maxRelease` tier, and lens default categories apply to it.
15. **The checker's report reads as if the vault were not checked.** `"vaultContentRead": false` appears even when the checker has read a vault file and compared its hash (SR-2 fires on a tampered file; verified). Proposal: report `vaultHashesChecked` (a count) next to `vaultContentRead`, and define `vaultContentRead` as "the content was not interpreted".

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
