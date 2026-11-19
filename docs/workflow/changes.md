# Life of a change

A change is one unit of work with its own folder in `changes/`. It is the only
place where work happens; the living specs are the only place where the
result is described.

## 1. Open

1. Create the folder:
   `make new-change SLUG=add-tags CODE=TAGS TITLE="Add tags to notes"`
   (or ask an agent: `/new-change add tags to notes`).
2. Fill `proposal.md`: why, what changes, out of scope, `Behavior change:
   yes|no`, `Specs touched:`.
3. Fill `plan.md` (how) and `tasks.md` (small tasks, `docs/workflow/task-rules.md`).
4. Open a draft pull request with the folder. The owner approves the proposal
   by merging it. From now on the change is visible to everyone, so nobody
   starts the same work twice.

## 2. Change the living spec (`[SPEC]` task)

Only if `Behavior change: yes`.

- Add new criteria at the end of the spec's table with the next free
  `AC-<AREA>-NNN`.
- For a changed rule: add the new row and set the old row's status to
  `replaced by AC-<AREA>-NNN`. For a dropped rule: set `removed`.
- Add requirements to `core/requirements/<area>.md` the same way.
- Add a row to the spec's History table: date, change folder, what changed.
- Fill `Covers:` in the following tasks with the new criterion IDs.

If two changes edit the same part of the same spec, git shows a conflict in the
second pull request. That is intended: two changes disagree about behavior and
a person decides (`docs/workflow/team.md`).

## 3. Tests (`[TEST]` task)

Tests for every covered criterion, named after the criterion and marked
`awaits("T-CODE-NN")` with the `[IMPL]` task. They are merged before the code
exists; until the `[IMPL]` box is ticked, a failing awaiting test shows as
skipped.

## 4. Code (`[IMPL]` task)

Make the awaiting tests pass. Tick the box in the same pull request: from that
moment the tests are blocking. Never touch tests, specs or rules (the guard in
CI rejects it).

## 5. Close

When every task is ticked: `make close-change CHANGE=<folder>` (or
`/close-change <folder>`). It checks that all boxes are ticked and that a
behavior change has a ticked `[SPEC]` task, then moves the folder to
`changes/archive/`. Commit that in a small `chore` pull request.

## Changes without behavior change

Refactoring, tooling, docs: `Behavior change: no`, `Specs touched: none`, tasks
tagged `[CHORE]` or `[DOCS]`. Tests still must stay green.

## If the requirements move while you work

- The proposal is wrong: stop, update `proposal.md`, ask the owner.
- A criterion must change after its tests were merged: a new `[SPEC]` task
  replaces the criterion (new ID), then a `[TEST-CHANGE]` task updates the
  tests. The spec check fails on any test or open task that still points to
  the replaced ID, so nothing is forgotten.
