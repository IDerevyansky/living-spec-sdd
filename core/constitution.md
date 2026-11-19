# Constitution

The principles of this project. Everything else (specs, plans, code, tests)
must follow them. Change this file only through a pull request that the owner
approves, and record why in `core/decisions/`.

Replace the product part below with your own principles. Keep the method part
unless you have a strong reason; it is what makes the workflow safe.

## Part A. Product principles

Write 5–15 short, testable rules about what the product must and must not do.
Examples of the shape (delete them):

- **A1. <Name>.** One or two sentences. What is always true.
- **A2. <Name>.** What the product never does, and why.

## Part B. Method principles

- **B1. One source of truth.** `specs/<area>/spec.md` describes how the system
  behaves today. Anything else (change folders, chats, tickets) is a proposal
  until it is merged into a living spec.
- **B2. Every change has a folder.** Work happens in `changes/<date>-<slug>/`
  with a proposal, a plan, tasks and a handoff. No code change without a
  change folder.
- **B3. Behavior changes start with the spec.** If behavior changes, the first
  task of the change is a `[SPEC]` task that edits the living spec. Tests and
  code follow it.
- **B4. Stable IDs.** Requirement (`REQ-…`) and criterion (`AC-…`) IDs are never
  reused or rewritten. A changed criterion gets a new ID; the old one is marked
  `replaced by <new ID>`.
- **B5. Tests first, and immutable for implementers.** Tests come in a `[TEST]`
  task with an `awaits` marker naming the `[IMPL]` task. An `[IMPL]` task never
  changes tests, specs, rules or thresholds and never adds escape hatches.
- **B6. Small tasks.** A task fits in one sitting and one pull request (about
  300 changed lines, generated files aside).
- **B7. Automatic checks stay simple.** Tools check IDs, links, files and
  statuses, never the meaning of text.
- **B8. People decide.** Agents propose and implement; a person reviews and
  merges every pull request. When in doubt, stop and ask.
- **B9. Decisions are recorded.** Anything that would surprise a newcomer in a
  year goes into an ADR in `core/decisions/`.
- **B10. One language in the repository.** All files, code, commits and pull
  requests use one language (English by default), whatever language people
  speak with each other.

## Governance

- This file wins over every other document.
- Changing Part B changes the method; do it rarely and on purpose.
