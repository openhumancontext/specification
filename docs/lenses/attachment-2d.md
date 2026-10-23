# Adult attachment (two dimensions): recipe

**Recipe · lens `urn:ohc:lens:attachment-2d` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe shows how a person brings their own adult-attachment questionnaire result (two scores: attachment-related anxiety and avoidance), and what they recognise in it, into their OHC context, so that it stays about them, never about their partner, and never reaches a work context.

The descriptor is [spec/lenses/attachment-2d.lens.json](../../spec/lenses/attachment-2d.lens.json) (`descriptorStatus: draft`, measurement tier T2). Its one instrument is [ECR-R](../../spec/instruments/ecr-r.instrument.json), 36 items, scored as two scale means on a 1–7 scale.

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them.

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:attachment-2d-basic`](../../spec/playbooks/attachment-2d-basic.playbook.json) (Adult attachment: basic ways of working, by the OHC editors), for these situations: preparing a hard conversation in a close relationship; after a setback in a close relationship; looking back at something that happened in a close relationship. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

**Bringing a report through the person's window.** When an instrument's catalog entry carries an `import` block, a person can bring its result through their own window ([guide](../guides/BRING-A-RESULT.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). No entry of this lens has one yet, so the steps below record the report by hand.

## 1. What you may have

| Input | Applies? | Where it goes |
|---|---|---|
| A questionnaire result the person owns: an ECR-R score page or score sheet with the two scale means | yes | a Source (step 2) and an AssessmentRecord (step 3) |
| The person's own words: what they watch for in closeness, what they recognise in the scores | yes | Claims (step 4) |
| An occurrence in a close relationship, told by the person | yes | an Episode and the person's own reading (step 5) |
| Notes from therapy or coaching where the scores were discussed | yes, with the practitioner's release | the route `inherited-from-practice` (roles `therapist` or `coach`) and a Source of kind `practitioner-notes` under custody, as in the [process-work recipe](process-work.md), steps 1–2 |
| A result from another questionnaire, quiz or app (for example a four-category "style") | not as a result | the lens lists only ECR-R (AR-8). Keep the person's own words as a Claim, or describe that framework as a local lens ([LENSES.md §5.1](../../spec/LENSES.md#51-local-lenses)) |
| An agent's estimate of the scores, or an agent's reading through the lens | **only under the person's Grant** | `suggest` and `infer` naming the lens, the person's active adoption not set to `off` (I5), and an estimate's person-only signature (AR-2). The descriptor's guidance: never bring the topic up unprompted. In the example the person allows none. |

## 2. Before you start

**Route of adoption.** The descriptor allows all four routes (`adoption.routes`).

| Route | Who writes the LensAdoption | What it changes |
|---|---|---|
| `self-chosen` | the person (`assertedBy: "subject"`) | Active at once. This recipe follows this route. |
| `agent-suggested` | the agent, as a proposal | Only under a Grant that lets the agent suggest the lens (`suggest`, with a selector naming it); the descriptor's `suggestionRequires` says when: after the person asked for ways of looking at close relationships, as one option. The agent never brings the topic up itself (`agentPosture`). The adoption stays proposed until the person admits it (LA-1). The [cognitive-appraisal recipe](cognitive-appraisal.md) shows the steps. |
| `inherited-from-practice` | the person | A `practice` block with role `therapist` or `coach`, the practitioner as a Party, `confidentiality`, and `releaseRef` when session notes are stored (LA-3, LA-4). |
| `imported` | an importer | An import tool creates the adoption and the AssessmentRecord from a results file. Both stay proposed until the person admits them (LA-5). For a package, `tools/import_assessment.py` with `--adopt` does this. |

**Consent.** The person decides whether to adopt the lens, what is stored and who sees it. Nothing leaves the context without a Grant (R-G1). An allow grant that reaches this lens's records uses `basis.legal: "explicit-consent"` and expires within 180 days of its `recordedAt` (R-G10, R-G11, GR-1). A refusal (`effect: deny`) has no cap, so the refusal `g-02` in step 7 can run for five years.

**Defaults for this lens** (`defaults`): sensitivity `special`, category `intimate`, `reviewAfter: P2Y`.

- The LensAdoption, the AssessmentRecord and every Interpretation that names the lens are `special` (AR-5, I9). Set `"categories": ["intimate"]` on them.
- Claims, Episodes and Sources have no `lens` field, so the lens defaults do not reach them. A Claim derived from the AssessmentRecord, or citing it as evidence, inherits `special` and `intimate` through C3 (§8.4); an Episode does not. Set `"sensitivity": "special"` and `"categories": ["intimate"]` by hand on all of them anyway, so the record says it. An Episode that involves the partner also gets `third-party`.
- Handling that fits this lens: `subject-initiated-only` (an agent never brings the topic up), `no-quote-back` (never "your scores say you are anxious"), `no-leverage`.
- `agentInterpretation` is `"off"`, the default the person keeps here; `interpretationAuthors` is `["subject"]`. The person may change either (I5).
- `uses`: `store-results`, `speak-in-lens`, `interpret` (the person's own readings).

**Never stored.** ECR-R item text, item wording on a saved page, the scoring key (which items are reverse-keyed), raw item responses outside the person's own test data, and report prose. A category or "style" label as if it were a measured result. A label from another questionnaire or app renamed into this lens. Anything about the partner's or another person's attachment (TP-1). A score used as a judgement of the person.

**Synthetic marker.** In examples (a context whose `id` starts with `urn:ohc:example:`, or any folder named `examples` in the path), put `"synthetic": true` on the Context and on every Claim, Source, Episode, Interpretation, LensAdoption, AssessmentRecord, Practice and Outcome (X-1, CX-8). Never put it on a Grant, Proposal, Review or Event, nor on a Party: their schemas forbid it (S-3). For a real person, leave it out everywhere.

## 3. Steps

**0. Create the context file.** Make a folder for the context and create `context.json` in it (the single-document form). Start from this skeleton:

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:uuid:<new uuid>", "version": "1",
 "subject": {"id": "urn:uuid:<another new uuid>"},
 "holder": "subject", "lang": "en", "created": "2026-09-14T21:00:00Z",
 "conformance": {"level": "L1", "modules": ["core", "lenses", "governance"], "subjectIsAdult": true},
 "parties": [],
 "lenses": [{"id": "urn:ohc:lens:attachment-2d", "version": "0.2.0"}]}
```

