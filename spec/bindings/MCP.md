# MCP binding

Module `binding.mcp` · format `0.1.0-draft` · **experimental**. No conformance claim may rely on this binding.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as described in BCP 14 (RFC 2119,
RFC 8174) when, and only when, they appear in all capitals.

This binding describes an MCP tool surface for a holder: one tool compatible with GUM's MCP server
(`get_user_context`) and eight native tools that carry the exchange messages of [EXCHANGE.md](../EXCHANGE.md). The
tool input schemas are in [mcp/tools.json](mcp/tools.json).

A tool call is never authority to act in the world (R-G9), and a tool result is never consent.

## 1. The gumcp-compatible tool

**Exact signature.**

```python
get_user_context(query: str | None = "", start_hh_mm_ago: str | None = None, end_hh_mm_ago: str | None = None) -> str
```

`start_hh_mm_ago` and `end_hh_mm_ago` bound the time window as durations before now, in hours and minutes (`HH:MM`),
as their names indicate. Either may be omitted.

**Behaviour.**

- The tool requires an authenticated caller Party and a `given` grant with purpose `assist-personal` or
  `gum-export`. With no Party or no grant, it returns `""` (the empty string), and nothing else. When the grant is
  valid and nothing matches, it returns gumcp's own sentence, `No relevant context found for the given query and time
  window.`, which says nothing about what exists outside the grant.
- It runs the grant evaluation (`SPECIFICATION.md` §12.3), keeping Claims only, and excludes:
  - `proposed`, `rejected`, `contested`, `stale` (expired) and `special` records;
  - `person-only` records;
  - interpretation-layer records.
- It selects at most **3** items, ranked by lexical relevance to `query` and filtered by `recordedAt` within the time
  window.
- It never emits the subject id, a subject-named id or raw record ids. It uses only the pairwise alias and per-call
  handles.
- It logs a `projection-served` Event with the ids of the records served.

**Output format** (one block per item, in the layout of GUM's MCP server). Every line is built from the record **as
the grant's mode serves it** (§12.3, step 10), never from stored fields the mode withholds:

```text
• <text>
  Reasoning: <the served rationale | "Declared by the person." | "[withheld]" | "Inferred; reasoning withheld.">
  Confidence: <raw 1-10 if from GUM, else round(value*10)>
  Relevance Score: <0.00-1.00>
  Supporting Observations:
    - [ohc] <excerpt>
```

- `Reasoning` is the rationale when the mode serves it. Otherwise it is `Declared by the person.` only when the record
  is `declared` and asserted by the subject; `[withheld]` when a rationale exists but the mode (`summary`,
  `rule-only`) withholds it; and `Inferred; reasoning withheld.` for any other record.
- The `Confidence` line appears only when the mode serves a confidence.
- `Supporting Observations` and its lines appear only when excerpts are served (a grant with `cite-excerpt`, at the
  `excerpt` tier). When nothing is served there is no header.

Differences from gumcp, which a client may notice: the relevance score is lexical, the observation lines carry the
`[ohc]` prefix instead of an observer name, and the reasoning line can say that reasoning is withheld.

## 2. Native tools

Each native tool carries one exchange message. The holder applies the same rules as for the message.

| Tool | Message equivalent |
|---|---|
| `ohc_get_projection(grant, purpose, select, mode?, as_of?, without_interpretations?)` | `request` → `projection` or `denial` |
| `ohc_answer(grant, purpose, question, answer_form, choices?)` | `answer-request` → `answer` |
| `ohc_propose(grant, purpose, items, rationale, requests?)` | `proposal` → `proposal-result` or `denial` |
| `ohc_give_feedback(grant, purpose, about, feedback_kind, outcome?)` | `feedback` |
| `ohc_request_source_access(grant, purpose, targets, why, duration)` | `source-access-request` (step-up follows) |
| `ohc_open_source(grant, handle)` | Returns `source-content` after step-up. |
| `ohc_report_use(grant, purpose, projection, used_records, decision_ref?)` | `use-report` |
| `ohc_list_my_grants()` | Returns the caller's own grants only. |

**Rules for every tool.**

- Each call carries exactly one purpose (R-G7), except `ohc_list_my_grants` and `ohc_open_source`, whose purpose is
  the one confirmed in the step-up.
- Results that withhold something use `not-disclosed` and never counts (H-5).
- `ohc_open_source` returns content with `storage: "none"`; the caller MUST NOT keep it beyond the confirmed
  duration.
- A holder MUST NOT accept a step-up confirmation through any tool of this surface. Confirmation is out-of-band
  (SU-2).

## 3. Pins (informative)

- MCP protocol revision: `2025-11-25` **[verify]**. The tool surface uses only tool listing and tool calls, so it is
  expected to work with earlier and later revisions; this has not been tested.
- GUM's MCP server, whose tool this binding mirrors: `gumcp` 1.0.0, read at commit
  `6afbcf9fd0f441a104b6ec6252d2163979fc0a61`.
- Nothing in this binding has been run against a live MCP client.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
