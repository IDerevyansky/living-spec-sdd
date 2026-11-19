# Testing policy

The rules exist because an agent can make a red build green by weakening the
tests. That must be impossible, not just forbidden.

## Tests first

1. Tests are written in a `[TEST]` task from the acceptance criteria of the
   living spec, before the code.
2. Each test names its criterion ID: in the test name or docstring
   (`AC-NOTES-003`). The spec check fails when a test refers to a criterion
   that is replaced or removed.
3. Each test carries the `awaits` marker of the `[IMPL]` task that will make
   it pass:
   - Python: `from tools.lsdd.awaits import awaits` and `@awaits("T-CODE-NN")`.
   - Other languages: put `[awaits:T-CODE-NN]` in the test name and let the
     runner read `python tools/task_status.py --json` (done and pending task
     IDs) to treat failures of pending tasks as skipped.
4. While the `[IMPL]` box is not ticked, a failing awaiting test is reported
   as skipped. When the box is ticked, the test runs normally and must pass.
   Never edit or remove a marker.

## Implementation never weakens tests

An `[IMPL]` pull request must not:

- change any protected path (`living-spec.json` → `protected_for_impl`):
  tests, fixtures, golden data, thresholds, specs, core files, workflows,
  agent rules, tools;
- add escape hatches (`living-spec.json` → `escape_hatches`): skip, only,
  todo, ignore comments, coverage pragmas.

`tools/guard.py` checks both in CI. The pull request kind comes from its label
or from the task box it ticks.

## When a test is wrong

Stop. Explain in the change's `handoff.md` and the pull request, and propose a
`[TEST-CHANGE]` task. Only the owner approves it. The implementation waits.

## Good tests

- Mock only the outside world (network, clock, third-party services).
- Deterministic: fixed seeds, frozen time, no network in unit tests.
- One behavior per test; the name says which criterion and what.
- Boundaries: every limit in a criterion gets a test on both sides.
