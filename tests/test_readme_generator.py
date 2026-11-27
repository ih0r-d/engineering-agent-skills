"""Tests for deterministic README catalog rendering and freshness checks."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("generate_readme", ROOT / ".scripts/generate_readme.py")
assert SPEC and SPEC.loader
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


class ReadmeGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = {"categories": [{"id": "software-engineering", "name": "Software Engineering",
                                         "skills": ["sample-skill"]}]}
        self.descriptions = {"sample-skill": "Review API | compatibility and behavior."}
        self.inventory = {"skills": 1, "categories": 1, "references": 2, "assets": 1, "scripts": 0,
                          "evaluation_cases": 3}

    def test_catalog_render_is_deterministic_and_escapes_table_delimiters(self) -> None:
        result = generator.render_catalog(self.catalog, self.descriptions, self.inventory)
        self.assertEqual(result, generator.render_catalog(self.catalog, self.descriptions, self.inventory))
        self.assertIn("[`sample-skill`](skills/software-engineering/sample-skill/SKILL.md)", result)
        self.assertIn("Review API \\| compatibility", result)

    def test_replacement_is_idempotent_and_preserves_handwritten_sections(self) -> None:
        original = f"# Project\n\n{generator.BEGIN}\n\nold\n\n{generator.END}\n\n## Manual section\n"
        generated = generator.render_catalog(self.catalog, self.descriptions, self.inventory)
        updated = generator.replace_generated_section(original, generated)
        self.assertEqual(updated, generator.replace_generated_section(updated, generated))
        self.assertIn("## Manual section", updated)
        self.assertEqual(1, updated.count(generator.BEGIN))
        self.assertEqual(1, updated.count(generator.END))

    def test_rejects_missing_or_misordered_markers(self) -> None:
        for text in ("# Missing markers", f"{generator.END}\n{generator.BEGIN}"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                generator.replace_generated_section(text, "generated")

    def test_check_mode_does_not_modify_stale_readme(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            readme = Path(temporary) / "README.md"
            original = f"{generator.BEGIN}\nold\n{generator.END}\n"
            readme.write_text(original, encoding="utf-8")
            catalog_content = (self.catalog, self.descriptions, self.inventory)
            with patch.object(generator, "README", readme), \
                    patch.object(generator, "load_catalog_content", return_value=catalog_content), \
                    patch.object(sys, "argv", ["generate_readme.py", "--check"]):
                self.assertEqual(1, generator.main())
            self.assertEqual(original, readme.read_text(encoding="utf-8"))

    def test_write_mode_updates_only_generated_section(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            readme = Path(temporary) / "README.md"
            original = f"# Intro\n\n{generator.BEGIN}\nold\n{generator.END}\n\n## Notes\n"
            readme.write_text(original, encoding="utf-8")
            catalog_content = (self.catalog, self.descriptions, self.inventory)
            with patch.object(generator, "README", readme), \
                    patch.object(generator, "load_catalog_content", return_value=catalog_content), \
                    patch.object(sys, "argv", ["generate_readme.py"]):
                self.assertEqual(0, generator.main())
            updated = readme.read_text(encoding="utf-8")
            self.assertTrue(updated.startswith("# Intro\n"))
            self.assertTrue(updated.endswith("## Notes\n"))
            self.assertIn("sample-skill", updated)

    def test_repository_generated_block_lists_each_catalog_skill_once_by_category(self) -> None:
        catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        block = readme.split(generator.BEGIN, 1)[1].split(generator.END, 1)[0]
        skill_ids = [skill for category in catalog["categories"] for skill in category["skills"]]
        self.assertEqual(len(skill_ids), len(set(skill_ids)))
        for category in catalog["categories"]:
            self.assertIn(f"### {category['name']}", block)
            for skill in category["skills"]:
                self.assertEqual(1, block.count(f"[`{skill}`](skills/{category['id']}/{skill}/SKILL.md)"))


if __name__ == "__main__":
    unittest.main()
