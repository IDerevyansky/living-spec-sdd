"""Parsing and checks for the living-spec SDD layout.

Standard library only. Every rule here is deliberately simple: IDs, links,
files and statuses. Nothing tries to understand the meaning of the text.
"""

from __future__ import annotations

import fnmatch
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

CONFIG_NAME = "living-spec.json"

REQ_RE = re.compile(r"\bREQ-[A-Z][A-Z0-9]{0,9}-\d{3}\b")
AC_RE = re.compile(r"\bAC-[A-Z][A-Z0-9]{0,9}-\d{3}\b")
TASK_RE = re.compile(r"\bT-[A-Z][A-Z0-9]{0,9}-\d{2}\b")
CODE_RE = re.compile(r"^[A-Z][A-Z0-9]{1,9}$")
CHANGE_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
TASK_LINE_RE = re.compile(
    r"^- \[(?P<done>[ xX])\] (?P<id>T-[A-Z][A-Z0-9]{0,9}-\d{2}) \[(?P<tag>[A-Z-]+)\]\s*(?P<title>.*)$"
)
TASK_FIELD_RE = re.compile(r"^\s+- (?P<key>[A-Za-z ]+):\s*(?P<value>.*)$")
TABLE_ROW_RE = re.compile(r"^\|\s*(?P<id>(?:REQ|AC)-[A-Z][A-Z0-9]{0,9}-\d{3})\s*\|(?P<rest>.*)\|\s*$")
AWAITS_RES = (
    re.compile(r"awaits\(\s*[\"'](?P<id>T-[A-Z][A-Z0-9]{0,9}-\d{2})[\"']\s*\)"),
    re.compile(r"\[awaits:(?P<id>T-[A-Z][A-Z0-9]{0,9}-\d{2})\]"),
)

TAGS = {"SPEC", "TEST", "IMPL", "TEST-CHANGE", "DOCS", "CHORE", "OWNER"}
CHANGE_FILES = ("proposal.md", "plan.md", "tasks.md", "handoff.md")


# --------------------------------------------------------------------------
# Repository and configuration
# --------------------------------------------------------------------------


def find_root(start: Path | None = None) -> Path:
    """Walk up from `start` until the config file is found."""
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / CONFIG_NAME).is_file():
            return candidate
    raise FileNotFoundError(f"{CONFIG_NAME} not found above {here}")


def load_config(root: Path) -> dict:
    with (root / CONFIG_NAME).open(encoding="utf-8") as handle:
        return json.load(handle)


def matches_any(path: str, globs: list[str]) -> bool:
    """Glob match on a POSIX relative path; `**/` also matches the top level."""
    for pattern in globs:
        if fnmatch.fnmatch(path, pattern):
            return True
        if pattern.startswith("**/") and fnmatch.fnmatch(path, pattern[3:]):
            return True
    return False


def iter_text_files(root: Path, config: dict):
    skip = set(config.get("skip_dirs", []))
    exts = set(config.get("text_extensions", []))
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in skip for part in rel.parts):
            continue
        if path.is_file() and path.suffix in exts:
            yield path


# --------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------


@dataclass
class Row:
    id: str
    status: str
    refs: list[str]
    file: str
    line: int

    @property
    def active(self) -> bool:
        return self.status == "active"

    @property
    def replaced_by(self) -> str | None:
        match = re.match(r"replaced by ((?:REQ|AC)-[A-Z][A-Z0-9]{0,9}-\d{3})$", self.status)
        return match.group(1) if match else None


@dataclass
class Task:
    id: str
    tag: str
    done: bool
    title: str
    change: str
    file: str
    line: int
    fields: dict[str, str] = field(default_factory=dict)

    def field_ids(self, key: str, pattern: re.Pattern[str]) -> list[str]:
        return pattern.findall(self.fields.get(key, ""))


