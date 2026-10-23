# Lenses

Module `lenses` · format `0.1.0-draft`. The shapes and rules in this document are **normative-draft**. The catalog
entries under `spec/lenses/`, `spec/instruments/`, `spec/mappings/lens/` and `spec/playbooks/` are **experimental**:
each carries its own `descriptorStatus`, and every entry carries `legalReviewNeeded: true` until counsel has reviewed
it.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as described in BCP 14 (RFC 2119,
RFC 8174) when, and only when, they appear in all capitals. Sections 1–6 are normative-draft. Sections 7 and 8 are
informative.

Nothing in this document is legal advice. Trademark, copyright and licence entries record what the editors found and
where; they are not a clearance.

## 1. What a lens is

A **lens** is a framework of description that a person may use to understand themselves, and that an agent may use,
with permission, to work with them.

Four things are kept apart:

- the **lens**: the theory or frame;
- a **construct** inside it: a dimension, type, part, stage or column;
- an **instrument**: a specific test or procedure, with a form, a version and a publisher;
- a **result**: a dated record about the person (an AssessmentRecord, an Interpretation, a ModelView or a Part).

**OHC chooses no lens.** The useful question is which lens helps *this* person, in *this* state, for *this* task.
OHC records the person's relation to a lens (LensAdoption) and the outcomes of using it (Outcomes about ModelViews and
Practices). It never ranks lenses for a person.

Each lens descriptor carries three things:

- a **mental model** of working with the person (`mentalModel`);
- a **toolkit** (`toolkit`, `instruments`);
- **representation modes** (`representations`).

A person may **choose** a lens, an **agent may suggest** one, or it may be **inherited** from therapy, coaching or
practice (`adoption.routes`; LensAdoption `route`). A lens may come with **playbooks**: ways of using it, and the
person's accepted results in it, by situation (§2.2).

A lens carries facts and guidance, never a permission. What an agent may see, suggest, infer or decide is the
person's agreement with it: the Grant (`SPECIFICATION.md` §12), narrowed by the person's LensAdoption and handling
codes. Limits that protect the person from decisions of others hold for every grantee (`SPECIFICATION.md` §8.10).

Lens, Instrument, Mapping and Playbook documents are registry documents. They are shared and versioned, and they
contain no personal data: they MUST NOT reference any per-person record or contain any person's data (layer rule G2).

## 2. Lens descriptor (`format: ohc.lens`)

Schema: `spec/schema/lens.schema.json` (`urn:ohc:schema:lens:0.1.0-draft`). One file per lens:
`spec/lenses/<name>.lens.json`.

| Field | Type | Req | Notes |
|---|---|---|---|
| `format` | const `"ohc.lens"` | yes | |
| `specVersion` | const `"0.1.0-draft"` | yes | |
| `id` | URI `urn:ohc:lens:<name>` | yes | |
| `version` | semver | yes | The version of the descriptor, not of the framework. |
| `name` | `{"en", "ru"}` | yes | |
| `aliases` | [string] | no | Never a protected mark used as a generic name. |
| `descriptorStatus` | `stub` \| `draft` \| `reviewed` | yes | Every 0.1 entry is `draft` or `stub`. |
| `kind` | lens kind (§6) | yes | |
| `summary` | `{"en", "ru"}` | yes | One or two sentences, in OHC's own words. |
| `variants` | [`{"id", "note"}`] | no | For example 10 versus 19 Schwartz values. |
| `constructs` | [`{"id": "<lens>/<code>", "parent"?: id, "label": {"en", "ru"?}, "description"?: string, "sensitivity"?: tier, "categories"?: [code]}`] | cond | Exactly one of `constructs` and `constructsByReference`. Descriptions are always in OHC's own words. |
| `constructsByReference` | `{"url": URI, "reason": string, "idPattern": string}` | cond | Used when listing the construct names needs permission. |
| `mentalModel` | object | yes | `summary`, `assumptions` [string], `stance`, `unitOfAnalysis`, `attendsTo` [string], `howChangeHappens`, `languageGuidance`, `agentPosture` `{"do": [string], "dont": [string]}`, `exploratoryQuestions` [string], `helperMustNot` [string], `doesNotClaim` [string], `riskNotes` [string]. |
| `toolkit` | [ToolkitItem] | yes (may be `[]` for a stub) | `{"id": "<lens>.<item>", "name", "kind": "exercise" \| "worksheet" \| "dialogue" \| "observation" \| "instrument-use", "description", "facilitation": "self" \| "agent-offered" \| "practitioner", "requiresPractitioner": bool, "agentMayOffer": bool, "nonClinical": bool, "produces"?: "AssessmentRecord" \| "Interpretation" \| "ModelView" \| "Practice" \| "Part" \| "none", "cautions"?: [string]}` |
| `representations` | [`{"id", "kind": "score-profile" \| "type-label" \| "ranked-list" \| "circumplex" \| "parts-map" \| "stage" \| "thought-record" \| "narrative" \| "chart" \| "grid", "resultType"?: result type, "description"}`] | yes (at least one, except for a stub) | |
| `instruments` | [URI] | no | Instrument ids (§3). |
| `adoption` | `{"routes": [route], "suggestionRequires"?: [string], "inheritanceRoles"?: [string], "practitionerFor"?: [toolkit id]}` | yes | §6. Describes how the lens is usually adopted; never restricts a LensAdoption. |
| `evidence` | `{"measurementTier", "practiceTier": {"clinicianDelivered", "selfGuided", "agentOffered"}, "ontologicalStatus", "citations": [{"ref", "grade": "F" \| "F2" \| "U" \| "verify", "note"?}], "reviewedAt": date, "notes"?: string}` | yes | `agentOffered` is const `not-assessed` in 0.1. |
| `supports` | [string] | yes | What the lens can legitimately support, for example "self-reflection on tendencies". |
| `doesNotEstablish` | [string] | yes | What it does not establish. |
| `ip` | `{"conceptStatus": "free-concept" \| "proprietary-concept" \| "unclear", "marks": [{"mark", "owner", "status": "registered" \| "abandoned" \| "unverified" \| "none", "notice"?, "use": "nominative-only" \| "adjective-only" \| "avoid"}], "itemsLicence": string, "scoring": "public" \| "proprietary" \| "none", "restrictions": [string], "registryListing": "ok" \| "reference-by-url" \| "needs-permission", "lineageConsent"?: {"status": "obtained" \| "not-required", "ref"?}, "legalReviewNeeded": bool}` | yes | Every 0.1 entry has `legalReviewNeeded: true`. |
| `useLimits` | `{"crossLensMapping": "population-level-only" \| "not-allowed"}` | yes | Whether population-level Mappings involving this lens MAY be used (§4, AR-7, LN-3). |
| `defaults` | `{"sensitivity": tier, "categories": [code], "perConstruct"?: {id: {"sensitivity", "categories"}}, "reviewAfter": Duration \| "on-change"}` | yes | Descriptors may raise the default tiers of the records that cite them, never lower them. |
| `mappings` | [URI] | no | Mapping ids (§4). |
| `playbooks` | [URI] | no | Playbook ids (§2.2, PB-2). A registry descriptor lists registry playbooks only. |
| `descriptorAuthors` | [string] | yes | `["OHC editors"]` |
| `sources` | [string] | no | Public citations only. Never internal file paths. |

**Never-fields.** No descriptor, instrument entry or record contains item text, report prose, scoring keys or raw
proprietary responses. The schemas have no properties for them (LN-5; AR-3).

**Schema exception.** Like every OHC schema, the lens schema sets `additionalProperties: false`. The one exception is
`mentalModel`, which MAY carry further members whose values are arrays of strings, so that a descriptor can add
guidance lists without a schema change. Readers MUST ignore members they do not know there.

**What a descriptor decides, and what it does not.** `evidence`, `supports`, `doesNotEstablish` and the publisher's
own statements in `ip.restrictions` are facts: a holder shows them to the person in plain words, and they never act
as a ban. `defaults` raise the tiers of the records that cite the lens (C3, R-G3). `useLimits.crossLensMapping` says
whether population-level Mappings involving this lens MAY be used (§4). `mentalModel`, `toolkit` and
`representations` are guidance; I3 applies `helperMustNot`. `toolkit[].agentMayOffer` is guidance about a tool;
whether an agent offers it is the person's agreement. Seeing, suggesting, inferring and deciding live in the
person's Grant (`SPECIFICATION.md` §12, R-G14), never in the descriptor.

