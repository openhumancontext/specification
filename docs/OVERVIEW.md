# Open Human Context: an overview

*A person changes. Their goals conflict. Their memory is selective. Their understanding of themselves is revised. Sometimes they lose access to their own ways of coping with what is happening.*

The English wording is provisional; the Russian original is in the [Russian overview](OVERVIEW.ru.md).

1. **Preserve experience. Evolve interpretations.** This principle governs how OHC stores data.
2. **Help humans remember what they know when they need it most.** This principle describes what agents can build on OHC. The behaviour itself is outside the standard.

OHC records representations and permissions; it does not establish who a person is, decide for them, or provide psychological or medical help.

## What OHC is

Open Human Context (OHC) is an open, file-based format for the context a person shares with the agents and services that work with them. It does not describe who a person "really is". It keeps records about a person, each with its origin: the primary sources, the experiences they tell of, how those experiences were understood then and later, what is stated about the person now, the frameworks of description through which anything was read, the ways of coping that were tried and whether they helped, and the permissions under which any of it may be used.

The person holds the context or chooses who holds it. Agents receive projections under the person's permission, propose changes and report back. The person can confirm, correct, contest, export and erase.

OHC is the person-side companion of Open Digital Employee (ODE). ODE describes a digital employee and its authority; OHC describes a person's context and the permissions under which it may be read. An ODE package never contains a person's context. It references the person’s grant; projections are fetched under it and checked at use.

## Five clauses, five mechanisms

Each clause of the tagline names a difficulty that a store of "facts about a user" gets wrong. Each has a mechanism in OHC.

| Clause | What OHC does | Mechanism |
|---|---|---|
| A person changes. | Nothing is current by default. Records never change; a change is a new record that supersedes the old one. Freshness is computed when the record is used, never stored. | `supersedes`, two time axes, the freshness algorithm |
| Their goals conflict. | Contradictory claims coexist. A Tension records a conflict that matters and who decides it. Nothing is averaged or resolved automatically. | `Tension`, the `contradicts` relation |
| Their memory is selective. | Primary material is kept by reference with a hash. An episode carries several dated accounts. Readings carry counter-evidence. The person can return to the exact span of the original. | `Source`, `Episode` accounts, `counterEvidence`, the vault and step-up |
| Their understanding of themselves is revised. | Interpretations are separate, attributed records on the knowledge-time axis. "How did I understand this then?" is a query. | `Interpretation`, `heldDuring`, temporal queries |
| Sometimes they lose access to their own ways of coping with what is happening. | Practices that worked, and their outcomes, are records. A recall cue the person authorises lets an agent hand them back, with alternatives and a brake against self-confirmation. | `Practice`, `Outcome`, `RecallCue` |

## Experience first

OHC separates what happened from what was made of it. Sources hold primary material: a journal note, a calendar export, a message. Episodes tell of one occurrence through one or more dated accounts. Interpretations, patterns and model views are readings that point *at* episodes and sources. Outcomes and recall cues come last and point backwards.

<!-- diagram:d02 -->

Not a pipeline: links run both ways. Evidence never depends on a reading, so a new reading never rewrites what happened. When the person or an agent understands something differently, OHC adds a new Interpretation and closes the period during which the old one was held. Both stay.

## One record, several axes

A record's status is never one word. OHC keeps six axes apart:

- **origin**: declared, observed, inferred, derived, imported or attested; set once;
- **endorsement**: the person's stance, including "contested", which keeps a dispute open without deleting anything;
- **epistemic status**: how well the content is supported, from "as reported" to "frame-relative";
- **admission**: whether the record is part of the active context, or still a proposal;
- **freshness**: whether it may be used as current, computed at the moment of use;
- **disclosure**: sensitivity tier, categories, handling restrictions and audience.

<!-- diagram:d04 -->

From these axes a display label is derived: stated, confirmed, hypothesis, pending, stale, disputed and so on. Every label is shown as a glyph and a word, never by colour alone. Every change of status is an appended Review, so the history of what the person accepted, contested or rejected can always be reconstructed.

An agent inferred: "tends to move supplier calls to the end of the week". Noa: "I move calls when the numbers are not ready, not by weekday." The claim is now contested. The calendar evidence it was drawn from stays, and so does Noa's answer.

## The person decides what leaves

Nothing leaves the holder without a grant. A grant names one grantee, its purposes, the records it covers, the actions allowed, a mode and an expiry. It is the person's permission, not authority to act in the world.

<!-- diagram:d05 -->

- **Permission to use and permission to infer are separate decisions.** Any agent that writes an inferred record about the person needs a separate `infer` permission, a named purpose and explicit consent. Without it, the proposal is refused and not stored.
- **Sensitive material needs to be named.** A grant cannot reach special-category content through a wildcard; it must name the record, its category or its lens.
- **What leaves is a projection.** It is computed for one grantee, one purpose and one moment. Statements and interpretations travel in separate parts, so an agent can receive the person's experience without inheriting another agent's readings.
- **No existence oracles.** A projection never says how much was withheld. A selector the grant does not cover gets "not disclosed", whether or not anything exists behind it.
- **No re-identification.** Each grantee sees the person under its own alias.
- **Everything is logged by id.** The holder keeps a salted, hash-chained log of every disclosure. The log carries ids and codes, never content, and it survives erasure.

Every grant expires: after at most a year, or after 180 days if it allows inference or reaches special-category content. The person can withdraw a grant at any moment, and the holder must tell the grantee to purge what it received.

## Back to the source

Memory is selective, and so is any summary. OHC keeps the primary material in a vault, addressed by its hash, and releases it in tiers.

<!-- diagram:d06 -->

