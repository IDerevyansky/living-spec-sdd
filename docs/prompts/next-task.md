# Prompt: next task

The argument may be a task ID. Do exactly one task, open one pull request,
stop.

1. Read `AGENTS.md`, then `python tools/task_status.py --next`.
2. Choose the task:
   - if a task ID was given, take it only if it appears in the ready list;
   - otherwise take the first ready task that is not `[OWNER]` and has no open
     pull request or draft for it (check with `gh pr list` if available);
   - list ready `[OWNER]` tasks for the owner and do not do them;
   - if nothing is ready, report why and stop.
3. Read the change folder (`proposal.md`, `plan.md`, `handoff.md`) and the
   living specs and criteria the task covers.
4. Create a branch `<code-lowercase>/<task-id>-<short-name>` from the latest
   default branch.
5. Do the task by its tag:
   - `[SPEC]` → `docs/workflow/changes.md` section 2;
   - `[TEST]` → `docs/prompts/write-tests.md`;
   - `[IMPL]` → `docs/prompts/implement.md`;
   - `[DOCS]`, `[CHORE]` → change only the files the task names;
   - `[TEST-CHANGE]` → only with the owner's approval written in the task.
6. Run `make check` and make it green.
7. Tick the task box in `tasks.md`; add an entry at the top of the change's
   `handoff.md`.
8. Commit `<task-id>: <summary>`, push, open a pull request with the template,
   label it by the tag.
9. Stop after this one task. Report in the owner's language: what you did, the
   pull request link, what is next, questions.
