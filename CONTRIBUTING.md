# Propose a change

People and agents are welcome. Use English for issues, pull requests and comments.

Submit proposals and problems in [openhumancontext/specification](https://github.com/openhumancontext/specification/issues/new/choose). The forms are kept in `.github/ISSUE_TEMPLATE/`:

- `01-proposal.yml`: propose a change;
- `02-problem.yml`: report a problem;
- `03-lens-descriptor.yml`: propose or correct a lens descriptor.

## How to write a proposal

- Submit one independently decidable point per proposal.
- Name the draft version or commit and the affected section, rule id, object kind, catalog code, glossary id or file.
- Explain the problem with a concrete example. Suggest a change or a verification case if you have one; a complete solution is not required.
- Keep the layers apart: evidence and experience, statements, interpretations, outcomes and permissions are different records in OHC. A proposal that merges them needs a strong reason.
- Separate observed evidence from assumptions, and file checks from runtime trials. A passing check is not evidence of behaviour.
- Use stable glossary ids. English is the reference language; translations are reviewed separately.

Posting a proposal does not change the standard. Changes to normative semantics require a new specification version; released catalogs, lens descriptors and procedures change their own versions.

## Contributing a lens

A lens is a framework of description: a theory, a frame or a way of representing information. Lens descriptors follow [LENSES.md](spec/LENSES.md). A lens contribution:

- **Describes, in your own words.** Summaries, constructs and the mental model are written in OHC's own words. Never include item text, report prose, scoring keys or raw proprietary responses.
- **Grades every citation.** Each citation carries an evidence grade: `F` (primary source read), `F2` (secondary source), `U` (unverified) or `verify`. Grades below `F` stay visible wherever the descriptor is shown.
- **Separates the evidence axes.** The measurement tier of the constructs, the practice tier per delivery context (clinician-delivered, self-guided, agent-offered) and the ontological status are separate fields. Agent-offered delivery is always `not-assessed` in 0.1.
- **Records intellectual property honestly.** Name trademarks and their owners, the licence of the items, whether scoring is public, and whether the constructs may be listed or only referenced by URL. Use marks nominatively. Every 0.1 entry keeps `legalReviewNeeded: true` until counsel reviews it.
- **Asks the lineage first.** A living contemplative tradition is named only with written consent from its lineage holders (`ip.lineageConsent`). Without that consent, use a generic description that names no tradition.
- **Carries facts, not permissions.** Psychological lens results are treated as special category by default (`defaults`), and the descriptor says what the lens supports and does not establish. What an agent may suggest, infer or decide is the person's grant, never the descriptor; the prohibited purposes bind every grantee without being restated.
- **May bring a playbook.** Ways of using the lens by situation, written from its own mental model and toolkit ([LENSES.md §2.2](spec/LENSES.md#22-playbooks-format-ohcplaybook)): guidance, never a rule about the person, with no item text, score bands or claims of effect.

## Examples

Examples are **synthetic only**. Use fictional people, mark them "(fictional)", set `synthetic: true` on the context and on every content record (governance records carry no `synthetic` field), and give third parties pseudonymous role labels ("Supplier contact", "Coach"). Never use, paraphrase or allude to a real person's life, messages or records, including your own.

## Do not submit

- personal data, health information or private messages about anyone;
- credentials, tokens or keys;
- internal conversations, private project names, local file paths or e-mail addresses;
- material you are not authorised to publish under the licence of the affected file ([license map](LICENSING.md)). Identify third-party sources and their licensing constraints.

## Releases

- Only the tree exported by `python3 tools/build_release_manifest.py --export DIR` is ever published. It contains exactly the files in the release manifest and is initialised as a fresh Git repository with a neutral author; the working repository and its history are never pushed (REL-7).
- The release check scans every exported text file for private paths, hosts, e-mail addresses, credentials and internal design-section ids (REL-5). Project-specific private markers are not kept in the repository: they live in an untracked denylist (`.release-denylist.json`, or the file named by `OHC_DENYLIST`), and the release step fails closed when it is missing.

## Agents

Agents use the same forms as people. Include the agent name and the responsible submitting account or person. [AGENTS.md](AGENTS.md) has the reading order and the rules agents follow when they work with contexts.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
