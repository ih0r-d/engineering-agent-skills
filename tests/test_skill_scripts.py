"""Regression tests for portable scripts bundled with skills."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/software-delivery/git-workflow/scripts/validate-commit.py"


class CommitMessageScriptTests(unittest.TestCase):
    def run_script(self, *args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(SCRIPT), *args], input=input_text, capture_output=True,
            text=True, check=False, timeout=10,
        )

    def test_accepts_conventional_headers_and_breaking_footer(self) -> None:
        for message in (
            "feat: add feature",
            "fix(api): correct validation",
            "feat!: change public contract",
            "build(deps): update tooling\n\nBREAKING CHANGE: generated output changed",
            "custom-policy: retain consumer-defined type",
        ):
            with self.subTest(message=message):
                result = self.run_script("--message", message)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("valid", result.stdout)

    def test_accepts_optional_task_identifier_policy(self) -> None:
        result = self.run_script(
            "--message", "feat: ENG-123: add feature", "--task-id-regex", r"[A-Z]+-[0-9]+"
        )
        self.assertEqual(0, result.returncode, result.stderr)
        invalid = self.run_script(
            "--message", "feat: add feature", "--task-id-regex", r"[A-Z]+-[0-9]+"
        )
        self.assertEqual(1, invalid.returncode)
        self.assertIn("task identifier", invalid.stderr)

    def test_optional_allowed_type_policy_does_not_define_a_global_type_list(self) -> None:
        self.assertEqual(0, self.run_script("--message", "docs: update guide").returncode)
        rejected = self.run_script("--message", "docs: update guide", "--allowed-types", "feat,fix")
        self.assertEqual(1, rejected.returncode)
        self.assertIn("not allowed", rejected.stderr)

    def test_reads_hook_compatible_message_file_with_spaces_without_modifying_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "commit message.txt"
            original = "fix: retain the message file\n"
            path.write_text(original, encoding="utf-8")
            result = self.run_script(str(path))
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(original, path.read_text(encoding="utf-8"))

    def test_reads_standard_input(self) -> None:
        result = self.run_script(input_text="feat: from standard input\n")
        self.assertEqual(0, result.returncode, result.stderr)

    def test_invalid_header_and_empty_breaking_footer_return_invalid_status(self) -> None:
        for message, expected in (
            ("feat:no space", "header must use"),
            ("feat: ", "header must use"),
            ("feat: ok\n\nBREAKING CHANGE:", "must include a description"),
            ("feat: ok\n\nBREAKING-CHANGE: wrong token", "BREAKING CHANGE:"),
        ):
            with self.subTest(message=message):
                result = self.run_script("--message", message)
                self.assertEqual(1, result.returncode)
                self.assertIn(expected, result.stderr)
                self.assertEqual("", result.stdout)

    def test_input_errors_return_usage_status(self) -> None:
        missing = self.run_script()
        self.assertEqual(2, missing.returncode)
        self.assertIn("provide a commit message", missing.stderr)
        missing_file = self.run_script("/does/not/exist/commit.txt")
        self.assertEqual(2, missing_file.returncode)
        self.assertIn("cannot read", missing_file.stderr)

    def test_script_runs_from_a_copied_standalone_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            copied_script = Path(temporary) / "git-workflow/scripts/validate-commit.py"
            copied_script.parent.mkdir(parents=True)
            copied_script.write_bytes(SCRIPT.read_bytes())
            copied_script.chmod(SCRIPT.stat().st_mode)
            result = subprocess.run(
                [str(copied_script), "--message", "chore: standalone"],
                capture_output=True, text=True, check=False, timeout=10,
            )
            self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
