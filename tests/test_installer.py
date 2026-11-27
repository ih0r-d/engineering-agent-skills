"""Tests for offline, safe skill installation."""

from __future__ import annotations

import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".scripts"))

import skills

COMMAND = [sys.executable, str(ROOT / ".scripts/skills.py")]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(COMMAND + list(args), capture_output=True, text=True, check=False, timeout=10)


class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.project = Path(self.directory.name).resolve() / "project with spaces"
        self.project.mkdir()
        self.target = self.project / ".agents/skills/java-quality"

    def args(self, *args: str) -> tuple[str, ...]:
        return ("--agent", "codex", "--target", str(self.project), "--skill", "java-quality", *args)

    def test_skill_validation(self) -> None:
        completed = run_cli("validate")
        self.assertEqual(0, completed.returncode, completed.stderr)

    def test_general_engineering_skills_install_and_uninstall_for_both_agents(self) -> None:
        names = ("code-review", "refactoring")
        listing = run_cli("list")
        self.assertEqual(0, listing.returncode, listing.stderr)
        self.assertTrue(set(names) <= set(listing.stdout.splitlines()))
        args = ("--agent", "all", "--target", str(self.project), "--skill", ",".join(names))
        for mode in ("symlink", "copy"):
            with self.subTest(mode=mode):
                installed = run_cli("install", *args, "--mode", mode)
                self.assertEqual(0, installed.returncode, installed.stderr)
                targets = [self.project / path / name for path in (".agents/skills", ".claude/skills")
                           for name in names]
                for target in targets:
                    manifest = target / "SKILL.md"
                    self.assertEqual(mode == "symlink", target.is_symlink())
                    self.assertEqual((ROOT / "skills" / target.name / "SKILL.md").read_bytes(),
                                     manifest.read_bytes())
                removed = run_cli("uninstall", *args)
                self.assertEqual(0, removed.returncode, removed.stderr)
                self.assertFalse(any(os.path.lexists(target) for target in targets))

    def test_skill_authoring_copy_is_self_contained_and_valid(self) -> None:
        args = ("--agent", "codex", "--target", str(self.project), "--skill", "skill-authoring", "--mode", "copy")
        installed = run_cli("install", *args)
        self.assertEqual(0, installed.returncode, installed.stderr)
        target = self.project / ".agents/skills/skill-authoring"
        self.assertTrue(target.is_dir())
        self.assertFalse(target.is_symlink())
        standalone = self.project / "standalone-skill-authoring"
        shutil.copytree(target, standalone)
        (standalone / skills.MARKER).unlink()
        self.assertEqual([], skills.validate_skill(standalone))
        removed = run_cli("uninstall", "--agent", "codex", "--target", str(self.project),
                          "--skill", "skill-authoring")
        self.assertEqual(0, removed.returncode, removed.stderr)

    def test_legacy_python_entrypoint_matches_current_cli(self) -> None:
        legacy = [sys.executable, str(ROOT / "scripts/skills.py")]
        for args, status in (
            (("list",), 0),
            (("install", *self.args("--mode", "copy", "--dry-run")), 0),
            (("uninstall", *self.args("--dry-run")), 0),
            (("install", "--agent", "codex"), 2),
        ):
            with self.subTest(args=args):
                current = run_cli(*args)
                result = subprocess.run(legacy + list(args), cwd=self.project, capture_output=True,
                                        text=True, check=False, timeout=10)
                self.assertEqual(status, current.returncode)
                self.assertEqual((current.returncode, current.stdout, current.stderr),
                                 (result.returncode, result.stdout, result.stderr))
        self.assertFalse((self.project / ".agents").exists())

    @unittest.skipUnless(shutil.which("bash"), "Bash is required for the shell wrappers")
    def test_wrappers_resolve_their_checkout_with_cdpath_set(self) -> None:
        lookup = self.project.parent / "cdpath"
        for directory in (".scripts", "scripts"):
            (lookup / directory).mkdir(parents=True)
            for script, args, status, message in (
                ("validate.sh", (), 0, "PASS:"),
                ("install.sh", self.args("--dry-run"), 0, "DRY RUN install"),
                ("install.sh", self.args(), 0, "INSTALLED"),
                ("uninstall.sh", self.args("--dry-run"), 0, "DRY RUN remove"),
                ("uninstall.sh", self.args(), 0, "REMOVED"),
                ("install.sh", ("--agent", "unknown"), 2, "invalid choice"),
            ):
                with self.subTest(directory=directory, script=script, args=args):
                    result = subprocess.run(
                        [f"{directory}/{script}", *args],
                        cwd=ROOT,
                        env={**os.environ, "CDPATH": str(lookup)},
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=10,
                    )
                    self.assertEqual(status, result.returncode, result.stderr)
                    self.assertIn(message, result.stdout if status == 0 else result.stderr)
                    if "--dry-run" in args:
                        self.assertEqual(script == "uninstall.sh", self.target.is_symlink())
        self.assertFalse(os.path.lexists(self.target))

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
        self.assertEqual(1, marker["format"])
        self.assertTrue((target / "references/boundaries.md").is_file())
        repeated = run_cli("install", *self.args("--mode", "copy"))
        self.assertEqual(0, repeated.returncode, repeated.stderr)
        self.assertIn("SKIP", repeated.stdout)
        preview = run_cli("uninstall", *self.args("--dry-run"))
        self.assertEqual(0, preview.returncode, preview.stderr)
        self.assertIn("DRY RUN remove", preview.stdout)
        self.assertTrue(target.is_dir())
        self.assertEqual(0, run_cli("uninstall", *self.args()).returncode)
        self.assertEqual(0, run_cli("uninstall", *self.args()).returncode)
        self.assertFalse(target.exists())

    def test_offline_copy_accepts_standard_optional_frontmatter(self) -> None:
        checkout = self.project.parent / "checkout"
        source = checkout / "sample-skill"
        source.mkdir(parents=True)
        manifest = ("---\nname: sample-skill\ndescription: >-\n  Review sample changes.\n"
                    "compatibility: Requires Git\nmetadata: {author: 'Example team'}\n"
                    "allowed-tools: Read\n---\n# Instructions\n")
        (source / "SKILL.md").write_text(manifest, encoding="utf-8")
        args = ["--agent", "codex", "--target", str(self.project), "--skill", source.name]
        with patch.object(skills, "SKILLS", checkout), redirect_stdout(io.StringIO()):
            skills.apply_selection(skills.create_parser().parse_args(["install", *args, "--mode", "copy"]))
            target = self.target.with_name(source.name)
            self.assertEqual(manifest, (target / "SKILL.md").read_text(encoding="utf-8"))
            skills.apply_selection(skills.create_parser().parse_args(["uninstall", *args]))
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

    def test_selective_install_and_removal_preserve_consumer_instructions(self) -> None:
        consumer_files = {
            "AGENTS.md": b"# Consumer Codex instructions\n",
            "CLAUDE.md": b"# Consumer Claude instructions\n",
            ".claude/CLAUDE.md": b"# Consumer local configuration\n",
            "README.md": b"# Consumer project\n",
        }
        for relative, content in consumer_files.items():
            path = self.project / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)

        manifest = (ROOT / "skills/java-quality/SKILL.md").read_bytes()
        args = ("--agent", "all", "--target", str(self.project), "--skill", "java-quality")
        for mode in ("symlink", "copy"):
            with self.subTest(mode=mode):
                installed = run_cli("install", *args, "--mode", mode)
                self.assertEqual(0, installed.returncode, installed.stderr)
                for relative in (".agents/skills", ".claude/skills"):
                    directory = self.project / relative
                    self.assertEqual(["java-quality"], sorted(entry.name for entry in directory.iterdir()))
                    skill = directory / "java-quality"
                    self.assertEqual(mode == "symlink", skill.is_symlink())
                    self.assertEqual(manifest, (skill / "SKILL.md").read_bytes())
                for relative, content in consumer_files.items():
                    self.assertEqual(content, (self.project / relative).read_bytes())

                removed = run_cli("uninstall", *args)
                self.assertEqual(0, removed.returncode, removed.stderr)
                for relative, content in consumer_files.items():
                    self.assertEqual(content, (self.project / relative).read_bytes())

    def test_unknown_skill_is_rejected(self) -> None:
        result = run_cli("install", "--agent", "codex", "--target", str(self.project), "--skill", "missing-quality")
        self.assertNotEqual(0, result.returncode)
        self.assertFalse((self.project / ".agents").exists())

    def test_conflict_preflights_both_agents_and_all_selected_skills(self) -> None:
        conflict = self.project / ".claude/skills/python-quality"
        conflict.parent.mkdir(parents=True)
        conflict.write_text("unrelated file")
        args = ("--agent", "all", "--target", str(self.project),
                "--skill", "python-quality,java-quality", "--skill", "java-quality")
        for options in ((), ("--dry-run",)):
            with self.subTest(options=options):
                result = run_cli("install", *args, *options)
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertIn(str(conflict.resolve()), result.stderr)
                self.assertFalse(self.target.parent.exists())
                self.assertFalse((conflict.parent / "java-quality").exists())
                self.assertEqual("unrelated file", conflict.read_text())

    def test_uninstall_preflights_all_paths_before_removing_any(self) -> None:
        args = ("--agent", "all", "--target", str(self.project), "--all")
        installed = run_cli("install", *args, "--mode", "copy")
        self.assertEqual(0, installed.returncode, installed.stderr)
        edited = self.project / ".claude/skills/shell-quality/references/local.md"
        edited.write_text("Keep this.")
        refused = run_cli("uninstall", *args)
        self.assertEqual(2, refused.returncode, refused.stderr)
        self.assertIn("local changes", refused.stderr)
        self.assertEqual("Keep this.", edited.read_text())
        self.assertTrue(self.target.is_dir())

    def test_modified_copy_is_protected(self) -> None:
        self.assertEqual(0, run_cli("install", *self.args("--mode", "copy")).returncode)
        manifest = self.target / "SKILL.md"
        manifest.write_text("Local edits.\n")
        for command, options in (("install", ("--mode", "copy")), ("uninstall", ())):
            with self.subTest(command=command):
                result = run_cli(command, *self.args(*options))
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertIn("local changes", result.stderr)
                self.assertEqual("Local edits.\n", manifest.read_text())

    def test_unmanaged_or_looping_links_are_protected(self) -> None:
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(self.target.name, target_is_directory=True)
        for command in ("install", "uninstall"):
            with self.subTest(command=command):
                result = run_cli(command, *self.args())
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertIn("unmanaged", result.stderr)
                self.assertTrue(self.target.is_symlink())

    def test_rejects_linked_parent_directories(self) -> None:
        outside = self.project.parent / "outside"
        outside.mkdir()
        for parent in (self.target.parent.parent, self.target.parent):
            with self.subTest(parent=parent):
                parent.parent.mkdir(parents=True, exist_ok=True)
                parent.symlink_to(outside, target_is_directory=True)
                for command in ("install", "uninstall"):
                    result = run_cli(command, *self.args())
                    self.assertEqual(2, result.returncode, result.stderr)
                    self.assertIn("real directory", result.stderr)
                self.assertEqual([], list(outside.iterdir()))
                parent.unlink()

    def test_rejects_skills_parent_file_with_clean_error(self) -> None:
        self.target.parent.parent.mkdir()
        self.target.parent.write_text("unrelated")
        result = run_cli("install", *self.args())
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertIn("real directory", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_mode_change_requires_explicit_removal(self) -> None:
        self.assertEqual(0, run_cli("install", *self.args()).returncode)
        result = run_cli("install", *self.args("--mode", "copy"))
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertIn("already installed in symlink mode", result.stderr.lower())
        self.assertTrue(self.target.is_symlink())

    def test_user_scope_uses_agent_homes(self) -> None:
        simulated_user = self.project.parent / "user"
        simulated_user.mkdir()
        args = ["--agent", "all", "--scope", "user", "--skill", "shell-quality"]
        with patch.object(Path, "home", return_value=simulated_user), redirect_stdout(io.StringIO()):
            skills.apply_selection(skills.create_parser().parse_args(["install", *args, "--mode", "copy"]))
            for agent_path in (".agents/skills", ".claude/skills"):
                self.assertTrue((simulated_user / agent_path / "shell-quality/SKILL.md").is_file())
            skills.apply_selection(skills.create_parser().parse_args(["uninstall", *args]))
        self.assertFalse((simulated_user / ".agents/skills/shell-quality").exists())
        self.assertFalse((simulated_user / ".claude/skills/shell-quality").exists())
        self.assertFalse((self.project / ".agents").exists())

    def test_rejects_user_scope_target(self) -> None:
        result = run_cli("install", *self.args("--scope", "user"))
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertIn("project scope", result.stderr)

    def test_exact_relative_link_survives_project_relocation_and_dangling_source(self) -> None:
        checkout_path = Path(".tooling/engineering-agent-skills")
        checkout = self.project / checkout_path
        skill_path = checkout_path / "skills/java-quality"
        targets = (".agents/skills/java-quality", ".claude/skills/java-quality")
        shutil.copytree(ROOT / "skills/java-quality", checkout / "skills/java-quality")
        installer = checkout / ".scripts/skills.py"
        installer.parent.mkdir()
        shutil.copy2(ROOT / ".scripts/skills.py", installer)
        command = [sys.executable, str(installer)]
        options = ["--agent", "all", "--skill", "java-quality"]
        installed = subprocess.run(
            command + ["install", *options],
            cwd=self.project,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        self.assertEqual(0, installed.returncode, installed.stderr)
        self.assertIn("INSTALLED", installed.stdout)
        for target in targets:
            self.assertEqual(Path("../..") / skill_path, (self.project / target).readlink())
        moved = self.project.rename(self.project.with_name("relocated"))
        for target in targets:
            self.assertEqual(moved / skill_path, (moved / target).resolve(strict=True))
            self.assertTrue((moved / target / "SKILL.md").is_file())

        (moved / skill_path).rename(moved / skill_path.with_name("old-name"))
        for target in targets:
            self.assertTrue((moved / target).is_symlink())
            self.assertFalse((moved / target).exists())
        subprocess.run(
            [sys.executable, str(moved / checkout_path / ".scripts/skills.py"), "uninstall", *options],
            cwd=moved,
            capture_output=True,
            check=True,
            timeout=10,
        )
        for target in targets:
            self.assertFalse(os.path.lexists(moved / target))

    def test_legacy_copy_requires_matching_content(self) -> None:
        source = ROOT / "skills/java-quality"
        shutil.copytree(source, self.target)
        marker = self.target / skills.MARKER
        marker.write_text(json.dumps({"source": str(source), "skill": source.name}))
        added = self.target / "local.md"
        added.write_text("Keep this.")
        self.assertEqual(2, run_cli("uninstall", *self.args()).returncode)
        self.assertTrue(added.is_file())
        added.unlink()
        self.assertEqual(0, run_cli("uninstall", *self.args()).returncode)
        self.assertFalse(self.target.exists())

    def test_marker_symlink_cannot_claim_ownership(self) -> None:
        self.assertEqual(0, run_cli("install", *self.args("--mode", "copy")).returncode)
        marker = self.target / skills.MARKER
        saved = marker.rename(self.project / "marker.json")
        marker.symlink_to(saved)
        result = run_cli("uninstall", *self.args())
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertTrue(marker.is_symlink())
        self.assertTrue(saved.is_file())

    def test_copy_failure_removes_partial_destination(self) -> None:
        def failed_copy(source, destination, **kwargs):
            destination.write_text("partial")
            raise OSError("simulated write failure")

        args = skills.create_parser().parse_args(["install", *self.args("--mode", "copy")])
        with patch.object(skills.shutil, "copy2", side_effect=failed_copy):
            with self.assertRaisesRegex(OSError, "simulated write failure"):
                skills.apply_selection(args)
        self.assertFalse(self.target.exists())
        self.assertEqual(0, run_cli("install", *self.args("--mode", "copy")).returncode)

    def test_prevents_installation_inside_skill_source(self) -> None:
        catalog = self.project / "catalog"
        source = catalog / "java-quality"
        shutil.copytree(ROOT / "skills/java-quality", source)
        with patch.object(skills, "SKILLS", catalog):
            args = skills.create_parser().parse_args([
                "install", "--agent", "codex", "--target", str(source), "--skill", "java-quality",
            ])
            with self.assertRaisesRegex(skills.SkillError, "outside the source catalog"):
                skills.apply_selection(args)
        self.assertFalse((source / ".agents").exists())

    def test_copies_from_read_only_source_with_removable_directory_modes(self) -> None:
        catalog = self.project / "catalog"
        source = catalog / "java-quality"
        shutil.copytree(ROOT / "skills/java-quality", source)
        directories = [source, source / "references"]
        for directory in directories:
            directory.chmod(0o555)
        try:
            with patch.object(skills, "SKILLS", catalog), redirect_stdout(io.StringIO()):
                install = skills.create_parser().parse_args(["install", *self.args("--mode", "copy")])
                skills.apply_selection(install)
                self.assertTrue((self.target / "SKILL.md").is_file())
                skills.apply_selection(skills.create_parser().parse_args(["uninstall", *self.args()]))
            self.assertFalse(self.target.exists())
        finally:
            for directory in directories:
                directory.chmod(0o755)


if __name__ == "__main__":
    unittest.main()
