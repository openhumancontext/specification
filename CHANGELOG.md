# Change history

## 0.1.0-draft.3 — 2026-10-23

First public draft in `openhumancontext/specification`. The maintainer approved publication and the existing
Apache-2.0 / CC BY 4.0 license map. The public repository begins from a clean export, without the working history.

- ODE binding revision **0.2.0** targets `v0.4.0-draft.2` at `2de920485fb2665eaf7298ac65452a4a79412a9a`.
  Eleven current crosswalks accompany the eleven historical ODE 0.2 comparisons.
- The checker accepts a full ODE manifest and verifies the binding's Grant identity, version, standard declaration
  and required extension. Conflicting or duplicate Grant references now fail. Standalone extension validation
  explicitly warns that package consistency was not checked.
- Admission is no longer mapped to ODE definition status: an active OHC record can remain hypothetical or contested.
  The admission catalog is **0.2.0**. Preserve endorsement, epistemic status, contested and freshness independently.
- Clarified the exact recipient boundary across ODE Agent, DigitalEmployee, Identity and Assignment; access is not
  inherited through a role or Space. Private runtime evidence stays outside portable packages and shared memory.
- Added a complete synthetic ODE package, a worked TARA next-step scenario, an integration guide and a check against
  ODE's own pinned package validator. **CONTEXT-07 is 0.3.0.**

**Compatibility:** OHC's context serialization remains `0.1.0-draft`; draft.2 context files need no migration.
Binding behavior and crosswalk semantics changed in the separately versioned binding and catalog. Consumers relying
on `active → agreed` must remove that conversion. Inconsistent binding fragments previously accepted by shape alone
are now rejected. No live runtime, consent authentication or legal review is claimed.

## 0.1.0-draft.2 — 2026-10-12

Second draft, format `0.1.0-draft` unchanged. Local repository only; not published. **No compatibility with
draft.1:** every context, recipe, descriptor and fixture in the repository was upgraded in the same pass, and a draft.1
validator rejects draft.2 documents, and the reverse.

**In short.** A person can bring a test result from the report they hold, in five steps, through their own window.
What an agent may see, guess, weigh and remember is decided only by the person's agreement; between a person and their
own agent everything starts ticked, and only the limits that protect the person from others' decisions stay closed.
Lenses carry facts and ways of working by situation (playbooks), never permissions. Not compatible with draft.1.

**Why.** The maintainer's words, translated, are the reasons for this release:

- *"I have my [test] results in hand: how do I bring them in so that my agent sees me? And it has to be a proper part
  of the standard, at the right level."* A person can now bring a test result from the report they hold, through their
  own window, in an opt-in module rather than in the core.
- *"How the agent decides about the person, and on what basis, is a matter of the format of their agreements."* A
  lens carries facts and guidance; what an agent may see, suggest, infer, remember or weigh is the person's grant.
- *"Everything ticked; you untick what you don't need"* and *"make it as convenient for the person as possible, so they
  just take it and go; we don't protect them from themselves."* Between a person and their own agent the agreement
  screen opens with everything ticked. Only the limits that protect the person from decisions of others stay closed
  for every grantee; most rest on law, and COMPOSITION.md marks the few that OHC holds stricter or without a named
  basis yet.
- *"Lenses can come with recommendations and frameworks: how to use them, and in which situations."* Playbooks.
- *"Disclose: which inferences, what for, how they will be used."* An agent that asks to offer guesses says so on the
  screen; a request in the procedure, not a rule.
- *"Don't overcomplicate. Where did this come from? From which requirement, which condition?"* Members that carried
  permissions without a basis were removed, not kept as deprecated.

**Specification.**

