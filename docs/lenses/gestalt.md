# Lens recipe: `gestalt` (gestalt perspective, stub)

**Recipe · lens `urn:ohc:lens:gestalt` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe shows how a person who uses the gestalt perspective can name it and keep their own words in an OHC context, while the lens is still a stub: an agent reads through it only under the person's Grant (`infer` naming the lens) and adoption (I5), and its readings stay `frame-relative`.

> **This lens is a stub.** OHC lists the gestalt perspective so that a person can name it; the descriptor does not yet describe it. It has no constructs, no toolkit, no representations and no instruments, and its evidence is not assessed. This recipe therefore keeps only the safe steps: the adoption, the person's self-description in their own words, and the sources. There are **no assessment records, no agent readings, no model views, no parts and no practices from the lens**.

**The lens at a glance** (from [`spec/lenses/gestalt.lens.json`](../../spec/lenses/gestalt.lens.json); see also [LENSES.md §7.6](../../spec/LENSES.md#76-how-each-lens-works-with-a-person)):

| | |
|---|---|
| Kind and status | `process-experiential`, descriptor `stub` |
| What it attends to | what remains unfinished; what is happening now |
| Constructs, toolkit, representations, instruments | none yet |
| Agent suggestion | by the person's Grant (`suggest` naming the lens); the descriptor's guidance: only when the person asked for ways of looking at their experience |
| Agent interpretation | by the person's Grant and adoption (I5); `off` in the example, the default |
| Results | `frame-relative` (a stub, LA-6); cross-lens mapping `not-allowed` |
| Defaults | tier `special`; category `mental-health`; `reviewAfter` `on-change` |

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them.

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:gestalt-basic`](../../spec/playbooks/gestalt-basic.playbook.json) (Gestalt perspective: basic ways of working, by the OHC editors), for these situations: preparing a hard conversation; after a setback; looking back at something that happened. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

## 1. What you may have

- **Self-description in conversation.** The person uses the perspective's words for their own experience, for example "unfinished", and says what is happening for them now.
- **The person's own notes**, for example after a therapy session or a group evening.
- **Notes from gestalt therapy or a gestalt group**, written by the practitioner. This is practitioner material and has a custodian.

Not for this lens: an instrument report (there is none). An agent's reading comes only under the person's Grant and adoption (I5), and stays `frame-relative` (a stub, LA-6).

## 2. Before you start

**Route of adoption.**

| Route | When | What it changes |
|---|---|---|
| `self-chosen` | The person picked the perspective. | The person writes the adoption; it is active at once. No `practice`, no `onEnd`, `confidentiality: "none"`. |
| `agent-suggested` | The person asked you for ways of looking at their experience, you mentioned this perspective as one option among others, and the person took it. | Only under a Grant with `suggest` naming the lens; mention it only after such a request (`suggestionRequires`), then say nothing more in its terms until it is adopted. The adoption carries `suggestedBy` (your Party id) and stays `proposed` until the person admits it with a Review. The checker does not remind you of that Review (step 1). |
| `inherited-from-practice` | The person works in this perspective with a therapist or a group. | Add a `practice` block (role `therapist` or `facilitator`, practitioner Party, relationship). With a therapist, set `confidentiality: "therapy-confidential"`: the adoption and every record that cites it in `adoption` (here the person's question of step 3c) become `person-only` (LA-4); nothing else in this recipe carries the lens, so nothing else needs marking. With a group facilitator, `practitioner-scope`. If you store session material, `practice.releaseRef` must name the practitioner's release (LA-3). |
| `imported` | Not listed for this lens: there is no instrument to import from. | Routes describe usual practice and restrict nothing. |

**Consent.** The person adopts the perspective; you do not. An adoption gives nobody access, not even the practitioner (LA-2). Everything below is written by the person (`assertedBy: "subject"`); you may type what they dictate and read it back ([CONTEXT-01](../agents/procedures/CONTEXT-01.md)). Leave `recordedBy` out: if you set it to your own Party id, rule INF-1 requires a grant with `write`.

**Defaults for this lens.**

- `sensitivity: "special"` and `categories: ["mental-health"]` on the adoption, on any reading tagged with the lens, and on Sources from sessions.
- `agentInterpretation: "off"`: the default, which the person keeps here (I5).
- `uses: ["speak-in-lens"]` only: the person may use the perspective's words with you, and you may use the person's own words back. The other uses need a toolkit, representations or agent readings that a stub does not have.
- **Set `epistemic: "frame-relative"` yourself on every reading the person tags with the lens.** Nothing adds it for you (§6, item 4): without it, the reading is labelled `stated` instead of `frame` and can be taken for a fact. With it, the reading is meaningful inside the person's frame and never presented as an empirical fact (C-7).
- `reviewAfter`: `on-change`.

**Never stored.**

- Exercise scripts or instructions of the approach.
- Technical terms of the approach applied to the person by anyone but the person, for example names for ways of avoiding contact. If the person uses such a word about themselves, it stays inside their own text.
- An agent's reading, summary or "what this means" in the perspective's terms.
- Any AssessmentRecord, score, type or stage.
- The text of practitioner notes inside any record. Only the Source metadata is a record; the bytes stay in the vault.

## 3. Steps

Each step says what to do, which record it creates, the array of the context file it goes into, a minimal record that validates against the schema, and who sees it by default. The snippets are taken from the [worked example](#5-worked-example) or were checked against it; they carry `"synthetic": true` because the person is fictional, and you leave that field out for a real person. With no grant, nothing is disclosed to anyone but the person. Do the steps in order, and give each record a `recordedAt` later than the records it builds on.

### Step 0. Start the context file

Create a folder for the person's context and, in it, a file `context.json` (the single-document form, [§3.3](../../spec/SPECIFICATION.md#33-two-serializations-of-one-data-model); [schema](../../spec/schema/context.schema.json)). Start it with this envelope:

```json
{
  "format": "ohc.context",
  "specVersion": "0.1.0-draft",
  "id": "urn:ohc:example:edda:context",
  "version": "2026-10-02.1",
  "subject": {"id": "urn:ohc:example:edda", "displayName": "Edda (fictional)"},
  "holder": "subject",
  "lang": "en",
  "created": "2026-09-15T18:00:00Z",
  "conformance": {"level": "L1", "modules": ["core", "governance", "lenses"], "subjectIsAdult": true},
  "parties": [],
  "policy": {"admission": "subject-only", "resolver": "returnDialog"},
  "lenses": [{"id": "urn:ohc:lens:gestalt", "version": "0.2.0"}],
  "synthetic": true,
  "lensAdoptions": [], "sources": [], "episodes": [], "claims": [], "interpretations": [],
  "grants": [], "reviews": []
}
```

- **Modules.** Declare every module whose records you write, or the checker reports errors: `core` (Party, Source, Episode, Claim, Interpretation, Review), `governance` (Grant), `lenses` (LensAdoption).
- **Arrays.** Each record goes into the array of its kind: LensAdoption → `lensAdoptions`, Source → `sources`, Episode → `episodes`, Claim → `claims`, Interpretation → `interpretations`, Grant → `grants`, Review → `reviews`, Party → `parties`. Each step below names its array again.
- **`synthetic`.** In an example, the context and every content record carry `"synthetic": true`; Parties, Grants and Reviews never do (the schema rejects it there).
- **For a real person.** Use `urn:uuid:` ids for `id` and `subject.id`, for example from `python3 -c "import uuid; print('urn:uuid:' + str(uuid.uuid4()))"`; leave out `synthetic` everywhere; `displayName` is optional. Keep the folder out of any folder named `examples`. A context whose `id` starts with `urn:ohc:example:`, or that sits inside an `examples` folder, is checked as an example and then needs `"synthetic": true` on every content record (X-1, CX-8).
- **`version`** is yours to choose; change it with every set of changes.
- **The empty file does not pass yet.** A context needs at least one Claim, or one Episode with an account (LV-0); step 3 adds one. Check after step 3, and again at the end (step 5).

### Step 1. Record the adoption (Party → `parties`, LensAdoption → `lensAdoptions`)

Ask how the person came to the perspective ([§10.5](../../spec/SPECIFICATION.md#105-lensadoption), [schema](../../spec/schema/lens-adoption.schema.json)). In the example the person attends a gestalt group, so the route is `inherited-from-practice`. Put the facilitator in `parties` (the id prefix `p-` is required for a person):

```json
{"id": "p-01", "partyKind": "person", "label": "Group facilitator", "role": "practitioner"}
```

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:gestalt", "version": "0.2.0"}, "route": "inherited-from-practice",
 "practice": {"role": "facilitator", "practitioner": "p-01", "relationship": "active", "since": "2026-03-01"},
 "confidentiality": "practitioner-scope", "uses": ["speak-in-lens"], "interpretationAuthors": ["subject"],
 "agentInterpretation": "off", "onEnd": "ask",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-15T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

**Variant: with a therapist** whose notes the person keeps (see step 2). Give the Party the label `"Therapist"` and change the adoption to:

```json
{"practice": {"role": "therapist", "practitioner": "p-01", "relationship": "active", "since": "2026-03-01", "releaseRef": "src-03"},
 "confidentiality": "therapy-confidential"}
```

Do not add `handling` to the adoption: LA-4 already makes it, and every record that cites it in `adoption`, `person-only` (checked).

**Variant: `self-chosen` or `agent-suggested`.** Leave out `practice` and `onEnd`, set `"confidentiality": "none"`, and leave out the Party `p-01`. Those fields describe a practitioner relationship; the checker accepts them without one, but they are wrong there (§6, item 8). For `agent-suggested`, also put yourself in `parties` (`{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}`), add `"suggestedBy": "a-01"`, and write the person's Review into `reviews` right after the adoption:

```json
{"id": "rv-00", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-09-15T18:01:00Z"}
```

Without that Review the adoption stays `proposed`. **The checker does not remind you:** a context without it is still valid, and the person's question of step 3c is still served under a lens grant (§6, item 10). Write the admit Review before any record of step 3, with a `recordedAt` earlier than theirs.

**Who sees it:** only the person.

### Step 2. Keep the original in the vault (Source → `sources`)

The person's own note is a Source ([§10.1](../../spec/SPECIFICATION.md#101-source), [schema](../../spec/schema/source.schema.json)). The record holds only metadata; the bytes go into the vault:

1. Compute the hash: `shasum -a 256 <file>` (or `sha256sum <file>`). The 64 hexadecimal characters are `sha256`.
2. Compute the size in bytes: `wc -c < <file>`. That number is `size`.
3. Copy the file to `vault/<first two characters of the hash>/<hash>.<extension>`. `vaultPath` is relative to the folder that holds `context.json`.
4. The L1 checker does not open the vault (its report says `"vaultContentRead": false`): it does not notice a missing file, a wrong hash or a wrong size. Run the two commands again on the stored file and compare.

Set `maxRelease: "index"`.

```json
{"id": "src-01", "sourceKind": "journal-entry", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-29T22:00:00Z",
 "content": {"locator": {"vaultPath": "vault/2d/2d15b091fa8c73631202a6f058374bdf7a85c43569cdf0bc4e4dbdf234796b7f.md"},
             "sha256": "2d15b091fa8c73631202a6f058374bdf7a85c43569cdf0bc4e4dbdf234796b7f",
             "mediaType": "text/markdown", "size": 198},
 "capturedAt": "2026-09-29T21:45:00Z", "authorship": {"author": "subject"}, "contemporaneity": "retrospective",
 "maxRelease": "index",
 "summary": {"text": "My note after the group evening.", "authoredBy": "subject",
             "recordedAt": "2026-09-29T22:00:00Z", "method": "subject-written"},
 "retention": {"eraseOnRequest": true}, "sensitivity": "special", "categories": ["mental-health"],
 "synthetic": true}
```

The worked example ships these bytes: [examples/gestalt/vault/2d/…](examples/gestalt/vault/2d/2d15b091fa8c73631202a6f058374bdf7a85c43569cdf0bc4e4dbdf234796b7f.md).

Notes written by a therapist are a different Source, with custody, and the release is a second Source. Without a release the ceiling for every grantee is `index`; with one, `therapy` material still never goes beyond `summary` (§15.3). The hashes and sizes below stand for files that are not in the example: compute your own from your files.

```json
{"id": "src-02", "sourceKind": "practitioner-notes", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-30T18:00:00Z",
 "content": {"locator": {"vaultPath": "vault/b8/b81016884e0296fcb93739c2ea2e8dd1e2a8263bf098743644fe1f28a1ed9c67.md"},
             "sha256": "b81016884e0296fcb93739c2ea2e8dd1e2a8263bf098743644fe1f28a1ed9c67", "mediaType": "text/markdown", "size": 57},
 "capturedAt": "2026-09-30T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "custody": {"custodian": "p-01", "confidentiality": "therapy", "releaseRef": "src-03"},
 "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "src-03", "sourceKind": "practitioner-release", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-30T18:00:00Z",
 "content": {"locator": {"vaultPath": "vault/d1/d13acd83828d0a58241ee830abd2ddd45ba8d87ed0c4d7c5c91795c6b32ba5dd.md"},
             "sha256": "d13acd83828d0a58241ee830abd2ddd45ba8d87ed0c4d7c5c91795c6b32ba5dd", "mediaType": "text/markdown", "size": 71},
 "capturedAt": "2026-09-30T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "maxRelease": "index", "retention": {"eraseOnRequest": true}, "synthetic": true}
```

**Who sees it:** the person has every tier. A grantee gets at most `index`, and only under a grant that names the Source.

### Step 3. Self-description in the person's own words (Episode → `episodes`, Claim → `claims`, Interpretation → `interpretations`)

This is the whole of what the stub allows: the person's experience and their words for it. You help with structure, never with content.

**3a. The experience.** What happened, what was felt, what was done, and how it was understood then, as an Episode with the person's account ([§10.2](../../spec/SPECIFICATION.md#102-episode), [schema](../../spec/schema/episode.schema.json)). What is still open goes into `openQuestions`, in the person's words.

```json
{"id": "ep-01", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-29T22:05:00Z",
 "title": "Farewell lunch", "occurred": {"start": "2026-08-28", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-29T21:45:00Z", "addedAt": "2026-09-29T22:05:00Z",
    "accountKind": "later-reconstruction",
    "happened": "At the farewell lunch for my old team I said a quick goodbye and walked to the station.",
    "experienced": "A lump in my throat; then flat for the rest of the day.",
    "didOrTried": "Left before the coffee.",
    "understandingThen": "It was not the place for speeches.",
    "evidence": [{"source": "src-01", "selector": {"type": "whole"}}]}],
 "selection": {"selectedBy": "subject", "reason": "subject-chose"},
 "openQuestions": ["What did I not say?"], "contexts": ["work"], "synthetic": true}
```

**3b. How the person uses the perspective's words.** A Claim with facet `identity` and predicate `self-description` ([§9.4](../../spec/SPECIFICATION.md#94-claim)). It lets you use the person's own word back to them.

```json
{"id": "c-01", "facet": "identity", "predicate": "self-description",
 "text": "I use the word 'unfinished' for moments I walked away from without saying what mattered to me.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-29T22:10:00Z", "horizon": "focus",
 "synthetic": true}
```

**3c. The person's own question in the perspective.** If the person wants to keep an open question in the perspective's terms, write it as an Interpretation in question form, tagged with the lens ([§10.3](../../spec/SPECIFICATION.md#103-interpretation), [schema](../../spec/schema/interpretation.schema.json)). The descriptor's question ("What remains unfinished and seeks awareness?") may be offered only as one option; the person words it. Set `epistemic: "frame-relative"` yourself (it is not added for you), and `handling` `no-quote-back` and `subject-initiated-only`: the question comes up only when the person brings it up.

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading", "lens": {"id": "urn:ohc:lens:gestalt", "version": "0.2.0"},
 "adoption": "la-01",
 "question": "What remains unfinished from that lunch, and what would finishing it look like for me?",
 "epistemic": "frame-relative", "heldDuring": {"from": "2026-09-29"},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-29T22:12:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-quote-back", "subject-initiated-only"],
 "synthetic": true}
```

**Closing the question.** When the question no longer feels open, the person closes it with a Review in `reviews` (§6, item 5):

```json
{"id": "rv-01", "target": "in-01", "action": "mark-not-current", "by": "subject", "recordedAt": "2026-10-05T20:00:00Z"}
```

The companion still receives the question afterwards; the projection marks it `"heldNow": false` in `derived` (the stored `heldDuring` keeps no `until`; the end is computed from the Review, I7). If the person no longer wants the closed question shown at all, they add `person-only` with a second Review:

```json
{"id": "rv-02", "target": "in-01", "action": "restrict", "by": "subject", "recordedAt": "2026-10-05T20:01:00Z",
 "disclosure": {"addHandling": ["person-only"]}}
```

Both Reviews were checked; they are not in the example file.

**Who sees it:** only the person. The Episode is `special` because it cites the note; the Claim is `personal`; the question is `special`.

### Step 4. Who may see what (Party → `parties`, Grant → `grants`)

By default nobody sees anything. If the person wants a companion to recognise and use their words, first put the companion in `parties` (skip this if you already did in step 1); the id prefix `a-` is required for an agent:

```json
{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}
```

Then the person gives a read-only grant ([§12.1](../../spec/SPECIFICATION.md#121-grant), [schema](../../spec/schema/grant.schema.json)):

- `actions: ["read"]` only. Never `suggest`, `write` or `infer` for a stub.
- A selector that names the lens, plus the Claim by id; `basis.legal: "explicit-consent"`; an expiry of at most 180 days (R-G3, R-G10).
- `mode: "summary"`, `interpretations: "subject-endorsed"`, `maxSourceTier: "none"`.

```json
{"id": "g-01", "recordedAt": "2026-10-02T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:gestalt"]}, {"ids": ["c-01"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-30T09:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-10-02T09:00:00Z", "channel": "holder-ui"},
 "note": "So you can use my own word when I bring it up. No readings, no exercises."}
```

**What the companion receives.** From the repository root, run:

```sh
python3 -B tools/ohc_query.py <your context folder> project --grant g-01 --purpose self-reflection --now latest
```

For the worked example the folder is `docs/lenses/examples/gestalt`. `--purpose` is required and must be one of the grant's purposes. `--now latest` evaluates the grant at the time of the newest record in the file, so the result does not depend on today's date. The tool prints two lines (the time it used, the key) and then the projection as JSON. Served records are listed under `statements` (`lensAdoptions`: `la-01`; `claims`: `c-01`), `experience` (nothing here) and `interpretations` (`interpretations`: `in-01`). `derived` holds the computed labels (`in-01`: `"label": "frame"`), and `obligations.handling` the handling the companion must follow (`in-01`: `no-quote-back`, `subject-initiated-only`). The companion does not receive the Episode or the Source. With a therapist adoption, `la-01` and `in-01` are withheld too (LA-4); the Claim is still served, because the grant names it by id.

### Step 5. Check

From the repository root:

```sh
python3 -B tools/check.py <your context folder> --level L1 --json
```

Fix every error until it reports `"valid": true` and `"levelMet": "L1"`. The checker also compares its output with an `expected-check.json` next to the file (rule X-3), but only when the folder sits inside a folder named `examples`; your own context folder does not need one. The checker does not read the vault (step 2), does not tell you about a missing admit Review (step 1) and does not add `frame-relative` (step 3c): check all three yourself.

**Not in this recipe, while the lens is a stub:** AssessmentRecord, agent Interpretations, ModelView, Pattern, Part, Practice with the lens, RecallCue built on lens material. The checker does not stop all of them (§6, items 2 and 3); this recipe does.

## 4. Never

- **Prohibited purposes:** `personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting`. Never use any lens record for these or any other purpose of [§8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed), under any grant. A reading grounds a choice you propose for the person only under `decisionUse: approval-required`, only when the person accepted it, naming what you weighed (R-G14).
- **No agent interpretation unless the person allows it.** Write a reading, a pattern, a summary or a "what this means" in the perspective's terms only under the person's Grant (`infer` naming the lens) and adoption (I5), and it stays `frame-relative`. In the example `agentInterpretation` is `off`.
- **No exercises.** Never run or propose an exercise from the approach. Methods that work through direct experience can bring up strong material; deeper work belongs with a practitioner.
- **No practising.** Never present yourself as practising gestalt therapy or as a gestalt practitioner.
- **No suggestion unless asked** (`suggestionRequires`). Mention the perspective only when the person asks for ways of looking at their experience, as one option, in the person's own words, and only under a Grant that lets you suggest it.
- **No quoting back.** Never bring up the person's open question unless they do (`subject-initiated-only`), and never use it as proof (`no-quote-back`).
- **Trademark.** The descriptor lists no marks. Do not name a school, institute or training as if OHC represented it.

## 5. Worked example

[examples/gestalt/context.json](examples/gestalt/context.json) is one file at level L1 about Edda, who is fictional. The context and every content record carry `"synthetic": true`. It holds exactly the records of section 3, without the optional Reviews of step 3c:

| Step | Records |
|---|---|
| 0 | the envelope, with modules `core`, `governance`, `lenses` |
| 1 | the Party `p-01`, `la-01` |
| 2 | `src-01`, with its bytes in [vault/2d/](examples/gestalt/vault/2d/2d15b091fa8c73631202a6f058374bdf7a85c43569cdf0bc4e4dbdf234796b7f.md) |
| 3 | `ep-01`, `c-01`, `in-01` |
| 4 | the Party `a-01`, `g-01` |

The variants in steps 1, 2 and 3c (therapist, release, other routes, closing the question) are not in the file.

```sh
python3 -B tools/check.py docs/lenses/examples/gestalt --level L1 --json
```

It reports `"valid": true` and `"levelMet": "L1"`, with no errors and no warnings. [expected-check.json](examples/gestalt/expected-check.json) is the exact output. The projection of step 4:

```sh
python3 -B tools/ohc_query.py docs/lenses/examples/gestalt project --grant g-01 --purpose self-reflection --now latest
```

## 6. What does not fit yet

These are gaps in OHC 0.1 for this lens, found while writing this recipe and while a newcomer followed it. Each has a proposal for the next pass.

1. **The stub has nothing to hold practice.** Practices the person brings from their therapy or group (for example an experiment the group did) can be stored only as a Practice with `route: "from-practitioner"` and no template; this recipe leaves them out. *Proposal:* describe the lens after review, with practitioner-only toolkit items (`agentMayOffer: false`) and a `narrative` representation, so that such practices can cite a template.
2. **A stub adoption may claim uses it cannot have.** An adoption of this stub with `offer-practices`, `store-results` and `interpret` passes the checker, although the stub has no toolkit and no representations. *Proposal:* a warning when `uses` names what the descriptor does not describe.
3. **Assessment records in a stub are not stopped.** An AssessmentRecord in this lens passes, although a stub describes no constructs. *Proposal:* no AssessmentRecord for a lens whose descriptor is a stub. (Record `useLimits` are gone in 0.1.0-draft.2.)
4. **"Frame-relative" is manual.** A reading the person tags with a stub lens is not frame-relative unless the writer sets it (checked: without the field, `in-01` is labelled `stated`, not `frame`). Only lenses with `measurementTier` `T5` or `ontologicalStatus` `symbolic-frame` (AR-4), and lenses whose descriptor cannot be found at all (LA-6), get it automatically; this stub has a descriptor file, so it does not. *Proposal:* records tagged with a stub lens default to `frame-relative`, which keeps them out of inference (C-7).
5. **"Unfinished" has no status.** The perspective's central notion, something open that keeps asking for attention and later feels complete, can be held only as an `openQuestions` entry or a question-form Interpretation. Closing it means `mark-not-current`, which says "no longer held", not "completed", and the closed question is still served (`heldNow: false`). *Proposal:* a Review action such as `mark-complete` (or an open/closed status on question-form readings and open questions), set by the person, with its time.
6. **A practitioner's reading cannot carry the lens.** *Resolved in 0.1.0-draft.2:* LN-10 is retired and I5 applies `agentInterpretation` to agent and software authors only; a person listed in `interpretationAuthors` of the active adoption may read through the lens.
7. **The suggestion condition leaves no trace.** "The person asked for ways of looking at their experience" (`suggestionRequires`) has no place in the records, and an `agent-suggested` adoption passes without it. *Proposal:* an `agent-suggested` adoption cites the Episode, Source or message where the person asked; the checker warns when it is missing.
8. **Practitioner confidentiality without a practitioner.** LensAdoption accepts `confidentiality` `practitioner-scope` or `therapy-confidential`, and `onEnd`, without a `practice` block (checked with route `self-chosen`). Confidentiality that names a practitioner relationship, without any practitioner, is incoherent, and it can switch on the `person-only` effect of LA-4 on a self-chosen adoption by accident (checked: `la-01` and `in-01` are then withheld). *Proposal:* a rule that `confidentiality` other than `none`, and `onEnd`, require route `inherited-from-practice` and a `practice` block; an error otherwise (or a warning when the descriptor is a stub).
9. **The vault is never verified.** The L1 checker does not open the vault: a Source whose file is missing, or whose `size` or `sha256` is wrong, passes. *Proposal:* a check option (for example `--vault`) that resolves `vaultPath` relative to the context folder and verifies existence, size and hash, reporting a missing file as a warning; and run it over the published examples, which now ship their bytes.
10. **Records on a proposed adoption are served.** With an `agent-suggested` adoption and no admit Review, the adoption is withheld, but the person's question `in-01`, which cites it, is still active and served under the lens grant, with no warning (checked). *Proposal:* lens records whose `adoption` is not active inherit the adoption's computed admission (`proposed`); the checker warns when a lens-tagged record cites a non-active adoption.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
