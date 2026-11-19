# living-spec-sdd

A ready-to-use repository template for **living-spec SDD**: spec-driven
development where specs describe the system as it is today, every piece of
work has its own change folder, tests come first and cannot be weakened by
implementers, and AI coding agents (Claude Code, OpenCode, GitHub Copilot)
follow the same rules as people.

It works out of the box: Python 3.10+ and git are the only requirements, and
`make check` is green on a fresh copy.

- **What and why:** [`METHOD.md`](METHOD.md)
- **Rules for agents and people:** [`AGENTS.md`](AGENTS.md)
- **How work flows:** [`docs/workflow/`](docs/workflow/)

## Quick start

1. Click **Use this template** on GitHub (or copy the files) to create your
   project.
2. Check that everything works:

   ```sh
   make check        # spec check + tool tests + example tests
   make next         # tasks that are ready (none in a fresh template)
   ```

3. Remove the bundled example and check again:

   ```sh
   make remove-example
   make check
   ```

4. Make it yours:
   - write your product principles in `core/constitution.md` (Part A);
   - add your terms to `core/glossary.md`;
   - follow the one-time setup in [`docs/workflow/owner-guide.md`](docs/workflow/owner-guide.md)
     (branch protection, labels, merge queue).
5. Start working. With an agent:

   ```
   /new-change add user accounts with email sign-in
   ```

   Review and merge the proposal, then repeat:

   ```
   /next-task
   ```

   Each run does one task and opens one pull request. Review, merge, repeat.
   When a change is done: `/close-change <folder>`.

   Without an agent: `make new-change SLUG=user-accounts CODE=ACCT TITLE="User accounts"`
   and follow [`docs/workflow/changes.md`](docs/workflow/changes.md).

## How it works, in short

```
specs/<area>/spec.md        how the area behaves TODAY (the single source of truth)
changes/<date>-<slug>/      one unit of work: proposal, plan, tasks, handoff

proposal → [SPEC] edit the living spec → [TEST] tests with awaits markers
        → [IMPL] code, tick the box → tests become blocking → close (archive)
```

- **Stable IDs.** Requirements `REQ-<AREA>-NNN`, criteria `AC-<AREA>-NNN`,
  tasks `T-<CODE>-NN`. A changed criterion gets a new ID; the old one is
  marked `replaced by …`, and every test and task still using it fails the
  check.
- **Tests first.** `@awaits("T-CODE-NN")` lets tests merge before the code;
  ticking the `[IMPL]` box makes them blocking.
- **Guard.** An `[IMPL]` pull request cannot touch tests, specs, rules or
  thresholds and cannot add skip/ignore escape hatches.
- **Team-friendly.** Every change, area and decision has its own file; git
  conflicts appear only when two changes really edit the same behavior.

## Commands

| Command | What it does |
| --- | --- |
| `make check` | Everything CI runs |
| `make spec-check` | IDs, links, statuses, change folders, test markers, English-only text |
| `make test` | Tool tests and project tests |
| `make status` | Open changes and their tasks |
| `make next` | Ready tasks; owner tasks listed apart |
| `make new-change SLUG=… CODE=… TITLE="…"` | Create a change folder |
| `make close-change CHANGE=…` | Archive a finished change |
| `make guard BASE=origin/main` | Run the pull request guard locally |
| `make remove-example` | Delete the bundled example |

No `make`? Run the same Python commands from the `Makefile` directly, for
example `python tools/spec_check.py`.

## Agent commands

Available in Claude Code (`.claude/commands/`), OpenCode
(`.opencode/commands/`) and GitHub Copilot (`.github/prompts/`). Their text
lives once in `docs/prompts/`.

| Command | What it does |
| --- | --- |
| `/new-change <idea>` | Draft a change folder: proposal, plan, tasks |
| `/next-task [task-id]` | Do one ready task, open a pull request, stop |
| `/write-tests <task-id>` | `[TEST]` task |
| `/implement <task-id>` | `[IMPL]` task |
| `/review <pr-number>` | Review a pull request; report only |
| `/close-change <folder>` | Archive a finished change |
| `/new-area <name>` | Create a new living spec |

## Layout

```
core/            constitution, glossary, requirements, decisions
specs/           living specs, one folder per area (+ _template)
changes/         one folder per change (+ _template, archive/)
docs/workflow/   changes, tasks, testing, team work, reviews, UI references, owner guide
docs/prompts/    source text of agent commands
tools/           checks and helpers (Python standard library) with their own tests
src/, tests/     your code and tests (contain the small "notes" example)
living-spec.json configuration of the checks
```

## The bundled example

The `notes` area shows a complete, finished change: a living spec with a
replaced criterion (`AC-NOTES-002` → `AC-NOTES-003`), requirements, an archived
change folder with `[SPEC]`, `[TEST]` and `[IMPL]` tasks, tests with awaits
markers, and the code. Read it once, then `make remove-example`.

## License

MIT, see [`LICENSE`](LICENSE).