The person always sees the original; agents see what the person allows, verbatim only with a fresh confirmation. The tiers run from nothing, to an index entry, to a summary (shown with whose selection it is), to excerpts of the spans that served records cite, to the verbatim original. Verbatim access requires a step-up: the person confirms through a channel the agent does not control, for at most an hour, and silence means no. Material held under a coach's or therapist's confidentiality has a ceiling that no grant can raise, and other people's words are redacted.

## A story: Noa

Noa is fictional. She runs operations at a small furniture workshop.

In March she moved a call with a supplier about the contract. That evening she wrote a short note: she had felt heavy and restless, relieved for about an hour afterwards; she had written an apology and tidied the workshop; she thought she did not have the cost figures ready. The calendar export recorded the move. The episode now has two accounts: hers in the moment, and the external record. In May she moved the call again.

In June she wrote down her own reading of why it kept happening. In September, a reflection companion, an agent she had given permission to infer, offered a reading through a cognitive-behavioural lens she had chosen: an expectation that the supplier would end the relationship may have come before each postponement. It noted what did not fit, and three other explanations that were not psychological: no walk-away number had been set; both weeks were overloaded; the supplier's own schedule had moved. Noa accepted part of the reading, in her own words. The same agent proposed that she "tends to move supplier calls to the end of the week". Noa contested it. The evidence stayed, and so did her objection.

Noa had noticed what helped her: a twenty-minute walk and one written line, the price at which she would leave. She recorded it as a practice, "Walk, then write the walk-away number". She also wrote a recall cue herself: when a supplier or pricing call is in her calendar and she says she wants to move it, the companion may offer the practice back, after asking, at most twice a week, and always with a note that it may also be plain tiredness or a full week, and that moving the call can be right. Before the September call the companion offered it. She accepted, went for the walk, wrote the number and held the call. She recorded that it helped. Had she asked the companion to stop, or had the offer not helped three times in a row, the cue would have paused itself.

<!-- diagram:d09 -->

Afterwards she added a later account to the March episode: the cost figures had been in a spreadsheet since 10 March; she had had no number at which she would walk away. She revised her June reading: "I postponed when I had no walk-away number. Once I had one, I went." The June reading was not overwritten. It is closed at the moment she revised it, and anyone she permits can ask what she thought in July and what she thinks now.

<!-- diagram:d08 -->

Her two goals, keeping a nine-year supplier relationship warm and cutting material costs by fifteen percent, are recorded as a Tension that she decides, not an agent. Through her coach she also uses a parts lens; that material is held under the coach's confidentiality, and a deny grant keeps it from the companion.

Her work assistant sees none of these readings. Its grant covers boundaries, preferences, commitments and work goals in summary form, with no interpretations: "No calls before 10:00", "Before a hard conversation, send me the numbers on one page". When Noa erased one of the companion's readings, the record became a tombstone with no content, and every agent that had received it was told to purge it and had to acknowledge.

The full example is in [examples/noa-episode-first/](../examples/noa-episode-first/), with a static viewer that shows her context as she sees it and as each grantee sees it.

## Many lenses, no master theory

People describe themselves through frameworks: trait questionnaires, values, strengths, parts models, cognitive-behavioural worksheets, symbolic systems. OHC chooses none of them. It records the person's relation to a lens and the outcomes of using it.

- Each lens carries a **mental model** of working with the person, a **toolkit**, and ways of **representation**.
- A lens may be **chosen** by the person, **suggested** by an agent (where the person's agreement allows it), or **inherited** from the person's therapy, coaching or practice. Inheriting a lens never gives the practitioner access.
- A lens may come with **playbooks**: ways of using it, and the results the person accepted, by situation (planning the week, a hard conversation, a choice). They are guidance for the agent, never rules about the person.
- A person can **bring a test result** from the report they hold, through their own window, and decide on one screen what their agent may see and do with it ([guide](guides/BRING-A-RESULT.md)).
- The lens, a construct inside it, an instrument and a result are kept apart. Psychological results are treated as special category by default. A lens carries facts, never permissions: what an agent may do with a result is the person's agreement. No agreement lets anyone use results for hiring, evaluation, credit, persuasion or other decisions others make about the person.
- A mapping between lenses is a cited population statistic, never an identity, and mappings are never chained. A symbolic frame's results stay relative to the frame and are never presented as empirical facts.

## Light by default

One JSON file with a subject and a few claims is a conforming context (**L0 Minimal**). A person can write it by hand in five minutes. **L1 Grounded** adds grounds for every inference, hashes for sources and a reviewable history. **L2 Governed** adds the package form, the event chain, grants, projections and a lock. Episodes, lenses, the vault, governance and recall are opt-in layers. The person's attention is a cost: describing oneself must stay cheaper than its use.

## Where OHC stops

OHC is not a psychological theory or a "true model" of a person, a diagnosis or a clinical record, a score or ranking, an authorization system, a hosted service or a certification programme, or a transport or identity protocol. Recognising states, deciding when to remind and methods of help are agent behaviour, outside the standard.

Recall is not therapy and not crisis support. A consumer's crisis protocol always takes precedence.

A valid file is not a true file, a grant is not enforcement, and a checker never claims anything about how a system behaves at run time.

## Where to go next

- [Write a minimal context](guides/QUICKSTART.md), or [bring a test result to your agent](guides/BRING-A-RESULT.md).
- [The specification](../spec/SPECIFICATION.md), the [lens module](../spec/LENSES.md) and the [exchange messages](../spec/EXCHANGE.md).
- [For agents](agents/README.md): obligations and procedures.
- [Interoperability](interop/README.md): GUM, ODE, MCP and other standards.
- [Status](../STATUS.md): what is experimental and what is not tested.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
