# Lens recipe: `ifs` (parts lens)

**Recipe · lens `urn:ohc:lens:ifs` 0.2.0 · OHC 0.1.0-draft.2 · informative · 12 October 2026**

This recipe shows, step by step, how a person's own parts language enters an OHC context through the `ifs` lens, which records it creates, who sees them, and what an agent must never do with them.

> **Notice.** OHC features are not IFS therapy and are not IFS-certified. Internal Family Systems is the subject of US application SN 98151674 by The Center for Self Leadership, Inc. (IFS Institute), under opposition. The name is used here nominatively only, to identify the method the lens descriptor refers to.

**The lens at a glance** (from [`spec/lenses/ifs.lens.json`](../../spec/lenses/ifs.lens.json); see also [LENSES.md §7.6](../../spec/LENSES.md#76-how-each-lens-works-with-a-person)):

| | |
|---|---|
| Kind and status | `parts-model`, descriptor `draft` |
| Constructs | `ifs/self`, `ifs/manager`, `ifs/firefighter`, `ifs/exile` (trauma-adjacent), `ifs/burden` (trauma-adjacent) |
| Instruments | none: there is nothing to score |
| Toolkit | `ifs.noticing-a-part` (the person alone; an agent never offers it; produces a Part); `ifs.exile-work` (practitioner only; produces nothing in OHC) |
| Representation | `ifs.parts-map`: a view over Parts and part Relations, never stored as a shape (P-4) |
| Agent suggestion | by the person's Grant (`suggest` naming the lens); the descriptor's guidance: only after the person asked for ways of looking at an inner conflict |
| Agent interpretation | by the person's Grant (`infer` naming the lens) and adoption (I5); `off` in the example, the default; never naming or interpreting parts (`helperMustNot`) |
| Cross-lens mapping | `not-allowed` |
| Defaults | tier `special`; categories `mental-health`, `trauma-adjacent`; `reviewAfter` `P6M` |

**Facts, not permissions (0.1.0-draft.2).** The descriptor carries facts and guidance, never a permission. Whether an agent suggests this lens, reads through it, offers its tools or weighs its results in what it proposes is the person's agreement: a grant whose scope names the lens (`suggest`, `infer`; `decisionUse`, R-G14), narrowed by their adoption (`agentInterpretation`) and handling codes ([CONTEXT-08](../agents/procedures/CONTEXT-08.md)). The prohibited purposes ([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)) protect the person from decisions of others and bind every grantee; no record carries a copy of them.

**Ways of working.** The descriptor lists one playbook, [`urn:ohc:playbook:ifs-basic`](../../spec/playbooks/ifs-basic.playbook.json) (Internal Family Systems: basic ways of working, by the OHC editors), for these situations: under strain: tired, pressed or overloaded; preparing a hard conversation; after a setback. An agent receives it at session start with the person's records in this lens, follows a step only within the grant, and never lets a step outweigh what the person says now (PB-4, PB-5). The person may choose other playbooks, or none, in the adoption's `playbooks` (PB-3); a coach's or therapist's own way of using the lens comes in as a local playbook (`urn:ohc:playbook:x-<namespace>:<name>`) kept in the person's context.

## 1. What you may have

- **Self-description in conversation.** The person speaks of inner positions in their own words: "a part of me wants to check the figures again, another part wants to cancel".
- **The person's own notes.** A journal entry written after noticing a part.
- **Notes from therapy or coaching** in which parts language is used: the practitioner's notes, a session summary, or the person's own notes from a session. This is practitioner material and has a custodian.

Not for this lens:

- **An instrument report.** The lens has no instrument, so there is no score, profile or type to import.
- **An agent's reading** without the person's Grant (`infer` naming the lens) and adoption (I5). Even with them, an agent never names, invents or proposes a part (`helperMustNot`); in the example the grant has `read` only.

## 2. Before you start

**Route of adoption.** Choose the one that matches how the person came to the lens.

| Route | When | What it changes |
|---|---|---|
| `self-chosen` | The person picked the lens. | The person writes the adoption; it is active at once. |
| `agent-suggested` | The person asked you for ways of looking at an inner conflict, you mentioned this lens as one option among others, and the person took it. | Only under a Grant with `suggest` naming the lens; you mention it only after such a request (`suggestionRequires`), and you use no lens language until it is adopted. The adoption carries `suggestedBy` (your Party id) and stays `proposed` until the person admits it with a Review, even when the person writes it. The checker does not remind you of that Review (step 1). |
| `inherited-from-practice` | The person uses the lens in therapy or coaching. | Add a `practice` block (role, practitioner Party, relationship). With a therapist, set `confidentiality: "therapy-confidential"`: the adoption and every record that cites it in `adoption` (Parts, lens readings) become `person-only` (LA-4). A Practice cannot cite the adoption, so you add `person-only` to it yourself (step 6). With a coach, `practitioner-scope`. If you store any session material, `practice.releaseRef` must name the practitioner's release (LA-3). `onEnd` says what happens when the relationship ends. |
| `imported` | Not listed for this lens: there is no instrument to import from. | Routes describe usual practice and restrict nothing. |

**Consent.** The person adopts the lens; you do not. An adoption is the person's statement, not a permission: it gives nobody access, not even the practitioner (LA-2, R-G13). Access needs a Grant (step 7). Every Part is written by the person (P-2). You may type what the person dictates, read it back and let them correct it before saving ([CONTEXT-01](../agents/procedures/CONTEXT-01.md)). Leave `recordedBy` out: if you set it to your own Party id, rule INF-1 requires `underGrant` and `purpose` under a grant that includes `write`.

**Defaults for this lens.**

- `sensitivity: "special"` on every record of the lens: the adoption, Parts, lens readings, practices from the toolkit, and Sources from sessions. Documentation calls this "treated as special category".
- `categories: ["mental-health", "trauma-adjacent"]`: the lens defaults. Records can raise them, never lower them; only the person can lower a tier, with a `relax` Review.
- Parts carry `handling: ["person-only"]` by default (P-3). Adding `no-quote-back` and `no-forward` is recommended.
- `agentInterpretation: "off"`, always.
- `reviewAfter`: `P6M`.

**Never stored.**

- Any score or rating: there is no instrument, and "how much of each part" is not a measurement.
- Training or workshop materials of the method, or published exercise text (descriptor restriction).
- Part names, roles or descriptions that an agent invented or suggested.
- Anything about exiles or burdens that an agent wrote or asked for.
- Labels from other lenses attached to parts, for example a personality type on a part (`crossLensMapping: not-allowed`).
- Diagnoses or clinical terms.
- The text of practitioner notes inside any record. Only the Source metadata is a record; the bytes stay in the vault.

## 3. Steps

Each step says what to do, which record it creates, the array of the context file it goes into, a minimal record that validates against the schema, and who sees it by default. The snippets are taken from the [worked example](#5-worked-example) or were checked against it; they carry `"synthetic": true` because the person is fictional, and you leave that field out for a real person. With no grant, nothing is disclosed to anyone but the person. Do the steps in order, and give each record a `recordedAt` later than the records it builds on.

### Step 0. Start the context file

Create a folder for the person's context and, in it, a file `context.json` (the single-document form, [§3.3](../../spec/SPECIFICATION.md#33-two-serializations-of-one-data-model); [schema](../../spec/schema/context.schema.json)). Start it with this envelope:

```json
{
  "format": "ohc.context",
  "specVersion": "0.1.0-draft",
  "id": "urn:ohc:example:ysolde:context",
  "version": "2026-10-01.1",
  "subject": {"id": "urn:ohc:example:ysolde", "displayName": "Ysolde (fictional)"},
  "holder": "subject",
  "lang": "en",
  "created": "2026-09-20T19:00:00Z",
  "conformance": {"level": "L1", "modules": ["core", "governance", "lenses", "practices", "inner-system"], "subjectIsAdult": true},
  "parties": [],
  "policy": {"admission": "subject-only", "resolver": "returnDialog"},
  "lenses": [{"id": "urn:ohc:lens:ifs", "version": "0.2.0"}],
  "synthetic": true,
  "lensAdoptions": [], "sources": [], "episodes": [], "parts": [], "relations": [], "claims": [],
  "interpretations": [], "practices": [], "outcomes": [], "grants": [], "reviews": []
}
```

- **Modules.** Declare every module whose records you write, or the checker reports errors: `core` (Party, Source, Episode, Claim, Relation, Interpretation, Review), `governance` (Grant), `lenses` (LensAdoption), `practices` (Practice, Outcome), `inner-system` (Part and part-to-part Relations).
- **Arrays.** Each record goes into the array of its kind: LensAdoption → `lensAdoptions`, Source → `sources`, Episode → `episodes`, Part → `parts`, Relation → `relations`, Claim → `claims`, Interpretation → `interpretations`, Practice → `practices`, Outcome → `outcomes`, Grant → `grants`, Review → `reviews`, Party → `parties`. Each step below names its array again.
- **`synthetic`.** In an example, the context and every content record carry `"synthetic": true`; Parties, Grants and Reviews never do (the schema rejects it there).
- **For a real person.** Use `urn:uuid:` ids for `id` and `subject.id`, for example from `python3 -c "import uuid; print('urn:uuid:' + str(uuid.uuid4()))"`; leave out `synthetic` everywhere; `displayName` is optional. Keep the folder out of any folder named `examples`. A context whose `id` starts with `urn:ohc:example:`, or that sits inside an `examples` folder, is checked as an example and then needs `"synthetic": true` on every content record (X-1, CX-8).
- **`version`** is yours to choose; change it with every set of changes.
- **The empty file does not pass yet.** A context needs at least one Claim, or one Episode with an account (LV-0); step 3 adds one. Check after step 3, and again at the end (step 8).

### Step 1. Record the adoption (LensAdoption → `lensAdoptions`)

Ask the person how they came to the lens and what it may be used for. Write one LensAdoption ([§10.5](../../spec/SPECIFICATION.md#105-lensadoption), [schema](../../spec/schema/lens-adoption.schema.json)).

- `uses`: `speak-in-lens` (you may use the person's own part names when they bring them up), `store-results` (the person keeps Parts), `interpret` (the person's own readings). Do not list `offer-practices`: the only self-guided toolkit item is never offered by an agent.
- `interpretationAuthors`: `["subject"]`. A therapist the person adds here may author readings through the lens (I5; §6, item 4).

```json
{"id": "la-01", "lens": {"id": "urn:ohc:lens:ifs", "version": "0.2.0"}, "route": "self-chosen",
 "confidentiality": "none", "uses": ["speak-in-lens", "store-results", "interpret"],
 "interpretationAuthors": ["subject"], "agentInterpretation": "off", "representationPreference": "ifs.parts-map",
 "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-20T19:00:00Z",
 "sensitivity": "special", "categories": ["mental-health", "trauma-adjacent"], "synthetic": true}
```

**Variant: `inherited-from-practice` with a therapist.** Put the practitioner in `parties`: `{"id": "p-01", "partyKind": "person", "label": "Therapist", "role": "practitioner"}`. Then change the adoption to:

```json
{"route": "inherited-from-practice",
 "practice": {"role": "therapist", "practitioner": "p-01", "relationship": "active", "since": "2026-05-01", "releaseRef": "src-03"},
 "confidentiality": "therapy-confidential", "onEnd": "ask"}
```

Do not add `handling` to the adoption: LA-4 already makes it, and every record that cites it in `adoption`, `person-only`. `releaseRef` names the release Source of step 2; leave it out if you store no session material.

**Variant: `agent-suggested`.** Put yourself in `parties`: `{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}`. Add `"suggestedBy": "a-01"` to the adoption, and write the person's Review into `reviews` right after it:

```json
{"id": "rv-00", "target": "la-01", "action": "admit", "by": "subject", "recordedAt": "2026-09-20T19:01:00Z"}
```

Without that Review the adoption stays `proposed`. **The checker does not remind you:** a context without it is still valid, and the Parts and the Practice of the lens are still served (§6, item 9). Write the admit Review before any Part, Interpretation or Practice of the lens, with a `recordedAt` earlier than theirs.

**Who sees it:** only the person.

### Step 2. Keep the original in the vault (Source → `sources`)

If there is a note, keep it as a Source ([§10.1](../../spec/SPECIFICATION.md#101-source), [schema](../../spec/schema/source.schema.json)). The record holds only metadata; the bytes go into the vault:

1. Compute the hash: `shasum -a 256 <file>` (or `sha256sum <file>`). The 64 hexadecimal characters are `sha256`.
2. Compute the size in bytes: `wc -c < <file>`. That number is `size`.
3. Copy the file to `vault/<first two characters of the hash>/<hash>.<extension>`. `vaultPath` is relative to the folder that holds `context.json`.
4. The L1 checker does not open the vault (its report says `"vaultContentRead": false`): it does not notice a missing file, a wrong hash or a wrong size. Run the two commands again on the stored file and compare.

Set `maxRelease: "index"`, so that a grantee can learn at most that the note exists.

```json
{"id": "src-01", "sourceKind": "journal-entry", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-24T21:10:00Z",
 "content": {"locator": {"vaultPath": "vault/4f/4fd5d61f5cf141e1b4c566d9b5a007765966a167599bb3908e14230b452edb68.md"},
             "sha256": "4fd5d61f5cf141e1b4c566d9b5a007765966a167599bb3908e14230b452edb68",
             "mediaType": "text/markdown", "size": 313},
 "capturedAt": "2026-09-24T21:00:00Z", "authorship": {"author": "subject"}, "contemporaneity": "contemporaneous",
 "maxRelease": "index",
 "summary": {"text": "Evening note after the club meeting.", "authoredBy": "subject",
             "recordedAt": "2026-09-24T21:10:00Z", "method": "subject-written"},
 "retention": {"eraseOnRequest": true}, "sensitivity": "special", "categories": ["mental-health"],
 "contexts": ["community"], "synthetic": true}
```

The worked example ships these bytes: [examples/ifs/vault/4f/…](examples/ifs/vault/4f/4fd5d61f5cf141e1b4c566d9b5a007765966a167599bb3908e14230b452edb68.md).

Notes written by a therapist are a different Source: `sourceKind: "practitioner-notes"`, `authorship.author` the practitioner Party, `inbound: true`, and a custody block. The release itself is a second Source of kind `practitioner-release`. Without a release, the ceiling for every grantee is `index`; with one, `therapy` material still never goes beyond `summary` (§15.3). The hashes and sizes below stand for files that are not in the example: compute your own from your files.

```json
{"id": "src-02", "sourceKind": "practitioner-notes", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-30T18:00:00Z",
 "content": {"locator": {"vaultPath": "vault/b8/b81016884e0296fcb93739c2ea2e8dd1e2a8263bf098743644fe1f28a1ed9c67.md"},
             "sha256": "b81016884e0296fcb93739c2ea2e8dd1e2a8263bf098743644fe1f28a1ed9c67", "mediaType": "text/markdown", "size": 57},
 "capturedAt": "2026-09-30T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "custody": {"custodian": "p-01", "confidentiality": "therapy", "releaseRef": "src-03"},
 "maxRelease": "index", "retention": {"eraseOnRequest": true},
 "sensitivity": "special", "categories": ["mental-health", "trauma-adjacent"], "synthetic": true}
```

```json
{"id": "src-03", "sourceKind": "practitioner-release", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-30T18:00:00Z",
 "content": {"locator": {"vaultPath": "vault/d1/d13acd83828d0a58241ee830abd2ddd45ba8d87ed0c4d7c5c91795c6b32ba5dd.md"},
             "sha256": "d13acd83828d0a58241ee830abd2ddd45ba8d87ed0c4d7c5c91795c6b32ba5dd", "mediaType": "text/markdown", "size": 71},
 "capturedAt": "2026-09-30T17:00:00Z", "authorship": {"author": "p-01"}, "inbound": true,
 "maxRelease": "index", "retention": {"eraseOnRequest": true}, "synthetic": true}
```

**Who sees it:** the person has every tier (V-0). A grantee gets at most `index` (no title, no summary, no hash), and only under a grant that names the Source.

### Step 3. The experience and the parts (Episode → `episodes`, Part → `parts`, Relation → `relations`)

This lens describes its results as Parts, not as an AssessmentRecord.

**3a. The experience.** First write what happened, in plain words, as an Episode with the person's own account ([§10.2](../../spec/SPECIFICATION.md#102-episode), [schema](../../spec/schema/episode.schema.json)). Parts come later, in their own records.

```json
{"id": "ep-01", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-24T21:15:00Z",
 "title": "Budget evening at the club", "occurred": {"start": "2026-09-24", "precision": "day"},
 "accounts": [
   {"narrator": "subject", "narratedAt": "2026-09-24T21:00:00Z", "addedAt": "2026-09-24T21:15:00Z",
    "accountKind": "in-the-moment",
    "happened": "Before the club meeting I opened the budget file four times and drafted a message cancelling my slot.",
    "experienced": "Tight in the chest; a pull to check again and a pull to run.",
    "didOrTried": "Did not send the message. Wrote down what each side wanted, then went.",
    "understandingThen": "I thought I was just badly prepared.",
    "evidence": [{"source": "src-01", "selector": {"type": "whole"}}]}],
 "selection": {"selectedBy": "subject", "reason": "subject-chose"}, "salience": "medium",
 "contexts": ["community"], "synthetic": true}
```

**3b. The parts.** One Part per inner position the person names ([§20](../../spec/SPECIFICATION.md#20-inner-system-parts-experimental), [schema](../../spec/schema/part.schema.json)).

- `name` is the person's own words. Never suggest a name.
- `role` is optional. Set it only when the person chooses one of the lens constructs for this part themselves (`ifs/manager` or `ifs/firefighter`). Never use `ifs/self`: the Self is not a part in this lens. Never propose `ifs/exile` or `ifs/burden`. If the person brings such a part from therapy, they write it themselves, it stays `person-only`, and you do not ask about it.
- `authoredWith`: `alone`, `with-practitioner`, or `with-agent` when you typed what the person dictated.
- `adoption: "la-01"` ties the Part to the adoption; under a therapist, this is what makes it `person-only` through LA-4.

```json
{"id": "part-01", "name": "The double-checker", "description": "Goes over every figure again before anyone sees it.",
 "lens": {"id": "urn:ohc:lens:ifs", "version": "0.2.0"}, "adoption": "la-01", "role": "ifs/manager",
 "intention": "Make sure nobody finds a mistake in my numbers.", "concern": "Being shown up in front of the club.",
 "typicalTriggers": ["presenting figures to a group"], "firstNoticed": {"start": "2026-09-01", "precision": "month"},
 "authoredWith": "alone", "origin": "declared", "assertedBy": "subject", "recordedAt": "2026-09-24T21:20:00Z",
 "sensitivity": "special", "categories": ["mental-health", "trauma-adjacent"],
 "handling": ["person-only", "no-quote-back", "no-forward"], "synthetic": true}
```

The second part in the example, `part-02` ("The one who wants to cancel"), has no `role`: the person did not choose one.

**3c. How the parts relate.** A part-to-part link is a Relation `protects`, `polarized-with` or `allied-with`, written by the person ([§9.5](../../spec/SPECIFICATION.md#95-relation)).

```json
{"id": "r-01", "rel": "polarized-with", "from": "part-01", "to": "part-02", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-09-24T21:22:00Z", "synthetic": true}
```

The parts map (`ifs.parts-map`) is drawn from these records at display time and never stored.

**Who sees it:** only the person (Parts are `person-only`; part Relations are `special`).

### Step 4. Statements the person accepts (Claim → `claims`, Relation `held-by` → `relations`)

The lens has no results, so a Claim is never derived from it. A Claim also never rests on a Part, because a Part is a reading (layer `interpretation`). If noticing a part led the person to a need, a boundary or a preference they want to state, write it as an ordinary Claim in their words ([§9.4](../../spec/SPECIFICATION.md#94-claim)) and link it to the part with a Relation `held-by` ("this statement is voiced by this part").

```json
{"id": "c-01", "facet": "need", "predicate": "structure",
 "text": "I need the figures closed a day before I present them.", "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-26T08:00:00Z", "horizon": "focus", "contexts": ["community"], "synthetic": true}
```

```json
{"id": "r-02", "rel": "held-by", "from": "c-01", "to": "part-01", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-09-26T08:01:00Z", "synthetic": true}
```

**Who sees it:** the Claim keeps its own tier (`sensitive` for facet `need`), because tiers spread along citations and never along a Relation. A grant that names the facet can therefore serve the need without revealing which part holds it. The `held-by` Relation is `special` and is served only to a selector that names it.

### Step 5. Readings of an episode through the lens: the person's (Interpretation → `interpretations`)

In the example only the person reads through this lens (the grant has `read` only). You may ask, after the adoption and only when the person brings up an inner conflict, the descriptor's questions: "Which inner positions and needs are active right now?" and "What might this part be afraid would happen if it stepped back?" The answer is the person's to write.

Write the reading as an Interpretation about the Episode, with the lens and the adoption ([§10.3](../../spec/SPECIFICATION.md#103-interpretation), [schema](../../spec/schema/interpretation.schema.json)). Alternatives are not required from the person, but offer the slot: at least one non-psychological explanation (sleep, load, missing information) keeps the reading honest. An Interpretation cannot point at a Part in `about` (§6, item 1). If the reading names a part that is still `person-only`, mark the reading `person-only` too; otherwise the part's name travels in the reading's text (§6, item 2).

```json
{"id": "in-01", "about": ["ep-01"], "stance": "lens-reading", "lens": {"id": "urn:ohc:lens:ifs", "version": "0.2.0"},
 "adoption": "la-01",
 "text": "Two of my parts pulled in opposite directions: the double-checker wanted one more pass, the one who wants to cancel wanted out. Once each had been heard, I could go.",
 "alternatives": [
   {"text": "I had slept five hours the night before.", "kind": "physiological"},
   {"text": "The final bank figures only arrived that afternoon.", "kind": "informational"}],
 "heldDuring": {"from": "2026-09-27"}, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-27T20:00:00Z", "sensitivity": "special", "categories": ["mental-health", "trauma-adjacent"],
 "handling": ["person-only", "no-quote-back"], "contexts": ["community"], "synthetic": true}
```

**Who sees it:** only the person (`person-only`).

### Step 6. A practice from the toolkit and how it went (Practice → `practices`, Outcome → `outcomes`)

The only self-guided toolkit item is `ifs.noticing-a-part`: notice, name in your own words, ask what it wants you to know, change nothing. Its descriptor says `agentMayOffer: false`, so you never offer it (PC-2). If the person already does it and wants to keep it, they write it as a Practice ([§17.1](../../spec/SPECIFICATION.md#171-practice), [schema](../../spec/schema/practice.schema.json)) with `source.route: "from-lens"` and `templateId: "ifs.noticing-a-part"`, in their own words. `ifs.exile-work` is practitioner-only and is never a Practice here.

```json
{"id": "pr-01", "name": "Pause and ask the part",
 "description": "When I notice the pull, I name it in my own words and ask what it wants me to know, without trying to change it.",
 "practiceKind": "reflection",
 "source": {"route": "from-lens", "lens": "urn:ohc:lens:ifs", "templateId": "ifs.noticing-a-part"},
 "steps": ["Stop for a minute", "Name the pull in my own words", "Ask what it wants me to know", "Write one line, change nothing"],
 "duration": "PT5M",
 "limits": "Stop if it gets too much. Anything that feels like old hurt goes to a practitioner, not here.",
 "initialStatus": "in-use", "nonClinical": true, "origin": "declared", "assertedBy": "subject",
 "recordedAt": "2026-09-21T19:30:00Z", "sensitivity": "special", "categories": ["mental-health", "trauma-adjacent"],
 "synthetic": true}
```

**If the adoption is `therapy-confidential`,** add `"handling": ["person-only"]` to the Practice yourself. A Practice has no `adoption` field, so LA-4 does not reach it, and without the handling a lens grant serves it (checked; §6, item 8).

The person says how it went as an Outcome ([§17.2](../../spec/SPECIFICATION.md#172-outcome), [schema](../../spec/schema/outcome.schema.json)):

```json
{"id": "oc-01", "about": {"practice": "pr-01"}, "episode": "ep-01", "result": "helped", "origin": "declared",
 "assertedBy": "subject", "recordedAt": "2026-09-24T21:25:00Z", "synthetic": true}
```

**Who sees it:** with no grant, only the person. Under a grant that names the lens, the Practice is served, because it carries the lens in `source.lens`. The Outcome is not, because it carries no lens; it takes the Practice's tier.

### Step 7. Who may see what (Party → `parties`, Grant → `grants`, Review `relax` → `reviews`)

By default nobody sees anything. If the person wants a reflection companion to be able to use their part names, first put the companion in `parties` (skip this if you already did in step 1):

```json
{"id": "a-01", "partyKind": "agent", "label": "Reflection companion"}
```

The id prefix gives the kind of party and is checked: `a-` for an agent, `p-` for a person, `s-` for software, `o-` for an organization. Then the person gives a narrow grant ([§12.1](../../spec/SPECIFICATION.md#121-grant), [schema](../../spec/schema/grant.schema.json)):

- `actions: ["read"]` only, in this example: the person writes every lens record. Adding `suggest` or `infer` naming the lens is the person's choice (I5); an agent still never names, invents or interprets parts.
- A selector that names the lens (`lenses`), `basis.legal: "explicit-consent"` and an expiry of at most 180 days: special records require all three (R-G3, R-G10).
- `mode: "summary"`, `interpretations: "subject-endorsed"`, `maxSourceTier: "none"`.

```json
{"id": "g-01", "recordedAt": "2026-10-01T09:00:00Z", "grantor": "subject", "grantee": "a-01",
 "purposes": ["self-reflection"],
 "scope": {"include": [{"lenses": ["urn:ohc:lens:ifs"]}]},
 "actions": ["read"], "mode": "summary", "interpretations": "subject-endorsed", "maxSourceTier": "none",
 "constraints": {"expiresAt": "2027-03-28T09:00:00Z", "storage": "session", "forwarding": false,
                 "crossContextUse": false, "delegable": false},
 "basis": {"legal": "explicit-consent"},
 "expressedBy": {"actor": "subject", "at": "2026-10-01T09:00:00Z", "channel": "holder-ui"},
 "note": "Use my own part names when I bring them up. Never name, interpret or look for parts yourself."}
```

The grant alone does not reach any Part, because Parts are `person-only`. The person chooses, part by part, which one the companion may know, with a `relax` Review that removes `person-only` ([§11.1](../../spec/SPECIFICATION.md#111-review)):

```json
{"id": "rv-01", "target": "part-01", "action": "relax", "by": "subject", "recordedAt": "2026-10-01T09:05:00Z",
 "disclosure": {"removeHandling": ["person-only"]},
 "note": "The companion may know this part and use its name."}
```

**What the companion then receives.** From the repository root, run:

```sh
python3 -B tools/ohc_query.py <your context folder> project --grant g-01 --purpose self-reflection --now latest
```

For the worked example the folder is `docs/lenses/examples/ifs`. `--purpose` is required and must be one of the grant's purposes. `--now latest` evaluates the grant at the time of the newest record in the file, so the result does not depend on today's date or on the grant having expired since. The tool prints two lines (the time it used, the key) and then the projection as JSON. Served records are listed under `statements` (here `statements.lensAdoptions`: `la-01`; `statements.practices`: `pr-01`), `experience` (nothing here) and `interpretations` (here `interpretations.parts`: `part-01`). `derived` holds the computed labels of each served record, and `obligations.handling` the handling the companion must follow (`part-01`: `no-forward`, `no-quote-back`). The companion does not receive `part-02`, the reading `in-01`, the Episode, the Source, the Claim, the Outcome or any Relation.

### Step 8. Check

From the repository root:

```sh
python3 -B tools/check.py <your context folder> --level L1 --json
```

Fix every error until it reports `"valid": true` and `"levelMet": "L1"`. The checker also compares its output with an `expected-check.json` next to the file (rule X-3), but only when the folder sits inside a folder named `examples`; your own context folder does not need one. The checker does not read the vault (step 2) and does not tell you about a missing admit Review (step 1): check both yourself.

## 4. Never

- **Prohibited purposes:** `personnel-selection`, `task-allocation`, `performance-evaluation`, `promotion-decision`, `cross-person-ranking`, `persuasion-targeting` and every other purpose of [§8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed), under any grant. A reading grounds a choice you propose for the person only under `decisionUse: approval-required`, only when the person accepted it, naming what you weighed (R-G14).
- **No agent inference unless the person allows it.** Write a record with `origin: "inferred"` through this lens only under the person's Grant (`infer` naming the lens) and adoption (I5); in the example `agentInterpretation` is `off`. Even then never name, invent or interpret parts (`helperMustNot`), and never map Parts or lens readings to another lens (`crossLensMapping: not-allowed`).
- **No parts work by an agent.** Never present yourself as doing IFS therapy. Never name, invent or interpret parts. Never go toward exiles or burdens, and never suggest unburdening. Never author a Part (P-2).
- **A part is never an actor.** A Part never consents, never grants and never authorises anything (P-1, C-10). "This part agrees" is not consent.
- **No offering unless asked.** Never suggest the lens unless the person asked for ways of looking at an inner conflict (`suggestionRequires`) and the person's Grant lets you suggest it. Never offer `ifs.noticing-a-part` (`agentMayOffer: false`) or `ifs.exile-work` (practitioner only).
- **No quoting back.** Never use a part against the person, as in "your double-checker is at it again" (`no-quote-back`, `no-leverage`).
- **Trademark.** Use "Internal Family Systems" and "IFS" only to name the method the lens refers to, never as a label for what an agent does, and carry the notice above when naming it.

## 5. Worked example

[examples/ifs/context.json](examples/ifs/context.json) is one file at level L1 about Ysolde, who is fictional. The context and every content record carry `"synthetic": true`. It holds exactly the records of section 3:

| Step | Records |
|---|---|
| 0 | the envelope, with modules `core`, `governance`, `lenses`, `practices`, `inner-system` |
| 1 | `la-01` |
| 2 | `src-01`, with its bytes in [vault/4f/](examples/ifs/vault/4f/4fd5d61f5cf141e1b4c566d9b5a007765966a167599bb3908e14230b452edb68.md) |
| 3 | `ep-01`, `part-01`, `part-02`, `r-01` |
| 4 | `c-01`, `r-02` |
| 5 | `in-01` |
| 6 | `pr-01`, `oc-01` |
| 7 | the Party `a-01`, `g-01`, `rv-01` |

The variants shown in steps 1, 2 and 6 (therapist, release, agent suggestion, a `person-only` Practice) are not in the file.

```sh
python3 -B tools/check.py docs/lenses/examples/ifs --level L1 --json
```

It reports `"valid": true` and `"levelMet": "L1"`, with no errors and no warnings. [expected-check.json](examples/ifs/expected-check.json) is the exact output. The projection of step 7:

```sh
python3 -B tools/ohc_query.py docs/lenses/examples/ifs project --grant g-01 --purpose self-reflection --now latest
```

## 6. What does not fit yet

These are gaps in OHC 0.1 for this lens, found while writing this recipe and while a newcomer followed it. Each has a proposal for the next pass.

1. **A reading cannot be about a part.** `Interpretation.about` accepts Episodes, Claims, Patterns and AssessmentRecords only (RF-1); the checker rejects a Part there. Yet §8.3 and I9 speak of an Interpretation whose `about` includes a Part. *Proposal:* allow `about` → Part when the `inner-system` module is declared, and align I9 with RF-1.
2. **Part names leak through text.** A lens reading that names a `person-only` Part is served under a lens grant unless the writer remembers to mark it too: the Part's handling does not travel. *Proposal:* a field `mentions: [Part ids]` on Interpretations and Episode accounts that carries the Parts' tier and handling (C3); or default `person-only` for every reading through a `parts-model` lens.
3. **No "name only" sharing.** `uses: speak-in-lens` needs the agent to know the person's part names, but the only way is to `relax` the whole Part, which also serves its description, intention, concern and triggers. *Proposal:* a handling code or grant mode that serves only `name` and `role` of a Part.
4. **A practitioner's reading cannot carry the lens.** *Resolved in 0.1.0-draft.2:* LA-7 is retired and I5 applies `agentInterpretation` to agent and software authors only; a therapist listed in `interpretationAuthors` of the active adoption may read through the lens.
5. **Every record is "trauma-adjacent".** The lens defaults put `trauma-adjacent` on every record, so a part about checking figures counts as trauma-adjacent, a grant cannot exclude exile material by category, and every recall cue must be written by the person (RC-2). *Proposal:* lens default categories `["mental-health"]`; `trauma-adjacent` through `defaults.perConstruct` for `ifs/exile` and `ifs/burden`; the checker derives a Part's categories from its `role`.
6. **`Part.role` is not checked.** Any string passes, including `ifs/self`, although the Self is not a part in this lens. *Proposal:* a rule that `role` is a construct of the Part's lens, and a construct flag (for example `notAPartRole`) for `ifs/self`.
7. **The suggestion condition leaves no trace.** "The person asked for ways of looking at an inner conflict" (`suggestionRequires`) has no place in the records, and an `agent-suggested` adoption passes without it. *Proposal:* an `agent-suggested` adoption cites the Episode, Source or message where the person asked (for example in `derivedFrom`); the checker warns when it is missing.
8. **Therapy confidentiality does not reach the Practice.** LA-4 (`therapy-confidential` means `person-only`) travels only through an `adoption` field. Practice and AssessmentRecord have none, so a practice brought from therapy is served under a lens grant (checked: `pr-01` is served while `la-01` is withheld). *Proposal:* an optional `adoption` on Practice (route `from-lens`) and on AssessmentRecord, with LA-4 applied to them; or apply LA-4 to every record tagged with a lens (`lens` or `source.lens`) while the person's active adoption of that lens is `therapy-confidential`, and warn when such a record is not `person-only`.
9. **Records on a proposed adoption are served.** With an `agent-suggested` adoption and no admit Review, the adoption itself is withheld, but `part-01` and `pr-01` stay active and are served under the lens grant, and the checker gives no warning (checked). The admission gate can be bypassed by simply writing the lens records. *Proposal:* lens records whose `adoption` is not active inherit the adoption's computed admission (`proposed`); the checker warns (for example W-LA-ADM) when a lens-tagged record cites a non-active adoption.
10. **The vault is never verified.** The L1 checker does not open the vault: a Source whose file is missing, or whose `size` or `sha256` is wrong, passes (checked: `size` 999 and a missing file still give a valid L1). A wrong hash later breaks erasure and step-up checks silently. *Proposal:* a check option (for example `--vault`) that resolves `vaultPath` relative to the context folder and verifies existence, size and hash, reporting a missing file as a warning; and run it over the published examples, which now ship their bytes.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
