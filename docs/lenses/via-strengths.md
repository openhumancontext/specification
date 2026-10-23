# Lens recipe: VIA character strengths (by reference)

**Recipe · lens `urn:ohc:lens:via-strengths` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe shows, step by step, how a person's character strengths (from a survey report they own, from their coach, teacher or therapist, or from their own account of episodes) become OHC records that the person controls.

The lens descriptor is [spec/lenses/via-strengths.lens.json](../../spec/lenses/via-strengths.lens.json): `descriptorStatus: draft`, kind `strengths-ranked`, measurement tier `T2` (validated with caveats), ontological status `measured-construct`. The lens supports self-reflection on strengths in use and choosing practices that use the person's strengths. It does not establish how the person compares with others, skill or competence, or job fit or placement. A ranking describes one person and is never compared with anyone else (M-5).

The classification of strengths is copyrighted and is **referenced, not reproduced**: the descriptor has no construct list, only `constructsByReference` with the id pattern `via-strengths/<n>`, where `<n>` is a strength's published name in lowercase, with its words joined by hyphens.

The record shapes are in [SPECIFICATION.md](../../spec/SPECIFICATION.md) §10.5 (LensAdoption), §10.6 (AssessmentRecord), §10.3 (Interpretation), §17 (Practice, Outcome) and §12 (Grant); the schemas are in [spec/schema/](../../spec/schema/). The lens rules are in [LENSES.md](../../spec/LENSES.md).

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them.

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:via-strengths-basic`](../../spec/playbooks/via-strengths-basic.playbook.json) (VIA character strengths: basic ways of working, by the OHC editors), for these situations: planning the week ahead; looking back at something that happened; after a setback; giving feedback to someone. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

**Bringing a report through the person's window.** When an instrument's catalog entry carries an `import` block, a person can bring its result through their own window ([guide](../guides/BRING-A-RESULT.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). No entry of this lens has one yet, so the steps below record the report by hand.

## 1. What you may have

| Input | Use it? | Where it goes |
|---|---|---|
| The person's own account of their strengths, said in conversation ("curiosity is what carries me") | Yes | A Claim in their words (step 4) |
| A survey report the person took and owns: VIA-IS-R or GACS, the two instruments of the 0.1 catalog. The survey is free to individuals **[F2]** | Yes | Source (step 2) and AssessmentRecord with `mode: vendor-report-import` (step 3) |
| The person's own choice of their strongest strengths, without a survey | Yes | A Claim in their words (step 4), or an AssessmentRecord with `mode: self-identified` (step 3, variant) |
| Notes from a coach, teacher or therapist who works with the strengths | Yes, with the practitioner's written release | Route `inherited-from-practice` with `practice.releaseRef` (step 1), release and notes Sources (step 2, variant) |
| The person's accounts of episodes and their own reading of which strengths they used | Yes | Episode and Interpretation (step 5) |
| An agent's reading ("you clearly have leadership") | **Only under the person's Grant** | An Interpretation by the agent needs `suggest` and `infer` naming the lens, and the person's active adoption not set to `off` (I5). The descriptor's agent posture: do not infer strengths from behaviour. In the example the person allows none. |

**[F2]** is an evidence grade: a fact taken from a secondary source, to be re-verified before normative use ([LENSES.md](../../spec/LENSES.md) §7.3; the citation is listed there).

## 2. Before you start

### 2.1 Route of adoption

Choose one route with the person. It decides who writes the LensAdoption and when it becomes active. Step 1 has a complete record for each route that the worked examples use.

| Route | When | What it changes |
|---|---|---|
| `self-chosen` | The person picks the lens themselves. | The person writes the adoption: `assertedBy: "subject"`, `origin: "declared"`, no `practice` block. It is active at once. |
| `agent-suggested` | The person asked an agent for ways of looking at what they do well (the descriptor's `adoption.suggestionRequires`), and accepted the lens the agent offered. | First the person gives the agent a grant with the action `suggest` whose scope names the lens. The agent then writes the adoption under that grant: `suggestedBy` and `assertedBy` are its own Party id, `origin: "observed"` (`declared` is refused by ENV-2), `underGrant` is the grant's id and `purpose` is one of the grant's `purposes`. It stays `proposed` until the person writes a Review `admit` (LA-1). Records: step 1, variant "agent-suggested". |
| `inherited-from-practice` | The lens comes from the person's coach, teacher or therapist (the descriptor's `adoption.inheritanceRoles`). This is the route of the worked example. | The practitioner is a Party with `role: "practitioner"`; the adoption carries a `practice` block. If session material is stored, the practitioner's release is stored first as a Source of kind `practitioner-release`, and the **same id** goes in the adoption's `practice.releaseRef` (LA-3) and in the notes Source's `custody.releaseRef` (SR-7). Set `confidentiality`: `practitioner-scope` for a coach or teacher; for a therapist the person may choose `therapy-confidential`, which makes the adoption `special` and `person-only` (LA-4). LA-4 reaches only records that cite the adoption by id, and the person's own results, readings and practices in this lens do not cite it; so with `therapy-confidential`, also add `"person-only"` to the `handling` of every record that names the lens (section 6). Leave `onEnd` at `ask`: when the relationship ends, a superseding adoption with `"relationship": "ended"` is computed `paused` until the person decides. The adoption gives the practitioner no access (LA-2); access needs a Grant (step 7). |
| `imported` | An importer tool creates the adoption from a survey report. | `origin: "derived"`, `derivedFrom` naming the report Source, `generatedBy` naming the tool, and `importedFrom` with a `run` id; each record's `importedFrom.importedAt` equals its own `recordedAt` (ENV-3). The adoption and every AssessmentRecord with the same `importedFrom.run` stay `proposed` until the person admits them (LA-5). The [schwartz-values recipe](schwartz-values.md) shows this route in full. |

In the example `agentInterpretation` is `"off"` on every route, the default the person keeps: only the person writes readings through this lens (I5). The person may change it.

### 2.2 Consent

- An agent speaks in the lens's language once the person adopted it, in the person's own words; it never infers strengths from behaviour (`agentPosture`).
- Nothing leaves the context without a Grant (R-G1). Every result in this lens is treated as special category: a grant needs `basis.legal: "explicit-consent"`, must name the records by id, by the lens or by the category `mental-health` (R-G3), and lasts at most 180 days (GR-1).
- A practitioner's notes enter the context only with the practitioner's release, stored as its own Source.

### 2.3 Defaults for this lens

| Setting | Value | Why |
|---|---|---|
| `sensitivity` | `"special"` on every record that names the lens (LensAdoption, AssessmentRecord, Interpretation with `lens`, Practice with `source.lens`), on every Source of a report, release or notes, and on every Claim that cites a result | The descriptor's `defaults.sensitivity`; AR-5; I9; propagation rule C3 |
| `categories` | `["mental-health"]`; add `"belief"` to any record that names the strength `via-strengths/spirituality` | The descriptor's `defaults.categories` and `defaults.perConstruct` |
| `handling` on results | `["no-infer"]`; add `"subject-initiated-only"` when the record names `via-strengths/spirituality` | `no-infer`: the person keeps the ranking from every inference and mapping (M-7; the lens also sets `crossLensMapping: not-allowed`). `subject-initiated-only`: the descriptor forbids commenting on that strength unless the person raises it. |
| `reviewAfter` | `"P3Y"` | The descriptor's `defaults.reviewAfter` |
| Source `maxRelease` | `"index"` | The report is the publisher's copyrighted text; a grantee never receives its bytes, title or text |

### 2.4 What is never stored

- Survey item text, item responses, the scoring key and report prose, including the report's descriptions of each strength (AR-3; the instrument entries' `neverStore`). The report file may sit in the person's own vault; no record quotes it.
- The classification itself: the list of strengths with their groups, as reference data. Only the person's own results name strengths, by id.
- A changed classification: own groupings of strengths, merged or renamed strengths (`ip.restrictions`).
- Any comparison with other people: percentiles against others, "above average", group rankings (M-5).
- A low-ranked strength as a weakness or flaw, and any ranking as a judgement of the person.

## 3. Steps

Snippets are records from the worked examples (section 5) and validate against the named schemas. They carry `"synthetic": true` because they are examples. Use opaque ids (`as-1`, never `as-curiosity`; W-ID1). Times are RFC 3339 with an offset.

**Set up the context once.** Create a directory for the context (the *context directory*) and save this skeleton in it as `context.json`. Each step below names the array its record goes in; inside an array, the order of records does not matter.

```json
{"format": "ohc.context", "specVersion": "0.1.0-draft",
 "id": "urn:ohc:example:bento:context", "version": "2026-10-10.1",
 "subject": {"id": "urn:ohc:example:bento", "displayName": "Bento (fictional)"},
 "holder": "subject", "lang": "en", "created": "2026-09-20T18:00:00Z",
 "conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices"], "subjectIsAdult": true},
 "parties": [
   {"id": "p-01", "partyKind": "person", "label": "Coach", "role": "practitioner"},
   {"id": "s-01", "partyKind": "software", "label": "Survey report"}],
 "policy": {"admission": "subject-only", "resolver": "returnDialog"},
 "lenses": [{"id": "urn:ohc:lens:via-strengths", "version": "0.2.0",
             "sha256": "69a5583d8ef60955575b99cf4d706affc7d24c6d987a23d3ba628820e59ca500"}],
 "lensAdoptions": [], "sources": [], "assessments": [], "claims": [], "reviews": [],
 "episodes": [], "interpretations": [], "practices": [], "outcomes": [], "grants": [],
 "synthetic": true}
