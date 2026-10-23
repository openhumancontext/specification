# Big Five: how to bring a person's material into OHC

**Recipe · lens `urn:ohc:lens:big-five` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe turns a person's Big Five material (a questionnaire result they own, their own words about their tendencies, and readings of recent episodes) into OHC records, one step and one record at a time, with nothing stored that the lens or the instrument forbids.

The lens descriptor is `spec/lenses/big-five.lens.json` (`descriptorStatus: draft`, `legalReviewNeeded: true`). It is a full descriptor, not a stub, so every step below is available. Read it before you start: its `mentalModel`, `ip` and `defaults` are the facts and guidance this recipe applies.

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them.

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:big-five-basic`](../../spec/playbooks/big-five-basic.playbook.json) (Big Five: basic ways of working, by the OHC editors), for these situations: planning the week ahead; choosing between options; giving feedback to someone; looking back at something that happened; preparing a hard conversation; under strain: tired, pressed or overloaded. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

**Bringing a report through the person's window.** BFI-2's catalog entry carries an `import` block, so a person can bring a BFI-2 result through their own window ([guide](../guides/BRING-A-RESULT.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md); worked example: [Tove](../../examples/tove-bring-a-result/)). The steps below record a report by hand, as for IPIP-NEO-120 and NEO-PI-3.

## 1. What you may have

| Input | Example | Where it goes |
|---|---|---|
| Self-description in conversation | "I'm organised, but crowds drain me." | A Claim in the person's words (step 4). No AssessmentRecord: words are not a score. |
| An instrument report the person owns | An IPIP-NEO-120 score page; BFI-2 scores from a research study; a NEO-PI-3 report from a qualified practitioner | The report file is a Source (step 2); the scores are an AssessmentRecord (step 3). |
| Notes from coaching, teaching or therapy where Big Five was used | A coach's session notes that mention the person's scores | Adoption route `inherited-from-practice` (step 1); the notes are a Source under the practitioner's custody (step 2). Their text is never copied into a record. |
| An agent's reading | A companion that has talked with the person for weeks is asked: "what would you guess?" | Only if the person asks, and only under a Grant that gives you both `suggest` and `infer`: an AssessmentRecord with `mode: agent-inference` that only the person sees (step 3b), and readings of episodes (step 5). |

The lens lists three instruments: `urn:ohc:instrument:ipip-neo-120` (public-domain items, public scoring), `urn:ohc:instrument:bfi-2` (items copyright Soto and John; free for non-commercial research only) and `urn:ohc:instrument:neo-pi-3` (proprietary, PAR, Inc.; qualification level S). A test that is not one of these three cannot be named in `instrument` (AR-8); see §6.

## 2. Before you start

**Route of adoption.** Choose the one that matches how the person came to the lens. It goes into `LensAdoption.route`.

| Route | When | What it changes |
|---|---|---|
| `self-chosen` | The person picked the lens. This recipe's example takes this route. | The adoption is active as soon as it is written. |
| `agent-suggested` | You proposed the lens, under a Grant that lets you (`suggest`, with a selector naming the lens). The descriptor's `adoption.suggestionRequires` says when that usually makes sense: after the person asked for ways of describing their tendencies. | Add `suggestedBy` with your Party id. The adoption stays `proposed` until the person admits it with a Review `admit` (LA-1); see the snippet below. |
| `inherited-from-practice` | The lens came from the person's coach, teacher or therapist (`adoption.inheritanceRoles`). | Add a `practice` block: `role`, `practitioner` (a Party id), `relationship`, `since`, and `releaseRef` (a Source holding the practitioner's release) whenever a stored Source is authored by the practitioner or in their custody, the report included (LA-3). Set `confidentiality` and `onEnd`. The adoption gives the practitioner no access (LA-2); only a Grant does. |
| `imported` | An importer created the adoption from a report. | The adoption is `proposed` until the person admits it, and so is every AssessmentRecord from the same import run (LA-5). |

**The `agent-suggested` route in records.** The adoption stays the person's (`assertedBy: "subject"`); `suggestedBy` names you. Write the person's request in `note`, in their words: OHC 0.1 has no field for it (§6).

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"}, "route": "agent-suggested", "suggestedBy": "a-01",
 "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"],
 "interpretationAuthors": ["subject", "a-01"], "agentInterpretation": "ask-first",
 "representationPreference": "big-five.score-profile",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-08-10T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"],
 "note": "Kesi asked for ways to describe tendencies; the companion suggested the Big Five.", "synthetic": true}
```

Then the person's admit goes into `reviews`. Only the person admits: an admit by anyone else fails LA-1. Until the person admits it, the adoption is not active, and it neither stops nor allows anything.

```json
{"id": "rv-00", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-08-10T18:05:00Z"}
```

**Consent.** Ask before each step and read every record back before it is saved. The person can stop at any step. An agent's own readings and estimates need a separate yes: a Grant that gives the agent both `suggest` and `infer`, with `basis.legal: explicit-consent` (INF-1, R-G11). A Grant with `infer` but without `suggest` fails INF-1.

