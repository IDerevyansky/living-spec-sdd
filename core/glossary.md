# Glossary

Words with a fixed meaning. Add your product terms below the method terms.
Use these words exactly in specs, code, UI text and pull requests.

## Method terms

| Term | Meaning |
| --- | --- |
| Area | A part of the product with its own living spec, for example "billing" or "search" |
| Area code | 2–10 capital letters or digits that prefix the area's criterion IDs, for example `BILL` |
| Living spec | `specs/<area>/spec.md`: how the area behaves today. The single source of truth |
| Requirement | A need the product must meet, `REQ-<AREA>-NNN`, in `core/requirements/<area>.md` |
| Acceptance criterion | A checkable statement of behavior, `AC-<AREA>-NNN`, in a living spec |
| Change | One unit of work in `changes/<date>-<slug>/`: proposal, plan, tasks, handoff |
| Change code | 2–10 capital letters or digits that prefix the change's task IDs, for example `TAGS` |
| Task | One small step of a change, `T-<CODE>-NN`, with a tag |
| Tag | The kind of task: `[SPEC]`, `[TEST]`, `[IMPL]`, `[TEST-CHANGE]`, `[DOCS]`, `[CHORE]`, `[OWNER]` |
| Awaits marker | `@awaits("T-CODE-NN")` (Python) or `[awaits:T-CODE-NN]` in a test name: the `[IMPL]` task that makes the test pass |
| Archive | `changes/archive/`: finished changes, kept for history |
| Owner | The person who approves rules and merges pull requests |
| Protected path | A file an `[IMPL]` pull request may not touch (`living-spec.json`) |
| Escape hatch | A way to silence a check (skip, ignore comment, lowered threshold); forbidden in `[IMPL]` |

## Product terms

| Term | Meaning |
| --- | --- |
| Note | (example area, delete with `make remove-example`) A short text with a title |
