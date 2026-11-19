# Spec: Notes (example area)

Area code: NOTES
Owner: example

This is the bundled example. Delete it with `make remove-example` when you
start a real project.

## Purpose

People keep short notes. Every note has a title that appears in lists, so the
title must be present and readable.

## Behavior

- Before a note is saved, its title is cleaned and validated.
- Cleaning removes spaces at the start and the end.
- Validation returns a list of error codes; an empty list means the title is
  valid.

| Error code | When |
| --- | --- |
| `title_required` | The cleaned title is empty |
| `title_too_long` | The cleaned title is longer than 120 characters |

## Out of scope

Note bodies, storage and search.

## Acceptance criteria

| ID | Criterion | Requirements | Status |
| --- | --- | --- | --- |
| AC-NOTES-001 | An empty or space-only title is rejected with `title_required` | REQ-NOTES-002 | active |
| AC-NOTES-002 | A title longer than 80 characters is rejected | REQ-NOTES-002 | replaced by AC-NOTES-003 |
| AC-NOTES-003 | A title longer than 120 characters is rejected with `title_too_long`; 120 characters are accepted | REQ-NOTES-002 | active |
| AC-NOTES-004 | Spaces at the start and end of a title are removed before validation and saving | REQ-NOTES-001 | active |

## History

| Date | Change | What changed in this spec |
| --- | --- | --- |
| 2026-11-18 | `changes/archive/2026-11-18-note-titles` | Title validation added; the limit moved from 80 to 120 characters (AC-NOTES-002 replaced by AC-NOTES-003) |
