# CONTEXT-09 / 0.1.1 — Keep your model of your person

**Procedure · 0.1.1 · normative-draft modules `core` and `governance` · 12 October 2026.** For a persistent agent that works with one person over months: keep what you think about the person reconcilable with what the person thinks, so that your model never quietly becomes a verdict about them.

## Use when

You work with the same person over time, you form readings of what happens, and you want them to stay usable without drifting away from the person's own view. This applies whether or not you also hold the person's context ([§15.9](../../../spec/SPECIFICATION.md#159-an-agent-acting-as-holder)).

## Inputs

- A grant to your Party with `read`, `suggest` and `infer`, a purpose that fits your work, `basis.legal: explicit-consent` and an expiry (at most 180 days with `infer`).
- Optionally, the grant's `reviewCadence`: how often the person wants to go through your open proposals together, for example `P7D`. Without one, the person goes through your proposals in their window when they choose.
- The procedures [CONTEXT-02](CONTEXT-02.md) (propose an inference) and [CONTEXT-03](CONTEXT-03.md) (read a projection).

## Steps

1. **Keep two roles apart.** When the person dictates and confirms, inside a session they started, you write as their instrument: `assertedBy: "subject"`, in their words ([CONTEXT-01](CONTEXT-01.md)). Everything you notice or conclude yourself is yours: an observer account, an `observed` Episode or an `inferred` Interpretation, written under your grant and proposed ([CONTEXT-02](CONTEXT-02.md)).
2. **Record what you saw separately from what you think it means.** What happened goes into an observer account (`accountKind: observer-account`, narrated by your Party), without inner states. Your reading goes into an Interpretation that points at the Episode, with grounds, at least two alternatives (one of them not psychological) and limits.
3. **Look at your own proposals.** Request your proposer view (`ownProposals: true`). Your pending items are labelled `pending`; items that expired undecided are `not-accepted`, which means "not admitted by the person", not "wrong" and not "gone". Do not act on either as if it were the person's view (C-3), and do not re-propose without new grounds (C-2).
4. **Reconcile in batches, at the person's cadence.** Guesses you offer from results the person brought ([CONTEXT-10](CONTEXT-10.md)) are proposals like any other, filed in their window. At the `reviewCadence` the person set, or when they open their window, offer the open proposals together, grouped, with their alternatives (IB-1). The person decides with Reviews: admit, endorse, partially endorse in their own words, contest, decline. One Review may cover several items. Counted against the inbox limit (IB-4); never press for a decision, and silence stays "not admitted".
5. **Let the person's revision win.** When the person revises their own reading (a superseding Interpretation), use theirs. If they mark it `no-quote-back`, never cite it, or your model, back to them as proof; their words in the present conversation take precedence.
6. **Renew in person, before expiry.** A grant with `infer` expires within 180 days. Before it does, ask the person to renew it in their window, through the holder; the person gives a new grant (`renews` names the old one), possibly narrower. Nothing is extended automatically, and an expired grant means you stop reading and proposing. Treat the renewal as a reconciliation step: show the person what you proposed under the old grant and what they decided.
7. **Check** with `python3 tools/check.py`.

## Never

- Write your own reading as the person's statement, or as `declared`.
- Keep a private "real" model that the person cannot see, decide on or erase.
- Treat an expired or declined proposal as accepted, or as a fact about the person.
- Extend your own grant, or read "the person agreed earlier" as a renewal.

## Output and completion

A context in which your observations and readings are separate, attributed records; the person's decisions on them are Reviews made at their cadence; and your grant is current because the person renewed it. See [Mara's example](../../../examples/mara-l1-agent/) for a study companion doing this.

Do not invent a person; use only what the person said or granted.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
