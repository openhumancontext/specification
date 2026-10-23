#!/usr/bin/env python3
"""Static viewer for the examples, readable without JavaScript.

Usage:
    python3 tools/render_viewer.py            # (re)writes viewer/
    python3 tools/render_viewer.py --check    # exit 1 when viewer/ differs from a fresh render
    python3 tools/render_viewer.py --out DIR  # render elsewhere
    python3 tools/render_viewer.py --out DIR --home-href ../  # add a link back to an enclosing site

Output, for each example ``examples/<name>/`` (person = the part of <name> before the first hyphen):
- ``viewer/<person>/index.html``: the subject's view, 11 sections;
- ``viewer/<person>/as-<grantee>/index.html``: "view as <grantee>", rendered through the evaluation algorithm
  (SPECIFICATION.md §12.3), with only what the
  grant serves (one page per grantee; a grantee with several allow grants gets one section per grant);
- ``viewer/index.html``: an index.

Everything is computed at the context's latest knowledge time, so the output is deterministic. Pages use inline
CSS with the site's colour tokens (light and dark), no external fonts, scripts or images. Tables scroll inside their
own frame on narrow screens, so the page itself never scrolls sideways. ``--home-href`` (empty by default, so that the
viewer in this repository stays self-contained) adds a link to the site that embeds the viewer, relative to the
viewer's root. A small inline script only reveals
a text filter and a theme toggle; all content is in the HTML.
"""

import argparse
import difflib
import html
import os
import shutil
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)

from ohclib import grants, model, vocab  # noqa: E402

ROOT_CSS = """:root{--ink:#172235;--muted:#546174;--line:#d5deea;--paper:#fff;--wash:#f1f5fb;--night:#102544;--accent:#a3305c;--accent-ink:#7d2346;--accent-wash:#fbeaf0;--ode:#234cec;--ode-wash:#edf1ff;--evidence:#186453;--evidence-wash:#eaf5f0;--reading:#714296;--reading-wash:#f3eef9;--focus:#b96000;--radius:5px;color-scheme:light dark;font-family:Arial,Helvetica,sans-serif;color:var(--ink);background:var(--paper);font-size:16px;line-height:1.6}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ink:#e6edf6;--muted:#a9b6c8;--line:#33465f;--paper:#111c2b;--wash:#18263a;--night:#0b1422;--accent:#f39abb;--accent-ink:#f8c3d6;--accent-wash:#3a1f2c;--ode:#9dbffc;--ode-wash:#1b2c4a;--evidence:#7fd1b5;--evidence-wash:#11302a;--reading:#cfb0ea;--reading-wash:#2a2140;--focus:#ffb35c}}
:root[data-theme="dark"]{--ink:#e6edf6;--muted:#a9b6c8;--line:#33465f;--paper:#111c2b;--wash:#18263a;--night:#0b1422;--accent:#f39abb;--accent-ink:#f8c3d6;--accent-wash:#3a1f2c;--ode:#9dbffc;--ode-wash:#1b2c4a;--evidence:#7fd1b5;--evidence-wash:#11302a;--reading:#cfb0ea;--reading-wash:#2a2140;--focus:#ffb35c}
body{margin:0;background:var(--paper);color:var(--ink)}
::selection{background:var(--accent-wash);color:var(--ink)}
a{color:var(--accent-ink);text-underline-offset:4px}
a:focus-visible,button:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--focus);outline-offset:4px}"""

