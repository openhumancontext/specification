"""Shared set-up for the draft.2 tool tests: a small test registry and an empty person's package.

The registry copies two published lens descriptors and their instruments, brought to the draft.2 shape (only
``crossLensMapping`` in ``useLimits``, no ``adoption.agentSuggestion``), gives each instrument an ``import`` block and
each lens one playbook written for these tests. It overrides the published entries for the test only, so the tests
run the same before and after the registry itself is upgraded. People and numbers are synthetic.
"""

import copy
import os

import helpers

from ohclib import jsonio, vocab
from ohclib.package import Package

AT = "2026-10-12T09:00:00Z"
LATER = "2026-10-13T07:00:00Z"
BIG_FIVE = "urn:ohc:lens:big-five"
HEXACO = "urn:ohc:lens:hexaco"
BFI2 = "urn:ohc:instrument:bfi-2"
HEXACO_PI = "urn:ohc:instrument:hexaco-pi-r"

BLOCKS = {
    BFI2: {"scoredBy": {"partyKind": "organization", "id": "urn:ohc:scorer:bfi-2-report", "label": "Report scorer"},
           "scores": [{"kind": "raw", "range": [1, 5]}],
           "scales": ["big-five/O", "big-five/C", "big-five/E", "big-five/A", "big-five/N"]},
    HEXACO_PI: {"scoredBy": {"partyKind": "organization", "id": "urn:ohc:scorer:hexaco-report",
                             "label": "Report scorer"},
                "scores": [{"kind": "percentile", "range": [0, 100], "integer": True}],
                "scales": ["hexaco/H", "hexaco/E", "hexaco/X", "hexaco/A", "hexaco/C", "hexaco/O"],
                "normGroups": [{"id": "test-norms", "label": {"en": "Test norms", "ru": "Тестовые нормы"}}]},
}


def playbook(lens, name, tool, results):
    short = lens.rsplit(":", 1)[-1]
    return {
        "format": "ohc.playbook", "specVersion": "0.1.0-draft", "id": "urn:ohc:playbook:%s-basic" % short,
        "version": "0.1.0", "name": {"en": "%s: basic ways of working" % name, "ru": "%s: базовые способы" % name},
        "lenses": [lens], "author": "OHC editors", "sources": [], "licence": "CC-BY-4.0",
        "situations": [
            {"id": "plan-week", "when": {"en": "Planning a week", "ru": "Планирование недели"},
             "use": {"en": ["Ask which two outcomes matter most this week.",
                            "Where a tendency they accepted fits, shape the plan with it and say which one."],
                     "ru": ["Спросить, какие два результата важнее всего на этой неделе.",
                            "Где принятая склонность подходит, строить план с её учётом и назвать её."]},
             "toolkit": [], "results": results},
            {"id": "look-back-at-an-episode",
             "when": {"en": "Looking back at an episode", "ru": "Взгляд назад на эпизод"},
             "use": {"en": ["Ask what happened, in their words.",
                            "Offer the fit check on one tendency they accepted."],
                     "ru": ["Спросить, что произошло, их словами.",
                            "Предложить проверку соответствия по одной принятой склонности."]},
             "toolkit": [tool],
             "watchFor": {"en": "A score is a dated reading against a norm group, never a verdict on the episode.",
                          "ru": "Балл — датированное измерение, а не приговор эпизоду."}}]}


def upgraded(doc, playbooks):
    doc = copy.deepcopy(doc)
    doc["version"] = "0.2.0"
    doc["useLimits"] = {"crossLensMapping": (doc.get("useLimits") or {}).get("crossLensMapping",
                                                                            "population-level-only")}
    (doc.get("adoption") or {}).pop("agentSuggestion", None)
    doc["playbooks"] = list(playbooks)
    return doc


def write_registry(dest):
    """A registry directory overriding big-five, hexaco, bfi-2 and hexaco-pi-r; returns a Spec resolving it."""
    root = os.path.join(dest, "registry")
    spec_root = os.path.join(helpers.repo_root(), "spec")
    books = {BIG_FIVE: playbook(BIG_FIVE, "Big Five", "big-five.fit-check", ["big-five/C", "big-five/E"]),
             HEXACO: playbook(HEXACO, "HEXACO", "hexaco.fit-check", ["hexaco/C"])}
    for lens, name in ((BIG_FIVE, "big-five"), (HEXACO, "hexaco")):
        doc = jsonio.load_json(os.path.join(spec_root, "lenses", name + ".lens.json"))
        jsonio.write_pretty(os.path.join(root, "lenses", name + ".lens.json"), upgraded(doc, [books[lens]["id"]]))
        jsonio.write_pretty(os.path.join(root, "playbooks", name + "-basic.playbook.json"), books[lens])
    for instrument, name in ((BFI2, "bfi-2"), (HEXACO_PI, "hexaco-pi-r")):
        doc = jsonio.load_json(os.path.join(spec_root, "instruments", name + ".instrument.json"))
        doc["version"] = "0.2.0"
        doc["import"] = copy.deepcopy(BLOCKS[instrument])
        jsonio.write_pretty(os.path.join(root, "instruments", name + ".instrument.json"), doc)
    return vocab.Spec(registries=[root])


