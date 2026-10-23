# Instrument import

Module `instrument-import` · format `0.1.0-draft` · **normative-draft**. Requires the module `lenses`
([LENSES.md](LENSES.md)). It adds no kind. It says how a person brings a result of a test they took, from the report
they hold, so that their agent can see it under their agreement.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as described in BCP 14 (RFC 2119,
RFC 8174) when, and only when, they appear in all capitals.

Nothing in this document is legal advice, and nothing here establishes that a result is true, that a test is valid
for any purpose, or that consent was given.

## 1. What this module covers

A person who took a test holds its report. With this module they can bring the result into their context:

1. **The report stays theirs.** The report, when the person stores it, is a Source of kind `instrument-report` in
   their own vault. The subject always has access to their own vault (V-0); a grantee receives the report only under
   the grant's source tiers (§15.3 of the specification; default `none`).
2. **The numbers come in as an AssessmentRecord:** one value per scale, the date the test was taken and the norm
   group, as the report shows them. What the report does not show stays empty.
3. **The person decides on it** (R-A1): it fits, parts fit, not sure, I dispute it, it does not fit, or later.
4. **The person's agreement decides what an agent may see and do** (the Grant, §12 of the specification). The lens
   carries facts; the instrument entry says how a result is shaped. Neither carries a permission.

An **imported result** is an AssessmentRecord whose `importedFrom.system` is an instrument id
(`urn:ohc:instrument:…`). Records written by earlier converters, whose `importedFrom.system` names software, are not
imported results in this sense; the rules of §3 do not apply to them.

## 2. The instrument `import` block

An instrument entry ([LENSES.md](LENSES.md) §3) MAY carry an `import` block. Only an instrument with a block can be
the source of an imported result (IMP-2).

| Field | Type | Req | Notes |
|---|---|---|---|
| `scoredBy` | `{"partyKind": "organization", "id": URI, "label": string}` | yes | Who produced the scores. `id` is `urn:ohc:scorer:<slug>`; `label` is a role label of at most 60 characters. The context's Party for the scorer carries this `id` as its `uri` (IMP-3). |
| `scores` | [`{"kind", "range": [lo, hi], "integer"?: bool}`] | yes (1–2) | The score kinds a report shows: `raw`, or one standardized scale (`T`, `z`, `percentile`, `stanine`, `sten`). At most one standardized kind (INS-1). |
| `scales` | [construct id] | yes (≥1) | The constructs of the instrument's lens that a report scores, each once. |
| `normGroups` | [`{"id", "label": {"en", "ru"}}`] | no | The norm groups a report may name. |

The blank draft a holder offers the person is generated from this block; it is not a document of the standard.

**Example** (BFI-2, scored from its public key; the domains of the Big Five lens):

```json
"import": {
  "scoredBy": {"partyKind": "organization", "id": "urn:ohc:scorer:bfi-2-report", "label": "Report scorer"},
  "scores": [{"kind": "raw", "range": [1, 5]}],
  "scales": ["big-five/O", "big-five/C", "big-five/E", "big-five/A", "big-five/N"]
}
```

- **INS-1.** Import block. A block has the shape above. Every scale is a construct of the instrument's lens (or
  follows its `constructsByReference.idPattern`) and appears once; the score kinds are distinct, at most one of them
  standardized, and every range has `lo` < `hi`; norm-group ids are unique and none is `unknown`.

## 3. Imported results

The rules in this section apply to every imported result. A writer that is not the subject also follows INF-1 (§3.4
of the specification).

- **IMP-1.** Imported result; module claim. A context that holds an imported result lists `lenses` and
  `instrument-import` in `conformance.modules`.
- **IMP-2.** Instrument and values. The instrument entry named by `importedFrom.system` resolves and has an `import`
  block; the record's `instrument.id` equals it, and its `lens.id` equals the instrument's lens. Every result is a
  `dimension-score` whose `construct` is one of the block's `scales` and appears once; its values are of a kind the
  block's `scores` lists (`raw`, or `standardized.type`) and lie within that kind's range, as integers where the block
  says so. `normGroup.id`, when present, is one of the block's `normGroups`. `validityFlags` contains
  `vendor-algorithm-undisclosed` when the instrument's `scoring` is `proprietary`. When the entry's `version` differs
  from `importedFrom.systemVersion`, the checker warns (W-IMP2) instead of checking scales and values.
- **W-IMP2.** Warning: the instrument entry's version differs from the record's `importedFrom.systemVersion`; scales
  and values were not checked against the block.
- **IMP-3.** Who asserts, records and decides. `assertedBy` is the Party whose `uri` equals the block's `scoredBy.id`,
  with `partyKind` `organization`, never `"subject"`; `recordedBy` is `"subject"`; `origin` is `imported`. The result is
  therefore proposed until the subject decides on it (R-A1). A scorer Party is reused only when its `uri` is equal,
  never by its label.
- **IMP-4.** The report. When the person stored the report, the result's `source` names a Source of kind
  `instrument-report` whose stored `sensitivity` and `categories` are at least the result's.
- **IMP-5.** Time. `formulatedAt` is the first day of `administeredAt` (its `end`, else its `start`) at 00:00:00Z, and
  that day is not later than `recordedAt`. The freshness anchor (§7.2 of the specification) of an imported result is
  `administeredAt`, not `recordedAt`.
