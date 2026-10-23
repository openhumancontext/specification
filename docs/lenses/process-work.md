# Process-oriented perspective: recipe

**Recipe · lens `urn:ohc:lens:process-work` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe shows how a person brings what they have from process-oriented work (their own notes, their practitioner's summaries, their own readings and practices) into their OHC context, and what an agent may and may not do with it.

> **This lens is a stub.** Its descriptor ([spec/lenses/process-work.lens.json](../../spec/lenses/process-work.lens.json)) has `descriptorStatus: stub`: it names the perspective, but it lists no constructs, toolkit, representations or instruments. This recipe therefore keeps only the safe steps: adoption, the person's own words, sources, the person's own readings and practices, and sharing. It writes **no AssessmentRecord and no ModelView**, and, in the example, **no agent interprets through this lens**: the person keeps `agentInterpretation: off` (I5).

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them.

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:process-work-basic`](../../spec/playbooks/process-work-basic.playbook.json) (Process-oriented perspective: basic ways of working, by the OHC editors), for these situations: under strain: tired, pressed or overloaded; after a setback; looking back at something that happened. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

## 1. What you may have

| Input | Applies? | Where it goes |
|---|---|---|
| The person's own description in conversation: what they notice (a body signal, a movement, a dream, "something that wants to appear") | yes | Claims (step 3) and Episodes (step 4), in the person's words |
| The person's own notes after a session | yes | a Source of kind `note` or `journal-entry` (step 2), cited by an Episode |
| Notes or summaries from their practitioner (therapist, coach, facilitator) | yes, with the practitioner's release | a Source of kind `practitioner-notes` under custody, plus a Source of kind `practitioner-release` (step 2) |
| The practitioner's reading, as the person retells it | yes, as the person's own reading | an Interpretation by the person with a `practitioner` ground (step 5; §6 explains why not under the practitioner's name) |
| A practice the person learned in this work, or found themselves | yes | a Practice and its Outcomes (step 6) |
| An instrument report | **no** | the lens lists no instruments |
| An agent's reading through the lens | **only under the person's Grant** | `infer` naming the lens, and the person's active adoption not set to `off` (I5); a stub's readings stay `frame-relative`. The descriptor's guidance: never run exercises from it. In the example the person allows none. |

## 2. Before you start

**Route of adoption.** The descriptor allows three routes (`adoption.routes`).

| Route | Who writes the LensAdoption | What it changes |
|---|---|---|
| `self-chosen` | the person (`assertedBy: "subject"`) | Active at once. |
| `inherited-from-practice` | the person | Needs a `practice` block: the practitioner's role, the practitioner as a Party, `relationship` (`active` or `ended`), `since`, and `releaseRef` when session material is stored (LA-3). Choose `confidentiality`: `practitioner-scope` or `therapy-confidential`. With `therapy-confidential` the holder applies tier `special` and handling `person-only` automatically to the adoption and to every Interpretation, AssessmentRecord or ModelView whose `adoption` is this one (LA-4). It does **not** reach Claims, Episodes, Sources, Practices or Outcomes: if you choose it, add `"handling": ["person-only"]` by hand to `c-01`, `ep-01`, `src-02`, `src-03`, `pr-01` and `oc-01`. The grant in step 7 then serves only `c-02`. Leave `onEnd` at `ask`: when the relationship ends, the adoption is paused until the person decides. |
| `agent-suggested` | the agent, as a proposal | Only under a Grant with `suggest` naming the lens; the descriptor's guidance (`suggestionRequires`): an agent may name the perspective only when the person asked for ways of looking at their experience, as one option among several. It writes the adoption under a grant with `suggest`, and it stays proposed until the person admits it (LA-1). The [cognitive-appraisal recipe](cognitive-appraisal.md) shows this route step by step. |
| `imported` | — | Not available: the lens has no instruments to import from. |

**Consent.** The person decides whether to adopt the lens, what is stored and who sees it. Nothing leaves the context without a Grant (R-G1). An allow grant that reaches this lens's records uses `basis.legal: "explicit-consent"` and expires within 180 days of its `recordedAt` (R-G10, R-G11, GR-1). A refusal (`effect: deny`) has no cap.

**Defaults for this lens** (`defaults`): sensitivity `special`, category `mental-health`, `reviewAfter: on-change`.

- The LensAdoption and every Interpretation that names the lens are `special` automatically (lens default; I9).
- Claims and Sources keep whatever tier you write. A Source is never below `sensitive`, and a Source under `custody` is `special` on its own. Set `"sensitivity": "special"` and `"categories": ["mental-health"]` by hand on every Claim and Source that carries this work. The release `src-01` carries no session material and stays `sensitive`.
- A Practice is not raised either: its `source.lens` lets a grant's `lenses` selector find it, but it does not apply the lens defaults. Set the tier and category on it by hand.
- An Outcome about a `special` Practice, and an Episode whose evidence is a `special` Source, inherit `special` through C3 (§8.4). You may still write it on the Episode for clarity; `oc-01` in step 6 leaves it out and is still `special`.
- `agentInterpretation` is `"off"`, the default the person keeps here (I5). `interpretationAuthors` is `["subject"]`.
- `uses`: `speak-in-lens` and `interpret` (the person's own readings). Not `offer-practices` (there is no toolkit) and not `store-results` (there is no result shape).

**Never stored.** Training materials, exercise scripts or method texts of the approach; a practitioner's notes beyond what their release allows; labels from another lens or instrument restated in this lens's language; any score, type or verdict about the person; an agent's reading through the lens.

**Synthetic marker.** In examples (a context whose `id` starts with `urn:ohc:example:`, or any folder named `examples` in the path), put `"synthetic": true` on the Context and on every Claim, Source, Episode, Interpretation, LensAdoption, AssessmentRecord, Practice and Outcome (X-1, CX-8). Never put it on a Grant, Proposal, Review or Event, nor on a Party: their schemas forbid it (S-3). For a real person, leave it out everywhere.

## 3. Steps

**0. Create the context file.** Make a folder for the context and create `context.json` in it (the single-document form). Start from this skeleton:

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:uuid:<new uuid>", "version": "1",
 "subject": {"id": "urn:uuid:<another new uuid>"},
 "holder": "subject", "lang": "en", "created": "2026-09-05T18:00:00Z",
 "conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
 "parties": [],
 "lenses": [{"id": "urn:ohc:lens:process-work", "version": "0.2.0"}]}
```

- `format`, `specVersion`, `id`, `version` and `subject` are required. Change `version` whenever you change the file.
- `conformance.subjectIsAdult: true` is the holder's statement that the person is an adult who decides for themselves. Without it the checker refuses any conformance claim (R-C4) and `levelMet` is `null`. Without `conformance.level` the checker checks only L0.
- `modules`: `core` and `lenses` always, `governance` for the grant (step 7), `practices` for the practice (step 6).
- `lenses` pins the descriptor this context uses.
- Each record below goes into a top-level array named after its collection: `lensAdoptions`, `sources`, `claims`, `episodes`, `interpretations`, `practices`, `outcomes`, `grants`. Each Party goes into `parties`.
- In an example, use ids such as `urn:ohc:example:<name>:process-work` (context) and `urn:ohc:example:<name>` (subject), and add `"synthetic": true` to the Context (see §2).

**1. Adopt the lens.** The person says they work with this perspective. Add the practitioner to `parties` with a role label, never a name: `{"id": "p-01", "partyKind": "person", "label": "Practitioner", "role": "practitioner"}`. Then write a **LensAdoption** (collection `lensAdoptions`):

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:process-work", "version": "0.2.0"},
 "route": "inherited-from-practice",
 "practice": {"role": "therapist", "practitioner": "p-01", "relationship": "active", "since": "2025-11-01",
              "releaseRef": "src-01"},
 "confidentiality": "practitioner-scope", "uses": ["speak-in-lens", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off", "onEnd": "ask",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-05T18:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-forward"]}
