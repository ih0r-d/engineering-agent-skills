"""Check category membership against the canonical filesystem layout."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".scripts"))

import skills


class CatalogTests(unittest.TestCase):
    def test_repository_catalog_covers_filesystem(self) -> None:
        self.assertEqual(24, len(skills.available_skills()))
        self.assertEqual([], skills.validate_catalog(
            skills.CATALOG, set(skills.available_skills()), skills.discover_skill_locations()))

    def test_bundled_references_are_directly_discoverable(self) -> None:
        for name in skills.available_skills():
            with self.subTest(skill=name):
                package = skills.skill_path(name)
                manifest = package / "SKILL.md"
                _, body = skills.split_manifest(manifest.read_text(encoding="utf-8"))
                links = {(package / unquote(urlsplit(link).path)).resolve()
                         for link in skills.inline_destinations(body) if not urlsplit(link).scheme}
                references = set((package / "references").rglob("*.md"))
                self.assertFalse(references - links, references - links)

    def test_rejects_category_misplacement_and_unregistered_directories(self) -> None:
        misplaced = skills.SKILLS / "software-architecture/review-code"
        extra = skills.SKILLS / "software-engineering/unregistered-skill"
        issues = skills.validate_catalog(
            skills.CATALOG, set(skills.available_skills()),
            [misplaced, extra],
        )
        self.assertTrue(any("must be under category 'software-engineering'" in issue for issue in issues), issues)
        self.assertTrue(any("unregistered skill directory" in issue for issue in issues), issues)

    def test_empty_categories_are_valid(self) -> None:
        self.assertEqual([], self.issues(["review-code"], [], {"review-code"}))

    def test_rejects_missing_and_unknown_skill_ids(self) -> None:
        issues = self.issues(["unlisted-quality"], [], {"review-code"})
        self.assertEqual(["catalog.json: unknown skill 'unlisted-quality'",
                          "catalog.json: missing skill 'review-code'"], issues)

    def test_rejects_duplicate_skill_ids_within_and_across_categories(self) -> None:
        for first, second in ((["review-code", "review-code"], []), (["review-code"], ["review-code"])):
            with self.subTest(first=first, second=second):
                self.assertEqual(["catalog.json: duplicate skill 'review-code'"],
                                 self.issues(first, second, {"review-code"}))

    def test_rejects_invalid_skill_ids(self) -> None:
        issues = self.issues(["review-code", "../implement", False], [], {"review-code"})
        self.assertEqual(["catalog.json: invalid skill ID '../implement' in 'engineering'",
                          "catalog.json: invalid skill ID False in 'engineering'"], issues)

    def issues(self, first: list, second: list, available: set[str]) -> list[str]:
        categories = [
            {"id": "engineering", "name": "Engineering", "skills": first},
            {"id": "architecture", "name": "Architecture", "skills": second},
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            path.write_text(json.dumps({"categories": categories}), encoding="utf-8")
            return skills.validate_catalog(path, available)
