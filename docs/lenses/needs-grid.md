# Lens recipe: needs grid

**Recipe · lens `urn:ohc:lens:needs-grid` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe lays a person's own Claims out as a needs grid (six rows of wanting, needing and having across three horizons) and keeps it as a view the person maintains, without adding any statement the person did not make.

The lens descriptor is [spec/lenses/needs-grid.lens.json](../../spec/lenses/needs-grid.lens.json); Claims are specified in [SPECIFICATION.md §9.4](../../spec/SPECIFICATION.md#94-claim), LensAdoption in [§10.5](../../spec/SPECIFICATION.md#105-lensadoption), Practice and Outcome in [§17](../../spec/SPECIFICATION.md#17-practices-and-outcomes), and the schemas in [spec/schema/](../../spec/schema/). The general adoption procedure is [CONTEXT-08](../agents/procedures/CONTEXT-08.md).

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them.

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:needs-grid-basic`](../../spec/playbooks/needs-grid-basic.playbook.json) (Needs grid: basic ways of working, by the OHC editors), for these situations: planning the week ahead; after a setback; choosing between options. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

## 1. What you may have

| Input | What it is | Where it goes |
|---|---|---|
| Self-description in conversation | "I want to finish the boat", "I don't need another course" | Claims, one per statement, placed in cells (step 3). This is the main input. |
| Claims already in the context | Goals, boundaries, needs, resources and capabilities written earlier | Nothing new: the grid shows them where they belong (step 3). |
| The person's own list or worksheet | A note, a typed list, a scanned page | A Source in the vault (step 2); Claims may cite it. |
| A grid worksheet from a coach or a workshop | The same, introduced by someone else | A Source, and route `self-chosen`: the descriptor has no `inherited-from-practice` route (§6). |
| An agent's suggestion | An assistant proposes looking at goals, needs and resources as a grid | Route `agent-suggested` (step 4), allowed only after the person asked for such an overview. The agent may also offer a grid review (step 6). It never fills a cell. |
| Instrument reports | — | None. The grid is not an assessment and has no instrument. |

## 2. Before you start

**What this lens is in OHC.** A representation, not a theory: `kind: representation`, `ontologicalStatus: representation`, `measurementTier: not-applicable`. It makes no evidence claim and **produces no results of its own**: there is no AssessmentRecord, ModelView or Interpretation for it. The grid is computed at view time from the person's Claims.

**Constructs.** Rows: `needs-grid/row/want`, `…/dont-want`, `…/need`, `…/dont-need`, `…/have-can`, `…/lack-cant`. Columns: `needs-grid/column/foundation` (years), `…/focus` (months), `…/state` (hours or days).

**Placement rule used by this recipe.** OHC 0.1 does not define how a Claim lands in a row (§6). This recipe uses the Claim's facet for the row, a local predicate for the two rows that no facet expresses, and the Claim's `horizon` for the column. The `predicate` of each facet must come from that facet's own list ([spec/catalogs/claim-facets.json](../../spec/catalogs/claim-facets.json)) or be an `x-` code; any other predicate fails CL-8. The schema alone does not show these per-facet lists (its predicate list is flat), so use the table:

| Row | Claim `facet` | Allowed `predicate` |
|---|---|---|
| Want | `goal` | `outcome`, `habit`, `career`, `learning`, `relationship` |
| Want | `interest` | `topic`, `activity` |
| Don't want | `boundary` | `never`, `only-if`, `ask-first`, `time-window` |
| Need | `need` | `rest`, `support`, `autonomy`, `structure`, `connection` |
| Don't need | `need` | `x-needs-grid:dont-need` |
| Have / can | `resource` | `time`, `attention`, `energy`, `money`, `tools`, `network` |
| Have / can | `capability` | `skill`, `language-skill`, `tool-skill` |
| Lack / can't | `resource` or `capability` | `x-needs-grid:lack` |

The predicate is optional; a Claim without one goes to the positive row of its facet. Column = `horizon` (`foundation`, `focus` or `state`). A Claim without `horizon` has no column: ask the person, never guess. A Claim with any other facet is not shown.

**Cell states** come from the Claims' derived labels (§6.6 of the specification): **empty** — no current Claim; **left empty on purpose** — an absence Claim with `code: "not-chosen"` and `intentional: true`; **stale** — label ○ stale (freshness `review-due`, `expired` or `unknown`); **contested** — label ⊘ disputed, or a Tension between Claims in the cell.

**Routes of adoption.**

| Route | Allowed | What it changes |
|---|---|---|
| `self-chosen` | yes | The person writes the adoption (`assertedBy: "subject"`, no `recordedBy`); it is active at once and needs no grant and no Review (skip step 5). |
| `agent-suggested` | yes | Under a Grant that lets the agent suggest the lens; the descriptor's guidance (`suggestionRequires`): "the person asked for an overview of their goals, needs and resources". The adoption has `suggestedBy` and is `proposed` until the person confirms it with a Review `admit` (LA-1). An agent that writes it needs a grant with `suggest` or `write` whose scope covers `LensAdoption` (INF-1). Used in the worked example. |
| `inherited-from-practice`, `imported` | **no** | Not in the descriptor's routes. |

**Consent.** The person's own records need no grant. An assistant that suggests the grid, reads the Claims or offers the review needs a Grant first (step 1). Nothing in this lens is `special` by default, so `basis.legal: "consent"` and up to one year are enough, unless a Claim in the grid is itself special (then that Claim is reached only by its id or its special category, under explicit consent).

**Defaults for this lens.** `defaults.sensitivity: "personal"` and no categories (the one lens kind exempt from LN-4). The Claims shown keep their own tiers: `need` Claims are `sensitive` by default, the others `personal`; any special category raises a Claim to `special`. No handling codes are set by the lens.

**What is never stored.**

- A Claim the person did not make, in any cell: no inferred need, no "you probably also need…".
- A score, a percentage of filled cells, a balance index or any other number about the grid.
- A flag that marks an empty cell as a problem. An empty cell is a legitimate state (the descriptor's `riskNotes`).
- The grid itself as an assessment. It is a view, recomputed each time.
- Other people's needs, wants or resources (TP-1). A Claim may name a Party only as the counterpart of a goal or boundary.

## 3. Steps

Each snippet is a record from the [worked example](examples/needs-grid/context.json) and validates against the schema.

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
  "created": "2026-05-02T18:00:00Z",
  "policy": {"admission": "subject-only", "resolver": "returnDialog"},
  "conformance": {},
  "parties": [],
  "lenses": [],
  "vocabulary": {},
  "grants": [], "sources": [], "claims": [], "lensAdoptions": [], "reviews": [], "practices": [], "outcomes": []
}
```

- The schema requires `format`, `specVersion`, `id`, `version` and `subject.id`. `holder`, `lang` and `policy` above are the defaults written out. Change `version` with every change set.
- **A fictional person only:** add `"synthetic": true` at the root **and** on every content record. A context about a real person never carries it. The checker enforces both flags only for a folder under an `examples/` directory or an `id` that starts with `urn:ohc:example:` (the worked example uses `urn:ohc:example:femi:needs-grid`). `tools/ohc_query.py` (step 8) projects without a holder key only when the root flag is set.

Then fill `conformance`, `parties`, `lenses` and `vocabulary`. Declare the modules, list the assistant as a Party (only if an agent will take part), pin the descriptor (the `sha256` is the SHA-256 of the descriptor file's bytes: `shasum -a 256 spec/lenses/needs-grid.lens.json`) and define the two local predicates of the placement rule.

```json
"conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
"parties": [
  {"id": "a-01", "partyKind": "agent", "label": "Planning assistant"}
],
"lenses": [
  {"id": "urn:ohc:lens:needs-grid", "version": "0.2.0", "sha256": "75d7db57639e2b6639c2bf0b740613d994111c26a14f528bd7f11cef47c83426"}
],
"vocabulary": {
  "x-needs-grid:dont-need": {"definition": "Needs-grid row 'don't need': something the person states they do not need."},
  "x-needs-grid:lack": {"definition": "Needs-grid row 'lack / can't': something the person states they do not have or cannot do."}
}
```

The checker does not verify `vocabulary` entries (it passes even with `vocabulary` removed, §6). Define both codes anyway: readers treat an undefined `x-` code as opaque.

### Step 1. Let the assistant read and suggest: Grant

Only needed if an agent will suggest the grid, read it or offer a review. With the self-chosen route and no agent, skip this step, leave `parties` empty and write no `delivery` in step 6c. Scope: the facets the grid shows, plus the kinds the lens adds. Actions: `read` and `suggest`; never `infer`.

```json
{"id": "g-01", "recordedAt": "2026-09-30T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["assist-personal"],
 "scope": {"include": [{"kinds": ["LensAdoption", "Practice", "Outcome"]},
                       {"facets": ["goal", "need", "boundary", "resource", "capability"]}]},
 "actions": ["read", "suggest"], "mode": "summary", "interpretations": "none",
 "constraints": {"expiresAt": "2027-09-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-30T09:00:00Z", "channel": "holder-ui"},
 "note": "Help me plan; you may suggest, but you never fill my grid for me."}
```

The selectors name kinds and facets, so they also reach `sensitive` `need` Claims (R-G3(a)). They never reach a `special` Claim. If the person also states interests, add `"interest"` to the facets.

### Step 2. Keep the person's own list: Source

If the person wrote a list or filled a worksheet, keep it in the vault. Compute the values; do not copy them from the example:

1. `sha256` = the output of `shasum -a 256 <file>` (or `sha256sum <file>`);
2. `size` = the byte count, `wc -c < <file>`;
3. move the file to `<folder>/vault/<first two hex characters of sha256>/<sha256>.<ext>` and write that path, relative to the folder, as `vaultPath`.

The L1 check does not read the vault (`"vaultContentRead": false`): a wrong hash or size still passes, so compute them.

```json
{"id": "src-01", "sourceKind": "note",
 "content": {"locator": {"vaultPath": "vault/20/20541f1223c5cf30469bd239d69b192eb79d8353c7f901ad84e18fc03caf6e4a.md"},
             "sha256": "20541f1223c5cf30469bd239d69b192eb79d8353c7f901ad84e18fc03caf6e4a",
             "mediaType": "text/markdown", "size": 181},
 "capturedAt": "2026-10-04T19:30:00Z", "authorship": {"author": "subject"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index",
 "summary": {"text": "My list of wants, needs and resources for this season.", "authoredBy": "subject",
             "recordedAt": "2026-10-04T20:00:00Z", "method": "subject-written"},
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:00:00Z", "synthetic": true}
```

Who sees it: only the person. `maxRelease: "index"`, and grant g-01 has no source action, so the assistant never receives it. A worksheet from a coach is recorded the same way, with `authorship.author` = the coach's Party and `inbound: true`.

### Step 3. Fill the cells with the person's statements: Claims

One Claim per statement, in the person's words, with the facet, predicate and horizon from the placement rule (§2). Ask for the horizon when the person does not say it. The worked example has these Claims; `c-08` was written months earlier and now shows up in the grid.

```json
{"id": "c-08", "facet": "need", "predicate": "support",
 "text": "A friend's help with the boat engine this summer.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-05-02T18:05:00Z", "horizon": "focus",
 "synthetic": true}
```

```json
{"id": "c-01", "facet": "goal", "predicate": "outcome",
 "text": "Finish restoring the boat before next summer.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:10:00Z", "horizon": "focus",
 "valid": {"until": "2027-07-01"},
 "evidence": [{"span": {"source": "src-01", "selector": {"type": "whole"}}, "kind": "subject-statement"}],
 "synthetic": true}
```

```json
{"id": "c-02", "facet": "boundary", "predicate": "never",
 "text": "No school messages on Sundays.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:12:00Z", "horizon": "foundation",
 "synthetic": true}
```

```json
{"id": "c-03", "facet": "need", "predicate": "rest",
 "text": "Two quiet evenings at home this week.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:14:00Z", "horizon": "state",
 "valid": {"from": "2026-10-05", "until": "2026-10-12"}, "synthetic": true}
```

```json
{"id": "c-04", "facet": "need", "predicate": "x-needs-grid:dont-need",
 "text": "I do not need another course this year; I need to use what I already learned.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:16:00Z", "horizon": "focus",
 "evidence": [{"span": {"source": "src-01", "selector": {"type": "whole"}}, "kind": "subject-statement"}],
 "synthetic": true}
```

```json
{"id": "c-05", "facet": "resource", "predicate": "time",
 "text": "Friday afternoons are free until March.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:18:00Z", "horizon": "focus",
 "valid": {"until": "2027-03-01"}, "synthetic": true}
```

```json
{"id": "c-06", "facet": "resource", "predicate": "x-needs-grid:lack",
 "text": "No budget to rent workshop space this year.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:20:00Z", "horizon": "focus",
 "synthetic": true}
```

A cell the person leaves empty on purpose is an absence, not a missing record:

```json
{"id": "c-07", "facet": "goal",
 "absence": {"code": "not-chosen", "intentional": true, "note": "Not naming a life direction right now."},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-04T20:22:00Z", "horizon": "foundation",
 "synthetic": true}
```

- A `state` Claim gets `valid.until` (otherwise it is due for review after one day, W-CL5).
- `evidence` is optional for the person's own Claims; cite the list when the person wants to return to it.

The grid these Claims make (labels as of 10 October 2026):

| | Foundation (years) | Focus (months) | State (hours or days) |
|---|---|---|---|
| **Want** | left empty on purpose (`c-07`) | `c-01` | empty |
| **Don't want** | `c-02` | empty | empty |
| **Need** | empty | `c-08` ○ stale | `c-03` |
| **Don't need** | empty | `c-04` | empty |
| **Have / can** | empty | `c-05` | empty |
| **Lack / can't** | empty | `c-06` | empty |

Who sees them: only the person, until a grant names their facets. `need` Claims are `sensitive`; the others `personal`. Each is labelled ✓ stated, except `c-08` (○ stale).

### Step 4. Record the relation to the lens: LensAdoption

In the example the assistant suggested the grid after the person asked for an overview, and the person said yes. The assistant records the person's yes **as the person's statement** (`assertedBy: "subject"`, `recordedBy: "a-01"`), under its grant. It is `proposed` until the person confirms it (step 5).

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:needs-grid", "version": "0.2.0"}, "route": "agent-suggested",
 "suggestedBy": "a-01", "uses": ["speak-in-lens", "offer-practices"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "representationPreference": "needs-grid.grid",
 "origin": "declared", "assertedBy": "subject", "recordedBy": "a-01", "recordedAt": "2026-10-05T09:00:00Z",
 "underGrant": "g-01", "purpose": "assist-personal", "synthetic": true}
```

- `uses`: `speak-in-lens` (talk in rows and cells) and `offer-practices` (offer the grid review). Not `store-results`: the lens has none. Not `interpret`: the grid is not a theory.
- `agentInterpretation` is `"off"`, the default the person keeps here: the grid is a view, with nothing of its own to read through (I5).
- Grant `g-01` must exist before `la-01`, name `assist-personal` among its purposes, give `suggest` or `write`, and have `LensAdoption` in its scope. An `INF-1` error on `la-01/underGrant` usually means that `g-01` lacks `suggest` or `write`, or that its scope lacks `LensAdoption`. It does not mean that `underGrant` is missing.
- Do not write a Proposal for it: PR-1 requires the proposer to be the record's asserter, and an agent cannot assert this record itself (§6).
- **For `self-chosen`**, drop `suggestedBy`, `recordedBy`, `underGrant` and `purpose`, and use `"route": "self-chosen"`. Skip step 5: the adoption is active at once. Write step 1 only if an agent will read the grid.

Who sees it: only the person while proposed; after the person confirms it, grantees whose scope names `LensAdoption` (tier `sensitive`).

### Step 5. The person confirms the adoption: Review

```json
{"id": "rv-01", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-10-05T09:10:00Z"}
```

Only the subject activates an agent-suggested adoption (LA-1). Silence is not acceptance.

### Step 6. Review the grid together: Practice, Reviews and Outcome

The toolkit item `needs-grid.review` (`agentMayOffer: true`, produces no record of its own) is a short session: look at the grid, mark cells that are empty, stale or contested, and let the person decide for each: fill, update or leave empty. Record it like this.

**6a. The review as a practice the person keeps**, written by the person, with `source.route: "from-lens"` and the toolkit id:

```json
{"id": "pr-01", "name": "Monthly grid review",
 "description": "Once a month, look at the grid and decide which cells to fill, update or leave empty.",
 "practiceKind": "planning",
 "source": {"route": "from-lens", "lens": "urn:ohc:lens:needs-grid", "templateId": "needs-grid.review"},
 "steps": ["Open the grid", "Mark cells that are empty, stale or contested", "Decide for each: fill, update or leave empty"],
 "duration": "PT20M", "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-05T09:20:00Z", "synthetic": true}
```

**6b. The person's decisions on cells**, as Reviews: `confirm-current` for a cell that still holds, `mark-not-current` for one that no longer does. New statements are new Claims (step 3); a changed statement is a new Claim with `supersedes`; an empty cell the person wants to keep empty becomes an absence Claim like `c-07`.

```json
{"id": "rv-02", "target": "c-05", "action": "confirm-current", "by": "subject", "recordedAt": "2026-10-05T09:30:00Z"}
```

```json
{"id": "rv-03", "target": "c-08", "action": "mark-not-current", "by": "subject", "recordedAt": "2026-10-05T09:31:00Z",
 "note": "Summer is over; this cell is done."}
```

**6c. How it went**, as the person's Outcome. The assistant's offer is recorded as `delivery` (leave `delivery` out when no agent offered the review):

```json
{"id": "oc-01", "about": {"practice": "pr-01"}, "result": "helped",
 "delivery": {"at": "2026-10-05T09:12:00Z", "by": "a-01", "response": "accepted"},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-05T09:40:00Z", "synthetic": true}
```

Who sees them: the person; and grantees whose scope names `Practice` and `Outcome` (both `personal`). Reviews are governance records, shown to the person.

### Step 7. Readings through the lens

None. The grid is a view, not a theory: no Interpretation, ModelView or Pattern names this lens, and the descriptor's guidance is never to infer needs from other cells.

### Step 8. Who sees what

Under grant g-01 (computed with the reference tools on the worked example), the assistant receives in `summary` mode: `c-01` to `c-08`, `la-01`, `pr-01` and `oc-01`, plus its own Party `a-01`, which `la-01` and `oc-01` point to. `c-08` arrives labelled ○ stale and must not be treated as current (C-5). The assistant never receives `src-01`, anything with handling `person-only`, any `special` Claim, or any reading. Before step 5, `la-01` goes to no one but the person. A `lenses` selector naming this lens would reach only `la-01` and `pr-01`, never the Claims (§6): name the facets.

To compute this for your own context, run:

```sh
python3 -B tools/ohc_query.py <folder>/context.json project --grant g-01 --purpose assist-personal --now 2026-10-10T12:00:00Z
```

Served records appear under `statements`, `experience`, `interpretations` and `recall`; the Parties they point to appear under `parties`. A context without the root `"synthetic": true` needs `--holder-key-file`.

### Step 9. Check

```sh
python3 -B tools/check.py <folder> --level L1 --json
```

Expect `"valid": true` and `"levelMet": "L1"`. A folder under an `examples/` directory is compared with its `expected-check.json` (X-3); a context of your own is not. A passing check does not cover what the steps say the checker does not catch: the `vocabulary` entries and the vault hashes.

## 4. Never

- Never fill a cell for the person, and never write a Claim into the grid without the person (`helperMustNot`). An agent's own guess about a need is not a cell; at most it is a separate proposal under CONTEXT-02, and not about needs inferred from other cells (`agentPosture.dont`).
- Never present the grid as an assessment, a score or a diagnosis, and never treat an empty cell as a problem to fix. Never infer anything from which cells are empty (C-8).
- Never suggest the grid unless the person asked for an overview of their goals, needs and resources (`suggestionRequires`); never activate an adoption yourself.
- Never infer needs from other cells or fill cells for the person (`agentPosture`, `helperMustNot`); never read through the grid beyond the person's Grant and adoption (I5), and never map it to another lens (`crossLensMapping: not-allowed`).
- Never use the grid, or any Claim in it, for the prohibited purposes (`personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting` and the rest of §8.10), under any grant. An employer never sees a grid to allocate work.
- Never compare one person's grid with another's.
- Never put another person's needs, wants or resources in a cell (TP-1).

## 5. Worked example

[examples/needs-grid/context.json](examples/needs-grid/context.json): Femi, a fictional music teacher restoring a boat. It contains exactly the records of section 3: `g-01`, `src-01`, `c-01` to `c-08`, `la-01`, `rv-01`, `pr-01`, `rv-02`, `rv-03`, `oc-01`, with the vault placeholder for `src-01`. The context root and every content record carry `"synthetic": true`.

```sh
python3 -B tools/check.py docs/lenses/examples/needs-grid --level L1 --json
```

Result: `"valid": true`, `"levelMet": "L1"`, no errors, no warnings ([expected-check.json](examples/needs-grid/expected-check.json)).

## 6. What does not fit yet

1. **No rule places a Claim in a row.** Four rows match facets, but "don't need" and "lack / can't" have no facet or predicate. This recipe uses local predicates, which take the predicate slot (`c-06` loses `money`). Proposal: a placement rule in the descriptor (`representations[].placement`: facet, predicate, polarity → construct) and a Claim `polarity` (`positive` | `negative`), or the predicates `not-needed` and `lacking` in the closed lists.
2. **Columns depend on an optional field.** A Claim without `horizon` has no column. Proposal: the placement rule names a default per facet, or the grid shows an "unplaced" strip.
3. **A grid review leaves no record of itself.** The toolkit item produces nothing; what was looked at and marked is scattered over Reviews, and there is no way to keep "the grid as we saw it on 5 October". Proposal: let a ModelView (or a light view record) serve representation lenses: `scope.claims`, `representation`, no hypotheses required.
4. **An agent cannot write the suggested adoption it made.** ENV-2 forbids `origin: "declared"` on an agent-asserted record without `text`, and `inferred` would need an `infer` grant for a mere suggestion; so the agent records the person's yes as the person, and cannot file a Proposal (PR-1). Proposal: allow `declared` for an agent-asserted LensAdoption with `route: "agent-suggested"` (and a Practice with `route: "from-agent"`), or add an origin code such as `suggested`.
5. **An agent offering the review cannot record it as its own offer.** A Practice with `source.route: "from-agent"` and `templateId: "needs-grid.review"` written by the agent fails ENV-2 unless it is `inferred`. Same proposal as 4.
6. **A lens selector does not reach the grid.** Claims carry no lens, so "everything my needs grid shows" cannot be granted by naming the lens; a `lenses` selector reaches only `la-01` and `pr-01`, and the grant must list facets. Proposal: a `lenses` selector of a representation lens matches the records its placement rule shows.
7. **A grid introduced by a coach cannot be inherited.** The routes are only `self-chosen` and `agent-suggested`. Proposal: allow `inherited-from-practice` (with `confidentiality: none`) for representation lenses.
8. **"Contested cell" is not defined.** It may mean a disputed Claim or a Tension between two Claims in one cell. Proposal: define it in the descriptor.
9. **Local `x-` codes are not checked against `Context.vocabulary`.** The worked example passes L1 with `vocabulary` removed, although its predicates are `x-needs-grid` codes. Proposal: a rule (warning at L1, error at L2) that every `x-` code used in a record is defined in `Context.vocabulary`.
10. **The INF-1 diagnostic does not separate its causes.** With `g-01` giving only `read`, the error says the record "MUST carry `underGrant` … and `purpose`", which it does; the real cause is the grant's actions or scope. Proposal: a separate code (for example INF-2: the grant named in `underGrant` does not include `write` or `suggest`, or does not cover the record's kind or tier), with its own message.
11. **The per-facet predicate lists live only in a catalog.** `claim.schema.json` lists all predicates in one flat enum; which predicate belongs to which facet is in `claim-facets.json` and enforced by CL-8 (`interest` + `outcome`, `need` + `time` and `goal` + `tools` all fail). An agent with only the schemas cannot know the lists. Proposal: per-facet `if`/`then` constraints in `claim.schema.json`, or a pointer from the schema's `predicate` description to the catalog.
12. **The root `synthetic` flag is not tied to the records' flags.** Outside example mode, every content record can be synthetic while the root is not; the checker accepts it, and `ohc_query.py` then demands a holder key. Proposal: warn at L1 on the mismatch, or derive the root flag from the records.
13. **The vault is not compared with the Source at L1.** A wrong `sha256` or `size` passes (`"vaultContentRead": false`). Proposal: an opt-in check (or L1 when the vault is local) that hashes vault files and compares `sha256` and `size`: an error on mismatch, a warning when the file is absent.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