@dataclass
class Change:
    name: str
    path: Path
    archived: bool
    code: str | None = None
    behavior_change: str | None = None
    specs_touched: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)


@dataclass
class Spec:
    area: str
    path: Path
    code: str | None
    criteria: list[Row]


@dataclass
class Project:
    root: Path
    config: dict
    requirements: list[Row]
    specs: list[Spec]
    changes: list[Change]
    awaits: list[tuple[str, str, int]]  # task id, file, line
    ac_mentions_in_tests: list[tuple[str, str, int]]

    @property
    def criteria(self) -> list[Row]:
        return [row for spec in self.specs for row in spec.criteria]

    @property
    def tasks(self) -> list[Task]:
        return [task for change in self.changes for task in change.tasks]

    def task(self, task_id: str) -> Task | None:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None


# --------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def parse_table_rows(root: Path, path: Path, kind: str) -> list[Row]:
    rows: list[Row] = []
    if not path.is_file():
        return rows
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = TABLE_ROW_RE.match(line)
        if not match or not match.group("id").startswith(kind + "-"):
            continue
        cells = [cell.strip() for cell in match.group("rest").split("|")]
        status = cells[-1] if cells else ""
        middle = " ".join(cells[:-1])
        refs = REQ_RE.findall(middle) if kind == "AC" else []
        rows.append(Row(match.group("id"), status, refs, rel(root, path), number))
    return rows


def header_value(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, re.M)
    return match.group(1) if match else None


def parse_spec(root: Path, path: Path) -> Spec:
    text = path.read_text(encoding="utf-8")
    return Spec(
        area=path.parent.name,
        path=path,
        code=header_value(text, "Area code"),
        criteria=parse_table_rows(root, path, "AC"),
    )


def parse_tasks(root: Path, path: Path, change: str) -> list[Task]:
    tasks: list[Task] = []
    current: Task | None = None
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = TASK_LINE_RE.match(line)
        if match:
            current = Task(
                id=match.group("id"),
                tag=match.group("tag"),
                done=match.group("done") in "xX",
                title=match.group("title").strip(),
                change=change,
                file=rel(root, path),
                line=number,
            )
            tasks.append(current)
            continue
        field_match = TASK_FIELD_RE.match(line)
        if field_match and current is not None:
            current.fields[field_match.group("key").strip().lower()] = field_match.group("value")
        elif line.strip() and not line.startswith(" "):
            current = None
    return tasks


def parse_change(root: Path, path: Path, archived: bool) -> Change:
    change = Change(name=path.name, path=path, archived=archived)
    proposal = path / "proposal.md"
    if proposal.is_file():
        text = proposal.read_text(encoding="utf-8")
        change.code = header_value(text, "Change code")
        change.behavior_change = (header_value(text, "Behavior change") or "").lower() or None
        touched = header_value(text, "Specs touched") or ""
        change.specs_touched = [
            item.strip().strip("`") for item in touched.split(",") if item.strip() and item.strip() != "none"
        ]
    tasks_file = path / "tasks.md"
    if tasks_file.is_file():
        change.tasks = parse_tasks(root, tasks_file, path.name)
    return change