**Who writes.** The person's own holder writes the person's records with `assertedBy: "subject"`. If you are an agent, you write two kinds of records only:

- your own readings and estimates, with `assertedBy` set to your Party id, `origin: "inferred"`, and `underGrant` and `purpose` naming a Grant that gives you `suggest` and `infer` (INF-1). They stay `proposed` until the person decides;
- the person's own statements, only if the person gave you a Grant with `write`: keep `assertedBy: "subject"`, add `recordedBy` (your Party id), `underGrant` and `purpose`, and read the record back first. Such a record is active at once, so never write one the person has not confirmed word for word (§6).

**Defaults for this lens** (`defaults` in the descriptor):

- `sensitivity: "special"`: every record of this lens is treated as special category. A Grant reaches it only by naming its id, its lens or its category, under explicit consent (R-G3).
- `categories: ["mental-health"]`. The constructs `big-five/N`, `big-five/N/anxiety` and `big-five/N/depression` carry `mental-health` themselves.
- `reviewAfter: "P3Y"`: results are due for review after three years.
- Handling: the descriptor says a helper must not comment on the facets Anxiety or Depression unless the person raises them. Store those two facets in their own AssessmentRecord with handling `subject-initiated-only` and `no-quote-back` (step 3).

**Never stored.**

- Item text of any instrument. For NEO-PI-3 and BFI-2 this is a licence condition (`ip.restrictions`); for IPIP it is simply not needed.
- Item responses. The one exception is the person's own test data in `ext["ohc.test-data"]`, with handling `person-only` and the validity flag `test-data-personal-only` (AR-3).
- Scoring keys and report prose (the interpretive text of a NEO-PI-3 report, for example). Copy numbers, never sentences.
- Labels from other frameworks derived from these scores: no type letters, no "type" of any kind (M-4).
- A score as a judgement of the person: "low Agreeableness" is a range on one questionnaire, never "difficult".

## 3. Steps

Each step says what to do, which record to write, a JSON snippet that validates against `spec/schema/*.schema.json`, and who sees the record by default. The snippets are the records of the worked example (§5), in its single-document form: each goes into the array named in the step. **By default nobody but the person sees anything** (R-G1); step 7 is where that changes.

### Step 0. The file and its folder

One context is one folder. All records go into one file, `context.json`. The original files (reports, notes, releases) go next to it under `vault/`. You run the checker on the folder (step 8).

```text
<folder>/
  context.json
  vault/5a/5a96dfc655346df9acb02ed2398f819a8de6f082b1476299f4fff5048502a85c.json
```

Start `context.json` with its root. These are the root fields of the worked example:

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:ohc:example:kesi:big-five", "version": "2026-09-12.1",
 "subject": {"id": "urn:ohc:example:kesi", "displayName": "Kesi (fictional)"},
 "holder": "subject", "lang": "en", "created": "2026-08-10T18:00:00Z",
 "policy": {"admission": "subject-only", "resolver": "returnDialog"},
 "synthetic": true}
