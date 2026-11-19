# Use living-spec SDD as the development method

- Status: accepted
- Date: 2026-11-18

## Context

Spec-driven development (spec → plan → tasks → tests → code) makes AI coding
agents predictable. Feature-style spec folders work well for one stream of
work, but they age: after a year, "how does the system behave today" has to be
reconstructed from many feature specs and their later fixes, and several
people editing shared task and handoff files conflict all the time.
Delta-based tools solve this by merging spec deltas automatically, which adds
a fragile Markdown-merging step.

## Decision

1. Living specs per area (`specs/<area>/spec.md`) are the single source of
   truth for behavior.
2. Every unit of work is a change folder (`changes/<date>-<slug>/`) with its
   own proposal, plan, tasks and handoff.
3. Behavior changes edit the living spec directly, in the change's `[SPEC]`
   task. Git merges and shows conflicts; no tool merges spec deltas.
4. Requirement and criterion IDs are stable; changed criteria get new IDs.
5. Tests first with `awaits` markers; `[IMPL]` pull requests cannot touch
   tests, specs or rules.
6. Simple automatic checks (`tools/`), run locally and in CI.

## Why

- One place to read current behavior, for people and agents.
- Parallel work touches different folders, so conflicts appear only where two
  changes really edit the same behavior, which is exactly when a person should
  decide.
- No custom merge logic to break.

## Consequences

- People must remember to edit the living spec; the `[SPEC]` task rule and
  `close_change.py` enforce it for behavior changes.
- Finished change folders move to `changes/archive/` for history.

## Revisit when

The team grows beyond what one review queue can handle, or a spec tool offers
the same guarantees with less work.
