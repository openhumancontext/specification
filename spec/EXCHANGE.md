# Exchange messages

Module `exchange` · format `0.1.0-draft` · **experimental**. The message shapes in this document are published under
their own experimental format names (`ohc.experimental.<name>`). No conformance claim may rely on them, and they may
change before they become normative. The one exception is the Projection, which is the normative document
`ohc.projection` defined in `SPECIFICATION.md`.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as described in BCP 14 (RFC 2119,
RFC 8174) when, and only when, they appear in all capitals. Within this experimental module they state what an
exchange endpoint does when it implements a message.

## 1. Scope

The exchange module describes the messages between an **agent** (a grantee, or a party asking to become one) and a
**holder** (the person's own store, a personal agent acting as holder, or a router). It covers:

- asking for and receiving permission (grant request and notice);
- reading (projection request, projection, answer);
- writing back (proposal, proposal result, feedback, use report);
- going back to the source (source access request and source content, with step-up);
- withdrawing and erasing (revocation notice, erasure notice, purge acknowledgement);
- refusing (denial).

**Out of scope:** transport, authentication of either side and message signatures. An implementation chooses them.
Authentication of the requester is assumed by the grant evaluation (step 1 of the algorithm in `SPECIFICATION.md`
§12.3) and is never inferred from message content.

**Events.** Every message that touches content produces the Events listed in §3. Events hold ids, codes and times
only; they never hold text, values, quotes or content digests.

**Feedback from the person is not a message.** The person gives feedback through the holder's own interface. It
becomes Reviews (stance, admission, disclosure) or Outcomes recorded by the subject.

## 2. Common envelope

Every message carries:

```text
{"format": "ohc.experimental.<name>", "specVersion": "0.1.0-draft", "id": "msg-…", "from": Actor, "to": Actor,
 "at": DateTime, "inReplyTo"?: string}
```

| Field | Notes |
|---|---|
| `format` | `ohc.experimental.<name>`, where `<name>` is the message name in §3. |
| `specVersion` | `0.1.0-draft`. Records inside a message inherit it; they never carry their own version. |
| `id` | A message id with the prefix `msg-`. |
| `from`, `to` | Actors: `"subject"`, `"holder"`, or a Party id known to the holder. |
| `at` | RFC 3339 date-time with offset. |
| `inReplyTo` | The id of the message this one answers, when there is one. |

Schemas: `spec/schema/message.schema.json` (the envelope) and one schema per message,
`spec/schema/msg-<name>.schema.json`. The `projection` message is the document validated by
`spec/schema/projection.schema.json`.

## 3. Messages

| # | Message | Direction | Body | Holder behaviour and Events |
|---|---|---|---|---|
| 1 | `grant-request` | agent → holder | `purposes`, `scope`, `actions`, `mode`?, `interpretations`?, `maxSourceTier`?, `requestedExpiresAt`, `why` | The holder shows `why` to the person verbatim. The person decides. Silence means refused after 7 days. Event `grant-request-received`. |
| 2 | `grant-notice` | holder → agent | `status`: `given` \| `refused` \| `deferred`; `grant`? (the stored Grant without `note`) | Events `grant-given`, `grant-request-refused`, `grant-request-deferred`. |
| 3 | `request` | agent → holder | `grant`, `purpose`, `select` [GrantSelector], `asOf`?, `mode`?, `withoutInterpretations`?, `resolver`?, `ownProposals`? | Grant evaluation (`SPECIFICATION.md` §12.3) → `projection` or `denial`. With `ownProposals: true`, the projection also carries the requester's own pending and expired-undecided items (the proposer view, `SPECIFICATION.md` §12.5). |
| 4 | `projection` | holder → agent | the Projection document (`format: ohc.projection`) | Event `projection-served`. |
| 5 | `answer-request` | agent → holder | `grant`, `purpose`, `question` (text, or `{"facet", "predicate"?, "kind"?}`), `answerForm`: `boolean` \| `choice` \| `text` \| `time-window`, `choices`? | Needs the action `answer`. |
| 6 | `answer` | holder → agent | `answer`? (a value or text), `labels` [derived labels of the records used], `code`? = `not-disclosed` | The holder composes answers **only from records that the grant evaluation would serve under the same grant in `full` mode**. When it cannot answer, it always returns `not-disclosed`: an answer is never an existence oracle. Event `answer-served`. |
| 7 | `proposal` | agent → holder | `grant`, `purpose`, `items` [full records], `requests`?, `rationale`, `grounds`?, `expiresAt`? | Check PR-2. On failure: `denial` (`infer-not-granted` or `not-granted`) and **nothing is stored**. Otherwise the holder stores a Proposal and its items as `proposed`. Event `proposal-received`. |
| 8 | `proposal-result` | holder → agent | `proposal`, `items` [`{"id", "admission", "endorsement"?, "contested"?}`], `status`: `stored` \| `refused` \| `decided` \| `expired` | Sent on storage and again on each decision. Only the proposer receives it. |
| 9 | `feedback` | agent → holder | `grant`, `purpose`, `about`: id, `feedbackKind`: `outcome` \| `usage-note` \| `correction-request`, `outcome`? (an Outcome record), `requests`? | Needs the action `suggest`. Outcomes from agents are stored as proposed, as the agent's estimate (O-1). A correction request becomes Proposal `requests`. Event `feedback-received`. |
| 10 | `source-access-request` | agent → holder | `grant`, `purpose`, `targets` [`{"source", "selector"?}`] or [handle], `why`, `requestedDuration` (at most PT1H), `audience`: `subject-only` (default) \| `grantee` | Step-up (§5). Events `source-access-requested`, then `step-up-confirmed` or `step-up-declined`. |
| 11 | `source-content` | holder → agent | `source` (by handle), `tier`, `content` (redacted), `storage`: `"none"`, `validUntil` | Event `source-opened`. |
| 12 | `use-report` | agent → holder | `grant`, `purpose`, `projection`, `projectionDigest`?, `checkedAt`?, `usedRecords` [ids], `decisionRef`? `{"objectId", "version"}` (an ODE Decision), `note`? | Shows the person which items informed which decision. It is where an ODE employee records the projection it used (ODE binding §2). Event `use-report-received`. |
| 13 | `revocation-notice` | holder → agent | `grant`, `status`: `withdrawn` \| `revoked` \| `expired`, `at`, `purgeBy` | MUST be sent on withdrawal or revocation. Event `revocation-notice-sent`. |
| 14 | `erasure-notice` | holder → agent | `records` [ids], `erasedAt`, `purgeBy` | MUST be sent to every counterparty that received an erased record, as recorded by any disclosure Event (`SPECIFICATION.md` §13.1). Event `erasure-notice-sent`. |
| 15 | `purge-ack` | agent → holder | `status`: `purged` \| `not-held` \| `failed`, `at` | Events `erasure-notice-acknowledged`, `purge-receipt-received`. |
| 16 | `denial` | holder → agent | `code` (a reason code), `retryAfter`? | The code never depends on the data. Event `request-denied`. |

**Notes on the messages.**

- **Grant requests** are never stored as Grants. Requested, refused and deferred grants exist only as messages and
  Events. A stored Grant is always a permission the person gave, with `expressedBy` recording how they expressed it.
  An agent's statement that "the person agreed" is never `expressedBy`.
- **Requests** carry exactly one purpose (R-G7). `select` uses GrantSelectors; for every selector the grant does not
  cover, the Projection carries an absence with code `not-disclosed`, whether or not matching records exist. A
  Projection never carries counts.
- **Denial codes** (`spec/catalogs/reason-codes.json`) describe the grant or the request, never the data:
  `not-granted`, `infer-not-granted`, `expired-grant`, `purpose-mismatch`, `special-needs-explicit-consent`,
  `step-up-required`, `step-up-timeout`, `person-only`, `locked`, `quota-exceeded`, `subject-declined`,
  `holder-policy`, `security`, `legal`, `retention`.
- **Use reports** SHOULD be sent whenever a projected item informs a decision, including an ODE `Decision`, so that
  the person can see what was used.
- **Revocation and erasure** notices are obligations of the holder; purging and acknowledging them are obligations of
  the agent (consumer obligation C-12). If no acknowledgement arrives by `purgeBy`, the holder reminds once and shows
  the person the open notice.

## 4. Example: a projection request and a use report

The reflection companion of a synthetic person asks, before a call, for recall support:

```json
{"format": "ohc.experimental.request", "specVersion": "0.1.0-draft", "id": "msg-0310", "from": "a-02", "to": "holder", "at": "2026-09-24T07:30:00Z",
 "grant": "g-02", "purpose": "recall-support",
 "select": [{"kinds": ["Practice", "Outcome"]}, {"kinds": ["Episode"], "contexts": ["work"]}, {"facets": ["relationship"]}],
 "mode": "summary"}
```

The response is a Projection with:

- `statements.practices` ⊇ `pr-01`;
- `experience.episodes` ⊇ `ep-03` (only Episodes whose computed `recall` permits it, because the purpose is
  `recall-support`);
- `recall.outcomes` ⊇ `oc-01`;
- `absences: [{"selector": {"facets": ["relationship"]}, "code": "not-disclosed"}]`, because grant `g-02` does not
  cover relationships;
- **no counts**.

The companion then reports use:

```json
{"format": "ohc.experimental.use-report", "specVersion": "0.1.0-draft", "id": "msg-0311", "from": "a-02", "to": "holder", "at": "2026-09-24T07:32:00Z",
 "grant": "g-02", "purpose": "recall-support", "projection": "prj-0007", "usedRecords": ["pr-01", "ep-03"]}
```

## 5. Source access with step-up

Verbatim access to a primary source goes through the step-up flow defined in `SPECIFICATION.md` §15.4 (rules SU-1 to
SU-7). In message terms:

```text
Agent  ── source-access-request ──▶ Holder
           {grant, purpose ∈ grant.purposes, targets, why (shown to the person verbatim),
            requestedDuration ≤ PT1H, audience: "subject-only" (default) | "grantee"}
Holder: checks the grant (open-verbatim, maxSourceTier verbatim, custody ceiling, not person-only), and that every
        target Source passes SPECIFICATION.md §12.3 steps 3-7 under that grant now; else ── denial
Holder ── out-of-band prompt ──▶ Person   (holder interface or a signed channel the requesting agent does not control)
Person ── confirm / narrow / decline ──▶ Holder   (no answer within PT10M means decline)
Holder ── source-content ──▶ Agent   {redacted verbatim content, storage: "none", validUntil ≤ confirmation + maxDuration}
```

- An agent never confirms a step-up.
- `source-content` is the second, explicitly named channel by which content leaves the holder (`SPECIFICATION.md`
  §12.3). It is gated by the same grant evaluation as a projection, plus the step-up; a source outside the grant's
  scope is refused even when the grant allows `open-verbatim`.
- Verbatim content never enters a Projection and is never stored by the agent.
- Agent output that quotes the content MUST cite the span and show it only to the stated `audience`.

## 6. Proposal inbox (holders that accept proposals)

- **IB-1.** Open proposals are shown to the person grouped by proposer, newest first, with the `rationale`, the
  grounds and the **alternatives** of every inferred item.
- **IB-2.** The person's decision is recorded as Reviews (`admit`, `decline`, `endorse`, `partially-endorse`,
  `reject`, `contest`), applied to each item. A batch decision MAY use one Review with several targets.
