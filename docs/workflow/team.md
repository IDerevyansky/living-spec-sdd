# Working as a team

Living-spec SDD is built so that several people and agents can work at the
same time without stepping on each other.

## Why conflicts stay small

| Shared thing | How it is split |
| --- | --- |
| Tasks and handoff notes | Live in each change's own folder |
| Requirements | One file per area in `core/requirements/` |
| Decisions | One file per decision, named by date |
| Living specs | One per area; two changes conflict only when they edit the same lines of the same spec |
| Task and change IDs | Prefixed by a change code; the spec check rejects a duplicate code in the second pull request |

## Daily rules

1. **Claim before you start**: a draft pull request (or tracker assignment)
   for the task. `make next` shows ready tasks; skip claimed ones.
2. **Small pull requests, short branches.** Rebase on the default branch at
   least daily.
3. **Merge queue** (GitHub setting): a pull request merges only on top of the
   latest default branch with green checks, so two green pull requests cannot
   combine into a red one.
4. **Area owners** in `.github/CODEOWNERS` review changes to their living
   specs. The owner of the project keeps `core/`, `AGENTS.md`, workflows and
   `living-spec.json`.

## When two changes touch the same behavior

Git shows a conflict in the living spec in the second pull request. Do not
resolve it mechanically:

1. Read both changes' proposals.
2. If both behaviors should exist, combine them in the spec with new criterion
   IDs and tell the other change's author.
3. If they contradict, the area owner decides; the losing change updates its
   proposal and tasks.

## When the inputs change in the middle of work

- **A tool or approach changes** (linter, framework, library): do it as its
  own `[CHORE]` change first, merge it, then everyone rebases. Never mix a
  tooling switch into feature work.
- **A criterion changes**: replace it (new ID) in a `[SPEC]` task. The spec
  check then fails on every open task and test that still uses the old ID, so
  the list of affected work is produced for you. Fix tests through
  `[TEST-CHANGE]` tasks.
- **A requirement is dropped**: mark it `removed`; criteria that depend on it
  must be replaced or removed, or the spec check fails.

## Scaling up

| Team size | Recommendation |
| --- | --- |
| One person with agents | As is |
| 2–5 people | Add CODEOWNERS, merge queue, draft-PR claiming |
| Larger | Keep specs, tests and rules in the repository; move task assignment and status views to a tracker (issues and project boards) that links to task IDs |
