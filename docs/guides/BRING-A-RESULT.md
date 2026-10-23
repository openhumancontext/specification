# Bring a test result to your agent

**Guide · informative · 0.1.0-draft.2 · 12 October 2026.** For a person who took a test, keeps its report, and wants
their own agent to see the result and work with them in its light. Five steps; then you do nothing. The rules behind
this guide are the module [Instrument import](../../spec/INSTRUMENT-IMPORT.md); if you are the agent, follow
[CONTEXT-10](../agents/procedures/CONTEXT-10.md). На русском: [BRING-A-RESULT.ru.md](BRING-A-RESULT.ru.md).

The worked example is [Tove](../../examples/tove-bring-a-result/), a fictional person who brings a BFI-2 report. In
this release you can bring a BFI-2 result this way (its catalog entry carries an `import` block,
[LENSES.md §7.4](../../spec/LENSES.md#74-instruments)). For other tests, the lens recipes in
[docs/lenses/](../lenses/) describe how to record a result by hand.

## The five steps

**1. Tell your agent what you have.** "I have my test report." The first time, your agent asks to set up two things,
and does so only if you say yes: a folder for your context, private to your user account, with its holder key next
to it, and one step in its own settings so that it starts every session with what you allow. Keep the folder and the
key out of your agent's file tools. Then a separate window opens. It is yours: it talks only to you. Add your PDF
there; it stays yours, and you can always open it.

**2. Get the numbers in.** Your agent fills a short draft from a report you give it: one number per scale, the date
you took the test, the norm group. If you give it the PDF, the whole file passes through your agent, the report's
text included. To pass only the numbers, give it a screenshot of the score page, or type the numbers in your window.
What the report does not show stays empty; nothing is guessed.

**3. Check, and say what fits.** In your window, once per report: "yes, as on my report". Then: it fits · parts fit
(mark which scales fit and which don't; the rest stay unsaid) · not sure · I dispute it · it doesn't fit · later. Add your own words if you like. A sentence
about how your agent should work with you goes with the result; answer "no" to "keep it with this result?" and it
stands on its own.

**4. Look at what your agent may see and do, and confirm.** Everything is ticked; untick what you don't want:

- each result and your words;
- offer guesses about you, each only as a guess you keep or drop;
- weigh results you accepted when it proposes something for you, naming what it weighed;
- keep notes between sessions.

Each comes with an example. Next to each result, in plain words: what the test can and cannot tell, and the ways of
working your agent receives with it. The screen shows, word for word, what your agent will be told it may do; `p`
shows the text your agent will receive. Confirming the whole screen is your agreement.

**5. Change your mind at any time.** Untick something, fix a number, dispute a result, choose other ways of working,
erase a result or a report. Unticking and erasing reach your agent at its next message; other changes, at the start
of its next session.

*After that you do nothing: your agent starts each session with what you allowed, also after you change your mind.
It says each guess as a guess, you keep or drop it, and it keeps only what you kept. It never puts your results into
anything others use to decide about you; you can share your own report yourself.*

## What the screen looks like

Tove's screen at step 4, as the reference holder printed it (shortened; the full screen is
[window-3-agree.txt](../../examples/tove-bring-a-result/expected/window-3-agree.txt)):

```text
What "Personal agent" may see and do · for personal assistance · until 9 April 2027
Sees — each result is ticked; untick what you don't want
 [x] 1. BFI-2 · Big Five (Five-Factor Model) · 5 scales · you said parts fit: Openness, Conscientiousness, … fit; Extraversion does not; …
       with your words: "When you lay out options, show me the evidence behind each one."
       ways of working: basic (OHC editors) · change them with the playbooks command
     [x] Also seen, not about a test: "Give me the decision first, in one paragraph."
May do — each is ticked; untick what you don't want
 [x] a. Offer guesses about you from these results. For example: …
 [x] b. Weigh results you accepted when it proposes something for you. For example: …
 [x] c. Keep notes between sessions, until 9 April 2027. …
Never, whatever you tick: put your results into anything others use to decide about you (hiring, allocating or
evaluating your work, promotion, ranking you against others, credit or insurance); …
About the tests
 1. BFI-2
    Measured, with independent research behind it.
    Can help with: self-reflection on typical tendencies; choosing communication preferences you then state.
    Does not show: what you will do in a given moment; any clinical condition; job fit.
    Protected like mental health data.
What your agent will be told you agreed to (written by this program; your agent gave no words of its own): "…"
[ p: show what my agent will receive ]   [ ok: confirm ]
```

## Ways of working

A lens can come with **ways of working** (playbooks): short guidance on how to use the lens, and the results you
accepted, in everyday situations such as planning the week, choosing between options, preparing a hard conversation,
giving feedback or looking back at something that happened. Each public lens comes with one basic set, written by the
OHC editors from the lens's own model and tools ([LENSES.md §2.2](../../spec/LENSES.md#22-playbooks-format-ohcplaybook)).

- Your agent receives them with the result, grouped by situation, marked with what your agreement allows. They are
  guidance for your agent, never rules about you; what you say now always comes first.
- The `playbooks` command lets you choose others for that lens, or none. Your coach's or therapist's own way of working
  can be added; it is kept only in your context.
- A step that offers a guess is skipped when you unticked guesses; a step that weighs a result is skipped when you
  unticked weighing.

## What stays closed whatever you tick

Everything on the screen is open by default, because it is about you and your own agent. Some limits are not yours or
your agent's to open, because they protect you from decisions others make about you
([SPECIFICATION §8.10](../../spec/SPECIFICATION.md#810-prohibited-purposes-closed)): hiring and choosing between
candidates, allocating work, evaluating performance, promotion, ranking you against others, credit or insurance,
tailoring persuasion or advertising to you, inferring your political views, reading your emotions at work or in study,
selling your data or training models for others, and decisions with a significant effect on you made without a
person. Most of them rest on law (the GDPR and the EU AI Act); a few OHC holds stricter than the law, or without a
named legal basis yet ([COMPOSITION.md](../../spec/COMPOSITION.md#legal-hooks)). Your own choices, such as which role
to take, are not among them. If your employer or school runs the agent, the screen opens with nothing ticked: you tick
only what you want.

## Try it

The reference holder program is a terminal approximation of your window. From the repository root, with Python 3.9+
and `jsonschema`, Tove's whole session runs again in a scratch folder:

```sh
python3 -B tools/tests/tove_session.py examples/tove-bring-a-result --out "$(mktemp -d)"
```

Then open `<folder>/example/expected/`: what Tove saw in her window and what her agent received. What her agent
receives at the start of a session:

```sh
python3 tools/ohc_holder.py serve examples/tove-bring-a-result/context --for a-01 --purpose assist-personal \
  --now 2026-10-13T07:00:00Z --id prj-0001 --no-log
```

With your own report, in your own terminal (your agent fills `draft.json` with `template` and tells you the command):

```sh
python3 tools/ohc_holder.py setup ~/my-context --subject urn:ohc:person:<your name>
python3 tools/ohc_holder.py bring ~/my-context --draft draft.json --report report.pdf
python3 tools/ohc_holder.py agree ~/my-context --grantee a-01 --purpose assist-personal
```

`review`, `withdraw`, `correct`, `erase` and `playbooks` change things later; `--help` after a command says what it
does. The window talks only to a terminal and refuses without one. It is not a lock: an agent that opens a terminal of
its own could still type into it, which is why your agent's procedure forbids it. The program keeps your folder
private to your user account; an agent that runs as you can still read it, so keep it out of your agent's reach.

## What this guide does not promise

That a result is true of you, that a test is valid for what you use it for, or that an agent behaves as agreed. The
standard records what you brought, what you said about it and what you allowed; your agent's runtime does the rest.

---
Copyright 2026 Taras Pustovoy and contributors. Licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
