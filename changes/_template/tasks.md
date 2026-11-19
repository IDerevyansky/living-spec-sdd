# Tasks: {{TITLE}}

Rules: `docs/workflow/task-rules.md`. One task, one branch, one pull request.
Tick the box in the same pull request that does the task.

- [ ] T-{{CODE}}-01 [SPEC] Update the living spec
  - Covers: none yet (this task creates the criteria)
  - Depends on: none
  - Files: specs/<area>/spec.md, core/requirements/<area>.md
  - Done when: new or replaced criteria are in the spec with stable IDs; the spec's History table has a row for this change.

- [ ] T-{{CODE}}-02 [TEST] Tests for the new criteria
  - Covers: AC-AREA-NNN
  - Depends on: T-{{CODE}}-01
  - Files: tests/…
  - Done when: each covered criterion has tests marked `awaits("T-{{CODE}}-03")`; they fail only because the code is missing.

- [ ] T-{{CODE}}-03 [IMPL] Make the tests pass
  - Covers: AC-AREA-NNN
  - Depends on: T-{{CODE}}-02
  - Files: src/…
  - Done when: all tests awaiting this task pass after the box is ticked; no test, spec or rule file changed.