- **IB-3.** Silence is not acceptance. At `expiresAt` (default P30D), items still undecided are computed `declined`,
  with reason `expired`: not admitted by the person. The proposer still sees them in its proposer view
  (`SPECIFICATION.md` §12.5).
- **IB-4.** Attention is a cost. A holder SHOULD limit open proposals per proposer; the default limit is 20, and the
  holder refuses more with a `denial` with code `quota-exceeded`. A holder SHOULD batch notifications to the person,
  at most once per day by default, or at the grant's `reviewCadence` when the person set one; a batch review at that
  cadence settles the open proposals together.
- **IB-5.** Proposals that target `locked` records are declined by the holder automatically: a Review `decline` by
  `"holder"` with `reasonCode: locked` (`SPECIFICATION.md` §11.1).
- **IB-6.** Proposals that would create special-tier records, inner-system records or inferred interpretation-layer
  records are decided only by the subject in person (R-A1). No holder policy may admit them.

## 7. What an exchange endpoint must not do

- Serve anything that the grant evaluation does not yield at serve time (H-1), or act after `validUntil` (R-G6).
- Reveal, by an answer, a denial code, a count or a flag, whether records outside the grant exist (H-5).
- Store a proposal that fails PR-2 (H-4).
- Treat a grant, a projection or a message as authority to act in the world (R-G9).
- Take consent from a Part, from a steward outside scope, or from another agent's report (C-10).

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
