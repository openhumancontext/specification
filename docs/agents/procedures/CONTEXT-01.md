# CONTEXT-01 / 0.1.0 — Write a minimal context (L0) with a person

**Procedure · 0.1.0 · normative-draft module `core` · 9 October 2026.** Write a minimal Open Human Context with the person it is about: one JSON file, a subject and a few claims in the person's own words.

## Use when

A person wants to start a context, or wants to give their agents a small, portable description of goals, boundaries, preferences and current state. No other procedure is needed first.

## Inputs

- The person, present and willing. A context is written *with* them, not about them.
- A place the person controls where the file will live. By default the person is the holder.
- Optional: the [quickstart](../../guides/QUICKSTART.md) and [Ilse's example](../../../examples/ilse-minimal/context.json) as a shape.

## Steps

1. **Explain the boundary.** Tell the person what the file is for and that nothing in it leaves without a grant they give. With no grant, nothing is disclosed to anyone but them.
2. **Write the manifest.** `format: "ohc.context"`, `specVersion: "0.1.0-draft"`, an `id` the holder controls (`urn:uuid:…` is recommended), a `version` string, and `subject.id`. Add `displayName` only if the person wants it. Keep everything else out of `subject`: statements belong in claims.
3. **Ask, then write each statement as a Claim.** Use the six required fields: `id`, `facet`, `text`, `origin: "declared"`, `assertedBy: "subject"` and `recordedAt`. Keep the person's words in `text`. Choose the `facet` (goal, boundary, preference, state, need, declared-value …) and, if it helps, a `predicate`. Add a `horizon` when it is clear; give a `state` claim a `valid.until`.
4. **Read every claim back.** The person confirms or corrects it. Before the file is saved, correct the draft. After it is saved, a correction is a new claim that supersedes the old one; the old one stays in history.
5. **Keep gaps as gaps.** When the person chooses not to define something, write an absence (`{"code": "not-chosen", "intentional": true}`), not a guess and not a default.
6. **Do not add yourself.** Do not write your own observations or conclusions into this file. Anything you inferred is not `declared`. Proposing an inference is [CONTEXT-02](CONTEXT-02.md) and needs a grant.
7. **Mark sensitive content.** If the person states something about health, beliefs, relationships or similar, add the matching `categories`. Such claims are sensitive or special by default, and the file keeps that default.
8. **Check the file.** Run `python3 tools/check.py <file> --level L0 --json`. Fix every error. Tell the person which defaults the checker applied.
9. **Hand it over.** Tell the person where the file is, and that they can change, contest, export or erase anything in it.

## Output and completion

A single-document context that passes the checker at L0, in which every claim is in the person's words and was confirmed by them. The check shows that the file is well-formed. It does not show that the content is true or that the person agreed; the person's confirmation in step 4 is what matters.

## Missing information

If the person does not know or does not want to answer, record nothing or an absence with the right code (`unknown`, `not-asked`, `not-chosen`). Never fill a gap from elsewhere.

Do not invent a person; use only what the person said or granted.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
