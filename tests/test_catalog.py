"""Check category membership against the canonical filesystem layout."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".scripts"))

import skills


class CatalogTests(unittest.TestCase):
    def test_repository_catalog_covers_filesystem(self) -> None:
        self.assertEqual([], skills.validate_catalog(skills.CATALOG, set(skills.available_skills())))

    def test_empty_categories_are_valid(self) -> None:
        self.assertEqual([], self.issues(["java-quality"], [], {"java-quality"}))

    def test_rejects_missing_and_unknown_skill_ids(self) -> None:
        issues = self.issues(["unlisted-quality"], [], {"java-quality"})
        self.assertEqual(["catalog.json: unknown skill 'unlisted-quality'",
                          "catalog.json: missing skill 'java-quality'"], issues)

    def test_rejects_duplicate_skill_ids_within_and_across_categories(self) -> None:
        for first, second in ((["java-quality", "java-quality"], []), (["java-quality"], ["java-quality"])):
            with self.subTest(first=first, second=second):
                self.assertEqual(["catalog.json: duplicate skill 'java-quality'"],
                                 self.issues(first, second, {"java-quality"}))

    def test_rejects_invalid_skill_ids(self) -> None:
        issues = self.issues(["java-quality", "../python-quality", False], [], {"java-quality"})
        self.assertEqual(["catalog.json: invalid skill ID '../python-quality' in 'engineering'",
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