```

- `format`, `specVersion`, `id`, `version` and `subject` are required (`context.schema.json`). `holder`, `lang`, `created` and `policy` are optional; keep them as shown. Arrays you do not use may be left out.
- `"synthetic": true` marks an example. In an example it MUST be on the context root and on every content record, or the check fails with CX-8. **For a real person**, give `id` and `subject.id` the form `urn:uuid:<a new UUID>`, and leave out `synthetic` at the root and on every record.
- `lenses[].sha256` is the SHA-256 of the descriptor file's bytes: `shasum -a 256 spec/lenses/via-strengths.lens.json`.
- `governance` is needed for Grants (steps 1 and 7), `practices` for Practice and Outcome (step 6).
- Every Party you reference goes in `parties` (CX-3). The main path uses the coach `p-01` and the survey software `s-01`. The variant "agent-suggested" needs `{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}`.
- The check passes only once the context holds a Claim or an Episode with an account (LV-0); before step 4 it reports LV-0.

### Step 1. The person adopts the lens: LensAdoption

The person's coach works with strengths, and the person wants to use this lens. Write one LensAdoption (schema `lens-adoption.schema.json`, array `lensAdoptions`):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:via-strengths", "version": "0.2.0"}, "route": "inherited-from-practice",
 "practice": {"role": "coach", "practitioner": "p-01", "relationship": "active", "since": "2026-06-01"},
 "confidentiality": "practitioner-scope",
 "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"], "interpretationAuthors": ["subject"],
 "agentInterpretation": "off", "representationPreference": "via-strengths.ranked-list", "onEnd": "ask",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:00:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- No `releaseRef` here, because no session material is stored.
- `practice.role` is `coach`, `teacher` or `therapist` (the descriptor's `adoption.inheritanceRoles`).
- Choose `uses` with the person: `speak-in-lens`, `store-results`, `interpret` (the person's own readings), `offer-practices` (an agent may offer `via-strengths.strengths-in-episode`, the only toolkit item with `agentMayOffer: true`), `recall`.

**Variant "coach's notes": session material is stored.** Write the release Source first (step 2, variant), then the adoption with the release id in `practice.releaseRef`, then the notes Source. All are in [examples/via-strengths/variants/coach-notes/context.json](examples/via-strengths/variants/coach-notes/context.json):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:via-strengths", "version": "0.2.0"}, "route": "inherited-from-practice",
 "practice": {"role": "coach", "practitioner": "p-01", "relationship": "active", "since": "2026-06-01", "releaseRef": "src-2"},
 "confidentiality": "practitioner-scope", "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off", "representationPreference": "via-strengths.ranked-list",
 "onEnd": "ask", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:00:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- Without `practice.releaseRef`, LA-3 fails as soon as notes are stored.

**Variant "agent-suggested": the agent offered the lens.** Add `a-01` to `parties` and write three records in this order. All three are in [examples/via-strengths/variants/with-agent/context.json](examples/via-strengths/variants/with-agent/context.json).

(1) The person gives the agent a grant to suggest (array `grants`):

```json
{"id": "g-0", "recordedAt": "2026-09-19T10:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:via-strengths"]}], "exclude": [{"ids": ["as-2"]}]},
 "actions": ["suggest"], "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2027-03-17T00:00:00Z", "storage": "session", "forwarding": false, "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-19T10:00:00Z", "channel": "holder-ui"},
 "note": "The companion may suggest this lens and the episode exercise; it never sees my ranking."}
