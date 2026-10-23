# Mara — episode-first, with a persistent study companion

**Authored synthetic example.** Mara is fictional. No real person's data is included.

Mara is learning Portuguese with a persistent study companion, an agent that works with her over months. This is
one JSON file at conformance level **L1 Grounded**. It shows how such an agent keeps its model of Mara reconcilable
with Mara's own view ([CONTEXT-09](../../docs/agents/procedures/CONTEXT-09.md)).

## What it demonstrates

- **A context can start from an experience.** `ep-01` is Mara's account of a conversation drill she stopped early,
  with what she understood at the time ("too tired after work"). The companion added an **observer account** of the
  same session: what happened, with no inner states.
- **The companion's view is a proposal.** Under grant `g-01` (`read`, `suggest`, `infer`; explicit consent; three months),
  the companion proposed `prop-01`: its own observed Episode `ep-02`, an inferred reading `in-02` with grounds, two
  alternatives (one physiological, one informational) and limits, and an inferred preference `c-03`.
- **One reconciliation batch.** At the cadence Mara set (`reviewCadence: P7D`), she decided on all three at once
  (`rv-01`…`rv-03`): she admitted the Episode, partly endorsed the reading in her own words, and declined the
  preference as not true. Nothing was decided by silence.
- **The person's revision wins.** Mara then revised her own reading (`in-03` supersedes `in-01`): she stops when a
  correction cuts into a sentence, more than when she is tired. She marked it `no-quote-back`, so the companion uses
  it as background and never cites it back to her as proof. She also wrote down how she wants to be corrected
  (`c-02`).
- **A renewed grant.** Before `g-01` expired, Mara gave `g-02` in person (`renews: g-01`), narrower: readings now
  only when she has endorsed them, and a review every two weeks. Nothing was extended automatically.

## Try it

From the repository root, with Python 3.9+ and `jsonschema`:

```sh
python3 tools/check.py examples/mara-l1-agent --level L1 --json
python3 tools/ohc_query.py examples/mara-l1-agent project --grant g-01 --purpose learning-support --now 2026-09-13T08:00:00Z --own-proposals
python3 tools/ohc_query.py examples/mara-l1-agent project --grant g-02 --purpose learning-support --now 2026-12-02T08:00:00Z
```

The second command is the companion's proposer view before the review: its three items are labelled `pending`. The
third is what the companion sees under the renewed grant: the partly confirmed reading, Mara's revision with
`obligations.handling` carrying `no-quote-back`, and no declined preference. Under `g-01` the same request is refused
with `expired-grant` from 28 November on: the renewal replaced it when Mara gave it.

[expected-check.json](expected-check.json) is the exact checker output for this file.

## What this example does not establish

That the companion behaves as described at run time, that Mara consented in fact, or that any reading is true. The
file shows the shape of the records; the checker verifies their structure and rules only.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
