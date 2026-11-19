"""Close a finished change: check it and move it to changes/archive/.

Usage: python tools/close_change.py 2026-11-18-add-tags
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.lsdd.core import check_project, find_root, load_project


def blockers(root: Path, name: str) -> list[str]:
    project = load_project(root)
    change = next((c for c in project.changes if c.name == name), None)
    if change is None:
        return [f"no change folder named {name}"]
    if change.archived:
        return [f"{name} is already archived"]
    problems = [f"{task.id} [{task.tag}] is not ticked" for task in change.tasks if not task.done]
    if not change.tasks:
        problems.append("tasks.md has no tasks")
    if change.behavior_change == "yes" and not any(t.tag == "SPEC" and t.done for t in change.tasks):
        problems.append("behavior changes but no ticked [SPEC] task updated the living spec")
    return problems


def move(root: Path, source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if (root / ".git").exists() and shutil.which("git"):
        result = subprocess.run(["git", "mv", str(source), str(target)], cwd=root, capture_output=True, text=True)
        if result.returncode == 0:
            return
    shutil.move(str(source), str(target))


def close_change(root: Path, name: str) -> list[str]:
    problems = blockers(root, name)
    if problems:
        return problems
    project = load_project(root)
    source = root / project.config["changes_dir"] / name
    target = root / project.config["archive_dir"] / name
    move(root, source, target)
    report = check_project(load_project(root))
    return report.errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("change", help="change folder name, for example 2026-11-18-add-tags")
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args(argv)
    name = Path(args.change).name
    problems = close_change(find_root(args.root), name)
    if problems:
        for line in problems:
            print(f"error: {line}")
        return 1
    print(f"closed {name}: moved to the archive; the living specs already describe it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