### 2.1 Checker invariants (LN)

- **LN-1.** `requiresPractitioner: true` ⇒ `agentMayOffer: false`.
- **LN-3.** If `measurementTier` is `T5` or `ontologicalStatus` is `symbolic-frame`, `useLimits.crossLensMapping` is
  `not-allowed`.
- **LN-4.** `defaults.sensitivity` is `special` for every lens kind except `representation`.
- **LN-5.** There are no never-fields. The schema has no such properties, and a text heuristic flags long quoted item
  lists.
- **LN-6.** `practiceTier.agentOffered` is `not-assessed`.
- **LN-7.** Exactly one of `constructs` and `constructsByReference` is present.
- **LN-8.** A mark with status `registered` has a `use` other than `avoid` only when a `notice` is given. Construct
  labels never use a registered mark as a generic noun.
- **LN-9.** Every id in `mappings` resolves to a Mapping in the catalog.
- **LN-11.** `ontologicalStatus: contemplative-tradition` requires `ip.lineageConsent.status: obtained`. A living
  tradition is never named without its holders' consent.
- **LN-13.** Every citation with grade `F2`, `U` or `verify` is surfaced in the documentation with its marker
  (§7.3).

### 2.2 Playbooks (`format: ohc.playbook`)

Schema: `spec/schema/playbook.schema.json` (`urn:ohc:schema:playbook:0.1.0-draft`). One file per playbook:
`spec/playbooks/<name>.playbook.json`.

A **playbook** says how to use one or more lenses, and the person's accepted results in them, in named situations:
when it applies, a few steps, the lens's tools to offer, the results it draws on, and what not to do there. It is
guidance for the helper, never a rule about the person and never a permission (PB-4). The catalog ships one basic
playbook per lens, written by the OHC editors from the lens's own `mentalModel` and `toolkit`. A coach's or
therapist's way of using a lens comes in as a local playbook from practice.

| Field | Type | Req | Notes |
|---|---|---|---|
| `format` | const `"ohc.playbook"` | yes | |
| `specVersion` | const `"0.1.0-draft"` | yes | |
| `id` | URI | yes | `urn:ohc:playbook:<name>`; a local playbook: `urn:ohc:playbook:x-<namespace>:<name>`. |
| `version` | semver | yes | |
| `name` | `{"en", "ru"}` | yes | A local playbook may give `en` only. |
| `lenses` | [URI] | yes (≥1) | The lenses it is for. |
| `author` | string | yes | One string, as an entry of `descriptorAuthors`: `OHC editors`; or the name of a public source, which `sources` then cites; or, for a local playbook, the person's or practitioner's own label. |
| `sources` | [string] | yes (may be `[]`) | Public citations only; at least one when `author` is a public source. Never internal file paths. |
| `licence` | `Apache-2.0` \| `CC-BY-4.0` | cond | REQUIRED in the registry. |
| `situations` | [Situation] | yes (1–8) | Below. |

A **Situation** is `{"id", "when", "use", "toolkit", "results"?, "watchFor"?}`: `id` is a slug unique in the
playbook; `when` (`{"en", "ru"}`) is the situation in plain words; `use` (`{"en": [step], "ru": [step]}`, 2–5 steps,
the same count in each language) says how to use the lens and the person's accepted results here; `toolkit` lists
toolkit item ids of its lenses (it may be empty); `results` lists construct ids of its lenses that the steps draw on;
`watchFor` (`{"en", "ru"}`) says what not to do here. No member describes a person, carries a value, band or
cut-off, or quotes an instrument.

**Where a playbook lives.**

- **Registry:** `spec/playbooks/<name>.playbook.json`. A lens descriptor lists its playbooks in `playbooks` (PB-2).
  There is no playbook catalog file: the descriptors' lists are the index.
- **Local, from practice:** in a package as `lenses/<name>@<version>.playbook.json`, pinned in `Context.playbooks`
  (`[{"id", "version", "sha256"?, "playbook"?}]`, the shape of `Context.lenses`; in a single document the playbook
  travels inline as the pin's `playbook`). It travels only inside the person's context and is never published
  without its author's permission, like a local descriptor (§5.1).
- A registry playbook a context uses is pinned the same way, so that what an agent receives at session start is a
  function of pinned documents (PB-5).

**The person's choice.** A LensAdoption's `playbooks` lists the playbooks the person uses with that lens. Absent: the
descriptor's `playbooks`. `[]`: none. Otherwise the person's choice among the descriptor's list, other registry
playbooks for the lens, and local playbooks pinned in the context (PB-3). Bringing a result writes no adoption.

**Situations.** There is no closed list of situations. The catalog's basic playbooks share seven slugs, so that a
rendering can group across lenses (informative): `plan-week`, `hard-conversation`, `choose-between-options`,
`after-setback`, `under-strain`, `give-feedback`, `look-back-at-an-episode`.

**Rules.**

- **PB-1.** Playbook. The document has the shape above; a registry playbook gives `ru` wherever it gives `en` and
  has a `licence`. Every lens in `lenses` resolves: a registry playbook to registry lenses; a local one also to
  lenses pinned in the same context. Every `toolkit` id is a toolkit item of one of its lenses with
  `agentMayOffer: true`, and every `results` id is a construct of one of its lenses. Situation ids are unique; `use`
  has 2–5 steps in each language given, the same count in both. An `author` other than `OHC editors` on a registry
  playbook comes with at least one `sources` entry.
- **PB-2.** A lens lists its playbooks. Every id in a descriptor's `playbooks` resolves to a playbook whose `lenses`
  include the descriptor's id; a registry descriptor lists only registry playbooks.
- **PB-3.** The person's playbooks. Every id in a LensAdoption's `playbooks` resolves, in the registry or among
  `Context.playbooks`, to a playbook whose `lenses` include the adoption's `lens`.
- **PB-4.** Guidance, not permission. A playbook grants nothing and states nothing about any person. An agent follows
  a step only within its grant and the person's adoption: a step that offers a guess needs `infer`; a step that
  weighs a result in what it proposes needs `decisionUse: approval-required` (R-G14); otherwise the agent skips the
  step. A step never outweighs what the person says now. A playbook holds no item text, report prose, scoring keys,
  score bands or claims of effect. A playbook of a lens whose `ontologicalStatus` is `symbolic-frame` or whose
  `measurementTier` is `T5` speaks in the frame and never presents frame content as a fact or a prediction (C-7).
- **PB-5.** Playbooks at session start. A holder's rendering for a persistent agent carries, for each lens named by a
  served record (AssessmentRecord, Interpretation, LensAdoption), the playbooks the person uses with it that resolve
  to pinned documents, grouped by situation, with the grant's terms printed above them (guesses as proposals: yes or
  no; weighing accepted results: yes or no). A lens with no served record brings no playbook.
- **W-PB5.** Warning: a pin in `Context.playbooks` resolves to no playbook; the rendering leaves it out.

## 3. Instrument registry record (`format: ohc.instrument`)

Schema: `spec/schema/instrument.schema.json`. One file per instrument: `spec/instruments/<name>.instrument.json`.

| Field | Type | Req | Notes |
|---|---|---|---|
| `format`, `specVersion`, `id` (`urn:ohc:instrument:<name>`), `version` | — | yes | |
| `name` | string | yes | Marks are used nominatively. |
| `lens` | URI | yes | The instrument appears in that lens's `instruments` list (AR-8). |
| `publisher` | string | yes | |
| `forms` | [`{"id", "items"?: int, "scale"?: string, "note"?}`] | yes | |
| `itemsLicence` | string | yes | |
| `scoring` | `public` \| `proprietary` \| `none` | yes | |
| `qualification` | string | no | For example "level S". |
| `marks` | as in Lens `ip.marks` | no | |
| `neverStore` | [string] | yes | For example `["item text", "report prose", "scoring key"]`. |
| `registryListing` | `ok` \| `reference-by-url` \| `needs-permission` | yes | |
| `citations` | as in Lens | yes | |
| `legalReviewNeeded` | bool | yes | |
| `reviewedAt` | date | yes | |
| `import` | `{"scoredBy", "scores", "scales", "normGroups"?}` | no | How a person brings a result of this instrument: who scores it, the score kinds and ranges a report shows, the scales, the norm groups. The module `instrument-import` ([INSTRUMENT-IMPORT.md](INSTRUMENT-IMPORT.md), INS-1). |

