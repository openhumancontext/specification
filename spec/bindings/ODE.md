# ODE binding

Module `binding.ode` · binding revision `0.2.0` · OHC format `0.1.0-draft` · **normative-draft for anyone claiming this ODE binding**.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as described in BCP 14 (RFC 2119,
RFC 8174) when, and only when, they appear in all capitals.

Open Digital Employee (ODE) describes a digital employee and its authority. OHC describes a person's context and the
permissions under which it may be read. This binding lets an ODE package use a person's context **without containing
it**: the package names the grant the person gave, and the employee fetches a projection under it and re-checks it at
every use.

## 1. Pins

| Item | Value |
|---|---|
| ODE release | `0.4.0-draft.2` (git tag `v0.4.0-draft.2`) |
| ODE format | `0.4.0-draft` |
| ODE commit | `2de920485fb2665eaf7298ac65452a4a79412a9a` |
| OHC format | `0.1.0-draft` |

Current bridge rows in `spec/mappings/ode/` have filenames ending in `ode-0.4.0-draft.2.mapping.json` and carry this pin in `to.pin`. Rows ending in `ode-0.2.0-draft.3.mapping.json` are historical comparisons, not claims of current compatibility.

## 2. Tier 0 rule: no ODE schema change

- An ODE package that uses a person's context MUST declare the person's **Grant** as an entry in
  `externalDependencies`, and MUST carry the extension `ohc.binding`, listed in `manifest.requiredExtensions`.
- **The durable dependency is the grant, not a projection.** The entry's `objectId` is `<contextId>#<grantId>` and its
  `version` is the grant's `recordedAt`. Grants are immutable records, so this pins the permission. The context
  version, which changes with every change set, is never pinned.
- **The ODE package never contains context values, and never a projection.** At run time, the employee fetches a
  projection under the grant and re-checks it at use (`checkAtUse: true`; consumer obligation C-1, rule R-G6).
  Projection ids, digests and check times are restricted run-time evidence: send a `use-report` to the holder.
  They never enter a portable employee package. ODE decision history must respect the evidence boundary in §9.
- A link between an ODE `Party` and an OHC Subject grants nothing (R-L0). Access comes only from a Grant.
- A grant is never authority to act (R-G9). Authority stays in ODE policies and the runtime.

The value of `extensions["ohc.binding"]` is validated by `spec/schema/ode-binding.schema.json`. The reference checker
accepts the extension value, the fragment below, or a full ODE 0.4 `manifest.json`:
`python3 tools/check.py <file.json> --json`. For a full manifest it extracts the binding-related fields; it does
not validate the rest of ODE's manifest, object graph or lock. Run ODE's own package checker separately.

The fragment is an editing aid, not an ODE serialization: its `manifest` members, `externalDependencies` and
`extensions` all belong at the top level of the real `manifest.json`. Other ODE dependencies and extensions may
coexist. [The combined example](../../examples/ohc-ode-tara/README.md) shows the assembled package and both checks.

- **OB-1.** A packaged binding MUST supply `grantRef.context` without a fragment identifier, so the grant dependency can be identified exactly.
- **OB-2.** Exactly one external dependency MUST have `objectId = grantRef.context + "#" + grantRef.id`, and its `version` MUST equal `grantVersion`; missing, duplicate or mismatched dependencies are invalid.
- **OB-3.** The manifest MUST declare exactly one standard with `id: ohc`, `url: urn:ohc:specification` and `revision: 0.1.0-draft`, and MUST list `ohc.binding` in `requiredExtensions`.
- **OB-4.** A full manifest submitted to this binding revision MUST declare ODE `specVersion: 0.4.0-draft`.
- **W-OB1.** A standalone extension value has no package to check against; its validation MUST NOT be presented as verification of a packaged binding.

These checks establish internal consistency only. The holder authenticates the requester and evaluates the actual
grant at use. Declared mode, purpose, facets or a matching version never override that evaluation.

**Employers and schools (informative).** When the employee's operator is the person's employer or school, consent is
presumed not to be freely given (GDPR Recital 43, Art. 7(4) and Art. 88). The holder should be the person, or a party
independent of that organisation, and the grant should be narrow: `rule-only` or `summary` mode, no `infer`, and no
special records. A typed operator relation is an open question for 0.2 ([STATUS](../../STATUS.md)).

## 3. Example: a synthetic person's scheduling employee "Planner"

This is the fragment in `examples/kofi-gum-ode/ode/planner-binding.json`; a test keeps them equal.

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

## 4. `ohc.binding` fields

| Field | Req | Notes |
|---|---|---|
| `subjectAlias` | yes | The pairwise alias for the employee's grantee Party. The subject id is never included. |
| `partyRef` | no | The ODE Party (person), `{"objectId", "version"}`. It is **not** identity: see the bridge row Subject ↔ Party (`not-identity`). Never the OHC Party id. |
| `grantRef` | yes | `{"id": "g-…", "context"?: URI}`: the Grant the employee reads under. |
| `grantVersion` | yes | The grant's `recordedAt`. |
| `locator` | no | Where the employee asks the holder for projections. |
| `mode` | yes | The grant mode (`full`, `summary`, `rule-only`, `answer-only`). |
| `purpose` | yes | Exactly one purpose. |
| `facets` | no | The facets the employee expects to receive. |
| `prohibitedPurposes` | yes | All 13 prohibited purposes. |
| `checkAtUse` | yes | Const `true`. |

## 5. Use reports

When a projected item informs an ODE `Decision`, the employee SHOULD send the exchange message `use-report` with
`decisionRef` `{"objectId", "version"}`, the projection id and its digest, so that the person can see which items
informed which decision ([EXCHANGE.md](../EXCHANGE.md)). This is where projection ids and digests belong.

