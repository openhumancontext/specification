# CONTEXT-02 / 0.1.1 — Propose an inference correctly

**Procedure · 0.1.1 · normative-draft modules `core` and `governance` · 9 October 2026.** Write something you concluded about a person, which they did not say themselves, as a proposal they can decide on.

## Use when

You noticed a recurrence, formed a reading of an episode, or want to suggest a statement about the person's preferences, goals or tendencies. Anything you did not hear from the person in their own words, and did not directly observe without generalising, is an inference.

## Inputs

- A grant to you, with computed status `given`, that includes the actions `suggest` (or `write`) **and `infer`**, a purpose that fits your task, and `basis.legal: explicit-consent`.
- The context declares the `governance` module in `conformance.modules`, and lists you as a Party in `parties` (the grant names you as `grantee`).
- The records you reason from, inside that grant's scope.

## Steps

1. **Check the grant now.** It is `given`; your purpose is among its purposes; its actions include `suggest` and `infer`; and the record you are about to write would match its scope, including the naming rules for sensitive and special content. If any check fails, stop and write nothing. You may ask for a grant with a `grant-request` message; the person decides, and silence means refused.
2. **Choose the right kind.**
   - A statement about the person → a Claim. Not facet `disposition`: a tendency you estimate is an AssessmentRecord with `mode: agent-inference`, which stays person-only and carries a validity ceiling.
   - A reading of episodes, spans or claims → an Interpretation.
   - A recurrence across two or more episodes → a Pattern (experimental).
   - A set of readings from one model → a ModelView.
   - Never a Part: only the person names their parts.
   - Never a mood, emotion, stress or affect value derived from voice, face, physiology, keystrokes or screen behaviour.
3. **Write the record honestly.** `origin: "inferred"`; `assertedBy`: your Party id; `underGrant` and `purpose`; `epistemic: "hypothesis"`. A reading written by an agent is never `declared`, even when you set `epistemic: "hypothesis"` (I10): `declared` means the asserter's own statement about themselves, and you are not the person. If you give a confidence, use `semantics: "support-score"` unless you have a calibration reference for a probability. Use an opaque id.
4. **Show your work** (Interpretations, Patterns and ModelViews):
   - at least one ground, citing spans or records;
   - at least two alternatives, at least one of them not psychological (situational, physiological, informational or external);
   - the limits of the reading;
   - counter-evidence you know of;
   - `causal` at most `hypothesized`: a sequence never proves a cause.
5. **Through a lens, only with an adoption.** Cite the LensAdoption. It must be active, allow agent interpretation, and list you among its interpretation authors. If it says `ask-first`, ask the person before writing. Never apply distortion labels, diagnoses or clinical terms unless the person adopted the lens and supplied the label themselves.
6. **Leave third parties alone.** Never describe another person's inner states, traits, health or beliefs.
7. **Propose.** Send a `proposal` message (or store a Proposal with its items) with a `rationale` the person will read, your grounds, and an expiry (default thirty days).
8. **Wait for the person.** Silence is not acceptance: undecided items expire as declined, meaning "not admitted by the person". Read the `proposal-result`, or ask for your proposer view (`ownProposals: true`) to see your own pending and expired items. If you work with this person over time, keep your model reconcilable with theirs: [CONTEXT-09](CONTEXT-09.md). Do not re-propose a rejected or declined item without new grounds. A contested item stays open for discussion; do not act on it except to ask.

## Output and completion

Either a stored Proposal whose items are `proposed` and carry grounds, alternatives and limits, or a correct refusal (`infer-not-granted` or `not-granted`) with nothing stored. The person's decision, not yours, completes the procedure.

Do not invent a person; use only what the person said or granted.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
