# Lens recipe: `cbt` (cognitive-behavioural lens, non-clinical use)

**Recipe · lens `urn:ohc:lens:cbt` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe shows, step by step, how a person's thought records and their use of the cognitive-behavioural lens enter an OHC context, which records they create, who sees them, and how an agent may offer a reading without labelling anyone's thoughts.

**The lens at a glance** (from [`spec/lenses/cbt.lens.json`](../../spec/lenses/cbt.lens.json); see also [LENSES.md §7.6](../../spec/LENSES.md#76-how-each-lens-works-with-a-person)):

| | |
|---|---|
| Kind and status | `practice-method`, descriptor `draft`, non-clinical use only |
| Constructs | `cbt/situation`, `cbt/automatic-thought`, `cbt/emotion`, `cbt/behavior`, `cbt/alternative-thought` |
| Instruments | none |
| Toolkit | `cbt.thought-record`: a worksheet the person fills in; an agent may offer it; produces an AssessmentRecord |
| Representation | `cbt.thought-record`: five columns in the person's words (result type `thought-record`) |
| Agent suggestion | by the person's Grant (`suggest` naming the lens); the descriptor's guidance: when the person asked for a way to look at a recurring reaction |
| Agent interpretation | by the person's Grant (`infer` naming the lens) and adoption (I5) |
| Cross-lens mapping | `not-allowed` |
| Defaults | tier `special`; category `mental-health`; `reviewAfter` `P3M` |
| Evidence | OHC makes no efficacy claim. The descriptor's one citation is graded **[verify]**: Hofmann et al. 2012, a review of meta-analyses on clinical efficacy, not reviewed for this use. |

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them.

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:cbt-basic`](../../spec/playbooks/cbt-basic.playbook.json) (Cognitive-behavioural lens: basic ways of working, by the OHC editors), for these situations: under strain: tired, pressed or overloaded; after a setback; preparing a hard conversation; choosing between options. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

## 1. What you may have

- **Self-description in conversation.** The person describes a situation, what went through their mind, what they felt and what they did.
- **A thought record the person wrote**: typed, in an app, or on paper and photographed.
- **Notes from therapy or coaching** where thought records were used, including worksheets filled in during a session.
- **An agent's reading.** Under the person's `infer` grant that names the lens and their adoption, and always as a proposal the person decides on.

Not for this lens: an instrument report. The lens has no instrument and no score.

## 2. Before you start

**Route of adoption.**

| Route | When | What it changes |
|---|---|---|
| `self-chosen` | The person picked the lens. | The person writes the adoption; it is active at once. |
| `agent-suggested` | The person asked for a way to look at a recurring reaction and you offered the thought record. | The adoption carries `suggestedBy` (your Party id) and stays `proposed` until the person admits it with a Review, even when the person writes it. The checker does not remind you of that Review (step 1). |
| `inherited-from-practice` | The person uses thought records with a therapist or coach. | Add a `practice` block. With a therapist, set `confidentiality: "therapy-confidential"`: the adoption and every record that cites it in `adoption` (here the agent's reading) become `person-only` (LA-4). AssessmentRecord and Practice cannot cite the adoption, so add `"handling": ["person-only"]` yourself to every thought record and practice of the lens (steps 4 and 7), and to Episodes from sessions. A thought record made in a session uses `mode: "practitioner-facilitated"`. If you store session material, `practice.releaseRef` must name the practitioner's release (LA-3). |
| `imported` | Not listed for this lens: there is no instrument to import from. | Routes describe usual practice and restrict nothing. |

**Consent.** The person adopts the lens; you do not. An adoption gives nobody access (LA-2). For you to read thought records or write a reading, the person must first give you a grant with `infer` and explicit consent. **Step 2 gives that grant; it must exist before any record you write or file** (rules INF-1 and PR-2 check that the grant was already given at the `recordedAt` of each of your records). Records the person dictates to you are written as theirs (`assertedBy: "subject"`), read back and confirmed ([CONTEXT-01](../agents/procedures/CONTEXT-01.md)). Leave `recordedBy` out: if you set it to your own Party id, rule INF-1 requires `underGrant` and `purpose` under a grant that includes `write`.

**Defaults for this lens.**

- `sensitivity: "special"` and `categories: ["mental-health"]` on every record of the lens: the adoption, thought records, lens readings, practices from the toolkit, and Sources holding thought records. Documentation calls this "treated as special category".
- A Claim that cites a thought record in `derivedFrom` inherits `special` and `mental-health` (C3; see step 5).
- `reviewAfter`: `P3M` on thought records.
- `agentInterpretation`: `off` by default. The person may set `ask-first` or `allowed`; with `off` on an active adoption, no agent reads through the lens (I5).

**Never stored.**

- Published worksheet text, instructions or examples from manuals or apps (descriptor restriction). Store the person's own entries only.
- Labels for thoughts ("distortion" names, "irrational", "catastrophising" and the like), diagnoses and clinical scores.
- An emotion, mood or stress value that you inferred, from behaviour or otherwise (R-X4). The emotion column is always the person's own word.
- A thought record filled in by an agent, or an alternative thought the person did not adopt as theirs.
- Any score treated as a judgement of the person.

## 3. Steps

Each step says what to do, which record it creates, the array of the context file it goes into, a minimal record that validates against the schema, and who sees it by default. The snippets are taken from the [worked example](#5-worked-example) or were checked against it; they carry `"synthetic": true` because the person is fictional, and you leave that field out for a real person. With no grant, nothing is disclosed to anyone but the person. Do the steps in order, and give each record a `recordedAt` later than the records it builds on: the checker rejects an agent record written before its grant, but it does not notice other records in the wrong order (§6, item 12).

### Step 0. Start the context file

Create a folder for the person's context and, in it, a file `context.json` (the single-document form, [§3.3](../../spec/SPECIFICATION.md#33-two-serializations-of-one-data-model); [schema](../../spec/schema/context.schema.json)). Start it with this envelope:

```json
{
  "format": "ohc.context",
  "specVersion": "0.1.0-draft",
  "id": "urn:ohc:example:jovana:context",
  "version": "2026-09-16.1",
  "subject": {"id": "urn:ohc:example:jovana", "displayName": "Jovana (fictional)"},
  "holder": "subject",
  "lang": "en",
  "created": "2026-09-03T19:00:00Z",
  "conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
  "parties": [],
  "policy": {"admission": "subject-only", "resolver": "returnDialog"},
  "lenses": [{"id": "urn:ohc:lens:cbt", "version": "0.2.0"}],
  "synthetic": true,
  "lensAdoptions": [], "grants": [], "sources": [], "episodes": [], "assessments": [], "claims": [],
  "interpretations": [], "proposals": [], "practices": [], "outcomes": [], "reviews": []
}
```

- **Modules.** Declare every module whose records you write, or the checker reports errors: `core` (Party, Source, Episode, Claim, Interpretation, Proposal, Review), `governance` (Grant), `lenses` (LensAdoption, AssessmentRecord), `practices` (Practice, Outcome).
- **Arrays.** Each record goes into the array of its kind: LensAdoption → `lensAdoptions`, Grant → `grants`, Source → `sources`, Episode → `episodes`, AssessmentRecord → `assessments`, Claim → `claims`, Interpretation → `interpretations`, Proposal → `proposals`, Practice → `practices`, Outcome → `outcomes`, Review → `reviews`, Party → `parties`. Each step below names its array again.
- **`synthetic`.** In an example, the context and every content record carry `"synthetic": true`; Parties, Grants, Proposals and Reviews never do (the schema rejects it there).
- **For a real person.** Use `urn:uuid:` ids for `id` and `subject.id`, for example from `python3 -c "import uuid; print('urn:uuid:' + str(uuid.uuid4()))"`; leave out `synthetic` everywhere; `displayName` is optional. Keep the folder out of any folder named `examples`. A context whose `id` starts with `urn:ohc:example:`, or that sits inside an `examples` folder, is checked as an example and then needs `"synthetic": true` on every content record (X-1, CX-8).
- **`version`** is yours to choose; change it with every set of changes.
- **The empty file does not pass yet.** A context needs at least one Claim, or one Episode with an account (LV-0); step 4 adds one. Check after step 4, and again at the end (step 8).

### Step 1. Record the adoption (Party → `parties`, LensAdoption → `lensAdoptions`, Review → `reviews`)

Ask how the person came to the lens and what it may be used for ([§10.5](../../spec/SPECIFICATION.md#105-lensadoption), [schema](../../spec/schema/lens-adoption.schema.json)).

- `uses`: `speak-in-lens`, `offer-practices` (you may offer the thought record), `store-results` (the person keeps thought records), `interpret` (readings through the lens).
- `interpretationAuthors`: `["subject"]`, plus any person (a therapist, say) whose readings the person wants kept. Listing your Party id, as the example does, is harmless; your own readings follow your Grant instead (I5). `agentInterpretation: "ask-first"` means you ask before each reading.

In the example you offered the thought record in a conversation and the person took it. First put yourself in `parties`; the id prefix `a-` is required for an agent (`p-` person, `s-` software, `o-` organization):

```json
{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}
```

Then the person writes the adoption and admits it:

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:cbt", "version": "0.2.0"}, "route": "agent-suggested",
 "suggestedBy": "a-01", "confidentiality": "none",
 "uses": ["speak-in-lens", "offer-practices", "store-results", "interpret"],
 "interpretationAuthors": ["subject", "a-01"], "agentInterpretation": "ask-first",
 "representationPreference": "cbt.thought-record",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-03T19:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "rv-01", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-09-03T19:01:00Z"}
```

Without the admit Review the adoption stays `proposed`, and a proposed adoption neither allows nor stops anything: your reading in step 6 would pass I5 on your grant alone, without the person's `ask-first` choice taking effect. The person's own thought records and practices of the lens are still served. Write the admit Review before any other record of the lens.

For `route: "self-chosen"`, leave out `suggestedBy` and the Review. For `route: "inherited-from-practice"`, see §2.

**Variant: you write the adoption yourself**, outside a conversation in which the person confirms it. Then it is your proposal: an agent cannot write it as `declared` (ENV-2), so it is `inferred`, cites where the person asked, and needs the grant of step 2 with `suggest` and `infer`. Do it in this order:

1. Write the Grant of step 2 first, with `recordedAt` and `expressedBy.at` earlier than everything below (for example `2026-09-03T18:40:00Z`).
2. Write the Episode (or Source) in which the person asked, with `recordedAt` earlier than the adoption:

   ```json
   {"id": "ep-00", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-03T18:50:00Z",
    "title": "Asked for a way to look at it", "occurred": {"start": "2026-09-03", "precision": "day"},
    "accounts": [{"narrator": "subject", "narratedAt": "2026-09-03T18:45:00Z", "addedAt": "2026-09-03T18:50:00Z",
      "accountKind": "in-the-moment",
      "happened": "I asked the companion for a way to look at why I keep holding drafts back."}],
    "selection": {"selectedBy": "subject", "reason": "subject-chose"}, "contexts": ["work"], "synthetic": true}
   ```

3. Change these fields of the adoption:

   ```json
   {"assertedBy": "a-01", "origin": "inferred", "underGrant": "g-01", "purpose": "self-reflection",
    "derivedFrom": ["ep-00"]}
   ```

4. File it in `proposals`. `expiresAt` is optional; without it the proposal expires 30 days after `recordedAt`:

   ```json
   {"id": "prop-00", "proposer": "a-01", "recordedAt": "2026-09-03T19:00:00Z", "underGrant": "g-01",
    "purpose": "self-reflection", "items": ["la-01"],
    "rationale": "The thought record is one way to look at holding drafts back. Take it only if it suits you.",
    "expiresAt": "2026-10-03T19:00:00Z", "presentation": {"channel": "agent-dialog", "askedAt": "2026-09-03T18:59:00Z"}}
   ```

5. Wait for the person's admit Review (`rv-01` above). Until then the adoption is `proposed`.

The checker does not check that `ep-00` is older than the adoption (§6, item 12): keep that order yourself. This variant was checked and passes at L1; it is not in the example file.

**Who sees it:** the person; and, under the grant of step 2, you.

### Step 2. Who may see what, before any reading (Grant → `grants`)

By default nobody sees anything. For a reflection companion that may read thought records and propose readings, the person gives this grant now ([§12.1](../../spec/SPECIFICATION.md#121-grant), [schema](../../spec/schema/grant.schema.json)). Its `recordedAt` and `expressedBy.at` must be earlier than every record you write or file under it (steps 6 and 7); otherwise the check fails with INF-1 and PR-2.

- `actions: ["read", "suggest", "infer"]`: `infer` is never implied by anything else (R-G11).
- A selector that names the lens, `basis.legal: "explicit-consent"`, and an expiry of at most 180 days (R-G3, R-G10).
- Episodes are `sensitive`: name them by kind, here limited to work.
- `maxSourceTier: "none"`: no access to the originals.

```json
{"id": "g-01", "recordedAt": "2026-09-03T19:05:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:cbt"]}, {"kinds": ["Episode"], "contexts": ["work"]}]},
 "actions": ["read", "suggest", "infer"], "mode": "full", "interpretations": "all", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-01T19:05:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "reviewCadence": "P7D", "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-03T19:05:00Z", "channel": "holder-ui"},
 "note": "Thought records and readings of work situations only. No labels for my thoughts."}
```

A work assistant never gets this lens: thought records are never a work input (prohibited purposes in §4). What the companion finally receives is shown at the end of step 7.

### Step 3. Keep the original in the vault (Source → `sources`)

If the person wrote the thought record somewhere, keep the original as a Source ([§10.1](../../spec/SPECIFICATION.md#101-source), [schema](../../spec/schema/source.schema.json)): `sourceKind: "note"` for typed text, `"image"` for a photo of a paper sheet, `"document"` for a PDF export. The record holds only metadata; the bytes go into the vault:

1. Compute the hash: `shasum -a 256 <file>` (or `sha256sum <file>`). The 64 hexadecimal characters are `sha256`.
2. Compute the size in bytes: `wc -c < <file>`. That number is `size`.
3. Copy the file to `vault/<first two characters of the hash>/<hash>.<extension>`. `vaultPath` is relative to the folder that holds `context.json`.
4. The L1 checker does not open the vault (its report says `"vaultContentRead": false`): it does not notice a missing file, a wrong hash or a wrong size. Run the two commands again on the stored file and compare.

Set `maxRelease: "index"`.

```json
{"id": "src-01", "sourceKind": "note", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-08T21:00:00Z",
 "content": {"locator": {"vaultPath": "vault/60/60c2313c1c1e4bd527ea894721a14ac04415d67f038538164558f77466802cef.md"},
             "sha256": "60c2313c1c1e4bd527ea894721a14ac04415d67f038538164558f77466802cef",
             "mediaType": "text/markdown", "size": 324},
 "capturedAt": "2026-09-08T20:40:00Z", "authorship": {"author": "subject"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index",
 "summary": {"text": "My thought record for Tuesday.", "authoredBy": "subject",
             "recordedAt": "2026-09-08T21:00:00Z", "method": "subject-written"},
 "retention": {"eraseOnRequest": true}, "sensitivity": "special", "categories": ["mental-health"],
 "contexts": ["work"], "synthetic": true}
```

The worked example ships these bytes: [examples/cbt/vault/60/…](examples/cbt/vault/60/60c2313c1c1e4bd527ea894721a14ac04415d67f038538164558f77466802cef.md).

A photo is a behavioural source kind (R-X4). A thought record that names it as `source` stays valid only as the person's own entries (`origin: "declared"`); a version transcribed by software (`origin: "derived"`) fails the checker (AR-1), and nothing about feelings may be derived from the photo.

**Who sees it:** the person has every tier. A grantee gets at most `index`, and only under a grant that names the Source.

### Step 4. The situation and the thought record (Episode → `episodes`, AssessmentRecord → `assessments`)

**4a. The situation.** Write what happened as an Episode in the person's own account ([§10.2](../../spec/SPECIFICATION.md#102-episode), [schema](../../spec/schema/episode.schema.json)).

```json
{"id": "ep-01", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-08T20:30:00Z",
 "title": "Floor-plan draft kept back", "occurred": {"start": "2026-09-08", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-08T20:30:00Z", "addedAt": "2026-09-08T20:30:00Z",
    "accountKind": "in-the-moment",
    "happened": "The floor-plan draft was due to my team lead on Tuesday. I kept it for a third day.",
    "experienced": "A knot in my stomach every time I opened the send window.",
    "didOrTried": "Changed the stair detail again. Did not send.",
    "understandingThen": "The draft was not ready."}],
 "selection": {"selectedBy": "subject", "reason": "subject-chose"}, "contexts": ["work"], "synthetic": true}
```

**4b. The thought record.** One AssessmentRecord per filled-in record ([§10.6](../../spec/SPECIFICATION.md#106-assessmentrecord), [schema](../../spec/schema/assessment-record.schema.json)), with one result of type `thought-record`.

- The five columns are the person's own words. You may ask the questions ("What went through your mind just before?", "What else could be true?"); you never fill a column.
- `mode: "self-identified"` with `origin: "declared"` and the flag `self-identified-only`: the closest fit in 0.1 for entries the person made (§6, item 1). With a practitioner in session, use `practitioner-facilitated`.
- `instrument` is left out: the lens has none.
- `derivedFrom: ["ep-01"]` links the record to its situation (§6, item 2). `source` names the original.
- Ratings, if the person gives any, stay inside the text of the column (§6, item 3).
- With a therapist (`therapy-confidential`), add `"handling": ["person-only"]` to the record: LA-4 does not reach it (§6, item 11).

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:cbt", "version": "0.2.0"}, "mode": "self-identified",
 "assessedBy": "subject", "administeredAt": {"start": "2026-09-08", "precision": "day"},
 "results": [
   {"type": "thought-record",
    "situation": "Draft ready to send to my team lead on Tuesday afternoon.",
    "thought": "If she sees the stair detail she will think I cannot do this job.",
    "emotion": "Dread, about 70 out of 100.",
    "behavior": "Kept the draft and reworked the stair detail.",
    "alternative": "She asked for a draft, not a finished plan. Early comments are cheaper for both of us."}],
 "validityFlags": ["self-identified-only"], "source": "src-01", "derivedFrom": ["ep-01"],
 "reviewAfter": "P3M", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-08T21:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "contexts": ["work"], "synthetic": true}
```

**Who sees it:** the person; under a grant that names the lens, the whole record, including the emotion column (§6, item 4). The Episode is served under the grant's Episode selector.

### Step 5. Statements the person accepts (Claim → `claims`)

If the thought record shows the person something they want to state about themselves, write it as a Claim in their words, only after they say it ([§9.4](../../spec/SPECIFICATION.md#94-claim)). A tendency the person recognises is facet `disposition` with predicate `self-described-tendency` (CL-3 allows `declared` by the person). `derivedFrom` names the thought record.

```json
{"id": "c-01", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "When I expect a draft to be criticised, I hold it back and keep reworking details.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-08T21:10:00Z", "horizon": "focus",
 "derivedFrom": ["as-01"], "contexts": ["work"], "synthetic": true}
```

**Who sees it:** through `derivedFrom` the Claim becomes `special` with `mental-health` (C3), so only a grant that names it by id or category reaches it; the grant of step 2 does not. If the person wants to share a plain statement more widely, for example a goal "Send a first draft by Wednesday noon" with a work assistant, write that Claim without `derivedFrom`: with it, the work assistant never receives it (checked; §6, item 6).

### Step 6. An agent's reading of the episode, with alternatives (Interpretation → `interpretations`, Proposal → `proposals`, Review → `reviews`)

Only under the grant of step 2 (`infer`, naming the lens), given before this record, and while the person's adoption does not say `off` (I5). With `ask-first`, ask the person before each reading ("May I offer one way of looking at Tuesday?"); at level L2 that question is logged as an Event `ask-first`.

Write the reading as your proposal ([§10.3](../../spec/SPECIFICATION.md#103-interpretation), [schema](../../spec/schema/interpretation.schema.json)):

- `origin: "inferred"`, `epistemic: "hypothesis"`, `causal` at most `hypothesized`, and `underGrant` with `purpose`.
- At least one ground, at least two alternatives with at least one that is not psychological, and `limits` (I4).
- A question or a "may have", never a correction. No labels for thoughts (I3). No feeling words of your own: the person's feelings stay in their thought record.

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading", "lens": {"id": "urn:ohc:lens:cbt", "version": "0.2.0"},
 "adoption": "la-01",
 "text": "An expectation that the team lead would judge her ability by one detail may have come before the draft was held back.",
 "causal": "hypothesized", "origin": "inferred", "assertedBy": "a-01", "recordedAt": "2026-09-09T08:00:00Z",
 "underGrant": "g-01", "purpose": "self-reflection", "epistemic": "hypothesis",
 "grounds": [{"ref": "as-01", "kind": "instrument"}, {"ref": "ep-01", "kind": "evidence"}],
 "alternatives": [
   {"text": "The stair detail really was open: the structural figures arrived late.", "kind": "informational"},
   {"text": "It was the third late evening that week.", "kind": "physiological"}],
 "limits": "One episode, one lens and one thought record; a self-reflection aid, not a clinical reading.",
 "sensitivity": "special", "categories": ["mental-health"], "contexts": ["work"], "synthetic": true}
```

File it with a Proposal ([§11.2](../../spec/SPECIFICATION.md#112-proposal)); `expiresAt` is optional and defaults to 30 days after `recordedAt`. The rationale is written for the person and quotes no record.

```json
{"id": "prop-01", "proposer": "a-01", "recordedAt": "2026-09-09T08:00:00Z", "underGrant": "g-01",
 "purpose": "self-reflection", "items": ["in-01"],
 "rationale": "One reading of Tuesday's draft, with two other explanations to weigh.",
 "expiresAt": "2026-10-09T08:00:00Z", "presentation": {"channel": "agent-dialog", "askedAt": "2026-09-09T07:58:00Z"}}
```

The person decides with a Review: `endorse`, `partially-endorse` (in their own words), `reject` or `contest`. Silence is not acceptance; an unanswered proposal expires as declined.

```json
{"id": "rv-02", "target": "in-01", "action": "partially-endorse", "by": "subject",
 "recordedAt": "2026-09-16T19:00:00Z",
 "endorsedPart": "I expected her to judge me by the stair detail."}
```

**Who sees it:** while the proposal is open, the person and you (in your proposer view, [§12.5](../../spec/SPECIFICATION.md#125-proposer-view)). After the person's Review, it is served under the grant with its label, here `partly-confirmed`. With a therapist, the reading cites the adoption and is `person-only` (LA-4).

### Step 7. A practice from the toolkit and how it went (Practice → `practices`, Episode → `episodes`, Outcome → `outcomes`)

You may offer the thought record as a practice (`agentMayOffer: true`). If the person keeps it, they write it in their own words as a Practice ([§17.1](../../spec/SPECIFICATION.md#171-practice), [schema](../../spec/schema/practice.schema.json)): `source.route: "from-lens"`, `templateId: "cbt.thought-record"`, and `source.by` set to you when you offered it. If you write the Practice yourself, it has `route: "from-agent"`, stays proposed until the person admits it (PC-1) and needs your grant (INF-1). With a therapist, add `"handling": ["person-only"]` (§6, item 11).

```json
{"id": "pr-01", "name": "Thought record before I hold a draft back",
 "description": "Ten minutes of writing before I decide to keep a draft another day.",
 "practiceKind": "writing",
 "source": {"route": "from-lens", "lens": "urn:ohc:lens:cbt", "templateId": "cbt.thought-record", "by": "a-01"},
 "steps": ["One line: the situation", "What went through my mind", "The feeling and how strong, 0 to 100", "What I did", "What else could be true"],
 "duration": "PT10M", "limits": "Not to talk myself out of a real problem in the drawing.",
 "initialStatus": "in-use", "nonClinical": true, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-10T19:00:00Z", "sensitivity": "special", "categories": ["mental-health"],
 "contexts": ["work"], "synthetic": true}
```

The person says how it went as an Outcome, pointing at the Episode where they used it ([§17.2](../../spec/SPECIFICATION.md#172-outcome)). In the example that Episode is `ep-02`, "Section draft sent", written like step 4a.

```json
{"id": "oc-01", "about": {"practice": "pr-01"}, "episode": "ep-02", "result": "helped", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-09-12T13:05:00Z", "contexts": ["work"], "synthetic": true}
```

**Who sees it:** the person; under the grant of step 2, you receive the Practice (it carries the lens in `source.lens`) and `ep-02` (through the Episode selector), but not the Outcome, because it carries no lens.

**What the companion receives in the end.** From the repository root, run:

```sh
python3 -B tools/ohc_query.py <your context folder> project --grant g-01 --purpose self-reflection --now latest
```

For the worked example the folder is `docs/lenses/examples/cbt`. `--purpose` is required and must be one of the grant's purposes. `--now latest` evaluates the grant at the time of the newest record in the file, so the result does not depend on today's date. The tool prints two lines (the time it used, the key) and then the projection as JSON. Served records are listed under `statements` (`lensAdoptions`: `la-01`; `assessments`: `as-01`; `practices`: `pr-01`), `experience` (`episodes`: `ep-01`, `ep-02`) and `interpretations` (`interpretations`: `in-01`). `derived` holds the computed labels; for `in-01` it is `"label": "partly-confirmed"`. The companion does not receive the Source `src-01`, the Claim `c-01` or the Outcome `oc-01`.

### Step 8. Check

From the repository root:

```sh
python3 -B tools/check.py <your context folder> --level L1 --json
```

Fix every error until it reports `"valid": true` and `"levelMet": "L1"`. If you see INF-1 on your reading or PR-2 on your Proposal although both carry `underGrant` and `purpose`, the grant was given after them: move the grant's `recordedAt` and `expressedBy.at` earlier (§6, item 13). The checker also compares its output with an `expected-check.json` next to the file (rule X-3), but only when the folder sits inside a folder named `examples`; your own context folder does not need one. The checker does not read the vault (step 3): check it yourself.

## 4. Never

- **Prohibited purposes.** Never use any record of this lens for `personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting` or any other purpose of [§8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed), under any grant; thought records are often about work, so keep that in mind. A result grounds a choice you propose for the person only under `decisionUse: approval-required`, only when the person accepted it, naming what you weighed (R-G14).
- **Agent inference only as proposals.** Write readings only with an `infer` grant, as `inferred` hypotheses with grounds, alternatives and limits. Never write a thought record for the person (`mode: "agent-inference"` is not for this lens, even where the checker lets it pass; §6, item 5). Never map results to another lens (`crossLensMapping: not-allowed`).
- **No labels.** Never apply a distortion, diagnosis or clinical label (I3). Never call a thought irrational or wrong, and never argue the person out of a view.
- **No therapy.** Never present yourself as CBT therapy. Clinical use belongs with clinicians; health records are pointers only (HealthRef).
- **No inferred feelings.** Never derive an emotion, mood or stress value from behaviour, voice, face or typing (R-X4), and never put one in your own readings.
- **No quoting back or leverage.** Never use a thought record or an endorsed reading to press the person ("you said yourself that…"); respect `no-quote-back` and `no-leverage` where the person sets them.
- **Trademark.** The descriptor lists no marks. Do not name a commercial programme or app as if OHC delivered it.

## 5. Worked example

[examples/cbt/context.json](examples/cbt/context.json) is one file at level L1 about Jovana, who is fictional. The context and every content record carry `"synthetic": true`. It holds exactly the records of section 3, and its times follow the order of the steps:

| Step | Records |
|---|---|
| 0 | the envelope, with modules `core`, `governance`, `lenses`, `practices` |
| 1 | the Party `a-01`, `la-01`, `rv-01` |
| 2 | `g-01` |
| 3 | `src-01`, with its bytes in [vault/60/](examples/cbt/vault/60/60c2313c1c1e4bd527ea894721a14ac04415d67f038538164558f77466802cef.md) |
| 4 | `ep-01`, `as-01` |
| 5 | `c-01` |
| 6 | `in-01`, `prop-01`, `rv-02` |
| 7 | `pr-01`, `ep-02`, `oc-01` |

The variants (an adoption written by the agent, a therapist) are not in the file.

```sh
python3 -B tools/check.py docs/lenses/examples/cbt --level L1 --json
```

It reports `"valid": true` and `"levelMet": "L1"`, with no errors and no warnings. [expected-check.json](examples/cbt/expected-check.json) is the exact output. The projection of step 7:

```sh
python3 -B tools/ohc_query.py docs/lenses/examples/cbt project --grant g-01 --purpose self-reflection --now latest
```

## 6. What does not fit yet

These are gaps in OHC 0.1 for this lens, found while writing this recipe and while a newcomer followed it. Each has a proposal for the next pass.

1. **No mode for the person's own worksheet.** The closed list of assessment modes has none for entries a person makes in a worksheet; `self-identified` ("the person chose the type or result") with the flag `self-identified-only` is the nearest. *Proposal:* add mode `self-recorded` (origin `declared`) for worksheets, logs and diaries within a lens.
2. **A thought record cannot say which situation it is about.** AssessmentRecord has no `about`; `derivedFrom: [Episode]` on a declared record is a stretch, and the `situation` column repeats the Episode. *Proposal:* an optional `about: [Episode]` on AssessmentRecord (or a `situationRef` in the result), with `situation` optional when it is present.
3. **Five strings only.** The result has no place for the intensity of a feeling, how strongly a thought is believed before and after, or several thoughts and feelings in one record, so the person's own numbers end up inside text. *Proposal:* optional numeric fields (`emotionIntensity`, `beliefBefore`, `beliefAfter`, 0 to 100) and arrays for several thoughts and feelings, all the person's own.
4. **No column-level sharing or authorship.** Under a lens grant the emotion column is served with the rest; the person cannot share the situation and the alternative while keeping the feeling to themselves. Nor can the record show that an alternative was first offered by an agent and then adopted by the person. *Proposal:* per-column handling (or a reference to a quarantined `state`/`emotion` Claim instead of inline text) and an optional `suggestedBy` per column.
5. **An agent-written thought record passes the checker.** `mode: "agent-inference"` with the AR-2 marks is accepted for result type `thought-record`, although the descriptor says the record holds the person's own entries only. *Proposal:* a rule that a `thought-record` result requires mode `self-identified` (or the proposed `self-recorded`) or `practitioner-facilitated`, written by the subject.
6. **Provenance makes a statement unshareable.** A Claim with `derivedFrom` a thought record inherits `special` and `mental-health`; a plain goal written that way never reaches a work assistant, while the same goal without `derivedFrom` does (checked). The person must choose between provenance and sharing. *Proposal:* a provenance link that does not carry the tier when the person writes the Claim themselves (for example `inspiredBy`), or a `relax` that may explicitly drop inherited categories.
7. **Record limits are not checked against the lens, and this lens's limits are narrow.** *Resolved in 0.1.0-draft.2:* records and lenses carry no prohibited purposes; all thirteen of §8.10 bind every grantee, whatever the lens.
8. **An agent's suggestion of a lens has no honest origin.** Written by the agent, an adoption cannot be `declared` (ENV-2 requires `text`, which LensAdoption lacks), so it must be `inferred` with grounds and an `infer` grant, although proposing a lens is not an inference about the person. Separately, an `agent-suggested` adoption stays proposed until admitted even when the person writes it, which §10.5's table does not say. *Proposal:* allow `declared` with a short `rationale` for an agent's lens suggestion, and state the admission rule in §10.5.
9. **The scribe needs a grant.** §15.9 lets an agent write what the person dictates as the subject, with `recordedBy` set to the agent, but INF-1 then requires a grant with `write`. *Proposal:* exempt `declared` records with `assertedBy: "subject"` and an agent `recordedBy` from INF-1 when the person confirms them, or define a scribe scope.
10. **The small test of an expectation has no template.** The descriptor says change happens by "trying small different actions", but the toolkit has only the thought record, and an Outcome has no place for what was expected and what happened. *Proposal:* a toolkit item `cbt.small-test` (exercise, self, agent may offer) and optional `expected`/`observed` texts on Outcome, written by the person.
11. **Therapy confidentiality does not reach thought records and practices.** LA-4 (`therapy-confidential` means `person-only`) travels only through an `adoption` field. AssessmentRecord and Practice have none, so lens results from therapy are served under a lens grant (checked with a therapist adoption: `as-01`, `pr-01` and both Episodes are served; only the adoption and the agent's reading are withheld). The confidentiality that the `inherited-from-practice` route promises does not reach the records that matter most. *Proposal:* an optional `adoption` on AssessmentRecord and on Practice (route `from-lens`), with LA-4 applied to them; or apply LA-4 to every record tagged with a lens (`lens` or `source.lens`) while the person's active adoption of that lens is `therapy-confidential`, and warn when such a record is not `person-only`.
12. **Provenance may point into the future.** A record may cite in `derivedFrom`, `grounds` or `evidence` a record whose `recordedAt` is later (checked: an agent-written adoption recorded on 2026-10-01 with `derivedFrom` an Episode recorded on 2026-10-04 passes). The `agent-suggested` audit trail relies on citing where the person asked, and a citation into the future makes that trail meaningless. *Proposal:* a rule (warning at L1, error at L2): every `derivedFrom`, `grounds.ref` and `evidence.source` target has `recordedAt` no later than the citing record's, unless the citing record supersedes a version.
13. **INF-1 does not say when the cause is timing.** When the grant exists but was given after the record, INF-1 still says the record "MUST carry `underGrant` … and `purpose`", although it carries both (checked). A writer cannot tell from the message that the order is wrong. *Proposal:* split INF-1 into "missing `underGrant`/`purpose`" and "grant not in force at `recordedAt` (given later, expired or revoked)", with the grant's given time in the message, as PR-2 already does.
14. **The vault is never verified.** The L1 checker does not open the vault: a Source whose file is missing, or whose `size` or `sha256` is wrong, passes. *Proposal:* a check option (for example `--vault`) that resolves `vaultPath` relative to the context folder and verifies existence, size and hash, reporting a missing file as a warning; and run it over the published examples, which now ship their bytes.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