```

(2) The agent writes the adoption under that grant (array `lensAdoptions`):

```json
{"id": "la-1", "lens": {"id": "urn:ohc:lens:via-strengths", "version": "0.2.0"}, "route": "agent-suggested",
 "suggestedBy": "a-01", "uses": ["speak-in-lens", "store-results", "interpret", "offer-practices"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "representationPreference": "via-strengths.ranked-list", "origin": "observed", "assertedBy": "a-01",
 "underGrant": "g-0", "purpose": "self-reflection", "recordedAt": "2026-09-19T10:05:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

(3) The person admits it (array `reviews`):

```json
{"id": "rv-1", "target": "la-1", "action": "admit", "by": "subject", "recordedAt": "2026-09-19T10:10:00Z"}
```

- `purpose` on the adoption MUST be one of the grant's `purposes`; otherwise INF-1 fails.
- The grant's scope MUST name the lens with `{"lenses": [...]}`. A wildcard such as `{"all": true}`, or a selector that does not name the lens, does not count, and INF-1 fails.
- The grant needs only the action `suggest`. Its `exclude` lists the ids of the person's results (here `as-2`, step 3), so that the suggesting agent never sees them; an id may be listed before its record exists.
- `origin` is `"observed"`: the agent records that the person accepted. `"declared"` fails ENV-2 (section 6).
- Until the person's `admit`, the adoption is `proposed` and no grantee receives it. Only the person writes the `admit` (LA-1).

**Who sees it by default:** only the person. The coach does not see it without a grant.

### Step 2. Keep the original: Source

If the person has a report file or a practitioner's notes:

1. compute the file's SHA-256: `shasum -a 256 <file>`;
2. copy the file into the context directory as `vault/<first two hex characters of the hash>/<hash>.<extension>`;
3. write a Source (schema `source.schema.json`, array `sources`) whose `content.locator.vaultPath` is that same path, relative to the context directory and starting with `vault/`.

```json
{"id": "src-1", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/82/82b74edd1ea2a5c1273c407ff5f91ffee9333e401b0e943c4ea4d7b510b0ce2a.pdf"}, "sha256": "82b74edd1ea2a5c1273c407ff5f91ffee9333e401b0e943c4ea4d7b510b0ce2a", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-18T19:00:00Z", "authorship": {"author": "s-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T18:02:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- `authorship.author` is a software Party for a survey report.
- Give no `title` and no `summary` that repeats report prose.
- When the file is present, the checker reads it and compares its hash with `sha256`; a mismatch fails SR-2. `"vaultContentRead": false` in the checker's report means that the content was not interpreted; the hash is still checked. When the file is absent, as in the worked examples, only the record is checked.

**Variant "coach's notes": the release, then the notes.** The release is the practitioner's written permission to keep the notes. Store it first:

```json
{"id": "src-2", "sourceKind": "practitioner-release",
 "content": {"locator": {"vaultPath": "vault/48/4806966871b1f06873d59a4ffbde1dfa7e4e3050f75278d715d3de4df1596e26.pdf"}, "sha256": "4806966871b1f06873d59a4ffbde1dfa7e4e3050f75278d715d3de4df1596e26", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-19T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T17:50:00Z", "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

Then the notes, citing the same release id:

```json
{"id": "src-3", "sourceKind": "practitioner-notes",
 "content": {"locator": {"vaultPath": "vault/27/2711ac21d0cf3dc92b0945151fdaf5ba811a16a8445142915e1a7420fbdfce02.pdf"}, "sha256": "2711ac21d0cf3dc92b0945151fdaf5ba811a16a8445142915e1a7420fbdfce02", "mediaType": "application/pdf"},
 "capturedAt": "2026-09-19T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "contemporaneity": "contemporaneous", "custody": {"custodian": "p-01", "confidentiality": "coaching", "releaseRef": "src-2"},
 "maxRelease": "index", "retention": {"eraseOnRequest": true}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-20T18:01:00Z", "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

- The release id `src-2` appears twice: in `custody.releaseRef` here (SR-7) and in the adoption's `practice.releaseRef` (step 1; LA-3).
- For a therapist, use `"confidentiality": "therapy"` in `custody`.
- A Claim that rests on the notes cites them as `{"ref": "src-3", "kind": "practitioner"}` (the Claim `c-2` in the coach-notes file).

**Who sees it by default:** only the person, at every tier (V-0). A grantee can receive at most the `index` tier.

### Step 3. Record the result: AssessmentRecord

Write one AssessmentRecord for the survey report (schema `assessment-record.schema.json`, array `assessments`):

```json
{"id": "as-1", "lens": {"id": "urn:ohc:lens:via-strengths", "version": "0.2.0"},
 "instrument": {"id": "urn:ohc:instrument:via-is-r", "form": "adult"}, "mode": "vendor-report-import",
 "assessedBy": "subject", "administeredAt": {"start": "2026-09-18", "precision": "day"},
 "results": [
   {"type": "ranking", "constructs": ["via-strengths/curiosity", "via-strengths/kindness", "via-strengths/honesty", "via-strengths/perseverance", "via-strengths/humor"], "signatureTopN": 5}],
 "validityFlags": ["vendor-algorithm-undisclosed"], "source": "src-1",
 "trademarkNotice": "VIA is used only to name the VIA Institute's instruments; OHC is not authored or endorsed by the VIA Institute.",
 "origin": "imported",
 "importedFrom": {"system": "survey report (PDF), top five copied by the person", "importedAt": "2026-09-20T18:05:00Z"},
 "formulatedAt": "2026-09-18T19:00:00Z", "reviewAfter": "P3Y", "assertedBy": "subject",
 "recordedAt": "2026-09-20T18:05:00Z", "sensitivity": "special", "categories": ["mental-health"],
 "handling": ["no-infer"],
 "note": "Only the five signature strengths are stored; the rest of the order stays in the report.",
 "synthetic": true}
```

- `instrument.id` is `urn:ohc:instrument:via-is-r` or `urn:ohc:instrument:gacs`, whichever the report names (AR-8). Add `instrument.version` only if the report states one.
- `mode: "vendor-report-import"` requires `origin: "imported"` and `importedFrom` (AR-1). `formulatedAt` is when the report was produced; `recordedAt` is when it entered the context (R-T5b).
- `importedFrom.importedAt` equals `recordedAt` (ENV-3). Do not set it to the moment the file was copied.
- **Construct ids.** For each strength, take its name as printed in the report, write it in lowercase, join its words with hyphens, and prefix `via-strengths/`. Drop any sign that is not a letter and keep the words: with placeholder names, `Alpha Beta` becomes `via-strengths/alpha-beta`, and `Alpha & Beta` also becomes `via-strengths/alpha-beta`. Nothing else is recorded about the dropped sign; the gap is listed in section 6.
- **The order.** `constructs` lists the strengths in the report's order, strongest first. `signatureTopN` is the number of signature strengths the report marks. Store the whole order, or only the signature strengths, as the person prefers; when you store only part, say so in `note` (section 6). The worked example stores only the top five, so that a public file does not reproduce the classification's list.
- Store no scores, percentiles or norm groups: the result is a ranking within one person (M-5).
- `trademarkNotice` is copied word for word from the `notice` of the `VIA` mark in the instrument entry ([via-is-r](../../spec/instruments/via-is-r.instrument.json), [gacs](../../spec/instruments/gacs.instrument.json)).
- **If the stored order contains `via-strengths/spirituality`**, set `"categories": ["mental-health", "belief"]` and `"handling": ["no-infer", "subject-initiated-only"]` on this record (the descriptor's `perConstruct`). The whole record then carries them (section 6).

**Variant "self-identified": the person's own choice, without a survey.** From the with-agent file:

```json
{"id": "as-2", "lens": {"id": "urn:ohc:lens:via-strengths", "version": "0.2.0"}, "mode": "self-identified",
 "assessedBy": "subject", "administeredAt": {"start": "2026-09-19", "precision": "day"},
 "results": [{"type": "ranking", "constructs": ["via-strengths/curiosity", "via-strengths/kindness", "via-strengths/humor"]}],
 "validityFlags": ["self-identified-only"],
 "origin": "declared", "reviewAfter": "P3Y", "assertedBy": "subject", "recordedAt": "2026-09-19T10:20:00Z",
 "sensitivity": "special", "categories": ["mental-health"], "handling": ["no-infer"], "synthetic": true}
```

- Compared with `as-1`: `mode: "self-identified"`, `origin: "declared"`, `validityFlags: ["self-identified-only"]`; no `instrument`, `trademarkNotice`, `importedFrom` or `formulatedAt`.
- Keep `assessedBy: "subject"`, `sensitivity`, `categories`, `handling` and `reviewAfter` as in `as-1`, including the Spirituality rule.
- `constructs` are the strengths the person names, in their order. Leave out `signatureTopN`, `note` and `source`, unless the person marks signature strengths (`signatureTopN`) or brings a written list (a Source, cited in `source`).

**Who sees it by default:** only the person. Tier `special`, audience `named`.

### Step 4. What the person accepts: Claim

Ask the person which strengths they recognise, and write only what they say, in their words, as a Claim (schema `claim.schema.json`, array `claims`). Cite the result in `evidence`. The Ground `kind` follows the cited result: `instrument` for a survey result (`as-1`), `subject-statement` for a self-identified result (`as-2`), `practitioner` for a practitioner's notes (`src-3`).

```json
{"id": "c-1", "facet": "disposition", "predicate": "self-described-tendency",
 "text": "Curiosity and kindness are what I lean on most, especially at the repair cafe.",
 "evidence": [{"ref": "as-1", "kind": "instrument"}], "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-20T18:10:00Z", "horizon": "foundation", "contexts": ["community"], "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- In the variant "self-identified", the same Claim cites `{"ref": "as-2", "kind": "subject-statement"}` (the with-agent file).
- Facet `disposition`, not `capability`: the lens does not establish skill or competence. `disposition` requires `origin: "declared"` by the person, or `derived` from an AssessmentRecord (CL-3). Prefer the person's own words.
- Never copy a strength's description from the report into `text`, and never write a Claim about strengths the person ranks low.
- If the person does not recognise the result, they write a Review (schema `review.schema.json`, array `reviews`) `{"id": "rv-3", "target": "as-1", "action": "reject", "by": "subject", "recordedAt": "<now>", "reasonCode": "not-true"}`, or `"partially-endorse"` with `endorsedPart` in their words. The record stays; a rejected record is no longer served to anyone.

**Who sees it by default:** only the person.

### Step 5. Strengths in an episode: Episode and Interpretation

This is the toolkit item `via-strengths.strengths-in-episode`: the person picks a recent episode and notes which strengths they used and how. The episode is an Episode (schema `episode.schema.json`, array `episodes`); the reading is an Interpretation (schema `interpretation.schema.json`, array `interpretations`):

```json
{"id": "ep-1", "occurred": {"start": "2026-09-26", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-26T19:00:00Z", "addedAt": "2026-09-26T19:05:00Z", "accountKind": "in-the-moment", "happened": "At the repair cafe a neighbour brought a radio that would not turn on.", "didOrTried": "Asked what she had already tried, then showed her how to test the fuse; we fixed it together.", "experienced": "Light and awake."}],
 "selection": {"selectedBy": "subject", "reason": "subject-chose"}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-26T19:05:00Z", "contexts": ["community"], "sensitivity": "sensitive", "synthetic": true}
```

```json
{"id": "in-1", "about": ["ep-1"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:via-strengths", "version": "0.2.0"},
 "text": "I used curiosity and kindness: I asked what she had tried before showing anything, and kept it light.",
 "alternatives": [{"text": "It was a quiet afternoon, so there was time to explain.", "kind": "situational"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-27T09:00:00Z",
 "heldDuring": {"from": "2026-09-27"}, "contexts": ["community"], "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

- Only the person writes the reading here (`assertedBy: "subject"`). An agent may offer the exercise and ask the descriptor's questions ("Which strengths did you use in that episode?", "Which strength would you like to use more?"), but an agent's reading through this lens fails I5 while the person's adoption has `agentInterpretation: off`.
- Name only strengths in use, in the person's words. The strengths are named in `text`; there is no structured field for them yet (section 6).
- Ask for at least one alternative that is not psychological (`situational`, `physiological`, `informational` or `external`), so that a good day is not credited to character alone.

**Who sees it by default:** only the person. The Interpretation is `special` because it names a lens (I9).

### Step 6. Practices and outcomes: Practice and Outcome

A way to use a strength in a new way, here suggested by the coach, is a Practice (schema `practice.schema.json`, array `practices`); how it went is an Outcome (schema `outcome.schema.json`, array `outcomes`):

```json
{"id": "pr-1", "name": "One question before every repair",
 "description": "Use curiosity in a new place: ask about the person's own attempt before I touch the tool.",
 "practiceKind": "conversation",
 "source": {"route": "from-practitioner", "lens": "urn:ohc:lens:via-strengths", "by": "p-01"},
 "steps": ["Ask what they have already tried", "Ask what they want to learn", "Only then pick up the tool"],
 "limits": "Not when someone only wants the thing fixed quickly.", "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-30T18:00:00Z", "contexts": ["community"],
 "sensitivity": "special", "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "oc-1", "about": {"practice": "pr-1"}, "result": "helped", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-10-08T20:00:00Z", "contexts": ["community"], "synthetic": true}
```

- The person records the coach's suggestion (`assertedBy: "subject"`, `source.by` the coach). It is active at once.
- A regular "strengths in an episode" practice that the person sets up themselves uses `"source": {"route": "from-lens", "lens": "urn:ohc:lens:via-strengths", "templateId": "via-strengths.strengths-in-episode"}`.
- An Outcome written by anyone other than the person is only an "agent's estimate" (O-1).

**Variant "agent-suggested": the agent offers the episode exercise.** An agent may offer only `via-strengths.strengths-in-episode` (`agentMayOffer: true`). It needs a grant with `suggest` whose scope names the lens: the grant `g-0` of step 1 (write it now, as shown there, if the adoption took another route). The agent writes the Practice; the person admits it. Both are in the with-agent file.

```json
{"id": "pr-2", "name": "Strengths in one episode a week",
 "description": "Once a week, pick an episode and note which strengths I used and how.",
 "practiceKind": "reflection",
 "source": {"route": "from-agent", "lens": "urn:ohc:lens:via-strengths", "templateId": "via-strengths.strengths-in-episode", "by": "a-01"},
 "steps": ["Pick one episode from the week", "Note which strengths I used", "Note one I would like to use more"],
 "limits": "Skip any week it feels like homework.", "initialStatus": "candidate", "nonClinical": true,
 "origin": "observed", "assertedBy": "a-01", "underGrant": "g-0", "purpose": "self-reflection",
 "recordedAt": "2026-09-27T09:00:00Z", "contexts": ["community"], "sensitivity": "special",
 "categories": ["mental-health"], "synthetic": true}
```

```json
{"id": "rv-2", "target": "pr-2", "action": "admit", "by": "subject", "recordedAt": "2026-09-27T09:30:00Z"}
```

- `underGrant` is `g-0`; `purpose` MUST be one of g-0's `purposes` (INF-1). The scope MUST name the lens; a wildcard does not count.
- `initialStatus` is `"candidate"`: the person has not tried it yet. `origin` is `"observed"` and `assertedBy` and `source.by` are the agent (`"declared"` fails ENV-2).
- Until the person's `admit`, the Practice and its Outcomes are withheld from every grantee (PC-1; verified with the projection tool). After it, grantees see the Practice labelled `observed` (section 6).
- An agent never offers `via-strengths.record-result` (PC-2).

**Who sees it by default:** only the person.

### Step 7. Who may see what: Grant

The person lets the coach read the strengths records for their coaching (schema `grant.schema.json`, array `grants`):

```json
{"id": "g-1", "recordedAt": "2026-10-01T09:00:00Z", "grantor": "subject", "grantee": "p-01",
 "purposes": ["coaching"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:via-strengths"]}, {"ids": ["c-1", "oc-1"]}]}, "actions": ["read"],
 "mode": "summary", "interpretations": "subject-endorsed",
 "constraints": {"expiresAt": "2027-03-25T00:00:00Z", "storage": "session", "forwarding": false, "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-10-01T09:00:00Z", "channel": "holder-ui"},
 "note": "For our coaching sessions: my strengths and how the practices went."}
```

- The selector `{"lenses": [...]}` reaches every record that names the lens: the adoption, the result, the reading and the Practice. The Claim and the Outcome do not name a lens; add them by `ids`. The Episode is not shared.
- `basis.legal` MUST be `explicit-consent`; `expiresAt` is at most 180 days after `recordedAt` (GR-1). `purposes` never include a prohibited purpose (section 4).
- `mode: "summary"` drops `note`, `evidence` and the import details; the ranking itself is served.
- Handling travels with each record: the grantee receives `no-infer` (and `subject-initiated-only` where Spirituality is named) in `obligations.handling` and must keep them (C-4, C-6).
- A record that names `via-strengths/spirituality` is still reached by the lens selector. To keep it from a grantee, exclude it by id: `"exclude": [{"ids": ["as-1"]}]`. That withholds the whole ranking (section 6).

**What this grantee receives.** Run the projection the grantee would get:

```sh
python3 -B tools/ohc_query.py <your context directory> project --grant g-1 --purpose coaching --now latest
```

`--purpose` is one of the grant's `purposes`; `--now latest` evaluates at the newest time in the context. **For a real person's context** (no `synthetic`), also pass `--holder-key-file <file>`, a file holding the holder's secret key (K_holder, §12.3 step 11); without it the tool stops with "--holder-key-file is required: this context is not marked synthetic". For the worked example it serves `la-1`, `as-1`, `c-1` and `pr-1` under `statements`, `in-1` under `interpretations`, and `oc-1` under `recall`; not `ep-1` or `src-1`.

### Step 8. Check

```sh
python3 -B tools/check.py <your context directory> --level L1 --json
```

Expect `"valid": true` and `"levelMet": "L1"`, then run the projection command of step 7 for each grant. The checker does not verify everything this recipe asks for. Check these by hand:

- every construct id follows `via-strengths/<n>` with a published name, written as in step 3;
- a record that names `via-strengths/spirituality` carries the category `belief` and the handling `subject-initiated-only`;
- every Ground `kind` matches the cited record (step 4);
- no record holds item text, report prose, strength descriptions, scores against others or the classification list;
- no record was written by an agent through the lens beyond what the person's grant and adoption allow.

## 4. Never

- **Prohibited purposes.** Never use any record of this lens for `personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting` or any other prohibited purpose (§8.10), under any grant. A result grounds a choice you propose for the person only under `decisionUse: approval-required`, only when the person accepted it, naming what you weighed (R-G14). The publisher's own guidance also rules out selection and placement.
- **No comparisons between people.** A ranking is within one person. Never compare it with another person's ranking or a group, and never map it to another lens (`crossLensMapping: not-allowed`).
- **No agent inference unless the person allows it.** An agent never infers a person's strengths from behaviour or text on its own (`agentPosture`). An estimate (`mode: agent-inference`) or a reading through the lens exists only under the person's Grant (`suggest` and `infer` naming the lens; I5 for readings), as a person-only proposal (AR-2).
- **No weaknesses.** Never describe a low-ranked strength as a flaw, a deficit or something to fix.
- **Spirituality only when the person raises it.** Never comment on that strength unless the person brings it up; it can reveal religious or philosophical beliefs.
- **No reproduction of the classification.** Never store, list, regroup or rename the classification, and never quote the publisher's descriptions of strengths.
- **The VIA name only to name the publisher's instruments.** Use it nominatively, with the notice, and never so as to suggest that the publisher authored or endorses OHC or the person's records.

## 5. Worked example

[examples/via-strengths/context.json](examples/via-strengths/context.json) is a single-document context about Bento, who is fictional. It contains exactly the records of the main path of section 3: `la-1`, `src-1`, `as-1`, `c-1`, `ep-1`, `in-1`, `pr-1`, `oc-1` and `g-1`, with two Parties and the pinned descriptor. Bento's coach works with strengths; Bento took the survey, stores his five signature strengths, reads an evening at a repair cafe through them, tries a practice his coach suggested, and lets the coach read these records for their coaching.

```sh
python3 -B tools/check.py docs/lenses/examples/via-strengths --level L1 --json
```

It reports `"valid": true`, `"levelMet": "L1"`, no errors and no warnings. Its output equals [examples/via-strengths/expected-check.json](examples/via-strengths/expected-check.json).

The variants of section 3 are in two more contexts about the same fictional Bento. Each passes the same way (`"valid": true`, `"levelMet": "L1"`, no errors, no warnings):

| Variant | File | Records |
|---|---|---|
| coach's notes | [variants/coach-notes/context.json](examples/via-strengths/variants/coach-notes/context.json) | `src-2`, `la-1`, `src-3`, `c-2` |
| agent-suggested, self-identified, agent-offered practice | [variants/with-agent/context.json](examples/via-strengths/variants/with-agent/context.json) | `g-0`, `la-1`, `rv-1`, `as-2`, `c-1`, `pr-2`, `rv-2` |

```sh
python3 -B tools/check.py docs/lenses/examples/via-strengths/variants/coach-notes --level L1 --json
python3 -B tools/check.py docs/lenses/examples/via-strengths/variants/with-agent --level L1 --json
```

No report, release or notes file is shipped; with the file absent, the checker checks only the Source record (step 2).

## 6. What does not fit yet

These are gaps in OHC 0.1 for this lens. They are collected for the next pass of the standard.

1. **A partial ranking looks like a complete one.** A `ranking` result cannot say that it holds only the first N strengths of a longer order; the example has to say so in `note`. Proposal: an optional `complete` (boolean, default `true`) on `ranking` results.
2. **The id pattern is not exact, and construct ids are not checked.** "Words joined by hyphens" does not say what happens to signs such as `&`; this recipe drops them, but the checker accepts both `via-strengths/alpha-beta` and `via-strengths/alpha-&-beta` (placeholder names), and any other id, including ids with spaces and capitals (verified), so a wrong choice is never caught. Proposal: define the normalisation in the descriptor (lowercase; signs that are not letters or digits dropped; spaces become hyphens; repeated hyphens collapse) and add a checker rule that tests construct ids against `constructs` or `constructsByReference.idPattern`.
3. **The Spirituality rule applies to a whole record.** `perConstruct` raises one strength to `belief`, but categories and handling sit on the AssessmentRecord, so the whole ranking becomes `belief` and `subject-initiated-only`, and a grantee can be denied that one strength only by withholding the whole ranking. The checker does not test `perConstruct` (verified). Proposal: categories per result entry, a projection step that drops constructs whose categories the grant's selector does not name, and a checker rule for `perConstruct`.
4. **A reading cannot name the strengths it is about.** An Interpretation or a Practice through the lens has only free text, so "which strengths showed in my episodes" cannot be counted without parsing text. Proposal: an optional `constructs` list (construct ids of the cited lens) on Interpretation and Practice.
5. **A practitioner's reading through the lens cannot be stored.** *Resolved in 0.1.0-draft.2:* LA-7 is retired and I5 applies `agentInterpretation` to agent and software authors only; a coach's reading needs the coach in `interpretationAuthors` of the active adoption.
6. **Practitioner access is described inconsistently.** CONTEXT-08 says access "would need its own grant, which 0.1 does not provide for practitioners", yet a Grant to a person Party with role `practitioner` validates and is the only way to share with the coach (as in the example). Proposal: state in CONTEXT-08 that a practitioner Party may be a grantee under `coaching` or `therapy-support`, and that the adoption itself never gives access.
7. **`therapy-confidential` does not reach the results.** LA-4 propagates `special` and `person-only` only to records that cite the adoption; the person's own AssessmentRecord, Claim, Interpretation and Practice in the lens do not cite it (the AssessmentRecord has no field to do so), so a lens selector still serves them (verified with the projection tool). Proposal: apply LA-4 to every record whose `lens` or `source.lens` is the adopted lens while the adoption is `therapy-confidential`.
8. **The origin of what an agent writes on the person's behalf is not stated.** A Practice with `source.route: from-agent` and an agent-written `agent-suggested` adoption have no `text`, so `origin: declared` fails ENV-2; `observed` passes but is documented nowhere (verified). Proposal: state `origin: observed` for these records in §10.5, §17.1 and CONTEXT-08.
9. **The copyright of a stored report has no marker.** The publisher's report may sit in the person's vault, but nothing on the Source records that its text belongs to the publisher; only `maxRelease` keeps it from grantees, and the person can relax it. Proposal: an optional `rights` note on Source (`holder`, `use: "personal-copy"`), with a holder warning before any release above `index`.
10. **A LensAdoption gates nothing.** A context with lens results, lens readings and from-lens Practices but no LensAdoption passes L1; results pass when the adoption's `uses` lack `store-results`, and when they were recorded before the adoption; while an `agent-suggested` or `imported` adoption is still `proposed`, a lens selector already serves the person's results, readings and Practices in that lens (verified). `uses` has no normative effect; §10.5 gives `uses` no rule. Proposal: a rule LA-8: a record with `lens` or `source.lens` by a non-subject author requires an adoption of that lens that is active at its `recordedAt` and whose `uses` include the matching use (`store-results`, `interpret`, `offer-practices`); a warning for the subject's own lens records with no active adoption; and a projection that withholds lens records while the adoption is `proposed` or `paused`.
11. **An agent-offered Practice reaches grantees labelled "observed".** After the person's `admit`, a Practice with `source.route: from-agent` and an admitted `agent-suggested` adoption are served with the derived `label: observed` and `endorsement: not-asked` (verified with the projection tool). The grantee sees the agent's suggestion presented as an observation about the person, and cannot see that the person admitted it. Proposal: derive `label: suggested` for these records, and `endorsement: admitted` once a subject `admit` Review exists; or add an origin `suggested` instead of reusing `observed`.
12. **Ground `kind` is not tied to the cited record.** A Claim can cite a self-identified ranking with `kind: instrument`; the checker accepts any Ground kind for any target, and an earlier version of this recipe gave `instrument` for every case. A grantee then reads a self-chosen ranking as survey evidence. Proposal: when a Ground's `ref` is an AssessmentRecord, `kind` matches its `mode` (`self-identified` → `subject-statement`; practitioner modes → `practitioner`; instrument modes → `instrument`), or the projection derives the kind from the mode.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
