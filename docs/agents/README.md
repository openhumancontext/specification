# Work with a person's context

**Agent entry · informative · 0.2.0 · 12 October 2026.** This is the entry point for agents that read, write or hold Open Human Context (OHC). A procedure is an instruction for a result; the schemas and the [specification](../../spec/SPECIFICATION.md) define the file contract.

OHC gives you a person's context only through a **projection**: what one grant allows, for one purpose, at one time. Everything you write about the person that they did not say themselves is a **proposal** that the person decides on. Nothing in a context is a verdict about who the person is.

## Before any task

1. Read the [consumer obligations](CONSUMER-OBLIGATIONS.md) C-1…C-12. They apply to every procedure.
2. Know your grant: its status, purposes, actions, mode, interpretations policy, source tier, storage, `decisionUse` and expiry.
3. Know what you may not do with any grant: the prohibited purposes in [§8.10 of the specification](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed).

Recall is not crisis support. A consumer's crisis protocol always takes precedence; recall MUST NOT delay, replace or condition it.

## Procedures

| ID / version | When to use | Prerequisites | Result / completion | Maturity |
|---|---|---|---|---|
| [CONTEXT-01 / 0.1.0](procedures/CONTEXT-01.md) | Write a minimal context (L0) with a person | The person is present and wants a context; you can write a file they control | A single-document context that passes the checker at L0; every claim in the person's words and confirmed by them | normative-draft (`core`) |
| [CONTEXT-02 / 0.1.1](procedures/CONTEXT-02.md) | Propose an inference correctly | A grant with `suggest` and `infer`, a purpose, and grounds you can cite; the `governance` module declared and you listed as a Party | A stored Proposal with inferred items that carry grounds, alternatives (at least one non-psychological) and limits; or a correct refusal with nothing stored | normative-draft (`core`, `governance`) |
| [CONTEXT-03 / 0.2.0](procedures/CONTEXT-03.md) | Read a projection and keep C-1…C-12; start a session from the holder's rendering | A projection served under a grant that is `given`, or its rendering at session start | Use that respects labels, freshness, handling, storage, `decisionUse` and the separation of statements from readings; playbooks followed only within the grant; use reported where requested | normative-draft (`governance`) |
| [CONTEXT-04 / 0.1.1](procedures/CONTEXT-04.md) | Request verbatim source access | A grant with `open-verbatim`, `maxSourceTier: verbatim` and step-up | A confirmed or declined step-up; verbatim content used once, cited by span, not stored | normative-draft (`governance`) |
| [CONTEXT-05 / 0.1.0](procedures/CONTEXT-05.md) | Offer recall under a RecallCue | An active cue authorised by the person; a grant with `recall` and purpose `recall-support` | An offer made within the cue's timing, with alternatives, and its outcome reported; or no offer | experimental (`recall`) |
| [CONTEXT-06 / 0.1.1](procedures/CONTEXT-06.md) | Import from GUM; refuse or quarantine affect | A GUM snapshot, an importer configuration naming the subject, and the person's agreement to import | Imported claims as proposals with lineage; affect drawn from behaviour refused, other affect quarantined; the person decides what stays | normative-draft (`binding.gum`) |
| [CONTEXT-07 / 0.3.0](procedures/CONTEXT-07.md) | Bind a person's grant into an ODE package | An ODE employee package and a grant for that employee's Party | An `externalDependencies` entry naming the grant and an `ohc.binding` extension; no context values and no projection in the package | normative-draft (`binding.ode`) |
| [CONTEXT-08 / 0.3.0](procedures/CONTEXT-08.md) | Suggest or adopt a lens, including one not in the catalog, and choose its playbooks | A lens descriptor, or the person's or practitioner's own description of their framework; for a suggestion, a grant with `suggest` naming the lens | A LensAdoption with the right route, uses, interpretation settings and playbooks, admitted by the person; a local stub descriptor when the lens is not in the catalog | normative-draft (`lenses`); catalog entries experimental |
| [CONTEXT-09 / 0.1.1](procedures/CONTEXT-09.md) | Keep your model of your person reconcilable with theirs | You work with one person over time under a grant with `suggest` and `infer` | Batch reviews at the cadence the person set; a renewal the person gives in person before the grant expires; nothing extended or assumed | normative-draft (`core`, `governance`) |
| [CONTEXT-10 / 0.1.0](procedures/CONTEXT-10.md) | Help a person bring a test result through their own window | The person hands over a report of a test whose instrument entry has an `import` block; a holder window the person controls | An imported result the person reviewed, the report in their vault, one grant they confirmed on the agreement screen, and a session start that renders it | normative-draft (`instrument-import`) |

These are routes, not a pipeline. Most tasks need only one procedure plus the consumer obligations. Every procedure ends where its result is checked; a passing check does not show that you behaved correctly at run time.

## Tools

- `tools/check.py`: the read-only checker. It never prints field values and never reads vault content.
- `tools/ohc_holder.py`: a reference holder in the terminal, the person's window: `setup`, `bring`, `review`, `agree`, `withdraw`, `correct`, `erase` and `playbooks` open only in the person's own terminal and refuse when an agent runs them; `serve --render agent` is the session-start step and `notices` the per-prompt step ([CONTEXT-10](procedures/CONTEXT-10.md), [CONTEXT-03](procedures/CONTEXT-03.md)).
- `tools/ohc_query.py`: temporal queries ("as known at", "as understood at", "when did my view change") and `project --grant --purpose` to see what a grant serves. `--now` defaults to the current UTC time (`--now latest` uses the newest time in the context, for reproducible examples) and is echoed on stderr. `project` needs `--holder-key-file` for any context that is not synthetic; the published example key is used only for synthetic examples. `--own-proposals` shows a proposer view. A grant with schema or grant-rule errors is refused as `not-granted`.
- The [MCP binding](../../spec/bindings/MCP.md): experimental tools, including a gumcp-compatible `get_user_context`.
- The [exchange messages](../../spec/EXCHANGE.md): requests, proposals, feedback, step-up, notices (experimental).

## Fictional examples

[Ilse](../../examples/ilse-minimal/) (L0), [Mara](../../examples/mara-l1-agent/) (L1, episode-first, with a persistent study companion), [Noa](../../examples/noa-episode-first/) (L2, episode-first), [Kofi](../../examples/kofi-gum-ode/) (GUM import, an assessment import and an ODE employee) and [Tove](../../examples/tove-bring-a-result/) (L2, a test result brought through her own window) are synthetic. Use them as shapes, never as facts about a real person.

## Maintenance

Each procedure has an ID and a semantic version. A change to its steps or meaning increments its version. Procedures change independently of the format version; the format changes only when its own contract changes.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
