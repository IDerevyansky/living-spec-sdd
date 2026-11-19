# Plan: Validate note titles

## Components

`src/notes/titles.py`: `validate_title(raw) -> (cleaned, errors)`.

## Data and contracts

Error codes `title_required` and `title_too_long`, as in the living spec.

## Test strategy

Unit tests in `tests/test_note_titles.py`, one per criterion, including the
120 / 121 character boundary.

## Risks

None.
