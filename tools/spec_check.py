"""Check requirements, living specs, change folders and test markers.

Usage: python tools/spec_check.py [--root PATH]
Exit code 0 when there are no errors (warnings are printed but allowed).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.lsdd.core import check_project, find_root, load_project


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=None, help="repository root (default: search upwards)")
    args = parser.parse_args(argv)
    root = find_root(args.root)
    project = load_project(root)
    report = check_project(project)
    for line in report.warnings:
        print(f"warning: {line}")
    for line in report.errors:
        print(f"error: {line}")
    summary = (
        f"{len(project.requirements)} requirements, {len(project.criteria)} criteria, "
        f"{len(project.specs)} specs, {len(project.changes)} changes, {len(project.tasks)} tasks, "
        f"{len(project.awaits)} awaiting tests"
    )
    if report.ok:
        print(f"spec-check: OK ({summary})")
        return 0
    print(f"spec-check: {len(report.errors)} error(s) ({summary})")
    return 1


if __name__ == "__main__":
    sys.exit(main())
