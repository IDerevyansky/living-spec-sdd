"""Show task status and the next tasks that are ready.

Usage:
  python tools/task_status.py            # table of open changes and their tasks
  python tools/task_status.py --next     # ready tasks (dependencies done), owner tasks listed apart
  python tools/task_status.py --json     # done and pending task ids, for other test runners
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.lsdd.core import TASK_RE, Project, Task, find_root, load_project


def ready(project: Project) -> list[Task]:
    done = {task.id for task in project.tasks if task.done}
    result = []
    for change in project.changes:
        if change.archived:
            continue
        for task in change.tasks:
            deps = task.field_ids("depends on", TASK_RE)
            if not task.done and all(dep in done for dep in deps):
                result.append(task)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Show task status")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--next", action="store_true")
    group.add_argument("--json", action="store_true")
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args(argv)
    project = load_project(find_root(args.root))

    if args.json:
        print(json.dumps({
            "done": sorted(t.id for t in project.tasks if t.done),
            "pending": sorted(t.id for t in project.tasks if not t.done),
        }, indent=2))
        return 0

    if args.next:
        tasks = ready(project)
        agent = [t for t in tasks if t.tag != "OWNER"]
        owner = [t for t in tasks if t.tag == "OWNER"]
        print("Ready for an agent or developer:" if agent else "No ready tasks for agents.")
        for task in agent:
            print(f"  {task.id} [{task.tag}] {task.title}  ({task.change})")
        if owner:
            print("Waiting for the owner:")
            for task in owner:
                print(f"  {task.id} [OWNER] {task.title}  ({task.change})")
        return 0

    open_changes = [c for c in project.changes if not c.archived]
    if not open_changes:
        print("No open changes.")
    for change in open_changes:
        done = sum(1 for t in change.tasks if t.done)
        print(f"{change.name}  [{change.code}]  {done}/{len(change.tasks)} done")
        for task in change.tasks:
            print(f"  [{'x' if task.done else ' '}] {task.id} [{task.tag}] {task.title}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