LAYOUT_CSS = """*{box-sizing:border-box}
html{scroll-padding-top:100px}
.wrap{max-width:1240px;margin:0 auto;padding:0 36px}
.top{position:sticky;top:0;z-index:2;background:var(--paper);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center;justify-content:space-between;min-height:64px}
.brand{font-weight:700;text-decoration:none;color:var(--ink)}
.home{font-size:14px}
.controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center;min-width:0}
.controls input{font:inherit;padding:6px 10px;border:1px solid var(--line);border-radius:var(--radius);background:var(--paper);color:var(--ink);max-width:220px;min-width:0;flex:1 1 140px}
.controls button{font:inherit;padding:6px 12px;border:1px solid var(--line);border-radius:var(--radius);background:var(--wash);color:var(--ink);cursor:pointer}
main{padding-block:32px 64px}
h1{font-size:clamp(36px,4.8vw,63px);font-weight:500;line-height:1.1;letter-spacing:-.02em;margin:8px 0 16px}
h2{font-size:clamp(24px,2.6vw,34px);font-weight:600;line-height:1.2;margin:56px 0 16px;padding-top:16px;border-top:1px solid var(--line)}
h3{font-size:19px;margin:24px 0 8px}
.kicker{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.055em;color:var(--accent-ink)}
.lead{font-size:19px;line-height:1.65;max-width:760px}
.small,.meta{font-size:14px;color:var(--muted)}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px 24px;margin:16px 0;padding:16px;background:var(--wash);border-radius:8px}
.facts div{min-width:0;overflow-wrap:anywhere}
.badge{display:inline-block;padding:2px 10px;border-radius:999px;border:1px solid var(--evidence);color:var(--evidence);background:var(--evidence-wash);font-size:14px;font-weight:700}
.badge.bad{border-color:var(--accent);color:var(--accent-ink);background:var(--accent-wash)}
.label{display:inline-block;white-space:nowrap;font-size:13px;font-weight:700;padding:0 8px;border-radius:999px;border:1px solid var(--line);background:var(--wash);color:var(--ink)}
.label.l-disputed,.label.l-not-accepted{border-color:var(--accent);color:var(--accent-ink);background:var(--accent-wash)}
.label.l-stated,.label.l-confirmed,.label.l-attested,.label.l-observed{border-color:var(--evidence);color:var(--evidence);background:var(--evidence-wash)}
.label.l-hypothesis,.label.l-frame,.label.l-partly-confirmed{border-color:var(--reading);color:var(--reading);background:var(--reading-wash)}
.table-wrap{overflow-x:auto;max-width:100%}
.table-wrap table{min-width:640px}
table{border-collapse:collapse;width:100%;font-size:15px}
th,td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--line);overflow-wrap:break-word;word-break:normal}
th{background:var(--wash);font-weight:700}
ul.records{list-style:none;padding:0;margin:0}
ul.records>li{padding:12px 0;border-bottom:1px solid var(--line)}
details>summary{cursor:pointer;color:var(--accent-ink)}
details dl{display:grid;grid-template-columns:minmax(120px,max-content) 1fr;gap:4px 16px;margin:8px 0 0;font-size:14px}
details dt{color:var(--muted)}
details dd{margin:0;overflow-wrap:anywhere}
.chips{display:flex;flex-direction:column;gap:6px}
.chip{display:block;font-size:14px;line-height:1.4;text-decoration:none;padding:6px 8px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink)}
.accounts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:8px}
.account{border:1px solid var(--line);border-radius:8px;padding:12px;background:var(--wash);min-width:0;overflow-wrap:anywhere}
.account p{margin:6px 0}
.timeline{display:flex;flex-direction:column;gap:14px}
.track{position:relative;height:12px;background:var(--wash);border:1px solid var(--line);border-radius:999px;overflow:hidden}
.bar{position:absolute;top:0;bottom:0;background:var(--reading);border-radius:999px}
.bar.subject{background:var(--accent)}
.bar.agent{background:var(--ode)}
.axis{display:flex;justify-content:space-between;font-size:13px;color:var(--muted)}
.served{border-left:4px solid var(--accent);padding-left:12px}
.note{padding:12px 16px;border-left:4px solid var(--evidence);background:var(--evidence-wash);border-radius:var(--radius)}
footer{border-top:1px solid var(--line);padding-block:24px 48px;font-size:14px;color:var(--muted)}
@media (max-width:1000px){.wrap{padding:0 24px}}
@media (max-width:760px){.wrap{padding:0 20px}}
@media (max-width:440px){.wrap{padding:0 16px}details dl{grid-template-columns:1fr}}"""

SCRIPT = ("(function(){var c=document.getElementById('controls');if(!c)return;c.hidden=false;"
          "document.getElementById('theme').addEventListener('click',function(){var r=document.documentElement;"
          "var t=r.getAttribute('data-theme');var dark=t?t==='dark':window.matchMedia('(prefers-color-scheme: dark)').matches;"
          "r.setAttribute('data-theme',dark?'light':'dark');});var f=document.getElementById('filter');"
          "f.addEventListener('input',function(){var q=f.value.toLowerCase();var els=document.querySelectorAll('[data-filter]');"
          "for(var i=0;i<els.length;i++){els[i].hidden=!!q&&els[i].textContent.toLowerCase().indexOf(q)<0;}});})();")

LABELS = [
    ("not-accepted", "—", "not accepted", "admission is declined or retracted"),
    ("disputed", "⊘", "disputed", "endorsement is rejected, or the record is contested"),
    ("stale", "○", "stale", "freshness is review-due, expired or unknown"),
    ("pending", "…", "pending", "admission is proposed"),
    ("frame", "◇", "frame", "epistemic status is frame-relative"),
    ("stated", "✓", "stated", "declared by the subject"),
    ("confirmed", "✓", "confirmed", "endorsed (including a steward within scope)"),
    ("partly-confirmed", "◐", "partly confirmed", "partially endorsed"),
    ("attested", "●", "attested", "origin is attested"),
    ("observed", "◉", "observed", "observed or derived, and not asked"),
    ("hypothesis", "~", "hypothesis", "everything else (inferred, or imported and not asked)"),
]
LABEL_TEXT = dict((code, (glyph, word)) for code, glyph, word, _rule in LABELS)
HORIZONS = ["foundation", "focus", "state", "none"]
GROUP_TITLES = {"statements": "Statements", "experience": "Experience", "interpretations": "Readings",
                "recall": "Recall", "links": "Links"}
FOOTER = ("Copyright 2026 Taras Pustovoy and contributors. Licensed under "
          '<a href="https://www.apache.org/licenses/LICENSE-2.0">Apache-2.0</a>.')


def esc(value):
    return html.escape("" if value is None else str(value), quote=True)


def label_html(code):
    glyph, word = LABEL_TEXT.get(code, ("~", code))
    return '<span class="label l-%s">%s %s</span>' % (esc(code), esc(glyph), esc(word))


def anchor(rid):
    return "rec-" + "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in rid)


HOME_HREF = ""


