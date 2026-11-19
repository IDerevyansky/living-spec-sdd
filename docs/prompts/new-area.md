# Prompt: new area

The argument is the name of a product area, for example "billing".

1. Read `AGENTS.md`, `core/constitution.md`, `specs/README.md` and the
   existing areas, to avoid overlap.
2. Pick a folder name (lowercase) and an area code (2–10 capital letters or
   digits, unused).
3. Inside a change (create one with `docs/prompts/new-change.md` if needed),
   as its `[SPEC]` task:
   - copy `specs/_template/spec.md` to `specs/<name>/spec.md` and fill
     purpose, behavior, out of scope, first criteria;
   - create `core/requirements/<name>.md` with the requirements the criteria
     refer to.
4. Ask the owner about anything uncertain instead of inventing behavior.
5. Run `make spec-check`, then continue with steps 7–9 of
   `docs/prompts/next-task.md`.
