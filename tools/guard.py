"""Guard a pull request: an [IMPL] change must not weaken tests, specs or rules.

Usage: python tools/guard.py --base origin/main
Labels come from the LSDD_PR_LABELS environment variable (comma separated);
without labels, the kind is taken from the task boxes ticked in the diff.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.lsdd.core import find_root, load_config
from tools.lsdd.guard import Diff, evaluate


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout


def read_diff(root: Path, base: str) -> Diff:
    changed: list[str] = []
    for line in git(root, "diff", "--name-status", "-M", f"{base}...HEAD").splitlines():
        parts = line.split("\t")
        changed.extend(parts[1:])
    added: list[tuple[str, str]] = []
    task_lines: list[str] = []
    current = ""
    for line in git(root, "diff", "-U0", "--no-color", f"{base}...HEAD").splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else ""
            continue
        if line.startswith("--- "):
            continue
        if line.startswith("+"):
            added.append((current, line[1:]))
        if current.endswith("tasks.md") and line[:1] in "+-":
            task_lines.append(line)
    return Diff(changed=sorted(set(changed)), added_lines=added, raw_task_lines=task_lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", required=True, help="base ref, for example origin/main")
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args(argv)
    root = find_root(args.root)
    labels = os.environ.get("LSDD_PR_LABELS", "").split(",")
    kind, report = evaluate(read_diff(root, args.base), labels, load_config(root))
    for line in report.warnings:
        print(f"warning: {line}")
    for line in report.errors:
        print(f"error: {line}")
    print(f"guard: pull request kind = {kind}; {'OK' if report.ok else f'{len(report.errors)} error(s)'}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
