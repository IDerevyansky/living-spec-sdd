# Prompt: new change

The argument is an idea in plain words (any language). You draft a change
folder; you write no product code and no tests.

1. Read `AGENTS.md`, `core/constitution.md`, `core/glossary.md` and the living
   specs of the areas the idea touches.
2. If the idea is unclear or conflicts with the constitution or a living spec,
   ask the owner up to three short questions and stop.
3. Pick a short slug (lowercase, dashes) and a change code (2–10 capital
   letters or digits, not used yet: `python tools/task_status.py` and
   `changes/archive/` show used codes).
4. Create a branch `<code-lowercase>/proposal` from the latest default branch.
5. Run `python tools/new_change.py --slug <slug> --code <CODE> --title "<title>"`.
6. Fill `proposal.md` (why, what changes, out of scope, `Behavior change`,
   `Specs touched`, risks), `plan.md` and `tasks.md`:
   - behavior change: first a `[SPEC]` task, then `[TEST]` and `[IMPL]` pairs;
   - tasks small (one pull request each), with `Depends on`, `Files`,
     `Done when`; decisions only a person can take become `[OWNER]` tasks.
7. Translate everything into English. Run `make spec-check` and fix errors
   (the `[SPEC]` task's `Covers` stays "none yet").
8. Add a first `handoff.md` entry, commit `<CODE>: propose <title>`, push,
   open a pull request labelled `spec` with the proposal summary.
9. Stop. Report to the owner in their language: the proposal in five lines
   and the open questions.
