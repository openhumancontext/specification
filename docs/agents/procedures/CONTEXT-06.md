# CONTEXT-06 / 0.1.1 — Import from GUM; refuse or quarantine affect

**Procedure · 0.1.1 · normative-draft module `binding.gum` · 9 October 2026.** Bring the propositions of a General User Models (GUM) instance into a person's context as proposals, keep their lineage, refuse affect drawn from behaviour, and quarantine any other affect content. The binding itself is specified in [bindings/GUM.md](../../../spec/bindings/GUM.md); this procedure is the route through it.

## Use when

A person has a GUM instance that observed their screen, calendar or other activity, and wants its propositions in their context where they can inspect, correct and control them.

## Inputs

- A GUM snapshot: the `observations`, `propositions` and `observation_proposition` tables (SQLite or JSON).
- An importer configuration `{subjectId, gumInstanceId, digestOnly}`. The subject comes **from this configuration only**; GUM has no subject column, and the subject is never guessed from the data.
- The person's agreement to import. If anyone other than the person runs the import, that writer needs a grant with `write` or `suggest` and `infer`.

## Steps

1. **Run the importer.**

   ```sh
   python3 tools/convert_gum.py import <snapshot> --config importer-config.json --out <package> [--previous <package>] [--digest-only]
   ```

2. **Know what it produces.**
   - One `import-run` Event per snapshot, and `importedFrom` on every record.
   - Observations become Sources with opaque ids and a default `maxRelease` of `index`. GUM does not keep capture time, so `capturedAt` is absent; the GUM creation time goes to `formulatedAt`. Screen observers become `screen-observation` Sources. With `--digest-only`, no vault object is stored.
   - Propositions become Claims with facet `other`, the proposition text verbatim, `origin: inferred`, `assertedBy` the GUM agent Party, `epistemic: hypothesis`, and admission `proposed`. GUM's 1–10 confidence becomes `value = raw/10` with `semantics: support-score`; a missing confidence stays absent, never 0. Creation and update times go to `formulatedAt` and `lastEvidenceAt`. Raw GUM ids and other columns are kept under `ext["gum.import"]`.
   - Category `third-party` is added when other people are named.
3. **Refuse or quarantine affect.** A proposition about affect, mood, stress or mental condition that rests on a screen or other behavioural observation is refused: it is not imported, whatever its wording, and the importer reports only how many were refused (R-X4). Any other such proposition is quarantined: tier `special`, category `mental-health`, handling `no-infer` and `person-only`, so only the person sees it (R-X3). When the classifier is uncertain, it refuses or quarantines. If the person wants to say how they feel, they say it themselves, as a declared claim.
4. **Keep lineage on re-import.** With `--previous`, a proposition missing from the new snapshot gets a `retract` Review by the GUM Party; a revised proposition in the same revision group supersedes the old one. Nothing is deleted.
5. **Let the person decide.** Nothing imported is active until the person reviews it: admit, decline, endorse, contest or reject. A classifier may propose a separate, more specific claim; it never rewrites an imported one.
6. **Check the package.** `python3 tools/check.py <package> --level L2 --json`.
7. **Export back only under a grant.** An export to GUM needs a grant with purpose `gum-export` to the GUM instance's Party, and records are selected by the grant evaluation under it. Outside a synthetic example, pass the holder key with `--holder-key-file`. Only active records go out; never declined, retracted, rejected or contested records, special-category records, records with `no-infer`, `person-only` or `no-forward`, frame-relative records, or readings unless the grant allows all interpretations.

   ```sh
   python3 tools/convert_gum.py export <package> --grant <grant-id> --mode A|B --out <dir> [--holder-key-file <file>]
   ```

## Output and completion

A package in which every imported proposition is a proposed, inferred Claim with its evidence, lineage and original columns preserved; affect drawn from behaviour is refused and other affect content is quarantined; and the person's decisions are recorded as Reviews. The checker passes at L2. Whether the propositions are true is not established by the import.

Do not invent a person; use only what the person said or granted.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
