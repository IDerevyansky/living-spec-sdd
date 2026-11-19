import unittest

from tools.lsdd.core import check_project, load_project
from tools.tests.helpers import TempRepo


class SpecCheckTests(unittest.TestCase):
    def setUp(self):
        self.repo = TempRepo()

    def tearDown(self):
        self.repo.cleanup()

    def check(self):
        return check_project(load_project(self.repo.root))

    def assertError(self, fragment):
        report = self.check()
        self.assertTrue(any(fragment in e for e in report.errors), f"no error with '{fragment}' in {report.errors}")

    # ---- baseline -------------------------------------------------------

    def test_minimal_repository_is_valid(self):
        report = self.check()
        self.assertEqual(report.errors, [])

    # ---- requirements and specs ----------------------------------------

    def test_duplicate_requirement(self):
        self.repo.write("core/requirements/beta.md", "| REQ-ALPHA-001 | Again | active |\n")
        self.assertError("duplicate requirement REQ-ALPHA-001")

    def test_unknown_status(self):
        self.repo.write("core/requirements/beta.md", "| REQ-ALPHA-009 | Thing | maybe |\n")
        self.assertError("unknown status 'maybe'")

    def test_replaced_by_missing_target(self):
        self.repo.write("core/requirements/beta.md", "| REQ-ALPHA-009 | Thing | replaced by REQ-ALPHA-777 |\n")
        self.assertError("replaced by REQ-ALPHA-777, which does not exist")

    def test_missing_area_code(self):
        self.repo.write("specs/beta/spec.md", "# Spec: Beta\n")
        self.assertError("missing or invalid 'Area code:'")

    def test_criterion_must_use_area_code(self):
        self.repo.write("specs/beta/spec.md", "Area code: BETA\n\n| AC-ALPHA-003 | x | REQ-ALPHA-001 | active |\n")
        self.assertError("AC-ALPHA-003 must use the area code BETA")

    def test_criterion_refers_to_unknown_requirement(self):
        self.repo.write("specs/beta/spec.md", "Area code: BETA\n\n| AC-BETA-001 | x | REQ-BETA-404 | active |\n")
        self.assertError("refers to unknown REQ-BETA-404")

    def test_active_criterion_needs_a_requirement(self):
        self.repo.write("specs/beta/spec.md", "Area code: BETA\n\n| AC-BETA-001 | x | none | active |\n")
        self.assertError("AC-BETA-001 lists no requirement")

    def test_duplicate_area_code(self):
        self.repo.write("specs/other/spec.md", "Area code: ALPHA\n")
        self.assertError("area code ALPHA is already used")

    # ---- changes and tasks ----------------------------------------------

    def test_change_folder_name(self):
        self.repo.write_change("feature-x", code="FX", tasks="- [ ] T-FX-01 [SPEC] s\n")
        self.assertError("folder name must be YYYY-MM-DD-short-slug")

    def test_change_missing_file(self):
        folder = self.repo.write_change("2026-01-02-x", code="XX", tasks="- [ ] T-XX-01 [SPEC] s\n")
        (folder / "plan.md").unlink()
        self.assertError("missing plan.md")

    def test_duplicate_change_code(self):
        self.repo.write_change("2026-01-02-x", code="FEAT", tasks="- [ ] T-FEAT-09 [SPEC] s\n")
        self.assertError("change code FEAT is already used")

    def test_behavior_change_needs_spec_task(self):
        self.repo.write_change("2026-01-02-x", code="XX", tasks="- [ ] T-XX-01 [IMPL] code\n")
        self.assertError("there is no [SPEC] task")

    def test_behavior_change_needs_specs_touched(self):
        self.repo.write_change("2026-01-02-x", code="XX", tasks="- [ ] T-XX-01 [SPEC] s\n", specs="none")
        self.assertError("'Specs touched:' is empty")

    def test_specs_touched_must_exist(self):
        self.repo.write_change("2026-01-02-x", code="XX", tasks="- [ ] T-XX-01 [SPEC] s\n", specs="specs/nope/spec.md")
        self.assertError("specs/nope/spec.md, which does not exist")

    def test_behavior_must_be_yes_or_no(self):
        self.repo.write_change("2026-01-02-x", code="XX", tasks="- [ ] T-XX-01 [DOCS] d\n", behavior="perhaps")
        self.assertError("'Behavior change:' must be yes or no")

    def test_task_must_use_change_code(self):
        self.repo.write_change("2026-01-02-x", code="XX", tasks="- [ ] T-YY-01 [DOCS] d\n", behavior="no", specs="none")
        self.assertError("T-YY-01 must use the change code XX")

    def test_unknown_tag(self):
        self.repo.write_change("2026-01-02-x", code="XX", tasks="- [ ] T-XX-01 [MAGIC] d\n", behavior="no", specs="none")
        self.assertError("unknown tag [MAGIC]")

    def test_duplicate_task(self):
        self.repo.write_change("2026-01-02-x", code="XX", tasks="- [ ] T-XX-01 [DOCS] a\n- [ ] T-XX-01 [DOCS] b\n", behavior="no", specs="none")
        self.assertError("duplicate task T-XX-01")

    def test_unknown_dependency(self):
        self.repo.write_change("2026-01-02-x", code="XX", tasks="- [ ] T-XX-01 [DOCS] a\n  - Depends on: T-XX-07\n", behavior="no", specs="none")
        self.assertError("depends on unknown T-XX-07")

    def test_ticked_task_with_open_dependency(self):
        self.repo.write_change("2026-01-02-x", code="XX", tasks="- [ ] T-XX-01 [DOCS] a\n- [x] T-XX-02 [DOCS] b\n  - Depends on: T-XX-01\n", behavior="no", specs="none")
        self.assertError("T-XX-02 is ticked but its dependency T-XX-01 is not")

    def test_open_task_cannot_cover_replaced_criterion(self):
        self.repo.write_change("2026-01-02-x", code="XX", tasks="- [ ] T-XX-01 [SPEC] s\n  - Covers: AC-ALPHA-001\n")
        self.assertError("covers AC-ALPHA-001, which is replaced by AC-ALPHA-002")

    def test_archived_change_may_cover_replaced_criterion(self):
        self.repo.write_change("2025-01-01-old", code="OLD", tasks="- [x] T-OLD-01 [SPEC] s\n  - Covers: AC-ALPHA-001\n", base="changes/archive")
        self.assertEqual(self.check().errors, [])

    # ---- tests ----------------------------------------------------------

    def test_awaits_unknown_task(self):
        self.repo.write("tests/test_x.py", 'from x import awaits\n@awaits("T-FEAT-99")\ndef test_a(): pass\n')
        self.assertError("test awaits unknown task T-FEAT-99")

    def test_awaits_must_name_impl_task(self):
        self.repo.write("tests/test_x.py", '@awaits("T-FEAT-02")\ndef test_a(): pass\n')
        self.assertError("which is [TEST], not [IMPL]")

    def test_awaits_marker_in_test_name(self):
        self.repo.write("web/app.test.ts", 'it("shows the title [awaits:T-FEAT-03]", () => {})\n')
        project = load_project(self.repo.root)
        self.assertIn(("T-FEAT-03", "web/app.test.ts", 1), project.awaits)
        self.assertEqual(check_project(project).errors, [])

    def test_test_refers_to_replaced_criterion(self):
        self.repo.write("tests/test_x.py", '"""AC-ALPHA-001"""\n')
        self.assertError("test refers to AC-ALPHA-001, which is replaced by AC-ALPHA-002")

    def test_done_impl_without_awaiting_test_is_a_warning(self):
        self.repo.write_change("2026-01-02-x", code="XX", tasks="- [x] T-XX-01 [IMPL] code\n", behavior="no", specs="none")
        report = self.check()
        self.assertEqual(report.errors, [])
        self.assertTrue(any("T-XX-01 is done but no test awaits it" in w for w in report.warnings))

    # ---- language -------------------------------------------------------

    def test_non_latin_letters_are_errors(self):
        self.repo.write("docs/note.md", "Hello \u043c\u0438\u0440\n")
        self.assertError("non-Latin letters")

    def test_latin_accents_and_symbols_are_fine(self):
        self.repo.write("docs/note.md", "Caf\u00e9 \u2014 a \u2192 b \u2264 c\n")
        self.assertEqual(self.check().errors, [])


if __name__ == "__main__":
    unittest.main()