def page(title, body, depth, controls=True):
    prefix = "../" * depth
    home = ('<a class="home" href="%s%s">Back to the site</a>' % (prefix, esc(HOME_HREF))) if HOME_HREF else ""
    control_html = ('<span class="controls" id="controls" hidden><label class="small" for="filter">Filter</label>'
                    '<input id="filter" type="search" autocomplete="off">'
                    '<button id="theme" type="button">Theme</button></span>') if controls else ""
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<meta name=\"robots\" content=\"noindex,nofollow\">\n"
            "<link rel=\"canonical\" href=\"./\">\n<link rel=\"alternate\" hreflang=\"en\" href=\"./\">\n"
            "<title>%s</title>\n<style>\n%s\n%s\n</style>\n</head>\n<body>\n"
            "<header class=\"top\"><div class=\"wrap\"><a class=\"brand\" href=\"%sindex.html\">Open Human Context "
            "&middot; example viewer</a>%s%s</div></header>\n<main class=\"wrap\" id=\"main\">\n%s\n</main>\n"
            "<footer class=\"wrap\"><p>All people in these examples are fictional. Generated by "
            "<code>tools/render_viewer.py</code>; nothing here is a real person&#39;s data.</p><p>%s</p></footer>\n"
            "<script>%s</script>\n</body>\n</html>\n") % (
        esc(title), ROOT_CSS, LAYOUT_CSS, prefix, home, control_html, body, FOOTER, SCRIPT if controls else "")


class Example(object):
    def __init__(self, root, name, spec):
        self.name = name
        self.dir = os.path.join(root, "examples", name)
        target = os.path.join(self.dir, "context.json")
        if not os.path.isfile(target):
            target = os.path.join(self.dir, "context", "context.json")
        self.target = target
        self.spec = spec
        self.ctx = model.Context(target, spec)
        self.now = self.ctx.latest_time()
        self.state = model.State(self.ctx, self.now)
        self.person = name.split("-")[0]

    def party_label(self, actor):
        if actor in ("subject", "holder"):
            return actor
        party = self.ctx.parties.get(actor) or {}
        return "%s (%s)" % (party.get("label", actor), actor) if party else actor

    def ref_link(self, rid):
        if rid in self.ctx.by_id:
            return '<a href="#%s">%s</a>' % (anchor(rid), esc(rid))
        return esc(rid)

    def content_text(self, data):
        for key in ("text", "name", "title", "description", "happened"):
            if data.get(key):
                return data[key]
        if "value" in data:
            return "value: %s" % (data["value"],)
        if data.get("absence"):
            return "intentionally absent (%s)" % (data["absence"].get("code"),)
        return ""


def check_badge(example):
    import check

    report = check.run_context(example.target, spec=example.spec)
    if report["valid"]:
        return '<span class="badge">checker: valid &middot; %s met</span>' % esc(report["levelMet"])
    return '<span class="badge bad">checker: %s error(s)</span>' % esc(len(report["errors"]))


# --------------------------------------------------------------------- subject page
def drawer(example, item):
    state, now, data = example.state, example.now, item.data
    status = state.status.get(item.id) or model.Status()
    freshness, since = state.freshness_detail(item.id, now)
    fresh = freshness + (" since %s" % model.format_time(since) if since is not None else "")
    rows = [
        ("origin", data.get("origin")), ("asserted by", example.party_label(data.get("assertedBy"))),
        ("admission", status.admission), ("endorsement", status.endorsement),
        ("contested", "yes" if status.contested else "no"), ("epistemic", status.epistemic),
        ("freshness", fresh), ("sensitivity", state.tier(item.id)),
        ("handling", ", ".join(sorted(state.handling(item.id))) or "none"),
        ("categories", ", ".join(sorted(state.categories(item.id))) or "none"),
        ("recorded", data.get("recordedAt")),
    ]
    if data.get("formulatedAt"):
        rows.append(("formulated", data["formulatedAt"]))
    if data.get("supersedes"):
        rows.append(("supersedes", None))
    refs = [ref for path, ref in model.refs_of(item.kind, data)
            if any(part in path for part in ("/evidence", "/grounds", "/counterEvidence", "/derivedFrom", "/about",
                                             "/between", "/episodes", "/hypotheses", "/targets"))]
    out = ["<details><summary>Details</summary><dl>"]
    for key, value in rows:
        if key == "supersedes":
            out.append("<dt>supersedes</dt><dd>%s</dd>" % example.ref_link(data["supersedes"]))
            continue
        out.append("<dt>%s</dt><dd>%s</dd>" % (esc(key), esc(value)))
    successor = state.successor.get(item.id)
    if successor:
        out.append("<dt>superseded by</dt><dd>%s</dd>" % example.ref_link(successor))
    if refs:
        out.append("<dt>evidence and links</dt><dd>%s</dd>" % ", ".join(example.ref_link(r) for r in dict.fromkeys(refs)))
    history = [r for r in example.ctx.reviews if item.id in model.review_targets(r.data)]
    history.sort(key=lambda r: (r.data.get("recordedAt") or "", r.id))
    if history:
        lines = []
        for review in history:
            note = review.data.get("reasonCode") or ""
            lines.append("%s &middot; %s by %s%s" % (esc(review.data.get("recordedAt")), esc(review.data.get("action")),
                                                     esc(example.party_label(review.data.get("by"))),
                                                     (" (%s)" % esc(note)) if note else ""))
        out.append("<dt>review history</dt><dd>%s</dd>" % "<br>".join(lines))
    out.append("</dl></details>")
    return "".join(out)


def record_li(example, item, extra=""):
    label = example.state.label(item.id, example.now)
    return ('<li id="%s" data-filter data-id="%s">%s <strong>%s</strong> <span class="meta">%s &middot; %s</span>%s%s</li>'
            % (anchor(item.id), esc(item.id), label_html(label), esc(example.content_text(item.data)),
               esc(item.kind), esc(item.id), extra, drawer(example, item)))


