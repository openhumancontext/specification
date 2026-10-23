# CONTEXT-07 / 0.3.0 — Bind a person's grant into an ODE package

**Procedure · 0.3.0 · normative-draft module `binding.ode` revision 0.2.0 · 23 October 2026.** Let an Open Digital Employee (ODE 0.4) use a person's context without the context ever entering the ODE package. The binding is specified in [bindings/ODE.md](../../../spec/bindings/ODE.md); it needs no change to ODE's schemas.

## Use when

A digital employee described as an ODE package (for example a scheduling employee) should respect a person's boundaries, preferences or availability.

## Inputs

- The ODE package of the employee.
- The employee as a Party in the person's context, with the `governance` module declared. An `odeRef` on the Party is optional and is not identity.
- A grant from the person to that Party, for example: purpose `scheduling`, mode `rule-only`, `interpretations: none`, an expiry of a few months. The person gives it; you do not.

## Steps

1. **Get the person's grant.** Ask through the holder (`grant-request`). Keep the scope to what the work needs; work contexts rarely need readings, states beyond availability and load, or any special-category content. When the employee's operator is the person's employer or school, keep the grant narrow (`rule-only` or `summary`, no `infer`, no special records): consent there is presumed not to be freely given.
2. **Never copy context values, and never pin a projection.** The ODE package names the person's grant. Projections are fetched at run time.
3. **Declare the extension and the standard.** In the ODE package, `manifest.requiredExtensions` contains `"ohc.binding"`, and `manifest.standards` contains `{"id": "ohc", "url": "urn:ohc:specification", "revision": "0.1.0-draft", "required": false}`.
4. **Declare the dependency on the grant.** Add an `externalDependencies` entry whose `objectId` is `<contextId>#<grantId>` and whose `version` is the grant's `recordedAt` (grants are immutable). Give a `reason` that says values are not included and the grant is re-checked at every use, and a `locator` where the employee asks the holder.
5. **Add the binding extension.** `extensions["ohc.binding"]` holds:
   - `subjectAlias`: the pairwise alias the holder issued for the employee's Party;
   - `partyRef` (optional): the person's ODE Party, `{"objectId", "version"}`. It is not identity, and never the OHC Party id;
   - `grantRef`: `{"id": "g-…", "context": "<contextId>"}`, and `grantVersion`: the grant's `recordedAt`;
   - `locator`, `mode`, `purpose`, optional `facets`;
   - `prohibitedPurposes`: all thirteen prohibited purposes (a lens adds none);
   - `checkAtUse: true`.

   This is the synthetic example from [examples/kofi-gum-ode/ode/planner-binding.json](../../../examples/kofi-gum-ode/ode/planner-binding.json):

   ```json
   {
     "manifest": {
       "requiredExtensions": [
         "ohc.binding"
       ],
       "standards": [
         {
           "id": "ohc",
           "url": "urn:ohc:specification",
           "revision": "0.1.0-draft",
           "required": false
         }
       ]
     },
     "externalDependencies": [
       {
         "objectId": "urn:ohc:example:kofi:context#g-03",
         "version": "2026-10-01T09:00:00Z",
         "reason": "Person context held by the person; read under OHC grant g-03 for scheduling; values not included; projections fetched and the grant re-checked at every use",
         "locator": "ohc+mcp://holder.example/kofi"
       }
     ],
     "extensions": {
       "ohc.binding": {
         "subjectAlias": "urn:ohc:alias:mej2a2du5ccc4xp4umm4quxgib",
         "partyRef": {
           "objectId": "urn:ode:example:party:kofi",
           "version": "0.2.0"
         },
         "grantRef": {
           "id": "g-03",
           "context": "urn:ohc:example:kofi:context"
         },
         "grantVersion": "2026-10-01T09:00:00Z",
         "locator": "ohc+mcp://holder.example/kofi",
         "mode": "rule-only",
         "purpose": "scheduling",
         "facets": [
           "boundary",
           "preference",
           "state"
         ],
         "prohibitedPurposes": [
           "personnel-selection",
           "task-allocation",
           "performance-evaluation",
           "promotion-decision",
           "cross-person-ranking",
           "persuasion-targeting",
           "advertising",
           "political-profiling",
           "credit-or-insurance-decision",
           "emotion-recognition-at-work-or-education",
           "model-training",
           "sale-or-transfer",
           "significant-automated-decision"
         ],
         "checkAtUse": true
       }
     }
   }
   ```
6. **Assemble and check.** The fragment is an editing aid: place its `manifest` members, `externalDependencies` and `extensions` at the top level of the real ODE `manifest.json`. Run `python3 tools/check.py <manifest.json> --json`. It checks the OHC binding schema and agreement between the grant reference, dependency version and standard declaration (OB-1…OB-4). Run ODE's own package checks separately. The [combined example](../../../examples/ohc-ode-tara/README.md) includes both checks.
7. **At run time, re-check.** The holder authenticates the exact grantee, evaluates the current grant and fetches a permitted projection. When a projected item informs a decision, send a restricted `use-report` back to the holder, with the projection id and digest and any decision reference. These remain restricted run-time evidence and never go into a portable package or another agent's memory. Keep R-G14, storage, erasure and no-forwarding limits.

## Keep in mind

- A Grant is never authority to act; an ODE Policy is never consent.
- A link between the person and an ODE Party grants nothing.
- ODE Agent, DigitalEmployee, Identity and Assignment are distinct. A shared agent, address or successor in a role does not transfer a grant or permit use in another working context.
- Admission is not endorsement. Never turn an active but contested OHC record into an agreed fact, and never invent the confidence required by ODE Fact.
- When the grant is withdrawn or expires, the employee stops using projections and purges them. A renewed grant is a new grant, with a new `grantRef` and `grantVersion`.

## Output and completion

An ODE 0.4 manifest (or an explicitly labelled editing fragment) that names the person's grant as an external dependency, carries a consistent `ohc.binding` extension, and contains no context values and no projection. The OHC checker establishes the binding's structure and internal consistency only. ODE's own package checks and the employee's run-time behaviour are not established by it.

Do not invent a person; use only what the person said or granted.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
