"""Tests for note titles (example area). Criteria: specs/notes/spec.md."""

import unittest

from src.notes.titles import validate_title
from tools.lsdd.awaits import awaits


class NoteTitleTests(unittest.TestCase):
    @awaits("T-TITLE-03")
    def test_ac_notes_001_empty_or_space_only_title_is_required(self):
        """AC-NOTES-001"""
        for raw in ("", "   "):
            self.assertEqual(validate_title(raw)[1], ["title_required"])

    @awaits("T-TITLE-03")
    def test_ac_notes_003_title_longer_than_120_is_too_long(self):
        """AC-NOTES-003"""
        self.assertEqual(validate_title("a" * 120)[1], [])
        self.assertEqual(validate_title("a" * 121)[1], ["title_too_long"])

    @awaits("T-TITLE-03")
    def test_ac_notes_004_spaces_are_trimmed_before_checks(self):
        """AC-NOTES-004"""
        cleaned, errors = validate_title("  Groceries  ")
        self.assertEqual(cleaned, "Groceries")
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
