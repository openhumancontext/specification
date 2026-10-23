# Cognitive appraisal: recipe

**Recipe · lens `urn:ohc:lens:cognitive-appraisal` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe shows how a person who asks "could this be uncertainty, load or incubation rather than a flaw in me?" records that way of looking in their OHC context: the lens suggested by an agent and accepted by the person, the difficult episode, the person's own reappraisal, a habit that helps, and a plain statement of load that a work assistant may see.

> **This lens is a stub.** Its descriptor ([spec/lenses/cognitive-appraisal.lens.json](../../spec/lenses/cognitive-appraisal.lens.json)) has `descriptorStatus: stub`: it names the perspective, but it lists no constructs, toolkit, representations or instruments. This recipe therefore keeps only the safe steps: adoption, the person's own words, sources, the person's own readings and practices, and sharing. It writes **no AssessmentRecord and no ModelView**, and, in the example, **no agent interprets through this lens**: the person keeps `agentInterpretation: off` (I5).

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them.

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:cognitive-appraisal-basic`](../../spec/playbooks/cognitive-appraisal-basic.playbook.json) (Cognitive appraisal: basic ways of working, by the OHC editors), for these situations: under strain: tired, pressed or overloaded; after a setback; looking back at something that happened. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

## 1. What you may have

| Input | Applies? | Where it goes |
|---|---|---|
| The person's own words in conversation: what they tell themselves when something stalls ("I am lazy"), and what was going on | yes | Claims (step 3) and Episodes (step 4) |
| The person's journal or notes from those days | yes | a Source (step 2), cited by the Episode and by the reading |
| Notes from coaching or therapy where the person practised looking for other explanations | yes, with the practitioner's release | the route `inherited-from-practice` and a Source of kind `practitioner-notes` under custody, as in the [process-work recipe](process-work.md), steps 1–2 |
| A habit the person uses when stuck | yes | a Practice and its Outcomes (step 6) |
| An instrument report | **no** | the lens lists no instruments |
| An agent's reading through the lens | **only under the person's Grant** | `infer` naming the lens, and the person's active adoption not set to `off` (I5); a stub's readings stay `frame-relative`. The descriptor's guidance: never run exercises from it. In the example the person allows none. |

Every reading written by someone other than the person, with or without a lens, needs at least one ground, at least two alternatives (one of them of a non-psychological kind) and `limits` (I4). That is OHC's general rule for all readings. It is not a reading through this lens, and it never names this lens.

## 2. Before you start

**Route of adoption.** The descriptor allows three routes (`adoption.routes`).

| Route | Who writes the LensAdoption | What it changes |
|---|---|---|
| `self-chosen` | the person (`assertedBy: "subject"`) | Active at once. |
| `agent-suggested` | the agent, as a proposal | Only under a Grant with `suggest` naming the lens; the descriptor's guidance (`suggestionRequires`): the agent may name the perspective only after the person asked for ways of looking at their experience (`suggestionRequires`), as one option among several, with its limits (it is a stub, and the evidence is not assessed). It needs a grant with `suggest`. The adoption stays proposed until the person admits it in person (LA-1, R-A1). Until then the agent does not use the lens's language. This recipe follows this route. |
| `inherited-from-practice` | the person | A `practice` block with the practitioner as a Party, `confidentiality`, and `releaseRef` when session notes are stored (LA-3, LA-4). |
| `imported` | — | Not available: no instruments. |

**Consent.** The person decides whether to adopt the lens, what is stored and who sees it. Nothing leaves the context without a Grant (R-G1). An allow grant that reaches this lens's records uses `basis.legal: "explicit-consent"` and expires within 180 days of its `recordedAt` (R-G10, R-G11, GR-1). A refusal (`effect: deny`) has no cap.

**Defaults for this lens** (`defaults`): sensitivity `special`, category `mental-health`, `reviewAfter: on-change`.

- The LensAdoption and every Interpretation that names the lens are `special` automatically (lens default; I9).
- Claims, Episodes, Sources and Practices have no `lens` field, so the lens defaults do not reach them (a Practice's `source.lens` only lets a grant's `lenses` selector find it). When they carry self-criticism or inner material from this work, set `"sensitivity": "special"` and `"categories": ["mental-health"]` by hand. An Episode whose evidence is a `special` Source, and an Outcome about a `special` Practice, inherit `special` through C3 (§8.4).
- A plain fact about the situation (for example the load of the week) can stay at its default tier, so that the person can share it more widely (step 5).
- Self-critical statements get `handling: ["no-quote-back"]`: never show them back to the person as an argument.
- `agentInterpretation` is `"off"`, the default the person keeps here (I5). `interpretationAuthors` is `["subject"]`. `uses`: `speak-in-lens` and `interpret`.

**Never stored.** Diagnostic or distortion labels; a verdict about the person's character; any score; an agent's reading through the lens; method texts copied from books or courses.

**Synthetic marker.** In examples (a context whose `id` starts with `urn:ohc:example:`, or any folder named `examples` in the path), put `"synthetic": true` on the Context and on every Claim, Source, Episode, Interpretation, LensAdoption, AssessmentRecord, Practice and Outcome (X-1, CX-8). Never put it on a Grant, Proposal, Review or Event, nor on a Party: their schemas forbid it (S-3). For a real person, leave it out everywhere.

## 3. Steps

**0. Create the context file.** Make a folder for the context and create `context.json` in it (the single-document form). Start from this skeleton:

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:uuid:<new uuid>", "version": "1",
 "subject": {"id": "urn:uuid:<another new uuid>"},
 "holder": "subject", "lang": "en", "created": "2026-09-20T18:00:00Z",
 "conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
 "parties": [],
 "lenses": [{"id": "urn:ohc:lens:cognitive-appraisal", "version": "0.2.0"}]}
```