- **W-IMP6.** Warning: two current imported results (neither superseded, declined nor retracted) have the same
  `instrument.id`, the same `administeredAt` and JCS-equal `results`. A correction supersedes the earlier result with
  the same `assertedBy` (R-V2).

**Self-report scales.** A result of a self-report instrument that the subject took counts as declared for R-X3, its
emotion or affect scales included: it is not quarantined and keeps its ordinary tier, `special` (AR-5). R-X4 is
unchanged: no record holds an emotion value derived from biometric or behavioural signals.

**What a record never carries.** No item text, report prose, scoring keys or raw responses (AR-3). The person's own
report in their own vault is a Source, not a field of the record.

**Example** (an imported result, abridged to two scales):

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:big-five", "version": "0.2.0"},
 "instrument": {"id": "urn:ohc:instrument:bfi-2", "form": "60"}, "mode": "self-report-instrument",
 "assessedBy": "subject", "administeredAt": {"start": "2026-09-14", "precision": "day"},
 "results": [
   {"type": "dimension-score", "construct": "big-five/E", "label": "Extraversion", "raw": 2.9},
   {"type": "dimension-score", "construct": "big-five/C", "label": "Conscientiousness", "raw": 4.2}],
 "origin": "imported", "assertedBy": "o-01", "recordedBy": "subject", "recordedAt": "2026-10-01T18:00:00Z",
 "formulatedAt": "2026-09-14T00:00:00Z",
 "importedFrom": {"system": "urn:ohc:instrument:bfi-2", "systemVersion": "0.2.0",
                  "importedAt": "2026-10-01T18:00:00Z"},
 "source": "src-01", "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

Here `o-01` is the Party `{"id": "o-01", "partyKind": "organization", "label": "Report scorer", "uri":
"urn:ohc:scorer:bfi-2-report"}`, and `src-01` is the person's report, a Source of kind `instrument-report`.

## 4. Agents

An agent that helps a person bring a result follows these rules and the procedure CONTEXT-10.

- **IMA-1.** The person's own result. Bring only a result about the person that the person hands over.
- **IMA-2.** Blank stays blank. Never write a value the report does not show, whether from another scale,
  instrument, lens or the report's text.

The agent never confirms, decides, grants, erases or types for the person in the holder's window (C-8…C-10, H-17).
What it may then see, infer or decide is the person's grant: `read` to see a result, `infer` to offer hypotheses
from it (filed as proposals, INF-1), `decisionUse: approval-required` to weigh a result the person accepted when it
proposes something for them (R-G14), and `storage` for its notes between sessions (C-1).

## 5. Holders: the agreement screen

- **IMH-1.** The agreement screen. Before the person confirms a grant that reaches an imported result, the holder
  shows: (1) one row per result, with the person's stance, the words that go with it, and the playbooks the agent
  will receive with it ([LENSES.md](LENSES.md) §2.2); (2) next to each row, in plain words, the lens's facts: what it
  supports and does not establish, the publisher's own stated limits, and the special categories that protect the
  result, naming the construct that raises them; (3) the grant's terms in plain words, each with an example, each
  ticked unless the grantee's operator is the person's employer or school: hypotheses (`infer`), weighing in what the
  agent proposes (`decisionUse`), notes between sessions (`storage`), and the expiry; (4) every purpose of §8.10 of
  the specification; (5) the grantee view (H-15); (6) word for word, the text the grant will store as `basis.note`:
  the agent's own, or the holder's default when the agent gave none. What the grantee will not receive is shown to the person only. When
  the grantee's operator is the person's employer or school, the screen pre-ticks nothing, says so, and follows §12.4
  of the specification.

**Defaults.** Between the person and their own agent the screen opens with everything ticked: each result row, the
person's words, and the three terms. The person unticks what they do not want. Confirming the whole screen in the
person's own window is the explicit consent (§12.1 of the specification); the ticks are not. One screen records one
grant: rows differ only in what is seen, and every other term is grant-wide. To keep hypotheses away from one result
only, the person marks that record `no-infer` (§8.5).

**What stays closed whatever is ticked.** Prohibited purposes, for every grantee, the person's own agent included
(§8.10); special records only through a selector that names them, under explicit consent (R-G3); at most 180 days for
a grant with `infer` or special records (R-G10); nothing pre-ticked for an employer's or school's agent (§12.4).

**Later changes.** Unticking later withdraws the grant (`withdraw-grant`, `ohc.revocation-notice`, purge by
`purgeBy`, C-12) and records a new one the person confirms. Erasing a result: the holder first shows what cites it
and the report Source, and the person chooses what goes with it; words the person keeps keep their tier unless the
person relaxes it (C3, §15.5).

## 6. What the agent receives

A projection carries an imported result like any AssessmentRecord, with its status in `derived`: `endorsedPart` for a
partly endorsed result (PJ-8), and, in `summary` mode, without `importedFrom` and `source` (§12.2). `obligations`
carry the grant's `decisionUse` (R-G14). A holder's rendering for a persistent agent adds the descriptor's own
description of each scale, the lens's facts and language guidance, and the playbooks of the served lenses (PB-5).

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
