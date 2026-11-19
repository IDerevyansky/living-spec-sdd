# Task rules

## Format

In `changes/<folder>/tasks.md`:

```
- [ ] T-TAGS-02 [TEST] Tests for tag limits
  - Covers: AC-NOTES-007, AC-NOTES-008
  - Depends on: T-TAGS-01
  - Files: tests/test_tags.py
  - Done when: one test per criterion, each awaiting T-TAGS-03.
```

- ID: `T-<CHANGE CODE>-NN`, numbered in order, never reused.
- `Covers:` criterion IDs from living specs (must be `active`).
- `Depends on:` task IDs or `none`. A task is ready when all its dependencies
  are ticked.
- `Files:` the files the task may change. Touching others needs a reason in
  the pull request.
- `Done when:` a checkable sentence.
- Optional `Tests: none, <reason>` for an `[IMPL]` task that has no tests.

## Tags

| Tag | Who | May change |
| --- | --- | --- |
| `[SPEC]` | Agent or person; owner approves | Living specs, `core/requirements/` |
| `[TEST]` | Agent or person; owner reviews closely | Test files and fixtures only |
| `[IMPL]` | Agent or person | Product code; never protected paths (`living-spec.json`) |
| `[TEST-CHANGE]` | Proposed by anyone, approved by the owner | Tests, when a test is wrong or a criterion was replaced |
| `[DOCS]` | Anyone | Documentation |
| `[CHORE]` | Anyone | Tooling, dependencies, configuration, archiving |
| `[OWNER]` | A person only | Decisions, accounts, settings outside the repository |

## Size

One task = one sitting = one pull request, about 300 changed lines or less
(generated files and lock files aside). Bigger: split it before starting.

## Order

`[SPEC]` → `[TEST]` → `[IMPL]` for each piece of behavior. Several pieces can
run in parallel when their tasks do not depend on each other.

## Claiming

Open a draft pull request (or assign yourself on the tracker issue) as soon as
you start a task. `task_status.py --next` lists ready tasks; skip those with
an open draft.