def items_of(example, kind):
    out = [i for i in example.ctx.items if i.kind == kind and i.id not in example.state.tombstoned]
    out.sort(key=lambda i: (i.data.get("recordedAt") or "", i.id))
    return out


def section(title, ident, inner):
    return '<section aria-labelledby="%s"><h2 id="%s">%s</h2>\n%s\n</section>' % (ident, ident, esc(title), inner)


def needs_grid(example):
    claims = [c for c in items_of(example, "Claim") if not example.state.superseded(c.id)
              and (example.state.status.get(c.id) or model.Status()).admission in ("active", "proposed")]
    facets = []
    for claim in claims:
        facet = claim.data.get("facet")
        if facet not in facets:
            facets.append(facet)
    if not claims:
        return '<p class="small">No current statements.</p>'
    head = "".join("<th scope=\"col\">%s</th>" % esc(h) for h in HORIZONS)
    rows = []
    for facet in facets:
        cells = []
        for horizon in HORIZONS:
            chips = []
            for claim in claims:
                if claim.data.get("facet") == facet and (claim.data.get("horizon") or "none") == horizon:
                    label = example.state.label(claim.id, example.now)
                    glyph, word = LABEL_TEXT.get(label, ("~", label))
                    chips.append('<a class="chip" href="#%s">%s %s &middot; %s</a>' % (
                        anchor(claim.id), esc(glyph), esc(word), esc(example.content_text(claim.data))))
            cells.append("<td><div class=\"chips\">%s</div></td>" % "".join(chips))
        rows.append("<tr><th scope=\"row\">%s</th>%s</tr>" % (esc(facet), "".join(cells)))
    return ('<div class="table-wrap"><table><thead><tr><th scope="col">facet</th>%s</tr></thead><tbody>%s</tbody>'
            "</table></div>" % (head, "".join(rows)))


def claims_section(example):
    out = ['<ul class="records">%s</ul>' % "".join(record_li(example, c) for c in items_of(example, "Claim"))]
    sources = items_of(example, "Source")
    if sources:
        out.append("<h3>Sources (index)</h3><ul class=\"records\">")
        for item in sources:
            data = item.data
            extra = ' <span class="meta">%s &middot; release up to %s</span>' % (
                esc(data.get("sourceKind")), esc(grants.default_max_release(data)))
            label = example.state.label(item.id, example.now)
            out.append('<li id="%s" data-filter data-id="%s">%s <strong>%s</strong>%s%s</li>' % (
                anchor(item.id), esc(item.id), label_html(label), esc(item.id), extra, drawer(example, item)))
        out.append("</ul>")
    health = items_of(example, "HealthRef")
    if health:
        out.append("<h3>Health pointers</h3><ul class=\"records\">")
        for item in health:
            out.append(record_li(example, item, ' <span class="meta">%s %s, held by %s</span>' % (
                esc(item.data.get("system")), esc(item.data.get("resourceType")),
                esc(example.party_label(item.data.get("custodian"))))))
        out.append("</ul>")
    return "".join(out)


def episodes_section(example):
    out = []
    for item in items_of(example, "Episode"):
        data = item.data
        occurred = data.get("occurred") or {}
        accounts = []
        for account in data.get("accounts") or []:
            parts = ['<div class="account"><div class="kicker">%s</div><div class="meta">%s &middot; narrated %s'
                     " &middot; added %s</div>" % (esc(account.get("accountKind")),
                                                   esc(example.party_label(account.get("narrator"))),
                                                   esc(account.get("narratedAt")), esc(account.get("addedAt")))]
            for key, title in (("happened", "What happened"), ("experienced", "What was experienced"),
                               ("didOrTried", "What was done or tried"), ("understandingThen", "Understood then")):
                if account.get(key):
                    parts.append("<p><strong>%s:</strong> %s</p>" % (title, esc(account[key])))
            parts.append("</div>")
            accounts.append("".join(parts))
        note = ""
        successor = example.state.successor.get(item.id)
        if successor:
            note = ' <span class="meta">superseded by %s; its accounts are kept</span>' % example.ref_link(successor)
        label = example.state.label(item.id, example.now)
        out.append('<article id="%s" data-filter data-id="%s"><h3>%s %s</h3><p class="meta">%s &middot; occurred %s'
                   " &middot; recall %s%s</p><div class=\"accounts\">%s</div>%s</article>" % (
                       anchor(item.id), esc(item.id), label_html(label), esc(data.get("title") or item.id),
                       esc(item.id), esc(occurred.get("start")), esc(example.state.recall(item.id)), note,
                       "".join(accounts), drawer(example, item)))
    patterns = items_of(example, "Pattern")
    if patterns:
        out.append("<h3>Patterns across episodes</h3><ul class=\"records\">%s</ul>"
                   % "".join(record_li(example, p) for p in patterns))
    return "".join(out) or '<p class="small">No episodes.</p>'


