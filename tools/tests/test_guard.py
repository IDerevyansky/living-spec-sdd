import json
import unittest

from tools.lsdd.guard import Diff, evaluate, ticked_tasks
from tools.tests.helpers import REPO

CONFIG = json.loads((REPO / "living-spec.json").read_text(encoding="utf-8"))
TICK_IMPL = ["-- [ ] T-FEAT-03 [IMPL] Code", "+- [x] T-FEAT-03 [IMPL] Code"]
TICK_TEST = ["-- [ ] T-FEAT-02 [TEST] Tests", "+- [x] T-FEAT-02 [TEST] Tests"]
TASKS = "changes/2026-01-01-feature/tasks.md"


def diff(changed, added=(), task_lines=()):
    return Diff(changed=list(changed), added_lines=list(added), raw_task_lines=list(task_lines))


class GuardTests(unittest.TestCase):
    def test_ticked_tasks_need_an_unticked_line(self):
        self.assertEqual(ticked_tasks(diff([], task_lines=TICK_IMPL)), {"T-FEAT-03": "IMPL"})
        self.assertEqual(ticked_tasks(diff([], task_lines=["+- [x] T-FEAT-03 [IMPL] Code"])), {})

    def test_impl_may_change_code_and_its_change(self):
        kind, report = evaluate(diff(["src/a.py", TASKS], task_lines=TICK_IMPL), [], CONFIG)
        self.assertEqual(kind, "impl")
        self.assertEqual(report.errors, [])

    def test_impl_must_not_touch_tests(self):
        _, report = evaluate(diff(["src/a.py", "tests/test_a.py", TASKS], task_lines=TICK_IMPL), [], CONFIG)
        self.assertTrue(any(e.startswith("tests/test_a.py") for e in report.errors))

    def test_impl_must_not_touch_specs_or_rules(self):
        for path in ("specs/alpha/spec.md", "AGENTS.md", "living-spec.json", ".github/workflows/check.yml", "web/a.test.ts"):
            _, report = evaluate(diff(["src/a.py", TASKS, path], task_lines=TICK_IMPL), [], CONFIG)
            self.assertTrue(any(e.startswith(path) for e in report.errors), path)

    def test_impl_must_not_add_escape_hatches(self):
        added = [("src/a.py", "x = f()  # type: ignore"), ("web/b.ts", "// @ts-ignore")]
        _, report = evaluate(diff(["src/a.py", "web/b.ts", TASKS], added, TICK_IMPL), [], CONFIG)
        self.assertEqual(len([e for e in report.errors if "must not add" in e]), 2)

    def test_label_overrides_detection(self):
        kind, report = evaluate(diff(["src/a.py", "tests/test_a.py", TASKS]), ["impl"], CONFIG)
        self.assertEqual(kind, "impl")
        self.assertFalse(report.ok)

    def test_code_change_needs_a_change_folder(self):
        _, report = evaluate(diff(["src/a.py"]), ["chore"], CONFIG)
        self.assertTrue(any("no change folder was touched" in e for e in report.errors))

    def test_test_pull_request_must_not_change_code(self):
        _, report = evaluate(diff(["tests/test_a.py", "src/a.py", TASKS], task_lines=TICK_TEST), [], CONFIG)
        self.assertTrue(any("[TEST] pull request must not change product code" in e for e in report.errors))

    def test_docs_pull_request_is_fine(self):
        kind, report = evaluate(diff(["README.md"]), ["docs"], CONFIG)
        self.assertEqual(kind, "docs")
        self.assertTrue(report.ok)

    def test_unknown_kind_is_a_warning(self):
        kind, report = evaluate(diff(["README.md"]), [], CONFIG)
        self.assertEqual(kind, "unknown")
        self.assertTrue(report.ok)
        self.assertTrue(report.warnings)


if __name__ == "__main__":
    unittest.main()