```

- `format`, `specVersion`, `id`, `version` and `subject` are required (`spec/schema/context.schema.json`).
- `id` and `subject.id`: for a real person, a `urn:uuid:` you generate, never a name or an email. `urn:ohc:example:<name>[:<context>]` is for examples only.
- `version`: any text you choose; change it whenever you change the file.
- `synthetic: true` only in examples, where it goes on the root and on every record. Leave it out for a real person.
- Add to the same object `conformance`, `parties` and `lenses` (step 1), then the arrays this recipe fills: `lensAdoptions` (step 1), `sources` (2), `assessments` (3, 3b), `claims` and `relations` (4), `episodes` and `interpretations` (5), `reviews` (3b, 5), `practices` and `outcomes` (6), `grants` (7). Leave out any array you do not use.
- **Codes for `contexts`** (on any record that has the field): `work`, `family`, `partner`, `friends`, `health`, `learning`, `money`, `home`, `community`, `spiritual`, `creative`, `personal-practice`, `therapy`, `coaching`. Anything else must be a local code `x-<namespace>:<code>` defined in the root `vocabulary`, for example `"vocabulary": {"x-kesi:choir": {"definition": "Singing in a community choir"}}`. Any other value fails S-3.

### Step 1. Pin the lens and record the adoption

Ask how the person came to the lens and what they want to do with it. Then:

1. In the manifest, declare the modules you will use and pin the lens. `sha256` is the SHA-256 of the descriptor file you read (`shasum -a 256 spec/lenses/big-five.lens.json`); it lets anyone check later which version was used.
2. List every Party you will name: the agents, the software that produced a report, any practitioner.
3. Write the LensAdoption into `lensAdoptions`.

```json
"conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
"parties": [
  {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"},
  {"id": "a-02", "partyKind": "agent", "label": "Work assistant"},
  {"id": "s-01", "partyKind": "software", "label": "Public IPIP scoring page"}
],
"lenses": [{"id": "urn:ohc:lens:big-five", "version": "0.2.0", "sha256": "6af97400e92c87df43cdb7aa7d7406c0a6688c4f819d456182559bd4d41b0a4d"}]
```

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"}, "route": "self-chosen",
 "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"],
 "interpretationAuthors": ["subject", "a-01"], "agentInterpretation": "ask-first",
 "representationPreference": "big-five.score-profile",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-08-10T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- `uses` records what the person agreed to: `speak-in-lens`, `store-results`, `interpret`, `offer-practices`, `recall`. OHC 0.1 does not enforce it: no rule ties a record to `uses`. So you and the holder keep to it yourselves: store results only with `store-results`, write readings only with `interpret`, offer the toolkit only with `offer-practices` (§6).
- `agentInterpretation`: `off` (default), `ask-first` or `allowed`. While the adoption is active, `off` stops every agent reading through the lens, whatever the Grant says. With `ask-first`, ask before every reading; a context with an event log (L2) records each confirmation as an Event `ask-first` (I5).
- `interpretationAuthors`: which people besides the person (a coach, for example) may write readings through the lens. An agent reads through it under its Grant instead: an `infer` grant whose scope names the lens (I5).
- `representationPreference`: the descriptor's one representation, `big-five.score-profile` (raw score, range and percentile with the norm group named).

**Who sees it:** the person only. Adopting a lens gives nobody access.

### Step 2. Keep the original report as a Source

Store the report file the person gave you in the vault and describe it. Compute the three values from the file itself; never type them:

- `sha256`: the SHA-256 of the file's bytes, in lowercase hex (`shasum -a 256 <file>` or `sha256sum <file>`);
- `size`: the file's length in bytes (`wc -c < <file>`);
- `vaultPath`: `vault/<first two characters of the sha256>/<sha256>.<extension>`, relative to the folder that holds `context.json`.

The checker only compares `sha256` with the name in `vaultPath` (SR-3). It never opens vault files (`vaultContentRead: false`), so a wrong hash, a wrong size or a missing file passes unnoticed (§6).

```json
{"id": "src-01", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/5a/5a96dfc655346df9acb02ed2398f819a8de6f082b1476299f4fff5048502a85c.json"},
             "sha256": "5a96dfc655346df9acb02ed2398f819a8de6f082b1476299f4fff5048502a85c",
             "mediaType": "application/json", "size": 644},
 "capturedAt": "2026-08-14T19:40:00Z", "authorship": {"author": "s-01"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index",
 "summary": {"text": "Score page saved after taking the IPIP-NEO-120.", "authoredBy": "subject",
             "recordedAt": "2026-08-14T20:00:00Z", "method": "subject-written"},
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-08-14T20:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- `authorship.author`: whoever produced the report: the scoring software (a `software` Party), or the practitioner who handed it over (a `person` Party).
- `maxRelease: "index"`: a grantee learns at most that the report exists. Keep it at `index` for every report; a NEO-PI-3 report contains proprietary prose that must never travel.
- **From a practitioner** (a NEO-PI-3 report, coaching notes): add `"custody": {"custodian": "<practitioner Party id>", "confidentiality": "coaching" | "therapy", "releaseRef": "<Source id of the practitioner's release>"}`, keep `maxRelease: "index"`, and use `sourceKind: "practitioner-notes"` for notes. For a teacher, use `"confidentiality": "none"`: 0.1 has no code for teaching (§6), so `maxRelease: "index"` is what protects the file. Store the release itself as its own Source (`sourceKind: "practitioner-release"`, authored by the practitioner).
- `summary.text` is the person's own one-line description. Never paste report text into `summary`, `title` or `note` (SR-4).

**Who sees it:** the person, always in full. A grantee at most at the `index` tier, and only when a Grant names it.

### Step 3. Record the result as AssessmentRecords

Copy only numbers from the report. Ask the person whether they want the facets Anxiety and Depression stored at all; if yes, put them in a second record with their own handling.

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"}, "lensVariant": "5-domain-30-facet",
 "instrument": {"id": "urn:ohc:instrument:ipip-neo-120", "form": "120"},
 "mode": "self-report-instrument", "assessedBy": "subject",
 "administeredAt": {"start": "2026-08-14", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "big-five/O", "label": "Openness", "raw": 4.2, "rawRange": [1, 5], "standardized": {"type": "percentile", "value": 81}},
   {"type": "dimension-score", "construct": "big-five/C", "label": "Conscientiousness", "raw": 3.9, "rawRange": [1, 5], "standardized": {"type": "percentile", "value": 66}},
   {"type": "dimension-score", "construct": "big-five/E", "label": "Extraversion", "raw": 2.6, "rawRange": [1, 5], "standardized": {"type": "percentile", "value": 22}},
   {"type": "dimension-score", "construct": "big-five/A", "label": "Agreeableness", "raw": 3.7, "rawRange": [1, 5], "standardized": {"type": "percentile", "value": 52}},
   {"type": "dimension-score", "construct": "big-five/N", "label": "Neuroticism", "raw": 3.1, "rawRange": [1, 5], "standardized": {"type": "percentile", "value": 55}}],
 "normGroup": {"id": "ipip-neo-120-internet-2014", "year": 2014, "note": "Internet sample published with the IPIP-NEO-120"},
 "validityFlags": [],
 "source": "src-01",
 "reviewAfter": "P3Y",
 "origin": "derived", "derivedFrom": ["src-01"],
 "generatedBy": {"software": "public IPIP scoring page", "method": "means of keyed items on a 1-5 scale; percentiles against the published internet norms"},
 "assertedBy": "subject", "recordedAt": "2026-08-14T20:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "as-02", "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"}, "lensVariant": "5-domain-30-facet",
 "instrument": {"id": "urn:ohc:instrument:ipip-neo-120", "form": "120"},
 "mode": "self-report-instrument", "assessedBy": "subject",
 "administeredAt": {"start": "2026-08-14", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "big-five/N/anxiety", "label": "Anxiety (facet)", "raw": 3.5, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "big-five/N/depression", "label": "Depression (facet)", "raw": 2.5, "rawRange": [1, 5]}],
 "normGroup": {"id": "ipip-neo-120-internet-2014", "year": 2014, "note": "Internet sample published with the IPIP-NEO-120"},
 "validityFlags": [],
 "source": "src-01",
 "reviewAfter": "P3Y",
 "origin": "derived", "derivedFrom": ["src-01"],
 "generatedBy": {"software": "public IPIP scoring page", "method": "means of keyed items on a 1-5 scale"},
 "assertedBy": "subject", "recordedAt": "2026-08-14T20:06:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["subject-initiated-only", "no-quote-back"],
 "synthetic": true}