- `format`, `specVersion`, `id`, `version` and `subject` are required. Change `version` whenever you change the file.
- `conformance.subjectIsAdult: true` is the holder's statement that the person is an adult who decides for themselves. Without it the checker refuses any conformance claim (R-C4) and `levelMet` is `null`. Without `conformance.level` the checker checks only L0.
- `modules`: `core` and `lenses` always, `governance` for the grants (step 7).
- `lenses` pins the descriptor this context uses.
- Each record below goes into a top-level array named after its collection: `lensAdoptions`, `sources`, `assessments`, `claims`, `episodes`, `interpretations`, `grants`. Each Party goes into `parties`.
- In an example, use ids such as `urn:ohc:example:<name>:attachment-2d` (context) and `urn:ohc:example:<name>` (subject), and add `"synthetic": true` to the Context (see §2).

**1. Adopt the lens.** Write a **LensAdoption** (collection `lensAdoptions`):

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:attachment-2d", "version": "0.2.0"}, "route": "self-chosen",
 "uses": ["store-results", "speak-in-lens", "interpret"], "interpretationAuthors": ["subject"],
 "agentInterpretation": "off", "representationPreference": "attachment-2d.two-dimension-plot",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-14T21:05:00Z",
 "sensitivity": "special", "categories": ["intimate"], "handling": ["subject-initiated-only"]}
```

Who sees it by default: only the person.

**2. Put the score page in the vault.** Save only the two scale means. The simplest way, and the one the worked example uses, is to type them into a short JSON file of your own, in this shape (one line; in an example, add `"synthetic": true`). If you keep the page itself instead, remove any item wording first.

```json
{"instrument": "ECR-R", "form": "36", "takenOn": "2026-09-14", "scaleMeans": {"anxiety": 4.2, "avoidance": 2.3}, "range": [1, 7]}
```

The folder `vault/` sits next to `context.json`, and every `vaultPath` is relative to the folder that holds `context.json`. Then:

1. compute the sha256 of the file's bytes with `shasum -a 256 <file>` (or `sha256sum <file>`) and its size in bytes with `wc -c < <file>`;
2. store it as `vault/<first two hex characters>/<sha256>.<ext>`;
3. write a **Source** (collection `sources`) with that path, hash and size.

The checker does not open the vault (its report says `"vaultContentRead": false`). A missing or empty file, or a wrong hash or size, still passes step 8, so check the path, `sha256` and `size` yourself before step 8.

The page that produced the scores is a Party: `{"id": "s-01", "partyKind": "software", "label": "Questionnaire scoring page"}`.

```json
{"id": "src-01", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/90/9009fc94cbbec1b99c895cb69ba4fcee3fdfd7091ec12bbe9f4ac45e01e67503.json"},
             "sha256": "9009fc94cbbec1b99c895cb69ba4fcee3fdfd7091ec12bbe9f4ac45e01e67503",
             "mediaType": "application/json", "size": 149},
 "capturedAt": "2026-09-14T21:10:00Z", "authorship": {"author": "s-01"}, "inbound": true, "maxRelease": "index",
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-14T21:15:00Z",
 "sensitivity": "special", "categories": ["intimate"]}
