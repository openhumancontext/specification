# Status and scope

**Public draft 0.1.0-draft.3 · format 0.1.0-draft.** Published in [openhumancontext/specification](https://github.com/openhumancontext/specification).

Open Human Context describes the context a person shares with agents and the permissions under which it may be read. It is not a runtime, a hosted service, a registry service, a certification programme or a guarantee of any behaviour.

## Maturity per module

| Module | Maturity in 0.1 |
|---|---|
| `core` (Context, Subject, Party, Claim, Relation, Source, Episode, Interpretation, Tension, Review, Proposal, Tombstone; status axes, time, disclosure) | normative-draft |
| `governance` (Grant, Event, Projection, ContextLock; evaluation, step-up, erasure, obligations) | normative-draft (required at L2) |
| `lenses` (registry shapes and rules; LensAdoption, AssessmentRecord, ModelView; playbooks) | normative-draft; **every catalog entry, playbooks included, is experimental** |
| `instrument-import` (the instrument `import` block, imported results, the agreement screen) | normative-draft |
| `practices` (Practice, Outcome) | normative-draft |
| `patterns` (Pattern) | experimental |
| `recall` (RecallCue) | experimental |
| `inner-system` (Part) | experimental |
| `health-ref` (HealthRef) | experimental |
| `exchange` (16 messages) | experimental |
| `binding.gum` | normative-draft, for anyone claiming GUM compatibility |
| `binding.ode` | normative-draft, for anyone claiming ODE binding |
| `binding.mcp` | experimental |
| crosswalks (JSON-LD, PROV-O, DPV, ODRL and others) | informative |

"Normative-draft" text may still change before 1.0. No conformance claim may rely on experimental material. A context must stay valid with its experimental records removed.

## What is tested

The JSON Schemas, the reference checker, the five context examples, the converters (GUM and assessment import), the reference holder program (run through a pseudo-terminal, as a person would), the static viewer and the release manifest are checked automatically by the local check sequence (`tools/check_all.py`). These checks cover file structure, schema validity, references, hashes, the event chain, projection reproducibility and the rules listed in the specification's rules index.

The additional [OHC–TARA–ODE example](examples/ohc-ode-tara/README.md) is checked with the pinned ODE 0.4 package
checker and OHC's binding checker (`tools/check_ode_example.py --ode-root CHECKOUT`). CI runs both. Its TARA decision
scenario is explanatory; it is not an executed agent evaluation.

## What is not tested

- Live runtime behaviour.
- Any holder or agent implementation.
- Consent authentication: the checker cannot tell whether a person really gave a grant.
- Truth of content: schema validity is not truth.
- **What the reference holder program does not do yet.** It does not take an agent's guesses as proposals for the person to keep or drop in the window (the standard's mechanism: Proposal and the person's Review, CONTEXT-02); in this release the agent says each guess as a guess and keeps only what the person kept. Its window refuses without a terminal but is not a lock against an agent with a terminal of its own, and a folder private to the person's user account is still readable by an agent running as that user.

The checker reports these limits in its own output (`truthVerified`, `consentVerified`, `consentAuthenticated`, `endorsementAuthenticated`, `behaviorTested` and `runtimeTested` are always `false`).

## Scope limits

Contexts about children, or about adults whose decisions are made by a guardian, are non-conforming in 0.1 (R-C4), and deployments with minors are out of scope: a context that declares a level attests that its subject is an adult (`conformance.subjectIsAdult`). Shared contexts for couples, families or groups are not modelled in 0.1. Practitioner access (therapists, coaches) is not part of 0.1; a lens adoption inherited from a practice never gives the practitioner access.

Recall is experimental. Per-episode recall defaults to `not-permitted`, and recall is not therapy and not crisis support.

## Legal

- No legal review has been performed.
- GDPR and EU AI Act hooks are documented in [COMPOSITION.md](spec/COMPOSITION.md) as design intent, not advice.
- Russian Federal Law No. 152-FZ has not been analysed.
- Lens IP entries carry `legalReviewNeeded: true`.
- **Consent on the agreement screen.** Between a person and their own agent the screen opens with everything ticked, and confirming the whole screen in the person's own window is recorded as their explicit consent (maintainer's decision for this draft; [INSTRUMENT-IMPORT.md](spec/INSTRUMENT-IMPORT.md) §5). Whether this design satisfies applicable consent requirements remains an open legal-review question. The recorded agreement is not a claim of legal compliance.

- **Prohibited purposes without a named legal basis.** `advertising`, `credit-or-insurance-decision`, `model-training` and `sale-or-transfer` are closed by OHC's own choice; several others are held stricter than the law ([COMPOSITION.md](spec/COMPOSITION.md#legal-hooks)). The legal review names a basis or confirms the choice.

The maintainer authorized publication as a draft on 2026-10-23, with legal review still outstanding. Publication
does not resolve these questions, certify implementations or establish readiness for handling real personal data.

## Wording, naming and examples

- The EN tagline is provisional wording; the RU tagline is the original. The single canonical EN wording is the `tagline` entry of the [glossary](spec/glossary.json); every English page reuses it unchanged.
- The maintainer selected **Open Human Context** and the `openhumancontext/specification` repository for this public draft. The `urn:ohc:` namespace remains provisional. This project claims no affiliation with similarly named projects and no trademark clearance.
- Examples are synthetic; no real person's data is included.

## Open questions for 0.2

- **Typed operator relation.** When a grantee's operator is the person's employer or school, consent is presumed not to be freely given. 0.1 gives informative guidance only (narrow grants, an independent holder; SPECIFICATION §12.4); 0.2 may type the operator relation and constrain grants by it.
- **An agent's model of its person.** 0.1 defines the proposer view (§12.5), batch reconciliation at the person's cadence (`reviewCadence`) and grant renewal (`renews`), and the separation of roles when an agent is the holder (§15.9, H-17). Whether a persistent agent needs a dedicated, person-visible "model" record, and how an agent's estimates travel to another agent the person chooses, is open.
- **Handling propagated from lenses.** `no-quote-back` is set per record. Whether a lens descriptor or a LensAdoption should propagate it to every record made through that lens is open.
- **Repository history.** The working repository's history is not published. Only the tree exported by `tools/build_release_manifest.py --export` is ever pushed (see [CONTRIBUTING](CONTRIBUTING.md)); rewriting the private history is a separate decision.

## Relationship to Open Digital Employee

**Proposed** governance statement, pending the maintainer's decision: "ODE's 'Person profile' and 'Personal space' proposed extensions are realised by OHC. ODE keeps `Party` as the in-package anchor and references the person's OHC grants; projections are fetched under them at run time."

ODE binding revision `0.2.0` targets ODE `v0.4.0-draft.2`: no ODE schema change is needed ([bindings/ODE.md](spec/bindings/ODE.md)). Proposals for closer integration are informative and have not been filed. Current and historical crosswalks are distinguished by their exact source pins.

## Licensing

The maintainer confirmed the licence map on 2026-10-23: Apache-2.0 for the normative specification, schemas, examples and tools; CC BY 4.0 for explanatory documentation and the glossary. Copyright: **Taras Pustovoy and contributors**. See [license scope](LICENSING.md). The release manifest records the licence of every file and the checks actually performed.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
