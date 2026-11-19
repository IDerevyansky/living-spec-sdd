# Prompt: close a change

The argument is a change folder name, for example `2026-11-18-add-tags`.

1. Run `python tools/close_change.py <folder>` on a branch
   `<code-lowercase>/close` from the latest default branch.
2. If it lists blockers (open tasks, missing `[SPEC]` task), report them and
   stop.
3. Check that the living specs named in `Specs touched` describe the result
   and have a History row for this change. If not, report it and stop.
4. Run `make check`, commit `<CODE>: close change`, push, open a pull request
   labelled `chore`.
5. Report in the owner's language.
