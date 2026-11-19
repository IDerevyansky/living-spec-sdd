# Living-spec SDD: the method

This document explains the whole method: what it is, why it is built this way,
and how every piece works. It is written so that someone who has never heard of
it can apply it to a new project from this file alone.

## 1. In one paragraph

**Living-spec SDD** is spec-driven development where the specs describe the
system **as it is today**, one living spec per product area, and every unit of
work happens in its own **change folder** next to them. Behavior changes edit
the living spec first, then tests are written against the spec, then code makes
the tests pass, and implementers can never weaken the tests. Git is the only
merge mechanism; simple scripts check IDs, links and rules in CI. It works for
one person with AI coding agents and scales to a small team without shared
files that everybody edits.

## 2. Where it comes from

| Idea | Taken from | What we keep |
| --- | --- | --- |
| Spec → plan → tasks → code | Spec-driven development (for example GitHub Spec Kit) | Agents work from written intent, not from chat memory |
| Current-state specs and per-change folders | OpenSpec and "docs as code" | One source of truth plus isolated work |
| Branches, pull requests, review, CI | GitHub Flow | The team process stays the ordinary git process |
| Test-first, protected tests | Test-driven development and CI policy | A red build can never be made green by weakening tests |

What we deliberately leave out: tools that merge spec deltas into the living
spec automatically. Merging Markdown by script is the most fragile part of
such systems. Here a behavior change edits the living spec directly in its
pull request, and git shows a conflict when two changes touch the same lines.

## 3. Three levels

| Level | Question | Answer in this method |
| --- | --- | --- |
| Team process | How do people and agents work together? | Branches, pull requests, review, CI, merge queue, code owners |
| Feature delivery | How does an idea become code? | Change folder: proposal → `[SPEC]` → `[TEST]` → `[IMPL]` → close |
| Long-term truth | Where do we read how the system behaves now? | Living specs per area, with stable criterion IDs and a history table |

Most SDD setups cover only the middle level. The third level is what keeps the
project understandable after a year, and the first is what lets several people
work at once.

## 4. Repository layout

```
core/                     principles and shared vocabulary (rarely change)
  constitution.md         product principles + method principles
  glossary.md             fixed terms
  requirements/<area>.md  requirements REQ-<AREA>-NNN, one file per area
  decisions/              decision records, one file per decision, named by date
specs/                    LIVING SPECS: how each area behaves today
  _template/spec.md
  <area>/spec.md          purpose, behavior, out of scope, criteria AC-<AREA>-NNN, history
changes/                  WORK: one folder per change
  _template/              proposal.md, plan.md, tasks.md, handoff.md
  <date>-<slug>/          an open change
  archive/<date>-<slug>/  finished changes, kept for history
docs/workflow/            how we work (changes, tasks, tests, team, reviews, UI)
docs/prompts/             source text of agent commands
.claude/ .opencode/ .github/prompts/   thin command wrappers for each agent tool
tools/                    checks and helpers, Python standard library only
living-spec.json          configuration of the checks
AGENTS.md / CLAUDE.md     rules every agent reads first
```

## 5. The objects and their IDs

| Object | ID | Lives in | Rule |
| --- | --- | --- | --- |
| Area | area code, `NOTES` | `specs/<area>/spec.md` (`Area code:` line) | Unique, 2–10 capital letters or digits |
| Requirement | `REQ-NOTES-001` | `core/requirements/notes.md` | Never reused or rewritten |
| Acceptance criterion | `AC-NOTES-003` | the area's living spec | Never reused or rewritten; changes create a new ID |
| Change | change code, `TITLE` | `changes/<date>-<slug>/proposal.md` | Unique across open and archived changes |
| Task | `T-TITLE-02` | the change's `tasks.md` | Prefixed by the change code; never reused |

Statuses of requirements and criteria: `active`, `removed`, or
`replaced by <ID>`. A replaced row stays in the table forever, so history and
old tests can always be traced.

**Why stable IDs matter.** Tests name the criterion they check. When a
criterion is replaced, the check fails on every test and every open task that
still points to the old ID. The list of work affected by a requirement change
is therefore produced automatically, not remembered by people.

## 6. Life of a change

```
1. new change      make new-change / /new-change     proposal, plan, tasks
2. approve         owner merges the proposal PR
3. [SPEC]          edit the living spec: new/replaced criteria, history row
4. [TEST]          tests per criterion, marked awaits("T-CODE-NN")
5. [IMPL]          code; tick the box → the tests become blocking
6. close           make close-change / /close-change → changes/archive/
```

- One task = one branch = one pull request, about 300 changed lines or less.
- The task box is ticked in the same pull request that does the task.
- Each change keeps its own `handoff.md`; whoever stops writes where the work
  is, what is next and what is unclear.
- A change without behavior change (refactoring, tooling, docs) says
  `Behavior change: no` and has no `[SPEC]` task.

Full rules: `docs/workflow/changes.md`, `docs/workflow/task-rules.md`.

## 7. Tests that cannot be weakened

Three mechanisms work together.

**1. Awaits markers.** Tests are written before the code and carry the ID of
the `[IMPL]` task that will make them pass:

```python
from tools.lsdd.awaits import awaits

@awaits("T-TITLE-03")
def test_ac_notes_003_title_longer_than_120_is_too_long(self):
    """AC-NOTES-003"""
```

