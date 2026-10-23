#!/usr/bin/env python3
"""Build or verify the release manifest and run the REL checks.

Usage:
    python3 tools/build_release_manifest.py               # write release-manifest.json (the release step)
    python3 tools/build_release_manifest.py --check       # recompute everything; exit 1 on any difference
    python3 tools/build_release_manifest.py --out FILE    # write the manifest elsewhere (for inspection)
    python3 tools/build_release_manifest.py --export DIR  # copy exactly the released files into a fresh tree
                                                          # (the only tree that is ever published)

Input is ``release-plan.json``: an allowlist of globs (``include``), globs never exported (``exclude``, which
always contains the private tree), the licensing rules, the licence sources, the checks run and the verification
sources. ``**`` spans any number of path segments (including none), ``*`` and ``?`` stay within one segment, and
every glob is matched against the whole repository-relative path.

The REL checks (also run by ``check.py --release``):
- REL-1 every exported file is in the manifest with a matching sha256, and the manifest lists nothing else;
- REL-2 the private tree is absent from the export and listed in ``exclude``;
- REL-3 LICENSING.md rules equal the release-plan rules (and the manifest's);
- REL-4 every exported Markdown file ends with the CC BY or Apache footer matching its licence (vault objects of the
  examples are data, not documents, and are exempt);
- REL-5 no private marker, no path, host or e-mail, no credential pattern and no internal design-section id in any
  exported text file;
- REL-6 the flags ledger is present and honest where it can be computed;
- REL-7 an exported tree holds no private tree, in its files or (when it is a Git repository) in its index.

Private markers are not in this file. They are a list kept outside the repository and loaded at run time from the
file named by ``OHC_DENYLIST``, or from an untracked ``.release-denylist.json`` at the root (format
``ohc.release-denylist/1``: ``{"patterns": [{"group", "regex", "ignoreCase"}]}``). The release step and ``--check``
fail closed without it (REL-5), and ``flags.privateMarkersAndCredentialPatternScan`` is true only when it was loaded.
Only generic patterns (paths, hosts, e-mail, credentials, design-section ids) are public.

The manifest carries no timestamps, so a rebuild of unchanged files is byte-identical.
"""

import argparse
import hashlib
import os
import re
import struct
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)

from ohclib import jsonio, vocab  # noqa: E402

PLAN = "release-plan.json"
MANIFEST = "release-manifest.json"
FORMAT = "ohc.public-export/1"
PRIVATE_TREE = "inter" + "nal"
FOOTERS = {
    "CC-BY-4.0": "Copyright 2026 Taras Pustovoy and contributors. Licensed under "
                 "[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).",
    "Apache-2.0": "Copyright 2026 Taras Pustovoy and contributors. Licensed under "
                  "[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).",
}
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
        ".webp": "image/webp", ".pdf": "application/pdf", ".ico": "image/x-icon"}


def _lit(*parts):
    """A literal pattern, written in fragments so that this file does not match its own generic list."""
    return re.compile(re.escape("".join(parts)))


DENYLIST_ENV = "OHC_DENYLIST"
DENYLIST_FILE = ".release-denylist.json"
DENYLIST_FORMAT = "ohc.release-denylist/1"
# Generic patterns only: paths, hosts, e-mail. Private markers come from the run-time denylist.
FORBIDDEN = [
    ("paths-and-hosts", _lit("/Us", "ers/")), ("paths-and-hosts", _lit("fi", "le://")),
    ("paths-and-hosts", _lit("127.0", ".0.1")), ("paths-and-hosts", _lit("local", "host")),
    ("paths-and-hosts", _lit("thr", "ead://")), ("paths-and-hosts", _lit(PRIVATE_TREE, "/")),
    ("personal", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z][A-Za-z0-9-]*(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")),
]
# Internal design-section ids (letter, dot, number) have no public anchor; tools cite § numbers instead.
DESIGN_ID = re.compile(r"(?<![A-Za-z0-9.§])[A-I]\.\d+(?:\.\d+)*(?![A-Za-z0-9])")
DESIGN_ID_SCOPE = ("tools/",)
CREDENTIALS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    re.compile(r"(?i)\b(?:api[_-]?key|secret|password|token)\b\s*[:=]\s*[\"'][^\"'\s]{12,}[\"']"),
]
# The design requires `exclude: ["<private tree>/**"]` in the plan itself, so the plan may name the tree.
FORBIDDEN_EXEMPT = {(PLAN, PRIVATE_TREE + "/")}