def then_and_now(example):
    readings = items_of(example, "Interpretation")
    if not readings:
        return '<p class="small">No readings.</p>'
    starts = [example.state.held_from(r.id) for r in readings]
    start = min(s for s in starts if s is not None)
    end = example.now
    span = max((end - start).total_seconds(), 1.0)
    rows = []
    for item in sorted(readings, key=lambda r: (example.state.held_from(r.id), r.id)):
        held_from = example.state.held_from(item.id)
        held_until = example.state.held_until(item.id)
        left = (held_from - start).total_seconds() / span * 100.0
        right = ((held_until or end) - start).total_seconds() / span * 100.0
        width = max(right - left, 1.0)
        author = "subject" if item.data.get("assertedBy") == "subject" else "agent"
        status = example.state.status.get(item.id) or model.Status()
        marks = []
        if status.contested:
            marks.append("contested")
        if status.endorsement == "rejected":
            marks.append("rejected")
        if status.endorsement == "partial":
            marks.append("partly endorsed")
        held = "held %s to %s" % (model.format_time(held_from)[:10],
                                  model.format_time(held_until)[:10] if held_until else "now")
        rows.append('<div id="%s" data-filter data-id="%s"><div>%s <strong>%s</strong> <span class="meta">%s &middot; %s '
                    "&middot; %s reading by %s%s</span></div><div class=\"track\" aria-hidden=\"true\">"
                    '<div class="bar %s" style="left:%.2f%%;width:%.2f%%"></div></div>%s</div>' % (
                        anchor(item.id), esc(item.id), label_html(example.state.label(item.id, example.now)),
                        esc(example.content_text(item.data) or item.data.get("question")), esc(item.id), esc(held),
                        esc(item.data.get("stance")), esc(example.party_label(item.data.get("assertedBy"))),
                        (" &middot; " + esc(", ".join(marks))) if marks else "", author, left, width,
                        drawer(example, item)))
    axis = '<div class="axis"><span>%s</span><span>%s</span></div>' % (
        esc(model.format_time(start)[:10]), esc(model.format_time(end)[:10]))
    return ('<p class="small">Readings on a knowledge-time line. Bars show when each reading was held; the person&#39;s '
            'own readings and agents&#39; readings are marked in words.</p><div class="timeline">%s%s</div>'
            % ("".join(rows), axis))


def tensions_section(example):
    items = items_of(example, "Tension")
    if not items:
        return '<p class="small">No tensions.</p>'
    out = []
    for item in items:
        between = ", ".join(example.ref_link(r) for r in item.data.get("between") or [])
        out.append(record_li(example, item, ' <span class="meta">%s between %s &middot; who decides: %s</span>' % (
            esc(item.data.get("tensionKind")), between, esc(item.data.get("whoDecides")))))
    return '<ul class="records">%s</ul>' % "".join(out)


def lenses_section(example):
    out = []
    adoptions = items_of(example, "LensAdoption")
    if adoptions:
        out.append("<h3>Adoptions</h3><ul class=\"records\">")
        for item in adoptions:
            lens = item.data.get("lens") or {}
            extra = ' <span class="meta">route %s &middot; agent readings %s%s</span>' % (
                esc(item.data.get("route")), esc(item.data.get("agentInterpretation", "off")),
                (" &middot; " + esc(item.data["confidentiality"])) if item.data.get("confidentiality") else "")
            label = example.state.label(item.id, example.now)
            out.append('<li id="%s" data-filter data-id="%s">%s <strong>%s@%s</strong>%s%s</li>' % (
                anchor(item.id), esc(item.id), label_html(label), esc(lens.get("id")), esc(lens.get("version")),
                extra, drawer(example, item)))
        out.append("</ul>")
    views = items_of(example, "ModelView")
    if views:
        out.append("<h3>Model views</h3><ul class=\"records\">")
        for item in views:
            data = item.data
            hyp = ", ".join(example.ref_link(r) for r in data.get("hypotheses") or [])
            alts = ", ".join(esc(a) for a in data.get("alternatives") or [])
            extra = '<p class="small">Readings: %s. Limits: %s. Alternatives: %s.</p>' % (
                hyp or "none", esc(data.get("limits") or "none"), alts or "none")
            label = example.state.label(item.id, example.now)
            out.append('<li id="%s" data-filter data-id="%s">%s <strong>%s</strong> <span class="meta">%s</span>%s%s</li>' % (
                anchor(item.id), esc(item.id), label_html(label), esc(data.get("question") or item.id),
                esc((data.get("lens") or {}).get("id")), extra, drawer(example, item)))
        out.append("</ul>")
    assessments = items_of(example, "AssessmentRecord")
    if assessments:
        out.append("<h3>Assessment records</h3><ul class=\"records\">")
        for item in assessments:
            data = item.data
            results = "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                esc(r.get("label") or r.get("construct")), esc(r.get("raw", r.get("value"))),
                esc(r.get("rawRange"))) for r in data.get("results") or [])
            extra = ('<details><summary>Results</summary><div class="table-wrap"><table><thead><tr><th scope="col">'
                     'construct</th><th scope="col">raw</th><th scope="col">range</th></tr></thead><tbody>%s</tbody>'
                     "</table></div></details>" % results)
            label = example.state.label(item.id, example.now)
            out.append('<li id="%s" data-filter data-id="%s">%s <strong>%s</strong> <span class="meta">%s &middot; %s</span>%s%s</li>'
                       % (anchor(item.id), esc(item.id), label_html(label), esc((data.get("lens") or {}).get("id")),
                          esc((data.get("instrument") or {}).get("id")), esc(data.get("mode")), extra,
                          drawer(example, item)))
        out.append("</ul>")
    parts = items_of(example, "Part")
    if parts:
        out.append("<h3>Parts</h3><ul class=\"records\">%s</ul>" % "".join(record_li(example, p) for p in parts))
    out.append(playbooks_html(example))
    return "".join(out) or '<p class="small">No lenses adopted.</p>'