While `T-TITLE-03` is not ticked, a failing test is reported as skipped, so
tests can be merged first. When the implementer ticks the box, the same test
runs normally and must pass. Ticking the box is the moment the implementer
declares "done", and from then on the test is part of the build. Other
languages put `[awaits:T-CODE-NN]` in the test name and read the done/pending
list from `python tools/task_status.py --json`.

**2. The guard.** `tools/guard.py` runs on every pull request. It finds the
pull request kind from its label or from the task box it ticks. For `[IMPL]`
it rejects any change to protected paths (tests, fixtures, specs, `core/`,
agent rules, workflows, tools, the config) and any added escape hatch (skip,
only, todo, ignore comments, coverage pragmas). For every pull request it
rejects product code changed outside a change folder.

**3. The spec check.** `tools/spec_check.py` checks every ID and link:
duplicates, unknown references, statuses, tasks covering inactive criteria,
dependencies, tests that await non-`[IMPL]` tasks, tests that refer to
replaced criteria, change folders with missing files, behavior changes without
a `[SPEC]` task, and non-English text.

If a test is genuinely wrong, the implementer stops and proposes a
`[TEST-CHANGE]` task; only the owner approves it.

## 8. Working as a team

Conflicts come from shared files. This layout has almost none:

- tasks and handoff notes live in each change's folder;
- requirements are one file per area; decisions one file each, named by date;
- task IDs carry the change code, and the spec check rejects a reused code.

The only place two changes can collide is the same lines of the same living
spec, and that is exactly when two pieces of work disagree about behavior and
a person should decide. Add code owners per area, a merge queue, and claiming
tasks with draft pull requests, and a small team works in parallel without
friction. Details: `docs/workflow/team.md`.

**When inputs change in the middle of work:**

| What changes | What to do |
| --- | --- |
| A tool, framework or approach | Its own `[CHORE]` change first; everyone rebases after it merges |
| A criterion | Replace it with a new ID in a `[SPEC]` task; the spec check lists every affected test and task; fix tests via `[TEST-CHANGE]` |
| A requirement is dropped | Mark it `removed`; criteria that depend on it must be replaced or removed |
| The proposal itself | Stop, update `proposal.md`, the owner decides |

## 9. Agents

Any coding agent (Claude Code, OpenCode, GitHub Copilot, others) reads
`AGENTS.md` first. The same commands exist for all of them; their text lives
once in `docs/prompts/` and thin wrappers point to it:

| Command | Purpose |
| --- | --- |
| `/new-change <idea>` | Draft a change folder |
| `/next-task [id]` | Do one ready task and open a pull request |
| `/write-tests <id>` | `[TEST]` task |
| `/implement <id>` | `[IMPL]` task |
| `/review <pr>` | Review only |
| `/close-change <folder>` | Archive a finished change |
| `/new-area <name>` | Create a living spec |

The owner's loop: `/new-change` → merge the proposal → `/next-task` → review
→ merge → repeat → `/close-change`. Agents never merge and never do `[OWNER]`
tasks.

## 10. Frontend work

Before writing interface code, the agent looks at 3–5 references (a pattern
library such as Mobbin, and strong products solving the same job), picks a
pattern and lists the links in the pull request. If the owner provided a
mockup, it wins. This is a step inside the task, not a separate task
(`docs/workflow/ui-references.md`).

## 11. Comparison

| | Feature-folder SDD (Spec Kit style) | Delta-based SDD (OpenSpec style) | Living-spec SDD |
| --- | --- | --- | --- |
| Where current behavior is described | Spread over feature specs | Main specs, updated by merging deltas | Living specs, edited directly |
| Parallel work | Shared task/plan files conflict | Isolated change folders | Isolated change folders |
| Merge mechanism for specs | n/a | Tool merges Markdown deltas | Git |
| Protection against weakened tests | Not built in | Not built in | Awaits markers + guard + spec check |
| Tools needed | Templates and prompts | CLI | Python standard library scripts |

## 12. Adopting it

**New project:** create a repository from this template, run
`make remove-example`, write your principles, create areas, start the first
change (`README.md` → Quick start).

**Existing project:**

1. Copy `core/`, `docs/`, `tools/`, `living-spec.json`, `AGENTS.md`,
   `CLAUDE.md`, the command folders, `.github/` files and the `Makefile`.
2. Write living specs for the areas you are about to touch first; describe
   current behavior, not wishes. Other areas get specs when work reaches them.
3. Existing tests do not need markers; new tests do.
4. Adjust `code_globs` and `protected_for_impl` in `living-spec.json` to your
   layout.

## 13. Known limits

- **Discipline is still needed.** The checks catch missing spec tasks, broken
  IDs and weakened tests, but not a spec that describes behavior badly.
  Reviews of `[SPEC]` pull requests matter most.
- **Spec conflicts need people.** That is intended; no tool should decide
  between two behaviors.
- **The guard trusts labels and ticked boxes.** Branch protection and review
  keep that honest.
- **Large teams** should move task assignment and dashboards to an issue
  tracker, keeping specs, tests and rules in the repository.

## 14. FAQ

**Why not keep requirements inside specs?** Several criteria in different
areas can serve one requirement, and requirements change at a different pace
than behavior details.

**Why dates in change and decision names?** They make names unique without a
central counter, so two people never pick the same number.

**Why Python for the tools?** It is available almost everywhere, needs no
dependencies here, and the tools are small enough to read in minutes. The
project itself can use any language.

**Can I rename folders?** Yes: adjust `living-spec.json`, the docs and the
prompts together, and keep `make check` green.
