"""Regression checks for the catalog's standalone skill format."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".scripts"))

import skills


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

    def test_rejects_missing_resources_and_allows_unlinked_resources(self) -> None:
        reference = self.directory / "references/unlinked.md"
        reference.parent.mkdir()
        reference.write_text("# Unreachable\n", encoding="utf-8")
        self.write_skill(body="Read [the rules](references/missing.md).\n")
        issues = skills.validate_skill(self.directory)
        self.assertEqual(["sample-skill: Missing resource: references/missing.md"], issues)

    def test_valid_resources_with_spaces_parentheses_and_optional_directories(self) -> None:
        for path in ("guide.txt", "assets/flow (draft).svg", "scripts/run.py"):
            resource = self.directory / path
            resource.parent.mkdir(exist_ok=True)
            resource.touch()
        self.write_skill(body="Read [the guide](./guide.txt), use [the script](scripts/run.py), "
                         "and see ![the diagram](<assets/flow (draft).svg>) or "
                         "[its link](assets/flow%20(draft).svg).\n")
        self.assertEqual([], skills.validate_skill(self.directory))

    def test_resource_examples_in_code_are_ignored(self) -> None:
        self.write_skill(body="Example `[a link](missing.md)`.\n\n```md\n[a link](missing.md)\n```\n")
        self.assertEqual([], skills.validate_skill(self.directory))

    def test_rejects_reference_escape_and_symlink(self) -> None:
        outside = self.directory.parent / "outside.md"
        outside.write_text("# Outside skill\n", encoding="utf-8")
        references = self.directory / "references"
        references.mkdir()
        self.write_skill(body="[Out](references/../../outside.md)\n")
        issues = skills.validate_skill(self.directory)
        self.assertTrue(any("leaves the skill" in issue for issue in issues), issues)

        (references / "linked.md").symlink_to(outside)
        self.write_skill(body="[Link](references/linked.md)\n")
        issues = skills.validate_skill(self.directory)
        self.assertTrue(any("Unexpected link" in issue for issue in issues), issues)

    def test_rejects_absolute_resources(self) -> None:
        for path in ("/tmp/guide.md", "file:///tmp/guide.md", "C:/tmp/guide.md", "%2Ftmp/guide.md"):
            with self.subTest(path=path):
                self.write_skill(body=f"[Guide]({path})\n")
                self.assertIn("portable relative resource path", skills.validate_skill(self.directory)[0])

    def test_rejects_oversized_directory_name(self) -> None:
        self.directory = self.directory.rename(self.directory.with_name("a" * 65))
        self.manifest = self.directory / "SKILL.md"
        self.write_skill()
        self.assertTrue(skills.validate_skill(self.directory))

    def test_accepts_unicode_skill_names(self) -> None:
        self.assertTrue(skills.valid_name("révision-code"))
        self.assertFalse(skills.valid_name("Révision-code"))

    def test_rejects_no_instructions(self) -> None:
        self.write_skill(body="")
        self.assertTrue(skills.validate_skill(self.directory))