def playbooks_html(example):
    """The playbooks the context pins (LENSES.md §2.2): ways of working by situation. Guidance for the helper, never
    a permission and never a statement about the person (PB-4)."""
    docs = [example.ctx.playbook_doc(p.get("id"), p.get("version")) for p in example.ctx.manifest.get("playbooks") or []
            if isinstance(p, dict)]
    docs = [d for d in docs if d]
    if not docs:
        return ""
    out = ['<h3>Ways of working (playbooks)</h3><p class="small">Guidance for the helper, by situation: never a '
           "permission and never a statement about the person (PB-4).</p><ul class=\"records\">"]
    for doc in docs:
        situations = []
        for situation in doc.get("situations") or []:
            steps = "".join("<li>%s</li>" % esc(step) for step in (situation.get("use") or {}).get("en") or [])
            watch = (situation.get("watchFor") or {}).get("en")
            situations.append("<details><summary>%s</summary><ol>%s</ol>%s</details>" % (
                esc((situation.get("when") or {}).get("en")), steps,
                '<p class="small">Watch for: %s</p>' % esc(watch) if watch else ""))
        out.append('<li data-filter data-id="%s"><strong>%s</strong> <span class="meta">%s &middot; %s@%s</span>%s</li>'
                   % (esc(doc.get("id")), esc((doc.get("name") or {}).get("en")), esc(doc.get("author")),
                      esc(doc.get("id")), esc(doc.get("version")), "".join(situations)))
    out.append("</ul>")
    return "".join(out)


def practices_section(example):
    out = []
    for kind, title in (("Practice", "Practices"), ("Outcome", "Outcomes"), ("RecallCue", "Recall cues")):
        items = items_of(example, kind)
        if not items:
            continue
        out.append("<h3>%s</h3><ul class=\"records\">" % title)
        for item in items:
            data = item.data
            if kind == "Outcome":
                about = data.get("about") or {}
                targets = ", ".join(example.ref_link(v) for v in about.values() if isinstance(v, str))
                extra = ' <span class="meta">result %s for %s</span>' % (esc(data.get("result")), targets)
                text = "Outcome: %s" % data.get("result")
            elif kind == "RecallCue":
                status = example.state.status.get(item.id) or model.Status()
                offer = data.get("offer") or {}
                extra = ' <span class="meta">state %s &middot; offers %s &middot; asks first: %s</span>' % (
                    esc(status.lifecycle or "active"),
                    ", ".join(example.ref_link(t) for t in offer.get("targets") or []),
                    "yes" if (data.get("timing") or {}).get("askBeforeReminding") else "no")
                text = (data.get("trigger") or {}).get("description")
            else:
                status = example.state.status.get(item.id) or model.Status()
                extra = ' <span class="meta">%s &middot; %s</span>' % (
                    esc(data.get("practiceKind")), esc(status.lifecycle or data.get("initialStatus")))
                text = data.get("name")
            label = example.state.label(item.id, example.now)
            out.append('<li id="%s" data-filter data-id="%s">%s <strong>%s</strong>%s%s</li>' % (
                anchor(item.id), esc(item.id), label_html(label), esc(text), extra, drawer(example, item)))
        out.append("</ul>")
    return "".join(out) or '<p class="small">No practices.</p>'


def grants_section(example):
    items = [i for i in example.ctx.items if i.kind == "Grant"]
    if not items:
        return '<p class="small">No grants.</p>'
    rows = []
    for item in sorted(items, key=lambda i: i.id):
        data = item.data
        status = example.state.grant_status(item.id, example.now) or "unknown"
        if data.get("effect") == "deny":
            view = "deny grant"
        else:
            view = '<a href="as-%s/index.html">view as %s</a>' % (esc(data.get("grantee")), esc(data.get("grantee")))
        rows.append("<tr id=\"%s\"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            anchor(item.id), esc(item.id), esc(example.party_label(data.get("grantee"))),
            esc(", ".join(data.get("purposes") or [])), esc(data.get("mode", "full")),
            esc(", ".join(data.get("actions") or [])), esc(status), view))
    return ('<div class="table-wrap"><table><thead><tr><th scope="col">grant</th><th scope="col">grantee</th>'
            '<th scope="col">purposes</th><th scope="col">mode</th><th scope="col">actions</th>'
            '<th scope="col">status now</th><th scope="col">view</th></tr></thead><tbody>%s</tbody></table></div>'
            % "".join(rows))


def events_section(example):
    if not example.ctx.events:
        return '<p class="small">No Event log (single-document context).</p>'
    rows = []
    for item in example.ctx.events:
        data = item.data
        rows.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            esc(data.get("id")), esc(data.get("at")), esc(data.get("eventType")),
            esc(data.get("actor") or ""), esc(", ".join(data.get("records") or []))))
    erased = [i for i in example.ctx.items if i.kind == "Tombstone"]
    note = ""
    if erased:
        note = "<p class=\"small\">Erased records (Tombstones): %s.</p>" % ", ".join(
            "%s (%s, %s)" % (esc(i.id), esc(i.data.get("erasedKind")), esc(i.data.get("erasedAt"))) for i in erased)
    return ('<div class="table-wrap"><table><thead><tr><th scope="col">id</th><th scope="col">at</th>'
            '<th scope="col">type</th><th scope="col">actor</th><th scope="col">records</th></tr></thead><tbody>%s'
            "</tbody></table></div>%s" % ("".join(rows), note))


