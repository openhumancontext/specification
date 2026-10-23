# CONTEXT-08 / 0.3.0 — Suggest or adopt a lens

**Procedure · 0.3.0 · normative-draft module `lenses`; catalog entries experimental · 12 October 2026.** Record a person's relation to a framework of description: one they chose, one an agent suggested, or one they bring from therapy, coaching or another practice. Lens descriptors, playbooks and the lens rules are in [LENSES.md](../../../spec/LENSES.md). A lens carries facts and guidance; what you may suggest, read through or weigh is the person's agreement with you (their grant), narrowed by their adoption and handling codes.

## Use when

The person asks for ways of looking at their experience, or tells you they work with a lens, or brings one from their practice.

## Inputs

- The lens descriptor, pinned by id and version, or, for a framework that is not in the catalog, the person's or practitioner's own description of it.
- The person's request, in their words.
- For a suggestion by you: a grant with `suggest` whose scope names the lens; to read through the lens yourself, also `infer` (INF-1, I5).

## Steps

1. **Read the descriptor first.** Its mental model, what it supports and does not establish, its evidence tiers and grades, its intellectual-property notes, what a helper must not do, and its playbooks (§2.2 of LENSES.md). These are facts and guidance; show them to the person in plain words.
2. **Follow the route.**
   - **Suggested by an agent.** Suggest a lens only under a grant that lets you (`suggest`, with a selector naming the lens). `adoption.suggestionRequires` describes when a suggestion usually makes sense, for example after the person asked for ways of looking. Present the lens with its limits and evidence grades, as one option. If the person wants it, write a LensAdoption with `route: agent-suggested` and `suggestedBy` set to you; it stays proposed until the person admits it (LA-1). You never activate it yourself.
   - **Chosen by the person.** Write a LensAdoption with `route: self-chosen` and `assertedBy: "subject"`.
   - **Not in the catalog** (for example, inherited from therapy or coaching, or a practitioner's own model). Write a local descriptor with the person, in their or the practitioner's words: an id with an `x-` namespace (`urn:ohc:lens:x-<namespace>:<name>`), `descriptorStatus: stub`, `kind: author-framework`, a `summary`, and a `mentalModel` with `summary`, `attendsTo`, `agentPosture` and `helperMustNot` ([LENSES.md §5.1](../../../spec/LENSES.md#51-local-lenses)). Store it as `lenses/<name>@<version>.lens.json` in a package, or inline as the pin's `descriptor` in a single document. Its results are `frame-relative` (LA-6); whether you suggest it or read through it is the person's agreement, as for any lens. Without any descriptor the checker warns (W-LA6) and treats the lens the same way. Then continue with the route below that applies.
   - **Inherited from practice.** Add the `practice` block: the practitioner's role, the practitioner as a Party, whether the relationship is active, since when, and a `releaseRef` when session material is stored. Choose `confidentiality` (`practitioner-scope` or `therapy-confidential`). The adoption gives the practitioner **no access**; access would need its own grant, which 0.1 does not provide for practitioners. Leave `onEnd` at `ask` unless the person decides otherwise. The practitioner's way of using the lens can come in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`), written with the person and kept in the context like a local descriptor.
3. **Set the uses and the interpretation policy with the person.** `uses` lists what the lens may be used for (speaking in its terms, offering its practices, storing results, interpreting, recall). `interpretationAuthors` defaults to the person alone. `agentInterpretation`, when absent, counts as `off`. When the person activates an adoption of a lens that a grant already lets an agent read through, ask them for `agentInterpretation` and show what each value does: `off` stops every agent reading through the lens, whatever the grant says; `ask-first` means you ask each time before writing a reading (at L2 the holder records the yes as an Event `ask-first`); `allowed` leaves it to the grant (I5). Show it with `allowed` pre-selected; the person changes it. An absent member stays `off`: absence is not consent. Choosing ways of working (step 4) does not change it.
4. **Choose the ways of working.** The adoption's `playbooks` lists the playbooks the person uses with the lens: absent means the descriptor's own; `[]` means none; otherwise the person's choice among the descriptor's list, other registry playbooks for the lens and local playbooks pinned in the context (PB-3). Pin each playbook the context uses in `Context.playbooks`. The reference holder asks the person in their window (`ohc_holder.py playbooks <context> <lens id>`).
5. **Pin the descriptor** in `Context.lenses` (id, version and, for a file in `lenses/`, its `sha256`).
6. **Check** with `python3 tools/check.py`.

## Never

- Suggest a lens, or read through one, beyond what the person's grant and adoption allow.
- Present a result of a symbolic or non-empirical frame, or anything inferred from one, as an empirical fact or a prediction (C-7).
- Convert one person's result from one lens into another, except as a person-only cross-lens estimate through a single published mapping; never chain mappings, and never give a generic result a branded label.
- Do what the descriptor's `helperMustNot` list forbids, or present yourself as providing therapy.
- Let a lens result ground a choice for the person beyond the grant's `decisionUse` (R-G14), or use it for any prohibited purpose (§8.10 of the specification).

## Output and completion

A LensAdoption with the right route, uses, interpretation settings and playbooks, admitted by the person, and a pinned descriptor. Adopting a lens does not establish that the lens is valid for the person; outcomes of using it are recorded separately.

Do not invent a person; use only what the person said or granted.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
