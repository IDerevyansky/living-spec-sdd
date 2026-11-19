# Living specs

One folder per area. `spec.md` says how that area behaves **today**. It is
the single source of truth for people and agents.

- Create an area: copy `_template/` to `specs/<area>/`, pick an area code, add
  `core/requirements/<area>.md`.
- Change behavior: only inside a change, in its `[SPEC]` task
  (`docs/workflow/changes.md`).
- Never delete or rewrite a criterion row. Mark it `removed` or
  `replaced by AC-<AREA>-NNN` and add the new row at the end of the table.
- Keep it short and concrete. A spec says **what**, never **how** (that goes
  into a change's `plan.md`).