def legend():
    rows = "".join("<tr><td>%d</td><td>%s</td><td>%s</td></tr>" % (n, label_html(code), esc(rule))
                   for n, (code, _g, _w, rule) in enumerate(LABELS))
    return ('<p class="small">Each record shows one derived label, glyph and word together; the first matching rule '
            'wins. Colour never carries the meaning alone.</p><div class="table-wrap"><table><thead><tr>'
            '<th scope="col">#</th><th scope="col">label</th><th scope="col">rule</th></tr></thead><tbody>%s</tbody>'
            "</table></div>" % rows)


def subject_page(example):
    manifest = example.ctx.manifest
    subject = manifest.get("subject") or {}
    name = subject.get("displayName") or example.person.capitalize()
    if "fictional" not in name:
        name += " (fictional)"
    conformance = manifest.get("conformance") or {}
    header = ('<p class="kicker">Subject view</p><h1>%s</h1><p class="lead">The person&#39;s own view of the example '
              "context <code>examples/%s</code>, computed at its latest knowledge time %s.</p>"
              '<div class="facts"><div><span class="meta">context</span><br>%s</div><div><span class="meta">version'
              '</span><br>%s</div><div><span class="meta">holder</span><br>%s</div><div><span class="meta">spec '
              'version</span><br>%s</div><div><span class="meta">declared level</span><br>%s</div><div>%s</div></div>'
              % (esc(name), esc(example.name), esc(model.format_time(example.now)), esc(manifest.get("id")),
                 esc(manifest.get("version")), esc(manifest.get("holder", "subject")), esc(manifest.get("specVersion")),
                 esc(conformance.get("level", "L0")), check_badge(example)))
    body = [header,
            section("Needs grid", "needs", needs_grid(example)),
            section("Statements", "claims", claims_section(example)),
            section("Episodes", "episodes", episodes_section(example)),
            section("Then and now", "then-and-now", then_and_now(example)),
            section("Tensions", "tensions", tensions_section(example)),
            section("Lenses", "lenses", lenses_section(example)),
            section("Practices, outcomes and recall", "practices", practices_section(example)),
            section("Grants", "grants", grants_section(example)),
            section("Event log", "events", events_section(example)),
            section("Legend", "legend", legend())]
    return page("%s - example viewer" % name, "\n".join(body), 1)


# --------------------------------------------------------------------- view-as pages
def projection_for(example, grant_id):
    grant = example.ctx.record(grant_id)
    purpose = (grant.get("purposes") or [""])[0]
    try:
        return grants.build_projection(example.ctx, grant_id, purpose, example.now, "prj-view-%s" % grant_id,
                                       holder_key=grants.EXAMPLE_HOLDER_KEY,
                                       nonce=grants.new_nonce(b"viewer", grant_id)), None
    except grants.Denied as denied:
        return None, denied.code


def served_record(example, kind, record, derived):
    label = (derived or {}).get("label", "hypothesis")
    rid = record.get("id")
    text = example.content_text(record)
    detail = []
    if kind == "Source":
        detail.append("tier %s" % record.get("tier"))
        if record.get("sourceKind"):
            detail.append(record["sourceKind"])
    for key in ("facet", "predicate", "horizon", "stance", "result", "practiceKind"):
        if record.get(key):
            detail.append("%s %s" % (key, record[key]))
    excerpts = ""
    if record.get("excerpts"):
        excerpts = "".join("<blockquote>%s</blockquote>" % esc(e.get("text")) for e in record["excerpts"])
    accounts = ""
    if kind == "Episode":
        accounts = '<div class="accounts">%s</div>' % "".join(
            '<div class="account"><div class="kicker">%s</div><p>%s</p></div>' % (
                esc(a.get("accountKind")), esc(a.get("happened") or a.get("experienced") or ""))
            for a in record.get("accounts") or [])
    return ('<li data-filter data-id="%s">%s <strong>%s</strong> <span class="meta">%s &middot; %s%s</span>%s%s</li>' % (
        esc(rid), label_html(label), esc(text), esc(kind), esc(rid),
        (" &middot; " + esc(", ".join(detail))) if detail else "", excerpts, accounts))