**Example.**

```json
{"format": "ohc.instrument", "specVersion": "0.1.0-draft", "id": "urn:ohc:instrument:ipip-neo-120", "version": "0.1.0", "name": "IPIP-NEO-120",
 "lens": "urn:ohc:lens:big-five", "publisher": "International Personality Item Pool (public domain)",
 "forms": [{"id": "120", "items": 120, "scale": "5-point Likert; 4 items per facet; 30 facets"}],
 "itemsLicence": "IPIP items are public domain, usable for any purpose, commercial or non-commercial", "scoring": "public",
 "neverStore": ["raw item responses outside the person's own test data"], "registryListing": "ok",
 "citations": [{"ref": "doi:10.1016/j.jrp.2014.05.003", "grade": "F", "note": "Johnson 2014; facet alpha .63-.88; N = 619,150"}],
 "legalReviewNeeded": true, "reviewedAt": "2026-10-09"}
```

## 4. Mapping registry record (`format: ohc.mapping`)

**One shape for every bridge:** between lenses, between OHC and ODE, and between OHC and other standards. Schema:
`spec/schema/mapping.schema.json`. Id form: `urn:ohc:mapping:<from>--<to>--<source>`.

| Field | Type | Req | Notes |
|---|---|---|---|
| `format`, `specVersion`, `id`, `version` | — | yes | |
| `bridgeKind` | code | yes | `lens-lens` (between lenses), `ohc-ode` (the ODE bridge), `ohc-standard` (crosswalks to other standards). The catalog reserves one further code for bridges that are never released. |
| `from`, `to` | `{"lens"?: URI, "construct"?: string, "instrument"?: string, "standard"?: string, "concept"?: string, "pin"?: {"tag"?, "commit"?, "sha256"?}}` | yes | |
| `relation` | code | yes | §4.1 |
| `statistic` | `{"r"?: number, "n"?: int, "sample"?: string}` | cond | REQUIRED for `correlates`. |
| `source` | string | cond | A citation. REQUIRED for `correlates`. |
| `scope` | string | yes | For lens bridges, always "population-level only; never for converting one person's result". |
| `notIdentity` | const `true` | yes | |
| `chainable` | const `false` | yes | |
| `rowStatus` | code | yes | `accepted`, `accepted-with-loss`, `not-identity`, `not-permitted`, `unresolved`. |
| `lost` | string | cond | REQUIRED for `accepted-with-loss`. |
| `forbiddenUse` | string | no | |
| `reopenWhen` | string | no | |
| `evidenceGrade` | `F` \| `F2` \| `U` \| `verify` | yes | §7.3 |
| `reviewedAt` | date | yes | |

**Relations** (`spec/catalogs/mapping.json`):

| Code | Definition |
|---|---|
| `correlates` | A population-level statistic. |
| `corresponds` | The same role in both, with differences. |
| `specializes` | The target is a narrower form. |
| `carries-part` | The target carries part of the concept. |
| `projects` | The target is a projection of the source. |
| `stores` | The target stores the source. |
| `fills-seam` | The target fills a gap in the source. |
| `no-relation` | The two must never be linked (frames versus empirical constructs). |
| `not-covered` | No counterpart. |

### 4.1 Mapping policy (M)

- **M-1.** A mapping is a Mapping record, never an alias. Construct ids of different lenses MUST NOT be declared
  equal.
- **M-2.** Every lens-to-lens mapping carries its statistic, its source and its scope. It is population-level only.
- **M-3.** No chaining: A→B and B→C never give A→C.
- **M-4.** No branded output from generic input. Generic data never yields a branded type label.
- **M-5.** Ipsative results (rankings, centred values) stay within the person and are never compared across people.
- **M-6.** Frames have `no-relation` to empirical constructs. They MAY be **placed side by side** for the person's
  own reflection, labelled as such.
- **M-7.** The person MAY forbid mappings on their records with the handling code `no-infer`.
- **M-8.** Disagreement between instruments, or between self-report and observer report, is data. Both records are
  kept and linked by a Tension of kind `source-divergence`.

### 4.2 Cross-lens estimates

A result produced through a mapping is an AssessmentRecord with `mode: cross-lens-estimate`, constrained by AR-2 and
AR-7: it is person-only, carries a validity ceiling, is never a decision input and never carries a branded label.

## 5. Per-person lens records

Three stored record kinds connect a person's context to the registry. They carry the content-record envelope and are
specified, with their invariants, in `SPECIFICATION.md`:

| Kind | Layer | What it records | Specified in |
|---|---|---|---|
| LensAdoption (`la-`) | `assertion` | The person's relation to one lens: the route (`self-chosen`, `agent-suggested`, `inherited-from-practice`, `imported`), the uses allowed, who may interpret through it, confidentiality, and what happens when a practice relationship ends. | `SPECIFICATION.md` §10.5 (LA-1…LA-6, W-LA6) |
| AssessmentRecord (`as-`) | `assertion` | A dated result in one lens: lens, variant, instrument, mode, rater, results, norm group, validity flags. An imported result is governed by `INSTRUMENT-IMPORT.md`. | `SPECIFICATION.md` §10.6 (AR-1…AR-8) |
| ModelView (`mv-`) | `interpretation` | One lens's (or model's) view over episodes and evidence: the question it asks, its hypotheses, grounds, limits and alternatives. | `SPECIFICATION.md` §10.7 (MV-1…MV-4) |

How the registry constrains these records:

- A lens with no resolvable descriptor, neither pinned (in `lenses/` or inline) nor in the catalog, is treated as a
  stub: its results are `frame-relative` (LA-6). The checker warns (W-LA6).
- Whether an agent suggests a lens, reads through it or offers its tools is the person's agreement (an `infer`
  grant that names the lens, I5; `suggest` to file a proposal), narrowed by their adoption (`agentInterpretation`)
  and handling codes. An `agent-suggested` adoption is proposed and activated by the subject only (LA-1).
- An AssessmentRecord's instrument MUST appear in the lens's `instruments` list, and its result constructs come from
  the lens's `constructs` (or follow its `constructsByReference.idPattern`).
- A `trademarkNotice` is REQUIRED on a genuine result when the lens's `ip.marks` require a notice, and is forbidden on
  agent estimates and cross-lens estimates.
- Results in a lens whose `measurementTier` is `T5`, or whose `ontologicalStatus` is `symbolic-frame`, are
  `frame-relative`, and so is anything inferred from them (AR-4); they are never presented as empirical facts (C-7).
- `reviewAfter` defaults to the lens's `defaults.reviewAfter`; tiers and categories start from the lens's `defaults`.

### 5.1 Local lenses

A person's framework may not be in the catalog: one inherited from their therapy or coaching, a practitioner's own
model, or a framework of their own. It is described with a **local descriptor**, written in the person's or the
practitioner's words.

- **Id.** A local lens id carries an `x-` namespace: `urn:ohc:lens:x-<namespace>:<name>`, for example
  `urn:ohc:lens:x-coach-a:three-rooms`. The namespace is the person's or the practitioner's; it claims no registry.
- **Where it lives.** In a package, as `lenses/<name>@<version>.lens.json`, pinned in `Context.lenses` with its
  `sha256`. In a single document, inline as the pin's `descriptor`.
- **Light profile.** A local descriptor is always `descriptorStatus: stub`. It needs only `format`, `specVersion`,
  `id`, `version`, `name`, `kind` (usually `author-framework`), `summary` and a `mentalModel` with `summary`,
  `attendsTo`, `agentPosture` and `helperMustNot`. A toolkit and representations are optional.
- **Stub.** Its results are `frame-relative` (LA-6). Whether an agent suggests it, reads through it or offers what
  it describes is the person's agreement, as for any lens. The person can speak in the lens, keep results in it and
  share them by grant.
- **Privacy.** A local descriptor travels only inside the person's context. It is never published to the registry
  without the author's permission.
