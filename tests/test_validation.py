"""Regression checks for the catalog's standalone skill format."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import skills


class SkillValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        workspace = tempfile.TemporaryDirectory()
        self.addCleanup(workspace.cleanup)
        self.directory = Path(workspace.name) / "sample-skill"
        self.directory.mkdir()
        self.manifest = self.directory / "SKILL.md"

    def write_skill(self, description: str = "Review sample changes.", body: str = "# Instructions\n") -> None:
        self.manifest.write_text(
            f"---\nname: {self.directory.name}\ndescription: {description}\n---\n\n{body}",
            encoding="utf-8",
        )

    def test_missing_manifest_is_invalid(self) -> None:
        issues = skills.validate_skill(self.directory)
        self.assertTrue(any("regular SKILL.md" in issue for issue in issues), issues)

    def test_valid_skill_with_reference_anchor(self) -> None:
        reference = self.directory / "references/rules.md"
        reference.parent.mkdir()
        reference.write_text("# Check\n", encoding="utf-8")
        self.write_skill('"Use it for: sample review."',
                         "Read [the rules](references/rules.md#check).\n")
        self.assertEqual([], skills.validate_skill(self.directory))

    def test_rejects_missing_and_orphaned_references(self) -> None:
        reference = self.directory / "references/unlinked.md"
        reference.parent.mkdir()
        reference.write_text("# Unreachable\n", encoding="utf-8")
        self.write_skill(body="Read [the rules](references/missing.md).\n")
        issues = skills.validate_skill(self.directory)
        self.assertEqual(2, len(issues), issues)
        self.assertTrue(any("missing.md" in issue for issue in issues), issues)
        self.assertTrue(any("unlinked.md" in issue for issue in issues), issues)

    def test_rejects_reference_escape_and_symlink(self) -> None:
        outside = self.directory.parent / "outside.md"
        outside.write_text("# Outside skill\n", encoding="utf-8")
        references = self.directory / "references"
        references.mkdir()
        self.write_skill(body="[Out](references/../../outside.md)\n")
        issues = skills.validate_skill(self.directory)
        self.assertTrue(any("noncanonical" in issue for issue in issues), issues)

        (references / "linked.md").symlink_to(outside)
        self.write_skill(body="[Link](references/linked.md)\n")
        issues = skills.validate_skill(self.directory)
        self.assertTrue(any("Unexpected link" in issue for issue in issues), issues)

    def test_rejects_nonstring_or_oversized_descriptions(self) -> None:
        for description in ('""', "false", "[some, text]", "Review: multiple values", "A" * 1025):
            with self.subTest(description=description[:50]):
                self.write_skill(description)
                self.assertTrue(skills.validate_skill(self.directory))

    def test_rejects_nonmatching_duplicate_and_oversized_names(self) -> None:
        for header in ("name: wrong", "name: sample-skill\nname: different"):
            with self.subTest(header=header):
                self.manifest.write_text(f"---\n{header}\ndescription: Review sample changes.\n---\n\n# Review\n")
                self.assertTrue(skills.validate_skill(self.directory))
        self.directory = self.directory.rename(self.directory.with_name("a" * 65))
        self.manifest = self.directory / "SKILL.md"
        self.write_skill()
        self.assertTrue(skills.validate_skill(self.directory))

    def test_rejects_no_instructions(self) -> None:
        self.write_skill(body="")
        self.assertTrue(skills.validate_skill(self.directory))