def view_as_page(example, grantee, grant_ids):
    party = example.ctx.parties.get(grantee) or {}
    title = "View as %s" % (party.get("label") or grantee)
    out = ['<p class="kicker">View as grantee</p><h1>%s</h1>' % esc(title),
           '<p class="lead">Exactly what the evaluation algorithm (SPECIFICATION.md §12.3) serves to %s under its grant at %s. Nothing '
           'else exists for this grantee: there are no placeholders for what is withheld, and no counts.</p>'
           % (esc(example.party_label(grantee)), esc(model.format_time(example.now))),
           '<p><a href="../index.html">Back to the subject view</a></p>']
    for grant_id in grant_ids:
        projection, denied = projection_for(example, grant_id)
        out.append('<section aria-labelledby="g-%s"><h2 id="g-%s">Grant %s</h2>' % (esc(grant_id), esc(grant_id), esc(grant_id)))
        if projection is None:
            out.append('<p class="note">Nothing is served under this grant now (%s).</p></section>' % esc(denied))
            continue
        out.append('<div class="facts"><div><span class="meta">purpose</span><br>%s</div><div><span class="meta">mode'
                   '</span><br>%s</div><div><span class="meta">generated</span><br>%s</div><div><span class="meta">'
                   'valid until</span><br>%s</div><div><span class="meta">subject alias</span><br>%s</div></div>' % (
                       esc(projection["purpose"]), esc(projection["mode"]), esc(projection["generatedAt"]),
                       esc(projection["validUntil"]), esc(projection["subjectAlias"])))
        kinds = dict((name, kind) for group, name, kind in grants.MEMBERS)
        any_served = False
        for group in ("statements", "experience", "interpretations", "recall", "links"):
            members = projection.get(group) or {}
            if not members:
                continue
            out.append("<h3>%s</h3><ul class=\"records served\">" % GROUP_TITLES[group])
            for name, records in members.items():
                for record in records:
                    any_served = True
                    out.append(served_record(example, kinds.get(name, name), record,
                                             projection["derived"].get(record.get("id"))))
            out.append("</ul>")
        if not any_served:
            out.append('<p class="note">The grant is in force, and nothing in the context matches it.</p>')
        for absence in projection.get("absences") or []:
            out.append('<p class="note">Requested and not disclosed.</p>')
        if projection.get("parties"):
            out.append("<p class=\"small\">Parties named in what is served: %s.</p>" % ", ".join(
                "%s%s" % (esc(p.get("label")), (" (%s)" % esc(p["role"])) if p.get("role") else "")
                for p in projection["parties"]))
        out.append("</section>")
    return page("%s - example viewer" % title, "\n".join(out), 2)


def grantee_pages(example):
    by_grantee = {}
    for item in sorted((i for i in example.ctx.items if i.kind == "Grant"), key=lambda i: i.id):
        if item.data.get("effect") == "deny":
            continue
        by_grantee.setdefault(item.data.get("grantee"), []).append(item.id)
    return by_grantee


# --------------------------------------------------------------------- index and driver
def index_page(examples):
    items = []
    for example in examples:
        subject = example.ctx.manifest.get("subject") or {}
        name = subject.get("displayName") or example.person.capitalize()
        links = ['<a href="%s/index.html">subject view</a>' % esc(example.person)]
        for grantee in sorted(grantee_pages(example)):
            links.append('<a href="%s/as-%s/index.html">view as %s</a>' % (
                esc(example.person), esc(grantee), esc(example.party_label(grantee))))
        items.append("<li data-filter><strong>%s</strong> <span class=\"meta\">examples/%s &middot; declared %s</span><br>%s</li>"
                     % (esc(name), esc(example.name),
                        esc((example.ctx.manifest.get("conformance") or {}).get("level", "L0")), " &middot; ".join(links)))
    body = ('<p class="kicker">Example viewer</p><h1>Example contexts</h1><p class="lead">Static pages generated from '
            "the synthetic examples. Each person has a subject view and one &ldquo;view as&rdquo; page per grantee, "
            "rendered through the grant evaluation algorithm.</p><ul class=\"records\">%s</ul>" % "".join(items))
    return page("Example viewer", body, 0)


def load_examples(root, spec):
    base = os.path.join(root, "examples")
    out = []
    if not os.path.isdir(base):
        return out
    for name in sorted(os.listdir(base)):
        directory = os.path.join(base, name)
        if os.path.isdir(directory) and (os.path.isfile(os.path.join(directory, "context.json")) or
                                         os.path.isfile(os.path.join(directory, "context", "context.json"))):
            out.append(Example(root, name, spec))
    return out


def render_all(root=None, spec=None):
    root = root or vocab.default_root()
    spec = spec or vocab.Spec(root)
    examples = load_examples(root, spec)
    files = {"index.html": index_page(examples)}
    for example in examples:
        files["%s/index.html" % example.person] = subject_page(example)
        for grantee, grant_ids in grantee_pages(example).items():
            files["%s/as-%s/index.html" % (example.person, grantee)] = view_as_page(example, grantee, grant_ids)
    return files


def write(files, out):
    if os.path.isdir(out):
        shutil.rmtree(out)
    for rel, text in files.items():
        full = os.path.join(out, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)


def existing(out):
    found = {}
    for base, _dirs, names in os.walk(out):
        for name in names:
            full = os.path.join(base, name)
            with open(full, "r", encoding="utf-8") as handle:
                found[os.path.relpath(full, out).replace(os.sep, "/")] = handle.read()
    return found


def main(argv=None):
    parser = argparse.ArgumentParser(description="Render the static example viewer.")
    parser.add_argument("--check", action="store_true", help="verify that viewer/ is up to date")
    parser.add_argument("--out", help="output directory (default: viewer/ at the repository root)")
    parser.add_argument("--home-href", default="", help="link back to an enclosing site, relative to the viewer root")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    global HOME_HREF
    HOME_HREF = args.home_href or ""
    root = vocab.default_root()
    out = args.out or os.path.join(root, "viewer")
    files = render_all(root)
    if args.check:
        current = existing(out) if os.path.isdir(out) else {}
        problems = sorted(set(files) ^ set(current)) + sorted(k for k in files if k in current and files[k] != current[k])
        if problems:
            for rel in problems:
                print("viewer out of date: %s" % rel)
                if rel in files and rel in current:
                    diff = list(difflib.unified_diff(current[rel].splitlines(), files[rel].splitlines(), lineterm="", n=0))
                    for line in diff[2:8]:
                        print("  " + line)
            return 1
        print("viewer up to date (%d pages)" % len(files))
        return 0
    write(files, out)
    print("wrote %d pages to %s" % (len(files), os.path.relpath(out, root) if out.startswith(root) else out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
