# Noa — an episode-first context

**Authored synthetic example.** Noa, her workshop, the supplier, the coach and the agents are fictional. Third
parties appear only as pseudonymous roles. No real person's data, consent or agent behaviour is reported.

This is a complete **L2 Governed** package. It shows how OHC keeps what happened apart from how it was understood,
lets readings change over time without overwriting evidence, and lets an agent hand back what helped, only with the
person's permission.

## The story

Noa runs operations at a small furniture workshop. In March she moved a price call with the workshop's main
supplier; in May she moved the next one. In September she held the call, after a 20-minute walk and a walk-away
number written on a card.

Along the way:

- she kept a journal note, a calendar export, the supplier's email and her coach's notes in her own vault;
- she told the March episode three times: in the moment, through the calendar record, and in a later
  reconstruction;
- she read her own behaviour one way in June and another way in September;
- a reflection companion offered a cognitive-behavioural reading; she accepted part of it;
- the companion inferred that she moves calls toward the end of the week; she contested it, and the evidence stays;
- her work assistant sees only her boundaries, working preferences and work goals, never a reading.

## What the example demonstrates

| Feature | Records |
|---|---|
| Three accounts of the first episode | `ep-04` supersedes `ep-01`: in-the-moment, external record, later reconstruction; prior accounts are byte-identical |
| Readings then and now | `in-01` (June) → `in-03` (September revision); computed `heldDuring` |
| A reading that is never quoted back | `in-03` carries `no-quote-back`: an agent uses it as background and never cites it to Noa as proof |
| An agent's lens reading under an `infer` grant, with non-psychological alternatives, partly endorsed | `in-02`, `mv-01`, `prop-03`, `rv-02`, `rv-03`; the `ask-first` Event before them |
| An inferred claim the person contests; the evidence stays | `c-09`, `rv-01`; `src-02` is untouched |
| An explicit decline and a silent expiry | `rv-07` declines `c-13`; `c-14` is never answered and is computed declined when `prop-02` expires |
| A goal conflict | `t-01` between `c-03` and `c-04`, acknowledged by `rv-06` |
| Goals that change | `c-11` (April) is superseded by `c-12` (September); `c-10` keeps an intentional absence |
| A parts lens inherited from coaching (experimental) | `la-02` (`practitioner-scope`), `part-01` (person-only), `r-04` held-by |
| A practice that helped, with outcomes | `pr-01`, `oc-01`, `r-02` |
| A subject-authored recall cue (experimental) | `rc-01`, offered on 24 September, `oc-02` |
| A pattern across two episodes (experimental) | `pat-01` over `ep-04` and `ep-02`, with `ep-03` as counter-evidence |
| A health pointer, no clinical content (experimental) | `hr-01` |
| Grants | `g-01` work assistant (summary, no interpretations); `g-02` reflection companion (`infer`, recall, and step-up for the calendar export `src-02`, which it names); `g-03` a deny grant: material read through the parts lens never reaches the companion; `g-05` a former app, withdrawn by `rv-04` |
| Vault and custody | five synthetic vault objects; coach notes under coaching custody with a release (`src-04`, `src-05`); the supplier's email is third-party material held at `index` |
| One erased agent reading | `in-04` is a Tombstone, and so is its proposal `prop-04`: a Proposal whose every item is erased is erased with it. `record-erased`, the erasure notice and the purge receipt are in the Event log |
| Step-up for verbatim access | `source-access-requested` → `step-up-confirmed` → `source-opened` (tier `verbatim`) for `src-02` |
| Audit chain | `events.jsonl`: a salted hash chain with one redacted stub |
| Stored projections | `prj-0003` (work assistant) and `prj-0007` (companion, recall support) |

## Timeline

