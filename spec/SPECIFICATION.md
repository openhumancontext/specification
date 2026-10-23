# Open Human Context specification

**Draft release 0.1.0-draft.2 · format 0.1.0-draft.** Draft. Not published. The name and the `urn:ohc:` namespace are provisional.

This document is the normative specification of Open Human Context (OHC). It is licensed under Apache-2.0; see the [license scope](../LICENSING.md).

- Sections 1 and 3–17 are **normative-draft**. They use BCP 14 keywords and may still change before 1.0.
- Sections 18–21 are **experimental**. No conformance claim may rely on them.
- Section 2 and Annexes A–C are **informative**.

Companion documents: the lens module is specified in [LENSES.md](LENSES.md), and the instrument-import module in [INSTRUMENT-IMPORT.md](INSTRUMENT-IMPORT.md); the experimental exchange messages in [EXCHANGE.md](EXCHANGE.md); the bindings in [bindings/](bindings/); the relationship to other standards and the legal hooks, informatively, in [COMPOSITION.md](COMPOSITION.md). Schemas are in [schema/](schema/), controlled vocabularies in [catalogs/](catalogs/), and the bilingual glossary in [glossary.json](glossary.json).

## What this specification does not establish

OHC is not:

- a psychological theory or a "true model" of a person;
- a diagnosis or a clinical record (health appears only as pointers);
- agent behaviour: recognising states, deciding when to remind, methods of help;
- an authorization or delegation system (authority to act stays in ODE policies or the runtime);
- a score or ranking of a person;
- a hosted service, a registry service or a certification programme;
- a transport or identity protocol.

It also does not establish:

- that any content is true: schema validity is not truth;
- that a permission is enforced: a grant is not enforcement;
- runtime behaviour: a checker never claims it;
- that an example describes a real person: every example is synthetic;
- care: recall is not therapy and not crisis support.

OHC records representations and permissions; it does not establish who a person is, decide for them, or provide psychological or medical help.

## Contents

1. Scope, terminology and conformance language
2. Why: five clauses and two principles (informative)
3. Data model overview
4. Conformance: modules, levels and classes
5. Conventions
6. Status axes and derived labels
7. Time model, freshness and temporal queries
8. Disclosure
9. Context, Subject, Party, Claim, Relation
10. Source, Episode, Interpretation, Tension
11. Review, Proposal, Tombstone
12. Grant and grant evaluation
13. Event log
14. Projection, ContextLock and package layout
15. Vault, release tiers, step-up, erasure, export and multi-holder
16. Consumer and holder obligations
17. Practices and Outcomes
18. Patterns (experimental)
19. Recall cues (experimental)
20. Inner system: Parts (experimental)
21. Health pointers (experimental)
- Annex A. Rules index (informative)
- Annex B. Privacy and security considerations (informative)
- Annex C. Experience-first checks mapped to tests (informative)

## 1. Scope, terminology and conformance language

### 1.1. Scope

Open Human Context (OHC) is an open, file-based format for the context a person shares with the agents and services that work with them. It does not describe who a person "really is". Instead, it keeps **records about a person, each with its origin**:

- the primary sources they rest on;
- the experiences those sources tell of;
- how those experiences were understood at the time and later;
- what is stated about the person now;
- the frameworks of description through which anything was read;
- the ways of coping that were tried, and whether they helped;
- the permissions under which any of it may be used.

The person holds the context or chooses who holds it. Agents receive **projections** under the person's permission, propose changes and report back. The person can confirm, correct, contest, export and erase.

**Responsibility boundary.** OHC standardizes the representation and exchange of human context. Recognizing states, deciding whether and when to remind someone, and methods of psychological help are agent behaviour and are outside OHC.

OHC is the person-side companion of Open Digital Employee (ODE). ODE describes a digital employee and its authority. OHC describes a person's context and the permissions under which it may be read. An ODE package never contains a person's context; it references a projection that the person granted ([bindings/ODE.md](bindings/ODE.md)).

### 1.2. Terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY" and "OPTIONAL" in this document are to be interpreted as described in BCP 14 (RFC 2119, RFC 8174) when, and only when, they appear in all capitals, as shown here.

| Term | Meaning in this specification |
|---|---|
| subject | The person a context is about. In actor fields the subject is written `"subject"`. |
| holder | Whoever keeps the context and the vault, evaluates grants and serves projections: the person's own store, a personal agent acting as holder, or a context router. In actor fields it is written `"holder"`. |
| party | Anyone other than the subject who asserts, narrates, receives, holds or appears in a context: people, agents, software and organizations (§9.3). |
| steward | A party the subject authorised to act within an explicit scope (§9.1). |
| grantee | The party a Grant is given to (§12.1). |
| record | One immutable unit of a context, of one kind. |
| content record | A record in the evidence, experience, assertion, interpretation, recall, outcome or link layer (§3.4). |
| governance record | A Review, Proposal, Grant, Event or Tombstone. |
| document | A top-level JSON value with a `format` member: a Context, Projection, ContextLock, Lens, Instrument or Mapping, or an exchange message. |
| projection | What one grantee receives for one purpose at one time (§14.1). It is the only form in which OHC content leaves the holder. |
| vault | Where primary material is kept, content-addressed by hash (§15). |

The bilingual (EN/RU) [glossary](glossary.json) defines the shared vocabulary. English is the reference language.

### 1.3. Maturity

- **normative-draft:** 0.1 MUST/SHOULD text. It may still change before 1.0.
- **experimental:** the shape is published under its own version and may change. No conformance claim may rely on it. Experimental documents carry `format: "ohc.experimental.<name>"`, or the record's `kind` sits in an experimental module (§4.1).
- **informative:** explanatory only.

### 1.4. Rule identifiers

Rule identifiers (for example R-G1, CL-4, I5, C-7 or H-12) are stable. The reference checker, its tests and the documentation cite them.

