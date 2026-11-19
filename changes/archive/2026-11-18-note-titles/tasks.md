# Tasks: Validate note titles

- [x] T-TITLE-01 [SPEC] Add title validation to the notes spec
  - Covers: none yet (this task creates the criteria)
  - Depends on: none
  - Files: specs/notes/spec.md, core/requirements/notes.md
  - Done when: AC-NOTES-001, AC-NOTES-003, AC-NOTES-004 are active; AC-NOTES-002 is replaced by AC-NOTES-003.

- [x] T-TITLE-02 [TEST] Tests for title validation
  - Covers: AC-NOTES-001, AC-NOTES-003, AC-NOTES-004
  - Depends on: T-TITLE-01
  - Files: tests/test_note_titles.py
  - Done when: one test per criterion, each marked awaits T-TITLE-03.

- [x] T-TITLE-03 [IMPL] Implement title validation
  - Covers: AC-NOTES-001, AC-NOTES-003, AC-NOTES-004
  - Depends on: T-TITLE-02
  - Files: src/notes/titles.py, src/notes/__init__.py
  - Done when: the awaiting tests pass.
