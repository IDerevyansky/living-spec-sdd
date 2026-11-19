import shutil
import tempfile
import unittest
from pathlib import Path

from tools.close_change import blockers, close_change
from tools.lsdd.core import check_project, load_project
from tools.new_change import create_change
from tools.remove_example import remove_example
from tools.tests.helpers import REPO, TempRepo


class NewChangeTests(unittest.TestCase):
    def setUp(self):
        self.repo = TempRepo()

    def tearDown(self):
        self.repo.cleanup()

    def test_creates_folder_from_template(self):
        target = create_change(self.repo.root, "add-tags", "TAGS", "Add tags", "2026-02-03")
        self.assertEqual(target.name, "2026-02-03-add-tags")
        for name in ("proposal.md", "plan.md", "tasks.md", "handoff.md"):
            self.assertTrue((target / name).is_file())
        proposal = (target / "proposal.md").read_text()
        self.assertIn("Change code: TAGS", proposal)
        self.assertIn("# Change: Add tags", proposal)
        self.assertIn("T-TAGS-01 [SPEC]", (target / "tasks.md").read_text())

    def test_rejects_used_code(self):
        with self.assertRaises(ValueError):
            create_change(self.repo.root, "again", "FEAT", "Again", "2026-02-03")

    def test_rejects_bad_slug_and_code(self):
        with self.assertRaises(ValueError):
            create_change(self.repo.root, "Bad Slug", "OK", "x", "2026-02-03")
        with self.assertRaises(ValueError):
            create_change(self.repo.root, "ok", "lower", "x", "2026-02-03")


class CloseChangeTests(unittest.TestCase):
    def setUp(self):
        self.repo = TempRepo()

    def tearDown(self):
        self.repo.cleanup()

    def tick_all(self, name="2026-01-01-feature"):
        tasks = self.repo.root / "changes" / name / "tasks.md"
        tasks.write_text(tasks.read_text().replace("- [ ]", "- [x]"))

    def test_open_tasks_block_closing(self):
        problems = blockers(self.repo.root, "2026-01-01-feature")
        self.assertIn("T-FEAT-02 [TEST] is not ticked", problems)

    def test_behavior_change_needs_a_done_spec_task(self):
        self.repo.write_change("2026-01-02-x", code="XX", tasks="- [x] T-XX-01 [IMPL] code\n")
        problems = blockers(self.repo.root, "2026-01-02-x")
        self.assertTrue(any("no ticked [SPEC] task" in p for p in problems))

    def test_closing_moves_to_archive(self):
        self.tick_all()
        errors = close_change(self.repo.root, "2026-01-01-feature")
        self.assertEqual(errors, [])
        self.assertFalse((self.repo.root / "changes/2026-01-01-feature").exists())
        self.assertTrue((self.repo.root / "changes/archive/2026-01-01-feature/tasks.md").is_file())

    def test_unknown_change(self):
        self.assertEqual(blockers(self.repo.root, "2026-09-09-nope"), ["no change folder named 2026-09-09-nope"])


class RemoveExampleTests(unittest.TestCase):
    def test_repository_without_example_is_still_valid(self):
        if not (REPO / "specs/notes").exists():
            self.skipTest("the example was already removed from this repository")
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(REPO, copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            for change in (copy / "changes").iterdir():
                if change.name not in ("_template", "archive", "README.md"):
                    shutil.rmtree(change)
            removed = remove_example(copy)
            self.assertIn("specs/notes", removed)
            self.assertFalse((copy / "src/notes").exists())
            self.assertEqual(check_project(load_project(copy)).errors, [])


if __name__ == "__main__":
    unittest.main()
