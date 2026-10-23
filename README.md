# Open Human Context

*A person changes. Their goals conflict. Their memory is selective. Their understanding of themselves is revised. Sometimes they lose access to their own ways of coping with what is happening.*

Russian original: «Человек сам меняется. Его цели противоречивы. Его память избирательна. Его представления о себе пересматриваются. Иногда он теряет доступ к собственным способам справляться с происходящим.» The English wording is provisional, and this is its single canonical form (glossary entry `tagline`); see [STATUS](STATUS.md).

1. **Preserve experience. Evolve interpretations.** This principle governs OHC's data architecture.
2. **Help humans remember what they know when they need it most.** This principle describes what agents can build on OHC. The behaviour itself is outside the standard.

OHC records representations and permissions; it does not establish who a person is, decide for them, or provide psychological or medical help.

<!-- project-badges:start -->
[![documentation: read](.github/badges/documentation.svg)](spec/SPECIFICATION.md)
[![overview: read](.github/badges/overview.svg)](docs/OVERVIEW.md)
[![format: 0.1.0-draft](.github/badges/format.svg)](STATUS.md)
[![checks](https://github.com/openhumancontext/specification/actions/workflows/check.yml/badge.svg)](https://github.com/openhumancontext/specification/actions/workflows/check.yml)
[![spec license: Apache-2.0](.github/badges/spec-license.svg)](LICENSE)
[![docs license: CC BY 4.0](.github/badges/docs-license.svg)](LICENSE-DOCS)
<!-- project-badges:end -->

**Public draft 0.1.0-draft.3 · format 0.1.0-draft.** Published in [openhumancontext/specification](https://github.com/openhumancontext/specification). The normative specification, schemas, examples and reference tools use Apache-2.0; explanatory documentation and the glossary use CC BY 4.0. See [license scope](LICENSING.md) and [maturity and limits](STATUS.md).

OHC develops as a standalone standard in the **Open Human Context** organization, with room for independent tools for
describing, reviewing and sharing human context. [TARA Institute](https://opentara.org/) supports its development
alongside TARA Protocol and Open Digital Employee. Each standard keeps its own repository and versioning.

## What OHC is

**Open Human Context (OHC)** is an open, file-based format for the context a person shares with the agents and services that work with them. It does not describe who a person "really is". Instead, it keeps **records about a person, each with its origin**:

- the primary sources they rest on;
- the experiences those sources tell of;
- how those experiences were understood at the time and later;
- what is stated about the person now;
- the frameworks of description through which anything was read;
- the ways of coping that were tried, and whether they helped;
- the permissions under which any of it may be used.

The person holds the context or chooses who holds it. Agents receive **projections** under the person's permission, propose changes and report back. The person can confirm, correct, contest, export and erase.

OHC is the person-side companion of Open Digital Employee (ODE). ODE describes a digital employee and its authority. OHC describes a person's context and the permissions under which it may be read. An ODE package never contains a person's context. It references the person’s grant; projections are fetched under it and checked at use.

**Try the three standards together:** [OHC + TARA + ODE guide](docs/interop/TARA-ODE.md),
[complete synthetic package and worked example](examples/ohc-ode-tara/README.md). The binding targets ODE
`v0.4.0-draft.2`; passing file checks does not verify consent or runtime behaviour.

## What OHC is not

OHC is not:

- a psychological theory or a "true model" of a person;
- a diagnosis or a clinical record (health appears only as pointers);
- agent behaviour: recognising states, deciding when to remind, methods of help;
- an authorization or delegation system (authority to act stays in ODE policies or the runtime);
- a score or ranking of a person;
- a hosted service, a registry service or a certification programme;
- a transport or identity protocol.

## L0 in five minutes

One file with a subject and a few claims is a conforming context. This is the complete minimal example, [examples/ilse-minimal/context.json](examples/ilse-minimal/context.json). Ilse is fictional.

```json
{
  "format": "ohc.context",
  "specVersion": "0.1.0-draft",
  "id": "urn:ohc:example:ilse:context",
  "version": "1",
  "subject": {"id": "urn:ohc:example:ilse", "displayName": "Ilse (fictional)"},
  "synthetic": true,
  "claims": [
    {"id": "c-1", "facet": "goal", "text": "Finish the Dutch B1 course by June 2027.", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-09T08:00:00Z", "horizon": "focus", "valid": {"until": "2027-07-01"}, "synthetic": true},
    {"id": "c-2", "facet": "boundary", "predicate": "time-window", "text": "No work messages after 19:00 on weekdays.", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-09T08:00:00Z", "horizon": "foundation", "synthetic": true},
    {"id": "c-3", "facet": "preference", "predicate": "format", "text": "Short written summaries before calls.", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-09T08:00:00Z", "synthetic": true},
    {"id": "c-4", "facet": "state", "predicate": "availability", "text": "Travelling; slow replies.", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-09T08:00:00Z", "horizon": "state", "valid": {"from": "2026-10-09", "until": "2026-10-13"}, "synthetic": true},
    {"id": "c-5", "facet": "goal", "predicate": "career", "absence": {"code": "not-chosen", "intentional": true}, "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-10-09T08:00:00Z", "synthetic": true}
  ]
}
```

Each claim has six required fields: `id`, `facet`, `text` (or `absence`), `origin`, `assertedBy` and `recordedAt`. The last claim is an intentional absence: Ilse chose not to set a career goal, and that choice is kept rather than filled in. No grant is needed at this level. **With no grant, nothing is disclosed to anyone but the subject.**

Check it with the reference checker (Python 3.9+ and `jsonschema`):

```sh
python3 tools/check.py examples/ilse-minimal --level L0 --json
```

The checker reports which defaults it applied (the conformance level, sensitivity, admission, endorsement and epistemic status). The [quickstart](docs/guides/QUICKSTART.md) walks through writing such a file with a person.

## Who can read and write OHC tomorrow

| Consumer | Minimum to adopt | What it gains |
|---|---|---|
| A personal agent (including persistent, person-bound agents) | Write L0 with the person, as their instrument ([CONTEXT-01](docs/agents/procedures/CONTEXT-01.md)). Read under a `read` grant to its own Party. Propose under `suggest` (and `infer` for its own readings), and reconcile with the person in batches ([CONTEXT-09](docs/agents/procedures/CONTEXT-09.md)). Keep the consumer obligations C-1…C-12. | A record of what the person said and decided that the person can inspect, correct and take to another agent. The agent's own model stays proposals until the person decides; OHC does not make it portable as fact. |
| A GUM-style system | Run the GUM importer: observations become `Source`, propositions become proposed inferred `Claim`, and raw rows are kept in `ext["gum.import"]`. | A split between declared and inferred content, consent, and the lineage that GUM ≥0.1.11 no longer keeps. |
| A context router in the style of Loyal Agents | Map `Preference` ↔ `Claim` and `PermissionGrant` ↔ `Grant`. Keep the READ ⊂ SUGGEST ⊂ WRITE ladder, but flip the default to deny. | A typed schema for goals, boundaries, relationships and states behind the same MCP tools. |
| An ODE digital employee | Declare the person's grant as an `externalDependencies` entry plus `extensions["ohc.binding"]`. Fetch projections under it at run time; never pin one. | ODE's deferred person seam is filled without adding a new ODE kind. |

Details: [interoperability guide](docs/interop/README.md), [GUM binding](spec/bindings/GUM.md), [ODE binding](spec/bindings/ODE.md), [MCP binding](spec/bindings/MCP.md).

## Modules

| Module | Contents | Maturity in 0.1 | Where |
|---|---|---|---|
| `core` | Context, Subject, Party, Claim, Relation, Source, Episode, Interpretation, Tension, Review, Proposal, Tombstone; status axes, time, freshness, absence, disclosure, derived labels, layer rules | normative-draft | [SPECIFICATION §1–§11](spec/SPECIFICATION.md) |
| `governance` | Grant, Event, Projection, ContextLock; grant evaluation, step-up, erasure, obligations | normative-draft (usable at any level; required at L2) | [SPECIFICATION §12–§16](spec/SPECIFICATION.md) |
| `lenses` | Lens, Instrument, Mapping and Playbook registry documents; LensAdoption, AssessmentRecord, ModelView | shapes and rules normative-draft; catalog entries experimental | [LENSES.md](spec/LENSES.md); per-person records in [SPECIFICATION §10.5–§10.7](spec/SPECIFICATION.md) |
| `instrument-import` | Bringing a test result from the report the person holds: the instrument `import` block, imported results, the agreement screen | normative-draft | [INSTRUMENT-IMPORT.md](spec/INSTRUMENT-IMPORT.md) |
| `practices` | Practice, Outcome | normative-draft | [SPECIFICATION §17](spec/SPECIFICATION.md) |
| `patterns` | Pattern | experimental | [SPECIFICATION §18](spec/SPECIFICATION.md) |
| `recall` | RecallCue | experimental | [SPECIFICATION §19](spec/SPECIFICATION.md) |
| `inner-system` | Part and part relations | experimental | [SPECIFICATION §20](spec/SPECIFICATION.md) |
| `health-ref` | HealthRef (a FHIR pointer only) | experimental | [SPECIFICATION §21](spec/SPECIFICATION.md) |
| `exchange` | 16 message formats | experimental | [EXCHANGE.md](spec/EXCHANGE.md) |
| `binding.gum` | GUM import and export | normative-draft for GUM compatibility claims | [bindings/GUM.md](spec/bindings/GUM.md) |
| `binding.ode` | ODE Tier 0 binding | normative-draft for ODE binding claims | [bindings/ODE.md](spec/bindings/ODE.md) |
| `binding.mcp` | MCP tools, including a gumcp-compatible tool | experimental | [bindings/MCP.md](spec/bindings/MCP.md) |

Three conformance levels: **L0 Minimal** (a manifest and a claim or an episode), **L1 Grounded** (grounds, hashes, reviews, layer rules) and **L2 Governed** (package form, event chain, grants, projections, lock).

## Start here

1. [Read the overview](docs/OVERVIEW.md) ([на русском](docs/OVERVIEW.ru.md)).
2. [Write a minimal context](docs/guides/QUICKSTART.md), or [start from an experience](docs/guides/QUICKSTART.md#start-from-an-experience), or [bring a test result to your agent](docs/guides/BRING-A-RESULT.md) ([на русском](docs/guides/BRING-A-RESULT.ru.md)).
3. [Read the specification](spec/SPECIFICATION.md), then the [lens module](spec/LENSES.md) and the [exchange messages](spec/EXCHANGE.md).
4. Explore five fictional people: [Ilse](examples/ilse-minimal/) (L0), [Mara](examples/mara-l1-agent/) (L1, episode-first, with a persistent study companion), [Noa](examples/noa-episode-first/) (L2, episode-first), [Kofi](examples/kofi-gum-ode/) (GUM import, an assessment import and an ODE employee) and [Tove](examples/tove-bring-a-result/) (L2, bringing a test result to her agent through her own window). The [viewer](viewer/index.html) renders each context, and each grantee's view, as static HTML.
5. Check [scope, maturity and what is not tested](STATUS.md).

**For agents:** start with [AGENTS.md](AGENTS.md) and the [consumer obligations](docs/agents/CONSUMER-OBLIGATIONS.md).

## What is included

- A normative [specification](spec/SPECIFICATION.md), JSON Schemas, controlled-vocabulary catalogs and a type catalog.
- A [lens module](spec/LENSES.md) with 16 catalog entries, instrument entries, population-level mappings and one basic playbook per entry; the [instrument import](spec/INSTRUMENT-IMPORT.md) module.
- Bindings for GUM, ODE and MCP, and informative [composition notes](spec/COMPOSITION.md) with crosswalks to other standards.
- An EN/RU [glossary](spec/glossary.json).
- Five synthetic examples, a static viewer, read-only reference tools (a checker, converters and a temporal query tool) and a reference holder that plays the person's window in the terminal.
- Agent [procedures](docs/agents/README.md) CONTEXT-01…CONTEXT-10, and per-lens recipes in [docs/lenses/](docs/lenses/).
- [Change history](CHANGELOG.md), [contribution guidance](CONTRIBUTING.md) and a generated release manifest that records files, licences, hashes and checks.

## Maintainers and licensing

Copyright 2026 Taras Pustovoy and contributors. See [contributors](CONTRIBUTORS.md) and [license scope](LICENSING.md). This is the **Open Human Context** specification, an experimental draft for review. It has not been published.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
