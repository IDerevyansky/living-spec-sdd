import unittest

from tools.lsdd import awaits as awaits_module
from tools.lsdd.awaits import awaits
from tools.tests.helpers import TempRepo


class AwaitsTests(unittest.TestCase):
    def setUp(self):
        self.repo = TempRepo()  # T-FEAT-03 [IMPL] is not ticked; T-FEAT-01 is ticked
        awaits_module._DONE_CACHE.clear()

    def tearDown(self):
        awaits_module._DONE_CACHE.clear()
        self.repo.cleanup()

    def test_pending_failing_test_is_skipped(self):
        @awaits("T-FEAT-03", root=self.repo.root)
        def failing():
            raise AssertionError("not built")

        with self.assertRaises(unittest.SkipTest) as context:
            failing()
        self.assertIn("awaits T-FEAT-03", str(context.exception))

    def test_pending_passing_test_passes(self):
        @awaits("T-FEAT-03", root=self.repo.root)
        def passing():
            return None

        self.assertIsNone(passing())

    def test_done_task_makes_the_test_blocking(self):
        tasks = self.repo.root / "changes/2026-01-01-feature/tasks.md"
        tasks.write_text(tasks.read_text().replace("- [ ] T-FEAT-03", "- [x] T-FEAT-03"))

        @awaits("T-FEAT-03", root=self.repo.root)
        def failing():
            raise AssertionError("still broken")

        with self.assertRaises(AssertionError):
            failing()

    def test_marker_is_kept_on_the_function(self):
        @awaits("T-FEAT-03", root=self.repo.root)
        def some_test():
            return None

        self.assertEqual(getattr(some_test, "__awaits__"), "T-FEAT-03")
        self.assertEqual(some_test.__name__, "some_test")


if __name__ == "__main__":
    unittest.main()
