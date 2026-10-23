#!/usr/bin/env python3
"""Check the joint example with the pinned ODE package checker and OHC binding checks."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

import check
from ohclib import vocab

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ode-root", type=Path, required=True, help="Checkout of the exact ODE revision in sources.json")
    args = parser.parse_args()
    source = json.loads((ROOT / "examples/ohc-ode-tara/sources.json").read_text())
    expected = source["ode"]["commit"]
    revision = subprocess.check_output(["git", "-C", str(args.ode_root), "rev-parse", "HEAD"], text=True).strip()
    if revision != expected:
        parser.error("ODE checkout does not match the pinned source revision")
    changes = subprocess.check_output(["git", "-C", str(args.ode_root), "status", "--porcelain", "--untracked-files=no"], text=True)
    if changes.strip():
        parser.error("ODE checkout has tracked modifications; use an unchanged pinned checkout")
    package = ROOT / "examples/ohc-ode-tara/package"
    findings, _ = check.check_document(str(package / "manifest.json"), "manifest.json", vocab.Spec())
    if findings.items:
        print(json.dumps({"valid": False, "findings": findings.items}, indent=2))
        return 1
    result = subprocess.run([sys.executable, "-B", str(args.ode_root / ".github/checks/package_contract.py"),
                             str(package), "--standard-root", str(args.ode_root)], text=True, capture_output=True)
    if result.returncode:
        sys.stderr.write(result.stderr)
        return result.returncode
    print(json.dumps({"ohcBindingConsistent": True, "ode": json.loads(result.stdout),
                      "consentAuthenticated": False, "runtimeTested": False,
                      "taraMethod": "documented scenario; not an executed agent evaluation"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
