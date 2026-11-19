# AGENTS.md

Rules for every AI coding agent and every person working in this repository.
Claude Code, OpenCode, GitHub Copilot and other tools read this file first.
If a chat instruction conflicts with this file, follow this file and say so.

This repository uses **living-spec SDD** (`METHOD.md`).

## 1. Where things are

| Path | What it holds |
| --- | --- |
| `core/constitution.md` | Principles. Everything else follows them |
| `core/glossary.md` | Words with a fixed meaning |
| `core/requirements/<area>.md` | Requirements with stable IDs `REQ-<AREA>-NNN` |
| `core/decisions/` | Decision records (why things are the way they are) |
| `specs/<area>/spec.md` | **Living specs: how the system behaves today. Single source of truth** |
| `changes/<date>-<slug>/` | One unit of work: `proposal.md`, `plan.md`, `tasks.md`, `handoff.md` |
| `changes/archive/` | Finished changes, for history |
| `docs/workflow/` | How we work: changes, tasks, tests, team work, reviews, UI references |
| `docs/prompts/` | Source text of the agent commands below |
| `tools/` | Checks and helpers (`make check`) |
| `living-spec.json` | Configuration of the checks (protected paths, test globs, escape hatches) |

## 2. Golden rules

1. **The living spec is the truth.** Read `specs/<area>/spec.md` before you
   change an area. If code and spec disagree, stop and ask.
2. **No code without a change.** Work only inside a change folder. If none
   fits, create one with `/new-change` and ask the owner to approve the
   proposal.
3. **Behavior changes start with the spec.** A `[SPEC]` task edits the living
   spec first; tests and code follow.
4. **Stable IDs.** Never reuse, renumber or rewrite `REQ-…` or `AC-…` rows.
   A changed criterion gets a new ID; the old row becomes
   `replaced by <new ID>`.
5. **Tests are immutable for implementers.** See section 4.
6. **One task, one branch, one pull request.** Do only what the task says.
7. **Never push to the default branch.** A person reviews and merges every
   pull request.
8. **No secrets, no personal data** in code, tests, fixtures, logs, prompts or
   commits.
9. **Clean room.** Do not copy code from other projects or the internet. Learn
   the idea, write your own code. Respect licenses of dependencies.
10. **When in doubt, stop and ask.** Write the question in the change's
    `handoff.md` and in the pull request. Do not guess product decisions.
11. **English only in the repository.** Talk to people in their language;
    everything that goes into files, commits and pull requests is English.

## 3. How work flows

```
proposal (owner approves) → [SPEC] edit living spec → [TEST] tests with awaits
  → [IMPL] code → review → owner merges → close the change (archive)
```

Details: `docs/workflow/changes.md` and `docs/workflow/task-rules.md`.

To pick work: `python tools/task_status.py --next` lists ready tasks (all
dependencies done). Take a ready task nobody has claimed (no open pull
request or draft for it). `[OWNER]` tasks are for people: report them, do
not do them.

## 4. Testing rules

1. Tests come first, in a `[TEST]` task, written from the acceptance criteria
   of the living spec. Each test names the criterion ID (`AC-…`) in its name
   or docstring and carries an `awaits("T-CODE-NN")` marker for the `[IMPL]`
   task (`[awaits:T-CODE-NN]` in the test name for other languages).
2. An `[IMPL]` pull request never changes tests, specs, core files, rules,
   workflows or thresholds, and never adds escape hatches (skip, only, todo,
   ignore comments, lowered thresholds). CI enforces it (`tools/guard.py`).
3. If a test looks wrong, stop. Explain in `handoff.md` and the pull request
   and propose a `[TEST-CHANGE]` task. Only the owner approves it.
4. Mock only the outside world (network, clock, third-party services).
5. Deterministic tests: fixed seeds, frozen time, no network in unit tests.

Full policy: `docs/workflow/testing-policy.md`.

## 5. Agent commands

The same commands work in Claude Code, OpenCode and GitHub Copilot. Source
text lives in `docs/prompts/`; the files in `.claude/commands/`,
`.opencode/commands/` and `.github/prompts/` only point there.

| Command | What it does |
| --- | --- |
| `/new-change <idea>` | Draft a change folder: proposal, plan, tasks |
| `/next-task [task-id]` | Do the next ready task (or the given one), open a pull request, stop |
| `/write-tests <task-id>` | Do a `[TEST]` task |
| `/implement <task-id>` | Do an `[IMPL]` task |
| `/review <pr-number>` | Review a pull request; report only |
| `/close-change <folder>` | Check a finished change and move it to the archive |
| `/new-area <name>` | Create a new living spec and its requirements file |

## 6. Commands

| Command | What it does |
| --- | --- |
| `make check` | Spec check and all tests (what CI runs) |
| `make spec-check` | Requirements, specs, changes, tasks and test markers |
| `make test` | Tool tests and project tests |
| `make status` / `make next` | Task status / ready tasks |
| `make new-change SLUG=… CODE=… TITLE="…"` | Create a change folder |
| `make close-change CHANGE=…` | Archive a finished change |
| `make guard BASE=origin/main` | Run the pull request guard locally |

Add your project's own commands (format, lint, typecheck, run) to the
`Makefile` and list them here.

## 7. Pull requests

- Branch: `<change-code-lowercase>/<task-id>-short-name`, for example
  `tags/T-TAGS-02-tests`.
- Commit message: `T-CODE-NN: short imperative summary`.
- Label: `spec`, `test`, `impl`, `test-change`, `docs` or `chore`.
- Tick the task box and add a `handoff.md` entry in the same pull request.
- Use the template. For frontend work, fill "UI references"
  (`docs/workflow/ui-references.md`).

## 8. Before you stop

Update the change's `handoff.md` (newest entry on top): last finished task and
pull request, what is next, open questions for the owner.
