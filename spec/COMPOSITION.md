# Compose with existing formats

**Informative.** This document explains how OHC relates to the formats, protocols and standards around it. The
normative parts of the bindings are in [bindings/GUM.md](bindings/GUM.md), [bindings/ODE.md](bindings/ODE.md) and
[bindings/MCP.md](bindings/MCP.md); everything else here is explanation, crosswalk or design intent. Nothing in this
document is legal advice.

OHC documents are plain JSON first. JSON-LD processing is optional, and every IRI OHC defines is provisional
(`urn:ohc:vocab:<term>`). A crosswalk row says how two formats relate; it never converts a person's data on its own,
and it never replaces a grant.

## Open Digital Employee (ODE)

OHC is the person-side companion of ODE. ODE describes a digital employee and its authority; OHC describes a person's
context and the permissions under which it may be read.

- **Tier 0 binding, no ODE schema change.** An ODE package declares the person's grant as an
  `externalDependencies` entry (`<contextId>#<grantId>`, version = the grant's `recordedAt`), carries the extension
  `ohc.binding`, and lists it in `manifest.requiredExtensions`. The package never contains context values or a
  projection; the employee fetches projections under the grant and re-checks them at every use. See
  [bindings/ODE.md](bindings/ODE.md).
- **Bridge rows.** Eleven current Mapping records (plus eleven historical rows) in `spec/mappings/ode/` relate OHC kinds and vocabularies to ODE ones,
  pinned to ODE release `0.4.0-draft.2`. Subject ↔ Party is `not-identity`; Grant ↔ Policy is `not-permitted`: a
  Grant is never authority, and a Policy is never consent.
- **Governance statement (proposed):** "ODE's 'Person profile' and 'Personal space' proposed extensions are realised
  by OHC. ODE keeps `Party` as the in-package anchor and references the person's OHC grants."

## General User Models (GUM)

GUM (the `gum-ai` package, version 0.1.11, MIT) learns natural-language propositions about a user from observation.
The binding imports its observations as Sources and its propositions as proposed, inferred Claims, refuses affect
propositions that rest on screen or other behavioural observations (R-X4), quarantines other propositions about
affect, mood, stress or mental condition, reconstructs lineage across snapshots, and exports back for GUM under a
`gum-export` grant with a mandatory filter. GUM → OHC → GUM (Mode B, same grant) reproduces every column of each
proposition that is admitted and passes the export filter; refused, quarantined, special, `no-infer`, `person-only`,
rejected, contested and retracted propositions do not return. OHC → GUM → OHC restores ids, text, origin and dates;
the other axes stay on the OHC side. Only the `propositions` table is round-tripped, through an OHC JSON interchange
file; observations and the join table are one-way. See [bindings/GUM.md](bindings/GUM.md).

## Model Context Protocol (MCP)

An OHC holder can expose `get_user_context` with the same name, parameters and block layout as GUM's MCP server, so
that clients built for GUM work unchanged, with consent and purpose filtering behind the tool. The lines it prints come
from what the grant's mode serves, so a summary-mode grant shows that reasoning is withheld; the remaining
differences are listed in the binding. Eight native tools carry
the exchange messages. The binding is experimental. See [bindings/MCP.md](bindings/MCP.md) and
[bindings/mcp/tools.json](bindings/mcp/tools.json).

## Who can read and write OHC tomorrow

| Consumer | Minimum to adopt | What it gains |
|---|---|---|
| A personal agent (including persistent, person-bound agents) | Write L0 with the person, as their instrument (CONTEXT-01). Read under a `read` grant to its own Party. Propose under `suggest` (and `infer` for its own readings), and reconcile with the person in batches (CONTEXT-09). Keep consumer obligations C-1 to C-12. | A record of what the person said and decided that the person can inspect, correct and take to another agent. The agent's own model stays proposals until the person decides. |
| A GUM-style system | Run the GUM importer: observations become Sources, propositions become proposed inferred Claims, and raw rows are kept in `ext["gum.import"]`. | A split between declared and inferred content, consent, and the lineage that GUM 0.1.11 and later no longer keeps. |
| A context router in the style of Loyal Agents | Map `Preference` ↔ Claim and `PermissionGrant` ↔ Grant (see [Other crosswalks](#other-crosswalks)). Keep the READ ⊂ SUGGEST ⊂ WRITE ladder, but flip the default to deny. | A typed schema for goals, boundaries, relationships and states behind the same MCP tools. |
| An ODE digital employee | Declare the person's grant as an `externalDependencies` entry plus `extensions["ohc.binding"]`. Fetch projections under it at run time; never pin one. | ODE's deferred person seam is filled without adding a new ODE kind. |

## JSON-LD

- [bindings/jsonld/ohc.context.jsonld](bindings/jsonld/ohc.context.jsonld) maps OHC member names to provisional IRIs
  `urn:ohc:vocab:<term>` (through `@vocab`), maps `id` to `@id` and `kind` to `@type`, types the time fields as
  `xsd:dateTime`, keeps `ext`, `value` and `card` as JSON literals, and declares the prefixes `prov:`, `dpv:` and
  `odrl:`.
- JSON-LD processing is optional. OHC documents are plain JSON first.
- The IRIs are provisional, and the DPV namespace IRI declared in the context (`https://w3id.org/dpv#`) is
  **[verify]** against DPV 2.x.

## PROV-O

| OHC | PROV-O |
|---|---|
| `assertedBy` | `prov:wasAttributedTo` |
| `generatedBy` | `prov:wasGeneratedBy`, a `prov:Activity` |
| `evidence`, `grounds` | `prov:wasDerivedFrom` (`prov:hadPrimarySource` for Sources) |
| `supersedes` | `prov:wasRevisionOf` |
| `recordedAt` | `prov:generatedAtTime` |
| `retract` Review | `prov:invalidatedAtTime` |
| Source | `prov:Entity` |
| Party | `prov:Agent` |

## DPV (Data Privacy Vocabulary)

Concept names from DPV 2.3. The IRIs are **[verify]** against DPV 2.x before any normative use.

| OHC | DPV |
|---|---|
| origin | data-source concepts: Provided, Observed, Inferred, Derived, Collected (`declared` → ProvidedPersonalData, `observed` → ObservedPersonalData, `inferred` → InferredPersonalData, `derived` → DerivedPersonalData, `imported` and `attested` → CollectedPersonalData) |
| Grant status | ConsentGiven, ConsentWithdrawn, ConsentRevoked, ConsentExpired, ConsentInvalidated; and, in messages, ConsentRequested, ConsentRefused, ConsentRequestDeferred |
| `basis.legal` | Consent, ExplicitlyExpressedConsent, Contract |
| purposes | the candidate concepts listed per purpose in `spec/catalogs/purposes.json` **[verify]** |
| categories | special-category concepts **[verify]** |

## ODRL

A Grant can be expressed as an ODRL 2.2 policy. Actions prefixed `ohc:` are OHC-defined ODRL terms with provisional
IRIs.

| Grant | ODRL |
|---|---|
| the Grant | `odrl:Agreement` (`uid` = the grant id) |
| `grantor` / `grantee` | `odrl:assigner` (the subject alias) / `odrl:assignee` |
| `scope` | `odrl:target`, an `odrl:AssetCollection` with an `odrl:refinement` per selector field |
| `read` | permission `odrl:read` |
| `suggest` / `write` | permission `ohc:suggest` / `ohc:write` |
| `infer` | permission `ohc:infer` |
| `cite-excerpt` | permission `ohc:citeExcerpt` |
| `open-verbatim` | permission `ohc:openVerbatim`, with duty `ohc:stepUp` |
| `export` | permission `odrl:distribute`, constrained to the named recipient |
| `purposes` | constraint `odrl:purpose` `odrl:isAnyOf` |
| `expiresAt` | constraint `odrl:dateTime` `odrl:lt` |
| `maxUses` | constraint `odrl:count` `odrl:lteq` |
| `forwarding: false` | prohibition `odrl:distribute` |
| handling `no-quote` / `no-infer` / `no-leverage` | prohibitions `ohc:quote` / `ohc:infer` / `ohc:leverage` |
| revocation and erasure | duty `odrl:delete` (by `purgeBy`) |
| `effect: deny` | `odrl:prohibition` on the target |
| status | `dpv:hasConsentStatus` |

## Other crosswalks

| Standard or system | Mapping |
|---|---|
| **Human Context Protocol (Loyal Agents)** | ACTIVE / SUGGESTED / REJECTED → admission `active` / `proposed`, and endorsement `rejected`.<br>USER / INFERRED / IMPORTED / SYSTEM → origin `declared` / `inferred` / `imported` / `observed`.<br>READ ⊂ SUGGEST ⊂ WRITE → the same ladder, plus a separate `infer`; **the default is flipped to deny**.<br>`McpAccessEvent` → Event `projection-served`. |
| **GUMO** | SituationalStatements (UserML, used with GUMO) arrange attributes in five boxes:<br>mainpart (subject, auxiliary, predicate, range, object) → Subject, `facet` + `predicate`, `text` / `value`;<br>situation (start, end, durability, location, position) → `valid` + `recordedAt` (location and position are lost);<br>explanation (source, creator, method, evidence, confidence) → `origin`, `assertedBy`, `evidence`, `confidence`;<br>privacy (key, owner, access, purpose, retention) → Grant (owner → `grantor`, access → `audience` and `grantee`, purpose → `purposes`, retention → `expiresAt`; GUMO's values are qualitative, so accepted with loss);<br>administration (id, unique, replaces, group) → `id` and `supersedes` (partial).<br>The conflict resolvers `mostPersonal`, `mostRecent`, `returnDialog` and `returnNone` are kept (Heckmann 2006, §6.3.3, situation retrieval). |
| **JSContact (RFC 9553)** | A Card is embedded verbatim in `Subject.card` (category `identity-linking`). |
| **schema.org Person** | Public projections only (name; `jobTitle` from `role` claims). Never for sensitive content. |
| **Verifiable Credentials 2.0** | `origin: attested`. The credential is embedded in `ext["vc.credential"]`. Verification is outside OHC. |
| **HL7 FHIR R4/R5** | HealthRef pointers only. FHIR Consent is not used for OHC grants. |
| **IEEE 7012-2025 (MyTerms)** | `Grant.basis.myTermsRef` |
| **ISO/IEC TS 27560 consent records and the Kantara Consent Receipt** **[verify field names]** | Grant ↔ consent record: `grantor` ↔ PII principal; holder ↔ PII controller; `grantee` ↔ recipient; `purposes` ↔ purposes; selector categories ↔ PII categories; `basis` ↔ legal basis; `expressedBy.at` ↔ consent timestamp; `expiresAt` ↔ termination; status ↔ consent state.<br>Event `grant-given` ↔ issuing a consent receipt.<br>`projection-served` has no receipt counterpart: it is a disclosure log. |
| **ffielitz memory schema** | source human / ai / derived / import → origin `declared` / `inferred` / `derived` / `imported`; authority proposed / authoritative → admission `proposed` / endorsement `endorsed`. |
| **postnikov privacy flags** | Not to Remember / Not to Quote / Not to Infer → handling `no-remember` / `no-quote` / `no-infer`. |
| **Mem0, Letta, Graphiti** | `valid_at` / `invalid_at` → `valid.from` / `valid.until`; `created_at` → `recordedAt` (or `formulatedAt` on import); `expired_at` → a `retract` Review or a supersession. |
| **ODE** | [Open Digital Employee (ODE)](#open-digital-employee-ode) above, and [bindings/ODE.md](bindings/ODE.md). |

## Machine-readable crosswalks

Every row in the PROV-O, DPV, ODRL and other crosswalk tables above is also published as a Mapping record (`format: ohc.mapping`, `bridgeKind: ohc-standard`). Each
file in `spec/crosswalks/` is a JSON array of such records:

| File | Standard or system |
|---|---|
| `hcp-loyal.json` | Human Context Protocol reference code (Loyal Agents), pinned by commit |
| `gumo.json` | GUMO |
| `dpv.json` | DPV 2.3 |
| `prov.json` | PROV-O |
| `odrl.json` | ODRL 2.2 |
| `jscontact.json` | JSContact (RFC 9553) |
| `schema-org.json` | schema.org Person |
| `vc.json` | Verifiable Credentials 2.0 |
| `fhir.json` | HL7 FHIR |
| `myterms.json` | IEEE 7012-2025 |
| `consent-receipts.json` | ISO/IEC TS 27560 and the Kantara Consent Receipt |
| `ffielitz.json` | ffielitz memory schema, pinned by commit |
| `postnikov.json` | postnikov privacy flags, pinned by commit |
| `memory-systems.json` | Mem0, Letta, Graphiti |

Rows whose external side was not read in its primary form carry evidence grade `verify`; every row is
`notIdentity: true` and `chainable: false`.

## Legal hooks

**Not legal advice.** No legal review has been performed. This table records design intent: which OHC mechanism was
designed with which legal text in mind.

| Source | OHC mechanism |
|---|---|
| GDPR Art. 9; CJEU C-184/20 (indirect revelation of special data) | the `special` tier; category minimums; tier propagation (C3) |
| GDPR Art. 4(4) (profiling) | the `infer` action, separate and off by default (INF-1, R-G11) |
| GDPR Art. 22 | `significant-automated-decision` is a prohibited purpose; a grant's `decisionUse` is `deny` unless the person chose `approval-required`, under which the person confirms every proposal (R-G14) |
| GDPR Arts. 15, 16, 17, 20; Art. 7(3) | read (H-15), correct (supersession, Reviews), erase (erasure flow), export (H-9); withdrawal of consent (`withdraw-grant`) |
| GDPR Recital 43, Art. 7(4), Art. 88 (consent of employees is presumed not freely given) | informative guidance for grants to an employer's or school's agents: an independent holder, narrow grants, no `infer`, no special records (`SPECIFICATION.md` §12.4); a typed operator relation is open for 0.2 |
| GDPR Arts. 17(2), 19 | the erasure notice is a MUST |
| EU AI Act Art. 5(1)(f); Recital 44; Commission guidelines C(2025) 884 final (4 Feb 2025) | R-X3 (quarantine of affect content), R-X4 (biometric and behavioural ban), `emotion-recognition-at-work-or-education` is a prohibited purpose. Art. 5(1)(f) concerns emotion recognition from biometric data; R-X4 deliberately also covers behavioural and screen signals, and the prohibited purpose also covers emotions read from text: **stricter than the act**. |
| EU AI Act Annex III 4(a), 4(b) | `personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision` are prohibited purposes |
| EU AI Act Art. 5(1)(a), 5(1)(b) (manipulation; exploiting vulnerabilities) **[verify]** | `persuasion-targeting` is a prohibited purpose. **Stricter than the act:** OHC closes any tailoring of persuasion to the person's psychology, not only harmful manipulation. |
| EU AI Act Art. 5(1)(c) (social scoring) **[verify]** | `cross-person-ranking` is a prohibited purpose. **Stricter than the act:** OHC closes any ranking of the person against others, not only social scoring by public or private actors with detrimental effect. |
| GDPR Art. 9(1) (political opinions) | the `political` category is special; `political-profiling` is a prohibited purpose. **Stricter than the regulation:** no consent opens it (C-7). |
| — (no named legal basis yet) | `advertising`, `credit-or-insurance-decision`, `model-training` and `sale-or-transfer` are prohibited purposes by OHC's own choice: they protect the person from others' decisions and from uses they cannot follow. A legal basis is open for the review before publication. |
| Professional confidentiality | `custody` and its ceilings; no practitioner access in 0.1 |
| Trademarks and copyright (17 U.S.C. §102(b); *Arica Institute v. Palmer*) | lens `ip`, never-fields, `trademarkNotice`, `constructsByReference` |
| Russian Federal Law No. 152-FZ | **not analysed** |

Documentation says that a record is "treated as special category"; it never says that a record "is Art. 9 data".

## What composition does not establish

- A crosswalk row is not a conversion, and a mapping between formats is never an identity.
- Embedding a JSContact card or a verifiable credential does not verify it.
- An ODE reference to a grant gives the employee no access by itself; only the Grant's computed status, re-checked at
  every use, does, and only for its purpose.
- No binding in this release has been run against a live GUM store, MCP client or ODE runtime.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