- **Local playbooks.** A practitioner's way of using a lens, catalog or local, is a local playbook
  (`urn:ohc:playbook:x-<namespace>:<name>`, §2.2), kept the same way: in `lenses/` in a package, inline in a single
  document, pinned in `Context.playbooks`, never published without its author's permission.

A minimal local descriptor:

```json
{"format": "ohc.lens", "specVersion": "0.1.0-draft", "id": "urn:ohc:lens:x-coach-a:three-rooms", "version": "0.1.0",
 "name": {"en": "Three rooms (my coach's model)", "ru": "Три комнаты (модель моего коуча)"},
 "descriptorStatus": "stub", "kind": "author-framework",
 "summary": {"en": "Work, rest and repair as three rooms; trouble starts when one room takes over the others.",
             "ru": "Работа, отдых и восстановление как три комнаты; трудности начинаются, когда одна занимает остальные."},
 "mentalModel": {"summary": "Balance between three rooms matters more than any single habit.",
                 "attendsTo": ["which room a week was spent in", "what pushed the others out"],
                 "agentPosture": {"do": ["ask which room the person is in"], "dont": ["diagnose an imbalance"]},
                 "helperMustNot": ["present the model as a theory of the person"]}}
```

## 6. Lens vocabularies

The catalogs `spec/catalogs/lens-kinds.json`, `evidence-tiers.json`, `ontological-status.json`, `adoption.json` and
`assessment.json` are authoritative. This section restates them for reading.

**Lens kinds.** `trait-dimensional`, `type-categorical`, `strengths-ranked`, `values-circular`,
`stage-developmental`, `style`, `parts-model`, `practice-method`, `process-experiential`, `contemplative`,
`explanatory-model`, `author-framework`, `representation`, `self-description-frame`.

**Measurement tier** (applies to the constructs).

| Tier | Definition |
|---|---|
| `T1` | Established psychometric construct: replicated structure, norms, outcome validity. |
| `T2` | Validated with caveats: good psychometrics, but narrower or newer evidence, or cultural variance. |
| `T3` | Publisher-validated or practitioner tool: reliability shown mainly by the vendor; limited independent validity. |
| `T4` | Contested: core structural claims not supported, or validity "not demonstrated". |
| `T5` | Non-empirical self-description frame: makes no claim to empirical validity. |
| `not-applicable` | The lens makes no measurement claim (practice methods, contemplative perspectives, representations). |
| `not-assessed` | Not reviewed yet. |

**Practice tier** (applies to the lens's practices, per delivery context: `clinicianDelivered`, `selfGuided`,
`agentOffered`).

| Tier | Definition |
|---|---|
| `P1` | Replicated randomised controlled trials in this delivery context, on relevant outcomes. |
| `P2` | At least one randomised controlled trial in a stated population, not replicated. |
| `P3` | Uncontrolled studies, case series or practitioner reports. |
| `P4` | No systematic evidence. |
| `not-assessed` | Not reviewed. `agentOffered` is always `not-assessed` in 0.1. |

**Ontological status.**

| Code | Definition |
|---|---|
| `measured-construct` | Constructs defined by measurement. |
| `theoretical-model` | A model of mind or behaviour used to understand, not to measure. |
| `practice-frame` | A frame of practices. |
| `symbolic-frame` | Meaning-making without an empirical claim. |
| `contemplative-tradition` | A living tradition of practice. Naming one requires its holders' consent (LN-11). |
| `representation` | A way of arranging information, not a theory. |

**Adoption routes.** `self-chosen` (the person picked the lens); `agent-suggested` (an agent proposed it and the
person accepted; it is proposed until the subject admits it); `inherited-from-practice` (brought from the person's
therapy, coaching, teaching or practice, with a `practice` block); `imported` (created by an importer from an
instrument report; proposed until admitted).

**Assessment modes.** `self-report-instrument`, `observer-report`, `interview-scored`, `practitioner-facilitated`,
`self-identified`, `vendor-report-import`, `agent-inference` (constrained by AR-2), `cross-lens-estimate`
(constrained by AR-2 and AR-7), `computed-from-birth-data`.

**Result types.** `dimension-score`, `type-assignment`, `ranking`, `values-profile`, `circumplex`, `stage`,
`thought-record`, `frame-attributes`, `narrative`.

**Validity flags.** `incomplete`, `random-responding`, `acquiescence`, `translated-form`, `norm-mismatch`,
`agent-estimate-not-validated`, `cross-lens-population-estimate`, `self-identified-only`,
`vendor-algorithm-undisclosed`, `test-data-personal-only`.

**Adoption fields.** `confidentiality`: `none`, `practitioner-scope`, `therapy-confidential`. `uses`:
`speak-in-lens`, `offer-practices`, `store-results`, `interpret`, `recall`. `agentInterpretation`: `off`,
`ask-first`, `allowed`. `onEnd`: `ask`, `keep-read-only`, `archive-person-only`, `erase`.

## 7. The 0.1 catalog (informative)

The catalog has **16 entries**: 12 descriptors and 4 stubs. Every descriptor has a mental model, at least one
toolkit item (18 in all; `enneagram` has three, and `ifs`, `jungian-type`, `schwartz-values` and `via-strengths` two
each) and at least one representation; §7.6 shows each of them. The four stubs sketch a mental model of perspectives
that people use, without a toolkit or representations yet. All 16 entries are experimental catalog data with
`legalReviewNeeded: true`. There are 11 instrument entries (`bfi-2` carries an `import` block), 8 lens-to-lens
Mapping records and 16 basic playbooks, one per entry (§2.2).

**Not in the catalog.**

- `neris-16p` is excluded from 0.1: it would be a separate vendor lens (NERIS Type Explorer®, © NERIS Analytics, built on the Big Five), and it must not be called MBTI.
- No author framework is in the 0.1 catalog.
- No named living contemplative tradition appears without the consent of its lineage holders (LN-11). The
  `contemplative-observation` stub names no tradition.

**Choices worth knowing.**

- `needs-grid` is a `representation`: a view over the person's Claims with no results of its own. Its
  `defaults.sensitivity` is `personal` (the LN-4 exception); the records it shows keep their own tiers.
- A descriptor carries facts and guidance, never a permission (§1, §2). Whether an agent suggests a lens, reads
  through it or weighs its results is the person's agreement (`SPECIFICATION.md` §12, R-G14), for every entry,
  `astrology` and `human-design` included. What stays with these two symbolic frames is their facts (T5,
  `symbolic-frame`, `crossLensMapping: not-allowed`): their results, and anything inferred from them, are
  frame-relative (AR-4) and never presented as empirical fact or prediction (C-7, PB-4).
- Each entry lists one basic playbook, `<lens>-basic`, written by the OHC editors from the lens's own mental model
  and toolkit, with three or four of the seven shared situations (§2.2). A playbook names only toolkit items an agent
  may offer: `attachment-2d-basic`, `ifs-basic` and the four stubs' playbooks name none, and the stubs' steps only
  offer the perspective's question when the person asks for ways of looking.
- Each entry has a recipe, `docs/lenses/<lens>.md` (and `.ru.md`): how to bring a person's material in that lens into records, step by step, with a checked worked example, and which playbook the lens lists. A person brings a test result whose instrument entry has an `import` block through their own window instead (`docs/guides/BRING-A-RESULT.md`; module `instrument-import`).
- `crossLensMapping: population-level-only` is set only for the lenses that have Mapping rows (`big-five`, `hexaco`,
  `jungian-type`, `enneagram`). Ipsative lenses (`via-strengths`, `schwartz-values`) are `not-allowed` (M-5).
- `via-strengths` lists no construct names (`constructsByReference`). `<n>` in its id pattern is a strength's
  published name in lowercase, with words joined by hyphens; the Spirituality strength is treated as category
  `belief` through `defaults.perConstruct`.

### 7.1 Catalog index

