#!/usr/bin/env python3
"""Run the CI sequence (.github/workflows/check.yml) locally, step by step, and stop at the first failure.

Usage:
    python3 tools/check_all.py               # every step, as in .github/workflows/check.yml
    python3 tools/check_all.py --no-release  # skip the release-manifest step (before the release is built)
    python3 tools/check_all.py --keep-going  # run every step and report all failures
"""

import argparse
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STEPS = [
    ["tools/check.py", "--self-test"],
    ["tools/check.py", "examples/ilse-minimal", "--level", "L0", "--json"],
    ["tools/check.py", "examples/noa-episode-first", "--level", "L2", "--json"],
    ["tools/check.py", "examples/kofi-gum-ode/context", "--level", "L2", "--json"],
    ["tools/check.py", "examples/mara-l1-agent", "--level", "L1", "--json"],
    ["tools/check.py", "examples/tove-bring-a-result/context", "--level", "L2", "--json"],
    ["tools/lens_tables.py", "--check"],
    ["-m", "unittest", "discover", "-s", "tools/tests", "-v"],
    ["tools/render_viewer.py", "--check"],
    ["tools/build_release_manifest.py", "--check"],
]


# The same path on instruments kept outside the release while their publication is on hold: checked here when that
# tree is present (a released copy has none), with its registry; tools/tests/test_tove.py rebuilds it byte for byte.
PRIVATE = "inter" + "nal"
LOCAL_STEPS = [
    ["tools/check.py", PRIVATE + "/examples/tove-hogan-import/context", "--registry", PRIVATE, "--level", "L2", "--json"],
    ["tools/check.py", PRIVATE + "/examples/tove-hogan-import/variants/hds-unticked", "--registry", PRIVATE, "--level",
     "L2", "--json"],
]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the CI sequence locally.")
    parser.add_argument("--no-release", action="store_true", help="skip build_release_manifest.py --check")
    parser.add_argument("--keep-going", action="store_true", help="run every step even after a failure")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    failures = []
    steps = list(STEPS)
    if os.path.isdir(os.path.join(ROOT, PRIVATE, "examples")):
        # plus each checker kept in that tree (<tree>/<folder>/check_*.py), found rather than named
        found = sorted(glob.glob(os.path.join(ROOT, PRIVATE, "*", "check_*.py")))
        steps[6:6] = LOCAL_STEPS + [[os.path.relpath(path, ROOT)] for path in found]
    for step in steps:
        if args.no_release and step[0] == "tools/build_release_manifest.py":
            continue
        command = [sys.executable, "-B"] + step
        label = " ".join(["python", "-B"] + step)
        result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ok = result.returncode == 0
        print("%s  %s" % ("ok  " if ok else "FAIL", label))
        if not ok:
            sys.stdout.write(result.stdout.decode("utf-8", "replace")[-6000:])
        if not ok:
            failures.append(label)
            if not args.keep_going:
                break
    if failures:
        print("%d step(s) failed" % len(failures))
        return 1
    print("all steps passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