## 6. Bridge rows

Each row is a Mapping record (`bridgeKind: ohc-ode`) in `spec/mappings/ode/`. A row describes how two formats relate;
it never converts a person's data.

| OHC | ODE | Relation | Row status | Lost or forbidden use |
|---|---|---|---|---|
| Subject | Party (person) | `corresponds` | `not-identity` | Needs an explicit mapping. Never infer access from a Party link. |
| Claim | Fact | `corresponds` | `accepted-with-loss` | An ODE Fact requires a confidence. Origin and endorsement travel in extensions until Tier 1. |
| Grant | Policy | `not-covered` | `not-permitted` | A Grant is never authority. A Policy is never consent. |
| Grant reference | `externalDependencies` entry | `corresponds` | `accepted` | The package pins the grant, never a projection; projections are run-time evidence. |
| resource `attention` | `attentionBudget` | `carries-part` | `accepted-with-loss` | The total stays with the holder; the share is in the contract. |
| interaction preferences | InteractionContract `decisionBrief` / `channelRef` / `proactivity` | `corresponds` | `accepted-with-loss` | The reasons stay in OHC. |
| Proposal | IntakeRecord | `corresponds` | `not-identity` | Person-side versus pair-side. |
| glossary: person, person-profile, personal-space, consent, current-state, history | Subject, context, holder, Grant, `state` facet, knowledge time | `corresponds` | `unresolved` | ODE's `current-state` → RoleState is a mis-assignment. Reopen when ODE revises its glossary. |
| derived label | ODE `knowledgeOrigin` | `corresponds` | `accepted-with-loss` | One value per label (`spec/catalogs/labels.json`). |
| admission | ODE definition `status` | `not-covered` | `not-permitted` | Admission is not agreement with content. Preserve admission, endorsement, epistemic status, contested and freshness separately; do not convert active to agreed. |
| horizons | ODE lifecycles | `corresponds` | `accepted-with-loss` | `spec/catalogs/horizons.json` |

Three ODE terms in this table (IntakeRecord, `knowledgeOrigin` and the person-profile lifecycles) belong to ODE's
proposed person-profile extension, which is not part of the pinned release schemas. Their rows carry evidence grade
`verify` and a `reopenWhen` note.

## 7. Governance statement

**Status: proposed.**

> ODE's "Person profile" and "Personal space" proposed extensions are realised by OHC. ODE keeps `Party` as the
> in-package anchor and references the person's OHC grants; projections are fetched under them at run time.

## 8. Tier 1 proposals to ODE (informative)

These proposals are listed for discussion with ODE's maintainers. They have not been filed, and nothing in this
binding depends on them.

1. A person-context `contextRef`, if a future example justifies it. Typed participants already exist in ODE 0.4; this proposal concerns only the separate context reference.
2. `attentionBudget.holderRef`.
3. `AgentDNA.personRequirements[]` = `{"facet", "minLabel", "maxAge", "purpose", "requiredForLaunch"}`.
4. ODE `Fact` reuses OHC's absence codes.

## 9. Receiver, communication and evidence boundaries

OHC Party is a local recipient or author record. ODE distinguishes the persistent `Agent`, its working configuration
`DigitalEmployee`, an addressable `Identity`, and a role tenure `Assignment`. `Party.odeRef` may explicitly select
the corresponding ODE Party, Agent or DigitalEmployee; it is a declared correspondence, not authentication.
The optional binding `partyRef` remains the human subject's ODE Party, never the receiving agent.

The holder MUST authenticate the requester as the exact OHC grantee at use. A shared Agent, address, Space, home or
role does not propagate a grant. A new working configuration must remain within the same authenticated grantee,
purpose and permitted context; otherwise it needs its own grant. Role succession does not transfer prior access or
correspondence. Cross-context use, forwarding and delegation remain forbidden by GR-2; ODE contact permission does
not open OHC content. Do not silently relink a local recipient to a different principal.

There are separate decisions: permission to use context (OHC Grant), endorsement of a reading or confirmation of
a choice based on it (including R-G14), and authority to act (ODE Policy/runtime and, when needed, a scoped
authorization request). An information response cannot replace them. ODE 0.4's independent requests preserve this
separation; a request to disclose context follows OHC's holder channel, not another agent's assurance of consent.

An OHC Claim MUST NOT be copied into a portable package as an ODE Fact. The Claim/Fact bridge describes concepts,
not permission to convert data. In any separately permitted representation, preserve source, origin, endorsement,
epistemic status, contested and freshness. Missing confidence remains missing; do not invent the number ODE Fact
requires. Admission to OHC, including an active but contested record, does not set an ODE definition to `agreed`.

Private run-time evidence is subject to C-1, C-6 and C-12, including derived explanations, identifiers and digests.
Never copy a projection into a shared Space, a reusable skill or another agent's memory. A second recipient obtains
its own projection from the holder. Keep the holder's `use-report` and restricted evidence separate from portable
package resources and backups. Where required erasure cannot be enforced, do not store the content there.
An erasure or incident record can preserve the permitted fact that an event occurred without retaining erased
content; it must not falsely rewrite an unauthorized attempt as an authorized step.

## 10. Relationship to TARA

TARA's bounded-next-step method can operate on OHC context only within the grant and ODE's authority. A useful
step does not require resolving every Tension; `held-as-is` may remain. A successful action does not endorse an
interpretation of the person or authorize a permanent change to the agent. See the
[combined guide](../../docs/interop/TARA-ODE.md) and [synthetic example](../../examples/ohc-ode-tara/README.md).

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
