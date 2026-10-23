# Lens recipe: astrology

**Recipe · lens `urn:ohc:lens:astrology` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe turns a person's astrology (their birth data, a computed chart and the way they use its language) into OHC records that keep the frame as the person's chosen language and never let it become a fact about them, a prediction or an input to anyone's inference.

The lens descriptor is [spec/lenses/astrology.lens.json](../../spec/lenses/astrology.lens.json); the record shapes are in [SPECIFICATION.md §10.5–§10.6](../../spec/SPECIFICATION.md#105-lensadoption) and the schemas in [spec/schema/](../../spec/schema/). The general adoption procedure is [CONTEXT-08](../agents/procedures/CONTEXT-08.md).

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them. Results of this frame, and anything read from them, stay `frame-relative` and are never presented as an empirical fact or a prediction (AR-4, C-7).

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:astrology-basic`](../../spec/playbooks/astrology-basic.playbook.json) (Astrology as a self-description frame: basic ways of working, by the OHC editors), for these situations: looking back at something that happened; choosing between options; preparing a hard conversation. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

**Bringing a report through the person's window.** When an instrument's catalog entry carries an `import` block, a person can bring its result through their own window ([guide](../guides/BRING-A-RESULT.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). No entry of this lens has one yet, so the steps below record the report by hand.

## 1. What you may have

| Input | What it is | Where it goes |
|---|---|---|
| Self-description in conversation | "My Sun is in Pisces", "my Moon is in Taurus" | A LensAdoption (step 1) and the person's own Claims (step 5). Without a chart: a self-identified result (step 4, variant). |
| Birth data | Date, time and place of birth | One `fact` Claim with category `birth-data` (step 2). |
| A chart the person computed with software | An export or printout of placements and aspects | A Source in the vault (step 3) and one AssessmentRecord with `frame-attributes` (step 4). |
| A chart export loaded by an importer | The same, read by a tool | Route `imported` (§2): the adoption and the result stay proposed until the person confirms them with Reviews. |
| Notes from a consultation with an astrologer | The astrologer's reading of the chart | A Source, authored by the astrologer's Party (`role: "practitioner"`, step 3). The person writes their own reading in their own words (step 6). Since 0.1.0-draft.2 the astrologer's reading can also be a lens reading, under an `inherited-from-practice` adoption that lists the astrologer in `interpretationAuthors` (I5); the example does not do this. |
| An agent's reading | — | **Only under the person's Grant.** An agent suggests the frame, or reads through it, only when the person's agreement lets it (`suggest`, `infer` naming the lens) and their active adoption is not `off` (I5). Whatever it reads stays `frame-relative` and is said in the frame's language, never as a fact or a prediction (AR-4, C-7). |

## 2. Before you start


**Routes of adoption.**

| Route | Allowed | What it changes |
|---|---|---|
| `self-chosen` | yes | The person writes the adoption with `assertedBy: "subject"`; it is active at once. The worked example uses this route. |
| `imported` | yes | An importer creates the adoption and the chart result from an export, both with the same `importedFrom.run`. Both are `proposed` until the person confirms them with a Review (LA-5). The Human Design recipe shows this route in full. |
| `agent-suggested` | only under the person's Grant | Listed, usually when the person brought up the frame themselves; routes describe usual practice and restrict nothing. An agent suggests the frame only under a Grant with `suggest` naming the lens, and the adoption stays proposed until the person admits it (LA-1). |
| `inherited-from-practice` | yes | Listed (role `other`). A consultation with an astrologer can be inherited with a `practice` block; the astrologer's readings need them in `interpretationAuthors` (I5). Custody has no code for a consultation (§6). |

**Consent.** Recording needs no grant: the person writes into their own context, and with no grant nothing is disclosed to anyone (L0). To share, the person writes a Grant (step 8). Records that cite this lens are `special`, so the grant needs `basis.legal: "explicit-consent"` and an expiry within 180 days (R-G3, R-G10). `la-01`, `as-01` and `in-01` are frame-relative: only a selector that names the lens reaches them; ids alone never do (§12.3 step 8). An `ids` selector works only for the Episode and plain Claims.

**Defaults for this lens.**

- Records that cite the lens (LensAdoption, AssessmentRecord, Interpretation): `sensitivity: "special"`, `categories: ["birth-data"]`.
- The birth-data Claim: category `birth-data` (tier at least `sensitive`). Recommended: `handling: ["person-only"]`.
- The AssessmentRecord: `epistemic: "frame-relative"`. Recommended: `handling: ["no-infer", "no-quote-back"]`, if the person wants the chart kept from every inference.
- Every Claim derived from the chart: `epistemic: "frame-relative"`, set by hand (step 5a). The checker does not catch its absence.
- `agentInterpretation` is `"off"`, the default the person keeps here; `interpretationAuthors` stays `["subject"]`. The person may change either (I5).
- The lens's `reviewAfter` is `on-change`. A birth chart does not change, so leave `reviewAfter` off the AssessmentRecord.

**What is never stored.**

- Report prose: the interpretive text from chart software, a website, a book or an astrologer. It stays in the vault (step 3) or is not kept. Records hold only placements, aspects and the person's own words.
- Degrees, minutes, angles and cusps, unless the person asks for them. Together with the place, they let anyone reconstruct the date and time of birth. Store signs (and numbered houses only if the person wants them).
- Another person's chart or birth data: compatibility, synastry, a partner's or a child's chart. No record describes a third party (TP-1).
- Forecasts (transits or progressions read as predictions) as Claims or results.
- Labels carried across lenses in either direction, for example a type or a trait "from your chart", or a sign "from your test".
- Scores, rankings or judgements of the person. Frame attributes are never traits.

## 3. Steps

All records below are written by the person, or by an agent at the person's dictation as the person (`assertedBy: "subject"`). Each snippet is a record from the [worked example](examples/astrology/context.json) and validates against the schema, unless it is marked as a variant (variants were checked separately and also pass L1).

### Step 0. Prepare the context file

Make a folder for the context. Save the file as `<folder>/context.json`, put vault files under `<folder>/vault/`, and pass `<folder>` (not the file) to `check.py`. Start from this skeleton; the steps below fill its arrays.

```json
{
  "format": "ohc.context",
  "specVersion": "0.1.0-draft",
  "id": "urn:uuid:<new random UUID>",
  "version": "1",
  "subject": {"id": "urn:uuid:<another new random UUID>", "displayName": "<what the person wants to be called>"},
  "holder": "subject",
  "lang": "en",
  "created": "2026-09-03T18:30:00Z",
  "policy": {"admission": "subject-only", "resolver": "returnDialog"},
  "conformance": {},
  "parties": [],
  "lenses": [],
  "lensAdoptions": [], "claims": [], "sources": [], "assessments": [], "episodes": [],
  "interpretations": [], "grants": []
}
```

- The schema requires `format`, `specVersion`, `id`, `version` and `subject.id`. `holder`, `lang` and `policy` above are the defaults written out. Change `version` with every change set.
- **A fictional person only:** add `"synthetic": true` at the root **and** on every content record. A context about a real person never carries it. The checker enforces both flags only for a folder under an `examples/` directory or an `id` that starts with `urn:ohc:example:` (the worked example uses `urn:ohc:example:imre:astrology`). `tools/ohc_query.py` (step 8) projects without a holder key only when the root flag is set.
- Add `"reviews": []` for the imported route, and `"practices": []` if you do step 7.

Then fill `conformance`, `parties` and `lenses`. Declare the modules, list every Party you will reference (the chart software and any agent the person will later share with; labels are generic roles, never names), and pin the descriptor (the `sha256` is the SHA-256 of the descriptor file's bytes: `shasum -a 256 spec/lenses/astrology.lens.json`).

```json
"conformance": {"level": "L1", "modules": ["core", "governance", "lenses"], "subjectIsAdult": true},
"parties": [
  {"id": "s-01", "partyKind": "software", "label": "Chart software"},
  {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"},
  {"id": "a-02", "partyKind": "agent", "label": "Work assistant"}
],
"lenses": [
  {"id": "urn:ohc:lens:astrology", "version": "0.2.0", "sha256": "5ebefc64c34aa0c6a977e271b4c80d7bb8ade6a5c1d1e53a90cdb89e43e09e74"}
]
```

### Step 1. Record the person's relation to the lens: LensAdoption

The person says they use astrology to describe their experience. Write one LensAdoption. Choose `uses` with the person: `speak-in-lens` (an agent may use the frame's words after adoption), `store-results` (a chart may be kept), `interpret` (the person may read episodes through it).

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:astrology", "version": "0.2.0"}, "route": "self-chosen",
 "uses": ["speak-in-lens", "store-results", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "representationPreference": "astrology.chart",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-03T18:45:00Z",
 "sensitivity": "special", "categories": ["birth-data"], "synthetic": true}
```

Who sees it by default: only the person. Tier `special`, label ◇ frame. It is frame-relative: a grant reaches it only through a selector that names the lens, under explicit consent; a selector with its id alone never does.

### Step 2. Record the birth data: Claim

The chart is computed from it, so it is recorded once, in the person's words, at the precision the person chooses (a city is enough; never a street address).

```json
{"id": "c-01", "facet": "fact", "predicate": "birth-data",
 "text": "Born 14 March 1991 at about 06:40 local time in Porto.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-03T18:50:00Z", "horizon": "foundation",
 "sensitivity": "sensitive", "categories": ["birth-data"], "handling": ["person-only"], "synthetic": true}
```

Who sees it: only the person, always. `person-only` is never served to any grantee, whatever a grant says. Never put birth data in an id, a title or a note.

### Step 3. Keep the original chart: Source

The chart export (or a scan of a printout) goes into the vault. Compute the values; do not copy them from the example:

1. `sha256` = the output of `shasum -a 256 <file>` (or `sha256sum <file>`);
2. `size` = the byte count, `wc -c < <file>`;
3. move the file to `<folder>/vault/<first two hex characters of sha256>/<sha256>.<ext>` and write that path, relative to the folder, as `vaultPath`.

The L1 check does not read the vault (`"vaultContentRead": false`): a wrong hash or size still passes, so compute them. The Source record holds only metadata.

```json
{"id": "src-01", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/03/03b169fc93949c19bd13ceb6b0c931d850b13a17cc4f91b57a6cf66d74074162.json"},
             "sha256": "03b169fc93949c19bd13ceb6b0c931d850b13a17cc4f91b57a6cf66d74074162",
             "mediaType": "application/json", "size": 172},
 "capturedAt": "2026-09-03T18:55:00Z", "authorship": {"author": "s-01"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index",
 "summary": {"text": "Chart export saved from my chart software.", "authoredBy": "subject",
             "recordedAt": "2026-09-03T19:00:00Z", "method": "subject-written"},
 "retention": {"eraseOnRequest": true},
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-03T19:00:00Z",
 "sensitivity": "special", "categories": ["birth-data"], "synthetic": true}
```

- `custody` is omitted: the person owns the file.
- `summary.text` is the person's own one-line description, never copied report text.
- **An astrologer's written notes** (variant): add the astrologer to `parties` as `{"id": "p-01", "partyKind": "person", "label": "Consulting astrologer", "role": "practitioner"}` (the role is `practitioner`, the label a generic role, never a name). Store the notes as a Source with `sourceKind: "practitioner-notes"` (special by default), `authorship.author: "p-01"`, `inbound: true` and `maxRelease: "index"`, with no `summary`.

Who sees it: only the person (the subject always has every tier). `maxRelease: "index"` means no grantee ever gets more than the kind, media type and a coarse date.

### Step 4. Record the chart: AssessmentRecord

One AssessmentRecord with one `frame-attributes` result. Rules: `mode: "computed-from-birth-data"` requires `origin: "derived"` (AR-1), which requires `generatedBy.method` and `derivedFrom`. `computedFrom` names the birth-data Claim; `engine` names the software and version. Keys of `attributes` are the lens's construct ids (`astrology/placement`, `astrology/aspect`); values are signs only, without degrees. `lensVariant` is `western-tropical` or `vedic-sidereal`. There is no `instrument` (the lens lists none) and no `trademarkNotice` (the lens lists no marks). The checker checks none of the attribute keys, values or `computedFrom` (§6), so follow these rules yourself.

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:astrology", "version": "0.2.0"}, "lensVariant": "western-tropical",
 "mode": "computed-from-birth-data", "administeredAt": {"start": "2026-09-03", "precision": "day"},
 "results": [
   {"type": "frame-attributes",
    "attributes": {
      "astrology/placement": [
        {"point": "sun", "sign": "pisces"},
        {"point": "moon", "sign": "taurus"},
        {"point": "ascendant", "sign": "pisces"}],
      "astrology/aspect": [
        {"points": ["sun", "saturn"], "aspect": "sextile"}]},
    "computedFrom": "c-01",
    "engine": {"name": "example-chart-engine", "version": "3.2"}}],
 "source": "src-01",
 "origin": "derived",
 "generatedBy": {"software": "example-chart-engine", "version": "3.2", "method": "western tropical zodiac; signs only, no degrees and no houses"},
 "derivedFrom": ["c-01"], "assertedBy": "subject", "recordedAt": "2026-09-03T19:10:00Z",
 "epistemic": "frame-relative", "sensitivity": "special", "categories": ["birth-data"],
 "handling": ["no-infer", "no-quote-back"], "synthetic": true}
```

**Variant without a chart** (not in the worked example). If the person only knows a placement ("my Sun is in Pisces"), write the whole record like this:

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:astrology", "version": "0.2.0"}, "lensVariant": "western-tropical",
 "mode": "self-identified", "administeredAt": {"start": "2026-09-03", "precision": "day"},
 "results": [{"type": "type-assignment", "construct": "astrology/placement", "label": "Sun in Pisces", "method": "self-identified"}],
 "validityFlags": ["self-identified-only"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-03T19:10:00Z",
 "epistemic": "frame-relative", "sensitivity": "special", "categories": ["birth-data"],
 "handling": ["no-infer", "no-quote-back"], "synthetic": true}
```

- Keep `lensVariant` only if the person knows it.
- No `generatedBy`, `derivedFrom`, `computedFrom` or `engine`: nothing was computed. The checker accepts `generatedBy` and `derivedFrom` on a declared record (§6), but they would claim a computation that did not happen.
- No `source`, unless a Source exists (for example, a photo of the person's handwritten note).
- Skip step 3. Step 2 is needed only if the person wants the birth data recorded.

Who sees it: only the person. Tier `special`, label ◇ frame. Served only to a grant whose selector names the lens (§12.3 step 8 requires that for every frame-relative record).

### Step 5. Keep only what the person accepts: Claims

Show the person the result. Write a Claim only for what the person says they recognise, in their words. Two kinds:

**5a. A self-description in the frame's language.** `facet: "identity"`, `predicate: "self-description"`, `epistemic: "frame-relative"`, `derivedFrom` the chart. Never `facet: "disposition"`: this lens does not establish any trait (CL-3 and the descriptor's `doesNotEstablish`).

**You MUST set `epistemic: "frame-relative"` on every Claim derived from `as-01`.** The checker does not catch its absence. Without it, the Claim is computed as `as-reported`, labelled ✓ stated, and a grant that names its id serves it as a plain stated fact. Check it before step 8.

```json
{"id": "c-02", "facet": "identity", "predicate": "self-description",
 "text": "In my chart's language I am a Pisces Sun with a Taurus Moon: I do my best thinking alone, before the day starts.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-05T20:00:00Z", "horizon": "foundation",
 "derivedFrom": ["as-01"], "epistemic": "frame-relative", "handling": ["no-quote-back", "no-infer"],
 "synthetic": true}
```

Who sees it: only the person. Its tier is `special` by propagation from the chart. In OHC 0.1 no grant can serve it, not even one that names its id, because a Claim cannot name a lens (§6).

**5b. The same insight in plain words, if the person wants agents to act on it.** Ask: "Is there something here you want others to take into account, in your own plain words?" Write it as an ordinary Claim, with no frame words and **no** `derivedFrom`: it stands on the person's word, not on the chart.

```json
{"id": "c-03", "facet": "preference", "predicate": "timing",
 "text": "Keep my mornings for focused work; put meetings after 11:00.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-05T20:05:00Z", "horizon": "foundation",
 "contexts": ["work"], "synthetic": true}
```

Who sees it: only the person until a grant names it. Tier `personal`, label ✓ stated. Any grant whose selector matches `facet: "preference"` reaches it.

### Step 6. Read an episode through the lens, in the person's words: Episode and Interpretation

The person tells what happened (Episode). If they want, they read it through their chart (Interpretation with `lens` and `stance: "lens-reading"`). Only the person writes this reading. Add at least one alternative that is not psychological, so the frame never stands alone.

```json
{"id": "ep-01", "occurred": {"start": "2026-09-08", "end": "2026-09-19", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-20T21:00:00Z", "addedAt": "2026-09-20T21:00:00Z",
    "accountKind": "first-narrative",
    "happened": "For two weeks the translation stalled; I rewrote the opening of the same chapter five times.",
    "didOrTried": "Moved my desk to the window and started working at night.",
    "understandingThen": "I thought the text was simply hard."}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T21:00:00Z",
 "sensitivity": "sensitive", "contexts": ["work"], "synthetic": true}
```

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:astrology", "version": "0.2.0"},
 "text": "Read through my chart, those weeks were my Pisces Sun asking for more solitude than the shared office gave me.",
 "grounds": [{"ref": "as-01", "kind": "instrument"}],
 "alternatives": [
   {"text": "The publisher changed the style guide in the middle of the job.", "kind": "external"},
   {"text": "I was sleeping badly after the move.", "kind": "physiological"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-27T09:00:00Z",
 "epistemic": "frame-relative", "sensitivity": "special", "categories": ["birth-data"],
 "handling": ["no-quote-back"], "contexts": ["work"], "synthetic": true}
```

Who sees them: only the person. The Episode is `sensitive` (a grant must name its id, kind or facet); the reading is `special` and frame-relative (a grant must name the lens).

### Step 7. Practices from the toolkit

None for an agent to run. The toolkit has one item, `astrology.chart` (computing the chart), which is step 4; an agent may offer it (`agentMayOffer: true`) when the person's agreement lets it suggest the frame.

If the person has their own practice, record it as a Practice with `source.route: "self-discovered"` and no `templateId` (variant, not in the worked example). First add `"practices"` to `conformance.modules` and `"practices": []` to the file; without the module the check fails with CX-5. `practiceKind` is one of `breathing`, `movement`, `reflection`, `writing`, `conversation`, `rest`, `planning`, `environment`, `social-contact`, `creative`, `contemplative`, `other`.

```json
{"id": "pr-01", "name": "Evening notes", "description": "A few lines before sleep about what the day asked of me.",
 "practiceKind": "writing", "source": {"route": "self-discovered"}, "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-06T21:00:00Z", "synthetic": true}
```

### Step 8. Decide who may see what: Grant

Two typical grants. The reflection companion may read the frame records and the episode, to talk with the person in their chosen language. It gets no `suggest` and no `infer`: it writes nothing through this lens. The work assistant sees only plain preferences.

```json
{"id": "g-01", "recordedAt": "2026-09-06T10:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:astrology"]}, {"ids": ["ep-01"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-06T10:00:00Z", "channel": "holder-ui"},
 "note": "Chart language for my own reflection only; no advice, no predictions."}
```

```json
{"id": "g-02", "recordedAt": "2026-09-06T10:05:00Z", "grantor": "subject", "grantee": "a-02",
 "purposes": ["scheduling"],
 "scope": {"include": [{"facets": ["preference"], "contexts": ["work"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "none",
 "constraints": {"expiresAt": "2027-09-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-06T10:05:00Z", "channel": "holder-ui"}}
```

What each grantee receives under §12.3, computed with the reference tools on the worked example:

| Grantee | Served | Never served |
|---|---|---|
| `a-01` Reflection companion | `la-01`, `as-01`, `in-01`, `ep-01` | `c-01` (person-only), `c-02` (frame-relative Claim, §6), `c-03` (not in scope), `src-01` (`maxSourceTier: none`) |
| `a-02` Work assistant | `c-03` | everything that cites the lens |

To compute this table for your own context, run, for each grant:

```sh
python3 -B tools/ohc_query.py <folder>/context.json project --grant g-01 --purpose self-reflection --now 2026-10-10T12:00:00Z
python3 -B tools/ohc_query.py <folder>/context.json project --grant g-02 --purpose scheduling --now 2026-10-10T12:00:00Z
```

Served records appear under `statements`, `experience`, `interpretations` and `recall`; the Parties they point to appear under `parties`. A context without the root `"synthetic": true` needs `--holder-key-file`.

`expiresAt` is at most 180 days after `recordedAt` for g-01 (it reaches special records) and at most one year for g-02. A grant with only `{"ids": ["la-01", "as-01", "in-01"]}` serves none of them, even with explicit consent: name the lens. Never add `infer`, `write` or a wildcard selector for this lens.

### Step 9. Check

```sh
python3 -B tools/check.py <folder> --level L1 --json
```

Expect `"valid": true` and `"levelMet": "L1"`. A folder under an `examples/` directory is compared with its `expected-check.json` (X-3); a context of your own is not. A passing check does not cover what §2 and step 5a say the checker does not catch: `epistemic` on derived Claims, the attribute keys and precision, `computedFrom`, and the vault hashes.

## 4. Never

- Never bring the frame up or compute a chart unless the person's agreement lets you (`suggest` naming the lens), and then only as one option.
- Never read through the lens as an agent beyond the person's Grant and adoption (I5). An estimate is person-only (AR-2), and a reading or estimate in a symbolic frame is `frame-relative` (AR-4).
- Never present a chart attribute, or anything read from it, as an empirical trait or a prediction (C-7); never map chart attributes to any trait, type or score (LN-3, mapping `no-relation`).
- Never use anything from this lens for the prohibited purposes (`personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting` and the rest of §8.10), under any grant. That includes team composition, hiring "fit" and compatibility with colleagues or partners. A chart attribute grounds a choice you propose for the person only under `decisionUse: approval-required`, only when the person accepted it, named as the frame's language, never as a fact (R-G14, C-7).
- Speak in the frame in the person's own words. Never quote the chart back as proof ("according to your chart you are…"): `no-quote-back`.
- Never predict, and never present a frame attribute as a fact about the person.
- Never compute, store or discuss another person's chart (TP-1).
- Never serve the birth-data Claim; never put birth data in ids, titles or notes (R-I1).
- The descriptor lists no trademarks. Name chart software only as provenance (`engine`, `generatedBy`), never as a label for a result.

## 5. Worked example

[examples/astrology/context.json](examples/astrology/context.json): Imre, a fictional translator. It contains exactly the records of section 3 (without the variants): `la-01`, `c-01`, `src-01`, `as-01`, `c-02`, `c-03`, `ep-01`, `in-01`, `g-01`, `g-02`, with the vault placeholder for `src-01`. The context root and every content record carry `"synthetic": true`.

```sh
python3 -B tools/check.py docs/lenses/examples/astrology --level L1 --json
```

Result: `"valid": true`, `"levelMet": "L1"`, no errors, no warnings ([expected-check.json](examples/astrology/expected-check.json)).

## 6. What does not fit yet

1. **A frame-relative Claim can never be shared.** A Claim has no `lens` field, and §12.3 step 8 serves a frame-relative record only through a selector that names its lens. Step 5a's Claim is unservable even when a grant names its id. Proposal: allow `lens` on a Claim whose epistemic status is `frame-relative`, or let step 8 accept an `ids` selector.
2. **No link that records "this came up while I looked at my chart" without making the chart evidence.** `derivedFrom` and `evidence` make the frame a ground and propagate `special` to the plain Claim (step 5b). Proposal: a Relation code such as `prompted-by`: not evidence, no tier propagation, never an inference path.
3. **An astrologer's reading has no place.** *Resolved in 0.1.0-draft.2,* except custody: routes restrict nothing (LN-3 now only forbids cross-lens mapping), and I5 applies `agentInterpretation` to agent and software authors only, so an astrologer listed in `interpretationAuthors` of an inherited adoption may author a reading. Custody still has no confidentiality code for a consultation. Proposal: add a custody code such as `consultation`.
4. **`frame-attributes.attributes` is an unstructured object.** Nothing ties its keys to construct ids, and nothing limits precision (degrees reveal birth time): degree values and non-construct keys pass L1. Proposal: `attributes: [{"construct", "value"}]` with constructs from the descriptor, plus a descriptor field that lists attributes never to store.
5. **No self-identified shape for a frame attribute.** `frame-attributes` requires `computedFrom` and `engine`; a person who only knows a placement must borrow `type-assignment`. Proposal: make both optional when `mode` is `self-identified`.
6. **`computedFrom` is not checked.** It is not in the reference-targets catalog, and nothing verifies that it names a birth-data Claim; a dangling `computedFrom` passes. Proposal: add it to the catalog and a rule that it resolves to a Claim with `facet: "fact"` and `predicate: "birth-data"`.
7. **Lens defaults cannot set handling.** `no-infer` and `no-quote-back` fit every record of this lens but must be added by hand. Proposal: `defaults.handling` in the descriptor.
8. **`on-change` cannot be written on a record.** AssessmentRecord `reviewAfter` accepts only a duration, and §7.2 does not say how `on-change` computes freshness. Proposal: allow `on-change` and define it (current until superseded or marked not current).
9. **The adoption route is not checked against the descriptor.** *Closed in 0.1.0-draft.2 as intended:* `adoption.routes` describes usual practice and never restricts a LensAdoption.
10. **The frame-relative status does not pass along `derivedFrom`.** A Claim derived from a frame-relative AssessmentRecord, written without `epistemic`, is computed `as-reported` and labelled ✓ stated; a grant that names its id (tested with the scheduling assistant under explicit consent) then serves it. Chart language leaves as a plain stated fact, and no rule or warning fires. Proposal: make `frame-relative` pass along `derivedFrom` and `grounds` the way the tier does, or add a rule (error at L1): a record whose `derivedFrom` or `grounds` include a frame-relative record MUST be `frame-relative`.
11. **A declared record may carry `generatedBy` and `derivedFrom`.** A self-identified AssessmentRecord (`origin: "declared"`) that keeps `generatedBy` and `derivedFrom: ["c-01"]` passes. Its provenance then claims a software computation, while the record says the person stated it. Proposal: an envelope rule that `generatedBy` is allowed only with `origin` `derived` or `inferred`; a link from a declared record to what prompted it uses `evidence` or the proposed Relation `prompted-by` (item 2), not `derivedFrom`.
12. **The root `synthetic` flag is not tied to the records' flags.** Outside example mode (a folder not under `examples/`, an id not starting with `urn:ohc:example:`), every content record can be synthetic while the root is not; the checker accepts it, and `ohc_query.py` then demands a holder key. Proposal: warn at L1 when all content records are synthetic but the root is not, and the reverse; or derive the root flag from the records.
13. **The vault is not compared with the Source at L1.** A wrong `sha256` or `size` passes (`"vaultContentRead": false`). Proposal: an opt-in check flag (or L1 when the vault is local) that hashes vault files and compares `sha256` and `size`: an error on mismatch, a warning when the file is absent.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
