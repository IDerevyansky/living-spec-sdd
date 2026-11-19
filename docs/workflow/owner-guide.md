# Owner guide

What the person responsible for the project does by hand. Agents never do
these steps.

## Once, when the project starts

1. Create the repository from this template.
2. `make remove-example`, then `make check`.
3. Write your product principles in `core/constitution.md` (Part A).
4. Add your terms to `core/glossary.md`.
5. Create the first areas: `/new-area <name>` or copy `specs/_template/`.
6. GitHub settings:
   - Branch protection on the default branch: pull request required, status
     check `check` required, no force push.
   - Merge queue on (when more than one person works).
   - *Automatically delete head branches* on.
   - Labels: `spec`, `test`, `impl`, `test-change`, `docs`, `chore`.
   - Copilot (if used): "Suggestions matching public code" = Block.
7. Rename `.github/CODEOWNERS.example` to `.github/CODEOWNERS` when a second
   person joins.

## The everyday loop

1. Decide what to build next; ask an agent: `/new-change <idea>`.
2. Review the proposal; merge it when it is right.
3. Run `/next-task` (repeat). Each run does one task and opens one pull
   request.
4. Review with `docs/workflow/review-checklist.md`; for `[TEST]` pull
   requests check that the tests are strong; for `[IMPL]` check that the guard
   is green. Optionally run `/review <pr>` in another session or model.
5. Merge. When all tasks of a change are done: `/close-change <folder>`.

## `[OWNER]` tasks

Decisions and actions only a person can take: accounts, money, legal,
settings, choosing between options. `/next-task` lists them and skips them.
Tick the box in a small `docs` pull request when done.

## When something goes wrong

- A test looks wrong in an `[IMPL]` pull request: do not merge. Approve or
  reject the proposed `[TEST-CHANGE]` task.
- An agent goes beyond its task: close the pull request; tighten the task's
  `Files:` and `Done when:`.
- Specs and code disagree: the spec wins until a `[SPEC]` task changes it.