def denylist_path(root):
    return os.environ.get(DENYLIST_ENV) or os.path.join(root, DENYLIST_FILE)


def load_denylist(root):
    """[(group, compiled pattern)] from the private denylist, or None when it is absent or unreadable."""
    path = denylist_path(root)
    if not os.path.isfile(path):
        return None
    try:
        doc = jsonio.load_json(path)
    except (OSError, jsonio.JsonError):
        return None
    if not isinstance(doc, dict) or doc.get("format") != DENYLIST_FORMAT:
        return None
    out = []
    for entry in doc.get("patterns") or []:
        try:
            flags = re.IGNORECASE if entry.get("ignoreCase") else 0
            out.append((entry.get("group", "private"), re.compile(entry["regex"], flags)))
        except (KeyError, TypeError, re.error):
            return None
    return out or None


# ------------------------------------------------------------------ files and globs
def glob_regex(pattern):
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def glob_match(pattern, path):
    return glob_regex(pattern).match(path) is not None


def walk(root):
    out = []
    for base, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d != ".git" and not os.path.islink(os.path.join(base, d)))
        for name in sorted(names):
            full = os.path.join(base, name)
            if os.path.islink(full):
                continue
            out.append(os.path.relpath(full, root).replace(os.sep, "/"))
    return sorted(out)


def exported_files(root, plan):
    include = plan.get("include") or []
    exclude = plan.get("exclude") or []
    out = []
    for rel in walk(root):
        if rel == MANIFEST:
            continue
        if any(glob_match(p, rel) for p in exclude):
            continue
        if any(glob_match(p, rel) for p in include):
            out.append(rel)
    return out


def license_for(plan, rel):
    for rule in (plan.get("licensing") or {}).get("rules") or []:
        if glob_match(rule["glob"], rel):
            return rule["license"]
    return (plan.get("licensing") or {}).get("default", "Apache-2.0")


