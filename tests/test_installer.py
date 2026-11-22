"""Tests for offline, safe skill installation."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMAND = [sys.executable, str(ROOT / "scripts/skills.py")]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(COMMAND + list(args), capture_output=True, text=True, check=False)


class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.project = Path(self.directory.name) / "project"
        self.project.mkdir()

    def args(self, *args: str) -> tuple[str, ...]:
        return ("--agent", "codex", "--target", str(self.project), "--skill", "java-quality", *args)

    def test_skill_validation(self) -> None:
        completed = run_cli("validate")
        self.assertEqual(0, completed.returncode, completed.stderr)

    def test_symlink_installation_is_relative_and_reversible(self) -> None:
        installed = run_cli("install", *self.args())
        self.assertEqual(0, installed.returncode, installed.stderr)
        link = self.project / ".agents/skills/java-quality"
        self.assertTrue(link.is_symlink())
        self.assertFalse(link.readlink().is_absolute())
        self.assertTrue((link / "SKILL.md").is_file())
        self.assertEqual(0, run_cli("install", *self.args()).returncode)
        self.assertEqual(0, run_cli("uninstall", *self.args()).returncode)
        self.assertFalse(link.exists())

    def test_copy_installation_is_reversible(self) -> None:
        result = run_cli("install", *self.args("--mode", "copy"))
        self.assertEqual(0, result.returncode, result.stderr)
        target = self.project / ".agents/skills/java-quality"
        self.assertTrue(target.is_dir())
        self.assertFalse(target.is_symlink())
        marker = json.loads((target / ".engineering-agent-skills.json").read_text())
        self.assertEqual("java-quality", marker["skill"])
        self.assertEqual(0, run_cli("uninstall", *self.args()).returncode)
        self.assertFalse(target.exists())

    def test_unmanaged_files_are_never_overwritten_or_deleted(self) -> None:
        target = self.project / ".agents/skills/java-quality"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("User content\n", encoding="utf-8")
        self.assertNotEqual(0, run_cli("install", *self.args()).returncode)
        self.assertNotEqual(0, run_cli("uninstall", *self.args()).returncode)
        self.assertEqual("User content\n", (target / "SKILL.md").read_text())

    def test_dry_run_makes_no_changes(self) -> None:
        result = run_cli("install", *self.args("--dry-run"))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse((self.project / ".agents").exists())

    def test_install_for_both_agents(self) -> None:
        result = run_cli("install", "--agent", "all", "--target", str(self.project), "--skill", "java-quality")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.project / ".agents/skills/java-quality").is_symlink())
        self.assertTrue((self.project / ".claude/skills/java-quality").is_symlink())

    def test_unknown_skill_is_rejected(self) -> None:
        result = run_cli("install", "--agent", "codex", "--target", str(self.project), "--skill", "missing-quality")
        self.assertNotEqual(0, result.returncode)
        self.assertFalse((self.project / ".agents").exists())


if __name__ == "__main__":
    unittest.main()
