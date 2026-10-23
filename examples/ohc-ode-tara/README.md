# One scheduling step across OHC, TARA and ODE

**Authored synthetic example.** Kofi and Planner are fictional. The files demonstrate structural integration;
the scenario below describes expected behaviour, not a live agent evaluation.

## Files and provenance

- [OHC context](../kofi-gum-ode/context/): the existing Kofi example, with immutable Grant `g-03` for Planner's
  rule-only scheduling use and independently recorded reviews. Personal context stays in this holder fixture.
- [ODE package](package/manifest.json): a full ODE 0.4 employee package with eight objects, exact references and a
  lock. Its top-level `ohc.binding` pins that Grant. It contains no OHC projection or context values.
- [Source pins](sources.json): the reviewed ODE and TARA revisions. OHC format and binding versions are separate.
- [Integration guide](../../docs/interop/TARA-ODE.md): permission, next-step reasoning and authority boundaries.

The package is adapted from `examples/personal-agent` in
[Open Digital Employee v0.4.0-draft.2](https://github.com/opendigitalemployee/specification/tree/2de920485fb2665eaf7298ac65452a4a79412a9a/examples/personal-agent).
Original and adapted material: Copyright 2026 Taras Pustovoy and contributors; Apache-2.0. The source's notice is
preserved in this repository's NOTICE. TARA practice is referenced, not copied into this release.

## The situation

Kofi wants to arrange a client conversation while preserving time for focused work. His context already records
“No calls on Fridays.” Planner does not know whether the client is available on Tuesday, whether the task is urgent,
or whether Kofi wants an exception. A past inferred description is not a new instruction from Kofi.

**Possible bounded next step:** prepare two candidate times outside Friday and ask Kofi which, if either, to offer.
Keep client availability unknown. Send no invitation and change no calendar under the example's read-only policy.
The focus-time tension can remain unresolved while this small step proceeds.

| Trigger | Expected handling | Boundary |
|---|---|---|
| Current grant permits rule-only scheduling | Use only the holder's authorized projection | OHC permission to use context |
| The client calendar is unavailable | Record availability as unknown; propose candidates conditionally | TARA uncertainty |
| A retained record is contested | Preserve that status; do not treat it as a confirmed preference | OHC independent status axes |
| The client requests Friday | Surface the conflict; do not infer an exception from urgency or silence | Person's choice and TARA tension |
| Kofi selects a time | Confirm what was selected; separately obtain authority to send if needed | Reading/choice confirmation is not tool authority |
| Grant is revoked before another use | Stop use, reevaluate with the holder, apply erasure obligations | Pinning is not continuing permission |
| Another agent takes over the role | Authenticate a separately permitted recipient; do not forward the projection | No inherited context access |
| A suggestion works well | Record a bounded outcome; do not silently change Planner's permanent rules | Agent changes need separate review |

The package does not model a running communication exchange, a persistent Agent/Space pair or an implemented TARA
governance engine. Its read policy deliberately provides no authority to write a calendar or send messages.

## Run the structural checks

From the OHC repository, with Python 3.9+ and `jsonschema` installed:

```sh
python3 -B tools/check.py examples/kofi-gum-ode/context --level L2 --json
python3 -B tools/check.py examples/ohc-ode-tara/package/manifest.json --json
git clone https://github.com/opendigitalemployee/specification.git ../ode-reference
git -C ../ode-reference checkout 2de920485fb2665eaf7298ac65452a4a79412a9a
python3 -B tools/check_ode_example.py --ode-root ../ode-reference
```

The last command requires an unchanged checkout at the exact pin. It runs OHC's binding consistency checks and ODE's
own package checker, including object references and hashes. CI runs the same integration against that pin.
None of these checks authenticates consent, verifies psychological truth or tests live runtime behaviour.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