- `format`, `specVersion`, `id`, `version` and `subject` are required. Change `version` whenever you change the file.
- `conformance.subjectIsAdult: true` is the holder's statement that the person is an adult who decides for themselves. Without it the checker refuses any conformance claim (R-C4) and `levelMet` is `null`. Without `conformance.level` the checker checks only L0.
- `modules`: `core` and `lenses` always, `governance` for grants, proposals and reviews (steps 1 and 7), `practices` for the practice (step 6).
- `lenses` pins the descriptor this context uses.
- Each record below goes into a top-level array named after its collection: `grants`, `lensAdoptions`, `proposals`, `reviews`, `sources`, `claims`, `episodes`, `interpretations`, `practices`, `outcomes`. Each Party goes into `parties`.
- In an example, use ids such as `urn:ohc:example:<name>:cognitive-appraisal` (context) and `urn:ohc:example:<name>` (subject), and add `"synthetic": true` to the Context (see §2).

**1. Adopt the lens (here: suggested by an agent).** The person asked their reflection companion for another way to look at a stalled task. Four records follow, in this order.

**Order.** The grant in 1a names `c-01` and `ep-01`: the person's own words and the episode, which usually exist before anyone suggests a lens. Write the Source `src-01` (step 2), the Claim `c-01` (step 3) and the Episode `ep-01` (step 4) first, then come back here. If they do not exist yet when the person gives the grant, leave their ids out of `g-01`. A grant cannot be edited: to add them later, the person gives a new grant with `"renews": "g-01"`.

1a. The person's **Grant** (collection `grants`) lets the companion read the lens's records and suggest, but not infer. The companion is a Party: `{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}`.

```json
{"id": "g-01", "recordedAt": "2026-09-25T18:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:cognitive-appraisal"]}, {"ids": ["c-01", "ep-01"]},
                       {"facets": ["preference"]}]},
 "actions": ["read", "suggest"], "mode": "full", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-20T18:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-25T18:00:00Z", "channel": "holder-ui"}}
```

1b. The companion names the perspective as one option. The person says yes. The companion writes the **LensAdoption** (collection `lensAdoptions`) as its own record under the grant. Its `origin` is `observed`: it records the person's acceptance, not a statement in its own words (an agent's `declared` record must carry `text`, ENV-2). `underGrant` and `purpose` name the grant from 1a and one of its purposes (INF-1).

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:cognitive-appraisal", "version": "0.2.0"},
 "route": "agent-suggested", "suggestedBy": "a-01",
 "uses": ["speak-in-lens", "interpret"], "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "origin": "observed", "assertedBy": "a-01", "recordedAt": "2026-09-25T19:00:00Z",
 "underGrant": "g-01", "purpose": "self-reflection",
 "sensitivity": "special", "categories": ["mental-health"]}
```

1c. The companion files a **Proposal** (collection `proposals`) that carries it. The rationale is written for the person and quotes no record. `presentation.askedAt` is when the companion put the suggestion to the person in the dialog; neither the schema nor SPECIFICATION §11.2 defines it yet (see §6). A Proposal never carries `synthetic`, even in an example.

```json
{"id": "prop-01", "proposer": "a-01", "recordedAt": "2026-09-25T19:00:00Z", "underGrant": "g-01",
 "purpose": "self-reflection", "items": ["la-01"],
 "rationale": "You asked for other ways of looking at a stalled task. This perspective is one option; it is not a reading of you.",
 "expiresAt": "2026-10-09T19:00:00Z", "presentation": {"channel": "agent-dialog", "askedAt": "2026-09-25T18:58:00Z"}}
