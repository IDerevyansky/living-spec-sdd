# Prompt: implement (`[IMPL]` task)

The argument is the task ID.

1. Read `AGENTS.md` sections 2 and 4.
2. Find the tests that await this task: search for `awaits("<task-id>")` and
   `[awaits:<task-id>]`. They define "done".
3. If the task changes user interface, first do the step in
   `docs/workflow/ui-references.md` and keep the links for the pull request.
4. Write the smallest clear code that makes them pass, only in the files the
   task lists, following the change's `plan.md`.
5. Never touch protected paths (tests, fixtures, specs, `core/`, rules,
   workflows, `tools/`, `living-spec.json`) and never add escape hatches
   (skip, only, todo, ignore comments, coverage pragmas).
6. If a test looks wrong or contradicts the spec, stop. Do not change the test
   and do not bend the code to it. Explain in `handoff.md` and the chat and
   propose a `[TEST-CHANGE]` task.
7. Tick the task box, then run `make check`: the awaiting tests are now
   blocking and must pass.
8. Continue with steps 7–9 of `docs/prompts/next-task.md`. Label `impl`.
