# OHC, TARA and ODE: three distinct decisions

OHC represents a person's shared context and the permissions for using it. TARA helps participants choose a bounded
next step while keeping unknowns, disagreements and revision visible. ODE describes an agent's working configuration,
roles, communication and authority. None of these layers grants the permissions belonging to another.

| Question | Primary layer | What it does not establish |
|---|---|---|
| What context may this particular agent use, for this purpose, now? | OHC Grant and holder evaluation | Authority to act or endorsement of every claim |
| What do we know, what is disputed, and which limited step is acceptable? | TARA practice | Consent to read private context or automatic agreement |
| Which agent configuration may perform that step, with what authority? | ODE policies and runtime | Permission to access a person's OHC context |

## Start with one agent and one bounded task

1. Teach the agent the [TARA starter practice](https://github.com/opentara/tara-protocol/tree/f8fa6fff5e931a8bab00a9ab527f34277f636187). Keep evidence, interpretation and unknowns separate; identify affected parties and unresolved tensions; propose a limited step and a review trigger.
2. Start with a synthetic context. Choose one purpose and a narrow OHC Grant. Use [CONTEXT-07](../agents/procedures/CONTEXT-07.md) to reference it from an ODE package.
3. Check the OHC context, the binding and the ODE package separately. Passing these checks verifies files, not an agent's behaviour or a person's consent.
4. At use, the holder authenticates the exact grantee and reevaluates the current permission. A stale grant pin, a revoked grant or changed circumstances must never be bypassed with a cached projection.
5. Make the next step explicit. Ask for the appropriate confirmation or scoped authority before changing calendars, contacting others or revising the agent's configuration. Record the outcome without turning success into permission for future steps.

The [combined example](../../examples/ohc-ode-tara/README.md) supplies a complete ODE package, an existing synthetic
OHC context and a worked TARA decision. It requires no real personal data.

## Changes to the agent do not renew consent

ODE separates the persistent Agent from a DigitalEmployee working configuration, an addressable Identity and an
Assignment to a role. A role successor, another configuration or another agent in the same Space does not inherit
OHC access. The holder must resolve the exact authorized local grantee; where that relationship or permitted purpose
changes, establish a new Grant. Never infer identity from a display name or shared address.

Self-improvement needs the same separation. An apparently useful interpretation is still an interpretation. A
successful action does not endorse a psychological claim, permit new purposes or authorize permanent policy changes.
Preserve review and rollback boundaries around changes to memory, tools, roles and policies.

## Preserve disagreement and keep private evidence private

An admitted record can remain a hypothesis, unendorsed or contested. OHC admission `active` is not ODE `agreed`.
A Tension can remain `held-as-is` while a limited action proceeds. Missing confidence is not zero and must not be
invented to satisfy another schema.

Portable ODE packages reference Grants; they do not carry Claims, projections or private projection identifiers and
digests. Use the holder's restricted `use-report` channel for evidence of use. A shared Space, reusable skill or
another agent's memory is not a permitted onward destination. Required erasure also applies to derived explanations;
retain only permissible incident metadata and do not rewrite the history of an unauthorized attempt.

## Versions and scope

This guide accompanies OHC release `0.1.0-draft.3`, format `0.1.0-draft`, ODE binding revision `0.2.0`, and ODE
`v0.4.0-draft.2` at `2de920485fb2665eaf7298ac65452a4a79412a9a`. TARA is a separate conceptual draft at
`f8fa6fff5e931a8bab00a9ab527f34277f636187`; its practice is linked, not bundled or relicensed here.
No cross-standard runtime certification or legal assurance is implied.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