| When (2026) | What was recorded |
|---|---|
| 12 Mar | Journal note `src-01`, calendar export `src-02`, episode `ep-01`; role `c-01`; boundary `c-05` |
| 15 Mar | Grant `g-05` to a journaling app |
| 10 Apr | Goal `c-11`: leave the workshop within a year |
| 15 May | Supplier email `src-03`; episode `ep-02` |
| 2 Jun | Coach release `src-05`, coach notes `src-04`, parts-lens adoption `la-02` |
| 10 Jun | Part `part-01` |
| 20 Jun | Noa's first reading `in-01` |
| 1 Jul | Health pointer `hr-01` |
| 20 Aug | Cognitive-behavioural lens adoption `la-01` (agent readings: ask first) |
| 1 Sep | Grants `g-01`, `g-02`, `g-03`; `g-05` withdrawn |
| 2 Sep | Goals `c-02`, `c-03`, `c-04`; tension `t-01`; preference `c-06`; resource `c-08` |
| 18 Sep | The call is held: `ep-03`, practice `pr-01`, outcome `oc-01` |
| 19 Sep | Later reconstruction: `ep-04` supersedes `ep-01`; recall cue `rc-01` |
| 20 Sep | Step-up and verbatim access to `src-02`; proposals `prop-01` (`c-09`) and `prop-02` (`c-13`, `c-14`) |
| 21 Sep | Ask-first confirmation; proposal `prop-03` (`in-02`, `mv-01`); proposal `prop-04` (`in-04`) |
| 22 Sep | Contest `rv-01`, partial endorsement `rv-02`, admission `rv-03`, decline `rv-07` |
| 23 Sep | `in-04` and its proposal `prop-04` erased; notice sent and purge acknowledged |
| 24 Sep | Recall support: projection `prj-0007`, recall offered, use report; outcome `oc-02` |
| 25–26 Sep | Absence `c-10`, goal `c-12`; recall relaxed on `ep-04` (`rv-05`); revision `in-03`, question `in-05`, pattern `pat-01` |
| 6 Oct | State `c-07` |
| 9 Oct | Projection `prj-0003` to the work assistant |

## Episode-first checks and where they are shown

| # | Check | Shown in | Test |
|---|---|---|---|
| 1 | Observation and experience are kept apart from interpretation | the strands of `ep-04`; readings `in-01`…`in-05` are separate records | `test_retrospective_reading_not_in_episode` |
| 2 | Two contradicting readings coexist without being merged | `in-02` and `in-03`, linked by `r-03` (`alternative-to`) | `test_two_interpretations_coexist` |
| 3 | How the person's view changed | `in-01` → `in-03` with `heldDuring`; `c-11` → `c-12` | `test_temporal_self_model_query` |
| 4 | Patterns across episodes | `pat-01` (`ep-04`, `ep-02`) | `test_pattern_needs_two_episodes` |
| 5 | An independent agent uses the data without inheriting readings | `prj-0003` under `g-01` (`interpretations: none`) beside `prj-0007` under `g-02` | `test_independent_agent_does_not_inherit_interpretations` |
| 6 | The person contests a conclusion and the evidence survives | `rv-01` on `c-09`; `src-02` intact | `test_contest_keeps_evidence` |
| 7 | A timely reminder, with permission | `rc-01` + `g-02` (`recall`) + `oc-02` | `test_recall_requires_grant_action` |
| 8 | Did the reminder help? | `oc-02` (`result: helped`, authored by Noa) | `test_outcome_recorded_by_subject` |
| key | Can another agent use the experience without the first agent's readings? | statements and interpretations travel in separate projection members; `g-01` serves no interpretation | `test_naive_consumer_separation` |

