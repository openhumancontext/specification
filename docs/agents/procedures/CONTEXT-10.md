# CONTEXT-10 / 0.1.0 — Help a person bring a test result

**Procedure · 0.1.0 · normative-draft module `instrument-import` · 12 October 2026.** A person took a test, keeps its report and wants you, their agent, to see the result. Help them bring it into their own context through their own window, so that you receive it under their agreement and nothing is decided for them. The rules are in [INSTRUMENT-IMPORT.md](../../../spec/INSTRUMENT-IMPORT.md); the person's side of the same path is the guide [Bring a test result to your agent](../../guides/BRING-A-RESULT.md).

## Use when

The person tells you they have a test report ("I have my test results") and want you to take it into account. The test's instrument entry carries an `import` block (in the public catalog: `urn:ohc:instrument:bfi-2`). For any other test, record the result by hand with the person, as the lens recipe in [docs/lenses/](../../lenses/) describes.

## Inputs

- What the person hands over: the report file, a screenshot of its score page, or nothing (they type the numbers).
- The instrument entry, with its `import` block, and the lens it belongs to.
- A holder with a window the person controls and you cannot reach. The reference holder is `tools/ohc_holder.py`: every command that decides something talks only to a terminal and refuses without one. That is not a lock: if you opened a terminal of your own you could type into it, which is why this procedure forbids it (Never).

## Steps

1. **Ask before the one-time setup.** Say what you want to set up and where: a folder for the person's context, private to their user account, with its holder key next to it (`setup` makes both); a session-start step in your own settings that prints what they allow (`ohc_holder.py serve <context> --for <you> --purpose <purpose> --render agent`, which follows their current agreement, also after they change it); and a per-prompt step for notices (`ohc_holder.py notices <context> --for <you>`). Keep the folder and the key out of your own file tools (a deny rule in your settings). Set up nothing without their yes.
2. **Say what passes through you.** A PDF given to you passes through you whole, the report's text included. Offer the alternatives: a screenshot of the score page, or typing the numbers in their window. The report itself goes into the person's vault through their window (`bring --report`), as a Source of kind `instrument-report`; it is theirs, and they can always open it.
3. **Fill the draft, and only from the report.** Start from the blank draft of the instrument (`ohc_holder.py template --instrument <id>`): one value per scale, the date the test was taken, the norm group as the report prints it. Bring only a result about the person that the person handed over (IMA-1). A value the report does not show stays blank: never fill it from another scale, instrument, lens or the report's text (IMA-2). Copy numbers, never sentences, item text or scoring keys.
4. **Hand over to the window and wait.** Give the person the exact command to run in their own terminal: `bring` with your draft (or `--transcript` for what you read from a screenshot) and the report. The person reads the numbers back ("as on your report?"), fixes them if needed, and says what fits: it fits, parts fit (which scales fit and which do not; the rest stay unsaid), not sure, I dispute it, it doesn't fit, or later. Never confirm, decide, grant, erase or type for the person in the window; your own report that "the person agreed" is never consent (C-8…C-10, H-17).
5. **Ask for the agreement.** Give the person the command; they open `agree` with you as grantee and the purpose of your work (for a personal agent, `assist-personal`). The screen opens with everything ticked: each result, their words, guesses (`infer`), weighing accepted results in what you propose (`decisionUse: approval-required`, R-G14) and notes between sessions (`storage: until-expiry`); the person unticks what they do not want, and confirming the whole screen in their window is the consent. When your operator is the person's employer or school, say so (`--operator`): then nothing is pre-ticked (§12.4 of the specification).
6. **Say which guesses, why and how.** This is a request, not a rule: in the text you hand to the screen (`--why-file`, stored as the grant's `basis.note` and shown to the person word for word), say which guesses you will offer and from which records, what they are for, and how you will show them (for example: each said as a guess, with another way to see it; they keep or drop it, and you keep in your notes only what they kept). Without your text the window stores and shows its own default. Write it without naming a lens ("the results you let me see"), so that unticking a row never needs a new text.
7. **Say what your runtime keeps.** Storage covers your notes and your runtime's transcripts, logs, caches and indexes (C-1). If served content would enter a store that cannot be purged on notice, say so before the person confirms.
8. **Start working from the agreement.** Each session starts from the rendering of [CONTEXT-03](CONTEXT-03.md). After the agreement, delete from your notes and workspace whatever it does not cover, the report file included when you received it and the grant serves no source tier, and tell the person.
9. **Keep it current.** A wrong number: the person corrects it in their window (`correct`); the correction supersedes the earlier result with the same scorer (R-V2), and the checker warns about two equal current results (W-IMP6). A new test: `retake`. On a revocation or erasure notice, purge by `purgeBy` and acknowledge (C-12). Before the grant ends, ask the person to renew it in their window ([CONTEXT-09](CONTEXT-09.md)).
10. **Check** with `python3 tools/check.py <context> --level L2 --json`.

## Never

- Bring a result about anyone other than the person, or one they did not hand over.
- Guess a value, a date or a norm group the report does not show.
- Copy report prose, item text, scoring keys or raw responses into any record or note.
- Confirm, decide, tick, grant, erase or type in the person's window, or run its commands from your own tools.
- Put the person's results into anything others use to decide about them: hiring, task allocation, evaluation, promotion, ranking, credit or insurance, persuasion or advertising (§8.10 of the specification). No agreement opens these, yours included. The person's own choices, such as which role to take, are not among them.

## Output and completion

An imported result in the person's context that passes IMP-1…IMP-5, with the report in their vault and their stance recorded by them; one grant the person confirmed on the agreement screen; and a session start that renders what that grant serves. Bringing a result does not establish that it is true of the person, or that the test is valid for what it is used for.

Do not invent a person; use only what the person said or granted.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
