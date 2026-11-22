#!/usr/bin/env python3
"""Offline-first installer and validator for repository-local agent skills."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parent.parent
SKILLS = REPOSITORY / "skills"
MARKER = ".engineering-agent-skills.json"
AGENT_DIRECTORIES = {"codex": Path(".agents/skills"), "claude": Path(".claude/skills")}
SKILL_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
REFERENCE_LINK = re.compile(r"\]\((references/[^)#]+\.md)(?:#[^)]+)?\)")


class SkillError(Exception):
    """An expected installation or validation failure."""


def available_skills() -> list[str]:
    return sorted(path.name for path in SKILLS.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())


def select_skills(args: argparse.Namespace) -> list[str]:
    available = available_skills()
    requested = [name.strip() for raw in (args.skill or []) for name in raw.split(",") if name.strip()]
    if args.all and requested:
        raise SkillError("Use either --all or --skill, not both.")
    if not args.all and not requested:
        raise SkillError("Select one or more skills with --skill or use --all.")
    names = available if args.all else sorted(set(requested))
    invalid = set(names) - set(available)
    if invalid:
        raise SkillError(f"Unknown skills: {', '.join(sorted(invalid))}. Available: {', '.join(available)}")
    return names


def agent_targets(args: argparse.Namespace) -> list[tuple[str, Path]]:
    agents = list(AGENT_DIRECTORIES) if args.agent == "all" else [args.agent]
    if args.scope == "user":
        root = Path.home()
    else:
        root = Path(args.target).expanduser().resolve()
        if not root.is_dir():
            raise SkillError(f"Project directory does not exist: {root}")
    return [(agent, root / AGENT_DIRECTORIES[agent]) for agent in agents]


def is_owned(destination: Path, source: Path) -> bool:
    if destination.is_symlink():
        return destination.resolve() == source.resolve()
    if destination.is_dir():
        marker = destination / MARKER
        try:
            metadata = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            return False
        return metadata == {"source": str(source.resolve()), "skill": source.name}
    return False


def install(source: Path, destination: Path, mode: str, dry_run: bool) -> str:
    if destination.exists() or destination.is_symlink():
        if is_owned(destination, source):
            return f"SKIP (already installed): {destination}"
        raise SkillError(f"Refusing to overwrite existing path: {destination}")
    if dry_run:
        return f"DRY RUN install {source.name} ({mode}): {destination}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if mode == "symlink":
        relative_path = os.path.relpath(source, start=destination.parent)
        destination.symlink_to(relative_path, target_is_directory=True)
    else:
        shutil.copytree(source, destination)
        metadata = {"source": str(source.resolve()), "skill": source.name}
        (destination / MARKER).write_text(json.dumps(metadata) + "\n", encoding="utf-8")
    return f"INSTALLED {source.name} ({mode}): {destination}"


def uninstall(source: Path, destination: Path, dry_run: bool) -> str:
    if not destination.exists() and not destination.is_symlink():
        return f"SKIP (not installed): {destination}"
    if not is_owned(destination, source):
        raise SkillError(f"Refusing to remove unmanaged path: {destination}")
    if dry_run:
        return f"DRY RUN remove {source.name}: {destination}"
    if destination.is_symlink():
        destination.unlink()
    else:
        shutil.rmtree(destination)
    return f"REMOVED {source.name}: {destination}"


def validate() -> list[str]:
    issues: list[str] = []
    for name in available_skills():
        directory = SKILLS / name
        content = (directory / "SKILL.md").read_text(encoding="utf-8")
        if not SKILL_NAME.fullmatch(name):
            issues.append(f"{name}: invalid directory name")
        match = re.match(r"\A---\n(.*?)\n---\n", content, flags=re.DOTALL)
        if not match:
            issues.append(f"{name}: missing YAML frontmatter")
            continue
        frontmatter = match.group(1)
        names = re.findall(r"^name:\s*(.+?)\s*$", frontmatter, flags=re.MULTILINE)
        descriptions = re.findall(r"^description:\s*(.+?)\s*$", frontmatter, flags=re.MULTILINE)
        if len(names) != 1 or names[0].strip('"\'') != name:
            issues.append(f"{name}: name must match directory")
        if len(descriptions) != 1 or not descriptions[0].strip():
            issues.append(f"{name}: missing description")
        for linked_path in REFERENCE_LINK.findall(content):
            if not (directory / linked_path).is_file():
                issues.append(f"{name}: missing reference {linked_path}")
    if not available_skills():
        issues.append("No valid skill directories found")
    return issues


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List available skills")
    commands.add_parser("validate", help="Validate skill metadata and local reference links")
    for command in ("install", "uninstall"):
        sub = commands.add_parser(command, help=f"{command.title()} selected skills")
        sub.add_argument("--agent", choices=["codex", "claude", "all"], required=True)
        sub.add_argument("--scope", choices=["project", "user"], default="project")
        sub.add_argument("--target", default=".", help="Project root; ignored for user scope")
        selection = sub.add_mutually_exclusive_group()
        selection.add_argument("--skill", action="append", help="Skill name; repeat or comma-separate")
        selection.add_argument("--all", action="store_true", help="Select all available skills")
        if command == "install":
            sub.add_argument("--mode", choices=["symlink", "copy"], default="symlink")
        sub.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = create_parser().parse_args()
    if args.command == "list":
        print("\n".join(available_skills()))
        return 0
    if args.command == "validate":
        issues = validate()
        if issues:
            print("\n".join(f"FAIL: {issue}" for issue in issues), file=sys.stderr)
            return 1
        print(f"PASS: {len(available_skills())} valid skills")
        return 0
    try:
        names = select_skills(args)
        targets = agent_targets(args)
        # Check all targets before changing any of them.
        for name in names:
            source = SKILLS / name
            for _, directory in targets:
                destination = directory / name
                if destination.exists() or destination.is_symlink():
                    if not is_owned(destination, source):
                        raise SkillError(f"Refusing to modify unmanaged path: {destination}")
        for name in names:
            source = SKILLS / name
            for _, directory in targets:
                destination = directory / name
                action = install(source, destination, args.mode, args.dry_run) if args.command == "install" else uninstall(source, destination, args.dry_run)
                print(action)
    except SkillError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
