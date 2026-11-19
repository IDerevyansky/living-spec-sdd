"""Build small throwaway repositories for the tool tests."""

from __future__ import annotations

import shutil
import tempfile
import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


class TempRepo:
    """A minimal valid repository: one area (ALPHA), one open change (FEAT)."""

    def __init__(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.root = Path(self._dir.name)
        shutil.copy(REPO / "living-spec.json", self.root / "living-spec.json")
        shutil.copytree(REPO / "changes" / "_template", self.root / "changes" / "_template")
        shutil.copytree(REPO / "specs" / "_template", self.root / "specs" / "_template")
        self.write("core/requirements/alpha.md", """
            | ID | Requirement | Status |
            | --- | --- | --- |
            | REQ-ALPHA-001 | First need | active |
            """)
        self.write("specs/alpha/spec.md", """
            # Spec: Alpha

            Area code: ALPHA

            | ID | Criterion | Requirements | Status |
            | --- | --- | --- | --- |
            | AC-ALPHA-001 | Old rule | REQ-ALPHA-001 | replaced by AC-ALPHA-002 |
            | AC-ALPHA-002 | New rule | REQ-ALPHA-001 | active |
            """)
        self.write_change("2026-01-01-feature", code="FEAT", tasks="""
            - [x] T-FEAT-01 [SPEC] Spec
              - Depends on: none
            - [ ] T-FEAT-02 [TEST] Tests
              - Covers: AC-ALPHA-002
              - Depends on: T-FEAT-01
            - [ ] T-FEAT-03 [IMPL] Code
              - Covers: AC-ALPHA-002
              - Depends on: T-FEAT-02
            """)

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")
        return path

    def write_change(
        self,
        name: str,
        code: str,
        tasks: str,
        behavior: str = "yes",
        specs: str = "specs/alpha/spec.md",
        base: str = "changes",
    ) -> Path:
        folder = f"{base}/{name}"
        self.write(f"{folder}/proposal.md", f"""
            # Change: test

            Change code: {code}
            Behavior change: {behavior}
            Specs touched: {specs}
            """)
        self.write(f"{folder}/plan.md", "# Plan\n")
        self.write(f"{folder}/handoff.md", "# Handoff\n")
        self.write(f"{folder}/tasks.md", tasks)
        return self.root / folder

    def cleanup(self) -> None:
        self._dir.cleanup()