**Recall is not crisis support. A consumer's crisis protocol always takes precedence; recall MUST NOT delay, replace
or condition it.** The recall cue here is authored by Noa, names a non-psychological alternative ("plain tiredness or
a full week") and is offered only under a grant with the `recall` action.

## Inspect the files

- [context.json](context.json): the manifest: subject, parties (role labels only), conformance, lens pins and
  collections.
- [records/](records/): one JSON Lines file per collection, each line in RFC 8785 canonical form, ordered by
  `recordedAt` then id. `in-04` and `prop-04` are Tombstones in their original positions.
- [events.jsonl](events.jsonl): 72 Events, ids and codes only. Event 50 is a redacted stub: an id-only entry about
  the erased reading `in-04` (like every Event, it held ids, codes and times, never content) was removed at Noa's
  request, and the chain still verifies through its stored `entryDigest`.
- [projections/](projections/): the two stored projections. Each carries a pairwise subject alias, a nonce, the
  computed `derived` block, `completeness: partial`, `omissions: hidden` and its digest.
- [lenses/](lenses/): byte-identical pinned copies of the two catalog descriptors this context uses.
- `vault/`: five short synthetic primary sources, named by their sha256. The checker hashes them and never reads
  them.
- [context.lock.json](context.lock.json): file-byte hashes of the package (vault excluded).
- [queries/](queries/): the expected outputs of the temporal queries.
- [expected-check.json](expected-check.json): the exact JSON output of the reference checker.

### The requests behind the stored projections

A projection serves only what the grant allows **and** what was asked for. A requested selector the grant does not
cover comes back as `not-disclosed`, whether or not matching records exist.

```json
{"format": "ohc.experimental.request", "specVersion": "0.1.0-draft", "id": "msg-0310", "from": "a-02", "to": "holder", "at": "2026-09-24T07:30:00Z",
 "grant": "g-02", "purpose": "recall-support",
 "select": [{"kinds": ["Practice", "Outcome"]}, {"kinds": ["Episode"], "contexts": ["work"]}, {"facets": ["relationship"]}],
 "mode": "summary"}
```

```json
{"format": "ohc.experimental.request", "specVersion": "0.1.0-draft", "id": "msg-0402", "from": "a-01", "to": "holder", "at": "2026-10-09T09:00:00Z",
 "grant": "g-01", "purpose": "scheduling",
 "select": [{"facets": ["boundary"]}, {"facets": ["preference"], "predicates": ["decision-brief"]}, {"facets": ["state"]}]}
```

`prj-0007` serves `pr-01`, `ep-03` and `oc-01`. Only `ep-03` among the episodes has a computed recall permission at
that time, so only it is served for recall support. The companion's request for relationships returns
`not-disclosed`. `prj-0003` serves `c-05` and `c-06` in summary form; the request for states returns `not-disclosed`,
because `g-01` does not cover them.

Aliases, handles and nonces are derived with the repository's published example holder key, so the reference tools
can reproduce them. A real holder keeps its key secret.

### Temporal queries

| File | Query | Result |
|---|---|---|
| [as-understood-at-2026-07-01--ep-04.json](queries/as-understood-at-2026-07-01--ep-04.json) | How did Noa understand the March episode on 1 July? | the two accounts known then, and `in-01` |
| [view-changes--ep-04.json](queries/view-changes--ep-04.json) | When did her view change? | `in-01` → `in-03` on 26 September |
| [stopped-convincing.json](queries/stopped-convincing.json) | Which explanations stopped convincing her? | `in-01`, superseded by her own revision |
| [actions-vs-explanations.json](queries/actions-vs-explanations.json) | Did her actions change, or only her explanation? | what she did in March, May and September, beside the readings she held at each time; no judgement |

A query about an episode includes the episodes it supersedes (`ep-04` includes `ep-01`).

## Check and interpret

From the repository root, with Python 3.9+ and `jsonschema`:

```sh
python3 tools/check.py examples/noa-episode-first --level L2 --json
```

The checker verifies the schemas, references, layer rules, inference grants, reviews, the Event chain, the lock and
that each stored projection is what the evaluation algorithm would serve at its `generatedAt`. It does not establish
that any of this is true, that consent was given in the way recorded, or how any agent behaves.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
