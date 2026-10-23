# HEXACO: how to bring a person's material into OHC

**Recipe · lens `urn:ohc:lens:hexaco` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe turns a person's HEXACO material (most often a HEXACO-PI-R score sheet from their coach, their own words, and a coach's remark) into OHC records step by step, keeping Honesty-Humility with the person and storing nothing the lens or the instrument forbids.

The lens descriptor is `spec/lenses/hexaco.lens.json` (`descriptorStatus: draft`, `legalReviewNeeded: true`). It is a full descriptor, not a stub, so every step below is available. Read it before you start: its `mentalModel`, `ip` and `defaults` are the facts and guidance this recipe applies. HEXACO is not the Big Five with a sixth factor added: several dimensions are defined differently, and its records never borrow Big Five ids or scores.

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them.

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:hexaco-basic`](../../spec/playbooks/hexaco-basic.playbook.json) (HEXACO: basic ways of working, by the OHC editors), for these situations: planning the week ahead; choosing between options; giving feedback to someone; looking back at something that happened. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

**Bringing a report through the person's window.** When an instrument's catalog entry carries an `import` block, a person can bring its result through their own window ([guide](../guides/BRING-A-RESULT.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). No entry of this lens has one yet, so the steps below record the report by hand.

## 1. What you may have

| Input | Example | Where it goes |
|---|---|---|
| Self-description in conversation | "I keep my word, even when it costs me." | A Claim in the person's words (step 4). No AssessmentRecord: words are not a score. |
| An instrument report the person owns | A HEXACO-PI-R score sheet (60-, 100- or 200-item form) from a coach, a course or a research study | The sheet is a Source (step 2); the scores are AssessmentRecords (step 3). |
| Notes or remarks from coaching, teaching or therapy where HEXACO was used | A coach's remark in a session, written down by the person | Adoption route `inherited-from-practice` (step 1); the coach's material is a Source under the coach's custody (step 2); a remark the person wants to keep is an Interpretation attributed to the coach (step 5). |
| An agent's reading | A companion asked to guess the person's scores | When the person asks, under a Grant that gives the agent both `suggest` and `infer` and names the lens. See step 3b. |

The lens lists one instrument: `urn:ohc:instrument:hexaco-pi-r` (forms `60`, `100`, `200`; items copyright Kibeom Lee and Michael C. Ashton; free to download only for non-profit academic research; online use only on password-protected or not-searchable pages; non-academic use requires contacting the authors). Scoring is public.

## 2. Before you start

**Route of adoption.** Choose the one that matches how the person came to the lens. It goes into `LensAdoption.route`.

| Route | When | What it changes |
|---|---|---|
| `self-chosen` | The person picked the lens. | The adoption is active as soon as it is written. |
| `agent-suggested` | You proposed the lens, under a Grant that lets you (`suggest`, with a selector naming the lens). The descriptor's `adoption.suggestionRequires` says when that usually makes sense: after the person asked for ways of describing their tendencies. | Add `suggestedBy` with your Party id. The adoption stays `proposed` until the person admits it with a Review `admit` (LA-1); see the snippet below. |
| `inherited-from-practice` | The lens came from the person's coach, teacher or therapist (`adoption.inheritanceRoles`). This recipe's example takes this route. | Add a `practice` block: `role`, `practitioner` (a Party id), `relationship`, `since`, and `releaseRef` (a Source holding the practitioner's release) whenever a stored Source is authored by the practitioner or in their custody, the score sheet included (LA-3). Set `confidentiality` and `onEnd`. The adoption gives the practitioner no access (LA-2); only a Grant does (step 7). |
| `imported` | An importer created the adoption from a report. | The adoption is `proposed` until the person admits it, and so is every AssessmentRecord from the same import run (LA-5). |

**The `agent-suggested` route in records.** The adoption stays the person's (`assertedBy: "subject"`); add `"suggestedBy": "<your Party id>"` and write the person's request in `note`, in their words (OHC 0.1 has no field for it; §6). Then the person's admit goes into `reviews`, with a `recordedAt` earlier than any reading through the lens; only the person admits (LA-1):

```json
{"id": "rv-00", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-06-05T18:01:00Z"}
```

**When the practice relationship ends.** The person writes a new LensAdoption that `supersedes` the old one, with `practice.relationship: "ended"` and the `onEnd` they choose (`keep-read-only`, `archive-person-only` or `erase`). While `onEnd` is `ask`, the adoption is paused until they decide. The coach's Grant does not end by itself: if the person wants that, withdraw it with a Review `{"id": "<new id>", "target": "<grant id>", "action": "withdraw-grant", "by": "subject", "recordedAt": "<now>"}`.

**Consent.** Ask before each step and read every record back before it is saved. The person can stop at any step. An agent's own readings and estimates need a separate yes: a Grant that gives the agent both `suggest` and `infer`, with `basis.legal: explicit-consent` (INF-1, R-G11). A Grant with `infer` but without `suggest` fails INF-1.

**Who writes.** The person's own holder writes the person's records with `assertedBy: "subject"`. A record that states what the coach scored or said is attributed to the coach (`assertedBy: "p-01"`) and recorded by the person (`recordedBy: "subject"`); it stays `proposed` until the person admits it. If you are an agent, you write only your own readings and estimates (`assertedBy` your Party id, `origin: "inferred"`, `underGrant` and `purpose` naming a Grant with `suggest` and `infer`), or, with a Grant that gives you `write`, the person's own confirmed statements with `recordedBy` set to your Party id.

**Defaults for this lens** (`defaults` in the descriptor):

- `sensitivity: "special"`: every record of this lens is treated as special category. A Grant reaches it only by naming its id, its lens or its category, under explicit consent (R-G3).
- `categories: ["mental-health"]`. The constructs `hexaco/E`, `hexaco/E/fearfulness` and `hexaco/E/anxiety` carry `mental-health` themselves.
- `reviewAfter: "P3Y"`.
- Handling. The descriptor says a helper must not comment on Honesty-Humility to anyone but the person, and must not comment on the facets Anxiety or Fearfulness unless the person raises them. Keep Honesty-Humility in its own AssessmentRecord with handling `no-forward` (step 3). A `lenses` selector reaches that record too, so in every Grant: exclude it by id (`"exclude": [{"ids": ["as-02", "in-01"]}]`) unless the person asks that this recipient have it, and then name it by id in `include` as well, so the Grant shows the person chose it (step 7). If the person stores the Emotionality facets, give Anxiety and Fearfulness their own record with handling `subject-initiated-only`.

**Never stored.**

- HEXACO-PI-R item text (`ip.restrictions`) and item responses. The one exception for responses is the person's own test data in `ext["ohc.test-data"]`, with handling `person-only` and the validity flag `test-data-personal-only` (AR-3).
- Report prose: copy numbers, never sentences.
- Big Five ids, Big Five scores or type labels derived from HEXACO scores (M-1, M-4).
- A score as a judgement of the person. A low Honesty-Humility score is never a judgement of character, and never a measure of trustworthiness.

## 3. Steps

Each step says what to do, which record to write, a JSON snippet that validates against `spec/schema/*.schema.json`, and who sees the record by default. The snippets are the records of the worked example (§5), in its single-document form: each goes into the array named in the step. **By default nobody but the person sees anything** (R-G1); step 7 is where that changes.

### Step 0. The file and its folder

One context is one folder. All records go into one file, `context.json`. The original files (score sheets, notes, releases) go next to it under `vault/`. You run the checker on the folder (step 8).

```text
<folder>/
  context.json
  vault/81/8112e383267bcb3907a5cbe6836fa0a9d308eec177ee39a4a40058e828cf805b.md
  vault/cf/cff3fcabb7196645be4bffd1029c62a93f6d1a79855f06dce3224114fd604bc8.json
```

Start `context.json` with its root. These are the root fields of the worked example:

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:ohc:example:sefa:hexaco", "version": "2026-06-12.1",
 "subject": {"id": "urn:ohc:example:sefa", "displayName": "Sefa (fictional)"},
 "holder": "subject", "lang": "en", "created": "2026-06-05T18:00:00Z",
 "policy": {"admission": "subject-only", "resolver": "returnDialog"},
 "synthetic": true}
```

- `format`, `specVersion`, `id`, `version` and `subject` are required (`spec/schema/context.schema.json`).
- `id` and `subject.id`: for a real person, a `urn:uuid:` you generate, never a name or an email. `urn:ohc:example:<name>[:<context>]` is for examples only.
- `version`: any text you choose; change it whenever you change the file.
- `synthetic: true` only in examples, where it goes on the root and on every record. Leave it out for a real person.
- Add to the same object `conformance`, `parties` and `lenses` (step 1), then the arrays this recipe fills: `lensAdoptions` (step 1), `sources` (2), `assessments` (3, 3b), `claims` (4), `episodes` and `interpretations` (5), `reviews` (3, 3b, 5), `practices` and `outcomes` (6, if used), `grants` (7). Leave out any array you do not use.
- **Codes for `contexts`** (on any record that has the field): `work`, `family`, `partner`, `friends`, `health`, `learning`, `money`, `home`, `community`, `spiritual`, `creative`, `personal-practice`, `therapy`, `coaching`. Anything else must be a local code `x-<namespace>:<code>` defined in the root `vocabulary`, for example `"vocabulary": {"x-sefa:course": {"definition": "Evening course on personality"}}`. Any other value fails S-3.

### Step 1. Pin the lens and record the adoption

Ask how the person came to the lens, who the coach is, and what they want to keep. Then declare the modules, list the Parties, pin the lens (`sha256` of the descriptor file you read: `shasum -a 256 spec/lenses/hexaco.lens.json`) and write the LensAdoption into `lensAdoptions`.

```json
"conformance": {"level": "L1", "modules": ["core", "governance", "lenses"], "subjectIsAdult": true},
"parties": [
  {"id": "p-01", "partyKind": "person", "label": "Coach", "role": "practitioner"},
  {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}
],
"lenses": [{"id": "urn:ohc:lens:hexaco", "version": "0.2.0", "sha256": "37e5ebddae7e8c9b6dc571d5b78cb9f056312db9d8bb2753bb5e640ecfa92a0a"}]
```

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:hexaco", "version": "0.2.0"}, "route": "inherited-from-practice",
 "practice": {"role": "coach", "practitioner": "p-01", "relationship": "active", "since": "2026-05-01", "releaseRef": "src-02"},
 "confidentiality": "practitioner-scope",
 "uses": ["speak-in-lens", "store-results", "interpret"],
 "interpretationAuthors": ["subject", "p-01"], "agentInterpretation": "allowed",
 "representationPreference": "hexaco.score-profile", "onEnd": "ask",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-06-05T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-forward"], "synthetic": true}
```

- `practice.role`: `coach`, `teacher` or `therapist` (the lens's `inheritanceRoles`).
- `confidentiality: "practitioner-scope"`: material from the coaching stays within that relationship. Use `therapy-confidential` for a therapist; it forces tier `special` and handling `person-only` on every record that cites the adoption (LA-4).
- `uses` records what the person agreed to: `speak-in-lens`, `store-results`, `interpret`, `offer-practices`, `recall`. OHC 0.1 does not enforce it: no rule ties a record to `uses`. So you and the holder keep to it yourselves (§6). Sefa did not agree to `offer-practices`, so nobody offers her the toolkit.
- `interpretationAuthors` lists which people besides the person may write readings through the lens: here the coach. Agents are not governed by this list: an agent reads through the lens under an `infer` grant that names it (I5).
- `agentInterpretation: "allowed"` lets an agent with such a grant read through the lens; here that is the companion under `g-02`. Since 0.1.0-draft.2 this field governs agent and software authors only, so `off` would keep agents out and still admit the coach's remark in step 5 (I5).
- `onEnd: "ask"`: see "When the practice relationship ends" in §2.
- `handling: ["no-forward"]` on the adoption: it names the coach and the relationship. A Grant with a `lenses` selector for this lens serves the adoption itself (and any `from-lens` Practice), not only the scores. Whoever receives it must not pass it on; if a recipient should not see it at all, exclude `la-01` by id in that Grant.

**Who sees it:** the person only. Adopting a lens gives the coach no access.

### Step 2. Keep the coach's release and the score sheet as Sources

Store both files in the vault. Compute the three values from each file itself; never type them:

- `sha256`: the SHA-256 of the file's bytes, in lowercase hex (`shasum -a 256 <file>` or `sha256sum <file>`);
- `size`: the file's length in bytes (`wc -c < <file>`);
- `vaultPath`: `vault/<first two characters of the sha256>/<sha256>.<extension>`, relative to the folder that holds `context.json`.

The checker only compares `sha256` with the name in `vaultPath` (SR-3). It never opens vault files (`vaultContentRead: false`), so a wrong hash, a wrong size or a missing file passes unnoticed (§6).

First the coach's release, because the adoption and the score sheet point to it; then the score sheet, under the coach's custody.

```json
{"id": "src-02", "sourceKind": "practitioner-release",
 "content": {"locator": {"vaultPath": "vault/81/8112e383267bcb3907a5cbe6836fa0a9d308eec177ee39a4a40058e828cf805b.md"},
             "sha256": "8112e383267bcb3907a5cbe6836fa0a9d308eec177ee39a4a40058e828cf805b",
             "mediaType": "text/markdown", "size": 169},
 "capturedAt": "2026-06-03T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "participants": ["p-01"], "maxRelease": "index",
 "retention": {"eraseOnRequest": true}, "contexts": ["coaching"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-06-05T17:50:00Z",
 "sensitivity": "sensitive", "synthetic": true}
```

```json
{"id": "src-01", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/cf/cff3fcabb7196645be4bffd1029c62a93f6d1a79855f06dce3224114fd604bc8.json"},
             "sha256": "cff3fcabb7196645be4bffd1029c62a93f6d1a79855f06dce3224114fd604bc8",
             "mediaType": "application/json", "size": 511},
 "capturedAt": "2026-06-03T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "participants": ["p-01"],
 "custody": {"custodian": "p-01", "confidentiality": "coaching", "releaseRef": "src-02"},
 "maxRelease": "index",
 "retention": {"eraseOnRequest": true}, "contexts": ["coaching"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-06-05T17:55:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- `custody` names the coach as custodian and the release as `releaseRef`. `custody.confidentiality` depends on the practitioner:

  | Practitioner | `custody.confidentiality` | `contexts` |
  |---|---|---|
  | coach | `coaching`: a grantee gets at most `excerpt` with a release, `index` without one (§15.3) | `["coaching"]` |
  | therapist | `therapy`: at most `summary` with a release, `index` without one | `["therapy"]` |
  | teacher | `none`: OHC 0.1 has no code for teaching (§6). Do not borrow `coaching`; `maxRelease: "index"` is what protects the file. | `["learning"]` |

  Keep `maxRelease: "index"` in every case.
- If the person took the questionnaire on their own (in a study), leave out `custody`, and use as `authorship.author` the Party that produced the sheet.
- Never paste sheet or note text into `summary`, `title` or `note` (SR-4).

**Who sees them:** the person, in full. A grantee at most at the `index` tier, and only when a Grant names the Source.

### Step 3. Record the scores as AssessmentRecords

Copy only numbers, and only what the sheet prints. Put Honesty-Humility and its facets in a record of their own.

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:hexaco", "version": "0.2.0"},
 "instrument": {"id": "urn:ohc:instrument:hexaco-pi-r", "form": "100"},
 "mode": "self-report-instrument", "assessedBy": "subject",
 "administeredAt": {"start": "2026-06-03", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "hexaco/E", "label": "Emotionality", "raw": 3.0, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/X", "label": "eXtraversion", "raw": 3.4, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/A", "label": "Agreeableness (versus Anger)", "raw": 3.2, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/C", "label": "Conscientiousness", "raw": 4.1, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/O", "label": "Openness to Experience", "raw": 3.6, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/altruism", "label": "Altruism (interstitial scale)", "raw": 3.8, "rawRange": [1, 5]}],
 "validityFlags": [],
 "source": "src-01",
 "reviewAfter": "P3Y",
 "origin": "derived", "derivedFrom": ["src-01"],
 "generatedBy": {"software": "coach's score sheet", "method": "means of keyed items on a 1-5 scale, with the authors' published scoring"},
 "assertedBy": "p-01", "recordedBy": "subject", "recordedAt": "2026-06-05T18:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "contexts": ["coaching"],
 "note": "The score sheet names no norm group; raw means only.", "synthetic": true}
```

```json
{"id": "as-02", "lens": {"id": "urn:ohc:lens:hexaco", "version": "0.2.0"},
 "instrument": {"id": "urn:ohc:instrument:hexaco-pi-r", "form": "100"},
 "mode": "self-report-instrument", "assessedBy": "subject",
 "administeredAt": {"start": "2026-06-03", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "hexaco/H", "label": "Honesty-Humility", "raw": 3.9, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/H/sincerity", "label": "Sincerity (facet)", "raw": 4.0, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/H/fairness", "label": "Fairness (facet)", "raw": 4.5, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/H/greed-avoidance", "label": "Greed Avoidance (facet)", "raw": 3.2, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "hexaco/H/modesty", "label": "Modesty (facet)", "raw": 3.9, "rawRange": [1, 5]}],
 "validityFlags": [],
 "source": "src-01",
 "reviewAfter": "P3Y",
 "origin": "derived", "derivedFrom": ["src-01"],
 "generatedBy": {"software": "coach's score sheet", "method": "means of keyed items on a 1-5 scale, with the authors' published scoring"},
 "assertedBy": "p-01", "recordedBy": "subject", "recordedAt": "2026-06-05T18:06:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-forward"], "contexts": ["coaching"],
 "note": "Honesty-Humility kept apart: it is never shown to anyone but Sefa unless she names it in a grant.",
 "synthetic": true}
```

The coach scored the sheet, so both records are the coach's assertion (`assertedBy: "p-01"`) recorded by the person. They are `proposed` until the person admits them, in person (R-A1):

```json
{"id": "rv-01", "target": ["as-01", "as-02"], "action": "admit", "by": "subject", "recordedAt": "2026-06-05T18:10:00Z"}
```

Fill the fields like this:

| Field | Value |
|---|---|
| `lens` | `{"id": "urn:ohc:lens:hexaco", "version": "0.2.0"}` |
| `instrument` | `{"id": "urn:ohc:instrument:hexaco-pi-r", "form": "60" \| "100" \| "200"}`, the form printed on the sheet. The 60-item form is a subset of the 100-item form. Add `version` only for an edition printed on the sheet (not the catalog entry's `0.1.0`); this sheet prints none. The checker does not check `form`, so copy it exactly (§6). |
| `mode` and `origin` (AR-1) | The person answered the questionnaire: `self-report-instrument` with `origin: "derived"`, `derivedFrom` (the Source) and `generatedBy` with a `method`. Another person rated them: `observer-report` with `assessedBy` (that rater's Party id) and `raterRelationship`. |
| `results` | One `dimension-score` per construct the sheet prints, with ids from the descriptor. The six dimensions: `hexaco/H`, `hexaco/E`, `hexaco/X`, `hexaco/A`, `hexaco/C`, `hexaco/O`. Their 24 facets: `hexaco/H/sincerity`, `hexaco/H/fairness`, `hexaco/H/greed-avoidance`, `hexaco/H/modesty`; `hexaco/E/fearfulness`, `hexaco/E/anxiety`, `hexaco/E/dependence`, `hexaco/E/sentimentality`; `hexaco/X/social-self-esteem`, `hexaco/X/social-boldness`, `hexaco/X/sociability`, `hexaco/X/liveliness`; `hexaco/A/forgivingness`, `hexaco/A/gentleness`, `hexaco/A/flexibility`, `hexaco/A/patience`; `hexaco/C/organization`, `hexaco/C/diligence`, `hexaco/C/perfectionism`, `hexaco/C/prudence`; `hexaco/O/aesthetic-appreciation`, `hexaco/O/inquisitiveness`, `hexaco/O/creativity`, `hexaco/O/unconventionality`. The interstitial scale: `hexaco/altruism`. Record only what the sheet prints: a form-60 sheet normally gives the six dimensions only, with no facets and no Altruism. Never a `big-five/…` id. `raw` and `rawRange` as printed; `standardized` only when the sheet gives it. |
| `normGroup` | The norm sample the sheet names. This sheet names none, so `normGroup` is left out and `note` says so; say "no norm group" whenever the scores are shown. |
| `reviewAfter`, `sensitivity`, `categories` | `P3Y`, `special`, `["mental-health"]`. |
| `handling` | `no-forward` on the Honesty-Humility record. `subject-initiated-only` on a record with the Anxiety or Fearfulness facets, if the person stores them (Sefa did not). |

**Who sees them:** the person. A grantee only when a Grant names the lens, the category or the id under explicit consent. `as-02` also travels with `no-forward`: a grantee that receives it never passes it on.

### Step 3b. Only if the person asks: an agent's estimate

Whether you may make an estimate is the person's Grant: one that gives you both `suggest` and `infer` and names the lens (`g-02` in step 7). In the example Sefa asks the companion for a rough guess at eXtraversion, to compare with the coach's sheet. The estimate rests on episodes the person told you about (`ep-02`, step 5).

```json
{"id": "as-03", "lens": {"id": "urn:ohc:lens:hexaco", "version": "0.2.0"},
 "mode": "agent-inference", "assessedBy": "a-01",
 "administeredAt": {"start": "2026-06-20", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "hexaco/X", "raw": 2.8, "rawRange": [1, 5]}],
 "validityFlags": ["agent-estimate-not-validated"], "validityCeiling": "agent-estimate-not-validated",
 "derivedFrom": ["ep-02"],
 "origin": "inferred", "assertedBy": "a-01", "recordedAt": "2026-06-20T10:00:00Z",
 "underGrant": "g-02", "purpose": "self-reflection", "epistemic": "hypothesis",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["person-only"],
 "note": "Asked for by Sefa: a rough guess from one episode, to compare with the coach's sheet.",
 "synthetic": true}
```

Sefa declines it; the estimate stays in history, unused. To keep one, the person writes `"action": "admit"` instead. Either Review goes into `reviews`, and only the person writes it (R-A1).

```json
{"id": "rv-03", "target": "as-03", "action": "decline", "by": "subject", "recordedAt": "2026-06-21T08:00:00Z",
 "note": "One evening says little; I keep the coach's sheet."}
```

- AR-2 requires all of these: handling `person-only`, the flag and ceiling `agent-estimate-not-validated`, and no `trademarkNotice` or branded label.
- `derivedFrom` names the episodes the guess rests on. Leave `label` out: it is a guess, not a measured result. No `instrument`.
- INF-1 needs the Grant named in `underGrant` to be given to you, to hold `suggest` **and** `infer`, to list the `purpose`, to reach the record (here through its `lenses` selector) and to be valid at `recordedAt`.
- Never estimate Honesty-Humility (`hexaco/H` or its facets) for anyone but the person who asked. OHC 0.1 cannot forbid an estimate of one construct; the checker would accept it (§6).

**Who sees it:** the person only, always (`person-only`); not even you receive it back in a projection.

### Step 4. Claims the person accepts

Show the score profile: raw score and range, and the norm group or the words "no norm group". Ask which tendencies the person recognises and where. Write a Claim only for what they say yes to.

```json
{"id": "c-01", "facet": "disposition", "predicate": "assessed-trait",
 "text": "Conscientiousness: raw 4.1 on a 1-5 scale (HEXACO-PI-R, 100-item self-report, scored by my coach, June 2026; no norm group).",
 "horizon": "foundation", "reviewAfter": "P3Y",
 "origin": "derived", "derivedFrom": ["as-01"],
 "generatedBy": {"software": "holder app", "method": "one result line of as-01 restated with instrument, form and date"},
 "assertedBy": "subject", "recordedAt": "2026-06-08T19:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "c-02", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "I plan ahead and finish what I promise, sometimes to the point of checking things twice.",
 "horizon": "foundation", "evidence": [{"ref": "as-01", "kind": "instrument"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-06-08T19:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- A result line the person accepts (`c-01`): facet `disposition`, predicate `assessed-trait`, `origin: "derived"`, `derivedFrom` the AssessmentRecord, `generatedBy.method` (CL-3).
- The same tendency in the person's own words (`c-02`): predicate `self-described-tendency`, `origin: "declared"`, `evidence` with kind `instrument`.
- Ask separately before writing any Claim about Honesty-Humility, and give such a Claim handling `no-forward`. Sefa wrote none.
- A preference the person chooses after seeing the profile (for example how they want feedback) is an ordinary `preference` Claim **without** a citation of the result, so it does not become special (C3).

**Who sees them:** both Claims are special (they cite the result) and reach only a Grant that names them by id or by the category `mental-health`; a `lenses` selector does not reach them (§6).

### Step 5. Readings through the lens: the person's fit check and the coach's remark

The descriptor's toolkit item `hexaco.fit-check` compares one dimension with three recent episodes and notes fit or no fit; its product is an Interpretation. Ask the descriptor's questions: "Where do you recognise fairness and modesty in how you act?" and "Where does the score not fit your experience?"

1. Write the episodes the person tells you about. `contexts` takes the codes listed in step 0.

```json
{"id": "ep-01", "title": "Quote for a new client", "occurred": {"start": "2026-06-09", "precision": "day"},
 "accounts": [{"narrator": "subject", "narratedAt": "2026-06-09T18:00:00Z", "addedAt": "2026-06-09T18:00:00Z",
               "accountKind": "in-the-moment", "happened": "Sent a new client a quote at my usual rate, although a colleague suggested doubling it.",
               "understandingThen": "The usual rate is what the work is worth."}],
 "contexts": ["work"], "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-06-09T18:00:00Z", "synthetic": true}
```

```json
{"id": "ep-02", "title": "Client evening", "occurred": {"start": "2026-06-16", "precision": "day"},
 "accounts": [{"narrator": "subject", "narratedAt": "2026-06-16T22:00:00Z", "addedAt": "2026-06-16T22:00:00Z",
               "accountKind": "in-the-moment", "happened": "Went to a client evening, talked with two people I already knew and left after an hour."}],
 "contexts": ["work"], "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-06-16T22:00:00Z", "synthetic": true}
```

2. The person's fit check. It is about Honesty-Humility, so it carries `no-forward` like the record it reads; OHC does not copy handling for you (§6).

```json
{"id": "in-01", "about": ["as-02", "ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:hexaco", "version": "0.2.0"},
 "text": "Fit check, Honesty-Humility: the Fairness facet fits this quote; Greed Avoidance I am less sure of.",
 "facets": ["disposition"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-06-09T18:10:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-forward"], "synthetic": true}
```

3. A coach's remark the person wants to keep is the coach's Interpretation, recorded by the person. Because the author is not the subject, it needs `adoption`, `epistemic: "hypothesis"`, grounds, at least two alternatives (one not psychological) and limits (I1, I4, I5). Say in `limits` who added the alternatives if the coach did not give them.

```json
{"id": "in-02", "about": ["as-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:hexaco", "version": "0.2.0"}, "adoption": "la-01",
 "text": "High Conscientiousness with middling Agreeableness may be why you take over colleagues' unfinished tasks instead of asking them.",
 "causal": "hypothesized",
 "grounds": [{"ref": "as-01", "kind": "instrument"}],
 "alternatives": [
   {"text": "The team is one person short this quarter.", "kind": "situational"},
   {"text": "Nobody else has access to the client files.", "kind": "informational"}],
 "limits": "A coach's remark in one session, written down by Sefa the same evening; the two alternatives are Sefa's.",
 "facets": ["disposition"], "contexts": ["coaching"],
 "origin": "declared", "assertedBy": "p-01", "recordedBy": "subject", "recordedAt": "2026-06-10T20:00:00Z",
 "epistemic": "hypothesis",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

4. The person decides on the coach's remark:

```json
{"id": "rv-02", "target": "in-02", "action": "partially-endorse", "by": "subject", "recordedAt": "2026-06-11T08:00:00Z",
 "endorsedPart": "I do take over unfinished tasks at work."}
```

Never write a reading that treats Honesty-Humility as a moral verdict or as trustworthiness. An agent writes readings through this lens only under a Grant with `suggest` and `infer` that names the lens, and only while the person's active adoption does not say `off` (I5).

**Who sees them:** the episodes are sensitive and reach only Grants that name the kind or the id. The readings are special: a Grant must name the lens (or the id) and allow interpretations (R-G8). `in-01` also carries `no-forward`.

### Step 6. Practices

The toolkit has one item, the fit check, and its product is the Interpretation of step 5. Sefa keeps no practice, so the example has no Practice. To keep the fit check as a repeated practice, write a Practice with `id`, the person's own `name`, `practiceKind: "reflection"`, `"source": {"route": "from-lens", "lens": "urn:ohc:lens:hexaco", "templateId": "hexaco.fit-check"}`, `nonClinical: true`, `origin: "declared"`, `assertedBy: "subject"` and `recordedAt`. Record each use as an Outcome with `id`, `"about": {"practice": "<practice id>"}`, a `result` (`helped`, `partly`, `no-effect`, `worse`, `unclear` or `not-tried`), `origin: "declared"`, `assertedBy: "subject"` and `recordedAt`. Add `"practices"` to `conformance.modules`. An agent offers the fit check (`agentMayOffer: true`) only if the adoption's `uses` has `offer-practices`. A `from-lens` Practice counts as a record of the lens: every Grant with a `lenses` selector for HEXACO receives it.

### Step 7. Who may see what

Nothing leaves the context without a Grant. The coach gets the results for the coaching sessions, without Honesty-Humility. The companion may read the lens's records, Honesty-Humility included because Sefa names it, the two dispositions and the episodes; it may make an estimate when Sefa asks, but does not interpret.

```json
{"id": "g-01", "recordedAt": "2026-06-12T09:00:00Z", "grantor": "subject", "grantee": "p-01",
 "purposes": ["coaching"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:hexaco"]}],
           "exclude": [{"ids": ["as-02", "in-01"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2026-12-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-06-12T09:00:00Z", "channel": "holder-ui"},
 "note": "For our coaching sessions; Honesty-Humility stays with me."}
```

```json
{"id": "g-02", "recordedAt": "2026-06-12T09:05:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:hexaco"]}, {"ids": ["as-02", "in-01", "c-01", "c-02"]}, {"kinds": ["Episode"]}]},
 "actions": ["read", "suggest", "infer"], "mode": "full", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2026-12-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "reviewCadence": "P7D",
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-06-12T09:05:00Z", "channel": "holder-ui"},
 "note": "The companion may talk with me in HEXACO terms, including Honesty-Humility, and make a rough estimate when I ask for one; it does not interpret through the lens."}
```

- Every Grant that reaches records of this lens, or that holds `infer`, uses `basis.legal: "explicit-consent"` and expires within 180 days (R-G10, GR-1, GR-4).
- Honesty-Humility (`as-02`, `in-01`) is excluded by id from the coach's Grant. Sefa asked that the companion have it, so `g-02` names both ids in `include`; it travels with `no-forward`.
- A `lenses` selector serves every record that carries the lens: the LensAdoption (with the coach's name and relationship), the AssessmentRecords, the readings and any `from-lens` Practice, not only the scores (§6). Exclude by id what a recipient should not have.
- `actions`: `suggest` and `infer` together let the companion write its own estimates as proposals (step 3b). Leave both out for a recipient who should only read, as for the coach.
- Never grant records of this lens to anyone in a work setting: the descriptor warns that disclosing Honesty-Humility at work risks reputational harm, and every work purpose that would judge the person is prohibited.
- `expressedBy` is how the person said yes; your statement that "the person agreed" is never consent.

### Step 8. Check

From the specification repository, run the checker on the folder of step 0:

```sh
python3 -B tools/check.py <folder> --level L1 --json
```

Fix every error. The checker never prints your values. It checks shape and rules, not truth or consent. It also does not open vault files, so check `sha256` and `size` against the files yourself with the commands of step 2.

## 4. Never

- **Never for these purposes,** under any grant: personnel selection, task allocation, performance evaluation, promotion decisions, ranking against other people, persuasion targeting, and the other prohibited purposes (§8.10). A result grounds a choice you propose for the person only under the grant's `decisionUse: approval-required`, only when the person accepted it, naming what you weighed (R-G14).
- **Never** treat Honesty-Humility as a measure of trustworthiness or moral character, and never comment on it to anyone but the person.
- **Never** comment on the facets Anxiety or Fearfulness unless the person raises them.
- **Never** suggest that the person suits or does not suit a job or role; never present results as clinical states; never predict a single moment from a trait.
- **Never** translate HEXACO scores into Big Five scores, and never declare a HEXACO id equal to a Big Five id (M-1). The catalog row `hexaco--big-five--ashton-lee-2007` is `corresponds` with `rowStatus: not-identity`; it can never produce a cross-lens estimate (AR-7).
- **Never** store HEXACO-PI-R item text or report prose. Never run the HEXACO-PI-R yourself in a product or service: online administration is allowed only on password-protected or not-searchable pages, and non-academic use requires contacting the authors.
- **Never** make an agent estimate unless the person asked, without a Grant that gives you both `suggest` and `infer`, or without `person-only`. Never estimate Honesty-Humility for anyone but the person who asked.
- **Trademarks:** the catalog records no marks for this lens or its instrument.

## 5. Worked example

[examples/hexaco/context.json](examples/hexaco/context.json) is a single-document context for Sefa, a fictional person whose coach used the HEXACO-PI-R. Every record carries `"synthetic": true`. It contains exactly the records of §3: `la-01`, `src-02` and `src-01` (with their vault files), `as-01`, `as-02` and `rv-01`, `as-03` and `rv-03`, `c-01` and `c-02`, `ep-01` and `ep-02`, `in-01`, `in-02` and `rv-02`, and `g-01` and `g-02`. The `agent-suggested` snippet of §2 (`rv-00`) and the teacher row of step 2 are alternatives, not part of the example; each was checked separately and passes L1.

```sh
python3 -B tools/check.py docs/lenses/examples/hexaco --level L1 --json
```

Result: `"valid": true`, `"levelMet": "L1"`, no errors and no warnings. The expected output is kept in [examples/hexaco/expected-check.json](examples/hexaco/expected-check.json).

## 6. What does not fit yet

Each item is recorded for the next revision of the standard.

1. **A practitioner's reading depends on `agentInterpretation`.** *Resolved in 0.1.0-draft.2:* I5 applies `agentInterpretation` to agent and software authors only; a coach's reading needs the coach in `interpretationAuthors` of the active adoption.
2. **Alternatives without an author.** I4 requires two alternatives on any non-subject reading, also on a coach's remark the person writes down. The person has to add alternatives the coach did not give, and nothing says who added them (only `limits` text).
3. **Handling does not follow citations.** C3 carries tier and categories along citations, not handling. `in-01` reads the `no-forward` record `as-02` and had to copy `no-forward` by hand.
4. **No handling per construct in the descriptor.** "Do not comment on Honesty-Humility to anyone but the person" and "do not comment on Anxiety or Fearfulness unless raised" can only be kept by splitting records; `defaults.perConstruct` has no `handling`, and this descriptor has no `perConstruct` at all.
5. **Instrument terms are free text.** "Online use only on password-protected or not-searchable pages" and "non-academic use: contact the authors" have no machine-readable form an agent could check before offering the questionnaire. The `forms` list also does not say whether a form is for self-report or observer report.
6. **Ending a practice relationship leaves the practitioner's Grant in place.** `onEnd` pauses or ends the adoption; the coach's Grant must be withdrawn separately, and nothing flags it.
7. **"No norm group" cannot be stated.** The descriptor tells a helper to show the norm group with every score; when a sheet names none, the record can only leave `normGroup` out and explain in `note`.
8. **Claims drawn from a result lose their lens.** A `lenses` selector does not reach `c-01` and `c-02`; every Grant must name them by id.
9. **Construct ids are not checked.** The checker would accept `big-five/E` in a HEXACO record, the very aliasing M-1 forbids.
10. **The import tool writes invalid records.** `tools/import_assessment.py` puts `percentile` directly into a `dimension-score` result, which the schema rejects (S-3); the `imported` route therefore needs a hand fix.
11. **`uses` and `agentInterpretation` have no force over results and estimates.** No rule ties a record to an active adoption of its lens or to its `uses`. An agent estimate passes L1 with an adoption whose `uses` is `["store-results"]` and whose `agentInterpretation` is `off`; AssessmentRecords and readings by the person pass with no LensAdoption at all. Only I5 looks at the adoption, and only for readings by someone other than the person.
12. **No code for teaching in custody.** `Source.custody.confidentiality` is `none`, `therapy`, `coaching`, `legal` or `medical`, although the lens lists `teacher` as an inheritance role. A teacher's material must either borrow `coaching` or carry no custody ceiling.
13. **No per-construct limit on agent estimates.** "Never estimate Honesty-Humility for anyone but the person" cannot be written: a Grant names a lens, an id or a category, never a construct, so an agent estimate on `hexaco/H` passes L1 under any `infer` grant for the lens.
14. **A `lenses` selector serves more than results.** It matches every record with a `lens` field and every Practice with `source.lens`: projecting through the coach's Grant gives the LensAdoption (practice block, relationship, `onEnd`) and any `from-lens` Practice, not only the scores. A person granting "my HEXACO results" cannot see that from the Grant.
15. **The person's request for a suggestion cannot be recorded.** `adoption.suggestionRequires` says when a suggestion usually makes sense (after the person asked for ways of describing tendencies); LensAdoption has no field for that request, so it lives in `note`.
16. **`form` is not checked, and `instrument.version` has no defined meaning.** `form: "999"` passes L1 (AR-8 checks only the instrument id). It is not said whether `version` is the publisher's edition or the catalog entry's version, and instrument entries cannot be pinned by `sha256` the way lenses are.
17. **Vault files are never compared with their description.** The checker does not read vault files (`vaultContentRead: false`); SR-3 only checks that `sha256` matches the name in `vaultPath`. A wrong `size`, a wrong hash used the same way in `vaultPath`, or a missing file passes L1.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
