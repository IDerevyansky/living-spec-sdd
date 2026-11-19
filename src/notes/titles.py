"""Note title validation (example area, see specs/notes/spec.md)."""

from __future__ import annotations

MAX_TITLE_LENGTH = 120


def validate_title(raw: str) -> tuple[str, list[str]]:
    """Return the cleaned title and a list of error codes (empty when valid)."""
    title = raw.strip()
    if not title:
        return title, ["title_required"]
    if len(title) > MAX_TITLE_LENGTH:
        return title, ["title_too_long"]
    return title, []