<!-- lens-catalog:start -->
| Lens | Name | Kind | Status | Measurement | Practice (clinician · self-guided · agent) | Ontological status | Routes | Instruments | Playbook |
|---|---|---|---|---|---|---|---|---|---|
| `big-five` | Big Five (Five-Factor Model) | `trait-dimensional` | draft | T1 | not-assessed · not-assessed · not-assessed | measured-construct | self-chosen, agent-suggested, inherited-from-practice, imported | `ipip-neo-120`, `bfi-2`, `neo-pi-3` | `big-five-basic` |
| `hexaco` | HEXACO model of personality structure | `trait-dimensional` | draft | T1 | not-assessed · not-assessed · not-assessed | measured-construct | self-chosen, agent-suggested, inherited-from-practice, imported | `hexaco-pi-r` | `hexaco-basic` |
| `jungian-type` | Psychological type (four preference pairs, after Jung) | `type-categorical` | draft | T4 | not-assessed · not-assessed · not-assessed | theoretical-model | self-chosen, agent-suggested, inherited-from-practice, imported | `mbti-form-m`, `mbti-form-q` | `jungian-type-basic` |
| `enneagram` | Enneagram (nine motivational patterns) | `type-categorical` | draft | T4 | not-assessed · not-assessed · not-assessed | theoretical-model | self-chosen, agent-suggested, inherited-from-practice, imported | `rheti-2.5` | `enneagram-basic` |
| `via-strengths` | VIA character strengths (by reference) | `strengths-ranked` | draft | T2 | not-assessed · not-assessed · not-assessed | measured-construct | self-chosen, agent-suggested, inherited-from-practice, imported | `via-is-r`, `gacs` | `via-strengths-basic` |
| `schwartz-values` | Schwartz theory of basic human values | `values-circular` | draft | T2 | not-assessed · not-assessed · not-assessed | measured-construct | self-chosen, agent-suggested, inherited-from-practice, imported | `pvq-rr` | `schwartz-values-basic` |
| `attachment-2d` | Adult attachment (two dimensions) | `trait-dimensional` | draft | T2 | not-assessed · not-assessed · not-assessed | measured-construct | self-chosen, agent-suggested, inherited-from-practice, imported | `ecr-r` | `attachment-2d-basic` |
| `ifs` | Internal Family Systems (as a parts lens) | `parts-model` | draft | not-applicable | P2 · not-assessed · not-assessed | theoretical-model | self-chosen, agent-suggested, inherited-from-practice | — | `ifs-basic` |
| `cbt` | Cognitive-behavioural lens (non-clinical use) | `practice-method` | draft | not-applicable | not-assessed · not-assessed · not-assessed | practice-frame | self-chosen, agent-suggested, inherited-from-practice | — | `cbt-basic` |
| `needs-grid` | Needs grid | `representation` | draft | not-applicable | not-assessed · not-assessed · not-assessed | representation | self-chosen, agent-suggested | — | `needs-grid-basic` |
| `astrology` | Astrology (as a self-description frame) | `self-description-frame` | draft | T5 | not-assessed · not-assessed · not-assessed | symbolic-frame | self-chosen, imported | — | `astrology-basic` |
| `human-design` | Human Design (as a self-description frame) | `self-description-frame` | draft | T5 | not-assessed · not-assessed · not-assessed | symbolic-frame | self-chosen, imported | — | `human-design-basic` |
| `gestalt` | Gestalt perspective (stub) | `process-experiential` | stub | not-assessed | not-assessed · not-assessed · not-assessed | practice-frame | self-chosen, agent-suggested, inherited-from-practice | — | `gestalt-basic` |
| `process-work` | Process-oriented perspective (stub) | `process-experiential` | stub | not-assessed | not-assessed · not-assessed · not-assessed | practice-frame | self-chosen, agent-suggested, inherited-from-practice | — | `process-work-basic` |
| `contemplative-observation` | Contemplative observation (stub) | `contemplative` | stub | not-assessed | not-assessed · not-assessed · not-assessed | practice-frame | self-chosen, agent-suggested, inherited-from-practice | — | `contemplative-observation-basic` |
| `cognitive-appraisal` | Cognitive appraisal (stub) | `explanatory-model` | stub | not-assessed | not-assessed · not-assessed · not-assessed | theoretical-model | self-chosen, agent-suggested, inherited-from-practice | — | `cognitive-appraisal-basic` |
<!-- lens-catalog:end -->

### 7.2 Exploratory questions

<!-- lens-questions:start -->
| Lens | Exploratory questions | Does not establish |
|---|---|---|
| `big-five` | Which of these tendencies do you recognise, and in which settings? Where does the score not fit your experience? | what the person will do in a given moment; any clinical condition; job fit |
| `hexaco` | Where do you recognise fairness and modesty in how you act? Where does the score not fit your experience? | what the person will do in a given moment; moral character or trustworthiness; any clinical condition; job fit |
| `jungian-type` | Which description fits you best? In which situations does the other pole show? | that the person belongs to a distinct type; ability, performance or job fit; any clinical condition |
| `enneagram` | Which pattern do you recognise under stress? What helps when that pattern is strong? | that nine distinct types exist; any diagnosis; job fit |
| `via-strengths` | Which strengths did you use in that episode? Which strength would you like to use more? | how the person compares with others; skill or competence; job fit or placement |
| `schwartz-values` | Which values pulled against each other here? Which value would you not give up in this situation? | which values are right; political or religious views; comparisons between people |
| `attachment-2d` | In close relationships, what do you tend to watch for? | any diagnosis; anything about another person; how a relationship will go |
| `ifs` | Which inner positions and needs are active right now? What might this part be afraid would happen if it stepped back? | the existence of parts; any diagnosis; the efficacy of agent-offered use |
| `cbt` | Which interpretations and expectations shaped the reaction and the action? What else could be true? | clinical efficacy for this person; any diagnosis |
| `needs-grid` | Which cells are empty, stale or contested? Is there a cell you would rather leave empty? | any need the person has not stated; that an empty cell is a problem |
| `astrology` | How does this language help you describe your experience? | any trait, state or behaviour of the person; predictions; compatibility with other people |
| `human-design` | How does this language help you describe your experience? | any trait, state or behaviour of the person; predictions; compatibility with other people |
| `gestalt` | What remains unfinished and seeks awareness? | anything about the person; the efficacy of the approach |
| `process-work` | Which less familiar process wants to appear? | anything about the person; the efficacy of the approach |
| `contemplative-observation` | What changes when experience is observed without fixing on a stable self? | anything about the person; the efficacy of the approach |
| `cognitive-appraisal` | Could this be uncertainty, load or incubation rather than a personal flaw? | anything about the person; the efficacy of the approach |
<!-- lens-questions:end -->

### 7.3 Evidence-grade markers

Every citation carries a grade:

| Grade | Meaning | Marker in documentation |
|---|---|---|
| `F` | Fact from a primary source that was read. | none |
| `F2` | Fact from a secondary source; to be re-verified before normative use. | **[F2]** |
| `U` | Unverified, or a known gap. | **[U]** |
| `verify` | Taken from general knowledge or an indirect source; to be checked. | **[verify]** |

Facts graded `F2`, `U` or `verify` never appear in normative text. They are listed here with their markers (LN-13).