```

Who sees it by default: only the person. The adoption gives the practitioner no access (LA-2).

**2. Put the originals in the vault.** The folder `vault/` sits next to `context.json`, and every `vaultPath` is relative to the folder that holds `context.json`. For each file (the practitioner's release, the person's own note, the practitioner's summary):

1. compute the sha256 of its bytes with `shasum -a 256 <file>` (or `sha256sum <file>`) and its size in bytes with `wc -c < <file>`;
2. store it as `vault/<first two hex characters>/<sha256>.<ext>`;
3. write a **Source** (collection `sources`) with that path, hash and size.

The checker does not open the vault (its report says `"vaultContentRead": false`). A missing file or a wrong hash or size still passes step 8, so check the path, `sha256` and `size` yourself before step 8.

The release:

```json
{"id": "src-01", "sourceKind": "practitioner-release",
 "content": {"locator": {"vaultPath": "vault/f8/f80a523bdc2eebff12a5884e805cc272be41e389d56f07d5ec2ff520dca2252e.md"},
             "sha256": "f80a523bdc2eebff12a5884e805cc272be41e389d56f07d5ec2ff520dca2252e",
             "mediaType": "text/markdown", "size": 174},
 "authorship": {"author": "p-01"}, "inbound": true, "maxRelease": "index",
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-05T18:00:00Z",
 "sensitivity": "sensitive"}