def sha256_file(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def is_text(path):
    with open(path, "rb") as handle:
        data = handle.read()
    if b"\x00" in data:
        return False
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def binary_asset(root, rel):
    full = os.path.join(root, rel)
    with open(full, "rb") as handle:
        data = handle.read()
    entry = {"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    mime = MIME.get(os.path.splitext(rel)[1].lower())
    if mime:
        entry["mimeType"] = mime
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        entry["width"], entry["height"] = struct.unpack(">II", data[16:24])
    return entry


# ------------------------------------------------------------------ manifest
def load_plan(root):
    return jsonio.load_json(os.path.join(root, PLAN))


def build_manifest(root, plan=None, denylist=None):
    plan = plan or load_plan(root)
    if denylist is None:
        denylist = load_denylist(root)
    files = {}
    exported = exported_files(root, plan)
    binaries = set(plan.get("binaryAssets") or [])
    for rel in exported:
        digest = sha256_file(os.path.join(root, rel))
        files[rel] = {"license": license_for(plan, rel), "sha256": digest, "adapted": False, "source": rel,
                      "sourceSha256": digest}
        if not is_text(os.path.join(root, rel)):
            binaries.add(rel)
    manifest = {
        "format": FORMAT,
        "releaseVersion": plan["releaseVersion"],
        "specVersion": plan["specVersion"],
        "rightsHolder": plan["rightsHolder"],
        "licensing": plan["licensing"],
        "licenseStatus": plan.get("licenseStatus", "approved-by-owner-pending"),
        "licenseSources": plan.get("licenseSources") or {},
        "files": files,
        "binaryAssets": [binary_asset(root, rel) for rel in sorted(binaries) if rel in files],
        "checks": list(plan.get("checks") or []),
        "verificationSources": [{"path": rel, "sha256": sha256_file(os.path.join(root, rel))}
                                for rel in plan.get("verificationSources") or []
                                if os.path.isfile(os.path.join(root, rel))],
        "sourcePlan": PLAN,
        "sourcePlanSha256": sha256_file(os.path.join(root, PLAN)),
        "publication": plan.get("publication", "none (local only)"),
        "flags": {
            "realPersonDataIncluded": False,
            "legalReviewPerformed": False,
            "publisherPermissionsObtained": False,
            "internalExcluded": not any(rel.split("/")[0] == PRIVATE_TREE for rel in files),
            "referenceToolsDistributed": any(rel.startswith("tools/") for rel in files),
            "privateMarkersAndCredentialPatternScan": denylist is not None,
            "liveRuntimeTested": False,
        },
    }
    return manifest


# ------------------------------------------------------------------ REL checks
def licensing_md_rules(root):
    """(rules, default) from the LICENSING.md table rows ``| `glob` | LICENSE |``."""
    path = os.path.join(root, "LICENSING.md")
    if not os.path.isfile(path):
        return None, None
    rules, default = [], None
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            match = re.match(r"^\|\s*`([^`]+)`\s*\|\s*([A-Za-z0-9.-]+)\s*\|\s*$", line)
            if match:
                rules.append({"glob": match.group(1), "license": match.group(2)})
                continue
            match = re.match(r"^\|\s*\(default[^|]*\)\s*\|\s*([A-Za-z0-9.-]+)\s*\|\s*$", line)
            if match:
                default = match.group(1)
    return rules, default


def footer_ok(text, license_code):
    lines = [line.rstrip() for line in text.rstrip("\n").split("\n")]
    return len(lines) >= 2 and lines[-2] == "---" and lines[-1] == FOOTERS.get(license_code)


def scan_text(rel, text, denylist=None):
    """[(rule, group)] for private markers, generic forbidden strings, credentials and design ids in one file."""
    hits = []
    for group, pattern in list(FORBIDDEN) + list(denylist or []):
        match = pattern.search(text)
        if match and (rel, match.group(0)) not in FORBIDDEN_EXEMPT:
            hits.append(("REL-5", group))
    for pattern in CREDENTIALS:
        if pattern.search(text):
            hits.append(("REL-5", "credential"))
    if rel.startswith(DESIGN_ID_SCOPE) and DESIGN_ID.search(text):
        hits.append(("REL-5", "design-section-id"))
    return hits


def release_findings(root, findings_class):
    """Run REL-1…REL-6 on the repository at ``root``; returns a Findings object (check.py's class)."""
    findings = findings_class()
    root = os.path.abspath(root)
    try:
        plan = load_plan(root)
    except (OSError, jsonio.JsonError):
        findings.add("REL-1", None, PLAN)
        return findings
    spec = vocab.Spec(vocab.default_root())
    for error in spec.validate("urn:ohc:schema:release-plan:0.1.0-draft", plan):
        findings.add("S-2", None, PLAN + "#" + error)
    denylist = load_denylist(root)
    if denylist is None:
        # Fail closed: without the private list the scan cannot say the release is clean.
        findings.add("REL-5", None, "%s (private denylist not loaded: set %s or add the untracked file)" % (
            DENYLIST_FILE, DENYLIST_ENV))
    expected = build_manifest(root, plan, denylist)
    exported = expected["files"]
    # REL-1
    manifest_path = os.path.join(root, MANIFEST)
    if not os.path.isfile(manifest_path):
        findings.add("REL-1", None, MANIFEST)
        manifest = None
    else:
        manifest = jsonio.load_json(manifest_path)
        for error in spec.validate("urn:ohc:schema:release-manifest:0.1.0-draft", manifest):
            findings.add("S-2", None, MANIFEST + "#" + error)
        listed = manifest.get("files") or {}
        for rel in sorted(set(exported) | set(listed)):
            if rel not in listed or rel not in exported or listed[rel].get("sha256") != exported[rel]["sha256"] \
                    or listed[rel].get("license") != exported[rel]["license"]:
                findings.add("REL-1", None, rel)
        for key in ("sourcePlanSha256", "verificationSources", "binaryAssets", "licensing", "licenseSources"):
            if manifest.get(key) != expected[key]:
                findings.add("REL-1", None, MANIFEST + "#/" + key)
    # REL-2
    if not any(glob_match(p, PRIVATE_TREE + "/x") for p in plan.get("exclude") or []):
        findings.add("REL-2", None, PLAN + "#/exclude")
    for rel in exported:
        if rel.split("/")[0] == PRIVATE_TREE:
            findings.add("REL-2", None, rel)
    # REL-3
    rules, default = licensing_md_rules(root)
    plan_licensing = plan.get("licensing") or {}
    if rules is None or rules != plan_licensing.get("rules") or default != plan_licensing.get("default"):
        findings.add("REL-3", None, "LICENSING.md")
    if manifest is not None and manifest.get("licensing") != plan_licensing:
        findings.add("REL-3", None, MANIFEST + "#/licensing")
    # REL-4 and REL-5
    for rel in exported:
        full = os.path.join(root, rel)
        if not is_text(full):
            continue
        with open(full, "r", encoding="utf-8") as handle:
            text = handle.read()
        if rel.endswith(".md") and "/vault/" not in "/" + rel:
            if not footer_ok(text, exported[rel]["license"]):
                findings.add("REL-4", None, rel)
        for rule, group in scan_text(rel, text, denylist):
            findings.add(rule, None, "%s (%s)" % (rel, group))
    # REL-6
    if manifest is not None:
        flags = manifest.get("flags")
        if not isinstance(flags, dict):
            findings.add("REL-6", None, MANIFEST + "#/flags")
        else:
            for key in ("internalExcluded", "referenceToolsDistributed", "privateMarkersAndCredentialPatternScan",
                        "realPersonDataIncluded", "liveRuntimeTested"):
                if flags.get(key) != expected["flags"][key]:
                    findings.add("REL-6", None, MANIFEST + "#/flags/" + key)
            for key in ("legalReviewPerformed", "publisherPermissionsObtained"):
                if not isinstance(flags.get(key), bool):
                    findings.add("REL-6", None, MANIFEST + "#/flags/" + key)
    for name in sorted(os.listdir(os.path.join(root, "examples"))) if os.path.isdir(os.path.join(root, "examples")) else []:
        for candidate in ("context.json", "context/context.json"):
            path = os.path.join(root, "examples", name, candidate)
            if os.path.isfile(path):
                doc = jsonio.load_json(path)
                if doc.get("synthetic") is not True:
                    findings.add("REL-6", None, "examples/%s/%s#/synthetic" % (name, candidate))
    return findings


def export_findings(directory, findings):
    """REL-7: the exported tree holds no private tree, neither as files nor in a Git index."""
    for rel in walk(directory):
        if rel.split("/")[0] == PRIVATE_TREE:
            findings.add("REL-7", None, rel)
    if os.path.isdir(os.path.join(directory, ".git")):
        import subprocess

        result = subprocess.run(["git", "ls-files", PRIVATE_TREE], cwd=directory, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL)
        if result.stdout.strip():
            findings.add("REL-7", None, PRIVATE_TREE + "/ (tracked in the exported tree)")
    return findings


def export_tree(root, out, manifest_text, git_init=False):
    """Copy exactly the manifest's files into ``out`` (which must not exist), with the manifest. With ``git_init``,
    initialise a fresh repository there whose single commit has a neutral author; the source history never travels."""
    import shutil
    import subprocess

    if os.path.exists(out):
        raise SystemExit("export directory exists: %s" % out)
    manifest = jsonio.loads_strict(manifest_text)
    for rel in sorted(manifest["files"]):
        target = os.path.join(out, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copy2(os.path.join(root, rel), target)
    with open(os.path.join(out, MANIFEST), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(manifest_text)
    if git_init:
        env = dict(os.environ, GIT_AUTHOR_NAME="OHC editors", GIT_AUTHOR_EMAIL="editors" + "@" + "invalid.invalid",
                   GIT_COMMITTER_NAME="OHC editors", GIT_COMMITTER_EMAIL="editors" + "@" + "invalid.invalid")
        subprocess.run(["git", "init", "-q"], cwd=out, check=True)
        subprocess.run(["git", "add", "-A"], cwd=out, check=True, env=env)
        subprocess.run(["git", "commit", "-q", "-m", "Open Human Context %s" % manifest["releaseVersion"]],
                       cwd=out, check=True, env=env)


class _Findings(object):
    def __init__(self):
        self.items = []

    def add(self, rule, rid, path, level=None):
        self.items.append({"rule": rule, "id": rid, "path": path, "level": level or "L0", "severity": "error"})


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build or verify release-manifest.json.")
    parser.add_argument("--check", action="store_true", help="recompute everything and fail on any difference")
    parser.add_argument("--out", help="write the manifest to this file instead of release-manifest.json")
    parser.add_argument("--root", help=argparse.SUPPRESS)
    parser.add_argument("--export", help="copy exactly the released files into this new directory")
    parser.add_argument("--git-init", action="store_true",
                        help="with --export: start a fresh Git repository there (neutral author, no source history)")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    root = os.path.abspath(args.root or vocab.default_root())
    if not os.path.isfile(os.path.join(root, PLAN)):
        sys.stderr.write("no %s\n" % PLAN)
        return 1
    expected = build_manifest(root)
    text = jsonio.dumps_pretty(expected)
    if args.export:
        findings = release_findings(root, _Findings)
        current = None
        if os.path.isfile(os.path.join(root, MANIFEST)):
            with open(os.path.join(root, MANIFEST), "r", encoding="utf-8") as handle:
                current = handle.read()
        if findings.items or current != text:
            for f in findings.items:
                print("%s %s" % (f["rule"], f["path"]))
            print("not exported: the release manifest must be built and clean first")
            return 1
        out = os.path.abspath(args.export)
        export_tree(root, out, text, git_init=args.git_init)
        problems = export_findings(out, _Findings()).items
        for f in problems:
            print("%s %s" % (f["rule"], f["path"]))
        if problems:
            return 1
        print("exported %d files to %s" % (len(expected["files"]), out))
        return 0
    if args.check:
        findings = release_findings(root, _Findings)
        current = None
        path = os.path.join(root, MANIFEST)
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as handle:
                current = handle.read()
        problems = [(f["rule"], f["path"]) for f in findings.items]
        if current != text and not any(rule == "REL-1" and p == MANIFEST for rule, p in problems):
            problems.append(("REL-1", MANIFEST + " differs from a fresh build"))
        for rule, where in problems:
            print("%s %s" % (rule, where))
        if problems:
            return 1
        print("release manifest up to date (%d files)" % len(expected["files"]))
        return 0
    pre = release_findings(root, _Findings)
    blocking = [f for f in pre.items if f["rule"] in ("REL-2", "REL-3", "REL-4", "REL-5", "S-2")
                and not f["path"].startswith(MANIFEST)]
    if blocking:
        for f in blocking:
            print("%s %s" % (f["rule"], f["path"]))
        print("not written: fix the findings above first")
        return 1
    out = args.out or os.path.join(root, MANIFEST)
    with open(out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print("wrote %s (%d files)" % (os.path.relpath(out, root) if out.startswith(root) else out, len(expected["files"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