<!-- lens-evidence:start -->
| Lens | Reference | Grade | Note |
|---|---|---|---|
| `big-five` | doi:10.1177/0956797619831612 | F | Soto 2019: 87% of replication attempts significant in the expected direction |
| `big-five` | doi:10.1037/0033-2909.126.1.3 | F | Roberts & DelVecchio 2000: rank-order consistency .31 in childhood to about .74 at ages 50-70 |
| `big-five` | doi:10.1016/j.jrp.2014.05.003 | F | Johnson 2014: IPIP-NEO-120 |
| `hexaco` | doi:10.1177/1088868306294907 | F | Ashton & Lee 2007: 'a viable alternative to the well-known Big Five', based on a cross-culturally replicated six-dimensional structure |
| `jungian-type` | doi:10.1111/j.1467-6494.1989.tb00759.x | F | McCrae & Costa 1989 (N = 267 men, 201 women): no support for truly dichotomous preferences or distinct types; the instrument measures four relatively independent dimensions |
| `jungian-type` | Pittenger 1993, as cited in a secondary source | **[F2]** | Between 39% and 76% of respondents received a different type on retest after five weeks [verify] |
| `jungian-type` | The Myers-Briggs Company, Trademark Guidelines, guideline 5 | **[verify]** | Use the MBTI marks only for genuine MBTI products and services; other instruments must not be described with them. Revision date of the guidelines to be re-checked |
| `jungian-type` | Myers & McCaulley 1985, Manual: A Guide to the Development and Use of the Myers-Briggs Type Indicator, as cited in a secondary source | **[F2]** | The judging–perceiving preference was added by Briggs and Myers; Jung's typology has the two attitudes and four functions |
| `enneagram` | doi:10.1002/jclp.23097 | F | Hook et al. 2021 (104 independent samples): 'mixed evidence of reliability and validity'; factor analyses typically find fewer than nine factors; little research supports wings |
| `via-strengths` | doi:10.1080/00223891.2022.2120402 | F | McGrath 2023: five samples, total N = 7,924; findings 'generally support the construct validity ... with exceptions noted' |
| `via-strengths` | VIA Institute on Character, permissions and guidelines for use and interpretation | F | Not recommended for personnel selection or placement decisions. Paraphrase of the guidance: the measures are most appropriate for insight into groups through aggregated data; they can be used with one person to estimate the relative strength of the 24 strengths within that person; people should not be compared with one another |
| `via-strengths` | VIA Institute on Character, survey availability | **[F2]** | The survey is free to individuals |
| `schwartz-values` | doi:10.1037/a0029393 | F | Schwartz et al. 2012: values form a circular motivational continuum; analyses support discrimination of the 19 values |
| `schwartz-values` | PMC9131418 | F | PVQ-RR measured all four higher-order values reliably in every cultural group studied; article licensed CC BY-NC 4.0 |
| `schwartz-values` | PVQ-RR instrument licence | **[U]** | The licence of the instrument itself was not found; versions and scoring instructions are distributed through the Open Science Framework |
| `attachment-2d` | doi:10.1037//0022-3514.78.2.350 | F | Fraley, Waller & Brennan 2000: item response theory analysis of self-report attachment measures |
| `attachment-2d` | R. Chris Fraley, ECR-R measure page | F | Classifying people by their scores reduces the precision of measurement |
| `ifs` | doi:10.3899/jrheum.121465 | F | Shadick et al. 2013: one proof-of-concept RCT (n = 79) in rheumatoid arthritis; some outcomes sustained at one year, others not |
| `cbt` | doi:10.1007/s10608-012-9476-1 (Hofmann et al. 2012, review of meta-analyses) | **[verify]** | Clinical efficacy literature not reviewed in this workflow |
| `astrology` | doi:10.1038/318419a0 | **[F2]** | Carlson 1985, Nature 318:419: chance-level matching in a double-blind test |
| `human-design` | Court of Florence, judgment of 3 June 2020 | **[F2]** | IP: no copyright in the system itself |
| `human-design` | USPTO registration No. 7724676 | F | IP: 'MYBODYGRAPH HUMAN DESIGN' registered 11 Mar 2025; owner Jovian Archive Media Pte. Ltd. |
| `human-design` | USPTO serials 97642294 and 98217560 | F | IP: both applications for 'THE HUMAN DESIGN SYSTEM' were abandoned |

Instrument citations graded F2, U or verify:

| Instrument | Reference | Grade | Note |
|---|---|---|---|
| `mbti-form-m` | The Myers-Briggs Company, Trademark Guidelines, guideline 5 | **[verify]** | Marks only for genuine MBTI® results; revision date to be re-checked |
| `mbti-form-q` | The Myers-Briggs Company, Trademark Guidelines, guideline 5 | **[verify]** | Marks only for genuine MBTI® results; revision date to be re-checked |
| `pvq-rr` | PVQ-RR instrument licence | **[U]** | Not found; commercial terms unknown |
| `via-is-r` | VIA Institute on Character, survey availability | **[F2]** | Free to individuals |
<!-- lens-evidence:end -->

### 7.4 Instruments

<!-- lens-instruments:start -->
| Instrument | Lens | Publisher | Forms | Items licence | Scoring | Listing |
|---|---|---|---|---|---|---|
| `bfi-2` (BFI-2 (Big Five Inventory-2)) | `big-five` | Christopher J. Soto and Oliver P. John (authors and copyright holders) | 60: 60 items | Copyright Soto & John; not in the public domain; free for non-commercial research only; commercial use requires a request to the authors | public | ok |
| `ipip-neo-120` (IPIP-NEO-120) | `big-five` | International Personality Item Pool (public domain) | 120: 120 items | IPIP items are public domain, usable for any purpose, commercial or non-commercial | public | ok |
| `neo-pi-3` (NEO-PI-3) | `big-five` | PAR, Inc. | self-report: 240 items; informant-report | Proprietary; copyright PAR, Inc., all rights reserved | proprietary | reference-by-url |
| `hexaco-pi-r` (HEXACO-PI-R) | `hexaco` | Kibeom Lee and Michael C. Ashton (authors) | 60: 60 items; 100: 100 items; 200: 200 items | Free to download only for non-profit academic research; online use only on password-protected or not-searchable pages; non-academic use: contact the authors. Copyright 2009 Kibeom Lee and Michael C. Ashton | public | ok |
| `mbti-form-m` (MBTI® Form M) | `jungian-type` | The Myers-Briggs Company (exclusive publisher of the MBTI® instrument) | M: 93 items | Proprietary; the MBTI® instrument may not be reproduced without written permission from the publisher | proprietary | ok |
| `mbti-form-q` (MBTI® Form Q (Step II)) | `jungian-type` | The Myers-Briggs Company (exclusive publisher of the MBTI® instrument) | Q: 144 items | Proprietary; the MBTI® instrument may not be reproduced without written permission from the publisher | proprietary | ok |
| `rheti-2.5` (RHETI® v2.5) | `enneagram` | The Enneagram Institute | 2.5: 144 items | Proprietary (The Enneagram Institute) | proprietary | ok |
| `gacs` (Global Assessment of Character Strengths (GACS)) | `via-strengths` | VIA Institute on Character | adult | Copyright VIA Institute on Character | proprietary | reference-by-url |
| `via-is-r` (VIA Inventory of Strengths-Revised (VIA-IS-R)) | `via-strengths` | VIA Institute on Character | adult | Copyright VIA Institute on Character; free to individuals [F2] | proprietary | reference-by-url |
| `pvq-rr` (Portrait Values Questionnaire - Revised (PVQ-RR)) | `schwartz-values` | Shalom H. Schwartz and colleagues (versions and scoring instructions distributed through the Open Science Framework) | 57: 57 items | Unknown [U]: the instrument licence was not found | public | ok |
| `ecr-r` (Experiences in Close Relationships - Revised (ECR-R)) | `attachment-2d` | R. Chris Fraley, Niels G. Waller and Kelly A. Brennan (authors) | 36: 36 items | Free for non-commercial research without contacting the authors; commercial applications require permission | public | ok |
<!-- lens-instruments:end -->

### 7.5 Mappings between lenses

**Population-level; never identity; never chained.** A mapping row describes a statistic about populations. It is
never used to convert one person's result, and two rows are never combined.

<!-- lens-mappings:start -->
| Mapping | From → to | Relation | Statistic | Row status | Grade |
|---|---|---|---|---|---|
| `astrology--any` | astrology → any empirical construct in any lens | no-relation | — | not-permitted | **[F2]** |
| `enneagram--big-five--hook-2021` | enneagram → big-five | correlates | Review of 104 independent samples; correlation magnitudes not retrieved | unresolved | **[U]** |
| `hexaco--big-five--ashton-lee-2007` | hexaco → big-five | corresponds | — | not-identity | F |
| `human-design--any` | human-design → any empirical construct in any lens | no-relation | — | not-permitted | **[U]** |
| `jungian-type.EI--big-five.E--mccrae-costa-1989` | jungian-type/EI → big-five/E | correlates | r = −.74; n = 267; US adults, men; women reported separately | accepted-with-loss | **[F2]** |
| `jungian-type.JP--big-five.C--mccrae-costa-1989` | jungian-type/JP → big-five/C | correlates | r = −.49; n = 267; US adults, men; women reported separately | accepted-with-loss | **[F2]** |
| `jungian-type.SN--big-five.O--mccrae-costa-1989` | jungian-type/SN → big-five/O | correlates | r = .72; n = 267; US adults, men; women reported separately | accepted-with-loss | **[F2]** |
| `jungian-type.TF--big-five.A--mccrae-costa-1989` | jungian-type/TF → big-five/A | correlates | r = .44; n = 267; US adults, men; women reported separately | accepted-with-loss | **[F2]** |
<!-- lens-mappings:end -->

### 7.6 How each lens works with a person

