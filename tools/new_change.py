"""Create a change folder from changes/_template.

Usage: python tools/new_change.py --slug add-tags --code TAGS --title "Add tags to notes"
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.lsdd.core import CODE_RE, find_root, load_project

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def create_change(root: Path, slug: str, code: str, title: str, date: str) -> Path:
    if not SLUG_RE.match(slug):
        raise ValueError("slug: lowercase letters, digits and dashes, for example add-tags")
    if not CODE_RE.match(code):
        raise ValueError("code: 2-10 capital letters or digits, starting with a letter, for example TAGS")
    project = load_project(root)
    used = {change.code for change in project.changes}
    if code in used:
        raise ValueError(f"change code {code} is already used")
    changes_dir = root / project.config["changes_dir"]
    target = changes_dir / f"{date}-{slug}"
    if target.exists():
        raise ValueError(f"{target.relative_to(root)} already exists")
    template = changes_dir / "_template"
    shutil.copytree(template, target)
    for path in target.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        text = text.replace("{{TITLE}}", title).replace("{{CODE}}", code).replace("{{DATE}}", date)
        path.write_text(text, encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--slug", required=True)
    parser.add_argument("--code", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args(argv)
    try:
        target = create_change(find_root(args.root), args.slug, args.code, args.title, args.date)
    except ValueError as error:
        print(f"error: {error}")
        return 1
    print(f"created {target}")
    print("next: fill proposal.md, then plan.md and tasks.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
