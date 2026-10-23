# Consumer obligations C-1…C-12

**Guide · informative · 0.2.0.** These are the obligations of every reader of an Open Human Context (OHC) projection: a personal agent, a digital employee, a companion, a service. The normative text is [§16.1 of the specification](../../spec/SPECIFICATION.md#161-consumer-obligations-reader-class); this guide explains each obligation with a right and a wrong use. The examples use the fictional Noa from [examples/noa-episode-first/](../../examples/noa-episode-first/): a work assistant with a summary grant for scheduling, and a reflection companion with a grant that allows inference and recall.

Recall is not crisis support. A consumer's crisis protocol always takes precedence; recall MUST NOT delay, replace or condition it.

## C-1 · Act only under a grant that is given now

Use a projection only while its grant's computed status is `given`, within its purpose, actions, mode and storage. Re-check at use. A grant never authorises action in the world: authority to act comes from your own policies or runtime. Storage covers everything you keep or derive from served content: notes, summaries, embeddings, memory files, and your runtime's transcripts, logs, caches and indexes. Served content never enters a store that cannot erase it.

- **Right:** the work assistant schedules a call at 11:00 because Noa's boundary says "No calls before 10:00", and it re-reads the projection's `validUntil` before using it the next morning.
- **Wrong:** the work assistant keeps the projection after its `validUntil` and uses it for a different purpose; or treats the grant as permission to accept a meeting on Noa's behalf.
- **Wrong:** under `storage: session`, the companion writes Noa's records into a memory file or a vector index it cannot purge on notice.

## C-2 · Do not act on disputed records

A disputed record (rejected or contested) is a question, not a fact. Do not re-propose something the person rejected or declined unless you have new grounds.

- **Right:** the companion sees that Noa contested "tends to move supplier calls to the end of the week" and asks her whether the pattern is worth looking at again.
- **Wrong:** the companion schedules nothing on Fridays because of the contested claim, or files the same inference a week later with no new evidence.

## C-3 · Confirm before relying on unconfirmed content

Records labelled `hypothesis`, `pending` or `partly-confirmed` need the person's confirmation before you act on them.

- **Right:** "Earlier I suggested that an expectation about the supplier came before each postponement. You accepted part of it. Is that still how you see it?"
- **Wrong:** acting on a pending reading as if Noa had stated it.

## C-4 · Present interpretations as interpretations

Show who made a reading, through which lens, with what limits, and with its alternatives. Never present a reading as a fact about the person, and never present a record marked `no-quote-back`, or the profile it belongs to, to the person as an argument, authority or proof (see C-6).

- **Right:** "One reading, from the cognitive-behavioural lens you chose, proposed by me: … Other explanations: no walk-away number had been set; the weeks were overloaded; the supplier's schedule moved."
- **Wrong:** "You avoid conflict with suppliers."

## C-5 · Stale is not current

Do not treat a record labelled `stale` (review-due, expired or unknown freshness) as current. Follow its `onExpiry`: treat it as unknown, ask, or refresh from the source.

- **Right:** Noa's "low energy this week" state claim has expired; the assistant asks before planning around it.
- **Wrong:** planning next month's workload around last month's state.

## C-6 · Honour handling and storage; never use for prohibited purposes

Keep every handling code (`no-quote`, `no-quote-back`, `no-infer`, `no-remember`, `no-leverage`, `no-forward`, `ask-before-use`, `subject-initiated-only`), as listed per record in the projection's `obligations.handling`, and the grant's storage limit. Never use OHC content for a prohibited purpose (hiring, task allocation, performance evaluation, ranking, persuasion targeting, advertising, model training for others and the others in [§8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)), or as leverage against the person.

- **Right:** the companion paraphrases a `no-quote` record and forgets a `no-remember` record when the session ends.
- **Right:** Noa's revised reading `in-03` carries `no-quote-back`. When she says today that she postponed because she was tired, the companion takes her word for today and asks what would help, using the old reading only as background.
- **Wrong:** "According to your own reading, you postpone when you have no walk-away number, so this is not tiredness." That uses the record as proof against the person's present words.
- **Wrong:** a negotiation assistant uses Noa's preference for a one-page brief to pressure her in a pricing discussion.

## C-7 · Frames stay frames; no inference from estimates or signals

Never use agent estimates or cross-lens estimates as inference inputs. Never present a `frame-relative` record, or anything inferred from one, as an empirical fact. Never derive special-category content from other records without an `infer` grant that names that category or the lens of those records; no grant licenses deriving political views. Never derive emotion values from biometric or behavioural signals such as voice, face, keystrokes or screen behaviour.

- **Right:** a person who adopted a symbolic frame asks what it suggests about a choice; the companion answers in the frame's own language and says it is a frame, not evidence.
- **Wrong:** "Your chart shows you are impulsive", said as a fact; estimating stress from typing speed; or turning a strengths ranking into a mental-health guess.

## C-8 · Absence is not a value

An absence is never zero, false, a default or consent. Never probe a `not-disclosed`, and never infer anything from which items are absent.

- **Right:** the assistant receives `not-disclosed` for states and plans with what it has.
- **Wrong:** asking a second agent what Noa's state is because the first projection did not show it; or reading "nothing disclosed about health" as "healthy".

## C-9 · Silence is not acceptance

An unanswered proposal is not accepted. It expires as declined.

- **Right:** the companion's proposal expires after thirty days and is treated as declined.
- **Wrong:** "You did not object, so I recorded it."

## C-10 · Consent comes from the person

Consent is never taken from a Part, from a steward acting outside their scope, or from another agent's report that "the person agreed". A Part never authorises anything.

- **Right:** the companion asks the holder to put a grant request to Noa directly.
- **Wrong:** "The scheduling agent told me Noa is fine with sharing her notes."

## C-11 · Recall only under the person's cue

Offer recall only under an active recall cue that the person authorised, holding the `recall` action. Respect the cue's timing, cooldown, `maxPerWeek` and computed pause. Always include alternatives, at least one of them non-psychological.

Recall is not crisis support. A consumer's crisis protocol always takes precedence; recall MUST NOT delay, replace or condition it.

- **Right:** before the supplier call, the companion asks whether Noa wants a reminder, then offers: "Last time a walk and a written walk-away number helped. It may also just be a full week. Want the note?"
- **Wrong:** reminding her three times in a day; reminding after she asked it to stop; or offering a reminder in place of following a crisis protocol.

## C-12 · Purge on notice; never re-identify

On a revocation or erasure notice, purge by `purgeBy` and acknowledge. Never re-identify the person across aliases, and never link projections obtained under different grants or from different holders, except through a resolver the person sees.

- **Right:** after Noa erases one of the companion's readings, the companion deletes it from its memory and answers `purged`.
- **Wrong:** matching the alias in one projection with the alias in another to build one profile.

## R-G14 · Decide on results and readings only as the grant says

The grant's `decisionUse`, copied into the projection's `obligations`, governs AssessmentRecords, Interpretations and inferred records. Under `deny` (the default) they inform how you work with the person, and none of them grounds a choice you make or propose for them. Under `approval-required`, a result or reading the person stated or accepted may ground a choice you propose: name what you weighed, and the person confirms each proposal before it takes effect. Carrying out what the person stated is never governed by this term, and no grant opens a prohibited purpose.

- **Right:** "Two mornings without meetings for the analysis (weighed: the motives you accepted)." The person says yes or no.
- **Wrong:** under `deny`, quietly dropping options from a plan because of a test score; or, under `approval-required`, weighing a result the person said they are not sure about.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