def load_project(root: Path) -> Project:
    config = load_config(root)
    templates = {root / item for item in config.get("template_dirs", [])}
    specs_dir = root / config["specs_dir"]
    changes_dir = root / config["changes_dir"]
    archive_dir = root / config["archive_dir"]

    specs = [
        parse_spec(root, path)
        for path in sorted(specs_dir.glob("*/spec.md"))
        if path.parent not in templates
    ]
    changes: list[Change] = []
    if changes_dir.is_dir():
        for path in sorted(changes_dir.iterdir()):
            if path.is_dir() and path not in templates and path != archive_dir:
                changes.append(parse_change(root, path, archived=False))
    if archive_dir.is_dir():
        for path in sorted(archive_dir.iterdir()):
            if path.is_dir():
                changes.append(parse_change(root, path, archived=True))

    awaits: list[tuple[str, str, int]] = []
    ac_mentions: list[tuple[str, str, int]] = []
    for path in iter_text_files(root, config):
        relative = rel(root, path)
        if not matches_any(relative, config.get("test_globs", [])):
            continue
        if matches_any(relative, config.get("test_scan_exclude", [])):
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for pattern in AWAITS_RES:
                for match in pattern.finditer(line):
                    awaits.append((match.group("id"), relative, number))
            for ac in AC_RE.findall(line):
                ac_mentions.append((ac, relative, number))

    return Project(
        root=root,
        config=config,
        requirements=[row for path in sorted(root.glob(config["requirements_files"])) for row in parse_table_rows(root, path, "REQ")],
        specs=specs,
        changes=changes,
        awaits=awaits,
        ac_mentions_in_tests=ac_mentions,
    )


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")

    @property
    def ok(self) -> bool:
        return not self.errors


def _check_status(report: Report, row: Row, known: set[str]) -> None:
    if row.status in ("active", "removed"):
        return
    target = row.replaced_by
    if target is None:
        report.error(f"{row.file}:{row.line}", f"{row.id} has unknown status '{row.status}' (use active, removed or 'replaced by <ID>')")
    elif target not in known:
        report.error(f"{row.file}:{row.line}", f"{row.id} is replaced by {target}, which does not exist")


def check_requirements(project: Project, report: Report) -> None:
    seen: dict[str, Row] = {}
    for row in project.requirements:
        if row.id in seen:
            report.error(f"{row.file}:{row.line}", f"duplicate requirement {row.id}")
        seen[row.id] = row
    for row in project.requirements:
        _check_status(report, row, set(seen))


def check_specs(project: Project, report: Report) -> None:
    requirements = {row.id: row for row in project.requirements}
    seen: dict[str, Row] = {}
    codes: dict[str, str] = {}
    for spec in project.specs:
        where = rel(project.root, spec.path)
        if not spec.code or not CODE_RE.match(spec.code):
            report.error(where, "missing or invalid 'Area code:' line (2-10 capital letters or digits)")
            continue
        if spec.code in codes:
            report.error(where, f"area code {spec.code} is already used by {codes[spec.code]}")
        codes[spec.code] = where
        if not spec.criteria:
            report.warn(where, "no acceptance criteria yet")
        for row in spec.criteria:
            if not row.id.startswith(f"AC-{spec.code}-"):
                report.error(f"{row.file}:{row.line}", f"{row.id} must use the area code {spec.code}")
            if row.id in seen:
                report.error(f"{row.file}:{row.line}", f"duplicate criterion {row.id}")
            seen[row.id] = row
            if row.active and not row.refs:
                report.error(f"{row.file}:{row.line}", f"{row.id} lists no requirement")
            for ref in row.refs:
                if ref not in requirements:
                    report.error(f"{row.file}:{row.line}", f"{row.id} refers to unknown {ref}")
                elif row.active and not requirements[ref].active:
                    report.error(f"{row.file}:{row.line}", f"active {row.id} refers to {ref}, which is {requirements[ref].status}")
    for row in project.criteria:
        _check_status(report, row, set(seen))