```

Who sees it by default: only the person. `maxRelease: index` keeps any grantee from the page itself.

**3. Record the result.** An **AssessmentRecord** (collection `assessments`). Fill it like this:

- `instrument.id` must be in the lens's `instruments` list (AR-8): `urn:ohc:instrument:ecr-r`, `form: "36"`.
- `instrument.version` is the edition as the publisher names it (ECR-R: `"2000"`), not the version of the OHC instrument descriptor (`0.1.0`). Leave it out if the score page does not say.
- `mode: self-report-instrument`, with `origin: derived`, `generatedBy.method` (the scoring rule as published) and `derivedFrom` (the Source) (AR-1). A copy of a vendor-style report made by an importer is `vendor-report-import` with `origin: imported` and `importedFrom`.
- `results`: one `dimension-score` per dimension, with the construct ids `attachment-2d/anxiety` and `attachment-2d/avoidance`, `raw`, and `rawRange: [1, 7]`. Add `standardized` and `normGroup` only if the report gives them; never invent a percentile.
- `validityFlags`: `incomplete` if items were skipped, `translated-form` for a translation, otherwise `[]`.
- The relationship target (romantic partners in general, or one relationship) has no field yet: put the life domain in `contexts` and say it in `note` (see §6).
- Do not store a category. The lens has no category constructs (see §6). The checker does not catch a stored category or a construct id that is not in the lens, so before step 8 confirm that `results` holds exactly two entries, both `dimension-score`, with the constructs `attachment-2d/anxiety` and `attachment-2d/avoidance`.
- No `trademarkNotice`: the lens lists no marks.

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:attachment-2d", "version": "0.2.0"},
 "instrument": {"id": "urn:ohc:instrument:ecr-r", "version": "2000", "form": "36"},
 "mode": "self-report-instrument", "assessedBy": "subject",
 "administeredAt": {"start": "2026-09-14", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "attachment-2d/anxiety", "label": "Attachment-related anxiety",
    "raw": 4.2, "rawRange": [1, 7]},
   {"type": "dimension-score", "construct": "attachment-2d/avoidance", "label": "Attachment-related avoidance",
    "raw": 2.3, "rawRange": [1, 7]}],
 "validityFlags": [],
 "reviewAfter": "P2Y", "source": "src-01",
 "origin": "derived",
 "generatedBy": {"software": "questionnaire scoring page",
                 "method": "mean of the 18 items of each scale after recoding reverse-keyed items"},
 "derivedFrom": ["src-01"], "formulatedAt": "2026-09-14T21:10:00Z",
 "assertedBy": "subject", "recordedAt": "2026-09-14T21:20:00Z",
 "sensitivity": "special", "categories": ["intimate"], "contexts": ["partner"],
 "handling": ["no-quote-back", "no-leverage", "subject-initiated-only"],
 "note": "Relationship target: romantic partners in general, as the questionnaire asks. Not about one person."}
```

Who sees it by default: only the person.

**4. Write only what the person accepts.** Show the person the two scores and ask what they recognise. For a dimension the person says fits, write a derived **Claim** (collection `claims`) that copies the number:

```json
{"id": "c-01", "facet": "disposition", "predicate": "assessed-trait",
 "text": "Attachment-related anxiety: 4.2 on the 1 to 7 scale (questionnaire, 14 September 2026).",
 "value": 4.2, "unit": "scale mean, 1-7", "horizon": "foundation", "reviewAfter": "P2Y",
 "origin": "derived", "derivedFrom": ["as-01"],
 "generatedBy": {"software": "manual entry", "method": "copy of one scale mean from as-01, at the person's request"},
 "assertedBy": "subject", "recordedAt": "2026-09-15T08:00:00Z",
 "sensitivity": "special", "categories": ["intimate"], "contexts": ["partner"],
 "handling": ["no-quote-back", "subject-initiated-only"]}
```

What the person recognises, in their own words, is a declared Claim that cites the result as evidence:

```json
{"id": "c-02", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "When someone close to me goes quiet, I start checking whether something is wrong.",
 "evidence": [{"ref": "as-01", "kind": "instrument"}], "horizon": "foundation",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-15T08:05:00Z",
 "sensitivity": "special", "categories": ["intimate"], "contexts": ["partner"], "handling": ["no-quote-back"]}
```

A dimension the person does not recognise gets no Claim; its score stays only in the AssessmentRecord. Who sees the Claims by default: only the person. The checker warns `W-CL4` on each derived `assessed-trait` Claim whose text names attachment-related anxiety (here `c-01`), because it reads the construct's name "anxiety" as a feeling. A Claim for avoidance, or a declared Claim such as `c-02`, gets no warning. The name is not a feeling, and the warning can stay (see §6).

**5. Read an occurrence through the lens (the person only).** The occurrence is an **Episode** (collection `episodes`). Say only what the other person did, never what they felt or meant (TP-1).

```json
{"id": "ep-01", "occurred": {"start": "2026-09-20", "precision": "day"}, "participants": ["p-01"],
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-20T23:00:00Z", "addedAt": "2026-09-20T23:05:00Z",
    "accountKind": "in-the-moment",
    "happened": "My partner was travelling and did not reply to messages from noon until late evening.",
    "experienced": "Restless; kept checking the phone.",
    "didOrTried": "Went for a run; sent one message instead of five.",
    "understandingThen": "Something must be wrong between us."}],
 "contexts": ["partner"], "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T23:05:00Z",
 "sensitivity": "special", "categories": ["intimate", "third-party"]}
```

The partner is a Party with a role label: `{"id": "p-01", "partyKind": "person", "label": "Partner", "role": "partner"}`. The person's own reading is an **Interpretation** (collection `interpretations`) about the episode and the result, with the ordinary explanations the person keeps open:

```json
{"id": "in-01", "about": ["ep-01", "as-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:attachment-2d", "version": "0.2.0"}, "adoption": "la-01",
 "text": "This was the anxiety side in action: I was watching for distance. It says how I relate, not anything about my partner.",
 "grounds": [{"ref": "ep-01", "kind": "evidence"}, {"ref": "as-01", "kind": "instrument"}],
 "alternatives": [{"text": "I had slept badly and was on edge anyway.", "kind": "physiological"},
                  {"text": "We had planned a call that evening and the time was unclear.", "kind": "informational"}],
 "heldDuring": {"from": "2026-09-21"},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-21T08:00:00Z",
 "sensitivity": "special", "categories": ["intimate"], "contexts": ["partner"]}
```

Who sees them by default: only the person. An agent writes such a reading only under the person's Grant and adoption (I5); in the example it writes none.

**6. Practices.** None. The lens's only toolkit item, "Record a questionnaire result", is this recipe itself; it is `instrument-use`, and an agent never offers it (`agentMayOffer: false`).

**7. Who may see what.** A reflection companion may read the result and the accepted Claims, for reflection, when the person brings the topic up (the records carry `subject-initiated-only`). The Episode is not named, so it is not served.

```json
{"id": "g-01", "recordedAt": "2026-09-21T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:attachment-2d"]}, {"ids": ["c-01", "c-02"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-15T09:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-21T09:00:00Z", "channel": "holder-ui"}}
```

A work assistant is refused everything in this lens and everything `intimate`, whatever another grant says (deny wins, R-G2):

```json
{"id": "g-02", "recordedAt": "2026-09-21T09:05:00Z", "grantor": "subject", "grantee": "a-02", "effect": "deny",
 "purposes": ["work-collaboration", "task-execution", "communication-adaptation"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:attachment-2d"]}, {"categories": ["intimate"]}]},
 "constraints": {"expiresAt": "2031-09-21T09:05:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent", "note": "An explicit refusal by the person."},
 "expressedBy": {"actor": "subject", "at": "2026-09-21T09:05:00Z", "channel": "holder-ui"}}
```

The schema requires `purposes` on a refusal too, but it does not narrow it: the holder never serves these records to `a-02`, whatever the purpose of the request (§12.3, step 6). A refusal needs no `actions`, `mode` or `interpretations`.

The grantees are Parties: `{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}` and `{"id": "a-02", "partyKind": "agent", "label": "Work assistant"}`.

**8. Check.** First confirm the vault (step 2) and the `results` of `as-01` (step 3) by hand. Then run `python3 -B tools/check.py <your context directory> --level L1 --json`. Expect `"valid": true` and `"levelMet": "L1"`, no errors, and one `W-CL4` warning on each derived `assessed-trait` Claim whose text names attachment-related anxiety, and none otherwise (step 4). What an error means:

- `R-C4`: `conformance.subjectIsAdult` is missing (step 0).
- `X-1` or `CX-8`: you are in example mode (the context id starts with `urn:ohc:example:`, or a folder in the path is named `examples`) and a content record or the Context lacks `"synthetic": true` (§2).
- `S-3` on a Grant: it carries `synthetic`, which its schema forbids.
- `AR-8`: the instrument is not ECR-R.
- `AR-2`: an agent estimate lacks `person-only`, or the flag and ceiling `agent-estimate-not-validated`.

## 4. Never

- An agent never administers the questionnaire or offers it (`agentMayOffer: false`). It estimates the scores or reads through the lens only under the person's Grant and adoption (I5), and an estimate is person-only (AR-2).
- Never assign a category or "style", from the scores or from conversation, and never present one as a diagnosis. Speak of tendencies in relating, never of attachment disorders (`languageGuidance`).
- Never describe a partner's or any other person's attachment, and never say how a relationship will go (TP-1, `doesNotEstablish`).
- Never bring the topic up unprompted, and keep the relationship target explicit (`agentPosture`).
- Never use the results in any work context (`helperMustNot`). Never use them for personnel selection, task allocation, performance evaluation, promotion decisions, ranking people against each other, persuasion targeting or any other prohibited purpose (§8.10), under any grant. A result grounds a choice you propose for the person only under `decisionUse: approval-required`, only when the person accepted it, naming what you weighed (R-G14).
- Never map the results to another lens (`crossLensMapping: not-allowed`), and never use an estimate as an input to another inference (C-7).
- Never store or repeat ECR-R items or its scoring key. The items are free for non-commercial research; commercial applications need the authors' permission (`itemsLicence`).

## 5. Worked example

[examples/attachment-2d/context.json](examples/attachment-2d/context.json) is a single-document context at level L1 about Eskil, who is fictional. It contains exactly the records of section 3: the LensAdoption `la-01`; the Source `src-01`; the AssessmentRecord `as-01`; the Claims `c-01` and `c-02`; the Episode `ep-01`; his reading `in-01`; and the Grants `g-01` and `g-02`. The folder also holds the synthetic vault file (a score summary with no item wording) and `expected-check.json`, which the checker compares with its own output for any example folder.

```sh
python3 -B tools/check.py docs/lenses/examples/attachment-2d --level L1 --json
```

Result: `"valid": true`, `"levelMet": "L1"`, no errors, one warning: `W-CL4` on `c-01` (see §6).

## 6. What does not fit yet

1. **No field for the relationship target.** The descriptor requires it (`ip.restrictions` names `relationshipTarget`; the mental model says results depend on it), but the AssessmentRecord has no such field. This recipe uses `contexts: ["partner"]` and a `note`.
2. **Categories have nowhere to go.** The descriptor allows a category only "as derived, with its rule" (AR-6), but it defines no category constructs, so a `type-assignment` result has no construct id to use. The checker does not verify that result constructs come from the lens.
3. **The affect warning misreads a construct name.** `W-CL4` fires on any derived Claim that names "attachment-related anxiety". Quarantining it (R-X3) would make it person-only, which the person did not ask for.
4. **Lens-wide limits are left to the person.** "Never in any work context" and "never unprompted" cannot be stated in the descriptor in a way the holder enforces. The person must write a deny grant and add `subject-initiated-only` to each record by hand.
5. **Instrument terms do not separate administering from recording.** ECR-R is free for non-commercial research and needs permission for commercial applications. Whether a commercial agent may record a score the person already has is not expressible.
6. **A refusal cannot be limited to some purposes.** A deny grant must list `purposes`, but the holder applies it for every purpose (§12.3, step 6). The person cannot say "refuse this for work, but allow it for personal scheduling", and the listed purposes suggest a narrower refusal than the one enforced (step 7).
7. **`instrument.version` has no defined meaning.** Examples use publication years (`"2000"`), editions or nothing, while the OHC instrument descriptors are versioned `0.1.0`. Results from different editions or translations cannot be compared reliably, and nothing pins which descriptor version was used. This recipe uses the publisher's edition.
8. **General gaps met here too:** `conformance.subjectIsAdult` is required by the checker but optional in the schema, and the checker never opens the vault, so an empty score file passes (see the [process-work recipe](process-work.md), §6 items 6–7).

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
