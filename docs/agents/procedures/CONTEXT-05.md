# CONTEXT-05 / 0.1.0 — Offer recall under a RecallCue

**Procedure · 0.1.0 · experimental module `recall` · 9 October 2026.** Hand a person back their own experience (a practice that helped, an episode, their own reading) at a moment they described in advance, with their permission.

Recall is not crisis support. A consumer's crisis protocol always takes precedence; recall MUST NOT delay, replace or condition it.

Recall is not therapy. Recognising states, deciding when to remind and methods of help are your own behaviour, outside OHC. This procedure covers what the data allows.

## Use when

The situation described in an active recall cue seems to be happening, and you hold a grant that allows recall.

## Inputs

- An active RecallCue: admitted by the person, not paused. If any target is special-category, mental-health or trauma-adjacent, the cue must have been written by the person themselves, not just accepted.
- A grant with the action `recall` and the purpose `recall-support`, whose scope covers the cue's targets.
- Target episodes whose recall permission is `ask-each-time` or `permitted`.

## Steps

1. **Crisis first.** If there is any sign of crisis, follow your crisis protocol. Do not offer recall instead of it, before it, or as a condition of it.
2. **Match the trigger.** Use only the signals the cue lists (calendar events, words in the person's own messages, their request, time of day, task type). Never physiological or biometric signals.
3. **Check timing.** Respect `notWhen`, the cooldown since the last offer, `maxPerWeek`, and the cue's computed pause. A cue pauses after the person asks to stop, or after three offers in a row that did not help or made things worse; only the person resumes it.
4. **Ask before reminding,** when the cue says so. Silence means no.
5. **Fetch only what you need.** Request a projection for the targets with purpose `recall-support`. Use nothing above the cue's `maxTier`; a cue never reaches verbatim.
6. **Offer, do not instruct.** Use the cue's framing, close to the person's own words. Always include the cue's alternatives note, with at least one non-psychological explanation (tiredness, load, health, circumstances). Make it easy to say no.
7. **Report what happened.** Send `feedback` with an Outcome about the cue: when, what you presented, your wording and the person's response (accepted, declined, deferred, asked to stop). Whether it helped is the person's rating; any rating you add is labelled as your estimate.
8. **Stop when asked.** After "stop", make no further offers under that cue.

## Output and completion

Either an offer made within the cue's timing and limits, with alternatives, and its outcome reported; or no offer, because a condition was not met. Both are complete results.

Do not invent a person; use only what the person said or granted.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
