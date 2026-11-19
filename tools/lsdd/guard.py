"""Pull request guard: what a pull request may touch, based on its kind.

Pure functions only; `tools/guard.py` feeds them from `git diff`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .core import Report, matches_any

TICKED_RE = re.compile(r"^\+- \[[xX]\] (?P<id>T-[A-Z][A-Z0-9]{0,9}-\d{2}) \[(?P<tag>[A-Z-]+)\]")
UNTICKED_RE = re.compile(r"^-- \[ \] (?P<id>T-[A-Z][A-Z0-9]{0,9}-\d{2}) \[(?P<tag>[A-Z-]+)\]")


@dataclass
class Diff:
    changed: list[str]                 # every path added, modified, deleted or renamed (old and new)
    added_lines: list[tuple[str, str]]  # (path, text of an added line, without the leading '+')
    raw_task_lines: list[str]          # '+' and '-' lines of tasks.md files, with the sign


def ticked_tasks(diff: Diff) -> dict[str, str]:
    """Tasks whose box went from [ ] to [x] in this diff: id -> tag."""
    unticked = {m.group("id") for line in diff.raw_task_lines if (m := UNTICKED_RE.match(line))}
    ticked: dict[str, str] = {}
    for line in diff.raw_task_lines:
        match = TICKED_RE.match(line)
        if match and match.group("id") in unticked:
            ticked[match.group("id")] = match.group("tag")
    return ticked


def pr_kind(labels: list[str], ticked: dict[str, str]) -> str:
    normalized = {label.strip().lower() for label in labels if label.strip()}
    for kind in ("impl", "test-change", "test", "spec", "docs", "chore"):
        if kind in normalized:
            return kind
    tags = set(ticked.values())
    for tag in ("IMPL", "TEST-CHANGE", "TEST", "SPEC", "DOCS", "CHORE", "OWNER"):
        if tag in tags:
            return tag.lower()
    return "unknown"


def evaluate(diff: Diff, labels: list[str], config: dict) -> tuple[str, Report]:
    report = Report()
    ticked = ticked_tasks(diff)
    kind = pr_kind(labels, ticked)

    if kind == "impl":
        protected = config.get("protected_for_impl", [])
        for path in diff.changed:
            if matches_any(path, protected):
                report.error(path, "an [IMPL] pull request must not change this protected path; propose a [TEST-CHANGE] or [SPEC] task instead")
        hatches = config.get("escape_hatches", [])
        for path, text in diff.added_lines:
            for hatch in hatches:
                if hatch in text:
                    report.error(path, f"an [IMPL] pull request must not add '{hatch}'")

    code_globs = config.get("code_globs", [])
    changes_dir = config.get("changes_dir", "changes").rstrip("/") + "/"
    test_globs = config.get("test_globs", [])
    # Tests often live inside code folders (packages/x/tests/): they are not code.
    touches_code = any(
        matches_any(path, code_globs) and not matches_any(path, test_globs) for path in diff.changed
    )
    touches_change = any(path.startswith(changes_dir) for path in diff.changed)
    if touches_code and not touches_change:
        report.error("pull request", "code changed but no change folder was touched: every code change belongs to a change in changes/")

    if kind == "test" and touches_code:
        report.error("pull request", "a [TEST] pull request must not change product code")

    if kind == "unknown" and diff.changed:
        report.warn("pull request", "kind unknown: add a label (spec, test, impl, test-change, docs, chore) or tick a task box")
    return kind, report