<!-- lens-how:start -->

Generated from the descriptors and their playbooks by `tools/lens_tables.py`. 16 entries: 12 descriptors, which together carry 18 toolkit items and at least one representation each, and 4 stubs, whose mental model is sketched but whose toolkit and representations are not described yet. Every entry lists its playbooks, with the situations each covers and the tools it offers (§2.2).

#### `astrology`: Astrology (as a self-description frame)

| | |
|---|---|
| Mental model | A chart computed from birth data offers symbols the person may find meaningful for describing their experience. |
| Attends to | how the person uses the language; what it helps the person put into words |
| Stance | symbolic and person-chosen |
| How change happens | Not addressed by OHC; the person decides how the frame is used. |
| Agent posture | Do: use the person's own words. Don't: treat frame attributes as facts about the person; present a frame attribute, or anything read from it, as an empirical trait or a prediction. |
| A helper must not | map chart attributes to any empirical construct |
| Toolkit | Chart from birth data (instrument-use; facilitation `self`; no practitioner required; an agent may offer it) |
| Representations | `astrology.chart` (chart) |
| Playbooks | `astrology-basic` by OHC editors: Looking back at something that happened (`astrology.chart`); Choosing between options; Preparing a hard conversation |

#### `attachment-2d`: Adult attachment (two dimensions)

| | |
|---|---|
| Mental model | People differ in how much they worry about closeness and how much they keep distance; both are continuous dimensions. |
| Attends to | what the person watches for in closeness; the relationship target the result refers to |
| Stance | descriptive and non-pathologising |
| How change happens | Gradually, with experience in relationships. |
| Agent posture | Do: keep the relationship target explicit; ask what the person recognises. Don't: assign a category; describe the other person in a relationship; bring the topic up unprompted. |
| A helper must not | describe a partner's or any other person's attachment (TP-1); present a category as a diagnosis; use results in any work context |
| Toolkit | Record a questionnaire result (instrument-use; facilitation `self`; no practitioner required; an agent never offers it) |
| Representations | `attachment-2d.two-dimension-plot` (chart) |
| Playbooks | `attachment-2d-basic` by OHC editors: Preparing a hard conversation in a close relationship; After a setback in a close relationship; Looking back at something that happened in a close relationship |

#### `big-five`: Big Five (Five-Factor Model)

| | |
|---|---|
| Mental model | People differ in typical tendencies across situations; these are measured, not diagnosed. |
| Attends to | typical tendencies across settings; differences from a reference population; fit with recent episodes |
| Stance | descriptive and comparative |
| How change happens | Slowly, mostly across years; rank-order stability rises with age. |
| Agent posture | Do: show raw score, range and norm group together; ask where the score does not fit. Don't: predict a single moment from a trait; use a score to explain away what the person says. |
| A helper must not | present a score as evidence of fit for a job or role; comment on facet Anxiety or Depression unless the person raises it |
| Toolkit | Fit check (exercise; facilitation `self`; no practitioner required; an agent may offer it) |
| Representations | `big-five.score-profile` (score-profile) |
| Playbooks | `big-five-basic` by OHC editors: Planning the week ahead (`big-five.fit-check`); Choosing between options; Giving feedback to someone; Looking back at something that happened (`big-five.fit-check`); Preparing a hard conversation; Under strain: tired, pressed or overloaded |

#### `cbt`: Cognitive-behavioural lens (non-clinical use)

| | |
|---|---|
| Mental model | Thoughts, feelings and actions influence each other; small tests of an expectation can change it. |
| Attends to | thoughts before an action; expectations; what was done; what else could be true |
| Stance | collaborative and empirical |
| How change happens | By noticing and testing interpretations and trying small different actions. |
| Agent posture | Do: ask what went through the mind; offer the thought record as an option. Don't: label distortions; argue the person out of a view. |
| A helper must not | apply distortion or diagnosis labels; present itself as CBT therapy |
| Toolkit | Thought record (worksheet; facilitation `self`; no practitioner required; an agent may offer it) |
| Representations | `cbt.thought-record` (thought-record) |
| Playbooks | `cbt-basic` by OHC editors: Under strain: tired, pressed or overloaded (`cbt.thought-record`); After a setback (`cbt.thought-record`); Preparing a hard conversation (`cbt.thought-record`); Choosing between options |

#### `cognitive-appraisal`: Cognitive appraisal (stub)

| | |
|---|---|
| Mental model | How a situation is appraised shapes the response; difficulties often have situational explanations. |
| Attends to | uncertainty; load; incubation; explanations other than personal flaws |
| Stance | explanatory and non-blaming |
| How change happens | Not described in this stub. |
| Agent posture | Do: mention the perspective only when the person asks for ways of looking; use the person's own words. Don't: run exercises from it. |
| A helper must not | present itself as practising the approach |
| Toolkit | Not described yet (stub). |
| Representations | Not described yet (stub). |
| Playbooks | `cognitive-appraisal-basic` by OHC editors: Under strain: tired, pressed or overloaded; After a setback; Looking back at something that happened |

#### `contemplative-observation`: Contemplative observation (stub)

| | |
|---|---|
| Mental model | Experience can be observed as it arises, without fixing it to a stable self-image. |
| Attends to | how experience arises and changes; what happens when it is not fixed to a self-image |
| Stance | observational and non-fixing |
| How change happens | Not described in this stub. |
| Agent posture | Do: mention the perspective only when the person asks for ways of looking; use the person's own words. Don't: run exercises from it. |
| A helper must not | present itself as practising the approach |
| Toolkit | Not described yet (stub). |
| Representations | Not described yet (stub). |
| Playbooks | `contemplative-observation-basic` by OHC editors: Under strain: tired, pressed or overloaded; After a setback; Looking back at something that happened |

#### `enneagram`: Enneagram (nine motivational patterns)

| | |
|---|---|
| Mental model | Nine patterns describe what a person tends to move towards and away from; recognising one's pattern is used as a starting point for growth. |
| Attends to | what the person moves towards or away from; patterns under stress and at ease; the person's own recognition |
| Stance | reflective and growth-oriented |
| How change happens | Through noticing the pattern in daily life, often over a long time. |
| Agent posture | Do: ask which pattern the person recognises; stay with the person's description. Don't: type the person; speak about core fears unless the person brings them; use school names as generic labels. |
| A helper must not | present type descriptions as facts about the person; present a type as evidence of fit for a role, task or team |
| Toolkit | Pattern recognition (exercise; facilitation `self`; no practitioner required; an agent may offer it); Record an instrument result (instrument-use; facilitation `self`; no practitioner required; an agent never offers it); Typing interview (dialogue; facilitation `practitioner`; practitioner required; an agent never offers it) |
| Representations | `enneagram.type-label` (type-label) |
| Playbooks | `enneagram-basic` by OHC editors: Under strain: tired, pressed or overloaded (`enneagram.recognition`); Looking back at something that happened (`enneagram.recognition`); Preparing a hard conversation; Choosing between options |

#### `gestalt`: Gestalt perspective (stub)

| | |
|---|---|
| Mental model | Experience is organised into wholes; what remains unfinished keeps asking for attention. |
| Attends to | what remains unfinished; what is happening now |
| Stance | experiential and present-centred |
| How change happens | Not described in this stub. |
| Agent posture | Do: mention the perspective only when the person asks for ways of looking; use the person's own words. Don't: run exercises from it. |
| A helper must not | present itself as practising the approach |
| Toolkit | Not described yet (stub). |
| Representations | Not described yet (stub). |
| Playbooks | `gestalt-basic` by OHC editors: Preparing a hard conversation; After a setback; Looking back at something that happened |

#### `hexaco`: HEXACO model of personality structure

| | |
|---|---|
| Mental model | People differ in six broad tendencies across situations, including how fair and modest they tend to be; these are measured, not diagnosed. |
| Attends to | typical tendencies across settings; fairness and modesty in how the person acts; differences from a reference population; fit with recent episodes |
| Stance | descriptive and comparative |
| How change happens | Slowly, mostly across years. |
| Agent posture | Do: show raw score, range and norm group together; ask where the score does not fit. Don't: treat Honesty-Humility as a measure of trustworthiness; translate HEXACO scores into Big Five scores. |
| A helper must not | present a score as evidence of fit for a job or role; comment on Honesty-Humility to anyone but the person; comment on the Anxiety or Fearfulness facets unless the person raises them |
| Toolkit | Fit check (exercise; facilitation `self`; no practitioner required; an agent may offer it) |
| Representations | `hexaco.score-profile` (score-profile) |
| Playbooks | `hexaco-basic` by OHC editors: Planning the week ahead (`hexaco.fit-check`); Choosing between options; Giving feedback to someone; Looking back at something that happened (`hexaco.fit-check`) |

