# Interoperability guide

For a bounded task across all three layers, start with [OHC, TARA and ODE](TARA-ODE.md) and the
[complete synthetic example](../../examples/ohc-ode-tara/README.md).

This guide is for people who build systems that should read or write Open Human Context: personal agents, user-model
stores, context routers, digital employees. It explains what each binding does and where its exact rules live. The
rules themselves are in `spec/`; this page only points to them.

All examples in OHC use synthetic people.

## Start here: who can read and write OHC tomorrow

| You build | Minimum to adopt | What you gain |
|---|---|---|
| A personal agent, including a persistent, person-bound agent | Write the minimal level (L0) with the person, as their instrument (CONTEXT-01). Read under a `read` grant to your own Party. Propose under `suggest` (and `infer` for your own readings), and reconcile with the person in batches (CONTEXT-09). Keep the consumer obligations C-1 to C-12. | A record of what the person said and decided that they can inspect, correct and take to another agent. Your own model stays proposals until the person decides. |
| A GUM-style user-model store | Run the GUM importer. | A split between declared and inferred content, consent, and lineage across revisions. |
| A context router in the style of Loyal Agents | Map preferences to Claims and permission grants to Grants. Keep the READ ⊂ SUGGEST ⊂ WRITE ladder, with deny as the default. | A typed schema for goals, boundaries, relationships and states behind the same tools. |
| An ODE digital employee | Declare the person's grant as an external dependency with the `ohc.binding` extension. Fetch projections under it at run time; never pin one. | The person seam of ODE, without a new ODE kind and without person data in the package. |

Three rules hold for every integration:

1. **Default deny.** Nothing reaches you without a grant from the person, and a grant covers named purposes only.
2. **Use is not inference.** Building or updating a model of the person needs a separate `infer` permission.
3. **A grant is not authority.** It lets you read under its terms; it never lets you act in the world.

## GUM: importing and exporting a user model

[spec/bindings/GUM.md](../../spec/bindings/GUM.md) (normative-draft for anyone claiming GUM compatibility).

- **Import.** GUM observations become Sources (screen observations default to the `index` release tier).
  Propositions become Claims with `origin: inferred`, admission `proposed` and the raw GUM row in
  `ext["gum.import"]`. The person admits or declines each one.
- **Time.** GUM's `created_at` becomes `formulatedAt`; the capture time is absent, because GUM does not keep it.
- **Confidence.** GUM's 1–10 score is kept raw and as `value = raw/10`, with `semantics: support-score`. A missing
  confidence stays missing; it never becomes 0.
- **Refusal and quarantine.** Propositions about affect, mood, stress or mental condition that rest on screen or
  other behavioural observations are refused and not imported (R-X4); the importer reports only how many. Other such
  propositions become special-tier, person-only and `no-infer`. When in doubt, the importer refuses or quarantines.
- **Lineage.** GUM rewrites propositions on revision. The importer reconstructs lineage across snapshots with Reviews
  and supersession; nothing is deleted.
- **Export.** Only under a `gum-export` grant, selected by the grant evaluation, only active records, never special,
  rejected, contested, frame-relative or `no-infer` content. Mode A seeds GUM with observations; Mode B writes the
  propositions' columns, raw timestamps included, to an OHC JSON interchange file, with a sidecar. GUM → OHC → GUM
  reproduces every column of each admitted proposition that passes the filter; refused, quarantined and withheld ones
  do not return. Only the `propositions` table round-trips; observations and the join table are one-way.
- **Tool:** `tools/convert_gum.py`. **Example:** `examples/kofi-gum-ode/`.

## MCP: a tool surface for agents

[spec/bindings/MCP.md](../../spec/bindings/MCP.md) (experimental) and
[spec/bindings/mcp/tools.json](../../spec/bindings/mcp/tools.json).

- **`get_user_context(query: str | None = "", start_hh_mm_ago: str | None = None, end_hh_mm_ago: str | None = None) -> str`**
  has the same name, parameters and block layout as GUM's MCP server. Behind it, the holder serves at most three
  active, non-special Claims under the caller's grant, printing only what the grant's mode serves. It returns an
  empty string when there is no grant, and gumcp's no-results sentence when a valid grant matches nothing.
- Eight native tools carry the exchange messages: projections, answers, proposals, feedback, source access, use
  reports and the caller's own grants. Their behaviour is in [spec/EXCHANGE.md](../../spec/EXCHANGE.md).

## ODE: a digital employee that uses a person's context

[spec/bindings/ODE.md](../../spec/bindings/ODE.md) (normative-draft for anyone claiming ODE binding), pinned to ODE
release `0.4.0-draft.2`.

- The ODE package lists `ohc.binding` in `manifest.requiredExtensions`, declares the person's **grant** as an
  `externalDependencies` entry (`<contextId>#<grantId>`, version = the grant's `recordedAt`), and describes it in
  `extensions["ohc.binding"]`: alias, grant reference and version, locator, mode, purpose, all prohibited purposes,
  and `checkAtUse: true`.
- **The package never contains the person's context, nor a projection.** The employee fetches projections under the
  grant at run time and re-checks the grant at every use.
- When a projected item informs an ODE `Decision`, the employee sends a `use-report` with the projection id and
  digest, so the person can see what was used.
- Eleven current bridge rows (plus eleven historical rows) in `spec/mappings/ode/` say how the two formats relate. A Party is not the person's identity in
  OHC, and an ODE Policy is never the person's consent.
- **Governance statement (proposed):** ODE's "Person profile" and "Personal space" proposed extensions are realised
  by OHC; ODE keeps `Party` as the in-package anchor and references the person's OHC grants.

## Crosswalks to other standards

[spec/COMPOSITION.md](../../spec/COMPOSITION.md) explains each crosswalk; `spec/crosswalks/*.json` publishes every row
as a Mapping record.

- **DPV:** origin codes map to data-source concepts; grant status maps to consent status concepts.
- **PROV-O:** attribution, generation, derivation and revision map one to one.
- **ODRL:** a Grant compiles to an ODRL Agreement with permissions, constraints, prohibitions and duties.
- **JSContact, schema.org, Verifiable Credentials, FHIR, IEEE 7012:** identity cards, public projections, attested
  claims, health pointers and MyTerms references.
- **Human Context Protocol (Loyal Agents), GUMO, ffielitz, postnikov, Mem0, Letta, Graphiti:** status, origin,
  permission and time vocabularies.
- **ISO/IEC TS 27560 and the Kantara Consent Receipt:** a Grant corresponds to a consent record; field names are still
  to be verified.

A crosswalk row is never a conversion of a person's data and never an identity between concepts.

## Checking your output

- `python3 tools/check.py <file-or-dir> --level L0|L1|L2 --json` validates a context against the schemas and the
  rules. It never follows external locators and never prints field values.
- Passing the checker means the file is well-formed and follows the rules that can be checked statically. It does not
  establish that the content is true, that consent was given, or that any runtime behaves correctly.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
