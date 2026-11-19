# Changes

One folder per unit of work: `changes/YYYY-MM-DD-short-slug/`.

| File | Holds |
| --- | --- |
| `proposal.md` | Why, what changes, what does not; change code; whether behavior changes; which specs it touches |
| `plan.md` | How: components, data, contracts, test strategy, risks |
| `tasks.md` | Small tasks `T-<CODE>-NN` with tags, dependencies and covered criteria |
| `handoff.md` | Where work stopped: last task, next task, open questions. Newest entry on top |

Create one with `make new-change SLUG=add-tags CODE=TAGS TITLE="Add tags"`.
Close it with `make close-change CHANGE=<folder>` when every task is ticked:
the folder moves to `archive/`.

Full workflow: `docs/workflow/changes.md`.
