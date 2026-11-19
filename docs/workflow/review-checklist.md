# Review checklist

## Every pull request

- [ ] One task; the task box is ticked; `handoff.md` has an entry.
- [ ] Only the files the task names changed, or the reason is written.
- [ ] `make check` is green in CI; the guard passed.
- [ ] No secrets, personal data or copied code; new dependencies have allowed
      licenses.
- [ ] English only.

## `[SPEC]`

- [ ] New criteria are checkable sentences, each linked to a requirement.
- [ ] Changed criteria are replaced with new IDs, not rewritten.
- [ ] The History table has a row for this change.
- [ ] The spec still says **what**, not **how**.

## `[TEST]`

- [ ] Every covered criterion has a test that names its ID.
- [ ] Each test awaits the right `[IMPL]` task.
- [ ] Tests would fail for a wrong implementation, not only for a missing one
      (boundaries, error cases).
- [ ] Only the outside world is faked.

## `[IMPL]`

- [ ] The awaiting tests pass after the box is ticked.
- [ ] No protected path touched, no escape hatch added (the guard checks it;
      look anyway).
- [ ] The code is small and clear enough to understand in a few minutes.
- [ ] Frontend: "UI references" section is filled.

## `[TEST-CHANGE]`

- [ ] The reason is real: a wrong test or a replaced criterion.
- [ ] The new test is not weaker than the old one without a stated reason.
