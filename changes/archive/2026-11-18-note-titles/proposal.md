# Change: Validate note titles

Change code: TITLE
Started: 2026-11-18
Behavior change: yes
Specs touched: specs/notes/spec.md

## Why

Notes appear in lists by title (REQ-NOTES-001). Empty or very long titles
make lists unreadable, so titles must be validated before saving
(REQ-NOTES-002).

## What changes

Titles are trimmed, then rejected when empty or longer than 120 characters.
The earlier draft limit of 80 characters (AC-NOTES-002) was too short for
real titles and is replaced.

## Out of scope

Note bodies and storage.

## Risks and open questions

None.
