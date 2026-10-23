# Psychological type: how to bring a person's material into OHC

**Recipe · lens `urn:ohc:lens:jungian-type` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe turns a person's psychological-type material (a genuine MBTI® result they received, their own best-fit type, and the situations where the other pole shows) into OHC records step by step, so that the person stays the authority on their type and no branded label lands on anything that is not a genuine result.

The lens descriptor is `spec/lenses/jungian-type.lens.json` (`descriptorStatus: draft`, `legalReviewNeeded: true`). It is a full descriptor, not a stub. Its evidence tier is `T4` (contested): the measures behind it are continuous, and the claim that people fall into distinct types is not supported. Read its `mentalModel`, `ip` and `defaults` before you start; they are the facts and guidance this recipe applies. **In OHC 0.1 a context holding these results passes the checker only at L0** (§6, items 1 and 2), so you also run the L1 rules and read their output yourself (step 8).

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them.

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:jungian-type-basic`](../../spec/playbooks/jungian-type-basic.playbook.json) (Psychological type: basic ways of working, by the OHC editors), for these situations: preparing a hard conversation; giving feedback to someone; planning the week ahead; looking back at something that happened. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

**Bringing a report through the person's window.** When an instrument's catalog entry carries an `import` block, a person can bring its result through their own window ([guide](../guides/BRING-A-RESULT.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). No entry of this lens has one yet, so the steps below record the report by hand.

## 1. What you may have

| Input | Example | Where it goes |
|---|---|---|
| Self-description in conversation | "I'm an introvert; I think best alone." | A Claim in the person's words (step 4). |
| The person's own best-fit type | After reading short descriptions of each pole, the person chooses the one that fits best on each pair | An AssessmentRecord with `mode: self-identified` (step 3b). |
| A genuine MBTI® report the person owns | An MBTI® Form M or Form Q (Step II™) report from a certified facilitator | The report file is a Source (step 2); the reported preferences are an AssessmentRecord with the trademark notice (step 3a). |
| A type from a free online quiz or another "16 types" test | A four-letter code from a website | Not a genuine MBTI® result and not one of the lens's instruments. If the person recognises it, record it as their own best fit (step 3b) or in their own words (step 4); never with the MBTI® marks. |
| Notes from coaching, teaching or facilitation where type was used | A facilitator's workshop notes | Adoption route `inherited-from-practice` (step 1); the notes are a Source with the facilitator as custodian, plus the facilitator's release (step 2). A facilitator's reading cannot be recorded in 0.1 (§6). |
| An agent's reading | "From our talks you sound like an introvert" | **Only under the person's Grant.** It needs `suggest` and `infer` naming the lens, and the person's active adoption not set to `off` (I5); an estimate is person-only and a proposal (AR-2), never a type assigned to the person. In the example the person grants neither. |

The lens lists two instruments: `urn:ohc:instrument:mbti-form-m` (form `M`) and `urn:ohc:instrument:mbti-form-q` (form `Q`). Both are proprietary (The Myers-Briggs Company); scoring is proprietary; item text, report prose, scoring keys and raw responses are never stored.

**What you may offer.** The toolkit has two items. You may offer the best-fit check (`jungian-type.best-fit`, `agentMayOffer: true`; step 3b). You never offer to record a genuine result (`jungian-type.record-genuine-result`, `agentMayOffer: false`): the person brings the report, and only then do you follow step 3a.

## 2. Before you start

**Route of adoption.** Choose the one that matches how the person came to the lens. It goes into `LensAdoption.route`.

| Route | When | What it changes |
|---|---|---|
| `self-chosen` | The person picked the lens on their own. | The adoption is active as soon as it is written. |
| `agent-suggested` | You mentioned the lens, under a Grant that lets you (`suggest`, with a selector naming the lens). The descriptor's `adoption.suggestionRequires` says when that usually makes sense: after the person asked for ways of describing their preferences. | Add `suggestedBy` with your Party id. The adoption stays `proposed` until the person admits it with a Review `admit` (LA-1); see the snippet below. |
| `inherited-from-practice` | The lens came from a coach, teacher or facilitator (`adoption.inheritanceRoles`), for example a facilitator who ran the questionnaire at a workshop and handed over the report. This recipe's example takes this route. | Add a `practice` block: `role`, `practitioner` (a Party id), `relationship`, `since`, and `releaseRef` (a Source holding the practitioner's release). Set `confidentiality` and `onEnd`. **LA-3 applies whenever a stored Source is authored by the practitioner or in their custody, the report included**: then `releaseRef` is required. The adoption gives the practitioner no access (LA-2). |
| `imported` | An importer created the adoption from a report. | The adoption is `proposed` until the person admits it, and so is every AssessmentRecord from the same import run (LA-5). |

In the example `agentInterpretation` is `off`, the default, and `interpretationAuthors` is `["subject"]`: the person keeps readings through this lens to themselves. They may change either (I5).

**The `agent-suggested` route in records.** The adoption stays the person's (`assertedBy: "subject"`); add `"suggestedBy": "<your Party id>"` and write the person's request in `note`, in their words (OHC 0.1 has no field for it; §6). Then the person's admit goes into `reviews`; only the person admits (LA-1):

```json
{"id": "rv-00", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-04-20T18:01:00Z"}
```

**Consent.** Ask before each step and read every record back before it is saved. The person can stop at any step. This lens gives an agent nothing to infer, so no Grant needs `infer` or `suggest`.

**Who writes.** The person's own holder writes every record of this lens with `assertedBy: "subject"`. If you are an agent with a Grant that gives you `write`, you may write the person's own confirmed statements with `recordedBy` set to your Party id. A reading or an estimate of your own is a proposal and needs the person's Grant (`suggest` and `infer` naming the lens); you never assign a type to the person.

**Defaults for this lens** (`defaults` in the descriptor):

- `sensitivity: "special"`: every record of this lens is treated as special category. A Grant reaches it only by naming its id, its lens or its category, under explicit consent (R-G3).
- `categories: ["mental-health"]`.
- `reviewAfter: "on-change"`: the person revises the type whenever they want. AssessmentRecord `reviewAfter` accepts only a duration, so leave it out (§6).

**Trademarks.** "MBTI", "Myers-Briggs" and "Myers-Briggs Type Indicator" are registered marks of the Myers & Briggs Foundation, Inc. (`ip.marks`, `use: adjective-only`). Use them only as adjectives ("an MBTI® Form M result") and only for genuine results from the publisher's instrument. Every genuine result carries the `trademarkNotice` from the descriptor. The Form Q instrument entry adds a fourth mark, "Step II", with its own notice (step 3a).

**Never stored.**

- MBTI® item text, item responses, scoring keys and report prose (`ip.restrictions`, the instruments' `neverStore`). The report's type descriptions are report prose: never copy them into any record, including a Claim.
- A branded label on anything that is not a genuine result: not on a best-fit check, a quiz, a Big Five profile or a guess (M-4).
- A type derived from other data, such as Big Five scores (M-4).
- A type as a judgement of the person, or as a kind of person.

## 3. Steps

Each step says what to do, which record to write, a JSON snippet that validates against `spec/schema/*.schema.json`, and who sees the record by default. The snippets are the records of the worked example (§5), in its single-document form: each goes into the array named in the step. **By default nobody but the person sees anything** (R-G1); step 7 is where that changes.

### Step 0. The file and its folder

One context is one folder. All records go into one file, `context.json`. The original files (the report, a release, notes) go next to it under `vault/`. You run the checker on the folder (step 8).

```text
<folder>/
  context.json
  vault/cd/cd7c35baaea6c4149af45f1cd8e3279f15289d079fd444b0e871dcab108d37d0.md
  vault/6f/6f5960410d0549d75304f8dc6d613a02b0747008f95b9c10c95a059e80c5e0c4.json
```

Start `context.json` with its root. These are the root fields of the worked example:

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:ohc:example:ilari:jungian-type", "version": "2026-05-10.1",
 "subject": {"id": "urn:ohc:example:ilari", "displayName": "Ilari (fictional)"},
 "holder": "subject", "lang": "en", "created": "2026-04-20T18:00:00Z",
 "policy": {"admission": "subject-only", "resolver": "returnDialog"},
 "synthetic": true}
```

- `format`, `specVersion`, `id`, `version` and `subject` are required (`spec/schema/context.schema.json`).
- `id` and `subject.id`: for a real person, a `urn:uuid:` you generate, never a name or an email. `urn:ohc:example:<name>[:<context>]` is for examples only.
- `version`: any text you choose; change it whenever you change the file.
- `synthetic: true` only in examples, where it goes on the root and on every record. Leave it out for a real person.
- Add to the same object `conformance`, `parties` and `lenses` (step 1), then the arrays this recipe fills: `lensAdoptions` (step 1), `sources` (2), `assessments` (3a, 3b), `tensions` (3c), `claims` (4), `episodes` and `interpretations` (5), `grants` (7). Leave out any array you do not use.
- **Codes for `contexts`** (on any record that has the field): `work`, `family`, `partner`, `friends`, `health`, `learning`, `money`, `home`, `community`, `spiritual`, `creative`, `personal-practice`, `therapy`, `coaching`. Anything else must be a local code `x-<namespace>:<code>` defined in the root `vocabulary`, for example `"vocabulary": {"x-ilari:workshop": {"definition": "Career workshop"}}`. Any other value fails S-3.

### Step 1. Pin the lens and record the adoption

Ask how the person came to the lens and what they want to keep. Then declare the modules, list the Parties, pin the lens (`sha256` of the descriptor file you read: `shasum -a 256 spec/lenses/jungian-type.lens.json`) and write the LensAdoption into `lensAdoptions`. The example declares level `L0` because of the known gap in step 3.

```json
"conformance": {"level": "L0", "modules": ["core", "governance", "lenses"], "subjectIsAdult": true},
"parties": [
  {"id": "p-01", "partyKind": "person", "label": "Workshop facilitator", "role": "practitioner"},
  {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}
],
"lenses": [{"id": "urn:ohc:lens:jungian-type", "version": "0.2.0", "sha256": "d6c8bd4a50aae2a7b7aba9372ddc3c042fa5fc5a77b8f147b8a12898c3804d69"}]
```

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:jungian-type", "version": "0.2.0"}, "route": "inherited-from-practice",
 "practice": {"role": "facilitator", "practitioner": "p-01", "relationship": "ended", "since": "2026-04-18", "releaseRef": "src-02"},
 "confidentiality": "practitioner-scope", "onEnd": "keep-read-only",
 "uses": ["speak-in-lens", "store-results", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "representationPreference": "jungian-type.type-label",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-04-20T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- `practice`: `role` is `coach`, `teacher` or `facilitator`; `relationship` is `active` or `ended`. Ilari met the facilitator at a one-day workshop, so it is `ended`. `releaseRef` points to the facilitator's release (step 2); LA-3 requires it because the report was authored by the facilitator.
- `onEnd: "keep-read-only"`: what happens once the relationship has ended. With `ended` and `onEnd: "ask"` the adoption is paused until the person chooses `keep-read-only`, `archive-person-only` or `erase`.
- `uses` records what the person agreed to: here `speak-in-lens` (an agent may use the person's own type wording in conversation), `store-results` and `interpret` (the person's own readings may be stored). OHC 0.1 does not enforce it: no rule ties a record to `uses`. So you and the holder keep to it yourselves (§6). Only the person interprets.
- `agentInterpretation: "off"`: the default, which the person keeps here; no agent reads through the lens while this adoption is active (I5).
- `representationPreference`: the descriptor's one representation, `jungian-type.type-label` (four letters with clarity per pole and whether the person confirmed the type by best fit).

**Who sees it:** the person only.

### Step 2. Keep the facilitator's release and the genuine report as Sources

Store both files in the vault. Compute the three values from each file itself; never type them:

- `sha256`: the SHA-256 of the file's bytes, in lowercase hex (`shasum -a 256 <file>` or `sha256sum <file>`);
- `size`: the file's length in bytes (`wc -c < <file>`);
- `vaultPath`: `vault/<first two characters of the sha256>/<sha256>.<extension>`, relative to the folder that holds `context.json`.

The checker only compares `sha256` with the name in `vaultPath` (SR-3). It never opens vault files (`vaultContentRead: false`), so a wrong hash, a wrong size or a missing file passes unnoticed (§6).

First the facilitator's release (a short note saying the report is the person's to keep), because the adoption points to it:

```json
{"id": "src-02", "sourceKind": "practitioner-release",
 "content": {"locator": {"vaultPath": "vault/cd/cd7c35baaea6c4149af45f1cd8e3279f15289d079fd444b0e871dcab108d37d0.md"},
             "sha256": "cd7c35baaea6c4149af45f1cd8e3279f15289d079fd444b0e871dcab108d37d0",
             "mediaType": "text/markdown", "size": 224},
 "capturedAt": "2026-04-18T16:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "participants": ["p-01"], "maxRelease": "index",
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-04-20T17:55:00Z",
 "sensitivity": "sensitive", "synthetic": true}
```

Then the report, the person's own copy, described so that its text never travels:

```json
{"id": "src-01", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/6f/6f5960410d0549d75304f8dc6d613a02b0747008f95b9c10c95a059e80c5e0c4.json"},
             "sha256": "6f5960410d0549d75304f8dc6d613a02b0747008f95b9c10c95a059e80c5e0c4",
             "mediaType": "application/json", "size": 476},
 "capturedAt": "2026-04-18T16:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "participants": ["p-01"], "maxRelease": "index",
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-04-20T18:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-quote"], "synthetic": true}
```

- `authorship.author`: the facilitator who handed the report over (a `person` Party). Because of this, LA-3 needs `practice.releaseRef` under `inherited-from-practice`, even for a report the person owns. Under `self-chosen` LA-3 does not apply, but store the release anyway if the facilitator gave one.
- `maxRelease: "index"` and handling `no-quote`: a grantee learns at most that the report exists, and nobody but the person ever sees its words. A real report contains proprietary prose.
- The report is the person's own copy, so it has no `custody`. The facilitator's own notes are different: give them `sourceKind: "practitioner-notes"` and `"custody": {"custodian": "p-01", "confidentiality": "none", "releaseRef": "src-02"}`. OHC 0.1 has no custody code for facilitation or teaching (§6); `none` sets no ceiling, so `maxRelease: "index"` is what protects them. For a coach, use `coaching`.
- Leave `summary` out, or let the person write one line in their own words. Never paste report text into `summary`, `title` or `note`.

**Who sees them:** the person, in full. A grantee at most at the `index` tier, and only when a Grant names them.

### Step 3a. Record a genuine MBTI® result

Only for a genuine result from `mbti-form-m` or `mbti-form-q` that the person brought. Copy the reported pole and its clarity for each pair, nothing else.

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:jungian-type", "version": "0.2.0"},
 "instrument": {"id": "urn:ohc:instrument:mbti-form-m", "form": "M"},
 "mode": "vendor-report-import", "assessedBy": "subject",
 "administeredAt": {"start": "2026-04-18", "precision": "day"},
 "results": [
   {"type": "type-assignment", "construct": "jungian-type/EI", "label": "Extraversion", "clarity": "slight", "method": "instrument"},
   {"type": "type-assignment", "construct": "jungian-type/SN", "label": "Intuition", "clarity": "clear", "method": "instrument"},
   {"type": "type-assignment", "construct": "jungian-type/TF", "label": "Feeling", "clarity": "moderate", "method": "instrument"},
   {"type": "type-assignment", "construct": "jungian-type/JP", "label": "Perceiving", "clarity": "moderate", "method": "instrument"}],
 "validityFlags": ["vendor-algorithm-undisclosed"],
 "source": "src-01",
 "trademarkNotice": "Myers-Briggs Type Indicator, Myers-Briggs and MBTI are trademarks or registered trademarks of the Myers & Briggs Foundation, Inc.; The Myers-Briggs Company is the exclusive publisher of the MBTI® instrument.",
 "origin": "imported",
 "importedFrom": {"system": "MBTI® Form M report handed over at a career workshop", "importedAt": "2026-04-20T18:10:00Z"},
 "assertedBy": "subject", "recordedAt": "2026-04-20T18:10:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

| Field | Value |
|---|---|
| `instrument` | `{"id": "urn:ohc:instrument:mbti-form-m", "form": "M"}` or `{"id": "urn:ohc:instrument:mbti-form-q", "form": "Q"}`. Add `version` only for an edition printed on the report, never the catalog entry's `0.1.0`. The checker does not check `form`, so copy it exactly (§6). |
| `mode`, `origin` | `vendor-report-import` with `origin: "imported"` and `importedFrom` (`system` naming the report, `importedAt` equal to `recordedAt`) (AR-1). |
| `results` | One `type-assignment` per pair. `construct` is the pair: `jungian-type/EI`, `jungian-type/SN`, `jungian-type/TF` or `jungian-type/JP`. `label` is the reported pole in plain words. `clarity` is the clarity printed on the report. `method: "instrument"`. |
| `validityFlags` | `vendor-algorithm-undisclosed`: the scoring rule is the publisher's. |
| `trademarkNotice` | The `notice` text from the descriptor's `ip.marks`, exactly. Required on every genuine result. |
| `reviewAfter` | Leave it out (`on-change` is not a duration). |

**A Form Q (Step II™) report.** Use `{"id": "urn:ohc:instrument:mbti-form-q", "form": "Q"}` and record the same four pairs. Then:

- `trademarkNotice`: the descriptor's notice, followed by one space and the notice of the "Step II" mark from `spec/instruments/mbti-form-q.instrument.json`. OHC 0.1 does not require this second notice (it reads only the lens's marks) and the checker does not look for it; add it anyway (§6). The result:

```json
"trademarkNotice": "Myers-Briggs Type Indicator, Myers-Briggs and MBTI are trademarks or registered trademarks of the Myers & Briggs Foundation, Inc.; The Myers-Briggs Company is the exclusive publisher of the MBTI® instrument. Step II™ is a mark of the Myers & Briggs Foundation, Inc.; used only as part of the instrument's name."
```

- Leave the 20 facet results of Form Q out. The lens has no construct ids for them (§6), and an invented id would break the rule that constructs come from the lens.

**Known gap.** The checker reports AR-6 for this record at L1: it asks for the continuous scores and the scoring rule behind the type, which for this instrument are proprietary and must not be stored. Do not invent scores or a rule to silence it (§6).

**Who sees it:** the person. A grantee only when a Grant names the id, the lens or the category under explicit consent.

### Step 3b. Record the person's best fit

The toolkit item `jungian-type.best-fit` produces this record, and you may offer it. Offer short descriptions of each pole **in your own words** (never text from a report or a questionnaire), ask "Which description fits you best?" for each pair, and note where neither fits.

```json
{"id": "as-02", "lens": {"id": "urn:ohc:lens:jungian-type", "version": "0.2.0"},
 "mode": "self-identified", "assessedBy": "subject",
 "administeredAt": {"start": "2026-04-25", "precision": "day"},
 "results": [
   {"type": "type-assignment", "construct": "jungian-type/EI", "label": "Introversion", "method": "best-fit"},
   {"type": "type-assignment", "construct": "jungian-type/SN", "label": "Intuition", "method": "best-fit"},
   {"type": "type-assignment", "construct": "jungian-type/TF", "label": "Feeling", "method": "best-fit"},
   {"type": "type-assignment", "construct": "jungian-type/JP", "label": "Perceiving", "method": "best-fit"}],
 "validityFlags": ["self-identified-only"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-04-25T20:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- `mode: "self-identified"` with `origin: "declared"` (AR-1); `method: "best-fit"`; the flag `self-identified-only`.
- No `instrument`, no `trademarkNotice`, and never a mark in a `label`: this is not an MBTI® result.
- If neither pole fits on a pair, leave that pair out of `results`.
- **Known gap.** The checker also reports AR-6 here at L1, although a best-fit result has no scores at all (§6).

**Who sees it:** the person. A grantee only when a Grant names it.

### Step 3c. When the report and the best fit disagree

Disagreement between two results is data (M-8). Keep both and link them with a Tension that the person decides.

```json
{"id": "t-01", "between": ["as-01", "as-02"], "tensionKind": "source-divergence", "whoDecides": "subject",
 "text": "The report shows a slight preference for Extraversion; my best fit is Introversion.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-04-25T20:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

The person is the authority on best fit. Never argue for the reported pole.

**Who sees it:** the person. A Tension is served only when every record it joins is served.

### Step 4. Claims in the person's own words

The type is a starting point, not a verdict. Write a Claim only in the person's own wording, citing the result they accept.

```json
{"id": "c-01", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "In the four-letter vocabulary my best fit is INFP: I recharge alone, and I host people I know well.",
 "horizon": "foundation", "evidence": [{"ref": "as-02", "kind": "instrument"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-04-25T20:10:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- Facet `disposition`, predicate `self-described-tendency`, `origin: "declared"`; `evidence` names the result with kind `instrument`.
- The person did not accept the reported Extraversion, so no Claim cites `as-01`.
- Use the marks in a Claim only for a genuine result and only as adjectives ("my MBTI® Form M result was …").

**Who sees it:** special (it cites a result). Only a Grant that names its id or the category `mental-health` reaches it.

### Step 5. The person's own reading: when does the other pole show?

Ask the descriptor's question: "In which situations does the other pole show?" Write the episode and the person's reading. Only the person reads through this lens; you never do. `contexts` takes the codes listed in step 0.

```json
{"id": "ep-01", "title": "Hosting a birthday", "occurred": {"start": "2026-05-02", "precision": "day"},
 "accounts": [{"narrator": "subject", "narratedAt": "2026-05-02T23:30:00Z", "addedAt": "2026-05-02T23:30:00Z",
               "accountKind": "in-the-moment", "happened": "Hosted a birthday dinner for eight old friends and stayed up talking until late.",
               "understandingThen": "I like hosting when I know everyone."}],
 "contexts": ["friends"], "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-05-02T23:30:00Z", "synthetic": true}
```

```json
{"id": "in-01", "about": ["as-02", "ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:jungian-type", "version": "0.2.0"},
 "text": "The other pole shows when I host people I know well; with strangers it does not.",
 "facets": ["disposition"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-05-03T10:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

**Who sees them:** the episode is sensitive and reaches only Grants that name the kind or the id. The reading is special: a Grant must name it (or the lens) and allow interpretations (R-G8).

### Step 6. Practices

Both toolkit items (`jungian-type.best-fit` and `jungian-type.record-genuine-result`) produce AssessmentRecords (step 3), not Practices. This lens has no practices, and the example has none.

### Step 7. Who may see what

In the example the reflection companion may read only the best-fit result, the person's own words and their reading, by id. The genuine report, its result, the release and the adoption (which names the facilitator) stay with the person.

```json
{"id": "g-01", "recordedAt": "2026-05-10T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"ids": ["as-02", "c-01", "in-01"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2026-11-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-05-10T09:00:00Z", "channel": "holder-ui"},
 "note": "My best-fit type and my own words only; the genuine report stays with me."}
```

- A Grant reaching records of this lens uses `basis.legal: "explicit-consent"` and expires within 180 days (R-G10, GR-1).
- `actions` include no `infer` or `suggest`: the person wants no readings or estimates from an agent through this lens.
- Selecting by id keeps the reach exact. A `lenses` selector would also serve the genuine result, the LensAdoption with the facilitator's name, and every reading (§6).
- Never grant records of this lens to an employer, a team lead or anyone choosing people for roles, tasks or teams: those purposes are prohibited, and the descriptor warns that type labels are misused in hiring.
- `expressedBy` is how the person said yes; your statement that "the person agreed" is never consent.

### Step 8. Check

From the specification repository, run the checker on the folder of step 0, twice:

```sh
python3 -B tools/check.py <folder> --level L0 --json
python3 -B tools/check.py <folder> --level L1 --json
```

- **`--level L0` is the pass/fail gate.** It must give `"valid": true` with no errors.
- **`--level L1` must also be run, and read.** L0 does not run the L1 rules at all, so it hides real mistakes such as a missing practitioner release (LA-3). At L1 the only acceptable errors are AR-6, one for each record with `type-assignment` results (in the example exactly two: `as-01` and `as-02`). Fix every other error.
- The checker does not open vault files, so check `sha256` and `size` against the files yourself with the commands of step 2. It checks shape and rules, not truth or consent.

## 4. Never

- **Never for these purposes,** under any grant: personnel selection, task allocation, performance evaluation, promotion decisions, ranking against other people, persuasion targeting, and the other prohibited purposes (§8.10). A result grounds a choice you propose for the person only under the grant's `decisionUse: approval-required`, only when the person accepted it, naming what you weighed (R-G14).
- **Never** assign a type to the person, or derive a type from Big Five or any other scores (M-4). An agent's estimate exists only when the person asks for one under a Grant with `suggest` and `infer` for the lens, and it is a person-only proposal (AR-2), never a type.
- **Never** offer to record a genuine result (`agentMayOffer: false`); wait until the person brings one.
- **Never** use a type to suggest roles, tasks or teams, and never explain behaviour away by type.
- **Never** speak of fixed kinds of people. Speak of preferences, in the person's own type wording.
- **Never** use a Mapping to turn a type into Big Five scores. The mapping rows to Big Five are population statistics; each forbids that use.
- **Trademarks:** never call a quiz result, a best-fit result or any agent output an MBTI® type, and never put "MBTI", "Myers-Briggs", "Myers-Briggs Type Indicator" or "Step II" in a `label` or `text` that is not about a genuine result. Use the marks only as adjectives. Every genuine result carries the `trademarkNotice`; a Form Q result also carries the Step II notice.
- **Never** store MBTI® item text, item responses, scoring keys or report prose, and never administer the MBTI® instrument yourself.

## 5. Worked example

[examples/jungian-type/context.json](examples/jungian-type/context.json) is a single-document context for Ilari, a fictional person who received a genuine report from a workshop facilitator. Every record carries `"synthetic": true`. It contains exactly the records of §3: `la-01`, `src-02` and `src-01` (each with a synthetic vault file; the report stand-in holds no report prose), `as-01`, `as-02`, `t-01`, `c-01`, `ep-01`, `in-01` and `g-01`. The `agent-suggested` snippet of §2 (`rv-00`) and the Form Q fields of step 3a are alternatives, not part of the example; each was checked separately: L0 passes, and L1 shows only AR-6 errors on records with `type-assignment` results.

```sh
python3 -B tools/check.py docs/lenses/examples/jungian-type --level L0 --json
python3 -B tools/check.py docs/lenses/examples/jungian-type --level L1 --json
```

At `--level L0`: `"valid": true`, `"levelMet": "L0"`, no errors and no warnings; kept in [examples/jungian-type/expected-check.json](examples/jungian-type/expected-check.json). At `--level L1`: `"valid": false` with exactly the two AR-6 errors on `as-01` and `as-02` and nothing else; kept in [examples/jungian-type/expected-check-L1.json](examples/jungian-type/expected-check-L1.json). Without `practice.releaseRef` the L1 run would add LA-3, while L0 would still pass. **L1 is the level this context would reach once AR-6 is fixed.**

## 6. What does not fit yet

Each item is recorded for the next revision of the standard.

1. **A genuine MBTI® result cannot pass L1.** AR-6 requires the continuous scores and the scoring rule behind a type with `method: instrument`. For a proprietary instrument both are the publisher's and must not be stored (AR-3, `neverStore`). A context that records a genuine result therefore stays at L0.
2. **AR-6 is applied to best-fit results.** The checker treats `method: best-fit` like a type derived from scores, although a best-fit result has no scores. The person's own best fit cannot pass L1 either, unless it is recorded as `self-identified`, which loses the fact that it was confirmed by best fit.
3. **No construct for a pole or for the whole type.** Constructs are the four pairs; the pole lives only in `label`, so `type-assignment.alternatives` cannot name the other pole, and the four-letter type (INFP) exists only in a Claim's text.
4. **Clarity has no scale.** `clarity` is a free number or string; there is no vocabulary of clarity bands and no range per instrument.
5. **Trademark rules are not checked.** The checker does not require `trademarkNotice` on a genuine result, and it does not notice a mark used as a `label` on a self-identified result. AR-2 covers only agent estimates, and M-4 is not checked.
6. **`reviewAfter: on-change` cannot be stored.** The descriptor's default is `on-change`, but AssessmentRecord `reviewAfter` accepts only a duration.
7. **A facilitator's reading cannot be recorded.** *Resolved in 0.1.0-draft.2:* LA-7 is retired and I5 applies `agentInterpretation` to agent and software authors only; a facilitator's reading needs the facilitator in `interpretationAuthors` of the active adoption.
8. **The descriptor's use limits pull in two directions.** *Resolved in 0.1.0-draft.2:* `inferenceInput` is gone; only `crossLensMapping: population-level-only` remains, and the Mapping rows' `forbiddenUse` still stops a cross-lens estimate from a type.
9. **No rights marker on a Source.** Nothing says machine-readably that a stored report contains a publisher's protected text. The example relies on `no-quote` and `maxRelease: index`.
10. **Unclear mode for a best fit reached with a facilitator.** `practitioner-facilitated` has no expected origin in the assessment catalog, and a best fit can be expressed both as a mode (`self-identified`) and as a method (`best-fit`).
11. **A lens with a known checker gap loses every L1 protection.** One AR-6 drops `levelMet` to L0, and `--level L0` does not run L1 rules at all. A context that can only declare L0 is never gated on LA-3 or any other L1 rule; the recipe has to tell the writer to run L1 and read the output by hand.
12. **Marks in instrument entries are ignored.** The "Step II" mark and its notice exist only in the Form Q instrument entry. LENSES §5 and AR-2 read only the lens's `ip.marks`, so the Step II notice is not required on a Form Q result, and "Step II" in the `label` of a self-identified result is not caught.
13. **The 20 facets of Form Q have no construct ids.** A Form Q report's facet results cannot be recorded at all.
14. **No code for facilitation or teaching in custody.** `Source.custody.confidentiality` is `none`, `therapy`, `coaching`, `legal` or `medical`, although the lens lists `teacher` and `facilitator` as inheritance roles. A facilitator's notes must either borrow `coaching` or carry no custody ceiling.
15. **LA-3 asks for a release even for the person's own copy of a report.** Any stored Source authored by the practitioner triggers it, whether it is the practitioner's notes or a report the person owns outright.
16. **`uses` has no force.** No rule ties a record to an active adoption of its lens or to its `uses`; AssessmentRecords and readings by the person pass L1 with no LensAdoption at all.
17. **The person's request for a suggestion cannot be recorded.** `adoption.suggestionRequires` says when a suggestion usually makes sense (after the person asked for ways of describing preferences); LensAdoption has no field for that request, so it lives in `note`.
18. **`form` is not checked, and `instrument.version` has no defined meaning.** `form: "999"` passes (AR-8 checks only the instrument id); `version` could be the publisher's edition or the catalog entry's version, and instrument entries cannot be pinned by `sha256` the way lenses are.
19. **Vault files are never compared with their description.** The checker does not read vault files (`vaultContentRead: false`); SR-3 only checks that `sha256` matches the name in `vaultPath`. A wrong `size`, a wrong hash used the same way in `vaultPath`, or a missing file passes.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