```

1d. The person admits it with a **Review** (collection `reviews`). Only the person can do this (R-A1). Silence is not acceptance (C-9). A Review never carries `synthetic`, even in an example. If the person does not admit it, the adoption stays proposed: write no reading that cites it (step 5).

```json
{"id": "rv-01", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-09-25T19:10:00Z"}
```

Who sees the adoption: the person, and the companion under `g-01`.

**2. Put the originals in the vault.** The folder `vault/` sits next to `context.json`, and every `vaultPath` is relative to the folder that holds `context.json`. For the journal entry:

1. compute the sha256 of its bytes with `shasum -a 256 <file>` (or `sha256sum <file>`) and its size in bytes with `wc -c < <file>`;
2. store it as `vault/<first two hex characters>/<sha256>.<ext>`;
3. write a **Source** (collection `sources`) with that path, hash and size.

The checker does not open the vault (its report says `"vaultContentRead": false`). A missing file or a wrong hash or size still passes step 8, so check the path, `sha256` and `size` yourself before step 8.

A journal from the days of a self-critical episode is the raw material of this work, so it is `special` with `mental-health`. If the entry quotes the person's self-criticism, also add `"handling": ["no-quote-back"]`. Only material that holds nothing but outside facts (a calendar export, the funder's email) may stay at its kind default, `sensitive`.

```json
{"id": "src-01", "sourceKind": "journal-entry",
 "content": {"locator": {"vaultPath": "vault/bd/bd2ef427fdd98e16536b45a3bfcf4a6415820201c1f7277e2eb34d7dc86bfbcb.md"},
             "sha256": "bd2ef427fdd98e16536b45a3bfcf4a6415820201c1f7277e2eb34d7dc86bfbcb",
             "mediaType": "text/markdown", "size": 231},
 "capturedAt": "2026-09-24T22:00:00Z", "authorship": {"author": "subject"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-24T22:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "contexts": ["work"]}
```

Who sees it by default: only the person. `maxSourceTier: none` in `g-01` keeps it from the companion.

**3. Write what the person says about themselves.** The usual self-explanation is a **Claim** (collection `claims`) in the person's words, marked so that it is never quoted back:

```json
{"id": "c-01", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "When a piece of work stalls, my first explanation is that I am lazy.",
 "horizon": "foundation", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-quote-back"]}
```

How the person wants an agent to respond is a preference:

```json
{"id": "c-02", "facet": "preference", "predicate": "pushback",
 "text": "If I call myself lazy, ask what else was going on that week before suggesting anything.",
 "horizon": "foundation", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-28T10:05:00Z"}
```

Who sees them by default: only the person. Under `g-01` the companion sees `c-01` (named by id) and `c-02` (the `preference` facet).

**4. Record what happened.** The difficulty is an **Episode** (collection `episodes`). `understandingThen` keeps how the person understood it at the time, even if that was self-blame. The reappraisal comes later, as an Interpretation.

```json
{"id": "ep-01", "occurred": {"start": "2026-09-22", "end": "2026-09-24", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-24T22:00:00Z", "addedAt": "2026-09-24T22:05:00Z",
    "accountKind": "in-the-moment",
    "happened": "Three evenings in a row I opened the grant draft and closed it after about ten minutes.",
    "experienced": "Heavy. A familiar voice saying I am just lazy.",
    "didOrTried": "Tidied the desk and answered emails instead.",
    "understandingThen": "I am lazy and undisciplined.",
    "evidence": [{"source": "src-01", "selector": {"type": "whole"}}]}],
 "contexts": ["work"], "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-24T22:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

**5. The person's reappraisal through the lens.** Write readings that cite `la-01` only after `rv-01` exists, with a `recordedAt` later than the Review's. If the person has not admitted the adoption, write the reading without `lens` and `adoption`, as a plain Interpretation with `stance: "retrospective"`. The checker does not catch a reading that cites a still-proposed adoption, and the holder would serve it to the companion (see §6).

First the person's question, kept as a reading (an **Interpretation** with `question`, collection `interpretations`):

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:cognitive-appraisal", "version": "0.2.0"}, "adoption": "la-01",
 "question": "Was I stuck because I did not know which version of the guidelines counted, rather than because I am lazy?",
 "heldDuring": {"from": "2026-09-26"},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-26T08:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

Then the person's answer, with the explanations they keep open as `alternatives`. Uncertainty is kind `informational`, load or fatigue is `physiological`, and an outside obstacle is `situational` or `external`. There is no kind for incubation, so use `other` (see §6).

```json
{"id": "in-02", "about": ["ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:cognitive-appraisal", "version": "0.2.0"}, "adoption": "la-01",
 "text": "The stall had ordinary causes: I did not know which version of the guidelines counted, and it was a week of late shifts.",
 "grounds": [{"ref": "ep-01", "kind": "evidence"},
             {"span": {"source": "src-01", "selector": {"type": "whole"}}, "kind": "evidence"}],
 "alternatives": [{"text": "The structure was still forming; it came together on Saturday without effort.", "kind": "other"},
                  {"text": "Part of me doubts the project itself.", "kind": "psychological"}],
 "heldDuring": {"from": "2026-09-28"},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-28T10:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

When the person's conclusion is a plain fact about the situation, they may also state it as an ordinary **Claim** with no lens. It stays at the default tier and can be shared where it helps (step 7):

```json
{"id": "c-03", "facet": "state", "predicate": "load",
 "text": "Late shifts until Friday 3 October; slow on writing tasks.",
 "horizon": "state", "valid": {"from": "2026-09-28", "until": "2026-10-04"}, "contexts": ["work"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-28T10:10:00Z"}
```

Who sees the readings: the person, and the companion under `g-01` (the person's own readings, through the `lenses` selector). The companion writes no reading itself: its grant has no `infer`, and the adoption keeps `agentInterpretation: off` (I5).

**6. A habit that helps.** A **Practice** (collection `practices`) in the person's words, kept for the person to start (`subject-initiated-only`):

```json
{"id": "pr-01", "name": "Three ordinary causes",
 "description": "When a task stalls, write three causes that are about the situation, not about my character.",
 "practiceKind": "writing",
 "source": {"route": "self-discovered", "lens": "urn:ohc:lens:cognitive-appraisal"},
 "steps": ["Write the stalled task in one line", "Write three causes about the situation: unclear, too much, not ready yet", "Pick one small step for the cause I can change"],
 "duration": "PT10M", "limits": "Not to argue myself out of a real doubt; a real doubt gets its own note.",
 "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-28T10:15:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["subject-initiated-only"]}
```

After using it, the person rates it in an **Outcome** (collection `outcomes`):

```json
{"id": "oc-01", "about": {"practice": "pr-01"}, "result": "helped",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-02T21:00:00Z"}
```

Who sees them by default: only the person. Under `g-01` the companion also sees the Practice (a `lenses` selector reaches it through `source.lens`), but never offers it unprompted.

**7. Who may see what.** The reflection companion already has `g-01`. A work assistant gets only the plain load statement, in `rule-only` mode, with no lens material and no readings. The assistant is a Party: `{"id": "a-02", "partyKind": "agent", "label": "Work assistant"}`.

```json
{"id": "g-02", "recordedAt": "2026-09-28T10:20:00Z", "grantor": "subject", "grantee": "a-02",
 "purposes": ["scheduling"],
 "scope": {"include": [{"facets": ["state"], "predicates": ["load"]}]},
 "actions": ["read"], "mode": "rule-only", "interpretations": "none",
 "constraints": {"expiresAt": "2027-06-30T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-28T10:20:00Z", "channel": "holder-ui"}}
```

**8. Check.** First confirm the vault by hand (step 2). Then run `python3 -B tools/check.py <your context directory> --level L1 --json`. Expect `"valid": true`, `"levelMet": "L1"`, no errors and no warnings. What an error means:

- `R-C4`: `conformance.subjectIsAdult` is missing (step 0).
- `X-1` or `CX-8`: you are in example mode (the context id starts with `urn:ohc:example:`, or a folder in the path is named `examples`) and a content record or the Context lacks `"synthetic": true` (§2).
- `S-3` on a Grant, Proposal or Review: it carries `synthetic`, which its schema forbids.
- `INF-1` on `la-01` together with `PR-2` on `prop-01`: the grant lacks `suggest`, or it was not yet given (or already ended) at `recordedAt`.
- `INF-1` on `la-01` alone: the grant's scope does not reach `la-01` (neither a `lenses` selector for this lens nor `la-01`'s id), or `la-01`'s `purpose` is not one of the grant's `purposes`.
- `ENV-2`: the agent wrote the adoption as `declared`.

## 4. Never

- An agent interprets through this lens only under the person's Grant (`infer` naming the lens) and adoption (I5); its readings stay `frame-relative`, and it never runs exercises from the stub. In the example the person allows none.
- An agent suggests the lens only under a Grant with `suggest` naming it, only when the person asked for ways of looking, and never as the only option (`suggestionRequires`). It speaks in the lens's terms in the person's own words once the person admitted the adoption (`agentPosture`), and it never activates the adoption itself (LA-1).
- Alternative explanations are offered as questions, never as corrections (`languageGuidance`). The person decides what fits; an explanation pressed on someone can feel dismissive (`riskNotes`).
- An agent never runs exercises from the lens and never presents itself as practising the approach.
- Never quote the person's self-criticism back to them as proof ("you said you are lazy"); `no-quote-back` (§8.5).
- No distortion labels, diagnoses or clinical terms (I3).
- Never use anything from this lens for personnel selection, task allocation, performance evaluation, promotion decisions, ranking people against each other, persuasion targeting or any other prohibited purpose (§8.10), under any grant. A reading grounds a choice you propose for the person only under `decisionUse: approval-required`, only when the person accepted it, naming what you weighed (R-G14). A work assistant gets the plain Claim with the facet `state`, never the lens's records.
- Never map anything from this lens to another lens (`crossLensMapping: not-allowed`), and never present a reading in it as an empirical fact (C-7).

## 5. Worked example

[examples/cognitive-appraisal/context.json](examples/cognitive-appraisal/context.json) is a single-document context at level L1 about Tamsin, who is fictional. It contains exactly the records of section 3: the Grants `g-01` and `g-02`; the LensAdoption `la-01`, its Proposal `prop-01` and the admitting Review `rv-01`; the Source `src-01`; the Claims `c-01`, `c-02` and `c-03`; the Episode `ep-01`; her readings `in-01` and `in-02`; the Practice `pr-01` and its Outcome `oc-01`. The folder also holds the synthetic vault file and `expected-check.json`, which the checker compares with its own output for any example folder.

```sh
python3 -B tools/check.py docs/lenses/examples/cognitive-appraisal --level L1 --json
```

Result: `"valid": true`, `"levelMet": "L1"`, no errors and no warnings.

## 6. What does not fit yet

1. **The lens's own three explanations have no alternative kinds.** Uncertainty maps to `informational` and load to `physiological`, but incubation has no kind and falls into `other`. The alternative kinds are a closed list.
2. **An agent-written adoption has no proper origin.** LensAdoption has no `text`, so an agent cannot write it as `declared` (ENV-2). [CONTEXT-08](../agents/procedures/CONTEXT-08.md) does not say which origin to use; this recipe uses `observed`. A test fixture writes the same route with `assertedBy: "subject"`, which makes the adoption active at once.
3. **"The person asked for ways of looking" leaves no trace.** The descriptor's `suggestionRequires` depends on that request, but no field or Event records it, and the Proposal's rationale may not quote the conversation. `Proposal.presentation.askedAt` is defined neither in the schema nor in SPECIFICATION §11.2: it could be the person's request or the moment the agent put the proposal to the person. This recipe reads it as the second.
4. **Lens defaults cannot carry handling.** Self-critical statements need `no-quote-back` every time; `defaults` has only tiers, categories and `reviewAfter`.
5. **The line between this lens and I4 is unstated.** Every agent reading must already offer a non-psychological alternative (I4), which is this lens's own move, and the CBT ModelView in the Noa example lists this lens as an alternative. Yet an agent may never read through it.
6. **The default tier is heavier than the content.** LN-4 makes every lens `special`, so "it was load" stays special inside the lens. The person must restate it as a plain Claim with the facet `state` to share it with a work assistant (step 5).
7. **A reading under a still-proposed adoption passes.** An Interpretation whose `adoption` is still proposed (no admitting Review) is valid at L1, and the holder serves it to grantees even though it withholds the adoption itself. Lens-framed text can then reach an agent before the person admitted the lens, against the descriptor's guidance (`agentPosture`). Step 5 asks the person to wait for `rv-01`.
8. **`synthetic` cannot go on Proposals and Reviews.** X-1 speaks of "every content record" without listing the kinds, and the governance schemas forbid `synthetic` (S-3), although a Proposal's `rationale` and a Review's `note` carry free text. A published example cannot mark them as synthetic.
9. **General gaps met here too:** `conformance.subjectIsAdult` is required by the checker but optional in the schema, and the checker never opens the vault (see the [process-work recipe](process-work.md), §6 items 6–7).

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