def check_changes(project: Project, report: Report) -> None:
    criteria = {row.id: row for row in project.criteria}
    codes: dict[str, str] = {}
    task_ids: dict[str, Task] = {}
    for change in project.changes:
        where = rel(project.root, change.path)
        if not CHANGE_DIR_RE.match(change.name):
            report.error(where, "folder name must be YYYY-MM-DD-short-slug")
        for name in CHANGE_FILES:
            if not (change.path / name).is_file():
                report.error(where, f"missing {name}")
        if not change.code or not CODE_RE.match(change.code):
            report.error(f"{where}/proposal.md", "missing or invalid 'Change code:' line")
        elif change.code in codes:
            report.error(f"{where}/proposal.md", f"change code {change.code} is already used by {codes[change.code]}")
        else:
            codes[change.code] = where
        if change.behavior_change not in ("yes", "no"):
            report.error(f"{where}/proposal.md", "'Behavior change:' must be yes or no")
        if change.behavior_change == "yes":
            if not change.specs_touched:
                report.error(f"{where}/proposal.md", "behavior changes but 'Specs touched:' is empty")
            if not any(task.tag == "SPEC" for task in change.tasks):
                report.error(f"{where}/tasks.md", "behavior changes but there is no [SPEC] task")
        for spec_path in change.specs_touched:
            if not change.archived and not (project.root / spec_path).is_file():
                report.error(f"{where}/proposal.md", f"'Specs touched' lists {spec_path}, which does not exist")
        for task in change.tasks:
            loc = f"{task.file}:{task.line}"
            if task.id in task_ids:
                report.error(loc, f"duplicate task {task.id} (also in {task_ids[task.id].file})")
            task_ids[task.id] = task
            if change.code and not task.id.startswith(f"T-{change.code}-"):
                report.error(loc, f"{task.id} must use the change code {change.code}")
            if task.tag not in TAGS:
                report.error(loc, f"unknown tag [{task.tag}]; use one of {', '.join(sorted(TAGS))}")
            if change.archived:
                continue
            for ac in task.field_ids("covers", AC_RE):
                if ac not in criteria:
                    report.error(loc, f"{task.id} covers unknown {ac}")
                elif not criteria[ac].active:
                    report.error(loc, f"{task.id} covers {ac}, which is {criteria[ac].status}")
    for task in project.tasks:
        for dep in task.field_ids("depends on", TASK_RE):
            if dep not in task_ids:
                report.error(f"{task.file}:{task.line}", f"{task.id} depends on unknown {dep}")
            elif task.done and not task_ids[dep].done:
                report.error(f"{task.file}:{task.line}", f"{task.id} is ticked but its dependency {dep} is not")


def check_tests(project: Project, report: Report) -> None:
    tasks = {task.id: task for task in project.tasks}
    awaited = set()
    for task_id, file, line in project.awaits:
        awaited.add(task_id)
        task = tasks.get(task_id)
        if task is None:
            report.error(f"{file}:{line}", f"test awaits unknown task {task_id}")
        elif task.tag != "IMPL":
            report.error(f"{file}:{line}", f"test awaits {task_id}, which is [{task.tag}], not [IMPL]")
    criteria = {row.id: row for row in project.criteria}
    for ac, file, line in project.ac_mentions_in_tests:
        row = criteria.get(ac)
        if row is None:
            report.error(f"{file}:{line}", f"test refers to unknown {ac}")
        elif not row.active:
            report.error(f"{file}:{line}", f"test refers to {ac}, which is {row.status}: update it through a [TEST-CHANGE] task")
    for task in project.tasks:
        if task.tag == "IMPL" and task.done and task.id not in awaited and "tests" not in task.fields:
            report.warn(f"{task.file}:{task.line}", f"{task.id} is done but no test awaits it (add 'Tests: none, <reason>' if intended)")


def check_language(project: Project, report: Report) -> None:
    settings = project.config.get("language_check", {})
    if not settings.get("enabled", False):
        return
    allow = settings.get("allow", [])
    for path in iter_text_files(project.root, project.config):
        relative = rel(project.root, path)
        if matches_any(relative, allow):
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            bad = [ch for ch in line if ch.isalpha() and ord(ch) > 0x024F]
            if bad:
                report.error(f"{relative}:{number}", f"non-Latin letters ({''.join(bad[:5])}): the repository is English only")
                break


def check_project(project: Project) -> Report:
    report = Report()
    check_requirements(project, report)
    check_specs(project, report)
    check_changes(project, report)
    check_tests(project, report)
    check_language(project, report)
    return report
