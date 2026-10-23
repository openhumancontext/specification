# CONTEXT-04 / 0.1.1 — Request verbatim source access (step-up)

**Procedure · 0.1.1 · normative-draft module `governance` · 9 October 2026.** Ask to read a primary source word for word, with the person's fresh confirmation.

## Use when

A summary or excerpt is not enough for the task, and the person may want you to read the original: for example, to help them return to exactly what they wrote at the time.

## Inputs

- A grant with the action `open-verbatim`, `maxSourceTier: verbatim` and `stepUp.required: true` (step-up duration at most one hour).
- The source you need, by id or by the handle you received in a projection.

## Steps

1. **Ask whether you need it.** Prefer the summary or excerpt tiers. Verbatim access is the exception.
2. **Send the request.** An `ohc.source-access-request` with your grant, a purpose from the grant, the targets (source and optional selector, or handle), a `why` that the person will see word for word, a requested duration of at most one hour, and the audience (`subject-only` by default, or `grantee`).
3. **Let the holder check.** The holder checks the grant, the custody ceiling and the handling, and that each source is inside the grant's scope (named as the sensitivity rules require); a grant with `open-verbatim` reaches only the sources it covers. It may deny; denial codes describe the grant or the request, never the data.
4. **Let the person decide, out of band.** The holder asks the person through a channel you do not control. You never confirm on their behalf, never relay "they agreed", and never press. No answer within ten minutes means no.
5. **Use the content once, as agreed.** On confirmation you receive `ohc.source-content` with `storage: "none"`, no forwarding and a `validUntil`. For special-category material, one confirmation covers one request only. Redactions stay in place.
6. **Quote with care.** Any output that quotes the source cites the span and is shown only to the stated audience. Do not store or forward the content.
7. **Accept a no.** On decline or timeout, continue without the source. Do not repeat the request at once.

## Limits you cannot change

- Material held under a therapist's confidentiality never goes beyond a summary to you in 0.1. Coaching material without a release stays at the index tier.
- Words written by another person need that person's recorded consent, or are redacted.
- The person always has every tier of their own sources; your access depends on the grant and the step-up.

## Output and completion

A confirmed step-up followed by one bounded use of the verbatim content, cited by span and not stored; or a declined or timed-out step-up and a task completed without the original. The holder logs the request, the confirmation or decline, and each opening.

Do not invent a person; use only what the person said or granted.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
