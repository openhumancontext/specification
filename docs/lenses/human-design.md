# Lens recipe: Human Design

**Recipe · lens `urn:ohc:lens:human-design` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe brings a person's Human Design chart, usually exported from an app, into OHC as frame-relative records that the person admits and reads in their own words, and that no one may use to infer anything about them or to decide for them.

The lens descriptor is [spec/lenses/human-design.lens.json](../../spec/lenses/human-design.lens.json); the record shapes are in [SPECIFICATION.md §10.5–§10.6](../../spec/SPECIFICATION.md#105-lensadoption) and the schemas in [spec/schema/](../../spec/schema/). The general adoption procedure is [CONTEXT-08](../agents/procedures/CONTEXT-08.md). Use the generic name "Human Design" only (§4).

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them. Results of this frame, and anything read from them, stay `frame-relative` and are never presented as an empirical fact or a prediction (AR-4, C-7).

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:human-design-basic`](../../spec/playbooks/human-design-basic.playbook.json) (Human Design as a self-description frame: basic ways of working, by the OHC editors), for these situations: looking back at something that happened; choosing between options; preparing a hard conversation. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

**Bringing a report through the person's window.** When an instrument's catalog entry carries an `import` block, a person can bring its result through their own window ([guide](../guides/BRING-A-RESULT.md), [CONTEXT-10](../agents/procedures/CONTEXT-10.md)). No entry of this lens has one yet, so the steps below record the report by hand.

## 1. What you may have

| Input | What it is | Where it goes |
|---|---|---|
| A chart exported from an app | A file with type, authority, profile and centres, computed from birth data | Route `imported`: an import run (step 1), a Source (step 2), the birth-data Claim (step 3), a LensAdoption (step 4) and an AssessmentRecord (step 5), all of which the person then reviews (step 6). The worked example uses this route. |
| Self-description in conversation | "I am a Projector", "my authority is splenic" | Route `self-chosen` (§2). Without a chart: a self-identified result (step 5, variant). The person's own Claims (step 7). |
| Birth data | Date, time and place of birth | One `fact` Claim with category `birth-data` (step 3). |
| Notes from a reading with an analyst | A practitioner's reading of the chart | A Source, authored by the analyst's Party (`role: "practitioner"`, step 2). The person writes their own reading (step 8). Since 0.1.0-draft.2 the analyst's reading can also be a lens reading, under an `inherited-from-practice` adoption that lists the analyst in `interpretationAuthors` (I5); the example does not do this. |
| An agent's reading | — | **Only under the person's Grant.** An agent suggests the frame, or reads through it, only when the person's agreement lets it (`suggest`, `infer` naming the lens) and their active adoption is not `off` (I5). Whatever it reads stays `frame-relative` and is said in the frame's language, never as a fact or a prediction (AR-4, C-7). |

## 2. Before you start

**What this lens is in OHC.** A symbolic frame: `kind: self-description-frame`, `measurementTier: T5`, `ontologicalStatus: symbolic-frame`. Every result, and anything read from it, is `frame-relative` and never presented as an empirical fact (AR-4, C-7), with `no-relation` to any empirical construct (mapping `urn:ohc:mapping:human-design--any`, `not-permitted`). The descriptor cites no empirical study; its citations concern intellectual property only (Court of Florence 2020 **[F2]**; two USPTO records, read).

**Routes of adoption.**

| Route | Allowed | What it changes |
|---|---|---|
| `imported` | yes | An importer creates the records from an export in one run. All carry `importedFrom` with the same `run` (an Event id). The LensAdoption and the AssessmentRecord are `proposed` until the person confirms them with Reviews (LA-5). Used in the worked example. |
| `self-chosen` | yes | The person writes the records; the adoption is active at once. Change the worked example like this: **no** `events` and **no** `reviews` (skip steps 1 and 6). `la-01`: `"route": "self-chosen"`, `"origin": "declared"`, and no `generatedBy`, `derivedFrom` or `importedFrom`. `as-01`: no `importedFrom` and no `formulatedAt`; it stays `origin: "derived"` (AR-1), and its `generatedBy` names the software that computed the chart (for example `{"software": "example-chart-app", "version": "5.1", "method": "computed by the chart app from the birth data; type, authority, profile and defined centres copied from its export"}`). `c-01` and `src-01`: `"origin": "declared"`, and no `importedFrom` or `formulatedAt`. |
| `agent-suggested` | only under the person's Grant | Listed, usually when the person brought up the frame themselves; routes describe usual practice and restrict nothing. An agent suggests the frame only under a Grant with `suggest` naming the lens, and the adoption stays proposed until the person admits it (LA-1). |
| `inherited-from-practice` | yes | Listed (role `other`). A reading with an analyst can be inherited with a `practice` block; the analyst's readings need the analyst in `interpretationAuthors` (I5). |

**Consent.** Recording needs no grant; with no grant nothing is disclosed. Records that cite the lens are `special`: sharing them needs a Grant with `basis.legal: "explicit-consent"` and an expiry within 180 days (R-G3, R-G10). `la-01`, `as-01` and `in-01` are frame-relative: only a selector that names the lens reaches them; ids alone never do (§12.3 step 8). An `ids` selector works only for the Episode and plain Claims.

**Defaults for this lens.**

- Records that cite the lens: `sensitivity: "special"`, `categories: ["birth-data"]`.
- The birth-data Claim: category `birth-data`; recommended `handling: ["person-only"]`.
- The AssessmentRecord: `epistemic: "frame-relative"`; recommended `handling: ["no-infer", "no-quote-back"]`, if the person wants the chart kept from every inference.
- Every Claim derived from the chart: `epistemic: "frame-relative"`, set by hand (step 7a). The checker does not catch its absence.
- `agentInterpretation` is `"off"`, the default the person keeps here; `interpretationAuthors` stays `["subject"]`. The person may change either (I5).
- The lens's `reviewAfter` is `on-change`; leave `reviewAfter` off the AssessmentRecord.

**What is never stored.**

- The app's or a book's descriptions of types, authorities, profiles or centres (report prose). The export stays in the vault; records hold only the attribute values and the person's own words.
- The registered composite mark or the abandoned one listed in the descriptor's `ip.marks`, anywhere: not in labels, names, notes or `engine` fields.
- Gate, channel and planetary positions with degrees, unless the person asks for them: they let anyone reconstruct the birth time.
- Another person's chart, or a chart that combines people (a couple, a family, a team). No record describes a third party (TP-1).
- Labels carried across lenses in either direction (a Human Design type "from your Big Five", a Big Five trait "from your type").
- Instructions about what the person should decide. "Strategy" and "authority" stay frame attributes, never rules for others to apply.

## 3. Steps

The person runs the importer (or an agent runs it for the person, writing as the person, `assertedBy: "subject"`). Each snippet is a record from the [worked example](examples/human-design/context.json) and validates against the schema, unless it is marked as a variant (variants were checked separately and also pass L1).

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
  "created": "2026-09-09T20:30:00Z",
  "policy": {"admission": "subject-only", "resolver": "returnDialog"},
  "conformance": {},
  "parties": [],
  "lenses": [],
  "events": [], "sources": [], "claims": [], "lensAdoptions": [], "assessments": [], "reviews": [],
  "episodes": [], "interpretations": [], "grants": []
}
```

- The schema requires `format`, `specVersion`, `id`, `version` and `subject.id`. `holder`, `lang` and `policy` above are the defaults written out. Change `version` with every change set.
- **A fictional person only:** add `"synthetic": true` at the root **and** on every content record. A context about a real person never carries it. The checker enforces both flags only for a folder under an `examples/` directory or an `id` that starts with `urn:ohc:example:` (the worked example uses `urn:ohc:example:wren:human-design`). `tools/ohc_query.py` (step 10) projects without a holder key only when the root flag is set.
- For the self-chosen route leave out `events` and `reviews`. Add `"practices": []` if you do step 9.

Then fill `conformance`, `parties` and `lenses`. Declare the modules (an Event and a Review belong to `governance`), list every Party you will reference (the chart app as `software` with a generic label, and any agent the person will share with), and pin the descriptor (the `sha256` is the SHA-256 of the descriptor file's bytes: `shasum -a 256 spec/lenses/human-design.lens.json`).

```json
"conformance": {"level": "L1", "modules": ["core", "governance", "lenses"], "subjectIsAdult": true},
"parties": [
  {"id": "s-01", "partyKind": "software", "label": "Chart app"},
  {"id": "a-01", "partyKind": "agent", "label": "Reflection companion"},
  {"id": "a-02", "partyKind": "agent", "label": "Personal assistant"}
],
"lenses": [
  {"id": "urn:ohc:lens:human-design", "version": "0.2.0", "sha256": "8348d08e660ee9a92c8d31d6400f92a80f5b1fe491d299b9101c2cd9fb819d6e"}
]
```

### Step 1. Log the import run: Event

One Event of type `import-run` names every record the run created. Its `id` is the `run` in each record's `importedFrom`. In a single file with one Event, `seq` is 1 and `prev` is `sha256:` followed by 64 zeros; `salt` is at least 16 random bytes in base64url. The checker does not compare `records` with the records that carry this `run` (§6): list exactly the records whose `importedFrom.run` is `e-01`, no more and no fewer.

```json
{"id": "e-01", "seq": 1, "at": "2026-09-12T19:00:00Z", "eventType": "import-run", "actor": "subject",
 "records": ["src-01", "c-01", "la-01", "as-01"], "salt": "kGllOqi3Niw8joCgjhcr3A",
 "prev": "sha256:0000000000000000000000000000000000000000000000000000000000000000"}
```

Who sees it: Events hold ids and codes only. They are the person's audit trail.

### Step 2. Keep the export: Source

The export file goes into the vault. Compute the values; do not copy them from the example:

1. `sha256` = the output of `shasum -a 256 <file>` (or `sha256sum <file>`);
2. `size` = the byte count, `wc -c < <file>`;
3. move the file to `<folder>/vault/<first two hex characters of sha256>/<sha256>.<ext>` and write that path, relative to the folder, as `vaultPath`.

The L1 check does not read the vault (`"vaultContentRead": false`): a wrong hash or size still passes, so compute them. The original creation time goes to `formulatedAt`; the import time to `recordedAt` (R-T5b).

```json
{"id": "src-01", "sourceKind": "instrument-report",
 "content": {"locator": {"vaultPath": "vault/80/802b521730c95985f71e8a4a9a8f5611ceaf3e5e34df5c4dff595e255d9c5d68.json"},
             "sha256": "802b521730c95985f71e8a4a9a8f5611ceaf3e5e34df5c4dff595e255d9c5d68",
             "mediaType": "application/json", "size": 152},
 "capturedAt": "2026-03-02T21:10:00Z", "authorship": {"author": "s-01"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "origin": "imported", "assertedBy": "subject", "recordedAt": "2026-09-12T19:00:00Z",
 "formulatedAt": "2026-03-02T21:10:00Z",
 "importedFrom": {"system": "example-chart-app", "systemVersion": "5.1", "importedAt": "2026-09-12T19:00:00Z", "run": "e-01"},
 "sensitivity": "special", "categories": ["birth-data"], "synthetic": true}
```

Who sees it: only the person. `maxRelease: "index"`: no grantee ever receives more than the kind, media type and a coarse date. **An analyst's notes** (variant): add the analyst to `parties` as `{"id": "p-01", "partyKind": "person", "label": "Chart analyst", "role": "practitioner"}` (a generic role, never a name) and store the notes as a Source with `sourceKind: "practitioner-notes"`, `authorship.author: "p-01"`, `inbound: true`, `maxRelease: "index"` and no `summary`.

### Step 3. Record the birth data: Claim

The export contains the birth data; the importer writes it once. Ask the person to check it.

```json
{"id": "c-01", "facet": "fact", "predicate": "birth-data",
 "text": "Born 2 November 1988 at 23:15 local time in Utrecht.",
 "origin": "imported", "assertedBy": "subject", "recordedAt": "2026-09-12T19:00:00Z",
 "formulatedAt": "2026-03-02T21:10:00Z",
 "importedFrom": {"system": "example-chart-app", "systemVersion": "5.1", "importedAt": "2026-09-12T19:00:00Z", "run": "e-01"},
 "horizon": "foundation", "sensitivity": "sensitive", "categories": ["birth-data"], "handling": ["person-only"],
 "synthetic": true}
```

Who sees it: only the person, always (`person-only`). Never put birth data in an id, a title or a note.

### Step 4. Record the relation to the lens: LensAdoption

`route: "imported"`, written by the import (`origin: "derived"`, so `generatedBy.method` and `derivedFrom` are required). It is `proposed` until the person confirms it in step 6.

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:human-design", "version": "0.2.0"}, "route": "imported",
 "uses": ["speak-in-lens", "store-results", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off",
 "representationPreference": "human-design.chart",
 "origin": "derived",
 "generatedBy": {"software": "example-chart-import", "version": "0.1.0", "method": "adopt the lens of the imported chart"},
 "derivedFrom": ["src-01"],
 "importedFrom": {"system": "example-chart-app", "systemVersion": "5.1", "importedAt": "2026-09-12T19:00:00Z", "run": "e-01"},
 "assertedBy": "subject", "recordedAt": "2026-09-12T19:00:00Z",
 "sensitivity": "special", "categories": ["birth-data"], "synthetic": true}
```

Who sees it: only the person; label … pending until confirmed, then ◇ frame. After that, a grant reaches it only through a selector that names the lens; its id alone never does.

### Step 5. Record the chart: AssessmentRecord

One AssessmentRecord with one `frame-attributes` result. `mode: "computed-from-birth-data"` requires `origin: "derived"` (AR-1) with `generatedBy.method` and `derivedFrom`. Keys of `attributes` are the descriptor's construct ids: `human-design/type`, `human-design/authority`, `human-design/profile`, `human-design/centres`. Values are short codes in lowercase, never descriptions. No `instrument` (the lens lists none); no `trademarkNotice` (the marks are never used). Because it shares the run of an imported adoption, it is `proposed` (LA-5). The checker does not check the attribute keys or values (§6), so follow these rules yourself.

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:human-design", "version": "0.2.0"},
 "mode": "computed-from-birth-data", "administeredAt": {"start": "2026-03-02", "precision": "day"},
 "results": [
   {"type": "frame-attributes",
    "attributes": {
      "human-design/type": "projector",
      "human-design/authority": "splenic",
      "human-design/profile": "2/4",
      "human-design/centres": {"defined": ["spleen", "throat", "ajna"]}},
    "computedFrom": "c-01",
    "engine": {"name": "example-chart-app", "version": "5.1"}}],
 "source": "src-01",
 "origin": "derived",
 "generatedBy": {"software": "example-chart-import", "version": "0.1.0", "method": "copy type, authority, profile and defined centres from the app export"},
 "derivedFrom": ["c-01", "src-01"],
 "importedFrom": {"system": "example-chart-app", "systemVersion": "5.1", "importedAt": "2026-09-12T19:00:00Z", "run": "e-01"},
 "formulatedAt": "2026-03-02T21:10:00Z",
 "assertedBy": "subject", "recordedAt": "2026-09-12T19:00:00Z",
 "epistemic": "frame-relative", "sensitivity": "special", "categories": ["birth-data"],
 "handling": ["no-infer", "no-quote-back"], "synthetic": true}
```

**Variant without a chart** (not in the worked example). If the person only names their type, write the whole record like this:

```json
{"id": "as-01", "lens": {"id": "urn:ohc:lens:human-design", "version": "0.2.0"},
 "mode": "self-identified", "administeredAt": {"start": "2026-09-12", "precision": "day"},
 "results": [{"type": "type-assignment", "construct": "human-design/type", "label": "Projector", "method": "self-identified"}],
 "validityFlags": ["self-identified-only"],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-12T19:00:00Z",
 "epistemic": "frame-relative", "sensitivity": "special", "categories": ["birth-data"],
 "handling": ["no-infer", "no-quote-back"], "synthetic": true}
```

- No `source`, `generatedBy`, `derivedFrom`, `computedFrom`, `engine`, `importedFrom` or `formulatedAt`: nothing was computed or imported. The checker accepts `generatedBy` and `derivedFrom` on a declared record (§6); leave them out anyway.
- With no chart there is no import: use the self-chosen route (§2), and write no Event and no Source (skip steps 1 and 2). Write step 3 only if the person wants the birth data recorded, then with `"origin": "declared"` and no `importedFrom` or `formulatedAt`. If other records of the context do come from an import run, leave `as-01` out of that Event's `records`.

Who sees it: only the person; served later only under a grant whose selector names the lens.

### Step 6. The person decides: Review

Nothing from the import counts until the person says so. Show the person what was imported. They confirm the adoption (`admit`), and accept the chart in full (`endorse`), in part (`partially-endorse`, with `endorsedPart` in their own words, which also confirms it), or not at all (`reject`). `endorsedPart` never quotes the record: name constructs, not values.

```json
{"id": "rv-01", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-09-13T08:00:00Z"}
```

```json
{"id": "rv-02", "target": "as-01", "action": "partially-endorse", "by": "subject", "recordedAt": "2026-09-13T08:05:00Z",
 "endorsedPart": "The authority and the profile speak to me; I leave the type aside."}
```

**If the person declines the adoption** (variant), write both Reviews: `decline` on the adoption **and** `reject` on the chart. A declined adoption does not withdraw the chart by itself: in OHC 0.1 a chart left `partially-endorse`d stays active and is served under the lens selector (§6). Then write no lens readings (skip steps 7a and 8).

```json
{"id": "rv-01", "target": "la-01", "action": "decline", "by": "subject", "recordedAt": "2026-09-13T08:00:00Z"}
```

```json
{"id": "rv-02", "target": "as-01", "action": "reject", "by": "subject", "recordedAt": "2026-09-13T08:00:00Z"}
```

Only the subject may make these decisions: the records are `special` (R-A1). Silence is not acceptance: an import the person never reviews stays `proposed`.

### Step 7. Keep only what the person accepts: Claims

**7a. A self-description in the system's terms.** `facet: "identity"`, `predicate: "self-description"`, `epistemic: "frame-relative"`, `derivedFrom` the chart. Never `facet: "disposition"` (CL-3; the lens establishes no trait).

**You MUST set `epistemic: "frame-relative"` on every Claim derived from `as-01`.** The checker does not catch its absence. Without it the Claim is computed as `as-reported`, labelled ✓ stated, and a grant that names its id serves it as a plain stated fact.

```json
{"id": "c-02", "facet": "identity", "predicate": "self-description",
 "text": "In this system's terms I decide by a quiet first yes or no in the moment; I trust that more than long lists.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-14T20:00:00Z", "horizon": "foundation",
 "derivedFrom": ["as-01"], "epistemic": "frame-relative", "handling": ["no-quote-back", "no-infer"],
 "synthetic": true}
```

Who sees it: only the person. In OHC 0.1 no grant can serve it (§6).

**7b. The same insight in plain words, for agents to act on.** Ask the person how they want to be worked with, in plain words. Write it without frame words and **without** `derivedFrom`, so it stands on the person's word. This is how an "authority" becomes something an assistant can respect without ever deciding for the person.

```json
{"id": "c-03", "facet": "preference", "predicate": "decision-brief",
 "text": "For a big request, give me the main point in one line and let me answer the same day; skip the long pros-and-cons list.",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-14T20:05:00Z", "horizon": "foundation",
 "synthetic": true}
```

Who sees it: only the person until a grant names it; tier `personal`, label ✓ stated.

### Step 8. Read an episode through the lens, in the person's words: Episode and Interpretation

In the example only the person writes a reading through this lens, after the adoption is confirmed (§6, item 10). Add at least one alternative that is not psychological.

```json
{"id": "ep-01", "occurred": {"start": "2026-09-01", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-09T21:00:00Z", "addedAt": "2026-09-09T21:00:00Z",
    "accountKind": "first-narrative",
    "happened": "At the first meeting I said yes to leading the neighbourhood garden project; a week later I stepped back.",
    "didOrTried": "Wrote to the group and offered to help with watering instead.",
    "understandingThen": "I thought I had simply taken on too much."}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-09T21:00:00Z",
 "sensitivity": "sensitive", "contexts": ["community"], "synthetic": true}
```

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading",
 "lens": {"id": "urn:ohc:lens:human-design", "version": "0.2.0"},
 "text": "In this system's terms I answered from the pressure of the room, not from my own first sense in the moment.",
 "grounds": [{"ref": "as-01", "kind": "instrument"}],
 "alternatives": [
   {"text": "The meeting ran late and everyone was waiting for a volunteer.", "kind": "situational"},
   {"text": "The project budget was cut the following week.", "kind": "external"}],
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-16T09:00:00Z",
 "epistemic": "frame-relative", "sensitivity": "special", "categories": ["birth-data"],
 "handling": ["no-quote-back"], "contexts": ["community"], "synthetic": true}
```

Who sees them: only the person. The Episode is `sensitive`; the reading is `special` and frame-relative.

### Step 9. Practices from the toolkit

None for an agent to run. The toolkit has one item, `human-design.chart` (the chart itself); an agent may offer it (`agentMayOffer: true`) when the person's agreement lets it suggest the frame.

A practice the person already has is recorded as a Practice with `source.route: "self-discovered"` and no `templateId` (variant, not in the worked example). First add `"practices"` to `conformance.modules` and `"practices": []` to the file; without the module the check fails with CX-5. `practiceKind` is one of `breathing`, `movement`, `reflection`, `writing`, `conversation`, `rest`, `planning`, `environment`, `social-contact`, `creative`, `contemplative`, `other`.

```json
{"id": "pr-01", "name": "Pause before saying yes", "description": "Wait until the next morning before taking on a new role.",
 "practiceKind": "reflection", "source": {"route": "self-discovered"}, "initialStatus": "in-use", "nonClinical": true,
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-16T09:30:00Z", "synthetic": true}
```

### Step 10. Decide who may see what: Grant

```json
{"id": "g-01", "recordedAt": "2026-09-15T10:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:human-design"]}, {"ids": ["ep-01"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-15T10:00:00Z", "channel": "holder-ui"},
 "note": "The system's language for my own reflection only; never advice about what I should decide."}
```

```json
{"id": "g-02", "recordedAt": "2026-09-15T10:05:00Z", "grantor": "subject", "grantee": "a-02",
 "purposes": ["assist-personal"],
 "scope": {"include": [{"facets": ["preference"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "none",
 "constraints": {"expiresAt": "2027-09-01T00:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "consent"},
 "expressedBy": {"actor": "subject", "at": "2026-09-15T10:05:00Z", "channel": "holder-ui"}}
```

What each grantee receives under §12.3, computed with the reference tools on the worked example, after the Reviews:

| Grantee | Served | Never served |
|---|---|---|
| `a-01` Reflection companion | `la-01`, `as-01` (endorsement `partial`, label ◇ frame), `in-01`, `ep-01` | `c-01` (person-only), `c-02` (frame-relative Claim, §6), `c-03` (not in scope), `src-01` (`maxSourceTier: none`) |
| `a-02` Personal assistant | `c-03` | everything that cites the lens |

Before step 6, `la-01` and `as-01` are proposed and go to no one but the person. With `decline` and `reject` (step 6 variant) and no readings, `a-01` receives only `ep-01`. A grant with only `{"ids": ["la-01", "as-01"]}` serves neither of them, even with explicit consent: name the lens. Grant g-01 gives no `suggest`, `write` or `infer`: the companion talks with the person in the person's terms and writes nothing through the lens.

To compute this table for your own context, run, for each grant:

```sh
python3 -B tools/ohc_query.py <folder>/context.json project --grant g-01 --purpose self-reflection --now 2026-10-10T12:00:00Z
python3 -B tools/ohc_query.py <folder>/context.json project --grant g-02 --purpose assist-personal --now 2026-10-10T12:00:00Z
```

Served records appear under `statements`, `experience`, `interpretations` and `recall`; the Parties they point to appear under `parties`. A context without the root `"synthetic": true` needs `--holder-key-file`.

### Step 11. Check

```sh
python3 -B tools/check.py <folder> --level L1 --json
```

Expect `"valid": true` and `"levelMet": "L1"`. A folder under an `examples/` directory is compared with its `expected-check.json` (X-3); a context of your own is not. A passing check does not cover what §2 and the steps say the checker does not catch: `epistemic` on derived Claims, the attribute keys, `e-01.records`, and the vault hashes.

## 4. Never

- Never bring Human Design up or offer to compute a chart unless the person's agreement lets you (`suggest` naming the lens), and then only as one option. Never read through it as an agent beyond the person's Grant and adoption (I5); an estimate is person-only (AR-2), and anything read in the frame is `frame-relative` (AR-4).
- Never use the registered composite mark listed in the descriptor (`use: avoid`) or the abandoned one, in any field. Say "Human Design" and use the construct ids.
- Never tell the person what to decide from their type, strategy or authority, and never use the chart to steer, pressure or persuade them (`persuasion-targeting` is prohibited; handling `no-leverage` if the person adds it). Under `decisionUse: approval-required` you may name a chart attribute the person accepted when you propose something, as the frame's language and never as a fact (R-G14, C-7). The person's own plain preference (step 7b) is what assistants follow.
- Never present a chart attribute, or anything read from it, as an empirical trait or a prediction (C-7); never map chart attributes to any trait, type or score (LN-3, mapping `no-relation`).
- Never use anything from this lens for the prohibited purposes (`personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting`), including composing teams or pairing people by chart.
- Never quote the chart back as proof ("your design says…"): `no-quote-back`. Speak in the frame in the person's words.
- Never compute, store or discuss another person's chart, or a combined chart (TP-1).
- Never serve the birth-data Claim; never put birth data in ids, titles or notes (R-I1).

## 5. Worked example

[examples/human-design/context.json](examples/human-design/context.json): Wren, a fictional neighbourhood volunteer. It contains exactly the records of section 3 (without the variants): `e-01`, `src-01`, `c-01`, `la-01`, `as-01`, `rv-01`, `rv-02`, `c-02`, `c-03`, `ep-01`, `in-01`, `g-01`, `g-02`, with the vault placeholder for `src-01`. The context root and every content record carry `"synthetic": true`.

```sh
python3 -B tools/check.py docs/lenses/examples/human-design --level L1 --json
```

Result: `"valid": true`, `"levelMet": "L1"`, no errors, no warnings ([expected-check.json](examples/human-design/expected-check.json)).

## 6. What does not fit yet

1. **A frame-relative Claim can never be shared.** A Claim has no `lens` field, and §12.3 step 8 serves a frame-relative record only through a selector that names its lens; step 7a's Claim is unservable even by id. Proposal: allow `lens` on a frame-relative Claim, or let step 8 accept an `ids` selector.
2. **No non-evidential "prompted by" link.** Citing the chart in the plain Claim (step 7b) would make the frame a ground and raise the Claim to `special`. Proposal: a Relation code such as `prompted-by`, with no tier propagation and never an inference path.
3. **An imported chart must be labelled `derived`.** AR-1 allows only `derived` for `computed-from-birth-data` (it rejects `imported`), although the values were copied from an app whose computation the person did not run. Proposal: allow `imported` (with `importedFrom`) for this mode.
4. **Imported birth data is active without the person's look.** LA-5 makes only AssessmentRecords of an imported run proposed; the birth-data Claim and the Source from the same run are active at once, and the Claim is even labelled ✓ confirmed. Proposal: extend LA-5 to every content record of the run.
5. **Exact provenance can collide with the marks.** If the app's own name contains a mark that the descriptor says to `avoid`, `engine.name` and `importedFrom.system` cannot name it. Proposal: allow nominative use in provenance fields only, with the mark's notice, or an `engine.ref` URI.
6. **An analyst's reading has no place.** *Resolved in 0.1.0-draft.2:* routes restrict nothing (LN-3 now only forbids cross-lens mapping), and I5 applies `agentInterpretation` to agent and software authors only, so an analyst listed in `interpretationAuthors` of an inherited adoption may author a reading.
7. **`frame-attributes.attributes` is unstructured.** Centres (defined, undefined), gates and channels have no shape, and nothing ties keys to constructs or limits precision. Proposal: `attributes: [{"construct", "value"}]` and a descriptor list of attributes never to store.
8. **`decisionUse: never` reads as if the person's own use were forbidden.** *Resolved in 0.1.0-draft.2:* records carry no `decisionUse`. The person's own choices are theirs; what an agent may weigh in what it proposes is the person's grant (R-G14), and decisions by others are closed by the prohibited purposes (§8.10).
9. **Lens defaults cannot set handling.** Proposal: `defaults.handling` in the descriptor. (That the adoption route is not checked against the descriptor's routes is intended since 0.1.0-draft.2: routes describe, they never restrict.)
10. **Records of a lens stay served when the person declines the adoption, and a reading is served while the adoption is still proposed.** After a Review `decline` of `la-01`, `as-01` from the same import run (left `partially-endorse`d) and `in-01` are still served under the lens selector. With no Reviews at all, `in-01` is served while `la-01` is proposed. Proposal (§12.3): a lens selector serves a lens's records only while the person's adoption of that lens is active; and LA-5: declining an imported adoption declines every record of its run.
11. **`importedFrom.run` is not resolved, and `Event.records` is not cross-checked.** `c-01` and `src-01` with `importedFrom.run: "e-01"` pass when no Event exists (the self-chosen route done literally leaves exactly this). An Event whose `records` omit `la-01`, while `la-01` carries that run, also passes. Proposal: add `importedFrom.run` to the reference-targets catalog, resolving to an Event with `eventType: "import-run"`; and a rule that every record carrying run `e` is listed in `e.records`, and the reverse.
12. **The frame-relative status does not pass along `derivedFrom`.** A Claim derived from the chart (step 7a) written without `epistemic` is computed `as-reported`, labelled ✓ stated, and served to a grant that names its id; no rule or warning fires. Proposal: make `frame-relative` pass along `derivedFrom` and `grounds` the way the tier does, or an error at L1 when a record derived from a frame-relative record is not `frame-relative`.
13. **A declared record may carry `generatedBy` and `derivedFrom`.** A self-identified AssessmentRecord (`origin: "declared"`) that keeps them passes, so its provenance claims a computation that did not happen. Proposal: `generatedBy` only with `origin` `derived` or `inferred`.
14. **The root `synthetic` flag is not tied to the records' flags.** Outside example mode, every content record can be synthetic while the root is not; the checker accepts it, and `ohc_query.py` then demands a holder key. Proposal: warn at L1 on the mismatch, or derive the root flag from the records.
15. **The vault is not compared with the Source at L1.** A wrong `sha256` or `size` passes (`"vaultContentRead": false`). Proposal: an opt-in check (or L1 when the vault is local) that hashes vault files and compares `sha256` and `size`: an error on mismatch, a warning when the file is absent.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