```

The practitioner's summary is held under the practitioner's confidentiality (`custody`). Choose `custody.confidentiality` from the practitioner's role in the adoption (`practice.role`):

| `practice.role` | `custody.confidentiality` | Ceiling for grantees without / with a release (§15.3) |
|---|---|---|
| `therapist` | `therapy` | `index` / `summary` |
| `coach` | `coaching` | `index` / `excerpt` |
| `facilitator`, `teacher` or `other` | `therapy` when the sessions are therapeutic, otherwise `coaching` | as above |

Keep `maxRelease` at `index` either way.

```json
{"id": "src-03", "sourceKind": "practitioner-notes",
 "content": {"locator": {"vaultPath": "vault/f0/f019f7f2face1e47c00a3739818e5eaf79fe0a06d7d4dec3df3457391bce52cc.md"},
             "sha256": "f019f7f2face1e47c00a3739818e5eaf79fe0a06d7d4dec3df3457391bce52cc",
             "mediaType": "text/markdown", "size": 214},
 "capturedAt": "2026-09-13T10:00:00Z", "authorship": {"author": "p-01"}, "inbound": true, "maxRelease": "index",
 "custody": {"custodian": "p-01", "confidentiality": "therapy", "releaseRef": "src-01"},
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-13T19:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

The person's own note after the session:

```json
{"id": "src-02", "sourceKind": "note",
 "content": {"locator": {"vaultPath": "vault/2e/2ec43e0965b6a0221313c116fabf00043b1c17679d145430e6e39faa7d935802.md"},
             "sha256": "2ec43e0965b6a0221313c116fabf00043b1c17679d145430e6e39faa7d935802",
             "mediaType": "text/markdown", "size": 229},
 "capturedAt": "2026-09-12T20:00:00Z", "authorship": {"author": "subject"}, "maxRelease": "index",
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-12T20:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

Who sees Sources by default: only the person, who always has every tier (V-0). No grantee ever gets more than `maxRelease`, and custody caps it further: `therapy` gives `index` without a release and `summary` with one (§15.3).

**3. Write what the person says about themselves.** Each statement is a **Claim** (collection `claims`) in the person's own words. A self-description:

```json
{"id": "c-01", "facet": "identity", "predicate": "self-description",
 "text": "I work with a process-oriented therapist. I pay attention to body signals and dreams that do not fit how I usually see myself.",
 "horizon": "focus", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-05T18:10:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

How agents should treat this material is a boundary. It carries no inner material, so it can stay at the default tier and reach any agent the person chooses:

```json
{"id": "c-02", "facet": "boundary", "predicate": "never",
 "text": "Do not explain my body signals or dreams to me. Ask what I notice.",
 "horizon": "foundation", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-05T18:12:00Z"}
```

Who sees them by default: only the person.

**4. Record what happened.** One occurrence is an **Episode** (collection `episodes`) with the person's account, separated into what happened, what was experienced, what was done and how it was understood then. A later reading never goes here (EP-4).

```json
{"id": "ep-01", "occurred": {"start": "2026-09-12", "precision": "day"}, "participants": ["p-01"],
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-12T20:00:00Z", "addedAt": "2026-09-12T20:05:00Z",
    "accountKind": "in-the-moment",
    "happened": "While I talked about moving flats, my left hand kept pushing against my knee.",
    "experienced": "Pressure in the hand; more curious than worried.",
    "didOrTried": "Let the hand push against a cushion for about a minute.",
    "understandingThen": "Just restlessness.",
    "evidence": [{"source": "src-02", "selector": {"type": "whole"}}]}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-12T20:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

Who sees it by default: only the person.

**5. The person's own reading through the lens.** The person reads the episode in the lens's terms: an **Interpretation** (collection `interpretations`) with `stance: lens-reading`. When the reading came from the practitioner, the person writes it in their own words and adds a ground of kind `practitioner` that points at the practitioner's notes. Alternatives are optional for the person, and worth adding.

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:process-work", "version": "0.2.0"}, "adoption": "la-01",
 "text": "The pushing hand looks like a less familiar side of me that wants to push back about the move.",
 "grounds": [{"ref": "ep-01", "kind": "evidence"},
             {"span": {"source": "src-03", "selector": {"type": "whole"}}, "kind": "practitioner"}],
 "alternatives": [{"text": "Two short nights before the session; the hand may just have been tired.", "kind": "physiological"}],
 "heldDuring": {"from": "2026-09-14"},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-14T08:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"]}
```

Who sees it by default: only the person. In the example an agent never writes this record: with `agentInterpretation: off` and only the person in `interpretationAuthors`, the checker refuses any non-subject reading that names this lens (I5).

**6. A practice the person already uses.** A **Practice** (collection `practices`) in the person's words, with where it came from. Add `handling: ["subject-initiated-only"]`, so that an agent uses it only when the person brings it up.

```json
{"id": "pr-01", "name": "Hand against the cushion",
 "description": "When my hand starts pushing in a hard conversation, I let it push against something for a minute and notice what it would say.",
 "practiceKind": "movement",
 "source": {"route": "from-practitioner", "lens": "urn:ohc:lens:process-work", "by": "p-01"},
 "steps": ["Notice the hand", "Let it push against a cushion or a wall for about a minute", "Write one line: what would it say?"],
 "limits": "Not in meetings. If it gets too strong, stop and bring it to the next session.",
 "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-14T08:10:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["subject-initiated-only"]}
```

After using it, the person rates it in an **Outcome** (collection `outcomes`):

```json
{"id": "oc-01", "about": {"practice": "pr-01"}, "result": "partly",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-30T19:00:00Z"}
```

Who sees them by default: only the person.

**7. Who may see what.** A **Grant** (collection `grants`) for a reflection companion: read only, for self-reflection, the person's own readings only. A `lenses` selector reaches the LensAdoption, the Interpretations and the Practice (through `source.lens`). Claims and Episodes carry no lens, so they are named by `ids`.

```json
{"id": "g-01", "recordedAt": "2026-10-01T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:process-work"]}, {"ids": ["c-01", "c-02", "ep-01"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-29T09:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-10-01T09:00:00Z", "channel": "holder-ui"}}
```

The grantee is a Party (`{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}`). With this grant the agent may speak in the person's words, follow the boundary `c-02`, and use the practice only when the person starts. It gets no `suggest` and no `infer`, because there is nothing it may propose through this lens. The Outcome is not served: the grant does not name it.

**8. Check.** First confirm the vault by hand (step 2). Then run `python3 -B tools/check.py <your context directory> --level L1 --json`. Expect `"valid": true`, `"levelMet": "L1"`, no errors and no warnings. What an error means:

- `R-C4`: `conformance.subjectIsAdult` is missing (step 0).
- `X-1` or `CX-8`: you are in example mode (the context id starts with `urn:ohc:example:`, or a folder in the path is named `examples`) and a content record or the Context lacks `"synthetic": true` (§2).
- `S-3` on a Grant: it carries `synthetic`, which its schema forbids.
- `I5`: a non-subject reading names this lens without the grant or adoption that allows it.

## 4. Never

- An agent interprets through this lens only under the person's Grant (`infer` naming the lens) and adoption (I5); its readings stay `frame-relative`, and it never runs exercises from the stub. In the example the person allows none.
- An agent mentions the perspective only under a Grant that lets it suggest the lens, only when the person asked for ways of looking, as one option among several (`suggestionRequires`), and speaks in its terms in the person's own words once the person adopted it (`agentPosture`).
- An agent never runs exercises from it, never presents itself as practising the approach, and never turns a stored Practice into an offer the person did not start. Experiential work can bring up strong material; deeper work belongs with a practitioner (`riskNotes`).
- Never use anything from this lens for personnel selection, task allocation, performance evaluation, promotion decisions, ranking people against each other, persuasion targeting or any other prohibited purpose (§8.10), under any grant. A reading grounds a choice you propose for the person only under `decisionUse: approval-required`, only when the person accepted it, naming what you weighed (R-G14).
- Never map anything from this lens to another lens (`crossLensMapping: not-allowed`), and never present a reading in it as an empirical fact (C-7).
- Never describe the practitioner's or other participants' inner states, for example in group work (TP-1).
- The descriptor lists no marks. Use the plain name "process-oriented perspective"; do not copy the approach's training texts or exercise scripts into any record.

## 5. Worked example

[examples/process-work/context.json](examples/process-work/context.json) is a single-document context at level L1 about Orsolya, who is fictional. It contains exactly the records of section 3: the LensAdoption `la-01`; the Sources `src-01` (release), `src-02` (her note) and `src-03` (the practitioner's summary); the Claims `c-01` and `c-02`; the Episode `ep-01`; her reading `in-01`; the Practice `pr-01` and its Outcome `oc-01`; and the Grant `g-01`. The folder also holds the three synthetic vault files and `expected-check.json`, which the checker compares with its own output for any example folder.

```sh
python3 -B tools/check.py docs/lenses/examples/process-work --level L1 --json
```

Result: `"valid": true`, `"levelMet": "L1"`, no errors and no warnings.

## 6. What does not fit yet

1. **A practitioner's reading cannot carry the lens under the practitioner's name.** *Resolved in 0.1.0-draft.2:* LN-10 is retired and I5 applies `agentInterpretation` to agent and software authors only, so a practitioner listed in `interpretationAuthors` of the active adoption may author the reading. The example keeps the workaround of step 5, the person's own reading with a `practitioner` ground.
2. **Records with no lens field.** Claims, Episodes, Sources and Outcomes cannot say that they belong to this lens. A `lenses` selector does not reach them, so every grant must list them by id, and the lens's default tier and category must be set by hand.
3. **Inner occurrences.** Dreams, body signals and gestures are the main material of this perspective. An Episode has no way to say that an occurrence is inner: `happened` is defined as observable events, and `experienced` loses the event.
4. **A stub has no result shape and no toolkit.** [LENSES.md §5.1](../../spec/LENSES.md#51-local-lenses) says a person may keep results in a stub, but no constructs or representations say what a result is. Practices learned in this work can only be ordinary Practices, and keeping agents from offering them depends on the person adding `subject-initiated-only`.
5. **`therapy-confidential` protects only the reading layer.** LA-4 reaches only records with an `adoption` field. Claims, Episodes, Sources, Practices (linked only through `source.lens`) and Outcomes that carry the same therapy material stay shareable unless the person adds `person-only` to each one (§2). A person who picks `therapy-confidential` reasonably expects all of it to be person-only.
6. **`subjectIsAdult` is required, but the schema does not say so.** `conformance.subjectIsAdult` is optional in `context.schema.json`, yet the checker refuses every conformance claim without it (R-C4). An agent that works only from the schemas cannot learn this.
7. **The vault is not checked.** The checker never opens `vaultPath`, so a missing file, a wrong `sha256` or a wrong `size` still passes L1. Step 2 asks the person to check by hand.
8. **Practitioner roles and custody kinds do not line up.** `practice.role` allows `facilitator`, `teacher` and `other`, but `custody.confidentiality` has only `therapy`, `coaching`, `legal` and `medical`. The table in step 2 is this recipe's guess, and the choice changes the release ceiling.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