- Each rule is defined exactly once: where its identifier appears **in bold** at the start of the rule. Every other occurrence of the identifier is a reference.
- Lens rules (LN-…), mapping rules (M-…) and playbook rules (PB-…) are defined in [LENSES.md](LENSES.md). Instrument-import rules (IMP-…, INS-…, IMA-…, IMH-…) are defined in [INSTRUMENT-IMPORT.md](INSTRUMENT-IMPORT.md). Proposal-inbox rules (IB-…) are defined in [EXCHANGE.md](EXCHANGE.md).
- Identifiers that begin with `W-` name checker warnings, not errors.
- Some rules are normative but not machine-checkable (for example I3). The reference checker lists them as such.
- Identifiers that only the reference checker uses (`J-`, `S-`, `ENV-`, `ID-`, `LV-`, `RA-1`, `TP-2`, `TP-3`, `X-2`, `X-3`, `REL-` and `SELF-`) are defined in [Annex A.2](#a2-checker-identifiers), each with the specification rule it implements.
- [Annex A](#annex-a-rules-index-informative) indexes every identifier.

"The checker" means the reference checker `tools/check.py`. A checker finding names the rule, the record id and the field path, and adds the rule's own sentence (`message`) and the place that defines it (`see`). For a schema failure it also names the failing JSON Schema keyword and the schema property (`detail`, for example `required: assertedBy`). It never contains a field value (§5.8).

### 1.5. Reading the field tables

- **Req** is `yes`, `no`, `cond` (the condition is in Notes) or `ctx` (required in package JSON Lines files and in messages, implied by the collection in the single document; R-S2).
- **Type** names refer to the shared types in §5.9.
- **Vocabulary** names refer to the section that defines the list. Every list is also published as a catalog in [catalogs/](catalogs/) (§5.10).
- Every schema sets `additionalProperties: false`, except inside `ext`, inside a Claim's `value` and inside the embedded JSContact `card` (and the lens descriptor exceptions stated in LENSES.md).
- All examples are synthetic. Their people (Noa, Ilse, Kofi and Mara) are fictional, and third parties appear only as role labels.
- The JSON examples in this document are taken from the published examples ([examples/](../examples/)). Where an example is abridged, its caption says so. A test (`tools/tests/test_spec_examples.py`) keeps them equal to the example files.

### 1.6. References

Normative:

- BCP 14: RFC 2119 and RFC 8174 (requirement keywords).
- RFC 8259 (JSON), RFC 8785 (JSON Canonicalization Scheme, JCS), RFC 3339 (date-time), ISO 8601 (durations), BCP 47 (language tags).
- JSON Schema draft 2020-12.
- FIPS 180-4 (SHA-256), RFC 2104 (HMAC), RFC 5869 (HKDF), RFC 4648 (base32 and base64url encodings).
- RFC 9553 (JSContact), for `Subject.card`.

Informative: the W3C Web Annotation Data Model (selector design), UCUM (units), and the standards listed in [COMPOSITION.md](COMPOSITION.md).

## 2. Why: five clauses and two principles (informative)

### 2.1. Five clauses and their mechanisms

The five clauses are the provisional English rendering of the Russian original, «Человек сам меняется. Его цели противоречивы. Его память избирательна. Его представления о себе пересматриваются. Иногда он теряет доступ к собственным способам справляться с происходящим.» The single canonical English wording is the `tagline` entry of the [glossary](glossary.json).

| Clause | What OHC does | Mechanism (sections) |
|---|---|---|
| A person changes. | Nothing is current by default. Content is immutable, and a change is a new record that supersedes the old one. Freshness is computed at use, never stored. | `supersedes`, the two time axes, the freshness algorithm (§3.4, §7) |
| Their goals conflict. | Contradictory claims coexist. A `Tension` records a conflict that matters and who decides it. Nothing is averaged or resolved automatically. | `Tension`, the `contradicts` relation, rule T1 (§10.4) |
| Their memory is selective. | Primary material is kept by reference with a hash. An episode carries several dated accounts: in the moment, later reconstruction, external record. Interpretations carry counter-evidence. The person can return to the exact span of the original. | `Source`, `Episode` accounts, `counterEvidence`, vault tiers and step-up (§10.1–§10.3, §15) |
| Their understanding of themselves is revised. | Interpretations are separate, attributed records on the knowledge-time axis, with `heldDuring`. "How did I understand this then?" is a query. | `Interpretation`, temporal self-model queries (§10.3, §7.3) |
| Sometimes they lose access to their own ways of coping with what is happening. | Practices that worked, and their outcomes, are first-class records. A recall cue the person authorises lets an agent hand them back, with alternatives and a brake against self-confirmation. | `Practice`, `Outcome`, `RecallCue` (§17, §19) |

### 2.2. Two principles

1. **Preserve experience. Evolve interpretations.** This principle governs OHC's data architecture.
2. **Help humans remember what they know when they need it most.** This principle describes what agents can build on OHC. The behaviour itself is outside the standard.

OHC records representations and permissions; it does not establish who a person is, decide for them, or provide psychological or medical help.

### 2.3. Design principles

1. **Representations, not the person.** OHC records who said what about a person, when, on what grounds and for whom. An agent may hold its own view. No agent has the exclusive right to define the person.
2. **Preserve experience, evolve interpretations.** Sources and episodes are kept apart from readings of them. Readings are separate, attributed records with their own history. A new reading never overwrites evidence or an earlier reading. Evidence never depends on interpretation (layer rule G1).
3. **The person decides; inference is a proposal.** Anything the person did not assert enters as `proposed`. Only the person endorses, rejects, contests or locks; a steward may do so within an explicit scope. Silence is never acceptance and never consent.
4. **Status has several axes; labels are derived.** Origin, endorsement, epistemic status, admission, freshness and disclosure are kept apart. "Stated", "hypothesis", "stale" and "disputed" are display labels computed from them.
5. **Absence is information, not a value.** Missing data never becomes zero, consent or permission. "Not disclosed" forbids probing. A gap blocks only the actions for which it is critical.
6. **Default deny. Consent to use is not consent to profile.** Nothing leaves the holder without a grant. Any inference about the person, written by anyone other than the person, needs a separate `infer` permission with a named purpose (INF-1, checked from L1). A link is not access, and a grant is not authority to act.
7. **The person's rights outrank append-only.** Correct, contest, export and erase always work. Erasure leaves a tombstone with no content; everything else is append-only.
8. **Many lenses, no master theory.** Frameworks of description are first-class lenses, each with a mental model of working with the person, a toolkit and ways of representation. A lens may be chosen by the person, suggested by an agent, or inherited from the person's therapy, coaching or practice, and it may come with playbooks: ways of using it by situation. A mapping between lenses is a cited population-level claim, never an identity. A non-empirical frame's results stay relative to the frame and are never presented as empirical facts.
9. **Minimal by default, rich by choice; the person's attention is a cost.** One JSON file with a subject and a few claims is a conforming context. Episodes, lenses, the vault, governance and recall are opt-in layers. Describing oneself must stay cheaper than its use.
10. **Say what is not established.** Schema validity is not truth. A grant is not enforcement. A checker never claims runtime behaviour. Examples state that they are synthetic. Recall is not therapy and not crisis support.

## 3. Data model overview

### 3.1. Kinds

OHC 0.1 defines **29 kinds**: 25 normative-draft and 4 experimental. The experimental exchange module additionally defines 16 message formats ([EXCHANGE.md](EXCHANGE.md)).

| # | Kind | Placement | Layer | Module | Maturity | Section |
|---|---|---|---|---|---|---|
| 1 | Context | document | subject | core | normative-draft | §9.1 |
| 2 | Subject | embedded in Context | subject | core | normative-draft | §9.2 |
| 3 | Party | embedded in Context | subject | core | normative-draft | §9.3 |
| 4 | Claim | stored record | assertion | core | normative-draft | §9.4 |
| 5 | Relation | stored record | link | core | normative-draft | §9.5 |
| 6 | Source | stored record | evidence | core | normative-draft | §10.1 |
| 7 | Episode | stored record | experience | core | normative-draft | §10.2 |
| 8 | Interpretation | stored record | interpretation | core | normative-draft | §10.3 |
| 9 | Tension | stored record | interpretation | core | normative-draft | §10.4 |
| 10 | Review | stored record | governance | core | normative-draft | §11.1 |
| 11 | Proposal | stored record | governance | core | normative-draft | §11.2 |
| 12 | Tombstone | stored record | governance | core | normative-draft | §11.3 |
| 13 | Grant | stored record | governance | governance | normative-draft | §12.1 |
| 14 | Event | stored record | governance | governance | normative-draft | §13 |
| 15 | Projection | document | governance | governance | normative-draft | §14.1 |
| 16 | ContextLock | document | governance | governance | normative-draft | §14.2 |
| 17 | Lens | document | registry | lenses | normative-draft shape | LENSES.md |
| 18 | Instrument | document | registry | lenses | normative-draft shape | LENSES.md |
| 19 | Mapping | document | registry | lenses | normative-draft shape | LENSES.md |
| 20 | Playbook | document | registry | lenses | normative-draft shape | LENSES.md §2.2 |
| 21 | LensAdoption | stored record | assertion | lenses | normative-draft | §10.5 |
| 22 | AssessmentRecord | stored record | assertion | lenses | normative-draft | §10.6 |
| 23 | ModelView | stored record | interpretation | lenses | normative-draft | §10.7 |
| 24 | Practice | stored record | assertion | practices | normative-draft | §17.1 |
| 25 | Outcome | stored record | outcome | practices | normative-draft | §17.2 |
| 26 | Pattern | stored record | interpretation | patterns | experimental | §18 |
| 27 | RecallCue | stored record | recall | recall | experimental | §19 |
| 28 | Part | stored record | interpretation | inner-system | experimental | §20 |
| 29 | HealthRef | stored record | assertion | health-ref | experimental | §21 |

That is 7 documents, 2 objects embedded in the Context and 20 stored record kinds. The machine-readable [type catalog](schema/type-catalog.json) gives, for every kind, its layer, module, maturity, collection name, id prefix, schema `$id` and default tier. Layer and module are never stored on records.

### 3.2. Layers and grounding direction

Every kind belongs to exactly one layer. The order follows an experience-first stack. It is conceptual, not a pipeline: links run in both directions only through computed indexes.

| Layer | Kinds |
|---|---|
| `subject` | Subject, Party (embedded in Context) |
| `evidence` | Source |
| `experience` | Episode (with embedded Accounts) |
| `assertion` | Claim, AssessmentRecord, LensAdoption, Practice, HealthRef |
| `interpretation` | Interpretation, ModelView, Tension, Pattern, Part |
| `recall` | RecallCue |
| `outcome` | Outcome |
| `link` | Relation |
| `governance` | Review, Proposal, Grant, Event, Tombstone (plus the documents Projection and ContextLock) |
| `registry` | Lens, Instrument, Mapping, Playbook (shared documents, not about any person) |

- **G1.** Evidence and experience never depend on interpretation. A `Source` MUST NOT reference any record except other Sources (`derivedFrom`, `custody.releaseRef`) and Parties. An `Episode` MUST reference only Sources (evidence spans), Parties and Episodes (`supersedes`). Readings of an episode live in Interpretations that point *at* it; the reverse view ("readings of this episode") is a computed index, never a stored field.
- **G2.** Registries carry no personal data. `Lens`, `Instrument`, `Mapping` and `Playbook` MUST NOT reference any per-person record or contain any person's data.
- **G3.** Governance references; it never copies. `Review`, `Proposal`, `Grant`, `Event` and `Tombstone` hold ids, codes and times only. They never hold record text, values, quotes or content digests. A `Projection` is a disclosure document with its own identity, not a stored record.
  - Four short texts written for the person are the only exception: `Proposal.rationale`, `Review.note`, `Review.endorsedPart` (the person's own words) and `Grant.note`. They MUST NOT quote a record's content or a Source. They are erased together with the records they concern (§15.5, step 2).
- **G4.** Outcome and recall point backwards only. `Outcome` and `RecallCue` MAY reference records of any earlier layer. No record in the evidence, experience or assertion layer may reference an Outcome or a RecallCue.

### 3.3. Two serializations of one data model

**Single-document form.** One file, conventionally `context.json`, with `format: "ohc.context"` and typed record arrays. A person or an agent can write it in minutes.

**Package form.** A directory (layout in §14.3) holding:

- `context.json`: the manifest, with `collections` and no record arrays;
- one JSON Lines file per collection under `records/`;
- `events.jsonl`;
- optional `vault/`, `projections/` and `lenses/`;
- `context.lock.json`.

| Kind | Single-document array | Package file |
|---|---|---|
| Claim | `claims` | `records/claims.jsonl` |
| Relation | `relations` | `records/relations.jsonl` |
| Source | `sources` | `records/sources.jsonl` |
| Episode | `episodes` | `records/episodes.jsonl` |
| Interpretation | `interpretations` | `records/interpretations.jsonl` |
| Tension | `tensions` | `records/tensions.jsonl` |
| Review | `reviews` | `records/reviews.jsonl` |
| Proposal | `proposals` | `records/proposals.jsonl` |
| Grant | `grants` | `records/grants.jsonl` |
| Event | `events` | `events.jsonl` |
| LensAdoption | `lensAdoptions` | `records/lens-adoptions.jsonl` |
| AssessmentRecord | `assessments` | `records/assessments.jsonl` |
| ModelView | `modelViews` | `records/model-views.jsonl` |
| Practice | `practices` | `records/practices.jsonl` |
| Outcome | `outcomes` | `records/outcomes.jsonl` |
| Pattern | `patterns` | `records/patterns.jsonl` |
| RecallCue | `recallCues` | `records/recall-cues.jsonl` |
| Part | `parts` | `records/parts.jsonl` |
| HealthRef | `healthRefs` | `records/health-refs.jsonl` |

Rules for both forms:

- **R-S1.** A package and a single document with the same records are the same context. A converter MUST round-trip between the two forms so that every record and every manifest field is JCS-equal (RFC 8785) before and after.
- **R-S2.** Within a collection, `kind` is implied by the collection name and MAY be omitted. If present, it MUST match. The one exception is a Tombstone (R-S4), which MUST carry `"kind": "Tombstone"`.
- **R-S3.** Records never carry `schemaVersion`. They inherit the enclosing document's `specVersion`, whether that document is a context, a message or a projection.
- **R-S4.** An erased record is replaced in place by its Tombstone: same collection, same position, same id (§11.3).
- **R-S5.** A collection MAY be split across files (for example `records/claims/2026.jsonl`) if `collections` lists every file.

### 3.4. The content-record envelope

**Content records** are the 15 kinds in the evidence, experience, assertion, interpretation, recall, outcome and link layers: Source, Episode; Claim, AssessmentRecord, LensAdoption, Practice, HealthRef; Interpretation, ModelView, Tension, Pattern, Part; RecallCue, Outcome; Relation.

Each content record carries the envelope fields below in addition to its own fields. Governance kinds (Review, Proposal, Grant, Event, Tombstone) have their own small field sets and do **not** carry this envelope.

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `kind` | string | ctx | kind names | Implied by the collection in the single document. |
| `id` | LocalId | yes | — | R-I1. Unique within the context and never reused. |
| `origin` | string | yes | §6.1 | How the content came to be. Set once; never changes (R-O1). |
| `assertedBy` | Actor | yes | §5.4 | Whose statement, reading or record this is. |
| `recordedAt` | DateTime | yes | — | Knowledge time: when it entered **this** context. Import and copy never change it (R-T4). |
| `recordedBy` | Actor | no | — | Who wrote it into the context. Defaults to `assertedBy`. Example: the subject records a coach's reading, so `assertedBy` is the coach's Party and `recordedBy` is `"subject"`. |
| `underGrant` | LocalId | cond | — | The Grant the writer used. REQUIRED under INF-1. |
| `purpose` | string | cond | §8.9 | REQUIRED with `underGrant`. MUST be one of the Grant's purposes. |
| `formulatedAt` | DateTime | no | — | When the content was first formulated. It may be earlier than `recordedAt` (R-T5b). |
| `supersedes` | LocalId | no | — | An earlier record of the **same kind** that this one replaces (R-V2). |
| `epistemic` | string | no | §6.3 | Initial epistemic status. The default depends on origin (§6.1). Later changes are made by Review `reassess`. |
| `confidence` | Confidence | no | §6.3 | A missing confidence is never 0 (R-N2). |
| `sensitivity` | string | no | §8.1 | Default per kind, facet, category and lens (§8.3). Propagation rule C3 applies. |
| `categories` | [string] | no | §8.2 | Sensitive categories this record touches. |
| `handling` | [string] | no | §8.5 | Restrictions that travel with the record. |
| `audience` | string | no | `grantees` \| `named` | `named`: served only to selectors that name the record (R-G3). Default `grantees` for ordinary and personal, `named` for sensitive and special. Never-to-anyone-else is the handling code `person-only`. |
| `contexts` | [string] | no | §9.4.3 life domains | For grant scoping (`work`, `family`, `health` …). |
| `lang` | string | no | BCP 47 | Overrides `Context.lang`. |
| `importedFrom` | ImportedFrom | cond | — | REQUIRED when `origin` is `imported`, and on every record an importer creates. |
| `generatedBy` | GeneratedBy | cond | — | REQUIRED when `origin` is `derived`. |
| `synthetic` | boolean | no | — | X-1. |
| `note` | string | no | — | Free remark by the writer. Never used for inference. |
| `ext` | object | no | §5.7 | Extensions. |

- **INF-1.** A content record whose `recordedBy` (or, by default, `assertedBy`) is neither `"subject"` nor a steward acting within scope MUST carry `underGrant`, naming the Grant the writer used, and `purpose`. That Grant MUST include `suggest` or `write`, and MUST include `infer` when `origin` is `inferred`. The record MUST match the Grant's scope (step 7 of §12.3, applied to the record itself). The check is made at `recordedAt`, and INF-1 is checked from L1.
  - **Steward.** A steward acts within scope when its `scope.actions` contains `write` (and `infer` for `origin: inferred`), the record's kind and facet are in its `scope`, and `recordedAt` lies between `validFrom` and `validUntil`.
  - **Holder.** `"holder"` writes content records only with `origin` `observed`, `derived` or `imported` (for example an import run), and needs no grant for them. It never writes `inferred` records: a holder's own inference is written by its agent Party, under an `infer` grant, like any other agent's (§15.9).
- **R-V2.** Supersession. A record MAY supersede only a record of the same kind. Superseding a record by a different `assertedBy` is itself a proposal. A locked record (§6.2) can be superseded only by the subject. The superseded record stays in the context: it is excluded from "current" views but remains in history and in the as-known-at queries of §7.3. Supersession chains are acyclic.
- **X-1.** In published examples, `synthetic` MUST be `true` on the context and on every content record. Governance records (§3.2) carry no `synthetic` field.
- **RF-1.** Every reference in a content record points at a record of a kind allowed for that field. The matrix `kind.field → allowed target kinds` is published as the catalog [reference-targets](catalogs/reference-targets.json); the "Allowed references" paragraphs of §9–§21 are its prose form. A reference to a tombstoned id is always allowed (TB-2).

The other rules that apply to every content record are R-O1 and R-O2 (§6.1), R-A1 (§6.4), C3 (§8.4) and TP-1 (§8.7).

## 4. Conformance: modules, levels and classes

### 4.1. Modules and maturity

| Module id | Contents | Maturity in 0.1 | Normative home |
|---|---|---|---|
| `core` | `Context` (manifest), `Subject`, `Party`, `Claim`, `Relation`, `Source`, `Episode`, `Interpretation`, `Tension`, `Review`, `Proposal`, `Tombstone`; status axes, time model, freshness algorithm, absence codes, disclosure fields, derived labels, layer rules | normative-draft | this document, §1–§11 |
| `governance` | `Grant`, `Event`, `Projection` (document), `ContextLock` (document); grant evaluation, step-up, erasure, consumer and holder obligations | normative-draft (required at L2) | this document, §12–§16 |
| `lenses` | registry documents `Lens`, `Instrument`, `Mapping`, `Playbook`; per-person `LensAdoption`, `AssessmentRecord`, `ModelView`; lens, mapping and playbook rules | shapes and rules: normative-draft. **Catalog entries: experimental** (each has its own `descriptorStatus`) | [LENSES.md](LENSES.md); per-person records in §10.5–§10.7 |
| `instrument-import` | imported results: AssessmentRecords a person brings from an instrument report, checked against the instrument's `import` block; requires `lenses`. Adds no kind | normative-draft | [INSTRUMENT-IMPORT.md](INSTRUMENT-IMPORT.md) |
| `practices` | `Practice`, `Outcome` | normative-draft | this document, §17 |
| `patterns` | `Pattern` | experimental | this document, §18 |
| `recall` | `RecallCue` | experimental | this document, §19 |
| `inner-system` | `Part`; the `held-by` relation; part-to-part relations | experimental | this document, §20 |
| `health-ref` | `HealthRef` (FHIR pointer only) | experimental | this document, §21 |
| `exchange` | 16 message formats | experimental | [EXCHANGE.md](EXCHANGE.md) |
| `binding.gum` | GUM import and export | normative-draft, for anyone claiming GUM compatibility | [bindings/GUM.md](bindings/GUM.md) |
| `binding.ode` | ODE Tier 0 binding | normative-draft, for anyone claiming ODE binding | [bindings/ODE.md](bindings/ODE.md) |
| `binding.mcp` | MCP tool surface, including the gumcp-compatible tool | experimental | [bindings/MCP.md](bindings/MCP.md) |
| (crosswalks) | JSON-LD, PROV-O, DPV, ODRL, JSContact, VC 2.0, FHIR, HCP (Loyal Agents), GUMO, ISO/IEC TS 27560 and Kantara consent receipts, memory systems | informative | [COMPOSITION.md](COMPOSITION.md), [crosswalks/](crosswalks/) |

Informative: the OHC core is `core` + `governance`; the experiential patterns are `practices` + `patterns` + `recall` + `lenses` (+ `instrument-import`); agent interaction is `exchange` + `binding.mcp`.

**Module ids** (closed): `core`, `governance`, `lenses`, `instrument-import`, `practices`, `patterns`, `recall`, `inner-system`, `health-ref`, `exchange`, `binding.gum`, `binding.ode`, `binding.mcp`.

- **R-M1.** A context MUST list every non-core module it uses in `conformance.modules`. A record whose kind belongs to an undeclared module is a checker error. A conforming reader MAY ignore experimental records. A context MUST stay valid with its experimental records removed.

### 4.2. Conformance levels

| Level | Name | A conforming context MUST contain or satisfy | Typical producer |
|---|---|---|---|
| **L0** | **Minimal** | `format`, `specVersion`, `id`, `version` and `subject.id`.<br>At least one content record to start from (LV-0): a Claim with the six required fields (`id`, `facet`, `text` or `absence`, `origin`, `assertedBy`, `recordedAt`), or an Episode with at least one account.<br>Every code valid against its vocabulary.<br>Absence rule R-B1.<br>**No grant is required. With no grant, nothing is disclosed to anyone but the subject.** | a person by hand, a personal agent, a GUM exporter, an ODE onboarding step |
| **L1** | **Grounded** | L0, plus:<br>- every record with `origin` `inferred` or `derived` cites at least one ground (`evidence`, `grounds` or `derivedFrom`);<br>- every `Source` has `content.sha256`, except `live-feed`;<br>- every `Episode` has at least one account;<br>- supersession chains are acyclic and stay within one kind;<br>- layer rules G1–G4 hold;<br>- every status change is a `Review` whose action is valid for its actor (§11.1), so endorsement and admission history can be reconstructed;<br>- Interpretation rules I1–I10 hold;<br>- inference rule INF-1 holds (records written under a grant cite it);<br>- every reference points at an allowed kind (RF-1). | a reflective personal agent, a journaling app, a lens importer |
| **L2** | **Governed** | L1, plus:<br>- package form with a valid `context.lock.json`;<br>- `events.jsonl` with an unbroken hash chain (redacted stubs allowed, §13.2);<br>- every disclosure has an Event, and every disclosure Event is covered by a Grant (EV-7);<br>- every Grant has `constraints.expiresAt` and `expressedBy`;<br>- every stored Projection is reproducible (its digest matches) and was covered by a Grant whose computed status was `given` at `generatedAt`;<br>- Tombstones are well-formed;<br>- every `source-opened` at verbatim tier is preceded by a `step-up-confirmed` Event (EV-5);<br>- every `record-erased` that reached a recipient is followed by `erasure-notice-sent` (EV-6);<br>- no vault object outlives its Source (V-6). | a holder: the person's own store, a personal agent acting as holder, a context router |

- **LV-0.** A context contains at least one content record to start from: a Claim, or an Episode with at least one account. A person may begin with an experience rather than a statement ([QUICKSTART](../docs/guides/QUICKSTART.md#start-from-an-experience)).
- **R-C1.** A context SHOULD declare `conformance.level`. If it is absent, the checker applies `L0` and reports that it applied the default. The checker verifies the declared level and also reports the highest level actually met.
- **R-C2.** Levels state minimum requirements and never forbid record kinds. A valid record of any declared module may appear at any level. For example, an L0 context may contain an Episode, but the L1 Episode rules are checked only when L1 or higher is claimed.
- **R-C3.** Module claims are additive, for example "OHC L1 + lenses + practices" or "OHC L2 + binding.gum + binding.ode".
- **R-C4.** No context about a child, or about an adult whose decisions are made by a guardian, can claim conformance in 0.1. A context that declares `conformance.level` MUST carry `conformance.subjectIsAdult: true`: the holder's attestation that the subject is an adult who decides for themselves. The checker reports R-C4 when it is missing. Deployments with minors are out of scope in 0.1.

**Weight principle.** The required path is the L0 manifest plus claims. No experimental kind is ever required for any level.

### 4.3. Conformance classes

| Class | Obligations |
|---|---|
| **Writer** | Emits valid records.<br>MUST NOT label an inference `declared` or `observed` (R-O2, I10).<br>Creates records about the subject as `proposed` unless the writer is the subject (R-A1).<br>Cites `underGrant` and `purpose` when it is not the subject (INF-1, checked from L1).<br>MUST NOT reuse a tombstoned id. |
| **Reader / consumer** (for example an agent) | Keeps the consumer obligations C-1…C-12 (§16.1). |
| **Holder** | Keeps the holder obligations H-1…H-17 (§16.2): default deny at serve time, events, tombstones, export, erasure notices, step-up, and the separation of roles when an agent is the holder (§15.9). |
| **Exchange endpoint** | Implements the experimental messages of [EXCHANGE.md](EXCHANGE.md) and writes the Events they require. |

## 5. Conventions

### 5.1. JSON

- Files are UTF-8 RFC 8259 JSON. Duplicate member names MUST be rejected, and so MUST `NaN` and `Infinity`.
- **Member names are ASCII.** OHC's own fields are camelCase. Foreign payloads under `ext` keep their own member names, which MUST also be ASCII. The one exemption is the embedded JSContact card (`Subject.card`): it keeps its own member names, and RFC 9553 allows them to be non-ASCII (for example vendor properties and `keywords` keys). The checker skips `/subject/card` for this rule (J-5).
- Numbers are integers, or decimals exactly representable as IEEE 754 binary64. Writers SHOULD avoid exponents.
- **Canonical form.** Every JSON digest OHC defines uses the RFC 8785 JSON Canonicalization Scheme (JCS): the projection `digest`; the Event `entryDigest` and the `prev` chain; `confirmationDigest`; R-S1 equality; and the pins in the ODE binding. File locks (`context.lock.json`, `release-manifest.json`) hash **file bytes**. Tools MUST implement JCS number serialization per RFC 8785 §3.2.2.3 and ship the RFC's test vectors.
- Schemas use JSON Schema draft 2020-12. The first four members of every schema are `$schema`, `$id`, `title` and `description`, in that order.

### 5.2. Discriminators and versions

| Axis | Value in 0.1 | Where |
|---|---|---|
| Release version | `0.1.0-draft.2` | `release-manifest.json` `releaseVersion`, [CHANGELOG](../CHANGELOG.md) |
| Format / spec version | `0.1.0-draft` | `specVersion` const on every OHC document |
| Record discriminator | `kind` (records carry no `schemaVersion` and no `layer`) | records |
| Document discriminator | `format: "ohc.<artifact>"` (normative) or `"ohc.experimental.<artifact>"` (experimental) | documents and messages |
| Catalogs | own semver `version` plus a pinned `specVersion` | [catalogs/](catalogs/) |
| Lens, Instrument, Mapping | own semver `version`, independent of the framework's own versions | registry ([LENSES.md](LENSES.md)) |
| Procedures | `ID / semver`, for example `CONTEXT-01 / 0.1.0` | [docs/agents/procedures/](../docs/agents/procedures/) |
| Glossary | `version: "0.1"` plus an integer `revision` per term | [glossary.json](glossary.json) |
| Release manifest format | `ohc.public-export/1` | `release-manifest.json` |

- **R-V0.** Readers MUST select schemas by `specVersion` and MUST reject unknown versions. Old formats stay byte-preserved under `spec/versions/<version>/`, which is empty in 0.1. Replacing `specVersion` is not a migration.

### 5.3. Identifiers

- **Schema `$id`:** one scheme, `urn:ohc:schema:<name>:0.1.0-draft`, for example `urn:ohc:schema:claim:0.1.0-draft`. No domain is claimed.
- **Registry ids:** `urn:ohc:lens:<name>`, `urn:ohc:instrument:<name>`, `urn:ohc:mapping:<from>--<to>--<source>`, `urn:ohc:catalog:<name>`. Each also has a separate `version`.
- **Context and subject ids:** a URI the holder controls: `urn:uuid:…` (RECOMMENDED for real holders), a DID, or `urn:ohc:example:<person>[:context]` (examples only).
- **Record ids:** strings unique within a context and never reused, even after erasure.
- **Global form:** `<contextId>#<recordId>`.
- **Cross-context reference:** `{"context": "<contextId>", "id": "<recordId>"}`, optionally with `"contextVersion"`. A cross-context reference is never followed by the checker.
- **Party ids** are local ids with the prefixes `p-` (person), `a-` (agent), `s-` (software or system) and `o-` (organization).

- **R-I1.** Record ids SHOULD match `^[a-z]{1,5}-[0-9a-z-]{1,36}$`: a kind prefix from the table below, then a counter, ULID or UUID. The ids of records whose effective sensitivity is `sensitive` or `special` MUST NOT contain words taken from their content, so that a tombstone cannot reveal what was erased.
- **W-ID1.** The checker warns for every sensitive or special record whose id has more than 4 consecutive letters after the prefix.

| Prefix | Kind | Prefix | Kind |
|---|---|---|---|
| `c-` | Claim | `rv-` | Review |
| `r-` | Relation | `prop-` | Proposal |
| `src-` | Source | `g-` | Grant |
| `ep-` | Episode | `e-` | Event |
| `in-` | Interpretation | `la-` | LensAdoption |
| `t-` | Tension | `as-` | AssessmentRecord |
| `mv-` | ModelView | `pr-` | Practice |
| `oc-` | Outcome | `pat-` | Pattern |
| `rc-` | RecallCue | `part-` | Part |
| `hr-` | HealthRef | `prj-` | Projection |
| `p-`, `a-`, `s-`, `o-` | Party (person, agent, software, organization) | `msg-` | exchange messages |

### 5.4. Actors

Every "who" field (`assertedBy`, `recordedBy`, `by`, `grantor`, `grantee`, `proposer`, `actor`, `narrator` …) holds a string. It is one of:

- `"subject"`: the person the context is about;
- `"holder"`: the context's holder, acting under its declared policy (admission, revocation, retention, quarantine);
- a Party id listed in `Context.parties`. Stewards are Parties named in `Context.stewards`.

Free-text names are labels only; they never identify an actor.

- **R-P2.** A Part (experimental, §20) is never an actor.

### 5.5. Time

- Instants are RFC 3339 date-times with an offset, for example `2026-10-09T08:00:00Z`.
- `YYYY-MM-DD` is used where precision is a day.
- Durations are ISO 8601 (`P3M`, `PT30M`).
- Experience time with partial precision uses `PartialTime` (§5.9).

All time fields are listed in §7.1.

### 5.6. Language

- `Context.lang` (BCP 47) sets the default language, `en` if absent.
- Any record, and any account inside an Episode, MAY override it with `lang`.
- A translation is a separate record of the same kind, linked by a Relation `translation-of`.

### 5.7. Local codes and extensions

- Any controlled vocabulary that is not closed MAY be extended with a code `x-<namespace>:<code>`, defined in `Context.vocabulary`. Readers treat unknown `x-` codes as opaque and never infer from them.
- `ext` is an object whose keys match `^[a-z0-9]+(?:[.-][a-z0-9]+)+$`.
  - Keys defined by OHC: `gum.import`, `gum.export`, `vc.credential`, `jscontact.extra`.
  - Third parties use a reverse-DNS key for a domain they control.
  - Unknown `ext` content MUST be preserved JCS-equal.
- `Context.requiredExtensions` lists `ext` keys a reader must support. A reader that does not support one MUST refuse the context.
- In ODE packages, the extension key OHC defines is `ohc.binding` ([bindings/ODE.md](bindings/ODE.md)).

### 5.8. Privacy in tooling

- Checkers, holders and tools MUST NOT echo field values in error messages or logs. They name the record id, the field path and the rule id, and may add text taken from this specification: the rule's own sentence, where it is defined, and for a schema failure the failing keyword and the schema's property name. An unknown property is reported by its pointer only.
- Checkers never follow external locators.
- Checkers never read vault content. When a vault file is present locally, they compute its sha256, and nothing else.

### 5.9. Shared types

| Type | Shape | Notes |
|---|---|---|
| `LocalId` | string matching `^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$` | The stricter R-I1 pattern is a SHOULD and is checked as warning W-ID1. |
| `Ref` | `LocalId` or `{"context": URI, "id": LocalId, "contextVersion"?: string}` | Cross-context references are never followed. |
| `Actor` | string: `"subject"`, `"holder"`, or a Party id | §5.4 |
| `DateTime` | RFC 3339 date-time with offset | |
| `PartialTime` | `{"start": date \| DateTime, "end"?: date \| DateTime, "precision": "exact" \| "day" \| "month" \| "year" \| "approximate" \| "unknown"}` | Experience time. |
| `Interval` | `{"from"?: date \| DateTime, "until"?: date \| DateTime}` | `until` is exclusive. |
| `Span` | `{"source": LocalId, "selector": Selector}` | Points into a Source. Records never store quoted text or quote digests (R-V1). |
| `Selector` | one of:<br>`{"type": "text-position", "start": int, "end": int}` (Unicode code points, 0-based, end exclusive, over the NFC text);<br>`{"type": "media-time", "start": number, "end": number}` (seconds);<br>`{"type": "page", "page": int, "region"?: {"x", "y", "w", "h"}}` (region as fractions 0..1);<br>`{"type": "whole"}` | Modelled on W3C Web Annotation selectors. The `text-quote` selector exists **only** in served excerpts (§15.3) and is never stored. |
| `Ground` | `{"ref"?: Ref, "span"?: Span, "kind": GroundKind, "note"?: string}`, with exactly one of `ref` and `span` | GroundKind (§10.3.1): `evidence`, `observation`, `sequence`, `pattern`, `instrument`, `testimony`, `practitioner`, `subject-statement` |
| `Alternative` | `{"text": string, "kind": AltKind}` | AltKind (§10.3.1): `psychological`, `situational`, `physiological`, `informational`, `relational`, `external`, `combination`, `other` |
| `Confidence` | `{"value": number 0..1, "semantics": string, "scale"?: string, "raw"?: number, "method"?: string, "calibrationRef"?: string}` | Semantics in §6.3. R-N1: `semantics: probability` requires `calibrationRef`. |
| `ImportedFrom` | `{"system": string, "systemVersion"?: string, "recordId"?: string, "importedAt": DateTime, "run"?: LocalId (Event id), "derivedFields"?: [string]}` | `derivedFields` lists the fields the importer computed rather than copied. |
| `GeneratedBy` | `{"software": string, "version"?: string, "method"?: string}` | |
| `GrantSelector` | `{"all"?: true, "kinds"?: [kind], "facets"?: [facet], "predicates"?: [string], "horizons"?: [horizon], "contexts"?: [domain], "categories"?: [category], "tiers"?: [tier], "lenses"?: [lens id], "ids"?: [LocalId]}` | AND across fields, OR within a field. A selector with `all` and nothing else is the wildcard. |

### 5.10. Controlled vocabularies

Every list in this specification is also published as a catalog under [catalogs/](catalogs/). Each catalog has an `id` (`urn:ohc:catalog:<name>`), a semver `version`, a `specVersion`, a `closed` flag, and codes with `{code, label{en, ru}, definition{en, ru}, notes, mappings}`. Schemas reference the catalogs; enumerations are generated from them and never edited by hand.

- **Closed lists** do not accept `x-` codes. Purposes, prohibited purposes, actions, sensitivity tiers, admission and origin are closed, because their semantics are safety-relevant. Each catalog states whether it is closed.
- **No enum value equals the name of a different field.** This is why the lifecycle axis is called `admission` (not `state`) and the facet is called `declared-value` (not `value`). The horizon value `state` and the facet value `state` are the same concept, content about the person's current condition, and `state` is the only allowed collision. The reference checker's self-test verifies this.

## 6. Status axes and derived labels

A record's status is kept on separate axes: origin, endorsement, epistemic status, admission, freshness and disclosure (§8). Only origin and the initial epistemic status are stored on the record. Endorsement, admission and freshness are **computed**: from Reviews (§11.1), Proposals (§11.2) and time (§7). A display label is derived from the axes (§6.6).

### 6.1. Origin (closed)

How the content came to be.

| Code | Definition | Default epistemic |
|---|---|---|
| `declared` | Stated by `assertedBy` in their own words. This covers the subject's self-statements, a steward's statements within scope, and a party's testimony. | `as-reported` |
| `observed` | Recorded from direct observation of events or behaviour (a calendar, a log, a sensor, an agent noting what happened), without generalisation. | `as-reported` |
| `inferred` | A generalisation, reading or prediction about the person that was neither stated nor directly observed. **Any profiling.** | `hypothesis` |
| `derived` | Computed deterministically from other records by a published rule, for example instrument scoring. Requires `derivedFrom` and `generatedBy.method`. | `as-reported` |
| `imported` | Copied from an external system whose original origin is unknown. When the origin is known, use that origin and add `importedFrom`. | `as-reported` |
| `attested` | Asserted by an issuer through a verifiable credential (`ext["vc.credential"]`). | `as-reported` |

- **R-O1.** `origin` is fixed at writing time and never changes.
- **R-O2.** A writer MUST NOT label an inference `declared` or `observed`. A generalisation about the person that nobody stated and nobody directly observed is `inferred`.
- **R-O3.** The label `stated` is reserved for `declared` content with `assertedBy: "subject"`.

### 6.2. Endorsement (computed)

The person's stance on a record.

| Code | Definition |
|---|---|
| `not-asked` | The person has not taken a stance. This is the initial value when the asserter is not the subject. |
| `endorsed` | The person accepts the record as true or fitting. This is the initial value for the subject's own records. |
| `partial` | The person accepts part of it, in their own words (`endorsedPart`). |
| `rejected` | The person says it is not true or not fitting. The record and its evidence are kept. |

Two flags complete the axis:

| Flag | Meaning |
|---|---|
| `contested` | The person disputes the record and keeps it open for discussion. **Contest is not reject:** contest is open; reject is final for the person. |
| `locked` | The person froze the record. Only the subject may supersede or retract it. Proposals targeting it are declined by the holder. Consumers MUST NOT suggest changes to it. |

- **ST-1.** A steward's endorsement is recorded with `by: <steward id>` and is shown as "confirmed by steward", never "stated". A steward never endorses, rejects or contests beyond the explicit `scope` of its stewardship, and never acts on special-tier or inner-system records.

### 6.3. Epistemic status and confidence

How well-supported the content is.

| Code | Definition |
|---|---|
| `as-reported` | Recorded as its asserter reported it. No further support is claimed. |
| `hypothesis` | A possibility that needs confirmation before use. |
| `supported` | At least one independent ground supports it. |
| `corroborated` | At least two independent grounds support it, from different Sources or Parties. The checker verifies the count. |
| `contradicted` | Grounds exist against it, recorded in `counterEvidence` or by a `contradicts` relation. |
| `frame-relative` | Meaningful only inside a non-empirical or interpretive frame (a symbolic or contemplative lens, or a parts model). **Never presented as an empirical fact**, and neither is anything inferred from it (C-7, AR-4). |

There is no `fact` status. Changes after writing are made with Review `reassess`, by the asserter or the subject.

**Confidence semantics** (`Confidence.semantics`):

| Code | Meaning |
|---|---|
| `support-score` | A heuristic strength of support. Not a probability. |
| `probability` | A calibrated probability. Requires `calibrationRef` (R-N1). |
| `self-rated-certainty` | The person's own certainty. |
| `instrument-reliability` | The reliability of the instrument used, such as α or a retest correlation. |
| `vendor-probability` | A probability reported by a vendor. Calibration unknown. |

- **R-N1.** A Confidence with `semantics: probability` MUST carry `calibrationRef`.
- **R-N2.** A missing confidence is never 0.

### 6.4. Admission (computed; closed)

Whether the record is part of the active context. Admission is a separate axis from endorsement: a record can be admitted and contested at the same time.

| Code | Definition |
|---|---|
| `proposed` | Written by someone other than the subject and not yet decided. Served only to the subject and, as its own proposal, to the proposer (the proposer view, §12.5). |
| `active` | Admitted, or written by the subject. |
| `declined` | Not admitted, including proposals that expired. |
| `retracted` | Withdrawn by the asserter or the subject. Terminal. |

Admission MUST NOT be converted automatically to an ODE definition status. In particular, `active` is not
`agreed`: an admitted record may still be contested or a hypothesis. Preserve the independent endorsement,
epistemic, contested and freshness axes in any permitted representation; see [ODE binding §9](bindings/ODE.md#9-receiver-communication-and-evidence-boundaries).

- **R-A1.** Admission.
  - A content record whose `assertedBy` is not `"subject"` is `proposed` until a Review admits it.
  - These records MUST be admitted by **the subject in person**; neither the holder nor a steward may admit them:
    - any record whose effective sensitivity is `special`;
    - any Part;
    - any Interpretation, Pattern or ModelView with `origin: inferred`;
    - any AssessmentRecord with `mode: agent-inference` or `mode: cross-lens-estimate`;
    - any RecallCue.
  - Other proposed records MAY be admitted by the holder only if `Context.policy.admission` is `holder-may-admit-ordinary` and the record is `ordinary` or `personal`.
  - A holder MAY always decline a proposed record. A decline protects the person; it never admits anything (§11.1).

A proposal that expires undecided is computed `declined` with reason `expired`. That means "not admitted by the person", not "gone": the proposer still sees it in its proposer view (§12.5).

### 6.5. Freshness (computed; never stored)

| Code | Definition |
|---|---|
| `current` | Usable as current. |
| `review-due` | Old enough that a consumer SHOULD ask or refresh before relying on it. |
| `expired` | MUST NOT be used as current. `onExpiry` applies (R-T6). |
| `unknown` | No anchor exists, or the `valueAddress` could not be resolved. Treated like `expired` for action. |
| `historical` | The kind is about the past (Episode, Outcome). Freshness does not apply. |
| `not-applicable` | The kind has no freshness (Relation, Source, governance records). |

The algorithm is in §7.2.

### 6.6. Derived display labels

Every served record has exactly one derived label. The first matching rule wins.

| # | Label | Glyph + word | Rule | ODE `knowledgeOrigin` |
|---|---|---|---|---|
| 0 | `not-accepted` | — not accepted | admission is `declined` or `retracted` | (not served) |
| 1 | `disputed` | ⊘ disputed | endorsement is `rejected`, or `contested` is set | `disputed` |
| 2 | `stale` | ○ stale | freshness is `review-due`, `expired` or `unknown` | `stale` |
| 3 | `pending` | … pending | admission is `proposed` | `hypothesis` |
| 4 | `frame` | ◇ frame | epistemic is `frame-relative` | `hypothesis` (never presented as an empirical fact) |
| 5 | `stated` | ✓ stated | origin is `declared` and assertedBy is `"subject"` | `stated` |
| 6 | `confirmed` | ✓ confirmed | endorsement is `endorsed` (including a steward within scope) | `confirmed` |
| 7 | `partly-confirmed` | ◐ partly confirmed | endorsement is `partial` | `hypothesis` |
| 8 | `attested` | ● attested | origin is `attested` | `observed` |
| 9 | `observed` | ◉ observed | origin is `observed` or `derived`, and endorsement is `not-asked` | `observed` |
| 10 | `hypothesis` | ~ hypothesis | everything else (`inferred`, or `imported` and `not-asked`) | `hypothesis` |

Display rules:

- Labels are always rendered as glyph + word. Colour is never the only carrier (WCAG 2.1 AA).
- Viewers print this table as their legend.
- A steward's endorsement is shown as "confirmed by steward" (ST-1).

### 6.7. Absence

An explicit absence is a Claim with `absence` instead of `text` (§9.4). Its `code` gives the reason for emptiness.

| Code | Definition |
|---|---|
| `unknown` | Nobody knows yet. |
| `not-asked` | The person was never asked. |
| `not-chosen` | The person chose not to define this. With `intentional: true`, it is a protected choice: the right not to set a goal. |
| `sources-diverge` | Sources disagree and the disagreement is not settled. Pair it with a Tension. |
| `not-disclosed` | Exists or may exist, but is not available to this reader. **This is the only code a projection uses**, and it is used regardless of existence (R-G5). |
| `not-applicable` | Does not apply to this person. |
| `not-assessed` | No instrument or method has assessed it. |

- **R-B1.** An absence never becomes zero, false, null, an empty value, an average, a default, consent or permission. A consumer MUST NOT probe a `not-disclosed` (C-8), and MUST NOT infer from the pattern of absences.

## 7. Time model, freshness and temporal queries

### 7.1. Two time axes

**Experience time:** when something was true or happened.

| Field | Kind |
|---|---|
| `valid {from, until}` | Claim |
| `occurred` (PartialTime) | Episode |
| `capturedAt` | Source |
| `administeredAt` | AssessmentRecord |
| `narratedAt` | Account (in an Episode) |
| `firstNoticed` | Part |
| `delivery.at` | Outcome |

**Knowledge time:** when this context learned it.

| Field | Kind | Meaning |
|---|---|---|
| `recordedAt` | all | Entry into this context. |
| `formulatedAt` | content records | First formulation, possibly elsewhere and earlier. |
| `addedAt` | Account | When the account entered. |
| `lastEvidenceAt` | Claim | The newest evidence at writing time. |
| `heldDuring` | Interpretation | When the author held the reading. |
| `recordedAt` | Review | Every status change. |
| `at` | Event | Every disclosure and write. |
| `generatedAt` | Projection | When the projection was computed. |

**Policy fields:** `reviewAfter`, `onExpiry`, `valueAddress {source, field, ttl}`, Grant `constraints.notBefore` and `expiresAt`, `Proposal.expiresAt`, `retention.until`.

- **R-T5b.** Import time rule. The original creation time of imported content goes to `formulatedAt`. The time of import goes to `recordedAt`. Never the reverse.

### 7.2. Freshness algorithm

The algorithm applies to Claim, AssessmentRecord, LensAdoption and Practice. Episodes and Outcomes are `historical`; Relations, Sources and governance records are `not-applicable` (§6.5).

```text
lastConfirmedAt = max(recordedAt of Reviews {confirm-current} on the record), if any
anchor = max(lastConfirmedAt, lastEvidenceAt, recordedAt)   (an imported result: administeredAt instead of recordedAt, IMP-5)
if a Review {mark-not-current} is newer than every confirm-current:  expired
elif valueAddress:  expired if (now - addressedValue.timestamp) > ttl, unknown if unresolvable, else current
elif valid.until and now >= valid.until:                              expired
elif valid.until and not reviewAfter and horizon == state:            current
elif reviewAfter:   review-due if now >= (date | anchor + duration) else current
else:               review-due if now >= anchor + interval[horizon] else current
```

Default intervals:

| Horizon | Interval |
|---|---|
| `state` | P1D (not used while a `state` Claim is inside its `valid` window) |
| `focus` | P90D |
| `foundation` | P2Y |
| none | P1Y |
| AssessmentRecord | the lens `defaults.reviewAfter` (for traits P3Y) |

- **R-T2.** A value held elsewhere (`valueAddress`) is never stored. Its freshness comes from the addressed value's timestamp.
- **R-T3.** Freshness is never stored.
- **R-T4.** Import, restore and copy never change dates.
- **R-T5.** A refresh from a live source is a new superseding record with a new `lastEvidenceAt`, not a Review.
- **R-T6.** `onExpiry` is one of: `treat-as-unknown` (default); `ask` (ask the person); `refresh-source` (re-read the `valueAddress` or the Source).

**Interpretations.** Freshness does not apply to Interpretations. Their derived `heldNow` is `true` while the computed `heldDuring.until` is open (I7).

### 7.3. Temporal queries

These semantics are normative. The reference tool `tools/ohc_query.py` implements them.

- **As valid at T:** records whose `valid` (or `occurred`) contains T, with admission and endorsement computed at now.
- **As known at K:** take only records and Reviews with `recordedAt` ≤ K, and replay. Tombstones apply retroactively: erased content is not reconstructable for any K.
- **As understood at K about episode E** ("how did I understand this three years ago?"): the union of
  - subject Interpretations whose computed `heldDuring` contains K, with `about` ∋ E, known at K;
  - accounts of E whose `addedAt` ≤ K, including `understandingThen`;
  - Interpretations whose `heldDuring` contains the asked-about time, even if they were recorded later.
- **When did my view change:** the supersession chain of subject Interpretations about E, with their `heldDuring` boundaries.
- **Which explanations stopped convincing me:** subject Interpretations with a closed `heldDuring`, or with a subject `reject` or `mark-not-current`.
- **Did my actions change, or only my explanation:** for each episode, compare `didOrTried` across Episodes in time order, against the Interpretations held at each episode's time. A tool shows them side by side and makes no judgement.
- **Which patterns recur across domains:** Patterns with `patternKind: cross-domain`, or Patterns whose episodes have different `contexts`.

## 8. Disclosure

Disclosure is the sixth status axis. It is set by `sensitivity`, `categories`, `handling` and `audience` on content records, changed only by `restrict` and `relax` Reviews, and evaluated against Grants (§12.3).

### 8.1. Sensitivity tiers (closed; ordered)

| Tier | Definition | Grant requirement (R-G3) |
|---|---|---|
| `ordinary` | It would be harmless if anyone knew it. | Any matching selector, including the wildcard. |
| `personal` | About the person, but low-risk. This is the default for Claims. | Any matching selector, including the wildcard. |
| `sensitive` | Could harm, embarrass, or reveal inner life, relationships or location. | A selector naming its kind, facet, category, lens or id. Never the wildcard. |
| `special` | **Treated as special category** (the GDPR Art. 9-like regime). Health, mental health, beliefs, sex life, ethnicity, biometrics and similar, plus psychological lens results, readings from inherited therapy, and parts. | A selector naming its **id, category or lens**, under a grant with `basis.legal: explicit-consent`. Never kind or facet alone. |

**Wording rule.** A record with tier `special`, or with a category whose minimum tier is `special`, is "treated as special category". Documentation never says that a record "is Art. 9 data".

### 8.2. Categories

The list is closed, with `x-` extension.

| Code | Definition | Minimum tier |
|---|---|---|
| `health` | Physical health, conditions, treatments, sleep and energy where health-related | special |
| `mental-health` | Mental health, psychological states and readings, psychological lens results | special |
| `belief` | Religious or philosophical beliefs, spiritual practice | special |
| `political` | Political opinions or affiliations | special |
| `sex-life` | Sex life or sexual orientation | special |
| `ethnicity` | Racial or ethnic origin | special |
| `biometric` | Biometric data (face, voice, physiology) | special |
| `genetic` | Genetic data | special |
| `trade-union` | Trade-union membership | special |
| `criminal` | Criminal convictions or offences (Art. 10-like) | special |
| `trauma-adjacent` | Material touching trauma, exiles and burdens (parts models), abuse | special |
| `intimate` | Intimate relationships, attachment results | special |
| `birth-data` | Date, time and place of birth (an identification risk; astrology inputs) | sensitive |
| `financial` | Income, debt, money worries | sensitive |
| `location` | Home, regular places, live location | sensitive |
| `third-party` | Content about identifiable other people | sensitive |
| `identity-linking` | Links to accounts, real names and identifiers | sensitive |
| `workplace` | Employer, performance context, workplace conflicts | personal |

### 8.3. Default tiers by kind

Defaults apply before propagation (§8.4).

| Kind | Default | Raised to `special` when |
|---|---|---|
| Claim | personal | facet `belief`; facet `state` with predicate `mood`, `emotion`, `stress` or `affect`; any special category |
| Claim facets `declared-value`, `relationship`, `disposition`, `need` | sensitive | any special category |
| Source | the `defaultTier` of its `sourceKind` in [source-kinds](catalogs/source-kinds.json): `sensitive` for most kinds, so that a wildcard selector never reaches primary material | `audio`, `video`, `voice`, `sensor`, `biometric` and `practitioner-notes` default to special; custody confidentiality not `none` raises any Source to special |
| Episode | sensitive | any special category |
| Interpretation | sensitive | a `lens` is present, `about` includes a Part, or the adoption's confidentiality is not `none` (I9) |
| Tension | maximum over `between` | — |
| Pattern | sensitive | a `lens` is present |
| ModelView, AssessmentRecord, Part, HealthRef | **special** | — |
| LensAdoption | sensitive | route is `inherited-from-practice`, confidentiality is not `none`, or the lens default is special |
| Practice | personal | — |
| Outcome | the tier of its `about` target | — |
| RecallCue | sensitive | any target is special (and then RC-2 applies) |
| Relation | maximum of `from` and `to` | — |

Lens descriptors (`defaults` in [LENSES.md](LENSES.md)) may raise these tiers, never lower them. Only the subject may lower a tier, and only with a `relax` Review.

### 8.4. Tier propagation

- **C3.** Tier propagation.
  - A record's effective tier is the maximum of: its stored `sensitivity`; the default for its kind; the minimum tier of its categories (§8.2); its lens default; and the effective tiers of every record it cites through `about`, `grounds`, `counterEvidence`, `evidence`, `derivedFrom`, `between`, `episodes`, `hypotheses`, `targets` and `scope`.
  - Effective categories are the union along the same edges.
  - Propagation follows citations only. It never runs along a Relation's endpoints, except for the Relation record itself.
  - Only the subject can lower an effective tier, with a `relax` Review (§11.1). Even then, the category naming rule R-G3(b) still applies.

### 8.5. Handling restrictions (closed)

Each code is an obligation on every holder and consumer.

| Code | Definition |
|---|---|
| `no-quote` | Never reproduce the record's text or its sources verbatim to anyone but the subject. Paraphrase only. |
| `no-quote-back` | Never present this record, or the profile it belongs to, back to the subject as an argument, authority or proof (for example 'according to your profile…'). Use it as background only; the person's own words in the present conversation take precedence. |
| `no-infer` | Never use as an input to inference, mapping, pattern finding or model training. |
| `no-remember` | A consumer MUST NOT keep it beyond the current use, whatever `storage` says. |
| `no-leverage` | Never use it to persuade, pressure, negotiate against or steer the person. |
| `no-forward` | Never pass it to anyone else, including other agents of the same operator. |
| `person-only` | Never served or used for any grantee, including in answers. Only the subject sees it. |
| `ask-before-use` | Every use needs a fresh confirmation from the subject (the step-up channel, without verbatim). |
| `subject-initiated-only` | Use only inside an interaction the subject started. Never proactively. |

The holder enforces handling at projection time (§12.3) and copies every served record's codes into `obligations.handling` (§14.1). Consumers keep it (C-4, C-6).

### 8.6. Audience

`audience` is `grantees` (default for ordinary and personal records) or `named` (default for sensitive and special records). A `named` record is served only to selectors that name it (R-G3(a)). Never-to-anyone-else is not an audience; it is the handling code `person-only`.

### 8.7. Third parties

- **TP-1.** Third parties.
  - No record may describe a third party's inner states, traits, health or beliefs.
  - A Party may be the counterpart of a relationship or commitment (`about`), a participant, a narrator, an author or a grantee. It is never the subject of a facet, interpretation, pattern or part.
  - Enforcement: `about` → Party is allowed only on Claims with facet `relationship`, `commitment`, `boundary`, `preference` or `goal`. No other kind has a field that can point an assertion at a Party.

### 8.8. Affect quarantine and the emotion-inference ban

- **R-X3.** Quarantine.
  - Applies to any record with predicate `mood`, `emotion`, `stress` or `affect`, and to any imported proposition about affect, mood, stress or mental condition, unless the subject declared it.
  - Treatment: tier `special`; categories ⊇ `["mental-health"]`; handling ⊇ `["no-infer", "person-only"]`.
  - Effect: it is shown only to the subject and never served in work or education contexts.
  - A result of a self-report instrument that the subject took counts as declared here, its emotion or affect scales included, whether it is recorded with mode `self-report-instrument` or `vendor-report-import`. It is not quarantined and keeps its ordinary tier (`special`, AR-5).
- **R-X4.** No record may hold an emotion, mood, stress or affect value derived from biometric or behavioural signals (voice, face, physiology, keystrokes, gaze, mouse or screen behaviour), **whatever the method label, facet or predicate says**.
  - Behavioural signals are Sources whose `sourceKind` is flagged `biometricOrBehavioural` in [source-kinds](catalogs/source-kinds.json): `audio`, `video`, `image`, `screen-observation`, `sensor`, `biometric`, `voice` and `keystroke`.
  - Grounding is followed transitively: through `evidence`, `grounds`, `derivedFrom`, the evidence of Episode accounts and an AssessmentRecord's `source`.
  - Such content is refused, not quarantined. An importer drops it (for GUM, [bindings/GUM.md](bindings/GUM.md)), and a holder refuses it at write (H-10). Rule CL-4 checks it.

The legal context of both rules is recorded informatively in [COMPOSITION.md](COMPOSITION.md#legal-hooks).

### 8.9. Purposes (closed)

Purposes are shared by Grants and the ODE binding. Every request carries exactly one purpose (R-G7).

| Code | Definition |
|---|---|
| `self-reflection` | Helping the person understand their own experience, at their request. |
| `assist-personal` | General personal assistance chosen by the person. |
| `work-collaboration` | Working with the person on work tasks in the person's role. |
| `scheduling` | Arranging the person's own time, at their request. |
| `task-execution` | Carrying out a task the person delegated. |
| `communication-adaptation` | Adapting tone, channel, timing and format to the person. |
| `recall-support` | Offering back the person's own experience under RecallCues. |
| `coaching` | A coaching relationship the person chose. |
| `therapy-support` | Supporting a therapy the person is in. Never clinical decisions. |
| `learning-support` | Supporting the person's learning. |
| `health-coordination` | Scheduling and coordination around care. **Pointers only.** |
| `research` | Research the person explicitly joined. |
| `service-provision` | Providing a service the person signed up for, as described in the grant note. |
| `backup` | Keeping a backup copy for the person. |
| `gum-export` | Exporting to a GUM-compatible store ([bindings/GUM.md](bindings/GUM.md)). |
| `profiling` | Building or maintaining a model of the person's characteristics for the grantee's service to the person. Requires `infer` and `explicit-consent`. |

The alignment of these purposes with DPV concepts is informative and recorded in [COMPOSITION.md](COMPOSITION.md).

### 8.10. Prohibited purposes (closed)

No grant opens these purposes, for any grantee, the person's own agent included. These are uses by others, or for others' decisions, about the person. The person's own choices, made with their own agent (which role to take, which offer to accept, how their week went), are not among them; what the agent may weigh in proposing one is set by `decisionUse` (R-G14).

| Code | Definition |
|---|---|
| `personnel-selection` | An organisation or another person hiring or screening the person, or choosing between them and other candidates. |
| `task-allocation` | An organisation allocating work among people on the basis of their traits, states or behaviour (AI Act Annex III 4(b)). This is different from `scheduling` the person's own time. |
| `performance-evaluation` | An organisation or another person evaluating the person's work performance. |
| `promotion-decision` | An organisation's decision to promote, demote or dismiss the person. |
| `cross-person-ranking` | Comparing or ranking this person against others. |
| `persuasion-targeting` | Tailoring persuasion to the person's psychology. |
| `advertising` | Advertising or marketing targeting. |
| `political-profiling` | Inferring or targeting political views. |
| `credit-or-insurance-decision` | A lender's or insurer's decision on the person's creditworthiness, insurance or price. |
| `emotion-recognition-at-work-or-education` | Inferring emotions in workplace or education settings (AI Act Art. 5(1)(f) context; R-X3 governs affect content in OHC). |
| `model-training` | Training or fine-tuning any model that serves anyone other than this person. |
| `sale-or-transfer` | Selling, licensing or transferring the data. |
| `significant-automated-decision` | Decisions with legal or similarly significant effect without human involvement (GDPR Art. 22-like). |

What a grantee may decide for the person on the basis of results and readings is set by the grant's `decisionUse` (R-G14).

## 9. Context, Subject, Party, Claim, Relation

### 9.1. Context (manifest)

Layer `subject` · module `core` · normative-draft. The root document of a context. It names the subject, the parties, the stewards and the holder, the declared conformance and the record collections.

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `format` | const `"ohc.context"` | yes | — | |
| `specVersion` | const `"0.1.0-draft"` | yes | — | R-V0 |
| `id` | URI | yes | — | §5.3 |
| `version` | string | yes | — | Chosen by the holder. Changes with every change set, for example `"2026-10-09.1"`. |
| `subject` | Subject | yes | — | §9.2 |
| `holder` | Actor | no | — | Default `"subject"`. A personal agent acting as holder is a Party. |
| `parties` | [Party] | cond | — | REQUIRED if any Party id is referenced anywhere. |
| `stewards` | [Steward] | no | — | `{"party": LocalId, "scope": {"kinds"?: [kind], "facets"?: [facet], "actions": [ReviewAction \| "write" \| "infer" \| "grant" \| "open-verbatim"]}, "basis": "delegated-by-subject" \| "power-of-attorney", "validFrom": DateTime, "validUntil": DateTime, "expressedBy": {"actor": "subject", "at": DateTime, "channel": Channel}}`. Stewards never act on special-tier or inner-system records (R-A1) and never endorse beyond scope (ST-1). |
| `conformance` | `{"level": "L0" \| "L1" \| "L2", "modules"?: [module id], "subjectIsAdult"?: true}` | no | §4.1 | R-C1. Default `L0`, `["core"]`. `subjectIsAdult: true` is REQUIRED when `level` is present (R-C4). |
| `lang` | BCP 47 | no | — | Default `en`. |
| `created` | DateTime | no | — | |
| `policy` | `{"admission"?: "subject-only" \| "holder-may-admit-ordinary", "retention"?: {"sourcesDefault"?: Duration}, "resolver"?: Resolver}` | no | §12.2 | Default admission `subject-only`. Default resolver `returnDialog`. |
| `lenses` | [`{"id": URI, "version": string, "sha256"?: string, "descriptor"?: Lens}`] | no | — | Pins the lens descriptor versions this context uses. A single document MAY carry a local descriptor inline (`descriptor`); a package ships it in `lenses/` ([LENSES.md](LENSES.md) §5.1). A pin that resolves to no descriptor is treated as a stub (LA-6, W-LA6). |
| `playbooks` | [`{"id": URI, "version": string, "sha256"?: string, "playbook"?: Playbook}`] | no | — | Pins the playbooks this context uses, in the shape of `lenses`. A local playbook from practice (`urn:ohc:playbook:x-…`) travels inline (`playbook`) in a single document and in `lenses/` in a package; a registry playbook is pinned the same way ([LENSES.md](LENSES.md) §2.2). A pin that resolves to no playbook is left out of the agent rendering (W-PB5). |
| `vocabulary` | object `code → {"definition": string, "broader"?: code}` | no | — | Definitions for `x-` codes. |
| `requiredExtensions` | [string] | no | — | §5.7 |
| `collections` | object `name → path \| [path]` | cond | — | Package form only. Paths are relative: no leading `/`, no `\`, no `..`, no `:`. |
| `claims`, `relations`, `sources`, `episodes`, `interpretations`, `tensions`, `reviews`, `proposals`, `grants`, `events`, `lensAdoptions`, `assessments`, `modelViews`, `practices`, `outcomes`, `patterns`, `recallCues`, `parts`, `healthRefs` | arrays of the matching kind | no | — | Single-document form only. They MUST NOT appear together with `collections`. |
| `synthetic` | boolean | no | — | MUST be `true` in examples (X-1). |
| `ext` | object | no | — | |

**Allowed references.** Party ids, through `holder` and `stewards`.

**Invariants.**

- **CX-1.** `format` and `specVersion` are known.
- **CX-2.** The document has either `collections` or record arrays, never both.
- **CX-3.** Every Party id referenced anywhere is listed in `parties`.
- **CX-4.** Ids are unique across all collections.
- **CX-5.** Every declared module covers the kinds present (R-M1).
- **CX-6.** The `version` string is non-empty.
- **CX-7.** No `stewards[].basis` is `guardianship` (R-C4).
- **CX-8.** In example files, `synthetic` is true on the context and on every content record (X-1).

**Example** (the Noa manifest as a single-document L1 illustration, with the record arrays left empty; the published Noa example is an L2 package):

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft", "id": "urn:ohc:example:noa:context",
 "version": "2026-10-09.4", "subject": {"id": "urn:ohc:example:noa", "displayName": "Noa (fictional)"},
 "holder": "subject", "lang": "en", "created": "2026-03-12T18:45:00Z",
 "conformance": {"level": "L1", "modules": ["core", "lenses", "practices", "patterns", "recall", "inner-system"],
                 "subjectIsAdult": true},
 "parties": [
   {"id": "p-01", "partyKind": "person", "label": "Supplier contact", "role": "supplier"},
   {"id": "p-02", "partyKind": "person", "label": "Coach", "role": "practitioner"},
   {"id": "a-01", "partyKind": "agent", "label": "Work assistant"},
   {"id": "a-02", "partyKind": "agent", "label": "Reflection companion"},
   {"id": "s-01", "partyKind": "software", "label": "Calendar export"},
   {"id": "s-02", "partyKind": "software", "label": "Former journaling app"},
   {"id": "o-01", "partyKind": "organization", "label": "Physio clinic"}],
 "policy": {"admission": "subject-only", "resolver": "returnDialog"},
 "lenses": [
   {"id": "urn:ohc:lens:cbt", "version": "0.2.0",
    "sha256": "a874745345edb48d824d35a3ae23cebaa3be8380dc2f6c165abbf1b5baf8a06a"},
   {"id": "urn:ohc:lens:ifs", "version": "0.2.0",
    "sha256": "6a0a5ea1fcc666659a29676679b32b788632dd9967d1ee2bef13bedad7ced09d"}],
 "claims": [], "episodes": [], "interpretations": [], "sources": [], "reviews": [], "grants": [], "synthetic": true}
```

### 9.2. Subject

Embedded in Context · module `core` · normative-draft. Identifies the person the context is about. It holds the minimum needed for identity, and nothing that belongs in claims.

| Field | Type | Req | Notes |
|---|---|---|---|
| `id` | URI | yes | Stable for this context. It is never sent to grantees, who get a pairwise alias instead (§12.3, step 11). |
| `displayName` | string | no | Examples MUST add "(fictional)". |
| `card` | object | no | A JSContact Card (RFC 9553), copied verbatim with its own member names (§5.1). Category `identity-linking`. Served only to a selector that names `identity-linking`. |
| `links` | [`{"rel": "same-as" \| "account" \| "did" \| "ode-party", "uri": URI, "odeRef"?: {"objectId": string, "version": string}}`] | no | Category `identity-linking`. A link is not access: a link to an ODE Party grants nothing (R-L0). |
| `aliases` | [`{"grantee": Actor, "alias": URI, "createdAt": DateTime}`] | no | An optional stored record of the pairwise aliases issued. Derivation: §12.3, step 11. |

**Invariants.**

- **SJ-1.** `id` is present.
- **SJ-2.** `card` validates against the bundled JSContact Card member list (only the `@type` and `version` members are checked).
- **SJ-3.** Aliases are unique per grantee.

**Example** (Noa's subject).

```json
{"id": "urn:ohc:example:noa", "displayName": "Noa (fictional)",
 "links": [{"rel": "account", "uri": "urn:ohc:example:noa:workshop-account"}],
 "aliases": [
   {"grantee": "s-02", "alias": "urn:ohc:alias:qagnd25qslce5ldesu324xahgn", "createdAt": "2026-04-02T08:00:00Z"},
   {"grantee": "a-01", "alias": "urn:ohc:alias:cgkknm2urepzjn6a6qmvpmz5yc", "createdAt": "2026-09-03T08:00:00Z"},
   {"grantee": "a-02", "alias": "urn:ohc:alias:xdtpvlyqbwczwjs3tztanuegrv", "createdAt": "2026-09-24T07:30:00Z"}]}
```

### 9.3. Party

Embedded in Context · module `core` · normative-draft. Anyone, other than the subject, who asserts, narrates, receives, holds or appears in the context: people, agents, software and organizations. Parts are never Parties (P-1).

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `id` | LocalId | yes | prefix `p-`, `a-`, `s-` or `o-` (§5.3) | |
| `partyKind` | string | yes | `person`, `agent`, `software`, `organization` | |
| `label` | string | yes | — | Pseudonymous wherever possible. Examples use role labels only. |
| `role` | string | no | relationship kinds (§9.4.3), plus `practitioner` | |
| `odeRef` | `{"objectId": string, "version": string}` | no | — | The ODE Party, Agent or DigitalEmployee this party explicitly corresponds to. Not authentication or access; a role or working-configuration change does not transfer a grant (ODE binding §9). |
| `uri` | URI | no | — | A DID or service URI. |
| `ext` | object | no | — | |

**Invariants.**

- **PA-1.** The id prefix matches `partyKind`.
- **PA-2.** No Party id equals a Part id.
- **PA-3.** In examples, a label matches the role-label pattern and never a personal name. This is a heuristic warning.

**Example** (Kofi's planner, an ODE digital employee).

```json
{"id": "a-01", "partyKind": "agent", "label": "Planner",
 "odeRef": {"objectId": "urn:ode:example:employee:planner", "version": "0.2.0"}}
```

### 9.4. Claim

Layer `assertion` · module `core` · normative-draft. One statement about the person in the present tense of its validity interval: identity, roles, goals, needs, values, boundaries, preferences, capabilities, resources, states, relationships, commitments, beliefs, or an explicit absence of any of these. Claims are what most consumers read. **A Claim never carries an interpretation:** readings live in Interpretation, Pattern and ModelView, which are separate kinds.

#### 9.4.1. Fields

The envelope (§3.4), plus:

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `facet` | string | yes | §9.4.2 | What kind of statement this is. |
| `predicate` | string | no | §9.4.2 (per facet) | A finer code within the facet, from the facet's closed list or an `x-` code defined in `Context.vocabulary`. When unsure, leave it out. |
| `text` | string | cond | — | Exactly one of `text` and `absence` (CL-1). Kept in the asserter's words. |
| `absence` | `{"code": string, "intentional"?: boolean, "note"?: string}` | cond | §6.7 | Never together with `value` or `valueAddress` (CL-2). `intentional: true` is allowed only with `not-chosen` and only when the asserter is the subject (CL-9; the right not to define). |
| `horizon` | string | no | §9.4.3 | `foundation`, `focus` or `state`. |
| `value` | any JSON | no | — | A machine value, if useful. Readers MUST NOT assume a structure without `unit` or documentation. MUST be absent when `valueAddress` is present (CL-7). |
| `unit` | string | no | UCUM or free text | |
| `valid` | Interval | no | — | Experience time: when the content is true or applies. |
| `lastEvidenceAt` | DateTime | no | — | The newest evidence at writing time. A refresh from a live source is a new superseding record, not a Review (R-T5). |
| `reviewAfter` | Duration or date | no | — | Overrides the horizon interval used by the freshness algorithm (§7.2). |
| `onExpiry` | string | no | `treat-as-unknown` (default), `ask`, `refresh-source` | R-T6 |
| `valueAddress` | `{"source": Ref \| URI, "field": string, "ttl": Duration}` | no | — | A live value held elsewhere. Freshness comes from the addressed value's own timestamp (R-T2). |
| `about` | LocalId (Party) | no | — | The counterpart. Allowed only with facets `relationship`, `commitment`, `boundary`, `preference` and `goal` (TP-1). |
| `evidence` | [Ground] | cond | — | REQUIRED at L1 when `origin` is `inferred` or `derived`. |
| `derivedFrom` | [Ref] | cond | — | REQUIRED when `origin` is `derived`, for example from an AssessmentRecord. |
| `rationale` | string | no | — | Why the asserter holds this. |

**Allowed references.** `about` → Party. `evidence` → Source spans, Episodes, Claims, AssessmentRecords. `derivedFrom` → Claims, AssessmentRecords, Sources. `supersedes` → Claim. `underGrant` → Grant. A Claim never rests on an interpretation-layer record: a statement drawn from a reading is itself an inference and cites the reading's own grounds (RF-1).

#### 9.4.2. Facets, families and predicates

Facet codes are flat and grouped into families. The facet list is closed. Predicates are optional finer codes; the list is closed per facet, with `x-` extension allowed.

| Family | Facet | Definition | Predicates |
|---|---|---|---|
| identity | `identity` | How the person names themselves; self-description | `name-use`, `pronouns`, `self-description`, `language` |
| identity | `role` | Roles held (work, family, community) | `work-role`, `family-role`, `community-role` |
| identity | `fact` | Plain facts about the person | `birth-data`, `residence-area`, `education`, `credential` |
| identity | `disposition` | Stable tendencies, **declared by the person or derived from an AssessmentRecord** (CL-3) | `self-described-tendency`, `assessed-trait` |
| aspiration | `goal` | What the person wants to achieve | `outcome`, `habit`, `career`, `learning`, `relationship` |
| aspiration | `interest` | What attracts the person's attention | `topic`, `activity` |
| aspiration | `need` | What keeps the person well, whatever they want | `rest`, `support`, `autonomy`, `structure`, `connection` |
| orientation | `declared-value` | What matters to the person, in their words | `principle`, `priority` |
| orientation | `boundary` | What the person will not do or accept, and conditions on contact | `never`, `only-if`, `ask-first`, `time-window` |
| orientation | `belief` | Beliefs the person holds about the world or themselves (special by default) | `worldview`, `spiritual`, `self-belief` |
| interaction | `preference` | How the person likes to be worked with | `channel`, `timing`, `tone`, `detail-level`, `format`, `decision-brief`, `pushback` |
| capacity | `capability` | Skills and abilities | `skill`, `language-skill`, `tool-skill` |
| capacity | `resource` | What the person has or lacks | `time`, `attention`, `energy`, `money`, `tools`, `network` |
| capacity | `state` | The current condition | `energy`, `attention`, `availability`, `load`, `location-status`, `mood`, `emotion`, `stress`, `affect` |
| social | `relationship` | A relationship with a Party (`about`) | the relationship kinds of §9.4.3 |
| social | `commitment` | Something promised to someone, or by someone (`about`) | `promise`, `agreement`, `deadline` |
| other | `other` | Anything else. GUM imports start here. | — |

Parts, practices, outcomes and recall cues are kinds, not facets.

#### 9.4.3. Horizons, life domains and relationship kinds

**Horizons** (closed):

| Code | Definition | Default freshness interval |
|---|---|---|
| `foundation` | Changes over years: values, life direction, "who I am". | P2Y |
| `focus` | Changes over months: the current chapter, projects, period commitments. | P90D |
| `state` | Changes over hours or days: energy, attention, availability. | P1D |

Informative mapping to ODE lifecycles: stable → `foundation`; agreement → `commitment` or `boundary` plus a Grant; live → `state` plus `valid.until` or `valueAddress`; history → Episodes, superseded records and Events; derived → origin `derived`; reference → Source or `valueAddress`; metadata → envelope fields.

**Life domains** (`contexts`; open list with `x-`): `work`, `family`, `partner`, `friends`, `health`, `learning`, `money`, `home`, `community`, `spiritual`, `creative`, `personal-practice`, `therapy`, `coaching`.

**Relationship kinds** (`relationship` predicates, Party `role`, `raterRelationship`; open list with `x-`): `partner`, `family`, `friend`, `colleague`, `manager`, `report`, `client`, `supplier`, `practitioner`, `mentor`, `teacher`, `community`, `other`.

#### 9.4.4. Invariants

- **CL-1.** Exactly one of `text` and `absence`.
- **CL-2.** `absence` never appears with `value` or `valueAddress`, and no `value` of `null`, `false`, `""`, `{}`, `[]` or a unitless `0` stands in for an absence (R-B1).
- **CL-3.** Facet `disposition` requires `origin` `declared` (by the subject) or `derived` (from an AssessmentRecord). Dispositions inferred by an agent are not Claims; they are AssessmentRecords with `mode: agent-inference` (AR-2).
- **CL-4.** Affect (R-X3, R-X4), independent of facet and method labels.
  - A record is **affect-bearing** when its predicate is `mood`, `emotion`, `stress` or `affect`, or an `x-` code whose `broader` chain in `Context.vocabulary` reaches one of them, or when it carries the R-X3 quarantine. An affect-bearing Claim requires `origin: declared` with `assertedBy: "subject"`, or the quarantine (handling ⊇ `["no-infer", "person-only"]`, categories ⊇ `["mental-health"]`, tier `special`).
  - It is an **error** for a record with `origin` `observed`, `inferred` or `derived` that rests, directly or transitively (R-X4), on a behavioural Source to be affect-bearing, or to have text that the affect classifier reads as affect. When unsure, the classifier says affect.
  - A Claim with facet `state` that rests on a behavioural Source MUST carry a non-affect predicate: `availability` or `load`.
- **CL-5.** A Claim with horizon `state` and without `valid.until`, `valueAddress` or `reviewAfter` uses the default interval P1D. The checker reports it as warning W-CL5. A `state` Claim with `valid.until` is current inside its window and expired after it (§7.2).
- **W-CL5.** Warning: a `state`-horizon Claim relies on the default freshness interval (CL-5).
- **W-CL4.** Warning: a record that the subject did not declare, that is not quarantined and that rests on no behavioural Source has text the affect classifier reads as affect. Consider the R-X3 quarantine.
- **CL-6.** `about` is used only with the allowed facets (TP-1).
- **CL-7.** `value` and `valueAddress` are mutually exclusive.
- **CL-8.** `predicate` belongs to the facet's predicate list, or is an `x-` code. It is checked only when the facet itself is known.
- **CL-9.** `absence.intentional: true` appears only with `absence.code: not-chosen`, and only when `assertedBy` is `"subject"`.

INF-1, R-V2 and C3 apply as defined in §3.4 and §8.4.

#### 9.4.5. Examples

Noa's goal is declared. The second Claim is an inferred preference, written by a reflection companion under grant `g-02` and contested by Noa in `rv-01`. The third is an intentional absence.

```json
{"id": "c-02", "facet": "goal", "text": "Renegotiate the supplier contract before the end of Q4 2026.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-02T08:10:00Z", "horizon": "focus",
 "valid": {"until": "2027-01-01"}, "contexts": ["work"], "synthetic": true}
```

```json
{"id": "c-09", "facet": "preference", "predicate": "timing",
 "text": "Tends to move supplier calls to the end of the week.", "origin": "inferred", "assertedBy": "a-02",
 "recordedAt": "2026-09-20T10:00:00Z", "underGrant": "g-02", "purpose": "self-reflection", "epistemic": "hypothesis",
 "confidence": {"value": 0.4, "semantics": "support-score", "method": "count of moved events, 2026-03..09"},
 "evidence": [{"span": {"source": "src-02", "selector": {"type": "whole"}}, "kind": "observation"}],
 "contexts": ["work"], "synthetic": true}
```

```json
{"id": "c-10", "facet": "goal", "predicate": "career",
 "absence": {"code": "not-chosen", "intentional": true, "note": "Not setting a career goal for 2027 yet."},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-25T19:00:00Z", "horizon": "focus",
 "synthetic": true}
```

### 9.5. Relation

Layer `link` · module `core` · normative-draft. A typed link between two records: support, contradiction, alternatives, same occurrence, conditions, practices for goals, translations, resource competition, and part relations. A conflict that the person needs to work on is a **Tension** (§10.4), not just a `contradicts` relation.

The envelope (§3.4), plus:

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `rel` | string | yes | below | |
| `from` | Ref | yes | — | |
| `to` | Ref | yes | — | |
| `strength` | number 0..1 | no | — | Only with `supports` or `contradicts`. Semantics are the asserter's. |

**Relation codes** (closed):

| Code | From → To | Definition |
|---|---|---|
| `supports` | any content → any content | `from` supports `to`. |
| `contradicts` | any content → any content | `from` speaks against `to`. Lightweight; use a Tension when someone needs to decide. |
| `refines` | Claim → Claim | `from` narrows `to` without replacing it. |
| `depends-on` | Claim → Claim | `from` holds only if `to` holds. |
| `alternative-to` | Interpretation → Interpretation; ModelView → ModelView | Competing readings, kept side by side. |
| `same-occurrence` | Episode → Episode | Two Episodes describe one occurrence (for example, recorded by different holders). |
| `conditioned-by` | Claim or Practice → Claim | Applies only under the condition `to`. |
| `practice-for` | Practice → Claim (goal, need, state) or Pattern | The practice serves that goal or situation. |
| `translation-of` | X → X (same kind) | A language version (§5.6). |
| `competes-for-resource` | Claim (goal or commitment) → Claim (goal or commitment) | Both draw on the same resource. |
| `held-by` | Claim or Interpretation → Part | This content is voiced by this part (`inner-system` module). |
| `protects` | Part → Part | Part relation (`inner-system` module). |
| `polarized-with` | Part → Part | Part relation (`inner-system` module). |
| `allied-with` | Part → Part | Part relation (`inner-system` module). |

**Allowed references.** The endpoint kinds per `rel` are in the table above. Relations never point at governance records.

**Invariants.**

- **RL-1.** `from` and `to` resolve. A tombstoned endpoint makes the Relation inert; it is still valid.
- **RL-2.** The endpoint kinds are allowed for `rel`.
- **RL-3.** Part relations require the `inner-system` module.
- **RL-4.** `from` ≠ `to`.
- **RL-5.** A Relation never makes a record reachable. Grant evaluation ignores Relations (R-L0).

**Example.**

```json
{"id": "r-01", "rel": "same-occurrence", "from": "ep-04", "to": "ep-01", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-09-19T20:05:00Z", "synthetic": true}
```

## 10. Source, Episode, Interpretation, Tension

### 10.1. Source

Layer `evidence` · module `core` · normative-draft. Metadata for one piece of primary material in the vault: a journal note, a message, a transcript, a calendar export, a recording, a scanned page, an instrument report, or a practitioner's release. The bytes live in the vault, addressed by `sha256`, and are released by tier (§15.3). Sources make "return to the original" possible when memory is selective.

The envelope (§3.4), plus:

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `sourceKind` | string | yes | below | |
| `title` | string | no | — | May itself be sensitive. Never served below the `summary` tier (§15.3). |
| `content` | `{"locator": {"vaultPath": string} \| {"uri": URI}, "sha256"?: string, "mediaType": string, "size"?: int, "encrypted"?: boolean}` | yes | IANA media types | `sha256` (64 lowercase hex characters) is REQUIRED except for `live-feed`. `vaultPath` follows `vault/<2hex>/<sha256>.<ext>`. |
| `capturedAt` | DateTime or PartialTime | no | — | When the material was created. If absent, it is unknown, never "now". |
| `authorship` | `{"author": Actor, "coAuthors"?: [Actor]}` | yes | — | |
| `inbound` | boolean | no | — | `true` = received from someone else (a message, a letter). See W-SR1. |
| `contemporaneity` | string | no | `contemporaneous`, `retrospective`, `unknown` | Default `unknown`. |
| `participants` | [LocalId] | no | — | Party ids. |
| `containsThirdParty` | boolean | no | — | When `true`, category `third-party` is added and the default `maxRelease` becomes `index`. |
| `maxRelease` | string | no | §15.3 | The ceiling for any grantee. Default `summary`. It is `index` when custody confidentiality is not `none`, when `containsThirdParty` is true, and for GUM observation streams. The subject always has every tier (V-0). |
| `custody` | `{"custodian": Actor, "confidentiality": "none" \| "therapy" \| "coaching" \| "legal" \| "medical", "releaseRef"?: LocalId, "terms"?: string}` | no | §15.3 | Material held under a professional's confidentiality. `releaseRef` names the Source holding the practitioner's release. |
| `summary` | `{"text": string, "authoredBy": Actor, "recordedAt": DateTime, "method"?: "subject-written" \| "agent-written" \| "practitioner-written" \| "imported"}` | no | — | A summary is a **selection by its author** and is shown with that author ("whose selection"). |
| `redactions` | [`{"selector": Selector, "reason": "third-party" \| "subject-request" \| "legal" \| "custody", "by": Actor, "at": DateTime}`] | no | — | Applied at release. Later redactions are Reviews `redact` (§11.1). |
| `derivedFrom` | [LocalId] | no | — | Other Sources. Example: a transcript derived from audio. |
| `retention` | `{"until"?: date, "eraseOnRequest": true}` | no | — | `eraseOnRequest` is const `true`. |

**Source kinds** (open list with `x-`): `journal-entry`, `note`, `message`, `email`, `transcript`, `audio`, `video`, `image`, `document`, `calendar`, `log`, `screen-observation`, `sensor`, `biometric`, `voice`, `keystroke`, `instrument-report`, `practitioner-notes`, `practitioner-release`, `consent-document`, `live-feed`, `import-bundle`, `other`. The [source-kinds](catalogs/source-kinds.json) catalog gives each kind its `defaultTier` (§8.3) and flags the behavioural kinds that trigger R-X4: `audio`, `video`, `image`, `screen-observation`, `sensor`, `biometric`, `voice` and `keystroke`. An `x-` kind defaults to `sensitive`.

**Allowed references.** Sources only (`derivedFrom`, `custody.releaseRef`) and Parties (G1).

**Invariants.**

- **SR-1.** `sha256` is present unless the kind is `live-feed`.
- **SR-2.** If the vault file is present locally, its sha256 matches. The checker never reads the content (§5.8).
- **SR-3.** `vaultPath` matches the content-addressed layout.
- **SR-4.** No field outside `summary.text` and `title` contains free text from the content. This is a heuristic.
- **SR-5.** `maxRelease` is no higher than the custody ceiling (§15.3).
- **SR-6.** G1 holds.
- **SR-7.** If custody confidentiality is not `none`, `releaseRef` is present or `maxRelease` is `index`.
- **W-SR1.** Warning `inboundOnlyEvidence`: a Claim's evidence consists only of inbound Sources.

**Example.**

```json
{"id": "src-01", "sourceKind": "journal-entry", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-03-12T18:45:00Z",
 "content": {"locator": {"vaultPath": "vault/2d/2dbfdd422fbc32bbdf09702fea766ba0cf0b4f9f8efa5e2f9eb7194d6fff0fc1.md"},
             "sha256": "2dbfdd422fbc32bbdf09702fea766ba0cf0b4f9f8efa5e2f9eb7194d6fff0fc1",
             "mediaType": "text/markdown", "size": 460},
 "capturedAt": "2026-03-12T18:40:00Z", "authorship": {"author": "subject"}, "contemporaneity": "contemporaneous",
 "maxRelease": "excerpt",
 "summary": {"text": "Evening note after moving the supplier call.", "authoredBy": "subject",
             "recordedAt": "2026-03-12T18:45:00Z", "method": "subject-written"},
 "retention": {"eraseOnRequest": true}, "sensitivity": "sensitive", "contexts": ["work"], "synthetic": true}
```

### 10.2. Episode

Layer `experience` · module `core` · normative-draft. One occurrence in the person's life, told through one or more **accounts**. Each account is dated and attributed, and separates what happened, what was experienced, what was done and what was understood at the time. Later readings are **not** stored here: they are Interpretations pointing at the Episode.

The envelope (§3.4), plus:

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `title` | string | no | — | Short and neutral. Served only at `named` audience. |
| `occurred` | PartialTime | yes | — | Experience time. |
| `accounts` | [Account] | yes (≥1) | — | Ordered. Prior accounts never change (EP-2). |
| `participants` | [LocalId] | no | — | Pseudonymous Party ids. |
| `externalConfirmation` | `{"status": "none" \| "partial" \| "confirmed", "basis"?: [LocalId], "by"?: Actor}` | no | — | `basis` lists Sources. |
| `selection` | `{"selectedBy": Actor, "reason": "subject-chose" \| "agent-suggested" \| "practitioner-suggested" \| "imported", "note"?: string}` | no | — | Who decided this occurrence is worth recording. |
| `recall` | string | no | `not-permitted` (default), `ask-each-time`, `permitted` | Per-episode recall permission. Only the subject sets or changes it, through `relax` or `restrict` Reviews. |
| `salience` | string | no | `low`, `medium`, `high` | Only when `assertedBy` is `"subject"`. |
| `openQuestions` | [string] | no | — | The person's open questions about the episode. |

**Account** (embedded):

| Field | Type | Req | Notes |
|---|---|---|---|
| `narrator` | Actor | yes | |
| `narratedAt` | DateTime or PartialTime | yes | When the account was given. |
| `addedAt` | DateTime | yes | Knowledge time: when this account entered the context. |
| `accountKind` | string | yes | below |
| `happened` | string | no | What happened, as observable events. |
| `experienced` | string | no | What was felt or sensed. Only in accounts narrated by the subject. |
| `didOrTried` | string | no | Actions and attempts. |
| `understandingThen` | string | no | How the narrator understood it **at the time of the episode**. A reading formed later MUST be an Interpretation (EP-4). |
| `text` | string | no | A free narrative, when strands are not used. |
| `affectTags` | [string] | no | Only when the narrator is `"subject"`. Free words, or `x-` codes. |
| `evidence` | [Span] | no | Spans into Sources only (G1). |
| `lang` | string | no | |

At least one of `happened`, `experienced`, `didOrTried`, `understandingThen` and `text` MUST be present.

**Account kinds** (closed):

| Code | Definition |
|---|---|
| `in-the-moment` | Narrated during or right after the episode. |
| `first-narrative` | The first telling, later than the episode. |
| `later-reconstruction` | Retold from memory after time has passed. |
| `external-record` | A system or document record (calendar, log). |
| `observer-account` | Another person's account of what happened. |

**Allowed references.** `accounts[].evidence` → Sources. `participants`, `narrator` → Parties. `supersedes` → Episode. `externalConfirmation.basis` → Sources.

**Invariants.**

- **EP-1.** No reference to any interpretation-layer record (G1).
- **EP-2 (R-E1).** A superseding Episode contains every account of the superseded one, JCS-equal and in the same order, and adds at least one account or changes only metadata. Adding an account is done this way: a new Episode that supersedes the old one.
- **EP-3.** `experienced` and `affectTags` appear only in accounts narrated by the subject.
- **EP-4.** Accounts have no field for later readings. The schema enforces this.
- **EP-5.** An `observer-account` narrator is a Party, and the account describes no third party's inner states (TP-1). This is a heuristic warning.
- **EP-6.** `recall` is `not-permitted` unless the subject set it.
- **EP-7.** Episodes are never given freshness. Their derived freshness is `historical`.

**Example.** `ep-04` supersedes `ep-01` and adds a later reconstruction.

```json
{"id": "ep-04", "supersedes": "ep-01", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-19T20:00:00Z", "title": "First postponed supplier call",
 "occurred": {"start": "2026-03-12", "precision": "day"}, "contexts": ["work"], "participants": ["p-01"],
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-03-12T18:40:00Z", "addedAt": "2026-03-12T18:45:00Z",
    "accountKind": "in-the-moment", "happened": "I moved the 15:00 call with the supplier to next week.",
    "experienced": "Heavy and restless; relieved for about an hour afterwards.",
    "didOrTried": "Wrote a short apology; tidied the workshop.",
    "understandingThen": "I did not have the cost figures ready.", "affectTags": ["heavy", "relieved"],
    "evidence": [{"source": "src-01", "selector": {"type": "text-position", "start": 0, "end": 412}}]},
   {"narrator": "s-01", "narratedAt": "2026-03-12T13:02:00Z", "addedAt": "2026-03-12T18:45:00Z",
    "accountKind": "external-record", "happened": "Event 'Supplier call' moved from 12 Mar 15:00 to 19 Mar 15:00.",
    "evidence": [{"source": "src-02", "selector": {"type": "whole"}}]},
   {"narrator": "subject", "narratedAt": "2026-09-19T19:50:00Z", "addedAt": "2026-09-19T20:00:00Z",
    "accountKind": "later-reconstruction",
    "happened": "The cost figures had been in a spreadsheet since 10 March. I had no number at which I would walk away."}],
 "externalConfirmation": {"status": "partial", "basis": ["src-02"], "by": "s-01"},
 "selection": {"selectedBy": "subject", "reason": "subject-chose"}, "salience": "high",
 "openQuestions": ["Did my actions change, or only my explanation?"], "sensitivity": "sensitive", "synthetic": true}
```

### 10.3. Interpretation

Layer `interpretation` · module `core` · normative-draft. One reading of one or more episodes, spans, claims, patterns or assessment results, by a named author, at a known time, possibly through a lens. Interpretations are kept side by side and never merged. They can contradict each other. Their history along the knowledge-time axis answers "how did I understand this then?". The form can be a statement (`text`) or a question (`question`).

The envelope (§3.4), plus:

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `about` | [Ref or Span] | yes (≥1) | — | Episodes, spans, Claims, Patterns, AssessmentRecords. Never a Party (TP-1). |
| `text` | string | cond | — | Exactly one of `text` and `question`. |
| `question` | string | cond | — | An open question, kept as a reading. |
| `stance` | string | yes | §10.3.1 | `in-the-moment`, `retrospective`, `revision`, `alternative`, `lens-reading` |
| `lens` | `{"id": URI, "version": string}` | no | — | |
| `adoption` | LocalId | cond | — | REQUIRED when `lens` is present and `assertedBy` is neither `"subject"` nor an agent or software Party (I5). An agent or software author MAY name the adoption it works under. |
| `causal` | string | no | `none` (default), `hypothesized`, `asserted` | I2 |
| `grounds` | [Ground] | cond | — | REQUIRED, with at least one entry, for non-subject authors (I4). |
| `counterEvidence` | [Ground] | no | — | What does not fit. |
| `alternatives` | [Alternative] | cond | — | REQUIRED, with at least two entries, for non-subject authors. At least one alternative MUST have kind `situational`, `physiological`, `informational` or `external` (I4). |
| `limits` | string | cond | — | REQUIRED for non-subject authors. |
| `heldDuring` | Interval | no | — | Knowledge time during which the author held this reading. `from` defaults to `formulatedAt` or `recordedAt`. The effective `until` is computed (I7). |
| `facets` | [string] | no | §9.4.2 | A topical facet, so that grants can scope interpretations. |

**Allowed references.** `about` → Episode, Span, Claim, Pattern, AssessmentRecord. `grounds` and `counterEvidence` → Source spans, Episodes, Claims, AssessmentRecords, Patterns. `adoption` → LensAdoption. `supersedes` → Interpretation.

#### 10.3.1. Interpretation vocabularies

**Stance** (closed):

| Code | Definition |
|---|---|
| `in-the-moment` | Formed during the episode, recorded as a reading. |
| `retrospective` | Formed later. |
| `revision` | Replaces the same author's earlier reading (uses `supersedes`). |
| `alternative` | Offered next to another reading. |
| `lens-reading` | Produced through a named lens. |

**Causal** (closed): `none`, `hypothesized`, `asserted` (I2).

**Ground kinds** (closed):

- `evidence`: a span or record that shows it;
- `observation`: an observed event;
- `sequence`: temporal order only, which never proves a cause;
- `pattern`: recurrence;
- `instrument`: an assessment result;
- `testimony`: a party's account;
- `practitioner`: a practitioner's reading;
- `subject-statement`: the person said so.

**Alternative kinds** (closed): `psychological`, `situational`, `physiological` (fatigue, load, health), `informational` (missing information), `relational`, `external` (outside obstacles), `combination`, `other`. I4 and RC-4 require at least one alternative that is not psychological.

#### 10.3.2. Invariants

- **I1.** If `assertedBy` is not `"subject"`, the record is `proposed` (computed), its epistemic status is `hypothesis` (or `frame-relative` for a non-empirical lens), and INF-1 applies.
- **I2.** `causal: asserted` requires at least one ground whose kind is not `sequence`; a sequence never proves a cause. Non-subject authors MUST NOT use `asserted`.
- **I3.** No distortion label, diagnosis or clinical term is applied unless the person adopted the lens and supplied the label. The lens's `helperMustNot` lists apply. This rule is normative and not machine-checkable.
- **I4.** For non-subject authors, `grounds` has at least one entry, `alternatives` has at least two (with at least one non-psychological kind), and `limits` is present.
- **I5.** With a `lens` and a non-subject author: an agent or software author writes under an `infer` grant whose scope names the lens (INF-1, R-G3(b)); any other author is listed in `interpretationAuthors` of the person's active adoption of the lens, which `adoption` names. A named `adoption` is an adoption of the same lens. An active adoption of the lens with `agentInterpretation: off` (or none) stops agent and software authors; with `ask-first`, at L2, an Event of type `ask-first` with `outcome: confirmed`, the author as `counterparty` and the adoption id in `records` precedes `recordedAt`.
- **I6.** Nothing in the evidence or experience layers references an Interpretation (G1).
- **I7.** The computed `heldDuring.until` is: the stored `until`, if any; otherwise the successor's `heldDuring.from` if the record is superseded; otherwise the time of a `mark-not-current` Review; otherwise open.
- **I8.** `about` never resolves to a Party.
- **I9.** The effective tier is `special` when a `lens` is present, when `about` includes a Part, or when the adoption's confidentiality is not `none` (C3).
- **I10.** An Interpretation, Pattern or ModelView whose `assertedBy` is a Party with `partyKind` `agent` or `software` MUST have `origin: inferred`, or `origin: derived` with `generatedBy.method`. A reading by an agent is never `declared`, so it always needs `infer` (INF-1). I1 is evaluated on the effective epistemic status: the stored value, or else the default for the origin (§6.1).

**Example.** An agent's lens reading, proposed under an `infer` grant and partly endorsed by Noa in `rv-02`.

```json
{"id": "in-02", "about": ["ep-04", "ep-02"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:cbt", "version": "0.2.0"}, "adoption": "la-01",
 "text": "An expectation that the supplier would end the relationship may have come before each postponement.",
 "causal": "hypothesized", "origin": "inferred", "assertedBy": "a-02", "recordedAt": "2026-09-21T09:30:00Z",
 "underGrant": "g-02", "purpose": "self-reflection", "epistemic": "hypothesis",
 "grounds": [
   {"span": {"source": "src-01", "selector": {"type": "text-position", "start": 120, "end": 260}}, "kind": "evidence"},
   {"ref": "ep-02", "kind": "pattern"}],
 "counterEvidence": [
   {"ref": "ep-03", "kind": "evidence", "note": "Held the call in September despite the same supplier."}],
 "alternatives": [
   {"text": "No walk-away number had been set.", "kind": "informational"},
   {"text": "Both weeks were overloaded; fatigue.", "kind": "physiological"},
   {"text": "The supplier's own schedule moved.", "kind": "situational"}],
 "limits": "Two episodes and one lens; a self-reflection aid, not a clinical reading.", "facets": ["goal"],
 "contexts": ["work"], "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

**Example.** The subject's own revision (temporal self-model).

```json
{"id": "in-03", "supersedes": "in-01", "about": ["ep-04", "ep-02", "ep-03"], "stance": "revision",
 "text": "I postponed when I had no walk-away number. Once I had one, I went.", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-09-26T20:10:00Z", "heldDuring": {"from": "2026-09-26"},
 "facets": ["goal"], "synthetic": true, "handling": ["no-quote-back"]}
```

### 10.4. Tension

Layer `interpretation` · module `core` · normative-draft. A conflict that matters: between goals, values, horizons or resources, inside the person, between sources, or between holders. It records who decides it. A Tension is never resolved by averaging, by majority or by an agent (T1).

The envelope (§3.4), plus:

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `between` | [Ref] | yes (≥2) | — | Claims, Interpretations, AssessmentRecords; Sources (only for `source-divergence`). |
| `tensionKind` | string | yes | below | |
| `whoDecides` | string | yes | below | `holder-policy` is allowed only for `source-divergence` and `holder-divergence` (T2). |
| `text` | string | no | — | How the asserter sees the conflict. |

The status (`open`, `acknowledged`, `exploring`, `held-as-is`, `resolved`) is **computed** from the Reviews `acknowledge`, `explore`, `hold-as-is` and `resolve` (§11.1).

**Tension kinds** (closed):

| Code | Definition |
|---|---|
| `goal-conflict` | Two goals cannot both be fully pursued. |
| `value-conflict` | Two declared values pull apart. |
| `horizon-conflict` | A `state` pulls against a `focus` or a `foundation` claim. |
| `resource-competition` | Goals or commitments compete for the same time, attention or money. |
| `inner-conflict` | Two sides within the person; both sides are explored. |
| `source-divergence` | Instruments, sources or raters disagree (M-8). |
| `holder-divergence` | Different holders hold different values. |

**Who decides** (closed):

| Code | Meaning |
|---|---|
| `subject` | The person decides. |
| `subject-with-practitioner` | The person decides, together with a practitioner. |
| `holder-policy` | Only for `source-divergence` and `holder-divergence`. |
| `not-applicable` | The tension is to be held, not decided. |

**Allowed references.** `between` → Claim, Interpretation, AssessmentRecord, Source.

**Invariants.**

- **T1.** A `resolve` Review on a Tension is authored by the subject, or by `"holder"` when `whoDecides` is `holder-policy`.
- **T2.** `whoDecides: holder-policy` is allowed only with `tensionKind` `source-divergence` or `holder-divergence`.
- **T3.** The effective tier is the maximum over `between`. A Tension is served only if every member of `between` is disclosable under the same grant. Otherwise it is omitted without any flag (§12.3, step 7).
- **T4.** Members of `between` are pairwise distinct.

**Example.**

```json
{"id": "t-01", "between": ["c-03", "c-04"], "tensionKind": "goal-conflict", "whoDecides": "subject",
 "text": "Keeping the nine-year supplier relationship warm pulls against cutting material costs by 15%.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-02T08:20:00Z", "contexts": ["work"],
 "synthetic": true}
```

### 10.5. LensAdoption

Layer `assertion` · module `lenses` · normative-draft. The person's relation to one framework of description: how they came to it (self-chosen, suggested by an agent, inherited from therapy, coaching or practice, or imported), what it may be used for, who may interpret through it, and what happens when a practice relationship ends. The lens descriptor itself is a registry document specified in [LENSES.md](LENSES.md).

The envelope (§3.4), plus:

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `lens` | `{"id": URI, "version": string}` | yes | — | Never duplicated in another field. |
| `route` | string | yes | below | `self-chosen`, `agent-suggested`, `inherited-from-practice`, `imported` |
| `suggestedBy` | Actor | cond | — | REQUIRED for `agent-suggested`. |
| `practice` | `{"role": "therapist" \| "coach" \| "teacher" \| "facilitator" \| "other", "practitioner": LocalId, "relationship": "active" \| "ended", "since"?: date, "releaseRef"?: LocalId}` | cond | — | REQUIRED for `inherited-from-practice`. |
| `confidentiality` | string | no | `none` (default), `practitioner-scope`, `therapy-confidential` | `therapy-confidential` forces tier `special` and handling `person-only` on the adoption and on every record citing it (LA-4). |
| `uses` | [string] | yes | `speak-in-lens`, `offer-practices`, `store-results`, `interpret`, `recall` | |
| `interpretationAuthors` | [Actor] | no | — | Default `["subject"]`. |
| `agentInterpretation` | string | no | `off` (default), `ask-first`, `allowed` | Whether agents may read through the lens while this adoption is active, under an `infer` grant that names the lens (I5). An absent member is `off`: absence is not consent. |
| `representationPreference` | string | no | lens representation id | |
| `playbooks` | [URI] | no | — | The playbooks the person uses with this lens. Absent: the descriptor's `playbooks`. `[]`: none. Each resolves to a playbook for this lens (PB-3; [LENSES.md](LENSES.md) §2.2). |
| `onEnd` | string | no | `ask` (default), `keep-read-only`, `archive-person-only`, `erase` | What happens when the practice relationship ends. With `ask`, the adoption is computed `paused` until the subject decides. |

**Adoption routes** (closed):

| Code | Definition |
|---|---|
| `self-chosen` | The person picked the lens. |
| `agent-suggested` | An agent proposed it and the person accepted. It is proposed until the subject admits it. |
| `inherited-from-practice` | Brought from the person's therapy, coaching, teaching or practice, with a `practice` block. |
| `imported` | Created by an importer from an instrument report. Proposed until admitted. |

The status (`proposed`, `active`, `paused`, `retired`) is computed from admission and from the Reviews `pause`, `resume` and `retire`. An ended practice relationship is recorded by a superseding LensAdoption with `practice.relationship: ended`.

**Invariants.**

- **LA-1.** An `agent-suggested` adoption is proposed and activated by the subject only.
- **LA-2.** No practitioner access is implied by an adoption. There is no grant-like field.
- **LA-3.** `inherited-from-practice` requires a `practice` block, and `releaseRef` when material from sessions is stored.
- **LA-4.** `confidentiality: therapy-confidential` propagates tier `special` and handling `person-only` to the adoption and to every record citing it.
- **LA-5.** `route: imported` makes AssessmentRecords from the same import run proposed until the subject admits them.
- **LA-6.** The lens id resolves to a pinned descriptor (`Context.lenses`, with the descriptor in `lenses/` or inline), or to a catalog entry when one is present locally. A lens with no resolvable descriptor is treated as a **stub**: its results are `frame-relative`.
- **W-LA6.** Warning: the lens of a LensAdoption has no resolvable descriptor, so the adoption is treated as a stub (LA-6). A person's or practitioner's own framework can be described with a local descriptor ([LENSES.md](LENSES.md) §5.1).

**Example.**

```json
{"id": "la-02", "lens": {"id": "urn:ohc:lens:ifs", "version": "0.2.0"}, "route": "inherited-from-practice",
 "practice": {"role": "coach", "practitioner": "p-02", "relationship": "active", "since": "2026-04-01",
              "releaseRef": "src-05"},
 "confidentiality": "practitioner-scope", "uses": ["speak-in-lens"], "interpretationAuthors": ["subject", "p-02"],
 "agentInterpretation": "off", "representationPreference": "ifs.parts-map", "onEnd": "ask", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-06-02T18:00:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "handling": ["no-forward"], "synthetic": true}
```

### 10.6. AssessmentRecord

Layer `assertion` · module `lenses` · normative-draft. A dated result about the person within one lens: a questionnaire score, a self-identified type, a ranking, a values profile, a thought record, frame attributes, or a narrative. It records how it was produced and under what limits. **Framework, construct, instrument and result are kept apart.**

The envelope (§3.4), plus:

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `lens` | `{"id": URI, "version": string}` | yes | — | |
| `lensVariant` | string | no | lens `variants[].id` | |
| `instrument` | `{"id": URI, "version"?: string, "form"?: string}` | no | — | |
| `mode` | string | yes | below | |
| `assessedBy` | Actor | no | — | The rater. Default `assertedBy`. |
| `raterRelationship` | string | no | §9.4.3 | For `observer-report`. |
| `administeredAt` | PartialTime | yes | — | Experience time. |
| `results` | [Result] | yes (≥1) | below | |
| `normGroup` | `{"id": string, "country"?: string, "year"?: int, "n"?: int, "note"?: string}` | no | — | |
| `validityFlags` | [string] | no | below | |
| `source` | LocalId | no | — | The Source holding the original report. Dropped in `summary` mode (§12.2). |
| `trademarkNotice` | string | cond | — | REQUIRED when the lens's `ip.marks` require a notice and the result is genuine (not agent-inferred). |
| `validityCeiling` | string | cond | `agent-estimate-not-validated`, `cross-lens-population-estimate` | REQUIRED for the agent modes (AR-2). |
| `mapping` | URI | cond | — | REQUIRED for `cross-lens-estimate`. |
| `reviewAfter` | Duration | no | — | Default from the lens `defaults.reviewAfter`. |

**Imported results.** An AssessmentRecord whose `importedFrom.system` is an instrument id (`urn:ohc:instrument:…`) is an *imported result*: a result the person brings from an instrument report. The module `instrument-import` governs it ([INSTRUMENT-IMPORT.md](INSTRUMENT-IMPORT.md), IMP-1…IMP-5). A record carries no permissions: what a grantee may see, infer or decide on the basis of it is the person's grant (§12, R-G14).

**Assessment modes** (closed):

| Code | Definition |
|---|---|
| `self-report-instrument` | The person took an instrument. |
| `observer-report` | Another rater used an instrument. |
| `interview-scored` | Scored from an interview. |
| `practitioner-facilitated` | Arrived at with a practitioner. |
| `self-identified` | The person chose the type or result. |
| `vendor-report-import` | Copied from a vendor report. |
| `agent-inference` | An agent estimated it. Constrained by AR-2. |
| `cross-lens-estimate` | Estimated through a population-level Mapping. Constrained by AR-2 and AR-7. |
| `computed-from-birth-data` | A frame computed from birth data. |

**Result shapes** (`type` discriminator; closed):

| `type` | Fields |
|---|---|
| `dimension-score` | `construct`, `label`?, `raw`?, `rawRange`?, `standardized`? `{"type": "T" \| "z" \| "percentile" \| "stanine" \| "sten", "value"}`, `sem`?, `ci`? |
| `type-assignment` | `construct`, `label`?, `clarity`?, `method`: `self-identified` \| `instrument` \| `interview` \| `best-fit`, `alternatives`? [construct] |
| `ranking` | `constructs` [ordered], `signatureTopN`? |
| `values-profile` | `scores` [`{"construct", "raw", "centered"}`] |
| `circumplex` | `angle`, `magnitude`, `axes` |
| `stage` | `construct`, `secondary`? |
| `thought-record` | `situation`, `thought`, `emotion`, `behavior`, `alternative` (the person's own entries) |
| `frame-attributes` | `attributes` object, `computedFrom` (Ref to a `birth-data` Claim), `engine` `{"name", "version"}` |
| `narrative` | `text` |

**Validity flags** (closed): `incomplete`, `random-responding`, `acquiescence`, `translated-form`, `norm-mismatch`, `agent-estimate-not-validated`, `cross-lens-population-estimate`, `self-identified-only`, `vendor-algorithm-undisclosed`, `test-data-personal-only`.

**Invariants.**

- **AR-1.** Origin by mode: instrument scores are `derived`, or `imported` for vendor reports; `self-identified` results are `declared`; `agent-inference` is `inferred` (INF-1 applies); `computed-from-birth-data` is `derived`.
- **AR-2.** `agent-inference` and `cross-lens-estimate` require: handling ⊇ `["person-only"]`; `validityFlags` ⊇ `["agent-estimate-not-validated"]` and the matching `validityCeiling`; and no construct `label` that is a mark listed in the lens's `ip.marks`, and no `trademarkNotice` (no branded labels).
- **AR-3.** Never-fields. The schema has no fields for item text, report prose, scoring keys or raw proprietary responses. The one exception is `ext["ohc.test-data"]` with handling `person-only` and the flag `test-data-personal-only`.
- **AR-4.** Results of lenses whose `ontologicalStatus` is `symbolic-frame`, or whose `measurementTier` is `T5` (a non-empirical self-description frame; see LENSES.md), have epistemic status `frame-relative`. A record inferred from such a result is `frame-relative` too.
- **AR-5.** The default tier is `special` for every AssessmentRecord. Only the subject may lower it, with `relax`. Documentation says "treated as special category", never "is Art. 9 data".
- **AR-6.** A type derived from continuous scores stores both the scores and the rule (`generatedBy.method`).
- **AR-7.** `cross-lens-estimate` requires a `mapping` that resolves, is not chainable and is never used in a chain (M-3), whose `rowStatus` is `accepted` or `accepted-with-loss`, whose `forbiddenUse` is empty, and whose `to.lens` equals the record's lens. Both lenses MUST have `useLimits.crossLensMapping: population-level-only`.
- **AR-8.** The instrument belongs to the lens's `instruments` list.

**Example** (self-report through a public-domain instrument):

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"}, "lensVariant": "5-domain-30-facet",
 "instrument": {"id": "urn:ohc:instrument:ipip-neo-120", "version": "2014", "form": "120"},
 "mode": "self-report-instrument", "assessedBy": "subject",
 "administeredAt": {"start": "2026-08-14", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "big-five/E", "label": "Extraversion", "raw": 2.7, "rawRange": [1, 5]},
   {"type": "dimension-score", "construct": "big-five/C", "label": "Conscientiousness", "raw": 4.1, "rawRange": [1, 5]}],
 "normGroup": {"id": "ipip-internet-2014", "note": "Internet sample, IPIP-NEO-120 norms (2014)"},
 "validityFlags": [],
 "reviewAfter": "P3Y", "origin": "derived",
 "generatedBy": {"software": "ohc-ipip-scorer", "version": "0.1.0", "method": "mean of keyed items"},
 "derivedFrom": ["src-11"], "assertedBy": "subject", "recordedAt": "2026-09-29T19:00:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true, "formulatedAt": "2026-08-14T20:00:00Z",
 "importedFrom": {"importedAt": "2026-09-29T19:00:00Z", "run": "e-0010", "system": "ohc-ipip-scorer",
                  "systemVersion": "0.1.0"},
 "source": "src-11"}
```

### 10.7. ModelView

Layer `interpretation` · module `lenses` · normative-draft. One named model's view over a set of episodes and evidence. It groups the hypotheses (Interpretations) a model produced, with the question the model asks, its grounds and limits, and the alternative views. The person's feedback on it is computed from Reviews and Outcomes. Its revision history is the `supersedes` chain.

The envelope (§3.4), plus:

| Field | Type | Req | Notes |
|---|---|---|---|
| `lens` | `{"id", "version"}` | cond | Exactly one of `lens` and `model`. |
| `model` | `{"name": string, "version": string}` | cond | For models not in the registry. |
| `adoption` | LocalId | cond | REQUIRED when `lens` is present and the author is neither the subject nor an agent or software Party (I5, MV-3). |
| `question` | string | no | What this view asks (from the lens's `mentalModel.exploratoryQuestions`). |
| `scope` | `{"episodes"?: [LocalId], "sources"?: [LocalId], "period"?: Interval}` | yes | At least one of `episodes` and `sources`. |
| `hypotheses` | [LocalId] | yes (≥1) | Interpretations. |
| `representation` | string | no | A lens representation id. |
| `summary` | string | no | |
| `grounds` | [Ground] | cond | REQUIRED for non-subject authors. |
| `limits` | string | cond | REQUIRED for non-subject authors. |
| `alternatives` | [Ref or URI] | cond | Other ModelViews, or lens ids. At least one is REQUIRED for non-subject authors. |

**Invariants.**

- **MV-1.** Every hypothesis is an Interpretation, and its `about` lies within `scope`.
- **MV-2.** A ModelView adds no new statements. It has no `text` field beyond `summary`.
- **MV-3.** I5 holds for `adoption`.
- **MV-4.** The default tier is `special`.

**Example.**

```json
{"id": "mv-01", "lens": {"id": "urn:ohc:lens:cbt", "version": "0.2.0"}, "adoption": "la-01",
 "question": "What went through your mind just before you moved the call?",
 "scope": {"episodes": ["ep-04", "ep-02"]}, "hypotheses": ["in-02"], "representation": "cbt.thought-record",
 "grounds": [{"ref": "ep-04", "kind": "evidence"}],
 "limits": "One lens among several; two episodes; no clinical meaning.",
 "alternatives": ["urn:ohc:lens:cognitive-appraisal"], "origin": "inferred", "assertedBy": "a-02",
 "recordedAt": "2026-09-21T09:31:00Z", "underGrant": "g-02", "purpose": "self-reflection", "epistemic": "hypothesis",
 "sensitivity": "special", "synthetic": true}
```

## 11. Review, Proposal, Tombstone

### 11.1. Review

Layer `governance` · module `core` · normative-draft. The **single mechanism for every status change**. Records are immutable. Endorsement, contest, lock, admission, retraction, epistemic reassessment, disclosure changes, redaction, pausing and Tension work are all appended as Reviews. Effective status is computed by replaying them. This makes endorsement and admission history reconstructable at L1.

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `kind` | const `"Review"` | ctx | — | |
| `id` | LocalId | yes | prefix `rv-` | |
| `target` | LocalId or [LocalId] | yes | — | At most 100 targets. Every target has the same kind. |
| `action` | string | yes | below | |
| `by` | Actor | yes | — | MUST be allowed for the action (below). |
| `recordedAt` | DateTime | yes | — | |
| `underGrant` | LocalId | cond | — | REQUIRED when `by` is a Party that is not a steward. |
| `basis` | string | cond | — | REQUIRED when `by` is a steward: `"steward-scope"`. |
| `note` | string | no | — | |
| `endorsedPart` | string | cond | — | REQUIRED for `partially-endorse`: what the person accepts, in their words. |
| `epistemic` | string | cond | §6.3 | REQUIRED for `reassess`. |
| `disclosure` | `{"sensitivity"?: tier, "audience"?: "grantees" \| "named", "addHandling"?: [code], "removeHandling"?: [code], "addCategories"?: [code], "recall"?: "not-permitted" \| "ask-each-time" \| "permitted"}` | cond | §8 | REQUIRED for `restrict` and `relax`. `restrict` may only raise a tier, add handling or categories, or narrow recall. `relax` does the reverse and is subject-only. |
| `selectors` | [Selector] | cond | — | REQUIRED for `redact` (Sources only). |
| `reasonCode` | string | no | `not-true`, `not-now`, `too-sensitive`, `not-relevant`, `outdated`, `wrong-person`, `locked`, `expired`, `quota-exceeded`, `other` | For `reject`, `decline` and `retract`. The holder uses `locked`, `expired` and `quota-exceeded` when it declines (IB-4, IB-5). |
| `ext` | object | no | — | |

**Review actions, allowed actors and effects** (closed):

| Action | Targets | Allowed `by` | Effect |
|---|---|---|---|
| `endorse` | content records | subject; steward in scope (not special or inner-system) | endorsement → `endorsed` (implies `admit`) |
| `partially-endorse` | content records | same | endorsement → `partial`, with `endorsedPart` (implies `admit`) |
| `reject` | content records | same | endorsement → `rejected` (implies `decline` if proposed) |
| `contest` | content records | same | `contested` = true (implies `admit`) |
| `withdraw-contest` | contested records | subject; steward in scope | `contested` = false |
| `resolve-contest` | contested records | subject | `contested` = false, with a note |
| `lock` / `unlock` | content records | subject | `locked` = true / false |
| `confirm-current` | Claim, AssessmentRecord, LensAdoption, Practice | subject; steward in scope | sets `lastConfirmedAt` |
| `mark-not-current` | Claim, AssessmentRecord, LensAdoption, Practice, Interpretation | subject; steward in scope | freshness → `expired`; for an Interpretation, closes `heldDuring` |
| `admit` | proposed records | subject; `"holder"` only under R-A1 policy | admission → `active` |
| `decline` | proposed records | subject; `"holder"` always (a protective decline: a target is locked, the proposal expired, or the inbox is over quota) | admission → `declined` |
| `retract` | any content record | its `assertedBy`; subject | admission → `retracted` (terminal) |
| `reassess` | content records | its `assertedBy`; subject | epistemic → the given value |
| `restrict` | content records | subject; steward in scope; `"holder"` (quarantine under R-X3, third-party protection) | raises the tier, adds handling or categories, narrows recall |
| `relax` | content records | **subject only** | lowers the tier, removes handling, sets audience `grantees`, widens recall |
| `redact` | Source | subject; `"holder"` (third-party protection) | adds release-time redactions |
| `pause` / `resume` / `retire` | LensAdoption, RecallCue, Practice | subject | lifecycle status |
| `acknowledge` / `explore` / `hold-as-is` / `resolve` | Tension | subject; `"holder"` for `resolve` under T2 | Tension status |
| `withdraw-grant` | Grant | subject; steward grantor in scope | status → `withdrawn` |
| `revoke-grant` | Grant | `"holder"` | status → `revoked` (for security or misuse) |

**Replay.**

- Reviews are applied in order of `recordedAt`, then file order.
- Each axis takes the last applicable action.
- `retract` is terminal.
- Implied actions (RV-3) are applied at the same point in the order.
- The as-known-at query (§7.3) replays only Reviews with `recordedAt` ≤ K.

**Invariants.**

- **RV-1.** Every target exists and is not a Review or an Event.
- **RV-2.** The actor is allowed for the action, the steward's scope covers the target kind and facet, and R-A1 holds.
- **RV-3.** Implied actions: `endorse`, `partially-endorse` and `contest` on a proposed record also admit it; `reject` on a proposed record also declines it, unless an `admit` by the subject follows.
- **RV-4.** No Review is recorded against a target at or after that target's `erasedAt`. Reviews recorded before the erasure stay, reduced as §15.5 step 2 says. (The erasure flow's own `record-erased` Event is not a Review.)
- **RV-5.** A `retract` is terminal. A later `admit` on the same target is an error.
- **RV-6.** A `resolve` follows T1.

**Example.** Noa contests the inferred claim. The evidence stays.

```json
{"id": "rv-01", "target": "c-09", "action": "contest", "by": "subject", "recordedAt": "2026-09-22T07:55:00Z",
 "reasonCode": "not-true", "note": "I move calls when the numbers are not ready, not by weekday."}
```

### 11.2. Proposal

Layer `governance` · module `core` · normative-draft. The stored intake record for anything a non-subject writer proposes. The proposed records themselves are stored in their collections with computed admission `proposed`. The Proposal carries who proposed them, under which grant and purpose, the rationale, and the expiry. The decision is made by Reviews (`admit` or `decline`) on the items. **Silence is not acceptance:** an expired proposal is computed as declined.

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `kind` | const `"Proposal"` | ctx | — | |
| `id` | LocalId | yes | prefix `prop-` | |
| `proposer` | Actor | yes | — | A Party. |
| `recordedAt` | DateTime | yes | — | |
| `underGrant` | LocalId | yes | — | It MUST include `suggest`, and also `infer` when any item is `inferred` (PR-2). |
| `purpose` | string | yes | §8.9 | |
| `items` | [LocalId] | cond | — | The stored proposed records. |
| `requests` | [`{"target": LocalId, "action": "retract" \| "mark-not-current" \| "reassess", "epistemic"?: string}`] | cond | — | Requests for the subject to act on existing records. At least one of `items` and `requests` is non-empty. |
| `rationale` | string | yes | — | Shown to the person. It MUST NOT quote record content (G3). |
| `grounds` | [Ground] | no | — | |
| `expiresAt` | DateTime | no | — | Default `recordedAt` + P30D. |
| `presentation` | `{"channel": "holder-ui" \| "agent-dialog" \| "message", "askedAt"?: DateTime}` | no | — | |

**Invariants.**

- **PR-1.** Every item exists, has `assertedBy` equal to `proposer`, and carries `underGrant` equal to this Proposal's grant.
- **PR-2.** The grant was `given` at `recordedAt`, covers `purpose`, and includes `suggest`; it includes `infer` when any item is inferred. A holder that receives a proposal failing this rule MUST refuse it **without storing the items** and answer `ohc.denial` with `infer-not-granted` or `not-granted`.
- **PR-3.** Expiry is computed. Items still `proposed` after `expiresAt` are computed `declined` with reason `expired`: not admitted by the person. The proposer still sees them in its proposer view (§12.5).
- **PR-4.** Requests target existing records.

The holder's handling of open proposals (grouping, batching, quotas and the subject-only decisions) is specified by IB-1…IB-6 in [EXCHANGE.md](EXCHANGE.md).

**Example.**

```json
{"id": "prop-03", "proposer": "a-02", "recordedAt": "2026-09-21T09:30:00Z", "underGrant": "g-02",
 "purpose": "self-reflection", "items": ["in-02", "mv-01"],
 "rationale": "Two postponed calls share a pattern; offering one reading and two alternatives to look at.",
 "expiresAt": "2026-10-21T09:30:00Z", "presentation": {"channel": "agent-dialog", "askedAt": "2026-09-21T09:29:00Z"}}
```

### 11.3. Tombstone

Layer `governance` · module `core` · normative-draft. It replaces an erased record in place (R-S4). It keeps the id from being reused and keeps chains and replays well-formed, **without content**.

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `kind` | const `"Tombstone"` | yes | — | Always explicit, even in a single document. |
| `id` | LocalId | yes | — | The erased record's id. |
| `erasedKind` | string | yes | kind names | |
| `erasedAt` | DateTime | yes | — | |
| `erasedBy` | Actor | yes | — | `"subject"`, a steward in scope and valid at `erasedAt`, or `"holder"` (retention or legal). Never another Party. |
| `reason` | string | yes | below | |

**Tombstone reasons** (closed): `subject-request`, `retention-expired`, `consent-withdrawn`, `legal`, `holder-error`.

A Tombstone MUST NOT contain any content, hash of content, date of the erased content, party reference, facet, category, lens or title.

**Invariants.**

- **TB-1.** A Tombstone has no fields other than those in the table above.
- **TB-2.** References to a tombstoned id are allowed from any record and render as `[erased]`. The layer rules (G1) and the reference rule (RF-1) do not apply to them.
- **TB-3.** The id is never reused.
- **TB-4.** At L2, a `record-erased` Event exists for every Tombstone.
- **TB-5.** `erasedBy` is `"subject"`, `"holder"` or a steward valid at `erasedAt`; `erasedKind` is the kind implied by the Tombstone's collection; and at L2 the `record-erased` Event that lists the id has the same actor and is not later than `erasedAt`.

**Example.**

```json
{"kind": "Tombstone", "id": "in-04", "erasedKind": "Interpretation", "erasedAt": "2026-09-23T08:00:00Z",
 "erasedBy": "subject", "reason": "subject-request"}
```

## 12. Grant and grant evaluation

### 12.1. Grant

Layer `governance` · module `governance` · normative-draft. The person's permission (or explicit denial) for one grantee: which purposes, which records, which actions, in what mode, until when. **Default deny (R-G1). A grant is never authority to act in the world (R-G9).**

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `kind` | const `"Grant"` | ctx | — | |
| `id` | LocalId | yes | prefix `g-` | |
| `recordedAt` | DateTime | yes | — | |
| `grantor` | Actor | yes | — | `"subject"`, or a steward whose `scope.actions` includes `grant`. |
| `grantee` | LocalId | yes | — | A Party. Never a Part (R-G13). |
| `effect` | string | no | `allow` (default), `deny` | Deny wins (R-G2). |
| `purposes` | [string] | yes (≥1) | §8.9 | |
| `scope` | `{"include": [GrantSelector], "exclude"?: [GrantSelector]}` | yes | — | |
| `actions` | [string] | cond | §12.2 | REQUIRED for `allow`. Never `grant` (GR-9). |
| `mode` | string | no | §12.2 | Default `summary`. |
| `interpretations` | string | no | `none`, `subject-endorsed` (default), `all` | R-G8 |
| `maxSourceTier` | string | no | §15.3 | Default `none`. |
| `constraints` | object | yes | — | `{"notBefore"?: DateTime, "expiresAt": DateTime (REQUIRED), "maxUses"?: int, "storage": "none" \| "session" \| "until-expiry" (default "session"), "forwarding": false, "crossContextUse": false, "decisionUse"?: "deny" \| "approval-required" (default "deny"), "delegable": false}`. The three booleans are const `false` in 0.1. `decisionUse`: R-G14. |
| `stepUp` | `{"required": boolean, "maxDuration": Duration}` | cond | — | REQUIRED when `actions` includes `open-verbatim`; `required` is then const `true`. `maxDuration` ≤ PT1H, default PT30M. |
| `reviewCadence` | Duration | no | — | How often the person wants to reconcile this grantee's open proposals in one batch, for example `P7D` ([CONTEXT-09](../docs/agents/procedures/CONTEXT-09.md)). Counted against the inbox limit (IB-4). Never a deadline for the person. |
| `renews` | LocalId | no | — | The earlier Grant this one renews, to the same grantee. A renewal is a new grant the person gives, and it ends the earlier one when given; nothing is extended automatically (R-G10). |
| `basis` | `{"legal": "consent" \| "explicit-consent" \| "contract" \| "other", "note"?: string, "myTermsRef"?: URI}` | yes | — | Grants that reach `special` records or include `infer` MUST use `explicit-consent` (R-G11). |
| `expressedBy` | `{"actor": Actor, "at": DateTime, "channel": "in-person" \| "holder-ui" \| "signed-message" \| "steward" \| "other", "evidenceRef"?: LocalId}` | yes | — | How the person expressed it. An agent's statement that "the person agreed" is never `expressedBy`: consent is not relayed. |
| `note` | string | no | — | Written for the person. It MUST NOT quote record content (G3). |

**Consent.** Explicit consent is the person's confirmation of the whole agreement, as the holder shows it in the person's own window (`expressedBy`), never the ticks on it. Rows and terms the holder shows already ticked, special records included, are consented to this way: the person unticks what they do not want and confirms the rest. Whether this meets every legal test of explicit consent is not established here; a legal review precedes any publication ([STATUS](../STATUS.md)).

**Status (computed).**

- `given` from `recordedAt`;
- `withdrawn` after a subject or steward `withdraw-grant` Review;
- `revoked` after a holder `revoke-grant` Review;
- `expired` at `expiresAt`, once `maxUses` is exhausted, or from the moment a renewal is given (a later Grant to the same grantee whose `renews` names it), so that a narrower renewal is never undercut by the grant it replaces;
- `invalidated` when the grantor steward's scope or validity has ended, or when the grantee Party is removed.

Requested, refused and deferred grants exist only as messages and Events ([EXCHANGE.md](EXCHANGE.md)); they are never stored Grants.

**Invariants.**

- **GR-1.** `expiresAt` is present and after `recordedAt`. For an allow grant the duration is at most P1Y, and at most P180D when the grant includes `infer` or reaches special records (R-G10). A deny grant (a refusal) is not capped: it lasts as long as the person sets.
- **GR-2.** The constraints `forwarding`, `crossContextUse` and `delegable` are `false`; `decisionUse`, when present, is `deny` or `approval-required`.
- **GR-3.** `open-verbatim` requires `stepUp.required: true`, a `maxDuration` of at most PT1H, and `maxSourceTier: verbatim`.
- **GR-4.** `infer` requires at least one purpose and `explicit-consent`.
- **GR-5.** The grantee is a Party.
- **GR-6.** No selector in an allow grant reaches `special` by wildcard (R-G3). Statically, `tiers` contains `special` only together with `ids`, `categories` or `lenses`. For GR-1 and GR-4 a grant also "reaches special" when an include selector matches a record that is special now and names it as R-G3(b) requires.
- **GR-7.** `effect: deny` grants have no `actions` and no `mode`.
- **GR-8.** A steward grantor has `grant` in scope and is valid at `recordedAt`.
- **GR-9.** `actions` never contains `grant`. Issuing grants is a steward scope action only (§9.1); a grantee never grants (R-G12).

**Example** (Noa's grant to the reflection companion).

```json
{"id": "g-02", "recordedAt": "2026-09-01T10:00:00Z", "grantor": "subject", "grantee": "a-02",
 "purposes": ["self-reflection", "recall-support"],
 "scope": {"include": [
             {"kinds": ["Episode", "Interpretation", "ModelView", "Practice", "Outcome", "Pattern", "RecallCue"]},
             {"facets": ["goal", "declared-value", "state", "preference"]},
             {"lenses": ["urn:ohc:lens:cbt"]},
             {"ids": ["src-02"]}],
           "exclude": [{"categories": ["intimate", "health"]}]},
 "actions": ["read", "suggest", "infer", "source-index", "source-summary", "cite-excerpt", "open-verbatim", "recall"],
 "mode": "full", "interpretations": "all", "maxSourceTier": "verbatim",
 "constraints": {"expiresAt": "2027-01-31T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "stepUp": {"required": true, "maxDuration": "PT30M"}, "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-01T10:00:00Z", "channel": "holder-ui"}}
```

### 12.2. Grant vocabularies

**Actions** (closed). Content ladder `read` ⊂ `suggest` ⊂ `write`:

- `read`: receive projections.
- `suggest`: also file Proposals and feedback.
- `write`: also write records directly. These are still `proposed` for non-subject writers (R-A1).

Separate actions:

- `infer`: create or propose records with `origin: inferred`. Required by INF-1 and PR-2. **Never implied by `write`** (R-G11).
- Source ladder `source-index` ⊂ `source-summary` ⊂ `cite-excerpt` ⊂ `open-verbatim`. `open-verbatim` requires step-up (§15.4).
- `answer`: receive `ohc.answer` messages derived from records in scope.
- `export`: receive a full export of the scope (portability to another holder the person names).
- `recall`: use RecallCues in scope.
- `grant`: steward scopes only (`Steward.scope.actions`). Allows issuing grants. It never appears in a Grant's `actions` (GR-9).

**Steward scope actions** are the Review actions (§11.1) plus `write`, `infer`, `grant` and `open-verbatim`.

**Modes** (closed):

| Code | Definition |
|---|---|
| `full` | Records with all fields allowed by §12.3. |
| `summary` | Records without their support. A Claim keeps only `id`, `facet`, `predicate`, `horizon`, `text`, `absence`, `valid` and `contexts`. Every other kind drops `evidence`, `grounds`, `counterEvidence`, `confidence`, `rationale`, `derivedFrom`, `generatedBy`, `importedFrom` and `note`, and an AssessmentRecord also drops `source` (PJ-8). An Episode keeps, in each account, only `narrator`, `narratedAt`, `addedAt`, `accountKind`, `happened`, `didOrTried` and `lang`: never `experienced`, `affectTags`, `understandingThen`, `text` or `evidence`. Status travels in `derived` (§14.1). |
| `rule-only` | Only the facets `boundary`, `preference` and `commitment`, plus the `state` predicates `availability` and `load`, rendered as their `text`. Nothing else. |
| `answer-only` | No records. Only `ohc.answer` replies to questions ([EXCHANGE.md](EXCHANGE.md)). |

**Interpretations policy** (closed):

| Code | Definition |
|---|---|
| `none` | No interpretation-layer records. |
| `subject-endorsed` (default) | Interpretation-layer records authored by the subject or endorsed by the subject. |
| `all` | Every admitted interpretation-layer record in scope. |

**Grant status** (computed; closed): stored grants are `given`, `withdrawn`, `revoked`, `expired` or `invalidated`. The statuses `requested`, `refused` and `deferred` exist only in messages and Events.

**Resolvers** (multi-holder disputes; closed):

| Code | Definition |
|---|---|
| `returnDialog` (default) | Return both values marked contested and ask the person. |
| `mostPersonal` | Prefer the value the subject asserted or endorsed. |
| `mostRecent` | Prefer the newest by `recordedAt`. Only for `state` facets. |
| `returnNone` | Return `not-disclosed`. Used whenever any holder marks the item `person-only`. |

**Channels** (`expressedBy.channel`; closed): `in-person`, `holder-ui`, `signed-message`, `steward`, `other`.

### 12.3. Grant evaluation and projection

This algorithm is normative. It is the only way OHC content leaves the holder.

```text
Input: q = {requester P, grant g, purpose u, select [GrantSelector], asOf?, mode?, withoutInterpretations?}; time now.

 1. Authentication of P is transport-level and outside OHC. If g.grantee != P: deny(not-granted).
 2. status(g) at now MUST be "given"; notBefore <= now < expiresAt; uses < maxUses; u is in g.purposes;
    u is not in §8.10; the action is in g.actions (ladder §12.2). On failure, deny with one of
    not-granted | expired-grant | purpose-mismatch. These codes describe the grant, never the data (H-5).
 3. S := the records known at (asOf or now), by Review replay. Remove Tombstones and superseded records.
    Keep only admission = active, except the proposer view (§12.5): with q.ownProposals, also keep P's own
    records that are proposed or that expired undecided.
 4. Remove records whose endorsement is "rejected" (only the subject sees them). Keep contested records; their
    derived.contested is true.
 5. For each record, compute the effective disclosure: tier (C3), categories, handling, audience,
    with restrict/relax Reviews applied. Remove every record with handling "person-only".
 6. Remove every record matched by an effect:"deny" grant for P (R-G2).
 7. Keep a record only if it matches at least one include selector and no exclude selector of g, AND:
      tier special  -> the matching selector names it by ids, by lenses, or by one of the record's categories
                       whose minimum tier is special (§8.2), AND g.basis.legal = explicit-consent  (R-G3(b))
      tier sensitive, or audience "named" -> the matching selector names it by ids, categories, lenses,
                       kinds or facets (not only all, tiers, horizons or contexts)     (R-G3(a))
    Tension: every member of `between` must pass, else remove it silently (no flag).
    Relation: both endpoints must pass. Outcome and RecallCue: every target must pass.
    Purpose recall-support: keep an Episode only if its computed recall is ask-each-time or permitted.
 8. Interpretation layer (Interpretation, ModelView, Pattern, Tension, Part):
      g.interpretations = none -> remove all; subject-endorsed -> keep only those asserted by the subject,
      or endorsed / partly endorsed by the subject; all -> keep. q.withoutInterpretations -> remove all.
      frame-relative records require a selector naming their lens.
 9. Compute freshness (§7.2), endorsement, contested, locked, admission and heldNow, and the label (§6.6).
10. Transform by mode (§12.2). Drop kind, underGrant, recordedBy, importedFrom.run and ext; drop Subject links.
    Sources go to tier t = min(source action in g, g.maxSourceTier, source.maxRelease, custody ceiling §15.3):
      index/summary -> no sha256; "handle" = HMAC handle (R-V1)
      excerpt       -> plus excerpts only for spans cited by served records:
                       {handle, selector (with a text-quote selector generated now), text}, third parties redacted
      verbatim      -> never inside a projection; only through ohc.source-content after §15.4
    Party references: include only the referenced Parties, with their pseudonymous labels.
    Each served record's handling codes go to obligations.handling[id].
11. subjectAlias := "urn:ohc:alias:" + lower(base32(HMAC-SHA256(K_holder, subject.id + "|" + P)))[0:26]
12. absences: for every selector in q.select that g does not cover, emit {selector, code: "not-disclosed"},
    whether or not matching records exist (R-G5). No counts. No per-record absences.
    completeness = "partial"; omissions = "hidden".
13. validUntil := min(g.expiresAt, storage limit: none -> generatedAt; session -> generatedAt + PT12H;
    until-expiry -> g.expiresAt). Add nonce. digest := sha256(JCS(projection without digest)).
14. Append Event projection-served {grant, purpose, records: ids, message: projection id}. Count one use.
```

**The second channel.** Verbatim source content leaves the holder only through `ohc.source-content` ([EXCHANGE.md](EXCHANGE.md)). It is gated by the same steps 1–7 for every target Source, and in addition by the step-up of §15.4. There is no third channel.

**Separation guarantee.** Statements and interpretations travel in different top-level members of the Projection (§14.1). A consumer that reads only `statements` never meets a reading.

### 12.4. Grant rules

- **R-G1.** Default deny. Nothing reaches a grantee without an allow grant.
- **R-G2.** Deny wins over allow.
- **R-G3.** Sensitivity ceiling:
  - (a) a sensitive tier or `named` audience requires a selector that names the record by kind, facet, category, lens or id;
  - (b) a special tier requires a selector that names it by id, by lens, or by one of its categories whose minimum tier is `special`, under `explicit-consent`. A `workplace` or `third-party` category never reaches a special record;
  - (c) `person-only` is never served.
- **R-G4.** Action ladders: `read` ⊂ `suggest` ⊂ `write`; `source-index` ⊂ `source-summary` ⊂ `cite-excerpt` ⊂ `open-verbatim`. `infer`, `answer`, `export`, `recall` and `grant` are separate.
- **R-G5.** `not-disclosed` is returned regardless of existence.
- **R-G6.** Check at use. Nothing is used after `validUntil`.
- **R-G7.** One purpose per request.
- **R-G8.** Interpretations follow the grant's `interpretations` policy and the request's `withoutInterpretations`.
- **R-G9.** A grant never authorises action in the world. Authority to act stays in ODE policies or the runtime.
- **R-G10.** Every allow grant expires: at most P1Y, and at most P180D with `infer` or when it reaches special records. A renewal is a new grant (`renews`); nothing is extended automatically. A refusal (`effect: deny`) is not capped.
- **R-G11.** `infer` is separate, needs `explicit-consent` and a named purpose, and is never implied by `write`.
- **R-G12.** `delegable: false`. A grantee never re-shares and never grants.
- **R-G13.** A grantee is a Party, never a Part. A LensAdoption never gives access.
- **R-G14.** Decisions on the basis of results and readings. `constraints.decisionUse` covers AssessmentRecords, Interpretations and records with `origin: inferred`; everything else served is used as before, and carrying out what the person stated is never governed by it. `deny` (member absent): such records never ground a choice the grantee makes or proposes for the person. `approval-required`: such a record the person stated or accepted (label `stated` or `confirmed`; for `partly-confirmed`, the parts named as fitting in `endorsedPart`, PJ-8) may ground a choice the grantee proposes for the person; the grantee names the records it weighed, and the person confirms the proposal before it takes effect, one confirmation per proposal; silence is not confirmation (C-9). Under both codes, records that need confirmation first still need it (C-3), and no code opens a prohibited purpose (§8.10, C-6), `significant-automated-decision` included. `obligations.decisionUse` is always present (§14.1).
- **R-L0.** A link is not access: Subject links, Relations and ODE references grant nothing.

The vault rules V-0…V-6, R-V1 and SU-1…SU-7 are in §15; INF-1 is in §3.4; R-A1 is in §6.4; R-X3 and R-X4 are in §8.8.

**Employers and schools (informative).** When the grantee's operator is the person's employer or school, consent is presumed not to be freely given (GDPR Recital 43, Art. 7(4) and Art. 88; [COMPOSITION.md](COMPOSITION.md#legal-hooks)). The holder should then be the person, or a party independent of that organisation, and grants should be narrow: `rule-only` or `summary` mode, no `infer`, and no special records. The holder's agreement screen then pre-ticks nothing and says why (IMH-1). A typed operator relation is an open question for 0.2 ([STATUS](../STATUS.md)).

### 12.5. Proposer view

A proposer sees its own proposals. Under the same grant and purpose, a request with `ownProposals: true` ([EXCHANGE.md](EXCHANGE.md)) also receives the requester's own records that are still `proposed`, and those that expired undecided (§12.3, step 3).

- They pass the same steps 4–10 and carry their computed status: `pending` while proposed, `not-accepted` once expired. "Expired" means "not admitted by the person", not "gone"; the proposer re-proposes only with new grounds (C-2).
- The projection carries `ownProposals: true`. C-3 applies, and nothing in a proposer view is ever served onward or to anyone else.
- A batch reconciliation at the cadence the person sets (`reviewCadence`) is the usual way to settle open proposals ([CONTEXT-09](../docs/agents/procedures/CONTEXT-09.md)).

## 13. Event log

### 13.1. Event

Layer `governance` · module `governance` · normative-draft. An append-only log of writes, disclosures, access, step-ups, notices, imports, exports and restores. It serves as the access-receipt trail. **Events carry ids, codes and times only. They never carry text, values, quotes, selectors' quoted text or content digests (G3).** The log is a salted hash chain that survives erasure (§13.2).

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `kind` | const `"Event"` | ctx | — | |
| `id` | LocalId | yes | prefix `e-` | |
| `seq` | int | yes | — | Strictly increasing from 1. |
| `at` | DateTime | yes | — | |
| `eventType` | string | yes | below | |
| `actor` | Actor | yes | — | |
| `counterparty` | Actor | no | — | A grantee, proposer or recipient. |
| `grant` | LocalId | no | — | |
| `purpose` | string | no | §8.9 | |
| `records` | [LocalId] | no | — | Record ids only. |
| `message` | string | no | — | The id of a message or a Projection. |
| `outcome` | string | no | `served`, `denied`, `asked`, `confirmed`, `declined`, `timeout`, `acknowledged`, `purged`, `failed` | |
| `reason` | string | no | reason codes below | |
| `tier` | string | cond | §15.3 | REQUIRED on `source-opened`: the release tier served. |
| `confirmationDigest` | string | cond | — | On `step-up-confirmed`: `"sha256:" + hex`, over the request parameters only (SU-5). |
| `salt` | string | yes | — | At least 16 random bytes, base64url. |
| `prev` | string | yes | — | `"sha256:" + hex`: the `entryDigest` of the previous Event. The first Event uses 64 zeros. |
| `entryDigest` | string | cond | — | Present only on redacted stubs (§13.2). |
| `redacted` | boolean | cond | — | `true` only on stubs. |

**Event types** (closed):

| Group | Event types |
|---|---|
| Writes | `record-written`, `record-proposed`, `record-admitted`, `record-declined`, `record-retracted`, `review-written`, `record-erased` |
| Grants | `grant-given`, `grant-withdrawn`, `grant-revoked`, `grant-request-received`, `grant-request-refused`, `grant-request-deferred` |
| Disclosure | `projection-served`, `answer-served`, `request-denied` |
| Proposals and feedback | `proposal-received`, `proposal-refused`, `ask-first`, `feedback-received`, `use-report-received` |
| Vault | `source-access-requested`, `step-up-confirmed`, `step-up-declined`, `source-opened` |
| Recall | `recall-offered` |
| Notices | `revocation-notice-sent`, `erasure-notice-sent`, `erasure-notice-acknowledged`, `purge-receipt-received` |
| Imports, exports and backups | `import-run`, `export-run`, `backup-created`, `backup-restored`, `tombstones-reapplied` |
| Log maintenance | `chain-resealed`, `redacted` (used on stubs only) |

**Disclosure Events** are `projection-served`, `answer-served`, `export-run` and `source-opened`: the Events that record content reaching a party. Erasure notices follow them (EV-6, §15.5), grants cover them (EV-7), and H-2 requires them.

**Reason codes** (closed): `not-granted`, `infer-not-granted`, `expired-grant`, `purpose-mismatch`, `special-needs-explicit-consent`, `step-up-required`, `step-up-timeout`, `person-only`, `locked`, `quota-exceeded`, `subject-declined`, `holder-policy`, `security`, `legal`, `retention`. Codes returned to a grantee describe the grant or the request, never the data (H-5).

**Invariants.**

- **EV-1.** `seq` is contiguous.
- **EV-2.** The chain verifies: `entryDigest(e) = sha256(JCS(e without "entryDigest" and "redacted"))`, and each `prev` equals the previous entryDigest. For a stub, the stored `entryDigest` is used.
- **EV-3.** No field contains free text. The schema has no free-text fields.
- **EV-4.** Every Projection in `projections/` has a `projection-served` Event.
- **EV-5.** Every `source-opened` with tier `verbatim` follows a `step-up-confirmed` for the same grant within its `maxDuration`, and:
  - the `step-up-confirmed` actor is the subject, or a steward with `open-verbatim` in scope when the Source is not special (SU-2);
  - its `records` include every opened Source id;
  - a Source with effective tier `special` is opened at most once per step-up (SU-3);
  - the Event's grant has `open-verbatim`, `maxSourceTier: verbatim` and `stepUp.required`, and the Source's own `maxRelease` is `verbatim`.
- **EV-6.** Every `record-erased` whose record appeared in an earlier disclosure Event is followed by `erasure-notice-sent` to each such counterparty.
- **EV-7.** Every disclosure Event names a grant whose grantee is the counterparty, whose status was `given` at `at`, and whose purposes include the Event's purpose. Every listed record was servable under §12.3 at `at` (for `source-opened` and `step-up-confirmed`, under steps 3–7 and §15.4). For a stored projection, the Event's records equal the records the projection serves. Records erased after the Event are skipped.

**Example** (the Event for Noa's projection `prj-0007`).

```json
{"id": "e-0060", "seq": 60, "at": "2026-09-24T07:30:00Z", "eventType": "projection-served", "actor": "holder",
 "counterparty": "a-02", "grant": "g-02", "purpose": "recall-support", "records": ["pr-01", "ep-03", "oc-01"],
 "message": "prj-0007", "outcome": "served", "salt": "0RrMt6hVnOPeFxqYjZrwQg",
 "prev": "sha256:f6eedfa32bc90cba6049c9946ee62715a813b2eba17f4137b12cae6105fa6d82"}
```

### 13.2. Hash chain, redacted stubs and re-seal

```text
entryDigest(e) = "sha256:" + hex(sha256(JCS(e minus {"entryDigest", "redacted"})))
e[1].prev      = "sha256:" + "0" * 64
e[n].prev      = entryDigest(e[n-1])
```

**Redacted stubs.** If an Event itself must be removed (for example on the person's request, where no retention duty applies), it is replaced by a stub. Noa's `e-0050`, an id-only entry about the reading she later erased, is one:

```json
{"id": "e-0050", "seq": 50, "at": "2026-09-21T09:40:00Z", "eventType": "redacted",
 "prev": "sha256:085a06c49b09f5d4069331ae09dc3b29c18f60f2e32ec076d9f520eaf6ab6d88",
 "entryDigest": "sha256:f57559eabf7be35aba3d9ea5b00c8221cbb53ccc58484a358aecaa06eaf980ab", "redacted": true}
```

- The original's `salt` makes `entryDigest` unguessable.
- Verification uses the stored `entryDigest` for stubs, so the chain stays intact.

**Re-seal.** If a chain must be rebuilt (for example after corruption), the holder writes a `chain-resealed` Event whose `records` is empty and whose `reason` is `holder-policy`, and starts a new segment from the head. The old segment is kept, or erased under §15.5.

## 14. Projection, ContextLock and package layout

### 14.1. Projection

Document · module `governance` · normative-draft. What one grantee actually receives for one purpose at one time. It is computed by §12.3 and is the **only** form in which OHC content leaves the holder. It carries computed status, keeps statements apart from interpretations, and is never an existence oracle.

| Field | Type | Req | Notes |
|---|---|---|---|
| `format` | const `"ohc.projection"` | yes | |
| `specVersion` | const `"0.1.0-draft"` | yes | |
| `id` | LocalId | yes | Prefix `prj-`. |
| `context` | `{"id": URI, "version": string}` | yes | |
| `subjectAlias` | URI | yes | Pairwise per grantee (§12.3, step 11). The subject id is never included. |
| `grantee` | Actor | yes | |
| `grant` | LocalId | yes | |
| `request` | string | no | The `ohc.request` message id. |
| `purpose` | string | yes | Exactly one (R-G7). |
| `mode` | string | yes | §12.2 |
| `asOf` | DateTime | no | The as-known-at time, if requested. |
| `ownProposals` | const `true` | no | Present when this is a proposer view (§12.5). |
| `generatedAt` | DateTime | yes | |
| `validUntil` | DateTime | yes | Not later than the grant's expiry and the storage limit. |
| `nonce` | string | yes | At least 16 random bytes, base64url, so that the digest cannot be guessed. |
| `parties` | [Party] | no | Only the Parties referenced by served records, pseudonymous. |
| `statements` | `{"claims"?: [...], "practices"?: [...], "lensAdoptions"?: [...], "assessments"?: [...], "healthRefs"?: [...]}` | no | Assertion-layer records. |
| `experience` | `{"episodes"?: [...], "sources"?: [...]}` | no | Sources only at their served tier (§15.3). |
| `interpretations` | `{"interpretations"?: [...], "modelViews"?: [...], "patterns"?: [...], "tensions"?: [...], "parts"?: [...]}` | no | **Always separate from `statements`.** Absent when the grant says `interpretations: none` or the request says `withoutInterpretations`. |
| `recall` | `{"recallCues"?: [...], "outcomes"?: [...]}` | no | |
| `links` | `{"relations"?: [...]}` | no | Relations whose both endpoints are served. |
| `derived` | object `id → {"label", "freshness", "endorsement", "contested", "locked", "admission", "heldNow"?, "endorsedPart"?, "computedAt"}` | yes | One entry per served record (§6.6). `endorsedPart`: PJ-8. |
| `absences` | [`{"selector": GrantSelector, "code": "not-disclosed"}`] | no | One entry for each requested selector that the grant does not cover. It is returned **whether or not matching records exist** (R-G5). |
| `completeness` | const `"partial"` | yes | A projection never claims completeness. |
| `omissions` | const `"hidden"` | yes | 0.1 never reports counts or kinds of what was withheld. |
| `obligations` | `{"storage", "forwarding": false, "crossContextUse": false, "decisionUse", "delegable": false, "handling": {"<id>": [code]}}` | yes | Copied from the grant and the records. `decisionUse` is always present: `deny` when the grant has no member (R-G14). `handling` lists, per served record, its effective codes (§8.5), for example `no-quote-back`. |
| `digest` | string | yes | `"sha256:" + hex(sha256(JCS(projection without "digest")))`. |

Served records keep their stored fields, except for the transforms of §12.3, step 10, which this list restates:

- `kind`, `underGrant`, `recordedBy`, `importedFrom.run`, `ext` and Subject links are dropped (the member a record sits in gives its kind);
- the mode reduces fields as §12.2 says (in `summary` mode an AssessmentRecord also drops `source`, PJ-8);
- Sources are cut to their served tier; spans keep `text-position`, `media-time` and `page` selectors;
- excerpts appear only at the `excerpt` tier, in `experience.sources[].excerpts`;
- only the Parties referenced by served records are included, with their pseudonymous labels.

**Invariants.**

- **PJ-1.** The digest verifies.
- **PJ-2.** No record appears that §12.3 would not serve (replay at `generatedAt`).
- **PJ-3.** There are no count fields anywhere.
- **PJ-4.** No served record carries an inferred psychological, state or value item unless the grant has `interpretations: all`, or the item is subject-endorsed.
- **PJ-5.** No `contested` flag on a Tension; Tensions with any member outside the grant are absent.
- **PJ-6.** `subjectAlias` is not the subject id.
- **PJ-7.** Replaying §12.3 at `generatedAt` yields exactly the stored record set.
- **PJ-8.** The person's words on a partly endorsed record. When a served record's endorsement is `partial`, its `derived` entry carries `endorsedPart`: the text of the latest `partially-endorse` Review. A holder that lets the person mark scales writes that text as "Fits: … Does not fit: …" from the scales the person marked, followed by the person's own words; a scale named in neither part is not decided (C-3, C-8). The parts named there as fitting count as confirmed by the person (C-3). In `summary` mode an AssessmentRecord also drops `source` (§12.2).

**Example** (Noa's work assistant, summary mode, no interpretations):

```json
{"format": "ohc.projection", "specVersion": "0.1.0-draft", "id": "prj-0003",
 "context": {"id": "urn:ohc:example:noa:context", "version": "2026-10-09.4"},
 "subjectAlias": "urn:ohc:alias:cgkknm2urepzjn6a6qmvpmz5yc", "grantee": "a-01", "grant": "g-01",
 "purpose": "scheduling", "mode": "summary", "generatedAt": "2026-10-09T09:00:00Z",
 "validUntil": "2026-10-09T21:00:00Z", "nonce": "DI3JTwOnH_IdBefaKAvZ3A",
 "statements": {"claims": [{"id": "c-05", "facet": "boundary", "text": "No calls before 10:00.", "horizon": "foundation", "contexts": ["work"]}, {"id": "c-06", "facet": "preference", "predicate": "decision-brief", "text": "Before a hard conversation, send me the numbers on one page.", "horizon": "focus", "contexts": ["work"]}]},
 "derived": {"c-05": {"label": "stated", "freshness": "current", "endorsement": "endorsed", "contested": false,
                      "locked": false, "admission": "active", "computedAt": "2026-10-09T09:00:00Z"},
             "c-06": {"label": "stated", "freshness": "current", "endorsement": "endorsed", "contested": false,
                      "locked": false, "admission": "active", "computedAt": "2026-10-09T09:00:00Z"}},
 "absences": [{"selector": {"facets": ["state"]}, "code": "not-disclosed"}], "completeness": "partial",
 "omissions": "hidden",
 "obligations": {"storage": "session", "forwarding": false, "crossContextUse": false, "decisionUse": "deny",
                 "delegable": false, "handling": {}},
 "digest": "sha256:caf0d73af1d2c5f2335ac8001dbed7c1329b5ff1310080ca853b90b62b314896", "request": "msg-0402"}
```

### 14.2. ContextLock

Document · module `governance` · normative-draft. An integrity lock over the package files, except the vault (whose objects are named by their hashes) and the lock itself. It is not a signature.

| Field | Type | Req | Notes |
|---|---|---|---|
| `format` | const `"ohc.lock"` | yes | |
| `specVersion` | const `"0.1.0-draft"` | yes | |
| `context` | `{"id": URI, "version": string}` | yes | It MUST equal the manifest. |
| `algorithm` | const `"sha256"` | yes | |
| `files` | object `path → "sha256:" + hex` | yes | File bytes. It covers `context.json`, `records/**`, `events.jsonl`, `projections/**` and `lenses/**`. |
| `createdAt` | DateTime | yes | |

**Invariants.**

- **LK-1.** Every listed file exists and its hash matches.
- **LK-2.** No unlisted file exists outside `vault/` and `ext/`.
- **LK-3.** The context id and version match the manifest.

**Example** (Noa's lock, abridged to one file).

```json
{"format": "ohc.lock", "specVersion": "0.1.0-draft",
 "context": {"id": "urn:ohc:example:noa:context", "version": "2026-10-09.4"}, "algorithm": "sha256",
 "createdAt": "2026-10-09T09:05:00Z",
 "files": {"context.json": "sha256:7691209567e5928032682d99eb48843620beda362f1baf96ace5cb17b1b63af2"}}
```

### 14.3. Package layout

This layout is normative for L2.

```text
<context-dir>/
  context.json                     manifest (format ohc.context, with "collections")
  records/
    claims.jsonl  relations.jsonl  sources.jsonl  episodes.jsonl  interpretations.jsonl  tensions.jsonl
    reviews.jsonl  proposals.jsonl  grants.jsonl  lens-adoptions.jsonl  assessments.jsonl  model-views.jsonl
    practices.jsonl  outcomes.jsonl  patterns.jsonl  recall-cues.jsonl  parts.jsonl  health-refs.jsonl
  events.jsonl                     Event log (salted hash chain)
  projections/<prj-id>.json        stored projections (holder-side; subject-visible)
  lenses/<name>@<version>.lens.json   pinned descriptor copies (optional)
  lenses/<name>@<version>.playbook.json   pinned playbook copies (optional; LENSES.md §2.2)
  vault/<2hex>/<sha256>.<ext>      primary sources (per-object encryption RECOMMENDED: crypto-shredding)
  ext/gum/sidecar.jsonl            binding.gum export sidecar (optional)
  context.lock.json                ContextLock
```

- Every JSON Lines line is one record, in RFC 8785 canonical form (JCS). Lines are ordered by `recordedAt`, then by id. Tombstones keep their position.
- Paths have no leading `/`, no `\`, no `..` and no `:`.

## 15. Vault, release tiers, step-up, erasure, export and multi-holder

### 15.1. Model

**Holder.** The holder keeps the context and the vault, evaluates grants and serves projections. It may be the person's own store, a personal agent acting as holder (§15.9), or a router.

**The vault and the metadata.**

- **Source records** are metadata. They are part of the context and travel in exports.
- **Vault objects** are the primary bytes. They are content-addressed (`vault/<2hex>/<sha256>.<ext>`). Encrypting each object under its own key is RECOMMENDED, so that erasure can be done by destroying the key (crypto-shredding).

**Release tiers** (§15.3) apply per grantee and per Source. The effective tier is `min(grant source action, grant.maxSourceTier, source.maxRelease, custody ceiling)`. `verbatim` additionally requires step-up (§15.4).

- **V-0.** The subject always has every tier over their own vault. Grantee redactions are never applied to the subject. Access to the primary material is what lets a person work with selective memory.

### 15.2. Flows

| Flow | Trigger | Steps | Events |
|---|---|---|---|
| **F1 Ingest** | The person or an importer adds material | Hash → store under `vault/` (encrypted) → write a Source record (`maxRelease` default per §10.1) → optionally write Episode accounts citing spans | `record-written` or `import-run` |
| **F2 Ordinary read** | `ohc.request` | §12.3 evaluation → Projection, with Sources at `index` or `summary` | `projection-served` |
| **F3 Excerpt** | `ohc.request` under a grant with `cite-excerpt` | §12.3 → spans cited by served records are released as excerpts, with third parties redacted and per-grant HMAC handles | `projection-served` |
| **F4 Verbatim** | `ohc.source-access-request` | §15.4 step-up → `ohc.source-content` with `storage: none` | `source-access-requested`, `step-up-confirmed` or `step-up-declined`, `source-opened` |
| **F5 Subject revisit** | The person opens their own source, account or reading | No grant needed. A viewer shows "then and now": accounts, `heldDuring`, counter-evidence | none required (MAY log) |
| **F6 Revocation and erasure** | The person withdraws a grant, or asks to erase | §15.5 | `grant-withdrawn` → `revocation-notice-sent`; `record-erased` → `erasure-notice-sent` → `erasure-notice-acknowledged` / `purge-receipt-received` |

### 15.3. Release tiers, custody, spans and handles

**Release tiers** (ordered; closed; also used for `maxRelease`, `maxSourceTier` and a RecallCue's `offer.maxTier`):

| Tier | Grantee receives |
|---|---|
| `none` | Nothing. References resolve as `not-disclosed`. |
| `index` | `sourceKind`, `mediaType`, a coarse `capturedAt` (day), `contemporaneity` and the `authorship` role. **No `sha256`, no title, no summary.** A per-grant HMAC handle is given instead (R-V1). |
| `summary` | Index, plus `title` and `summary.text`, with `summary.authoredBy` ("whose selection"). |
| `excerpt` | Summary, plus the text of the spans cited by served records. Third parties are redacted. Text-quote selectors and a per-grant HMAC of each span are generated at serve time. |
| `verbatim` | The full primary content with redactions applied. Only through step-up (§15.4). |

The subject always has every tier (V-0).

**Custody ceilings** (closed):

| Confidentiality | Ceiling without a release | Ceiling with a valid `releaseRef` |
|---|---|---|
| `none` | as set | as set |
| `therapy` | `index` | `summary` (never excerpt or verbatim to grantees in 0.1) |
| `coaching` | `index` | `excerpt` |
| `legal` | `index` | `summary` |
| `medical` | `index` | `index` (pointers belong in HealthRef) |

- **R-V1.** No guessable digests. A grantee below the `excerpt` tier never receives a content `sha256`, a span digest or quoted text, and a grantee below the `summary` tier never receives a title. Where a stable reference is needed, the holder gives a **per-grant HMAC handle**. Handles differ between grants, so two grantees cannot correlate them. Records never store quote digests, and Events never store content digests (G3).

```text
handle = "hmac:" + base64url(HMAC-SHA256(K_g, sourceId + "|" + JCS(selector)))
K_g    = HKDF-SHA256(K_holder, info = "ohc-grant|" + grantId)
```

- **V-1.** Excerpts are generated at serve time, only for spans cited by served records, and only at the `excerpt` tier or above.
- **V-2.** Third-party protection. Spans that cover a third party's words or details are redacted at the excerpt and verbatim tiers for grantees, unless the Source's `redactions` already handle them. The holder applies `redact` Reviews. Sources with `containsThirdParty: true` default to `maxRelease: index`.
- **V-3.** Citations are span-level. Every Episode account, Interpretation ground and Claim evidence that rests on a Source cites a Span. The selectors follow §5.9. `text-quote` selectors exist only in served excerpts.
- **V-4.** Custody ceilings cannot be raised by any grant. `therapy` material never goes beyond `summary` to grantees in 0.1.
- **V-5.** Summaries are shown with `summary.authoredBy`: "a selection by <author>".

### 15.4. Step-up for verbatim access

```text
Agent ──ohc.source-access-request──▶ Holder
   {grant, purpose ∈ grant.purposes, targets: [{source, selector?}] or [handle], why (shown to the person verbatim),
    requestedDuration ≤ PT1H, audience: "subject-only" (default) | "grantee"}
Holder: check the grant (open-verbatim, maxSourceTier verbatim, custody ceiling, not person-only), and that every
        target Source passes §12.3 steps 3-7 under that grant now (admitted, not denied, in scope, named per R-G3)
        ── else ohc.denial
Holder ──out-of-band prompt──▶ Person (holder UI or signed channel NOT controlled by the requesting agent)
Person ──confirm / narrow / decline──▶ Holder         (no answer within PT10M ⇒ decline)
Holder: Event step-up-confirmed {grant, records:[source ids], outcome: confirmed, confirmationDigest}
        or Event step-up-declined {outcome: declined | timeout}
Holder ──ohc.source-content──▶ Agent  {verbatim with redactions, storage: "none", forwarding: false, validUntil ≤ confirmedAt + maxDuration}
Holder: Event source-opened per open (tier: verbatim)
Agent output that quotes MUST cite the span and show it only to the stated audience.
```

- **SU-1.** The step-up duration is at most PT1H, with a default of PT30M from `grant.stepUp.maxDuration`. Restoring a backup never revives a step-up.
- **SU-2.** Confirmation is **out-of-band**, from the subject or from a steward with an explicit vault mandate (`scope.actions` ∋ `open-verbatim`; never for special material). **An agent never confirms.** EV-5 checks this in the log.
- **SU-3.** For material with effective tier `special`, a step-up covers **one request** and one opening. For other material it covers the session, up to `maxDuration`. EV-5 checks this in the log.
- **SU-4.** Timeout or silence means decline.
- **SU-5.** `confirmationDigest` covers request parameters only, never content. It is computed as follows.

```text
confirmationDigest = "sha256:" + hex(sha256(JCS({request, grant, purpose, targets, why, expiresAt, confirmedBy, at, nonce})))
```

- **SU-6.** Verbatim content is served with `storage: none` and never enters a Projection.
- **SU-7.** Verbatim access to material whose author is a third party needs that party's recorded consent (a Source of kind `consent-document`, cited in `custody.releaseRef`), or redaction.

### 15.5. Revocation and erasure

**Withdrawal of a grant.**

1. A Review `withdraw-grant` by the subject is written.
2. The holder stops serving at once.
3. The holder MUST send `ohc.revocation-notice {grant, at, purgeBy}` to the grantee.
4. The grantee purges data under the grant's storage terms and acknowledges.
5. Events: `grant-withdrawn` and `revocation-notice-sent`.

**Erasure.** The person's right outranks append-only.

1. **Request.** The subject, or a steward in scope (never for special material), names the record ids and chooses a cascade: `only`, or `with-dependents`.
   - The holder MUST show the computed dependents first: records whose `about`, `grounds`, `evidence`, `episodes`, `targets` or `hypotheses` reference **only** erased records, plus stored projections containing them.
   - Erasing a Source never forces erasure of readings that cite other evidence too. Their spans simply render as `[erased source]`.
2. **Replace.** Each erased record becomes a Tombstone in place (§11.3).
   - Vault objects are deleted, or their keys destroyed. No vault object outlives its Source (V-6).
   - Governance records follow the content they concern, whatever the cascade chosen: a Review whose targets are all erased, and a Proposal whose items are all erased, become Tombstones too (`erasedKind` `Review` or `Proposal`). A Review with some targets left loses `note` and `endorsedPart`; a Proposal with some items left has its `rationale` replaced by `"[erased]"`.
   - Stored projections containing erased records are deleted. Their `projection-served` Events remain; they hold ids only.
   - The holder adds each erased id, with `erasedAt`, to its content-free **erasure ledger**.
3. **Log.** Event `record-erased {records: ids}`.
4. **Notify.** For every counterparty that received any erased record (found from the disclosure Events, §13.1: `projection-served`, `answer-served`, `export-run` and `source-opened`), the holder MUST send `ohc.erasure-notice {records: ids, erasedAt, purgeBy}` (`purgeBy` default: P7D), and writes Event `erasure-notice-sent`.
5. **Acknowledge.** The recipient MUST purge and reply `ohc.purge-ack {status: purged | not-held | failed}`. The holder writes Events `erasure-notice-acknowledged` and `purge-receipt-received`. If no acknowledgement arrives by `purgeBy`, the holder MUST remind once and show the person the open notice.
6. **Deadline.** The holder completes steps 2–4 within P30D of the request.

**Opaque ids.** Because of R-I1, the Tombstone and the Events reveal nothing about the erased content.

- **V-6.** Every vault object's file name is the `content.sha256` of a Source that is not tombstoned. An object whose Source was erased is deleted from the package, even when its key was destroyed. The checker compares file names only and never reads content (§5.8).

### 15.6. Export, portability, backup and restore

**Export** (H-9).

- The subject's export is always the full package: every record, including proposed, declined and rejected ones; the Events; the projections; the lens pins; **the vault**; and the lock.
- It is delivered within P30D at no cost.
- Exports to another holder the person names use a grant with action `export` and the same package format. `export-run` is a disclosure Event: a later erasure sends that holder an erasure notice too (§15.5, step 4).

**Backups.**

- Backups SHOULD be encrypted.
- On restore, the holder MUST re-apply every Tombstone in the erasure ledger whose `erasedAt` is after the backup time, write `tombstones-reapplied`, and re-evaluate grant status.
- Step-ups never revive.
- Restore never changes dates (R-T4).

### 15.7. Multi-holder semantics

- Several holders can keep contexts about the same person, for example a personal agent and an app.
- Each holder's context is complete in itself.
- Cross-holder links are `same-occurrence` relations or cross-context references.
- A conflict between holders is a Tension `holder-divergence`.
- A consumer reading from several holders receives separate projections. It MUST NOT merge them silently; it applies a resolver (§12.2): `returnDialog` by default (show both values and ask the person), and `returnNone` whenever either side has `person-only`.

### 15.8. Selective-memory operations (informative)

| Operation | How OHC supports it |
|---|---|
| **Return to the source** | From any Interpretation ground, Claim evidence or Episode account, follow the span to the vault object. The subject has every tier; an agent has tiers by grant and step-up. |
| **Compare accounts** | An Episode's accounts are dated and typed (in the moment, first narrative, later reconstruction, external record, observer). A viewer shows them side by side. |
| **Then and now** | "As understood at K" (§7.3): what the person thought then, what they think now, and when it changed. |
| **Whose selection** | `summary.authoredBy`, `Episode.selection.selectedBy` and `Source.authorship` show who chose what was kept. |
| **What does not fit** | `counterEvidence`, `contradicts` relations and `externalConfirmation.status`. |
| **Hand back what helped** | Practices plus Outcomes; RecallCues under C-11. |

### 15.9. An agent acting as holder

A persistent, person-bound agent may hold that person's context. It then plays two roles that OHC keeps apart.

- **The subject's instrument.** Inside a session the subject started, the agent writes what the subject dictates and confirms, as the subject (`assertedBy: "subject"`, `recordedBy` the agent's Party). This is procedure [CONTEXT-01](../docs/agents/procedures/CONTEXT-01.md). It never writes its own readings this way.
- **A grantee.** For everything else, the agent is a Party like any other: it reads only projections under a grant, and writes its own readings, inferences and proposals under INF-1. Its model of the person stays reconcilable with the person's view through batch Reviews and renewed grants ([CONTEXT-09](../docs/agents/procedures/CONTEXT-09.md)).

- **H-17.** An agent acting as holder MUST keep the holder functions (grant evaluation, vault keys, step-up prompts and the Event log) behind a component that its own reasoning loop cannot bypass, with a confirmation channel the person controls. Where that is not possible, the agent MUST NOT be the vault holder at L2, and verbatim step-up (§15.4) is unavailable to it.
- **W-HO1.** Warning: the context's `holder` is a Party that is also the grantee of an allow grant in the same context. The checker cannot see whether H-17 holds and asks the reader to check it.

## 16. Consumer and holder obligations

### 16.1. Consumer obligations (Reader class)

- **C-1.** Act only under a grant whose computed status is `given`, within its purpose, actions, mode and storage. Re-check at use (R-G6). Never act in the world on the strength of a grant (R-G9). Storage covers everything a consumer keeps or derives from served content: notes, summaries, embeddings, memory files, and its runtime's transcripts, logs, caches and indexes. Served content never enters a store that cannot erase it.
- **C-2.** Do not act on `disputed` records except to ask the person. Do not re-propose a rejected or declined item without new grounds.
- **C-3.** Treat `hypothesis`, `pending` and `partly-confirmed` as needing confirmation before acting on them.
- **C-4.** Present interpretations as interpretations, with author, lens and limits, never as facts about the person. When showing an agent's reading, show its alternatives. Never present a record marked `no-quote-back`, or the profile it belongs to, to the person as an argument, authority or proof (§8.5).
- **C-5.** Do not treat `stale` (review-due, expired, unknown) as current. Follow `onExpiry`.
- **C-6.** Honour handling codes (§8.5, as listed in `obligations.handling`) and storage limits. Never use OHC content for any prohibited purpose (§8.10), or for leverage against the person.
- **C-7.** Never use agent estimates or cross-lens estimates as inference inputs. Never present a `frame-relative` record, or anything inferred from one, as an empirical fact. Never derive special-category content from other records without an `infer` grant that names that category or the lens of those records; no grant licenses deriving political views (`political-profiling`, §8.10). Never derive emotion values from biometric or behavioural signals (R-X4).
- **C-8.** Absence is never zero, false, default or consent. Never probe `not-disclosed`, and never infer from patterns of absence.
- **C-9.** Silence is not acceptance. An unanswered proposal is not accepted.
- **C-10.** Consent is never taken from a Part, from a steward outside scope, or from another agent's report that "the person agreed". A Part never authorises anything.
- **C-11.** Recall: offer only under an active RecallCue that the subject authorised, holding the `recall` action; respect the cue's timing, cooldown, `maxPerWeek` and computed pause; always include alternatives, at least one of them non-psychological. Recall is not crisis support. A consumer's crisis protocol always takes precedence; recall MUST NOT delay, replace or condition it (RC-5).
- **C-12.** On a revocation or erasure notice, purge by `purgeBy` and acknowledge. Never re-identify the subject across aliases, and never link projections obtained under different grants or from different holders, except through a resolver the person sees.

What a consumer may decide or propose for the person on the basis of results and readings is set by the grant's `decisionUse` (R-G14, `obligations.decisionUse`). A playbook a consumer follows is guidance, never permission (PB-4).

### 16.2. Holder obligations (Holder class)

- **H-1.** Default deny. Serve only what §12.3 yields at serve time.
- **H-2.** Write an Event for every disclosure (a disclosure Event, §13.1), write, Review, step-up, notice, import, export, backup and restore. Events carry ids and codes only, in a salted chain (§13.2).
- **H-3.** Serve proposed records only to the subject and to the proposer (its proposer view, §12.5, and `ohc.proposal-result`). Never serve declined, retracted or rejected records to any other grantee.
- **H-4.** Refuse writes and proposals that fail INF-1 or PR-2, **without storing them**. Answer `ohc.denial`.
- **H-5.** No existence oracles: no counts of withheld, special, rejected or contested items; no flags that reveal records outside the grant; `not-disclosed` whether or not data exists; denial codes that never depend on the data.
- **H-6.** No guessable digests to grantees (R-V1). No content digests in Events.
- **H-7.** Step-up per §15.4.
- **H-8.** Erasure per §15.5, including notices (MUST), crypto-shredding where used, the erasure ledger, and tombstone re-application on restore.
- **H-9.** Export per §15.6. The subject's own export always includes the vault.
- **H-10.** Quarantine under R-X3. Enforce R-X4 at write: refuse affect content grounded, directly or transitively, in biometric or behavioural sources, whatever its facet or label.
- **H-11.** Grants: refuse grants without `expiresAt`, or above the maximum duration (R-G10); compute status; on withdrawal or revocation, stop serving and send `ohc.revocation-notice`.
- **H-12.** Use pairwise aliases. Never send the subject id, the card or the links unless a selector names `identity-linking`.
- **H-13.** Third parties: apply V-2, enforce TP-1 at write, and keep party labels pseudonymous.
- **H-14.** Apply custody ceilings (§15.3). Grant no practitioner access through a LensAdoption.
- **H-15.** Keep the person informed. On request, show the pending proposals, the grants, the Event log and each projection, and let the person **view the context as any grantee** (the same algorithm, §12.3).
- **H-16.** Retention: apply `retention.until`; keep backups encrypted; keep the erasure ledger content-free.
- H-17 (an agent acting as holder) is defined in §15.9.

## 17. Practices and Outcomes

### 17.1. Practice

Layer `assertion` · module `practices` · normative-draft. A way of coping or acting that the person has, tried or wants to try. It records where the practice came from (the person themselves, a lens toolkit, a practitioner, an agent, another person, a tradition) and its limits. Practices make "lost access to one's own ways of coping" recoverable.

The envelope (§3.4), plus:

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `name` | string | yes | — | The person's own name for it. |
| `description` | string | no | — | |
| `practiceKind` | string | yes | below | |
| `source` | `{"route": string, "lens"?: URI, "templateId"?: string, "by"?: Actor}` | yes | below | `templateId` is a lens toolkit item id. |
| `steps` | [string] | no | — | |
| `duration` | Duration | no | — | |
| `limits` | string | no | — | When it should not be used. |
| `initialStatus` | string | no | `candidate` (default), `in-use`, `not-for-me` | |
| `nonClinical` | const `true` | yes | — | |

**Practice kinds** (open list with `x-`): `breathing`, `movement`, `reflection`, `writing`, `conversation`, `rest`, `planning`, `environment`, `social-contact`, `creative`, `contemplative`, `other`.

**Source routes** (closed): `self-discovered`, `from-lens`, `from-practitioner`, `from-agent`, `from-other-person`, `from-tradition`, `imported`.

The status (`candidate`, `in-use`, `paused`, `retired`, `not-for-me`) is computed from `initialStatus` and Reviews: `resume` gives `in-use`; `pause`, `retire` and `reject` give `paused`, `retired` and `not-for-me` respectively. "Times tried" is computed from Outcomes.

**Invariants.**

- **PC-1.** A Practice whose `source.route` is `from-agent` is proposed, and INF-1 applies.
- **PC-2.** A `templateId` whose toolkit item has `requiresPractitioner: true` or `agentMayOffer: false` MUST NOT come from an agent.
- **PC-3.** Evidence claims about efficacy are not stored on a Practice. The lens's evidence tiers apply ([LENSES.md](LENSES.md)), and agent-offered delivery is always `not-assessed`.
- **PC-4.** `nonClinical` is true. Clinical procedures are out of scope (HealthRef pointers only).

**Example.**

```json
{"id": "pr-01", "name": "Walk, then write the walk-away number",
 "description": "A 20-minute walk before a hard call; then one line: the price at which I would leave.",
 "practiceKind": "planning", "source": {"route": "self-discovered"},
 "steps": ["Walk 20 minutes without the phone", "Write the walk-away number", "Make the call"], "duration": "PT30M",
 "limits": "Not when the call is in less than an hour.", "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-18T19:10:00Z", "contexts": ["work"],
 "synthetic": true}
```

### 17.2. Outcome

Layer `outcome` · module `practices` · normative-draft. What happened when a practice was used, a recall cue fired, a proposal was offered, an interpretation was shown or a model view was used. It closes the loop: did the reminder help?

The envelope (§3.4), plus:

| Field | Type | Req | Vocabulary | Notes |
|---|---|---|---|---|
| `about` | `{"practice" \| "recallCue" \| "proposal" \| "interpretation" \| "modelView": LocalId}` | yes | — | Exactly one key. |
| `episode` | LocalId | no | — | Where it happened. |
| `delivery` | `{"at": DateTime, "by": Actor, "presented"?: [LocalId], "wording"?: string, "response": "accepted" \| "declined" \| "deferred" \| "asked-to-stop"}` | no | — | Agents record delivery as `observed` facts. |
| `result` | string | yes | `helped`, `partly`, `no-effect`, `worse`, `unclear`, `not-tried` | |

**Invariants.**

- **O-1.** An Outcome with `assertedBy` other than `"subject"` has epistemic status `hypothesis` and is labelled "agent's estimate". It is never the person's rating.
- **O-2.** A delivery `response` of `asked-to-stop` makes the target RecallCue or offering paused (computed; RC-3).
- **O-3.** `about` resolves to the matching kind.

**Example.**

```json
{"id": "oc-02", "about": {"recallCue": "rc-01"},
 "delivery": {"at": "2026-09-24T07:31:00Z", "by": "a-02", "presented": ["pr-01"],
              "wording": "Last time a walk and a written walk-away number helped. It may also just be a full week. Want the note?",
              "response": "accepted"},
 "result": "helped", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-24T19:00:00Z",
 "synthetic": true, "contexts": ["work"]}
```

## 18. Patterns (experimental)

**This section is experimental.** No conformance claim may rely on it.

Layer `interpretation` · module `patterns`. A Pattern is a recurrence across at least two episodes, such as a recurring situation, reaction, strategy or cycle, possibly across life domains. A Pattern can be revoked or corrected, and it never hardens into a disposition.

The envelope (§3.4), plus:

| Field | Type | Req | Notes |
|---|---|---|---|
| `text` | string | yes | |
| `patternKind` | string | yes | `recurring-situation`, `recurring-reaction`, `recurring-strategy`, `cross-domain`, `cycle`, `other` |
| `episodes` | [LocalId] | yes (≥2) | PT-1 |
| `grounds`, `counterEvidence`, `alternatives`, `limits` | as in Interpretation | cond | The I4 rule applies to non-subject authors. |
| `lens`, `adoption` | as in Interpretation | no | |
| `facets` | [string] | no | |

**Invariants.**

- **PT-1.** At least two distinct Episodes, not counting supersession chains.
- **PT-2.** The analogues of I1, I4 and I5 hold.
- **PT-3.** No Claim with facet `disposition` may cite a Pattern in `derivedFrom`.
- **PT-4.** The `patterns` module is declared.

**Example.**

```json
{"id": "pat-01", "text": "Supplier calls were moved when no walk-away number was written down.",
 "patternKind": "recurring-situation", "episodes": ["ep-04", "ep-02"],
 "counterEvidence": [{"ref": "ep-03", "kind": "evidence"}], "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-26T20:15:00Z", "contexts": ["work"], "sensitivity": "sensitive", "synthetic": true}
```

## 19. Recall cues (experimental)

**This section is experimental.** No conformance claim may rely on it.

Layer `recall` · module `recall`. A RecallCue is a cue **authorised by the person** that allows an agent to offer back the person's own experience (practices, episodes, interpretations) when a described situation recurs, with alternatives and limits. It supports the recall loop (recognition → retrieval → relevance → timing → permission → offer → feedback) at the data level. Recognition, timing decisions and the offer itself are agent behaviour, outside OHC. **Recall is not therapy and not crisis support.**

The envelope (§3.4), plus:

| Field | Type | Req | Notes |
|---|---|---|---|
| `trigger` | `{"description": string, "signals"?: [code], "contexts"?: [domain]}` | yes | Signals below. **No physiological or biometric signals** (R-X4). |
| `offer` | `{"targets": [LocalId], "framing": string, "suggestedWording"?: string, "includeAlternatives": true, "alternativesNote": string, "maxTier": "none" \| "index" \| "summary" \| "excerpt"}` | yes | `includeAlternatives` is const `true`. `alternativesNote` MUST name at least one non-psychological explanation (fatigue, load, health, circumstances) (RC-4). A cue never reaches `verbatim`. |
| `timing` | `{"askBeforeReminding": boolean, "notWhen"?: [string], "cooldown": Duration, "maxPerWeek": int}` | yes | Defaults: `true`, P1D, 2. |
| `safety` | `{"nonClinical": true, "note"?: string}` | yes | |

**Signals** (closed): `calendar-event`, `keyword-in-subject-message`, `subject-request`, `time-of-day`, `task-type`, `other`.

The status (`proposed`, `active`, `paused`, `retired`) is computed. **Auto-pause is computed (RC-3).**

**Invariants.**

- **RC-1.** Activation is by the subject only (R-A1). A cue proposed by an agent stays proposed until the subject admits it.
- **RC-2.** If any target's effective categories include `mental-health` or `trauma-adjacent`, or its tier is `special`, the cue MUST be **authored** by the subject (`assertedBy: "subject"`), not merely admitted.
- **RC-3.** The cue is computed `paused` after 3 consecutive Outcomes about it with result `no-effect` or `worse`, or with response `asked-to-stop`. Only a subject `resume` reactivates it.
- **RC-4.** `includeAlternatives` is true and `alternativesNote` is non-empty.
- **RC-5.** Recall is not crisis support. A consumer's crisis protocol always takes precedence; recall MUST NOT delay, replace or condition it.
- **RC-6.** Using a cue requires a grant with action `recall` and purpose `recall-support`.
- **RC-7.** A target Episode must have computed `recall` set to `ask-each-time` or `permitted`.

**Example.**

```json
{"id": "rc-01",
 "trigger": {"description": "A supplier or pricing call is in my calendar and I say I want to move it.",
             "signals": ["calendar-event", "keyword-in-subject-message"], "contexts": ["work"]},
 "offer": {"targets": ["pr-01", "ep-03"], "framing": "Last time a walk and a written walk-away number helped.",
           "includeAlternatives": true,
           "alternativesNote": "It may also be plain tiredness or a full week; moving the call can be right.",
           "maxTier": "summary"},
 "timing": {"askBeforeReminding": true, "notWhen": ["after 21:00", "on days off"], "cooldown": "P2D", "maxPerWeek": 2},
 "safety": {"nonClinical": true}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-19T20:20:00Z", "sensitivity": "sensitive", "synthetic": true}
```

## 20. Inner system: Parts (experimental)

**This section is experimental.** No conformance claim may rely on it.

Layer `interpretation` · module `inner-system`. A Part is an inner position or sub-personality as the person names it, usually within a parts lens. It is the person's own description, not an entity claim and not a diagnosis.

The envelope (§3.4), plus:

| Field | Type | Req | Notes |
|---|---|---|---|
| `name` | string | yes | The person's own words. |
| `description` | string | no | |
| `lens`, `adoption` | as in Interpretation | no | |
| `role` | string | no | A lens construct id, for example `ifs/manager`. |
| `intention`, `concern` | string | no | |
| `typicalTriggers` | [string] | no | |
| `firstNoticed` | PartialTime | no | |
| `authoredWith` | string | no | `alone`, `with-practitioner`, `with-agent` |

**Invariants.**

- **P-1.** A Part is never a Party, actor, grantor or grantee.
- **P-2.** `assertedBy` MUST be `"subject"`. Agents never author Parts.
- **P-3.** The default tier is `special` and the default handling is `["person-only"]`.
- **P-4.** A parts map is a **view** over Parts and part Relations, never a stored shape.
- **P-5.** The Relations `held-by` (Claim or Interpretation → Part), `protects`, `polarized-with` and `allied-with` require this module.

**Example.**

```json
{"id": "part-01", "name": "The keeper", "description": "Wants every number checked twice before anyone sees it.",
 "lens": {"id": "urn:ohc:lens:ifs", "version": "0.2.0"}, "adoption": "la-02", "role": "ifs/manager",
 "concern": "Being caught unprepared.", "authoredWith": "with-practitioner", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-06-10T19:00:00Z", "sensitivity": "special",
 "handling": ["person-only"], "synthetic": true}
```

## 21. Health pointers (experimental)

**This section is experimental.** No conformance claim may rely on it.

Layer `assertion` · module `health-ref`. A HealthRef is a pointer to a clinical record held elsewhere (FHIR). It carries **no clinical content**.

The envelope (§3.4), plus:

| Field | Type | Req | Notes |
|---|---|---|---|
| `system` | const `"fhir"` | yes | |
| `fhirVersion` | string | yes | `R4` or `R5` |
| `resourceType` | string | yes | `Condition`, `Observation`, `MedicationStatement`, `CarePlan`, `DocumentReference`, `Consent`, `other` |
| `reference` | URI | yes | An absolute FHIR URL or a `urn:uuid`. |
| `custodian` | LocalId | yes | A Party. |
| `purposeNote` | string | no | Why the person keeps the pointer. |

**Invariants.**

- **HR-1.** No fields other than the envelope and the fields above. No codes, values or narrative.
- **HR-2.** The tier is `special`, the categories include `health` or `mental-health`, and the audience is `named`.
- **HR-3.** It is served only to a grant naming its id, with purpose `health-coordination`.
- **HR-4.** No record cites a HealthRef as a ground.

**Example.**

```json
{"id": "hr-01", "system": "fhir", "fhirVersion": "R5", "resourceType": "CarePlan",
 "reference": "urn:uuid:5b3b2f7e-1c0a-4e57-9a5e-2f1f2a7c9d10", "custodian": "o-01",
 "purposeNote": "Physiotherapy plan, for scheduling only.", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-07-01T09:00:00Z", "sensitivity": "special", "categories": ["health"], "audience": "named",
 "synthetic": true}
```

## Annex A. Rules index (informative)

### A.1. Specification rules

Every rule identifier used by OHC 0.1, with the place that defines it.

| Identifiers | Subject | Defined in |
|---|---|---|
| G1–G4 | Layers and grounding direction | §3.2 |
| R-S1…R-S5 | Two serializations | §3.3 |
| INF-1, R-V2, X-1, RF-1 | Content-record envelope: inference under grant, supersession, synthetic examples, allowed references | §3.4 |
| R-M1 | Declared modules | §4.1 |
| LV-0, R-C1…R-C4 | Conformance levels; where a context starts; adult subjects only | §4.2 |
| R-V0 | Version selection | §5.2 |
| R-I1, W-ID1 | Opaque record ids | §5.3 |
| R-P2 | A Part is never an actor | §5.4 |
| R-O1…R-O3 | Origin | §6.1 |
| ST-1 | Steward endorsement and limits | §6.2 |
| R-N1, R-N2 | Confidence | §6.3 |
| R-A1 | Admission | §6.4 |
| R-B1 | Absence | §6.7 |
| R-T5b | Import time | §7.1 |
| R-T2…R-T6 | Freshness | §7.2 |
| C3 | Tier propagation | §8.4 |
| TP-1 | Third parties | §8.7 |
| R-X3, R-X4 | Affect quarantine; emotion-inference ban | §8.8 |
| CX-1…CX-8 | Context | §9.1 |
| SJ-1…SJ-3 | Subject | §9.2 |
| PA-1…PA-3 | Party | §9.3 |
| CL-1…CL-9, W-CL4, W-CL5 | Claim | §9.4.4 |
| RL-1…RL-5 | Relation | §9.5 |
| SR-1…SR-7, W-SR1 | Source | §10.1 |
| EP-1…EP-7 (EP-2 is also R-E1) | Episode | §10.2 |
| I1–I10 | Interpretation | §10.3.2 |
| T1–T4 | Tension | §10.4 |
| LA-1…LA-6, W-LA6 | LensAdoption | §10.5 |
| AR-1…AR-8 | AssessmentRecord | §10.6 |
| MV-1…MV-4 | ModelView | §10.7 |
| RV-1…RV-6 | Review | §11.1 |
| PR-1…PR-4 | Proposal | §11.2 |
| TB-1…TB-5 | Tombstone | §11.3 |
| GR-1…GR-9 | Grant | §12.1 |
| R-G1…R-G14, R-L0 | Grant rules; decisions on the basis of results and readings; a link is not access | §12.4 |
| EV-1…EV-7 | Event | §13.1 |
| PJ-1…PJ-8 | Projection | §14.1 |
| LK-1…LK-3 | ContextLock | §14.2 |
| V-0 | The subject's access to their own vault | §15.1 |
| R-V1, V-1…V-5 | Release tiers, handles, excerpts, third parties, custody | §15.3 |
| SU-1…SU-7 | Step-up | §15.4 |
| V-6 | No vault object outlives its Source | §15.5 |
| H-17, W-HO1 | An agent acting as holder | §15.9 |
| C-1…C-12 | Consumer obligations | §16.1 |
| H-1…H-16 | Holder obligations (H-17 is in §15.9) | §16.2 |
| PC-1…PC-4 | Practice | §17.1 |
| O-1…O-3 | Outcome | §17.2 |
| PT-1…PT-4 | Pattern (experimental) | §18 |
| RC-1…RC-7 | RecallCue (experimental) | §19 |
| P-1…P-5 | Part (experimental) | §20 |
| HR-1…HR-4 | HealthRef (experimental) | §21 |
| LN-1, LN-3…LN-9, LN-11, LN-13 | Lens descriptors | [LENSES.md](LENSES.md) |
| PB-1…PB-5, W-PB5 | Playbooks | [LENSES.md](LENSES.md) §2.2 |
| IMP-1…IMP-5, W-IMP2, W-IMP6, INS-1, IMA-1, IMA-2, IMH-1 | Instrument import: imported results, the import block, agents, the agreement screen | [INSTRUMENT-IMPORT.md](INSTRUMENT-IMPORT.md) |
| M-1…M-8 | Mapping policy | [LENSES.md](LENSES.md) |
| IB-1…IB-6 | Proposal inbox | [EXCHANGE.md](EXCHANGE.md) |
| J-…, S-…, ENV-…, ID-…, LV-1, LV-2, RA-1, TP-2, TP-3, X-2, X-3, REL-…, SELF-… | Checker identifiers | Annex A.2 |

I3 and most holder and consumer obligations are normative but cannot be verified from files alone. The reference checker lists the rules it cannot check, and reports a rule it checks under another identifier (for example R-A1 as RA-1) under that identifier.

### A.2. Checker identifiers

These identifiers name checks of the reference checker. Each implements the specification rule named in it; a finding under one of them points here.

**JSON and schemas** (§5.1, §5.9):

- **J-1.** A file is UTF-8 without a byte order mark (§5.1).
- **J-2.** No object has duplicate member names (§5.1).
- **J-3.** No number is `NaN` or `Infinity` (§5.1).
- **J-4.** A JSON Lines file has one JSON object per line and no blank lines inside (§14.3).
- **J-5.** Member names are ASCII, except inside `Subject.card` (§5.1).
- **J-6.** A path in `collections`, the lock or a `vaultPath` is relative, without a leading `/`, `\`, `..` or `:` (§14.3).
- **S-1.** A document's `format` and `specVersion` are known (R-V0).
- **S-2.** A manifest, plan or other document validates against its schema.
- **S-3.** A record validates against its kind's schema. The finding names the failing keyword and the schema property, for example `required: recordedAt`; `required` and `additionalProperties` failures are always reported, even next to a more specific rule.
- **S-4.** The vocabulary `$defs` in `common.schema.json` equal what the catalogs generate (§5.10).
- **S-5.** Every experimental kind present belongs to a declared module (R-M1).

**Envelope and ids** (§3.4, §5.3):

- **ENV-1.** A record carries only the envelope fields and its kind's own fields (reported as S-3).
- **ENV-2.** A record with `origin: declared` whose `assertedBy` is an agent Party carries `text`: an agent declares only in words it states itself (R-O2).
- **ENV-3.** An imported record's `importedFrom.importedAt` equals its `recordedAt`, and its `formulatedAt` is not later than `recordedAt` (R-T5b).
- **ENV-4.** `supersedes` names an existing record of the same kind, the chain is acyclic, and a locked record is superseded only by the subject (R-V2).
- **ENV-5.** A stored `sensitivity` lower than the kind's default is written only by the subject (§8.3).
- **ENV-6.** `synthetic` is true on example records (reported as X-1).
- **ID-1.** Record ids are unique across all collections (CX-4).
- **ID-2.** A tombstoned id is never reused (TB-3).
- **ID-3.** Every local reference resolves to a record, a Tombstone or a Party.
- **RA-1.** A Review that admits a record is written by an actor R-A1 allows for that record.
- **TP-2.** No interpretation-layer record points at a Party, except an Interpretation's `about` (checked as I8) (TP-1).
- **TP-3.** Warning: an observer account appears to describe a third party's inner states (TP-1, EP-5).

**Levels** (§4.2):

- **LV-1.** At L1, every record with `origin` `inferred` or `derived` cites at least one ground.
- **LV-2.** At L2, the context is a package with a lock and an Event log.

**Examples** (§1.5):

- **X-2.** An example names no person: no common personal name appears in its text.
- **X-3.** The checker's output for a published example equals its `expected-check.json`.

**Release** ([CONTRIBUTING](../CONTRIBUTING.md)):

- **REL-1.** Every exported file is in the release manifest with a matching sha256, and the manifest lists nothing else.
- **REL-2.** The private tree is absent from the export and listed in the plan's `exclude`.
- **REL-3.** The licensing rules in LICENSING.md equal those of the release plan and the manifest.
- **REL-4.** Every exported Markdown file ends with the licence footer matching its licence.
- **REL-5.** No exported text file contains a private path, host, e-mail address, credential pattern, internal design-section id, or a marker from the private denylist; the check fails closed when the denylist is not loaded.
- **REL-6.** The manifest's flags ledger is present and honest where it can be computed, and every published example is synthetic.
- **REL-7.** An exported tree holds no private tree, in its files or (when it is a Git repository) in its index.

**Self-checks:**

- **SELF-1.** No enum value equals the name of a different field of the same object.
- **SELF-2.** Every rule id cited in this specification is known to the checker.
- **SELF-3.** The JCS implementation passes the RFC 8785 test vectors.
- **SELF-4.** Every rule id the checker reports is defined in a specification document, so that each finding can say where to look.

## Annex B. Privacy and security considerations (informative)

**No existence oracles.** A projection never reveals whether withheld data exists. `completeness` is always `partial` and `omissions` always `hidden`; there are no count fields (PJ-3). An absence for a requested selector is `not-disclosed` whether or not matching records exist (R-G5). A Tension is served only if every member is disclosable, and is otherwise dropped without a flag (T3, PJ-5). Denial codes describe the grant or the request, never the data (H-5). Record ids carry no sequence a grantee could read gaps in: the reference window issues opaque ids, so a projection that leaves a record out shows no gap.

**No guessable digests.** Short quotes and short texts are guessable from their hashes. Below the excerpt tier a grantee receives per-grant HMAC handles instead of content hashes (R-V1). Records never store quote digests. Events never carry content digests (G3). Stored projections carry a random `nonce`, so their digest cannot be guessed; Events reference projections by id only.

**Pairwise aliases.** A grantee never receives the subject id. It receives an alias derived per grantee (§12.3, step 11). Consumers never re-identify the subject across aliases or link projections from different grants or holders (C-12).

**Third parties.** No record describes another person's inner states, traits, health or beliefs (TP-1). Sources containing third-party material default to the `index` tier, third-party spans are redacted for grantees (V-2), and verbatim access to a third party's own words needs their recorded consent or redaction (SU-7). Party labels stay pseudonymous (H-13).

**Affect.** Content about mood, emotion, stress or affect that the person did not declare is quarantined as special, person-only and not usable for inference (R-X3). Affect content derived, directly or transitively, from biometric or behavioural signals is refused whatever the method label, facet or predicate says (R-X4, CL-4, H-10).

**Quoting back.** A person's profile is not an argument against them. A record marked `no-quote-back` is background only: it is never presented to the person as authority or proof, and the person's own words in the present conversation take precedence (§8.5, C-4).

**Profiling.** Consent to use is not consent to profile. Every inferred record written by someone other than the person needs an `infer` grant with a named purpose and explicit consent (INF-1, R-G11). A proposal that fails this check is refused without storing anything (PR-2, H-4).

**Erasure that erases.** Record ids carry no words from sensitive content (R-I1). A Tombstone holds no content, hash, date of the content, party, facet, category, lens or title (TB-1). Reviews and Proposals about erased records are erased or reduced with them (§15.5). Vault objects are deleted or crypto-shredded, and none outlives its Source (V-6). The Event chain is salted, and a removed Event becomes a stub that keeps the chain verifiable (§13.2). Erasure notices to every recipient are mandatory (§15.5). Restoring a backup re-applies erasures from the ledger (§15.6). The subject's export always includes the vault (H-9).

**Naive consumers.** Statements and readings travel in separate members of a projection, so a consumer that reads only statements never meets an interpretation (§12.3). A grant decides whether readings are included at all (R-G8).

**Step-up.** Verbatim access is confirmed out of band by the person, for at most one hour, and per request for special material. Silence is decline, and an agent never confirms (SU-1…SU-4).

**Grants expire.** Every grant has an expiry (at most one year, and at most 180 days with `infer` or special material), and forwarding, cross-context use and delegation are off in 0.1. A result or reading grounds a choice for the person only under `decisionUse: approval-required`, and then only with the person's confirmation of each proposal (R-G10, GR-2, R-G14).

**Stewards and minors.** A steward acts only within an explicit scope, never on special or inner-system material, and is shown as such (ST-1). Contexts about children or about adults under guardianship are non-conforming in 0.1, and a context that claims a level attests that its subject is an adult (R-C4).

**Agents as holders.** A persistent agent that holds its person's context keeps the holder functions out of its own reasoning loop's reach, or does not hold the vault at L2 (H-17).

**Tooling.** Tools never echo field values in messages or logs, never follow external locators and never read vault content (§5.8).

**What a check does not establish.** A passing check does not verify that content is true, that consent was given or authenticated, that endorsements are authentic, or that any holder or agent behaves as specified. The reference checker reports these limits in its output.

## Annex C. Experience-first checks mapped to tests (informative)

OHC was designed against a set of experience-first checks. The table shows where each is visible in the synthetic Noa example ([examples/noa-episode-first/](../examples/noa-episode-first/)) and which automated test covers it.

| # | Check | Shown in the Noa example | Test |
|---|---|---|---|
| 1 | Separate observation and experience from interpretation | `ep-04` account strands; `in-01`…`in-05` are separate records | `test_retrospective_reading_not_in_episode` |
| 2 | Keep two contradicting interpretations without mixing them | `in-02` and `in-03`, with `r-03` `alternative-to` | `test_two_interpretations_coexist` |
| 3 | Show how the person's views changed | `in-01` → `in-03` (`heldDuring`); `c-11` → `c-12` | `test_temporal_self_model_query` |
| 4 | Find patterns across episodes | `pat-01` (`ep-04`, `ep-02`) | `test_pattern_needs_two_episodes` |
| 5 | An independent agent uses the data without inheriting explanations | `prj-0003` (`interpretations: none`) compared with `prj-0007` | `test_independent_agent_does_not_inherit_interpretations` |
| 6 | The person contests a conclusion and the evidence survives | `rv-01` on `c-09`; `src-02` intact | `test_contest_keeps_evidence` |
| 7 | A timely reminder with permission | `rc-01` + `g-02` (`recall`) + `oc-02` | `test_recall_requires_grant_action` |
| 8 | Did the reminder help? | `oc-02` (`result: helped`, authored by the subject) | `test_outcome_recorded_by_subject` |
| key | Can another agent use the experience without inheriting the first agent's readings? | Projection with `withoutInterpretations`; grant `interpretations: none`; separate projection members | `test_naive_consumer_separation` |

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
