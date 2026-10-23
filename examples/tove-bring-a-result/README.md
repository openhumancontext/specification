# Tove — bringing a test result to her agent

**Authored synthetic example.** Tove is fictional. No real person's data is included. Her report is a one-page
stand-in that says it is one; it carries no publisher text, items, scoring keys or report prose, and her numbers are
invented.

Tove took the BFI-2 in March and keeps the score report. She brings it to her persistent personal agent, so that the
agent starts every session knowing what she allows. Every file in `context/` and `expected/` was written by the
reference holder program, [`tools/ohc_holder.py`](../../tools/ohc_holder.py), as Tove answered in her own window
([`session.json`](session.json) lists her answers). The path is the one in
[INSTRUMENT-IMPORT.md](../../spec/INSTRUMENT-IMPORT.md) §5, at conformance level **L2**, with the modules `lenses`
and `instrument-import`.

## What it demonstrates

- **The holder asks first.** `setup` starts the context from one sentence Tove says (`c-mc2s`, "Give me the decision first,
  in one paragraph.").
- **The numbers come in, nothing is guessed.** Her agent read the score page from a screenshot
  ([`inputs/bfi-2-score-page.txt`](inputs/bfi-2-score-page.txt)); `bring` read the numbers back to her once ("as on
  your report?") and wrote one imported result, `as-nz95` (IMP-1…IMP-5): the scorer is a Party found by its `uri`, the
  record cites her report, and the report itself is in her vault as an `instrument-report` Source (`src-da5a`). The window gives records opaque ids, so a projection that leaves one out shows no gap.
  `bring` also pinned the lens descriptor and its basic playbook in her package.
- **She says what fits.** `review` recorded her stance as a Review by her (`rv-01`, partly endorsed: four scales fit,
  Extraversion does not, in her words; a scale she names neither way stays unsaid), and one sentence for her agent that goes with the result (`c-z7jn`).
- **One screen, everything ticked.** `agree` showed the agreement screen ([`expected/window-3-agree.txt`](expected/window-3-agree.txt)):
  the result and her words ticked, the three things her agent may do ticked, the facts about the test in plain words,
  and the purposes that stay closed whatever she ticks. She confirmed the whole screen: one grant, `g-01`, with a
  `grant-given` Event.
- **What the agent receives.** At session start `serve --for a-01` (her agent's current agreement) built `prj-0001` under `g-01` and printed the agent rendering
  ([`expected/session-start.txt`](expected/session-start.txt)): her words first, then the dated result with her
  stance, how to speak about it, the playbook of the lens by situation under the line saying what her agreement
  allows, and the agreement itself. The holder kept its copy of the projection in `context/projections/`.

## Try it

From the repository root, with Python 3.9+ and `jsonschema`:

```sh
python3 tools/check.py examples/tove-bring-a-result/context --level L2 --json
python3 tools/ohc_holder.py serve examples/tove-bring-a-result/context --for a-01 --purpose assist-personal --now 2026-10-13T07:00:00Z --id prj-0001 --no-log
python3 -B tools/tests/tove_session.py examples/tove-bring-a-result --out "$(mktemp -d)"
```

The second command prints what her agent receives; it equals `expected/session-start.txt`. The third rebuilds the
whole example by running her session again in a scratch directory; the test suite compares the result with these
files byte for byte.

## What it does not show

That her agent behaves as the rendering asks, that Tove consented in fact, or that any result is true of her. The
files show what the reference holder program writes; the checker verifies their structure and rules only.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