```

Fill the fields like this:

| Field | Value |
|---|---|
| `lens` | `{"id": "urn:ohc:lens:big-five", "version": "0.2.0"}` |
| `lensVariant` | `5-domain-30-facet` for IPIP-NEO-120 and NEO-PI-3; `bfi-2-15-facet` for BFI-2. The checker does not check this value, so copy it exactly (§6). |
| `instrument` | `id`: one of the three instrument ids. `form`: the form id from the instrument entry (`spec/instruments/<name>.instrument.json`, `forms[].id`): `"120"` for IPIP-NEO-120, `"60"` for BFI-2, `"self-report"` or `"informant-report"` for NEO-PI-3. `version`: the publisher's edition **printed on the report**, not the catalog entry's own `version` (`0.1.0`; `0.2.0` for BFI-2). Leave `version` out when the report prints none, as Kesi's score page does and as a BFI-2 sheet usually does. |
| `mode` and `origin` (AR-1) | You or a public scoring page computed the scores: `self-report-instrument` with `origin: "derived"`, plus `derivedFrom` (the Source) and `generatedBy` with a `method`. A vendor report copied as it is (NEO-PI-3): `vendor-report-import` with `origin: "imported"` and `importedFrom` (`importedAt` equal to `recordedAt`); see the fragment below. Someone else rated the person with an informant form: `observer-report` with `assessedBy` (their Party id) and `raterRelationship`. |
| `results` | One `dimension-score` per construct. `construct` comes from the descriptor's `constructs`: `big-five/O`, `big-five/C`, `big-five/E`, `big-five/A`, `big-five/N`, `big-five/N/anxiety`, `big-five/N/depression`. The descriptor lists no other facets, so leave the other facets of a report out; never invent an id (§6). `raw` and `rawRange` as printed; `standardized` only when the report gives it (`percentile`, `T`, `z`, `stanine` or `sten`). With BFI-2, keep the report's own wording in `label` (for example "Negative Emotionality") and the construct id `big-five/N`. |
| `normGroup` | The norm sample the report names. If it names none, leave `normGroup` out and say "no norm group" whenever the scores are shown. |
| `validityFlags` | What the report or the situation says: `incomplete`, `translated-form`, `norm-mismatch`, `vendor-algorithm-undisclosed` and so on. A NEO-PI-3 vendor report always has `vendor-algorithm-undisclosed` (its scoring is proprietary). An empty list says none applies. |
| `trademarkNotice` | Only on a genuine NEO-PI-3 result: the `notice` of the mark in `spec/instruments/neo-pi-3.instrument.json`, copied exactly. OHC 0.1 requires a notice only for marks in the lens descriptor (this lens has none), and the checker does not ask for this one; add it anyway (§6). Never on an agent estimate (AR-2). |
| `reviewAfter` | `P3Y`, from the descriptor's `defaults`. |
| `sensitivity`, `categories` | `special`, `["mental-health"]`. |

**A NEO-PI-3 report from a practitioner.** Build the record like `as-01`, leave out `derivedFrom` and `generatedBy`, and use these fields (Kesi has no such report, so the example has none; a record built this way passes L1):

```json
"lensVariant": "5-domain-30-facet",
"instrument": {"id": "urn:ohc:instrument:neo-pi-3", "form": "self-report"},
"mode": "vendor-report-import",
"validityFlags": ["vendor-algorithm-undisclosed"],
"trademarkNotice": "NEO-PI-3™ is a mark of PAR, Inc.; used here only to name the instrument.",
"origin": "imported",
"importedFrom": {"system": "NEO-PI-3 report handed over by the psychologist", "importedAt": "2026-08-15T10:00:00Z"},
"recordedAt": "2026-08-15T10:00:00Z"
```

**Who sees them:** the person. A grantee only when a Grant names the lens, the category or the id under explicit consent. `as-02` also travels with `subject-initiated-only` (used only inside a conversation the person started) and `no-quote-back` (never cited back to the person as proof).

### Step 3b. Only if the person asks: an agent's estimate

Whether you may make an estimate is the person's Grant: one that gives you both `suggest` and `infer` and names the lens (`g-01` in step 7). Make one when the person asks for it, for example to compare it with the questionnaire. Write it as your own record; the person then decides whether to keep it.

```json
{"id": "as-03", "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"},
 "mode": "agent-inference", "assessedBy": "a-01",
 "administeredAt": {"start": "2026-09-01", "end": "2026-09-10", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "big-five/E", "raw": 3.4, "rawRange": [1, 5]}],
 "validityFlags": ["agent-estimate-not-validated"], "validityCeiling": "agent-estimate-not-validated",
 "derivedFrom": ["ep-01", "ep-02", "ep-03"],
 "origin": "inferred", "assertedBy": "a-01", "recordedAt": "2026-09-10T10:05:00Z",
 "underGrant": "g-01", "purpose": "self-reflection", "epistemic": "hypothesis",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["person-only"],
 "note": "Asked for by Kesi: a rough guess from three episodes, to compare with the questionnaire.",
 "synthetic": true}
