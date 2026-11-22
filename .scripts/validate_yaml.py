# /// script
# requires-python = ">=3.10"
# dependencies = ["PyYAML==6.0.4"]
# ///
"""Check repository YAML and Skill frontmatter with a full YAML parser."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import yaml


def validate_file(path: Path) -> None:
    contents = path.read_text(encoding="utf-8")
    if path.name == "SKILL.md":
        header, delimiter, _ = contents[4:].partition("\n---\n")
        if not contents.startswith("---\n") or not delimiter:
            raise ValueError("Expected YAML frontmatter")
        fields = yaml.safe_load(header)
        if not isinstance(fields, dict) or not all(
            isinstance(fields.get(key), str) for key in ("name", "description")
        ):
            raise ValueError("Expected YAML strings for name and description")
    else:
        # Compose every document to check YAML syntax and alias resolution.
        for _ in yaml.compose_all(contents, Loader=yaml.SafeLoader):
            pass


def main() -> int:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--",
             "*.yaml", "*.yml", "skills/*/SKILL.md"],
            check=True, stdout=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"ERROR: Could not enumerate repository YAML files: {error}", file=sys.stderr)
        return 1

    paths = sorted({Path(os.fsdecode(entry)) for entry in result.stdout.split(b"\0") if entry})
    failures = []
    for path in paths:
        try:
            validate_file(path)
        except (OSError, ValueError, yaml.YAMLError) as error:
            failures.append(f"{path}: {error}")
    if failures:
        print("\n".join(f"FAIL: {failure}" for failure in failures), file=sys.stderr)
        return 1
    print(f"PASS: parsed YAML in {len(paths)} repository files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
