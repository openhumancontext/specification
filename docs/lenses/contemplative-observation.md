# Lens recipe: contemplative observation

**Recipe · lens `urn:ohc:lens:contemplative-observation` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe records that a person observes their experience in a contemplative way, without fixing it to a stable self-image, using only the steps that are safe for a stub lens: the adoption, the person's own words, practice and sources, and nothing that an agent reads into them.

The lens descriptor is [spec/lenses/contemplative-observation.lens.json](../../spec/lenses/contemplative-observation.lens.json); LensAdoption is specified in [SPECIFICATION.md §10.5](../../spec/SPECIFICATION.md#105-lensadoption), Practice and Outcome in [§17](../../spec/SPECIFICATION.md#17-practices-and-outcomes), and the schemas are in [spec/schema/](../../spec/schema/). The general adoption procedure is [CONTEXT-08](../agents/procedures/CONTEXT-08.md).

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them.

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:contemplative-observation-basic`](../../spec/playbooks/contemplative-observation-basic.playbook.json) (Contemplative observation: basic ways of working, by the OHC editors), for these situations: under strain: tired, pressed or overloaded; after a setback; looking back at something that happened. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

## 1. What you may have

| Input | What it is | Where it goes |
|---|---|---|
| Self-description in conversation | "I sit every morning", "I try to watch a thought without taking it as me" | A LensAdoption (step 1), plain Claims about how to work with the person (step 3), and the person's own Practice (step 4). |
| The person's practice journal | Notes written after sitting or after a hard moment | A Source in the vault (step 2), cited by the person's Episode and reading (step 5). |
| A teacher, a group or a retreat | The person practises with someone | Route `inherited-from-practice` with a `practice` block (step 1). The teacher's own notes are stored only together with the teacher's written release (step 2). |
| Data from a meditation app or a wearable | Session logs, heart rate, "calm" scores | At most a Source of kind `log` for session times. No state, mood or "depth" is ever derived from it (R-X4). |
| An agent's reading | — | **Only under the person's Grant.** An agent reads through the perspective only with `infer` naming the lens and the person's active adoption not set to `off` (I5); a stub's readings stay `frame-relative`, and it never runs exercises from the perspective (`agentPosture`). In the example the person allows none. |
| An instrument report | — | None. The lens has no instruments and no AssessmentRecord. |

## 2. Before you start

**This lens is a stub.** `descriptorStatus: stub`: the perspective is named, not described. It has no constructs, no toolkit, no representations, no instruments and no evidence review (`measurementTier: not-assessed`). It names no tradition. Therefore this recipe keeps only the safe steps: the adoption, the person's own statements, practice, episodes and readings, sources and grants. There is **no AssessmentRecord, no ModelView, no agent Interpretation, no Practice from an agent, no Pattern and no Part** for this lens. Every content record below is written by the person (`assertedBy: "subject"`).

**Routes of adoption.**

| Route | Allowed | What it changes |
|---|---|---|
| `inherited-from-practice` | yes | The person brings the perspective from practice with a teacher, a group or a retreat. Requires a `practice` block (`role: "teacher"`, the teacher as a Party, `relationship`, `since`). If the teacher's own notes are stored, a Source holding the teacher's release is also required, named in `practice.releaseRef` (LA-3). The adoption gives the teacher no access (LA-2). Used in the worked example. |
| `self-chosen` | yes | No teacher is involved. Drop the `practice` block, `confidentiality` and `onEnd` from the adoption, drop the teacher's Party and the teacher's Sources, and write the Practice's source as `{"route": "self-discovered", "lens": "urn:ohc:lens:contemplative-observation"}` with no `by`. Active at once. Full snippet in step 1. |
| `agent-suggested` | only as an offer | Only under a Grant with `suggest` naming the lens; the descriptor's guidance (`suggestionRequires`): an agent may mention the perspective only when the person asks for ways of looking at their experience, as one option among several. If the person takes it up, the adoption has `suggestedBy`, has no `practice` block, and stays `proposed` until the person confirms it with a Review `admit` (LA-1). Full snippets in step 1. |
| `imported` | not usual | Not in the descriptor's routes, which describe usual practice and restrict nothing. No instrument produces results in this perspective. |

**Naming a tradition.** The descriptor names none, and a living tradition is never named in the registry without its holders' consent (LN-11). The person may use their own words in their own records (for example, a Practice name). If they want a lens for their own tradition's frame, write a local descriptor `urn:ohc:lens:x-<namespace>:<name>` ([LENSES.md §5.1](../../spec/LENSES.md#51-local-lenses)); it is a stub, stays inside the person's context and is never published without its holders' consent. An agent never names, guesses or attributes a tradition.

**Consent.** The person's own records need no grant; with no grant nothing is disclosed. Records that cite this lens are `special`: sharing them needs a Grant with `basis.legal: "explicit-consent"`, a selector that reaches them, and an expiry within 180 days (R-G3, R-G10). The adoption (`la-01`) and the Practice (`pr-01`) are reached by a selector that names the lens or their ids. The person's reading (`in-01`) is frame-relative and is reached **only** by a selector that names the lens; ids alone never reach it (§12.3 step 8).

**Defaults for this lens.**

- `sensitivity: "special"`, `categories: ["mental-health"]` on records that cite the lens. If the practice is spiritual for the person, add `"belief"` (also special). See §6 on this default.
- `agentInterpretation` is `"off"`, the default the person keeps here; `interpretationAuthors` stays `["subject"]`. The person may change either; a teacher listed in `interpretationAuthors` may then author readings (I5).
- The person's readings through the lens: set `epistemic: "frame-relative"` yourself (the tools do not compute it for this lens, §6). **The checker does not catch a missing `epistemic` on a reading.** Check it before step 7; without it the reading is treated as `as-reported` and a grant that names its id serves it.
- A Practice that names the lens in `source.lens` does not take the lens default automatically: set `sensitivity` and `categories` on it by hand.
- With a teacher: recommended `confidentiality: "practitioner-scope"` and `onEnd: "ask"`. Without a teacher, leave both out.

**What is never stored.**

- A teacher's instructions, talks or texts copied into records. If kept at all, they stay in the vault as a Source, with the teacher's release.
- Levels, stages, "attainments", depth or progress ratings, or any score of the person's practice.
- States, moods or "calm" values from apps, wearables or sensors (R-X4).
- The name of a tradition, a teacher or a group that the person did not give; real names of anyone (Party labels are generic roles).
- Other participants' experiences from a group or a retreat (TP-1).

## 3. Steps

Each snippet is a record from the [worked example](examples/contemplative-observation/context.json) and validates against the schema, unless it is marked as a variant (variants were checked separately and also pass L1).

### Step 0. Prepare the context file

Make a folder for the context. Save the file as `<folder>/context.json`, put vault files under `<folder>/vault/`, and pass `<folder>` (not the file) to `check.py`. Start from this skeleton; the steps below fill its arrays.

```json
{
  "format": "ohc.context",
  "specVersion": "0.1.0-draft",
  "id": "urn:uuid:<new random UUID>",
  "version": "1",
  "subject": {"id": "urn:uuid:<another new random UUID>", "displayName": "<what the person wants to be called>"},
  "holder": "subject",
  "lang": "en",
  "created": "2026-09-20T18:00:00Z",
  "policy": {"admission": "subject-only", "resolver": "returnDialog"},
  "conformance": {},
  "parties": [],
  "lenses": [],
  "lensAdoptions": [], "sources": [], "claims": [], "practices": [], "episodes": [],
  "interpretations": [], "outcomes": [], "grants": []
}
```

- The schema requires `format`, `specVersion`, `id`, `version` and `subject.id`. `holder`, `lang` and `policy` above are the defaults written out. Change `version` with every change set.
- **A fictional person only:** add `"synthetic": true` at the root **and** on every content record. A context about a real person never carries it. The checker enforces both flags only for a folder under an `examples/` directory or an `id` that starts with `urn:ohc:example:` (the worked example uses `urn:ohc:example:ondine:contemplative-observation`). `tools/ohc_query.py` (step 7) projects without a holder key only when the root flag is set.
- For the agent-suggested route add `"reviews": []`.

Then fill `conformance`, `parties` and `lenses`: declare the modules, list the Parties by generic role, and pin the descriptor (the `sha256` is the SHA-256 of the descriptor file's bytes: `shasum -a 256 spec/lenses/contemplative-observation.lens.json`).

```json
"conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
"parties": [
  {"id": "p-01", "partyKind": "person", "label": "Practice teacher", "role": "teacher"},
  {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"},
  {"id": "a-02", "partyKind": "agent", "label": "Work assistant"}
],
"lenses": [
  {"id": "urn:ohc:lens:contemplative-observation", "version": "0.2.0", "sha256": "2dcef40d8a3565c56997241355551d4ec4d4052bd817a74cfd74a874c44e635c"}
]
```

The teacher's label is a generic role, never a name or the name of a group: every grantee that receives the adoption or the Practice also receives this Party (step 7).

### Step 1. Record the relation to the perspective: LensAdoption

`uses`: `speak-in-lens` (an agent may use the person's own words for this way of looking) and `interpret` (the person may read their episodes this way). Never `offer-practices` or `store-results`: the stub has neither practices nor results.

If the person also keeps the teacher's notes, write step 2 first: `practice.releaseRef` names the teacher's release (`src-03`). With no teacher material stored, leave `releaseRef` out.

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:contemplative-observation", "version": "0.2.0"},
 "route": "inherited-from-practice",
 "practice": {"role": "teacher", "practitioner": "p-01", "relationship": "active", "since": "2025-02-01", "releaseRef": "src-03"},
 "confidentiality": "practitioner-scope", "uses": ["speak-in-lens", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off", "onEnd": "ask",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-forward"], "synthetic": true}
```

Who sees it: only the person. Tier `special`. A grant reaches it through a selector naming the lens or its id, under explicit consent. The teacher sees nothing through it. When the practice relationship ends, write a superseding LensAdoption with `practice.relationship: "ended"`; with `onEnd: "ask"` the adoption is paused until the person decides.

**Variant: self-chosen** (no teacher). The adoption has no `practice`, `confidentiality` or `onEnd`; remove `p-01` from `parties`, skip the teacher's Sources in step 2, and use the Practice source shown in step 4.

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:contemplative-observation", "version": "0.2.0"},
 "route": "self-chosen", "uses": ["speak-in-lens", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-forward"], "synthetic": true}
```

**Variant: agent-suggested.** The person writes the adoption (or dictates it), with `suggestedBy` naming the agent and no teacher fields, and then confirms it with a Review. Add `"reviews": []` to the skeleton; drop `p-01` as for self-chosen.

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:contemplative-observation", "version": "0.2.0"},
 "route": "agent-suggested", "suggestedBy": "a-01", "uses": ["speak-in-lens", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-forward"], "synthetic": true}
```

```json
{"id": "rv-01", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-09-20T18:05:00Z"}
```

- Until `rv-01` exists, `la-01` is `proposed` and goes to no one but the person. Only the subject may write the `admit` (LA-1). Silence is not consent.
- If the agent itself records the person's yes, add `"recordedBy": "a-01", "underGrant": "g-00", "purpose": "self-reflection"` to `la-01`. Grant `g-00` must exist before `la-01`, give `suggest` (or `write`), and have a scope that names both the kind and the lens, because the adoption is special:

```json
{"id": "g-00", "recordedAt": "2026-09-20T17:50:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"kinds": ["LensAdoption"], "lenses": ["urn:ohc:lens:contemplative-observation"]}]},
 "actions": ["read", "suggest"], "mode": "summary", "interpretations": "none",
 "constraints": {"expiresAt": "2027-03-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-20T17:50:00Z", "channel": "holder-ui"}}
```

An `INF-1` error on `la-01/underGrant` here usually means that the grant lacks `suggest` or `write`, or that its scope does not name the lens. It does not mean that `underGrant` is missing. A `GR-4` error on the grant ("`infer` requires…") here means the grant reaches a special record without `explicit-consent`.

### Step 2. Keep the notes: Source

The person's journal entry goes into the vault. For every vault file, compute the values. Do not copy them from the example:

1. `sha256` = the output of `shasum -a 256 <file>` (or `sha256sum <file>`);
2. `size` = the byte count, `wc -c < <file>`;
3. move the file to `<folder>/vault/<first two hex characters of sha256>/<sha256>.<ext>` and write that path, relative to the folder, as `vaultPath`.

The L1 check does not read the vault (`"vaultContentRead": false`): a wrong hash or size still passes, so compute them. The person is the author of the journal, so no release is needed.

```json
{"id": "src-01", "sourceKind": "journal-entry",
 "content": {"locator": {"vaultPath": "vault/79/7951165ce25dba1062995826e6716283545f901a54d88483b1abdd5e6cfeea75.md"},
             "sha256": "7951165ce25dba1062995826e6716283545f901a54d88483b1abdd5e6cfeea75",
             "mediaType": "text/markdown", "size": 210},
 "capturedAt": "2026-09-22T21:30:00Z", "authorship": {"author": "subject"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index",
 "summary": {"text": "Practice-journal note after the planning meeting.", "authoredBy": "subject",
             "recordedAt": "2026-09-22T21:35:00Z", "method": "subject-written"},
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-22T21:35:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

**The teacher's notes, only with the teacher's release.** If the person wants to keep a note the teacher gave them, store two Sources: the note itself (`practitioner-notes`) and the teacher's written release (`practitioner-release`), both authored by the teacher's Party and marked `inbound`. Then set `la-01.practice.releaseRef` to the release's id (step 1). Storing the teacher's notes without `releaseRef` fails LA-3.

```json
{"id": "src-02", "sourceKind": "practitioner-notes",
 "content": {"locator": {"vaultPath": "vault/2f/2f461934c3398118ecb0abf30190545b0719bf98d15ca85a74c8f72e24811914.md"},
             "sha256": "2f461934c3398118ecb0abf30190545b0719bf98d15ca85a74c8f72e24811914",
             "mediaType": "text/markdown", "size": 219},
 "capturedAt": "2026-09-18T20:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T17:40:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "src-03", "sourceKind": "practitioner-release",
 "content": {"locator": {"vaultPath": "vault/37/37bf2083edef0444dd571621a9e0690328a8bd6979360b57eb38e7bc096cf8ec.md"},
             "sha256": "37bf2083edef0444dd571621a9e0690328a8bd6979360b57eb38e7bc096cf8ec",
             "mediaType": "text/markdown", "size": 234},
 "capturedAt": "2026-09-19T09:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T17:45:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- No `summary` on the teacher's Sources: a summary would be a selection of the teacher's words.
- No `custody`: OHC 0.1 has no confidentiality code for teaching (§6).

Who sees them: only the person. `maxRelease: "index"` on all three: no grantee ever gets more than the kind, the media type and a coarse date.

### Step 3. Say in plain words how to work with the person: Claims

The perspective itself stays the person's. What agents need is plain: what not to do, and how to listen. These Claims carry no lens and no frame words, so any agent the person chooses can respect them.

```json
{"id": "c-01", "facet": "boundary", "predicate": "never",
 "text": "Do not offer me breathing, attention or meditation exercises.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:10:00Z", "horizon": "foundation",
 "synthetic": true}
```

```json
{"id": "c-02", "facet": "preference", "predicate": "tone",
 "text": "When I describe a hard moment, ask what I noticed before asking what it means.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:12:00Z", "horizon": "foundation",
 "synthetic": true}
```

Who sees them: only the person until a grant names them. Tier `personal`, label ✓ stated.

### Step 4. Record the person's own practice: Practice

With a teacher, the practice comes from the teacher (`source.route: "from-practitioner"`, `source.by: "p-01"`). It is tagged with the lens so that one lens selector can share it. There is no `templateId`: the stub has no toolkit. Set tier and categories by hand (§2).

```json
{"id": "pr-01", "name": "Morning sitting",
 "description": "Twenty minutes of sitting and noting before opening email.",
 "practiceKind": "contemplative",
 "source": {"route": "from-practitioner", "by": "p-01", "lens": "urn:ohc:lens:contemplative-observation"},
 "steps": ["Sit before opening email", "Note what arises without following it", "Stop after twenty minutes"],
 "duration": "PT20M",
 "limits": "Not as a fix for a hard day; questions about the practice go to my teacher.",
 "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:20:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

**Variant: self-chosen or agent-suggested** (no teacher). Use `"source": {"route": "self-discovered", "lens": "urn:ohc:lens:contemplative-observation"}` with no `by`, and write `limits` without the teacher (for example, `"Not as a fix for a hard day."`). Never `from-agent`: no agent offers a practice from this lens.

Steps are the person's own short words, never the teacher's text. Who sees it: only the person; tier `special`.

### Step 5. An episode and the person's own reading of it: Episode and Interpretation

The person tells what happened. If they want, they read it in this way of looking (Interpretation with `lens`, `stance: "lens-reading"`, `epistemic: "frame-relative"`). Only the person writes this reading. Add at least one alternative that is not psychological. With the agent-suggested route, write no reading until `rv-01` exists (§6, item 10).

```json
{"id": "ep-01", "occurred": {"start": "2026-09-22", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-22T21:30:00Z", "addedAt": "2026-09-22T21:35:00Z",
    "accountKind": "in-the-moment",
    "happened": "In the planning meeting my proposal was cut from the budget.",
    "experienced": "A tight jaw, then quieter after a minute.",
    "didOrTried": "Waited before answering; asked when the next budget round opens.",
    "understandingThen": "I thought they did not value my work.",
    "evidence": [{"source": "src-01", "selector": {"type": "whole"}}]}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-22T21:35:00Z",
 "sensitivity": "sensitive", "contexts": ["work"], "synthetic": true}
```

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:contemplative-observation", "version": "0.2.0"},
 "text": "Watched as it arose, the irritation came and went; it was an event in me, not a verdict on who I am.",
 "grounds": [{"span": {"source": "src-01", "selector": {"type": "whole"}}, "kind": "evidence"}],
 "alternatives": [
   {"text": "The cut came from the overall budget, not from the quality of my proposal.", "kind": "situational"},
   {"text": "I had skipped lunch and the meeting ran into the afternoon.", "kind": "physiological"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-23T08:00:00Z",
 "epistemic": "frame-relative", "sensitivity": "special", "categories": ["mental-health"],
 "handling": ["no-quote-back"], "contexts": ["work"], "synthetic": true}
```

Before you go on, check that `in-01` has `"epistemic": "frame-relative"`. The checker does not report its absence (§2).

Who sees them: only the person. The Episode becomes `special` because it cites the special journal entry (C3); the reading is `special` and frame-relative, so only a lens selector reaches it.

### Step 6. What the practice did: Outcome

The person's own rating, linked to the episode where it happened.

```json
{"id": "oc-01", "about": {"practice": "pr-01"}, "episode": "ep-01", "result": "helped",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-23T08:05:00Z", "synthetic": true}
```

Who sees it: only the person; its tier follows the Practice (`special`).

### Step 7. Decide who may see what: Grant

The reflection companion may read what the person shares under this lens, to listen alongside the practice; it gets no `suggest`, `write` or `infer`. The work assistant sees only the plain boundary and preference, in `rule-only` mode.

```json
{"id": "g-01", "recordedAt": "2026-09-24T10:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:contemplative-observation"]}, {"ids": ["ep-01", "oc-01"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-24T10:00:00Z", "channel": "holder-ui"},
 "note": "To listen alongside my practice; never to teach it or interpret through it."}
```

```json
{"id": "g-02", "recordedAt": "2026-09-24T10:05:00Z", "grantor": "subject", "grantee": "a-02",
 "purposes": ["work-collaboration"],
 "scope": {"include": [{"facets": ["boundary", "preference"]}]},
 "actions": ["read"], "mode": "rule-only", "interpretations": "none",
 "constraints": {"expiresAt": "2027-09-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-24T10:05:00Z", "channel": "holder-ui"}}
```

What each grantee receives under §12.3, computed with the reference tools on the worked example:

| Grantee | Served | Never served |
|---|---|---|
| `a-01` Reflection companion | `la-01` (with its `practice` block, which includes the bare id `src-03`), `pr-01`, `in-01`, `ep-01`, `oc-01`, and the Party `p-01` (label "Practice teacher", role `teacher`), because `la-01` and `pr-01` point to it | `src-01`, `src-02`, `src-03` (`maxSourceTier: none`); `c-01` and `c-02` (not in scope) |
| `a-02` Work assistant | `c-01`, `c-02` (id, facet, predicate and text only) | everything that cites the lens, the episode and the sources |

The teacher sees nothing. The companion does learn that the person practises with a teacher, under the Party's label. That is why the label stays a generic role (§6, item 8). The Outcome is named by id because it carries no lens; it is served only together with its Practice.

To compute this table for your own context, run, for each grant:

```sh
python3 -B tools/ohc_query.py <folder>/context.json project --grant g-01 --purpose self-reflection --now 2026-10-10T12:00:00Z
python3 -B tools/ohc_query.py <folder>/context.json project --grant g-02 --purpose work-collaboration --now 2026-10-10T12:00:00Z
```

Served records appear under `statements`, `experience`, `interpretations` and `recall`; the Parties they point to appear under `parties`. A context without the root `"synthetic": true` needs `--holder-key-file`.

### Step 8. Check

```sh
python3 -B tools/check.py <folder> --level L1 --json
```

Expect `"valid": true` and `"levelMet": "L1"`. A folder under an `examples/` directory is compared with its `expected-check.json` (X-3); a context of your own is not. A passing check does not cover the things listed in §2 that the checker does not catch: the route, a missing `epistemic` on `in-01`, and the vault hashes.

## 4. Never

- Never interpret through this lens as an agent beyond the person's Grant (`infer` naming the lens) and adoption (I5). Your readings stay `frame-relative`. In the example the person keeps `agentInterpretation: off`, so no agent Interpretation, ModelView, Pattern or AssessmentRecord with this lens.
- Never run exercises or give practice instructions from it, and never present yourself as practising or teaching the approach (`helperMustNot`). Contemplative practice belongs with the person's own teachers and traditions (`riskNotes`).
- Never bring the perspective up unprompted. Mention it only when the person asks for ways of looking, as one option among several (`suggestionRequires`), and only under a Grant that lets you suggest it.
- Never name, guess or attribute a tradition, and never speak for one (LN-11).
- Never assess the practice: no levels, stages, depth, progress or comparison with other practitioners (`cross-person-ranking`).
- Never derive a state, a mood or "calm" from devices, voice or behaviour (R-X4).
- Never map anything from this lens to another lens (`crossLensMapping: not-allowed`), never present it as an empirical fact (C-7), and never use it for the prohibited purposes (`personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting` and the rest of §8.10), under any grant. A reading grounds a choice you propose for the person only under `decisionUse: approval-required`, only when the person accepted it (R-G14). An employer's assistant never sees records that cite this lens.
- Never quote the person's reading back as proof ("you said it was not a verdict…"): `no-quote-back`.
- Never treat the adoption as access for the teacher (LA-2), and never give the teacher's Party a personal name.

## 5. Worked example

[examples/contemplative-observation/context.json](examples/contemplative-observation/context.json): Ondine, a fictional project lead who practises with a teacher. It contains exactly the records of section 3 (without the variants): `la-01`, `src-01`, `src-02`, `src-03`, `c-01`, `c-02`, `pr-01`, `ep-01`, `in-01`, `oc-01`, `g-01`, `g-02`, with the three vault placeholders. The context root and every content record carry `"synthetic": true`.

```sh
python3 -B tools/check.py docs/lenses/examples/contemplative-observation --level L1 --json
```

Result: `"valid": true`, `"levelMet": "L1"`, no errors, no warnings ([expected-check.json](examples/contemplative-observation/expected-check.json)).

## 6. What does not fit yet

1. **The default category says "mental health" for a contemplative practice.** The descriptor's `defaults.categories` is `["mental-health"]`, while §8.2 puts spiritual practice under `belief`. A person may not want their practice labelled psychological. Proposal: `defaults.categories: ["belief"]`, or let the adoption choose between them.
2. **A resolvable stub's readings are not frame-relative, and nothing warns.** §6.3 names contemplative lenses among the frames whose readings are `frame-relative`, and a lens with no descriptor is treated that way (LA-6). The reference tools compute it only for T5 and symbolic frames, so a reading through this stub is `as-reported` unless set by hand. A reading without `epistemic` passes L1 with no warning. Proposal: every stub's results and readings are `frame-relative`; at least a warning when a lens reading through a stub has no `epistemic`.
3. **A Practice tagged with a lens does not take the lens's default tier.** C3 lists "its lens default", but the reference tools do not apply it through `Practice.source.lens`: a Practice under this lens with no tier of its own is `personal`. Proposal: apply the lens default through `source.lens`, or state that it does not apply.
4. **A teacher has no custody code.** Custody confidentiality has `therapy`, `coaching`, `legal` and `medical`, but nothing for teaching. *Resolved in 0.1.0-draft.2:* a teacher can read through the lens, since LN-10 is retired and I5 applies `agentInterpretation` to agent and software authors only; a teacher in `interpretationAuthors` of the active adoption may author a reading. Proposal: a custody code such as `teaching`.
5. **Nothing marks the lens as safe to mention but not to use.** Whether an agent suggests it is the person's grant; the only guard against an agent running exercises is the prose in `agentPosture` and `helperMustNot`. A person's boundary (step 3, `c-01`) carries it in practice. Proposal: a machine-readable `toolkitUse: "none"` (or `agentMayOffer` at lens level) for stubs.
6. **The adoption route is not checked against the descriptor's routes.** An `imported` adoption of this lens passes the checker; only `agent-suggested` is tested (LA-1). Proposal: a rule that `route` is one of the descriptor's `adoption.routes`.
7. **Teacher fields are not tied to a teacher.** A self-chosen adoption with `confidentiality: "practitioner-scope"` and `onEnd: "ask"` and no `practice` block passes. So does a Practice with `source.route: "from-practitioner"` and `by: "p-01"` when no adoption names `p-01` as practitioner. A person with no teacher can end up with a teacher-sourced Practice. Proposal: `confidentiality` other than `none`, and `onEnd`, require a `practice` block; `Practice.source.by` with route `from-practitioner` must be the practitioner of an active adoption, or a Party with role `practitioner` or `teacher`.
8. **A grantee always receives what the served records point to.** The projection for `a-01` carries the Party `p-01` (label and role) and the adoption's whole `practice` block, including `releaseRef: "src-03"`, the id of a record the grantee cannot receive. The person cannot share the perspective without showing that they practise with a teacher. Proposal: let a grant control referenced Parties (for example `constraints.parties: "include" | "role-only" | "omit"`), redact practitioner references by default for special-tier lenses, and drop references to records outside the projection.
9. **Two diagnostics point at the wrong cause.** For an agent-recorded adoption whose grant scope is `{"kinds": ["LensAdoption"]}` without the lens, or whose actions lack `suggest`, the checker reports INF-1 "MUST carry `underGrant` … and `purpose`", although both are present. With `basis.legal: "consent"`, GR-4 reports "`infer` requires … `explicit-consent`" for a grant with no `infer`; the real cause is that the grant reaches a special record. Proposal: a separate code for "the named grant does not cover this action, kind or tier" (for example INF-2), and a GR-4 message that names the special-tier reach.
10. **Records of a lens are served while the adoption is still proposed.** With the agent-suggested route and no `admit`, `la-01` is withheld, but `in-01` and `pr-01` are still served to `a-01` under the lens selector. Proposal (§12.3): a lens selector serves a lens's records only while the person's adoption of that lens is active.
11. **The root `synthetic` flag is not tied to the records' flags.** Outside example mode (a folder not under `examples/`, an id not starting with `urn:ohc:example:`), every content record can be synthetic while the root is not; the checker accepts it, and `ohc_query.py` then demands a holder key. Proposal: warn at L1 when all content records are synthetic but the root is not, and the reverse; or derive the root flag from the records.
12. **The vault is not compared with the Source at L1.** A wrong `sha256` or `size` passes (`"vaultContentRead": false`), so a recipe-follower who copies the example's hash gets a valid context that points at the wrong bytes. Proposal: an opt-in check flag (or L1 when the vault is local) that hashes vault files and compares `sha256` and `size`: an error on mismatch, a warning when the file is absent.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
