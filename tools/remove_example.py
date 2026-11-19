"""Remove the bundled example (the "notes" area) when you start a real project.

Usage: python tools/remove_example.py
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.lsdd.core import find_root

EXAMPLE_PATHS = (
    "specs/notes",
    "changes/archive/2026-11-18-note-titles",
    "src/notes",
    "tests/test_note_titles.py",
    "core/requirements/notes.md",
)
EXAMPLE_ROW = re.compile(r"^\| Note \| \(example area.*\n", re.M)


def remove_example(root: Path) -> list[str]:
    removed = []
    for item in EXAMPLE_PATHS:
        path = root / item
        if path.is_dir():
            shutil.rmtree(path)
            removed.append(item)
        elif path.is_file():
            path.unlink()
            removed.append(item)
    glossary = root / "core" / "glossary.md"
    if glossary.is_file():
        text = glossary.read_text(encoding="utf-8")
        cleaned = EXAMPLE_ROW.sub("", text)
        if cleaned != text:
            glossary.write_text(cleaned, encoding="utf-8")
            removed.append("core/glossary.md: example term")
    return removed


def main() -> int:
    removed = remove_example(find_root())
    for item in removed:
        print(f"removed {item}")
    print("example removed" if removed else "nothing to remove")
    return 0


if __name__ == "__main__":
    sys.exit(main())
