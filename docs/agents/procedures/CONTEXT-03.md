# CONTEXT-03 / 0.2.0 — Read a projection and keep C-1…C-12

**Procedure · 0.2.0 · normative-draft module `governance` · 12 October 2026.** Use what a person shared with you correctly: within the grant, with the right weight for each record, and without inferring what was not shared. A persistent agent also starts every session from the holder's rendering of the projection (§ Session start).

## Use when

You received an `ohc.projection` from a holder, directly, through the MCP tools, or as the rendering printed at the start of your session, and are about to use it for a task.

## Inputs

- The projection, or the holder's rendering of it.
- Your grant id, the purpose of your current task, and your own storage policy.
- The [consumer obligations](../CONSUMER-OBLIGATIONS.md).

## Steps

1. **Check the envelope.** `format` is `ohc.projection`; `specVersion` is one you support (reject unknown versions); `grant` is yours; `purpose` is the purpose of your task; `validUntil` has not passed. Verify `digest` if you store or forward a reference to the projection.
2. **Take on the obligations.** Read `obligations`: the storage limit, `decisionUse` and the handling codes per record. Storage covers everything you keep or derive: notes, summaries, embeddings, memory files, and your runtime's transcripts, logs, caches and indexes (C-1). A record marked `no-quote-back` is background only: never cite it, or the profile it belongs to, to the person as an argument, authority or proof; their words now take precedence. `forwarding`, `crossContextUse` and `delegable` are always false. Set your retention to match.
3. **Weigh each record by its derived label.**
   - `stated` and `confirmed`: usable within the grant.
   - `partly-confirmed`: the parts the person named as fitting (`derived[id].endorsedPart`, PJ-8) count as confirmed; confirm the rest with the person before acting on it.
   - `hypothesis` and `pending`: confirm with the person before acting.
   - `disputed`: do not act on it, except to ask the person.
   - `stale`: not current; follow the record's `onExpiry`.
   - `frame`: meaningful inside the frame the person uses. Speak of it in the frame's terms, and never present it, or anything you infer from it, as an empirical fact or a prediction (C-7).
4. **Decide on results and readings only as the grant says** (R-G14). `obligations.decisionUse` covers AssessmentRecords, Interpretations and inferred records. Under `deny` they inform how you work with the person, and none of them grounds a choice you make or propose for them. Under `approval-required`, a result or reading the person stated or accepted may ground a choice you propose: name what you weighed, and the person confirms each proposal before it takes effect; silence is not confirmation. Carrying out what the person stated (a boundary, a preference, a commitment) is never governed by this term.
5. **Keep statements and readings apart.** `statements` and `interpretations` are separate on purpose. If you show a reading, show its author, lens, limits and alternatives.
6. **Respect what is missing.** `completeness` is always `partial` and `omissions` always `hidden`. An entry in `absences` with `not-disclosed` tells you nothing about whether data exists. Do not probe it, do not ask another agent for it, and do not infer from it.
7. **Use the alias.** Refer to the person by `subjectAlias`. Never try to link it with aliases from other grants or holders.
8. **Stay inside the purpose.** Never use any content for a prohibited purpose or as leverage against the person. A grant is permission to read, not authority to act.
9. **Re-check at use.** Before each later use, check the grant's status and `validUntil` again. After expiry, request a fresh projection.
10. **Report use where asked.** When a projected item informs a decision (for example an ODE Decision), send a `use-report` naming the records used, so the person can see what informed what.
11. **Purge on notice.** On a revocation or erasure notice, delete what you hold by `purgeBy` and answer with `purge-ack`.

## Session start for a persistent agent

When the person set it up with you ([CONTEXT-10](CONTEXT-10.md), step 1), a step in your own settings runs the holder at the start of every session (reference: `ohc_holder.py serve <context> --for <you> --purpose <code> --render agent`, which serves the person's current agreement with you, also after they change it). The holder builds the projection outside your reasoning and prints a rendering of it into the session; nothing is written into your workspace (H-17). A second step prints pending revocation and erasure notices with each prompt; purge and let your runtime acknowledge (C-12). The rendering is a function of the projection, the grant and the pinned lens descriptors and playbooks, in this order:

1. **What the person said: act on these.** Their own sentences, first.
2. **Their results**, each a dated reading by an instrument they brought: the person's stance (fits, parts fit with their words, not sure, disputed), every scale with its value and the descriptor's own description, and what the test can and cannot show, in plain words.
3. **How to speak about them**, per lens: its language guidance, what a helper must never do (`helperMustNot`, I3) and the tools you may offer.
4. **Ways of working**: the playbooks the person uses with each served lens, grouped by situation, under a line that says what the agreement allows (guesses; weighing accepted results). They are guidance, never rules about the person (PB-4). Follow a step only within the grant: skip a step that offers a guess when the grant has no `infer`, and a step that weighs a result when `decisionUse` is `deny`. A step never outweighs what the person says now or the words printed first in the rendering; skip a step they have already answered. A lens with nothing served brings no playbook (PB-5).
5. **Your agreement with the person**: the text you gave the screen, as they confirmed it (`basis.note`); how to file guesses; what you may weigh and what to ask about first; how long to keep notes; and that their results never go into anything others use to decide about them.

The rendering is what the grant serves and nothing more. Use it as you would the projection (steps 2–11).

## Output and completion

The task is done using only what the projection allowed, with each record weighted by its label, readings presented as readings, choices grounded on results or readings only as `decisionUse` allows, nothing probed, and storage and handling kept. Where a use report or a purge acknowledgement was due, it was sent.

Recall is not crisis support. A consumer's crisis protocol always takes precedence; recall MUST NOT delay, replace or condition it.

Do not invent a person; use only what the person said or granted.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