- **New module `instrument-import`** ([INSTRUMENT-IMPORT.md](spec/INSTRUMENT-IMPORT.md), normative-draft, requires
  `lenses`): the instrument `import` block (INS-1); imported results (IMP-1…IMP-5, warnings W-IMP2 and W-IMP6): the
  scorer is a Party found by its `urn:ohc:scorer:` URI, the result stays proposed until the person decides, the report
  is a Source of kind `instrument-report` in the person's own vault, and the result's freshness runs from the day the
  test was taken; agent rules IMA-1 (only the person's own result, handed over by them) and IMA-2 (blank stays blank);
  the holder's agreement screen (IMH-1). `bfi-2` 0.2.0 carries the first `import` block.
- **Decisions on results and readings (R-G14).** Grant `constraints.decisionUse`: `deny` (the default) or
  `approval-required`, for AssessmentRecords, Interpretations and inferred records. Under `approval-required` a result
  or reading the person stated or accepted may ground a choice the agent proposes, naming what it weighed, with the
  person's yes to each proposal. It replaces `automatedDecisionUse`. `obligations.decisionUse` is always present in a
  projection. No grant opens a prohibited purpose (§8.10), for any grantee, the person's own agent included.
- **The person's words on a partly endorsed result (PJ-8).** A projection's `derived` entry carries `endorsedPart`;
  the scales the person named as fitting count as confirmed, and a scale they named neither way is not decided. In `summary` mode an AssessmentRecord also drops `source`.
- **Playbooks** (`format: ohc.playbook`, LENSES.md §2.2, PB-1…PB-5, W-PB5): ways of using a lens, and the person's
  accepted results in it, by situation: when, two to five steps, the lens's tools, the results drawn on, what to
  watch for. Guidance, never permission and never a rule about the person. A descriptor lists its playbooks, a
  LensAdoption names the ones the person uses, local playbooks from a practice live in the person's context like
  local lenses, and a holder's session-start rendering carries the playbooks of the served lenses.
- **Narrowed:** LN-3 (a symbolic frame only forbids cross-lens mapping), AR-4 and principle 8 (frame results, and
  what is inferred from them, stay frame-relative and are never presented as empirical facts), LA-6 (a stub's
  results are frame-relative), AR-2 (an agent estimate keeps its signature; the lens condition goes), LA-1 (an
  agent-suggested adoption is proposed and activated by the subject only), GR-2. **Widened:** C-7 (special-category
  content may be derived under an `infer` grant naming the category or the lens; never political views), I5 (an
  agent reads through a lens under an `infer` grant naming it; the person's adoption can stop it). **Amended:** C-1
  (storage covers the runtime's transcripts, logs, caches and indexes); R-X3 (a self-report result the person took,
  emotion scales included, counts as declared; R-X4 unchanged).
- **Retired:** LN-2, LN-10, LN-12, LA-7. **Removed members:** the lens `useLimits` members `decisionUse`,
  `inferenceInput`, `agentInference`, `speakInFrame` and `prohibitedPurposes` (only `crossLensMapping` stays),
  `adoption.agentSuggestion`, AssessmentRecord `useLimits`, Grant `automatedDecisionUse`.
- **Prohibited purposes (§8.10)** say plainly that they are others' decisions about the person: hiring, evaluation,
  promotion, credit or insurance by an organisation or another person. The person's own choices with their own agent,
  such as which role to take, are not among them.
- Record ids carry no sequence a grantee could read gaps in (Annex B); IMH-1 also shows, word for word, the text the
  grant stores as the agent's disclosure.
- Catalogs `modules` 0.2.0, `type-catalog` 0.2.0 (the `Playbook` kind) and the text of `prohibited-purposes`, `labels`, `epistemic`, `adoption` and
  `lens-descriptor`; the ODE binding's `prohibitedPurposes` no longer adds lens limits.

**Lenses.** The 16 descriptors are version 0.2.0 (pins move): the permission members are gone, items of
`helperMustNot` and `agentPosture` that decided use are removed or rewritten as facts ("present a score as evidence of
fit for a job or role"), and each lists one basic playbook written by the OHC editors from its own mental model and
toolkit. Astrology and Human Design describe all four adoption routes (routes describe, never restrict) and no longer
say "speak in the frame only after the person adopted it". The Big Five constructs carry plain descriptions. The lens tables in LENSES.md and the viewer show facts and playbooks only.

**Tools.** `tools/ohc_holder.py` (new): a reference holder that plays the person's window in the terminal (`setup`,
`bring`, `retake`, `review`, `words`, `correct`, `agree`, `preview`, `withdraw`, `erase`, `playbooks`, `serve`,
`notices`, `template`); every deciding command talks only to a terminal and refuses without one (not a lock: an agent
with a terminal of its own could type into it, which its procedure forbids); `setup` makes a private folder and the
holder key; `serve --for <agent>` prints the session-start rendering of the agent's current agreement, so the step
survives a change of mind; the preview shows that same text; the window issues opaque record ids; "parts fit" asks
which scales fit and which do not; `withdraw` opens the new screen with the earlier ticks and the agent's own words;
`--seed` makes ids, Event salts and projection nonces reproducible for synthetic contexts only; `serve --keep` keeps
the holder's copy of the projection. `import_assessment.py` writes
imported results and no longer writes use limits, refuses fields outside its accepted list, and writes valid
standardized scores. The checker registers the new rules and retires the old ones.

**Examples.** Tove (new, L2): a BFI-2 result brought through her window, partly endorsed in her words (four scales
fit, Extraversion does not), one grant with
everything ticked, and the text her agent receives at session start; every file was written by running the holder.
Noa, Kofi, Mara and all 22 recipe contexts were upgraded: no `automatedDecisionUse` and no record `useLimits`, lens
pins at 0.2.0, projections and locks recomputed (`decisionUse: "deny"`).

**Documentation.** A guide for the person, [Bring a test result to your agent](docs/guides/BRING-A-RESULT.md) (EN and
RU, five steps); procedures CONTEXT-10 0.1.0 (new: help a person bring a test result), CONTEXT-03 0.2.0 (`decisionUse`,
frame labels, session start from the holder's rendering, playbooks), CONTEXT-07 0.2.1, CONTEXT-08 0.3.0 (suggesting
and reading through a lens follow the person's agreement; choosing playbooks), CONTEXT-09 0.1.1; the 32 lens recipes
follow the new rules and name each lens's playbook; consumer obligations with R-G14.

**What did not change.** The data model's kinds, the status axes and labels, the conformance levels, grant
evaluation, step-up, erasure and the Event chain, recall, the GUM and MCP bindings, and the list of prohibited
purposes (their definitions are reworded, above).

**Open before publication.** Legal review, which now includes whether confirming a screen with every row pre-ticked is
explicit consent for special-category data, and a legal basis for the prohibited purposes that have none named yet
(see [STATUS.md](STATUS.md)); the naming decision.

## 0.1.0-draft.1 — 2026-10-09

First draft of Open Human Context, format `0.1.0-draft`. Local repository only; not published.

- **Specification.** A normative-draft data model of 28 kinds in ten layers, kept in one JSON file (L0) or a package (L2). Records are immutable; every status change is a Review, and endorsement, admission and freshness are computed. Six status axes (origin, endorsement, epistemic status, admission, freshness, disclosure) with derived display labels. Three conformance levels: L0 Minimal (a claim or an episode), L1 Grounded, L2 Governed; a declared level attests an adult subject.
- **Experience first.** Sources in a content-addressed vault, Episodes with several dated accounts, and Interpretations as separate attributed records with `heldDuring`, so that "how did I understand this then?" is a query.
- **Governance.** Default-deny Grants with a separate `infer` action, mandatory expiry, projections that keep statements apart from interpretations and never act as existence oracles, a salted Event chain that survives erasure, step-up for verbatim access, erasure notices to every recipient of a disclosure, a proposer view, the separation of roles when an agent is the holder, and consumer and holder obligations C-1…C-12 and H-1…H-17.
- **Lenses.** A lens descriptor shape with a mental model, a toolkit and representations; three adoption routes (chosen, suggested, inherited from practice); a 16-entry experimental catalog; instrument entries; population-level mappings that are never identities.
- **Practices and outcomes** as normative-draft records; **patterns, recall cues, parts and health pointers** as experimental modules.
- **Exchange and bindings.** Sixteen experimental exchange messages; GUM import and export with affect refusal (R-X4) and quarantine (R-X3), and a tested round trip of admitted propositions; an ODE Tier 0 binding that pins the person's grant, never a projection; an MCP tool surface; informative crosswalks.
- **Examples, tools and documentation.** Four synthetic people (Ilse, Mara, Noa, Kofi); a read-only reference checker, converters, a temporal query tool and a static viewer; an EN/RU overview and glossary; agent procedures CONTEXT-01…CONTEXT-09; a release manifest and an exported release tree.

**Revised after review, before publication.**

- Rules made checkable: allowed references (RF-1), agent readings are inferences (I10), Tombstone fields (TB-5), disclosure Events covered by grants (EV-7), step-up actors and coverage (EV-5), no vault object after erasure (V-6), grant actions (GR-9), lens interpretation limits (LA-7, W-LA6), intentional absences (CL-9), affect independent of facet and label (CL-4, W-CL4), adult attestation (R-C4); every checker identifier is defined (Annex A.2, SELF-4), and every finding carries its rule's sentence and where it is defined.
- Handling code `no-quote-back`; Source default tier per source kind; an erasure cascade for Reviews and Proposals; deny grants without a duration cap; holder declines with reason codes; summary-mode fields per kind; a single canonical provisional English tagline (glossary `tagline`).
- Local lens descriptors and a fail-closed stub for lenses without a descriptor; a per-lens "how it works with a person" section in LENSES.md; corrected mark records and citations.

What did not change: n/a — first release.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