#### `human-design`: Human Design (as a self-description frame)

| | |
|---|---|
| Mental model | A chart computed from birth data offers a symbolic system the person may use for self-description. |
| Attends to | how the person uses the system's terms; what it helps the person put into words |
| Stance | symbolic and person-chosen |
| How change happens | Not addressed by OHC; the person decides how the frame is used. |
| Agent posture | Do: use the person's own words. Don't: treat frame attributes as facts about the person; present a frame attribute, or anything read from it, as an empirical trait or a prediction. |
| A helper must not | map chart attributes to any empirical construct |
| Toolkit | Chart from birth data (instrument-use; facilitation `self`; no practitioner required; an agent may offer it) |
| Representations | `human-design.chart` (chart) |
| Playbooks | `human-design-basic` by OHC editors: Looking back at something that happened (`human-design.chart`); Choosing between options; Preparing a hard conversation |

#### `ifs`: Internal Family Systems (as a parts lens)

| | |
|---|---|
| Mental model | Inner multiplicity is normal; parts protect; change comes through relationship, not removal. |
| Attends to | which part is speaking; what it protects; polarisations between parts |
| Stance | relational and non-pathologising |
| How change happens | Through relationship with parts, usually with a practitioner for deeper work. |
| Agent posture | Do: reflect the person's own words; stay with noticing. Don't: interpret parts; go toward exiles or burdens; suggest unburdening. |
| A helper must not | present itself as doing IFS therapy; name or invent parts; work with exiles or burdens |
| Toolkit | Noticing a part (exercise; facilitation `self`; no practitioner required; an agent never offers it); Working with exiles (dialogue; facilitation `practitioner`; practitioner required; an agent never offers it) |
| Representations | `ifs.parts-map` (parts-map) |
| Playbooks | `ifs-basic` by OHC editors: Under strain: tired, pressed or overloaded; Preparing a hard conversation; After a setback |

#### `jungian-type`: Psychological type (four preference pairs, after Jung)

| | |
|---|---|
| Mental model | People show preferences on four pairs of poles; a type is a starting point that the person checks by best fit, not a verdict. |
| Attends to | which description the person recognises; pole clarity; situations where the opposite pole shows |
| Stance | descriptive and self-confirming |
| How change happens | Preferences are treated as relatively stable; the person may revise the best-fit type at any time. |
| Agent posture | Do: offer the best-fit question; show pole clarity when it is available. Don't: assign a type to the person; explain behaviour away by type; label any non-MBTI® result with the MBTI® marks. |
| A helper must not | derive a type from Big Five or other scores; present a type as evidence of fit for a role, task or team |
| Toolkit | Best-fit check (exercise; facilitation `self`; no practitioner required; an agent may offer it); Record a genuine instrument result (instrument-use; facilitation `self`; no practitioner required; an agent never offers it) |
| Representations | `jungian-type.type-label` (type-label) |
| Playbooks | `jungian-type-basic` by OHC editors: Preparing a hard conversation; Giving feedback to someone; Planning the week ahead; Looking back at something that happened (`jungian-type.best-fit`) |

#### `needs-grid`: Needs grid

| | |
|---|---|
| Mental model | Wanting, needing and having do not always line up; a grid shows where they diverge and which cells are empty, stale or contested. |
| Attends to | empty cells; stale cells; contested cells; where wanting and needing diverge |
| Stance | organising and neutral |
| How change happens | The person adds, updates or leaves cells empty; the grid only shows the state. |
| Agent posture | Do: ask which cells are empty, stale or contested; respect cells left empty on purpose. Don't: fill cells for the person; infer needs from other cells. |
| A helper must not | write claims into the grid without the person; present the grid as an assessment |
| Toolkit | Grid review (observation; facilitation `self`; no practitioner required; an agent may offer it) |
| Representations | `needs-grid.grid` (grid) |
| Playbooks | `needs-grid-basic` by OHC editors: Planning the week ahead (`needs-grid.review`); After a setback (`needs-grid.review`); Choosing between options |

#### `process-work`: Process-oriented perspective (stub)

| | |
|---|---|
| Mental model | Alongside familiar ways of experiencing, less familiar processes try to appear and can be followed with attention. |
| Attends to | signals that do not fit the familiar picture; what wants to appear |
| Stance | experiential and process-following |
| How change happens | Not described in this stub. |
| Agent posture | Do: mention the perspective only when the person asks for ways of looking; use the person's own words. Don't: run exercises from it. |
| A helper must not | present itself as practising the approach |
| Toolkit | Not described yet (stub). |
| Representations | Not described yet (stub). |
| Playbooks | `process-work-basic` by OHC editors: Under strain: tired, pressed or overloaded; After a setback; Looking back at something that happened |

#### `schwartz-values`: Schwartz theory of basic human values

| | |
|---|---|
| Mental model | Values form a circle: pursuing one value is compatible with its neighbours and in tension with its opposites. |
| Attends to | values that pulled against each other in a situation; the person's own priorities; neighbouring and opposite values |
| Stance | descriptive and within-person |
| How change happens | Priorities shift slowly with life stage and circumstance. |
| Agent posture | Do: ask which values pulled against each other; show centred scores with their meaning. Don't: compare the person's values with other people; infer political or religious views. |
| A helper must not | infer political or religious views from values; use values to tailor persuasion; turn a measured profile into declared values |
| Toolkit | Values in tension (exercise; facilitation `self`; no practitioner required; an agent may offer it); Record a questionnaire result (instrument-use; facilitation `self`; no practitioner required; an agent never offers it) |
| Representations | `schwartz-values.circular-chart` (chart) |
| Playbooks | `schwartz-values-basic` by OHC editors: Choosing between options (`schwartz-values.values-in-tension`); Planning the week ahead; Preparing a hard conversation; After a setback (`schwartz-values.values-in-tension`) |

#### `via-strengths`: VIA character strengths (by reference)

| | |
|---|---|
| Mental model | Everyone has a profile of character strengths; using one's strongest ones in daily life is a way to act well. |
| Attends to | which strengths showed in an episode; the person's signature strengths; strengths that are underused |
| Stance | appreciative and practical |
| How change happens | By noticing and deliberately using strengths in new ways. |
| Agent posture | Do: ask which strengths showed in an episode; use the person's own top strengths. Don't: compare the person's ranking with other people; infer strengths from behaviour. |
| A helper must not | use rankings for selection or placement; describe a low-ranked strength as a flaw; comment on the Spirituality strength unless the person raises it |
| Toolkit | Strengths in an episode (exercise; facilitation `self`; no practitioner required; an agent may offer it); Record a survey result (instrument-use; facilitation `self`; no practitioner required; an agent never offers it) |
| Representations | `via-strengths.ranked-list` (ranked-list) |
| Playbooks | `via-strengths-basic` by OHC editors: Planning the week ahead; Looking back at something that happened (`via-strengths.strengths-in-episode`); After a setback; Giving feedback to someone |

<!-- lens-how:end -->

## 8. Contributing a lens (informative)

A new descriptor or instrument entry is a proposal (see `CONTRIBUTING.md` and the lens-descriptor issue template).
It is accepted only when:

- it follows the shape in §2 or §3, and passes the LN rules (§2.1);
- it may come with a playbook (§2.2) that passes PB-1 and PB-2;
- every summary, construct description and mental-model text is written in OHC's own words, with no item text,
  report prose or scoring keys;
- every evidence statement has a citation with an honest grade (`F`, `F2`, `U` or `verify`), and the grade markers
  appear in this document;
- trademark and copyright facts are recorded in `ip`, with `legalReviewNeeded: true`; a construct list that may need
  permission is given by reference (`constructsByReference`);
- a living contemplative tradition is named only with written consent from its lineage holders (LN-11);
- examples use synthetic people only, and no descriptor contains any person's data (G2).

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
