# Requirements

One file per area (`<area>.md`), so parallel changes to different areas never
touch the same file. Specs refer to requirements; tests refer to the
acceptance criteria in specs.

Rules:

- ID format `REQ-<AREA>-NNN`, where `<AREA>` is the area code of the living
  spec. Never reuse or renumber an ID.
- Status is `active`, `removed`, or `replaced by REQ-<AREA>-NNN`.
- One table per file with the columns `ID | Requirement | Status`.

Copy this table into a new `<area>.md`:

```
| ID | Requirement | Status |
| --- | --- | --- |
```
