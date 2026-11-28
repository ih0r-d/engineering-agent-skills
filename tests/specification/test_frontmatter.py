"""Exercise the maintainer gate with the pinned upstream validator."""

import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import chdir, redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".scripts"))

import validate_yaml


class SpecificationTests(unittest.TestCase):
    def manifest(self, fields: str, name: str = "sample-skill") -> None:
        values = validate_yaml.skill_fields(f"---\n{fields}\n---\n# Instructions\n")
        validate_yaml.check_specification(values, Path(name))

    def test_accepts_all_standard_optional_fields(self) -> None:
        self.manifest("""name: sample-skill
description: >-
  Review sample changes for correctness.
  Use when reviewing Python changes.
license: Example-License.txt
compatibility: Requires git
metadata:
  author: Example team
  reviewed: '2026-01-01'
  enabled: 'true'
allowed-tools: Bash(git:*) Read""")

    def test_checks_new_yaml_after_an_unstaged_move(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "sample-skill" / "SKILL.md"
            manifest.parent.mkdir()
            manifest.write_text("---\nname: sample-skill\ndescription: Review code.\n---\n# Instructions\n",
                                encoding="utf-8")
            previous = Path("old.yaml")
            replacement = Path("new.yaml")
            (Path(directory) / replacement).write_text("invalid: [\n", encoding="utf-8")
            listing = subprocess.CompletedProcess([], 0, b"\0".join(map(os.fsencode, (previous, replacement))))
            errors = io.StringIO()
            with (
                chdir(directory),
                patch.object(validate_yaml.skills, "REPOSITORY", Path(directory)),
                patch.object(validate_yaml.skills, "skill_directories", return_value=[manifest.parent]),
                patch.object(validate_yaml.subprocess, "run", return_value=listing),
                patch.object(validate_yaml.sys, "argv", ["validate_yaml.py", "--spec"]),
                redirect_stderr(errors),
                redirect_stdout(io.StringIO()),
            ):
                self.assertEqual(1, validate_yaml.main())
                replacement.write_text("valid: true\n", encoding="utf-8")
                self.assertEqual(0, validate_yaml.main())
            self.assertIn("FAIL: " + str(replacement), errors.getvalue())
            self.assertNotIn(str(previous), errors.getvalue())

    def test_accepts_yaml_flow_quoted_keys_and_comments(self) -> None:
        self.manifest("""# Standard YAML mapping
{'name': sample-skill, description: 'Review: sample changes.', metadata: {on: off, samples: '1'}}""")

    def test_accepts_yaml_strings_and_delimiter_like_text(self) -> None:
        self.manifest("name: café-outil\ndescription: 'Review prefix---suffix.'", "café-outil")
        self.manifest("name: sample-skill\ndescription: !!str true\nmetadata: {date: 2026-01-01}")

    def test_enforces_required_fields_and_name_constraints(self) -> None:
        for manifest, name, message in (
            ("description: Review sample changes.", "sample-skill", "Missing required field.*name"),
            ("name: sample-skill", "sample-skill", "Missing required field.*description"),
            ("name: other-skill\ndescription: Review.", "sample-skill", "must match skill name"),
            ("name: Sample-skill\ndescription: Review.", "Sample-skill", "must be lowercase"),
            ("name: sample--skill\ndescription: Review.", "sample--skill", "consecutive hyphens"),
            ("name: ' sample-skill '\ndescription: Review.", "sample-skill", "surrounding whitespace"),
            (f"name: {'a' * 65}\ndescription: Review.", "a" * 65, "64 character limit"),
            ("name: sample-skill\nname: sample-skill\ndescription: Review.", "sample-skill", "Duplicate key"),
        ):
            with self.subTest(manifest=manifest), self.assertRaisesRegex(ValueError, message):
                self.manifest(manifest, name)

    def test_rejects_nonstring_blank_and_oversized_descriptions(self) -> None:
        for description in ('""', "false", "[some, text]", "1e2", "0o12", "A" * 1025):
            with self.subTest(description=description[:50]), self.assertRaises(ValueError):
                self.manifest(f"name: sample-skill\ndescription: {description}")
        with self.assertRaises(yaml.YAMLError):
            self.manifest("name: sample-skill\ndescription: Review: multiple values")

    def test_optional_fields_obey_types_and_constraints(self) -> None:
        for field, message in (
            ("compatibility: ''", "1 to 500"),
            ("compatibility: " + "x" * 501, "500 character limit"),
            ("license: [not-a-string]", "license must be a YAML string"),
            ("metadata: string", "metadata must be a YAML mapping"),
            ("metadata: {enabled: true}", "metadata.enabled must be a YAML string"),
            ("metadata: {123: yes}", "metadata key must be a YAML string"),
            ("metadata: {flag: '1', flag: '2'}", "Duplicate key 'flag'"),
            ("allowed-tools: [Read]", "allowed-tools must be a YAML string"),
            ('allowed-tools: "Read\\tGrep"', "space-separated"),
            ("custom: unsupported", "Unexpected fields"),
        ):
            with self.subTest(field=field[:50]), self.assertRaisesRegex(ValueError, message):
                self.manifest(f"name: sample-skill\ndescription: Review.\n{field}")
