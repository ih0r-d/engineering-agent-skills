#!/usr/bin/env python3
"""Offline installer and validator for engineering agent skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from collections.abc import Iterator
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parent.parent
SKILLS = REPOSITORY / "skills"
CATALOG = REPOSITORY / "catalog.json"
MARKER = ".engineering-agent-skills.json"
AGENT_DIRECTORIES = {"codex": Path(".agents/skills"), "claude": Path(".claude/skills")}
SKILL_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
REFERENCE_LINK = re.compile(r"\]\((references/[^)#\s]+)(?:#[^)]*)?\)")
FIELDS = {"name", "description"}


class SkillError(Exception):
    """An expected installation or validation failure."""


def is_redirect(path: Path) -> bool:
    # On Windows, directory junctions redirect traversal without being symlinks.
    return path.is_symlink() or (os.name == "nt" and path.is_dir() and path.resolve() != path)


def skill_directories() -> list[Path]:
    if is_redirect(SKILLS) or not SKILLS.is_dir():
        raise SkillError(f"Expected a local skills directory: {SKILLS}")
    return sorted(path for path in SKILLS.iterdir() if not path.name.startswith(".")
                  and (path.is_dir() or path.is_symlink()))


def valid_name(name: str) -> bool:
    return len(name) <= 64 and SKILL_NAME.fullmatch(name) is not None


def available_skills() -> list[str]:
    return [path.name for path in skill_directories()
            if valid_name(path.name) and not is_redirect(path) and (path / "SKILL.md").is_file()]


def validate_catalog(path: Path, skill_ids: set[str]) -> list[str]:
    """Check logical category membership against the discovered skill IDs."""
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return [f"catalog.json: {error}"]

    if (not isinstance(catalog, dict) or set(catalog) != {"categories"}
            or not isinstance(catalog["categories"], list) or not catalog["categories"]):
        return ["catalog.json: expected a nonempty categories list"]

    issues = []
    categories: set[str] = set()
    listed: set[str] = set()
    for index, category in enumerate(catalog["categories"], start=1):
        if (not isinstance(category, dict) or set(category) != {"id", "name", "skills"}
                or not isinstance(category["id"], str) or not valid_name(category["id"])
                or not isinstance(category["name"], str) or not category["name"].strip()
                or not isinstance(category["skills"], list)):
            issues.append(f"catalog.json: invalid category at position {index}")
            continue
        category_id = category["id"]
        if category_id in categories:
            issues.append(f"catalog.json: duplicate category ID {category_id!r}")
        categories.add(category_id)
        for skill_id in category["skills"]:
            if not isinstance(skill_id, str) or not valid_name(skill_id):
                issues.append(f"catalog.json: invalid skill ID {skill_id!r} in {category_id!r}")
                continue
            if skill_id in listed:
                issues.append(f"catalog.json: duplicate skill {skill_id!r}")
            listed.add(skill_id)

    issues.extend(f"catalog.json: unknown skill {name!r}" for name in sorted(listed - skill_ids))
    issues.extend(f"catalog.json: missing skill {name!r}" for name in sorted(skill_ids - listed))
    return issues


def select_skills(args: argparse.Namespace, targets: list[Path]) -> list[str]:
    available = [path.name for path in skill_directories()]
    if args.all:
        if not available:
            raise SkillError("No skills available in the checkout.")
        names = available
    else:
        names = sorted({name.strip() for raw in args.skill for name in raw.split(",") if name.strip()})

    if not names:
        raise SkillError("Provide at least one skill name with --skill.")
    for name in names:
        if valid_name(name) and (name in available or (
                args.command == "uninstall" and any(os.path.lexists(target / name) for target in targets)
        )):
            continue
        raise SkillError(f"Unknown skill {name!r}. Available: {', '.join(available)}")
    return names


def check_target(directory: Path) -> None:
    for path in (directory.parent, directory):
        if os.path.lexists(path) and (is_redirect(path) or not path.is_dir()):
            raise SkillError(f"Expected a real directory at installation path: {path}")


def agent_targets(args: argparse.Namespace) -> list[Path]:
    if args.scope == "user" and args.target is not None:
        raise SkillError("Use --target only with project scope.")
    root = (Path.home() if args.scope == "user" else Path(args.target or ".").expanduser()).resolve()
    if not root.is_dir():
        raise SkillError(f"Target directory does not exist: {root}")
    agents = list(AGENT_DIRECTORIES) if args.agent == "all" else [args.agent]
    targets = [root / AGENT_DIRECTORIES[agent] for agent in agents]
    for target in targets:
        if target.is_relative_to(SKILLS):
            raise SkillError(f"Installation directory must be outside the source catalog: {target}")
        check_target(target)
    return targets


def tree_entries(directory: Path, *, installed: bool = False) -> Iterator[Path]:
    if is_redirect(directory) or not directory.is_dir():
        raise SkillError(f"Expected a real skill directory: {directory}")
    pending = [directory]
    while pending:
        for entry in pending.pop().iterdir():
            if entry == directory / MARKER:
                if installed:
                    continue
                raise SkillError(f"Reserved installer marker in source: {entry}")
            if is_redirect(entry):
                raise SkillError(f"Unexpected link inside skill: {entry}")
            if entry.is_dir():
                pending.append(entry)
            elif not entry.is_file():
                raise SkillError(f"Expected a regular file or directory: {entry}")
            yield entry


def tree_digest(directory: Path, *, installed: bool = False) -> str:
    """Fingerprint relative paths, file bytes, and executable bits."""
    entries = []
    for entry in tree_entries(directory, installed=installed):
        relative = entry.relative_to(directory).as_posix()
        if entry.is_dir():
            entries.append((relative, "directory"))
            continue
        digest = hashlib.sha256()
        with entry.open("rb") as stream:
            for block in iter(lambda: stream.read(65536), b""):
                digest.update(block)
        entries.append((relative, "file", entry.stat().st_mode & 0o111, digest.hexdigest()))
    return hashlib.sha256(json.dumps(sorted(entries)).encode("ascii")).hexdigest()


def owned_mode(source: Path, destination: Path) -> str:
    if destination.is_symlink():
        expected = os.path.relpath(source, start=destination.parent)
        if os.readlink(destination) == expected:
            return "symlink"
    elif destination.is_dir() and not is_redirect(destination):
        marker = destination / MARKER
        if not marker.is_symlink() and marker.is_file():
            try:
                metadata = json.loads(marker.read_text(encoding="utf-8"))
            except ValueError as error:
                raise SkillError(f"Invalid installer marker: {marker}") from error
            if isinstance(metadata, dict) and metadata.get("skill") == source.name:
                if metadata.get("format") == 1:
                    expected = metadata.get("sha256")
                elif metadata == {"source": str(source), "skill": source.name} and source.is_dir():
                    expected = tree_digest(source)
                else:
                    raise SkillError(f"Unrecognized installer marker: {marker}")
                if tree_digest(destination, installed=True) != expected:
                    raise SkillError(f"Copied skill has local changes or an unverifiable snapshot: {destination}")
                return "copy"
    raise SkillError(f"Refusing to modify unmanaged path: {destination}")


def install(source: Path, destination: Path, mode: str, digest: str | None) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if mode == "symlink":
        target = os.path.relpath(source, start=destination.parent)
        destination.symlink_to(target, target_is_directory=True)
        return

    # Reserve the destination exclusively. Write the ownership marker after the copy succeeds.
    destination.mkdir()
    try:
        for entry in tree_entries(source):
            target = destination / entry.relative_to(source)
            if entry.is_dir():
                target.mkdir()
            else:
                shutil.copy2(entry, target, follow_symlinks=False)
        if tree_digest(destination, installed=True) != digest:
            raise SkillError(f"Source changed while copying {source}")
        metadata = {"format": 1, "skill": source.name, "sha256": digest}
        with (destination / MARKER).open("x", encoding="utf-8") as marker:
            marker.write(json.dumps(metadata) + "\n")
    except (OSError, SkillError, KeyboardInterrupt):
        shutil.rmtree(destination)
        raise


def apply_selection(args: argparse.Namespace) -> None:
    targets = agent_targets(args)
    names = select_skills(args, targets)
    installing = args.command == "install"
    digests = {}
    if installing:
        for name in names:
            source = SKILLS / name
            issues = validate_skill(source)
            if issues:
                raise SkillError(issues[0])
            if args.mode == "copy":
                digests[name] = tree_digest(source)

    # Reject known conflicts across the selection before changing any destination.
    plan = []
    for name in names:
        source = SKILLS / name
        for target in targets:
            destination = target / name
            mode = owned_mode(source, destination) if os.path.lexists(destination) else None
            if installing and mode is not None and mode != args.mode:
                raise SkillError(f"Already installed in {mode} mode: {destination}. Uninstall first.")
            plan.append((source, destination, mode))

    for source, destination, mode in plan:
        if installing and mode is not None:
            print(f"SKIP (already installed): {destination}")
        elif installing:
            if args.dry_run:
                print(f"DRY RUN install {source.name} ({args.mode}): {destination}")
            else:
                check_target(destination.parent)
                install(source, destination, args.mode, digests.get(source.name))
                print(f"INSTALLED {source.name} ({args.mode}): {destination}")
        elif mode is None:
            print(f"SKIP (not installed): {destination}")
        elif args.dry_run:
            print(f"DRY RUN remove {source.name} ({mode}): {destination}")
        else:
            check_target(destination.parent)
            if owned_mode(source, destination) != mode:
                raise SkillError(f"Installation mode changed during removal: {destination}")
            if mode == "symlink":
                destination.unlink()
            else:
                shutil.rmtree(destination)
            print(f"REMOVED {source.name}: {destination}")


def frontmatter(content: str) -> tuple[dict[str, str], str]:
    """Read this catalog's flat, single-line YAML string fields."""
    header, separator, body = content[4:].partition("\n---\n")
    if not content.startswith("---\n") or not separator or not body.strip():
        raise SkillError("Expected YAML frontmatter followed by instructions")
    fields = {}
    for line in header.splitlines():
        key, separator, value = line.partition(": ")
        value = value.strip()
        if not separator or key not in FIELDS or key in fields:
            raise SkillError(f"Unexpected or repeated frontmatter field: {line}")
        if value.startswith('"'):
            try:
                value = json.loads(value)
            except ValueError as error:
                raise SkillError(f"Invalid quoted string for {key}") from error
        elif (not re.match(r"[a-zA-Z]|[0-9]+-[a-z]", value)
              or re.search(r":(?:\s|$)|\s#", value)
              or value.lower() in {"true", "false", "null", "yes", "no", "on", "off", "y", "n"}):
            raise SkillError(f"Expected a plain or double-quoted string for {key}")
        if not value.strip() or not value.isprintable():
            raise SkillError(f"Expected a nonempty single-line string for {key}")
        fields[key] = value
    if fields.keys() != FIELDS:
        raise SkillError("Expected name and description fields")
    return fields, body