```

```json
{"id": "rv-02", "target": "as-03", "action": "admit", "by": "subject", "recordedAt": "2026-09-12T08:02:00Z"}
```

- AR-2 requires all of these: handling `person-only`, the flag and ceiling `agent-estimate-not-validated`, and no `trademarkNotice` or branded label.
- `derivedFrom` names the episodes the guess rests on (step 5). Leave `label` out: it is a guess, not a measured result. Never put an instrument name such as "NEO-PI-3" in it.
- Only the person can admit it (R-A1); the Review goes into `reviews`. If the person declines, write `"action": "decline"` instead; the estimate stays in history, unused.

**Who sees it:** the person only, always (`person-only`); not even you receive it back in a projection.

### Step 4. Claims the person accepts

Show the person the score profile: raw score, range and norm group together. Ask which tendencies they recognise and in which settings. Write a Claim only for what they say yes to.

```json
{"id": "c-01", "facet": "disposition", "predicate": "assessed-trait",
 "text": "Openness: high range (raw 4.2 of 5; 81st percentile; IPIP-NEO-120, internet norms 2014; August 2026).",
 "horizon": "foundation", "reviewAfter": "P3Y",
 "origin": "derived", "derivedFrom": ["as-01"],
 "generatedBy": {"software": "holder app", "method": "one result line of as-01 restated with its norm group"},
 "assertedBy": "subject", "recordedAt": "2026-09-06T20:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "c-02", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "I get absorbed in new ideas and need a quiet hour to think them through.",
 "horizon": "foundation", "evidence": [{"ref": "as-01", "kind": "instrument"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-06T20:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- **A result line the person accepts** (`c-01`): facet `disposition`, predicate `assessed-trait`, `origin: "derived"`, `derivedFrom` the AssessmentRecord, `generatedBy.method` saying how the line was restated (CL-3). Keep the instrument, the norm group and the date in the text.
- **The same tendency in the person's own words** (`c-02`): predicate `self-described-tendency`, `origin: "declared"`, and `evidence` pointing at the result with kind `instrument`.
- A line the person does not recognise gets no Claim. Use the fit check (step 5) instead.

The lens also supports "choosing communication preferences the person then states". Write such a preference as an ordinary Claim, **without** citing the result: a citation would raise it to special (C3) and keep it from the work assistant. If the person wants the link kept, add a Relation; a Relation does not raise the tier of the records it joins.

```json
{"id": "c-03", "facet": "preference", "predicate": "format",
 "text": "Send the agenda the day before; I prepare better in writing than on the spot.",
 "horizon": "focus", "contexts": ["work"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-06T20:10:00Z", "synthetic": true}
```

```json
{"id": "rl-01", "rel": "supports", "from": "as-01", "to": "c-03",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-06T20:11:00Z",
 "note": "Kesi chose this preference after reading the score profile.", "synthetic": true}
```

**Who sees them:** `c-01` and `c-02` are special (they cite the result) and travel only to a Grant that names them by id or by the category `mental-health`; a `lenses` selector does not reach them (§6). `c-03` is a personal-tier preference: a Grant with a `preference` facet selector reaches it. `rl-01` is special, like the result it cites.

### Step 5. Read recent episodes through the lens

The descriptor's toolkit item `big-five.fit-check` compares one domain with three recent episodes and notes fit or no fit. It produces an Interpretation.

1. Write the episodes the person tells you about into `episodes`, if they are not there yet. Keep what happened apart from how it was understood. `contexts` takes the codes listed in step 0.

```json
{"id": "ep-01", "title": "Team workshop", "occurred": {"start": "2026-08-27", "precision": "day"},
 "accounts": [{"narrator": "subject", "narratedAt": "2026-08-27T19:00:00Z", "addedAt": "2026-08-27T19:00:00Z",
               "accountKind": "in-the-moment", "happened": "Led a two-hour team workshop and did most of the talking.",
               "didOrTried": "Prepared written notes the evening before."}],
 "contexts": ["work"], "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-08-27T19:00:00Z", "synthetic": true}
```

`ep-02` (an old friends' dinner, `"contexts": ["friends"]`) and `ep-03` (a client call, `"contexts": ["work"]`) have the same fields.

2. The person's own fit check is their Interpretation, with `stance: "lens-reading"` and the lens:

```json
{"id": "in-01", "about": ["as-01", "ep-01", "ep-02", "ep-03"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"},
 "text": "Fit check, Extraversion: the low score fits the dinner, not the two work episodes.",
 "facets": ["disposition"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-06T19:30:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

3. Your reading as an agent needs a Grant that gives you `suggest` and `infer` and names the lens (I5, INF-1), and an adoption, if the person has an active one, whose `agentInterpretation` is not `off`; with `ask-first`, the person said yes this time. It needs grounds, what does not fit, at least two alternatives of which one is not psychological, and limits (I4):

```json
{"id": "in-02", "about": ["ep-01", "ep-03"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"}, "adoption": "la-01",
 "text": "At work you may speak up because the role asks for it; the low Extraversion score may describe what you choose when no role is set.",
 "causal": "hypothesized",
 "grounds": [{"ref": "ep-01", "kind": "evidence"}, {"ref": "ep-03", "kind": "evidence"}, {"ref": "as-01", "kind": "instrument"}],
 "counterEvidence": [{"ref": "ep-02", "kind": "evidence", "note": "Left early where no role was set."}],
 "alternatives": [
   {"text": "Both work episodes were prepared in writing the day before.", "kind": "informational"},
   {"text": "Both work topics were ones Kesi knows well.", "kind": "situational"},
   {"text": "The dinner came at the end of a long week.", "kind": "physiological"}],
 "limits": "Three episodes and one questionnaire; a reflection aid, not a description of who Kesi is.",
 "facets": ["disposition"],
 "origin": "inferred", "assertedBy": "a-01", "recordedAt": "2026-09-10T10:00:00Z",
 "underGrant": "g-01", "purpose": "self-reflection", "epistemic": "hypothesis",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

4. The person answers your reading with a Review. Here they accept part of it, in their own words:

```json
{"id": "rv-01", "target": "in-02", "action": "partially-endorse", "by": "subject", "recordedAt": "2026-09-12T08:00:00Z",
 "endorsedPart": "At work I speak up because the role asks for it."}
```

Use `causal: "hypothesized"` at most; an agent never asserts a cause (I2). Speak of tendencies and ranges; never use a score to explain away what the person says.

**Who sees them:** episodes are sensitive and reach only Grants that name the kind or the id. The readings are special: a Grant must name the lens, and its `interpretations` policy must allow them (R-G8). Your reading stays `proposed`, visible to the person and to you as its proposer, until the person decides.

### Step 6. A practice from the toolkit and its outcome

If the person wants to repeat the fit check, record it as a Practice with the toolkit item as its template, and record how it went as an Outcome.

```json
{"id": "pr-01", "name": "Yearly fit check",
 "description": "Take one domain and three recent episodes; note where the score fits and where it does not.",
 "practiceKind": "reflection",
 "source": {"route": "from-lens", "lens": "urn:ohc:lens:big-five", "templateId": "big-five.fit-check"},
 "steps": ["Pick one domain", "Pick three recent episodes from different settings", "Write fit or no fit for each, in one line"],
 "duration": "PT20M", "limits": "Not a re-test; it never changes the scores.", "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-06T19:00:00Z", "synthetic": true}
```

```json
{"id": "oc-01", "about": {"practice": "pr-01"}, "result": "helped",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-06T21:00:00Z", "synthetic": true}
```

- `big-five.fit-check` has `agentMayOffer: true`, so you may offer it, if the adoption's `uses` has `offer-practices`. If you write the Practice yourself, use `source.route: "from-agent"` and your Party id as `assertedBy`; it is then a proposal (PC-1).
- Never store claims about how well the practice works (PC-3). The Outcome is the person's own rating; an agent's Outcome is labelled "agent's estimate" (O-1).

**Who sees them:** the Practice is personal tier, so any Grant whose scope matches it reaches it, including a Grant with a `lenses` selector for this lens (a `from-lens` Practice counts as a record of the lens). It holds no score. The Outcome has the tier of its practice.

### Step 7. Who may see what

Nothing leaves the context without a Grant. Write one Grant per recipient and purpose. In the example the reflection companion may read the lens's records, the two dispositions and the episodes, and may propose readings and estimates; the work assistant sees stated work preferences only.

```json
{"id": "g-01", "recordedAt": "2026-09-01T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:big-five"]}, {"ids": ["c-01", "c-02"]}, {"kinds": ["Episode"]}]},
 "actions": ["read", "suggest", "infer"], "mode": "full", "interpretations": "all",
 "constraints": {"expiresAt": "2027-02-26T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "reviewCadence": "P7D",
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-01T09:00:00Z", "channel": "holder-ui"},
 "note": "Reflection only. Scores and readings never leave this companion."}
```

```json
{"id": "g-02", "recordedAt": "2026-09-06T20:15:00Z", "grantor": "subject", "grantee": "a-02",
 "purposes": ["communication-adaptation"],
 "scope": {"include": [{"facets": ["preference"], "contexts": ["work"]}]},
 "actions": ["read"], "mode": "rule-only", "interpretations": "none",
 "constraints": {"expiresAt": "2027-09-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-06T20:15:00Z", "channel": "holder-ui"},
 "note": "The work assistant sees stated work preferences only, never scores."}
```

- Any Grant that reaches records of this lens, or that includes `infer`, uses `basis.legal: "explicit-consent"` and expires within 180 days (R-G10, GR-1, GR-4). Other grants expire within a year.
- `actions`: `read` lets the agent see; `suggest` and `infer` together let it write its own readings and estimates as proposals (INF-1). Leave both out for a recipient who should only read.
- A `lenses` selector serves every record that carries the lens: the LensAdoption, the AssessmentRecords, the readings and any `from-lens` Practice, not only the scores (§6). Add an `exclude` by id for what this recipient should not have.
- `purposes` never include a prohibited purpose (§8.10). For this lens that means no hiring, task allocation, performance evaluation, promotion, ranking against others or persuasion.
- `expressedBy` is how the person said yes. Your statement that "the person agreed" is never consent.
- Grants go into `grants`. When the person wants something kept from one recipient, add an `exclude` selector, or a separate Grant with `"effect": "deny"`.

### Step 8. Check

From the specification repository, run the checker on the folder of step 0:

```sh
python3 -B tools/check.py <folder> --level L1 --json
```

Fix every error. The checker never prints your values. It checks shape and rules, not truth or consent: the person's confirmation in each step is what matters. It also does not open vault files, so check `sha256` and `size` against the files yourself with the commands of step 2.

## 4. Never

- **Never for these purposes,** under any grant: personnel selection, task allocation, performance evaluation, promotion decisions, ranking against other people, persuasion targeting, and the other prohibited purposes (§8.10). A result grounds a choice you propose for the person only under the grant's `decisionUse: approval-required`, only when the person accepted it, naming what you weighed (R-G14).
- **Never** suggest that the person suits or does not suit a job or role.
- **Never** comment on the facets Anxiety or Depression unless the person raises them.
- **Never** predict what the person will do in a given moment from a trait, and never use a score to explain away what the person says.
- **Never** present a high or low score as a flaw; never present results as a clinical state.
- **Never** make an agent estimate without a Grant that gives you both `suggest` and `infer` for the lens, or without `person-only`. Never use an estimate as input to any other inference (C-7).
- **Never** translate scores into another framework's labels: no type letters from Big Five scores (M-4), and no HEXACO scores from Big Five scores (M-1). Population-level Mappings are never used to convert one person's result. Every lens-to-lens row in the 0.1 catalog forbids that use (AR-7 refuses it).
- **Never** store item text, item responses (outside `ext["ohc.test-data"]`), scoring keys or report prose. Never administer NEO-PI-3 (qualification level S) or BFI-2 (non-commercial research only) yourself. If the person wants to take a questionnaire with you, use the IPIP-NEO-120, whose items are public domain.
- **Trademarks:** "NEO-PI-3" is a mark of PAR, Inc. (status unverified in the catalog; `use: nominative-only`). Use it only to name that instrument, never as a generic label and never in the `label` of an estimate. A genuine NEO-PI-3 result carries the instrument entry's notice in `trademarkNotice` (step 3).

## 5. Worked example

[examples/big-five/context.json](examples/big-five/context.json) is a single-document context for Kesi, a fictional person. Every record carries `"synthetic": true`. It contains exactly the records of §3: `la-01`, `src-01` (with its vault file), `as-01`, `as-02`, `as-03` and `rv-02`, `c-01`, `c-02`, `c-03`, `rl-01`, `ep-01` to `ep-03`, `in-01`, `in-02` and `rv-01`, `pr-01` and `oc-01`, and `g-01` and `g-02`. The route snippet of §2 (`agent-suggested` with `rv-00`) and the NEO-PI-3 fragment of step 3 are alternatives, not part of the example; each was checked separately and passes L1.

```sh
python3 -B tools/check.py docs/lenses/examples/big-five --level L1 --json
```

Result: `"valid": true`, `"levelMet": "L1"`, no errors and no warnings. The expected output is kept in [examples/big-five/expected-check.json](examples/big-five/expected-check.json).

## 6. What does not fit yet

Each item is recorded for the next revision of the standard.

1. **Handling per construct.** The rule "do not comment on Anxiety or Depression unless the person raises it" can only be kept by splitting those facets into their own record (`as-02`). Neither `defaults.perConstruct` nor a single result can carry `handling`.
2. **Which toolkit item produced a record.** `in-01` comes from `big-five.fit-check`, but an Interpretation (or an AssessmentRecord or ModelView) has no field to say so; only a Practice has `templateId`.
3. **Claims drawn from a result lose their lens.** A `lenses` selector reaches only records with a `lens` field. `c-01` and `c-02` must be named by id in every Grant.
4. **A link that is not evidence.** A preference prompted by a result cannot cite it without becoming special (C3), so `rl-01` uses `supports`, which reads as evidence. There is no relation code for "prompted by".
5. **An agent estimate has no grounds, alternatives or limits.** An Interpretation by an agent must carry them (I4); an AssessmentRecord with `mode: agent-inference` cannot. `as-03` uses `derivedFrom` and `note` instead.
6. **Instruments outside the catalog.** A Big Five test that is not one of the three listed cannot be named in `instrument` (AR-8), and there are no local instrument ids like local lenses (`x-`).
7. **Norm groups are free text.** `normGroup.id` is not tied to the instrument entry, so two records using the same norms cannot be recognised as such.
8. **The import tool writes invalid records.** *Resolved in 0.1.0-draft.2:* `tools/import_assessment.py` writes `standardized: {"type": "percentile", "value": …}` and only the catalog's mode codes.
9. **Records an agent writes in the person's name are active at once.** With `assertedBy: "subject"` and `recordedBy` set to an agent, nothing records that the person confirmed the text.
10. **`cross-lens-estimate` is unreachable.** Every lens-to-lens Mapping in the 0.1 catalog has a `forbiddenUse` or a blocked `rowStatus`, and the required `scope` text says "never for converting one person's result". The mode exists, but no record can use it.
11. **Most facets have no construct id.** The descriptor lists the five domains and two facets. The other 28 facets of IPIP-NEO-120 and NEO-PI-3, and the 15 facets of BFI-2, cannot be recorded with ids that "come from the lens's constructs".
12. **Construct ids are not checked.** The checker accepts any `construct` string in a result, even one from another lens (`hexaco/H` in a Big Five record passes), although LENSES.md §5 requires ids from the lens and M-1 forbids aliasing across lenses.
13. **`uses` has no force.** No rule ties a record to an active adoption of its lens or to the adoption's `uses`. AssessmentRecords, readings by the person and agent estimates all pass L1 with `uses: ["store-results"]` only, and even with no LensAdoption at all; only I5 looks at the adoption, and only for readings by someone other than the person.
14. **Marks in instrument entries are ignored.** NEO-PI-3's mark and notice live in its instrument entry, not in the lens's `ip.marks` (empty). A genuine NEO-PI-3 import without `trademarkNotice` passes, and so does an agent estimate labelled "NEO-PI-3 Extraversion"; AR-2's label check reads only the lens's marks.
15. **`form` and `lensVariant` are not checked.** `form: "999"` and `lensVariant: "no-such-variant"` pass L1. AR-8 checks only the instrument id, never the entry's `forms` or the lens's `variants`.
16. **`instrument.version` has no defined meaning, and instrument entries cannot be pinned.** It is not said whether the field holds the publisher's edition ("2014") or the catalog entry's version ("0.1.0"), and the manifest pins lenses by `sha256` but not instruments, so nobody can later tell which entry (with its `neverStore`, marks and terms) applied.
17. **The person's request for a suggestion cannot be recorded.** `adoption.suggestionRequires` says when a suggestion usually makes sense (after the person asked for ways of describing tendencies); LensAdoption has no field for that request, so it lives in `note`. Whether you may suggest is the person's Grant (`suggest`); LA-1 checks only that the person admits.
18. **Vault files are never compared with their description.** The checker does not read vault files (`vaultContentRead: false`). SR-3 only checks that `sha256` matches the name in `vaultPath`, so a `size` of 999 for a 379-byte file, a `sha256` that is not the file's hash (used the same way in `vaultPath`), or a file that is not there at all passes L1.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
