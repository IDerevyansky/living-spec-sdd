# Prompt: write tests (`[TEST]` task)

The argument is the task ID. You write tests only.

1. Read `AGENTS.md` section 4 and `docs/workflow/testing-policy.md`.
2. Read the task, its `Covers:` criteria in the living spec, and the change's
   `plan.md` (test strategy).
3. For each covered criterion write tests that:
   - name the criterion ID in the test name or docstring;
   - carry the `awaits` marker of the `[IMPL]` task that depends on this task;
   - check boundaries and error cases, so a wrong implementation fails, not
     only a missing one;
   - fake only the outside world, deterministically.
4. Change only test files and fixtures. Never product code.
5. Run the tests: they must fail or be skipped only because the code is
   missing, never because of a mistake in the test.
6. Continue with steps 6–9 of `docs/prompts/next-task.md`. Label `test`.