def validate_skill(directory: Path) -> list[str]:
    name = directory.name
    manifest = directory / "SKILL.md"
    try:
        if not valid_name(name):
            raise SkillError("Invalid skill directory name (expected 1-64 lowercase letters, digits or hyphens)")
        if is_redirect(directory) or manifest.is_symlink() or not manifest.is_file():
            raise SkillError("Expected a real skill directory with a regular SKILL.md")
        fields, body = frontmatter(manifest.read_text(encoding="utf-8"))
        if fields["name"] != name:
            raise SkillError("Frontmatter name must match the directory")
        if len(fields["description"]) > 1024:
            raise SkillError("Description exceeds 1024 characters")
        actual = {path.relative_to(directory).as_posix() for path in tree_entries(directory)
                  if path.is_file() and path.is_relative_to(directory / "references")}
        linked = set(REFERENCE_LINK.findall(body))
        issues = [f"{name}: Missing or noncanonical reference: {path}" for path in sorted(linked - actual)]
        issues.extend(f"{name}: Unlinked reference: {path}" for path in sorted(actual - linked)
                      if path.endswith(".md"))
        return issues
    except (SkillError, OSError, UnicodeError) as error:
        return [f"{name}: {error}"]


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List available skills")
    commands.add_parser("validate", help="Validate skills, local reference links, and catalog membership")
    for command in ("install", "uninstall"):
        sub = commands.add_parser(command, help=f"{command.title()} selected skills")
        sub.add_argument("--agent", choices=[*AGENT_DIRECTORIES, "all"], required=True)
        sub.add_argument("--scope", choices=["project", "user"], default="project")
        sub.add_argument("--target", help="Project root (default: working directory)")
        selection = sub.add_mutually_exclusive_group(required=True)
        selection.add_argument("--skill", action="append", help="Skill name; repeat or comma-separate")
        selection.add_argument("--all", action="store_true", help="Select all skills in the checkout")
        if command == "install":
            sub.add_argument("--mode", choices=["symlink", "copy"], default="symlink")
        sub.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = create_parser().parse_args()
    try:
        if args.command == "list":
            print("\n".join(available_skills()))
        elif args.command == "validate":
            directories = skill_directories()
            issues = [issue for directory in directories for issue in validate_skill(directory)]
            issues.extend(validate_catalog(CATALOG, {directory.name for directory in directories}))
            if not directories:
                issues.append("No skill directories found")
            if issues:
                print("\n".join(f"FAIL: {issue}" for issue in issues), file=sys.stderr)
                return 1
            print(f"PASS: {len(directories)} valid skills")
        else:
            apply_selection(args)
    except (SkillError, OSError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("ERROR: Interrupted", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