def new_package(dest, spec, words=("Give me the decision first, in one paragraph.",)):
    """An empty L2 package of a synthetic person with their own agent ``a-01`` and some words of theirs."""
    package = Package(dest, spec)
    package.create({
        "format": "ohc.context", "specVersion": "0.1.0-draft", "id": "urn:ohc:example:test-person:context",
        "version": "2026-09-15.1", "subject": {"id": "urn:ohc:example:test-person", "displayName": "Test (fictional)"},
        "holder": "subject", "lang": "en", "created": "2026-09-15T09:00:00Z",
        "conformance": {"level": "L2", "modules": ["core", "governance", "lenses"], "subjectIsAdult": True},
        "parties": [{"id": "a-01", "partyKind": "agent", "label": "Personal agent"}],
        "policy": {"admission": "subject-only", "resolver": "returnDialog"}, "synthetic": True})
    for index, text in enumerate(words, 1):
        package.add("Claim", {"assertedBy": "subject", "facet": "preference", "id": "c-%02d" % index,
                              "kind": "Claim", "origin": "declared", "recordedAt": "2026-09-15T09:05:00Z",
                              "synthetic": True, "text": text})
    package.save("2026-09-15T09:05:00Z")
    return dest


def bfi_draft(spec, **values):
    import import_assessment

    draft = import_assessment.template(spec, BFI2)
    draft["administeredAt"] = values.pop("taken", "2026-09-14")
    draft["form"] = "60"
    scores = dict(values or {"big-five/C": 4.2, "big-five/E": 2.9, "big-five/O": 3.6})
    for entry in draft["scores"]:
        entry["raw"] = scores.get(entry["scale"])
    return draft


def hexaco_draft(spec, **values):
    import import_assessment

    draft = import_assessment.template(spec, HEXACO_PI)
    draft["administeredAt"] = values.pop("taken", "2026-09-20")
    draft["normGroup"] = "test-norms"
    scores = dict(values or {"hexaco/H": 61, "hexaco/C": 74, "hexaco/X": 30})
    for entry in draft["scores"]:
        entry["percentile"] = scores.get(entry["scale"])
    return draft


def write_report(dest, name="report.pdf", body=b"%PDF-1.4\n% synthetic test report, no content\n"):
    path = os.path.join(dest, name)
    with open(path, "wb") as handle:
        handle.write(body)
    return path


def person_with_results(dest, spec, report=True):
    """A person who brought two results: BFI-2 (parts fit, with words) and HEXACO (not sure), and one sentence
    that is not about a test. Returns (package dir, {"bfi": id, "hexaco": id, "words": id, "source": id})."""
    import import_assessment
    from ohclib import window

    pkg = new_package(os.path.join(dest, "ctx"), spec)
    path = write_report(dest) if report else None
    first = import_assessment.import_result(pkg, [bfi_draft(spec)], "2026-10-12T09:05:00Z", report_path=path,
                                            spec=spec, seed="t", synthetic=True)
    second = import_assessment.import_result(pkg, [hexaco_draft(spec)], "2026-10-12T09:06:00Z", spec=spec,
                                             seed="t", synthetic=True)
    bfi, hexaco = first["assessments"][0], second["assessments"][0]
    package = Package(pkg, spec)
    window.record_stance(package, bfi, "parts", "2026-10-12T09:08:00Z", fits=["Conscientiousness"],
                         not_fits=["Extraversion"], words="I am quieter than this says.")
    window.record_stance(package, hexaco, "not-sure", "2026-10-12T09:09:00Z")
    words = window.add_words(package, "When you lay out options, show me the evidence behind each one.",
                             "2026-10-12T09:10:00Z", about=bfi, synthetic=True)
    package.save("2026-10-12T09:10:00Z")
    return pkg, {"bfi": bfi, "hexaco": hexaco, "words": words, "source": first["source"]}


class ScriptedTerminal(object):
    """Answers for the window's dialogue in tests; the command line itself only ever opens /dev/tty."""

    def __init__(self, answers):
        self.answers = list(answers)
        self.said = []

    def say(self, text=""):
        self.said.append(text)

    def ask(self, prompt):
        self.said.append(prompt)
        if not self.answers:
            raise EOFError()
        return self.answers.pop(0)
