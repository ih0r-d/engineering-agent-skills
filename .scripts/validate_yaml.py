# /// script
# requires-python = ">=3.10"
# dependencies = ["PyYAML==6.0.4"]
# ///
"""Check repository YAML and Skill frontmatter with a full YAML parser."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml
from yaml.nodes import MappingNode, Node, ScalarNode

import skills


YAML_TAG = "tag:yaml.org,2002:"


class FrontmatterLoader(yaml.SafeLoader):
    # Resolve plain scalars as YAML 1.2 core types so words such as `on` stay strings.
    yaml_implicit_resolvers = {
        first: [(tag, pattern) for tag, pattern in resolvers
                if tag.removeprefix(YAML_TAG) not in {"bool", "int", "float", "timestamp", "merge", "value"}]
        for first, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }


FrontmatterLoader.add_implicit_resolver(
    YAML_TAG + "bool", re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"), "tTfF",
)
FrontmatterLoader.add_implicit_resolver(
    YAML_TAG + "int", re.compile(r"^(?:[-+]?[0-9]+|0o[0-7]+|0x[0-9a-fA-F]+)$"), "-+0123456789",
)
FrontmatterLoader.add_implicit_resolver(
    YAML_TAG + "float",
    re.compile(r"^(?:[-+]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][-+]?[0-9]+)?"
               r"|[-+]?\.(?:inf|Inf|INF)|\.(?:nan|NaN|NAN))$"),
    "-+.0123456789",
)


def read_string(node: Node, field: str) -> str:
    if not isinstance(node, ScalarNode) or node.tag != YAML_TAG + "str":
        raise ValueError(f"{field} must be a YAML string")
    return node.value


def read_mapping(node: Node | None, field: str) -> dict[str, Node]:
    if not isinstance(node, MappingNode) or node.tag != YAML_TAG + "map":
        raise ValueError(f"{field} must be a YAML mapping")
    entries = {}
    for key_node, value in node.value:
        key = read_string(key_node, f"{field} key")
        if key in entries:
            raise ValueError(f"Duplicate key {key!r} in {field}")
        entries[key] = value
    return entries


def skill_fields(content: str) -> dict[str, str | dict[str, str]]:
    header, _ = skills.split_manifest(content)
    nodes = read_mapping(yaml.compose(header, Loader=FrontmatterLoader), "Frontmatter")
    fields = {}
    for key, node in nodes.items():
        if key == "metadata":
            fields[key] = {name: read_string(value, f"metadata.{name}")
                           for name, value in read_mapping(node, "metadata").items()}
        else:
            fields[key] = read_string(node, key)
    return fields


def check_specification(fields: dict[str, str | dict[str, str]], directory: Path) -> None:
    # Use the upstream metadata validator with parsed YAML. Its CLI parser accepts a YAML subset.
    from skills_ref.validator import validate_metadata

    issues = validate_metadata(fields, directory)
    name = fields.get("name")
    if isinstance(name, str) and name != name.strip():
        issues.append("name must not contain surrounding whitespace")
    if fields.get("compatibility") == "":
        issues.append("compatibility must contain 1 to 500 characters when provided")
    tools = fields.get("allowed-tools")
    if isinstance(tools, str) and any(c.isspace() and c != " " for c in tools.strip()):
        issues.append("allowed-tools must be a space-separated string")
    if issues:
        raise ValueError("; ".join(issues))


def validate_file(path: Path, *, spec: bool) -> None:
    contents = path.read_text(encoding="utf-8")
    if path.name == "SKILL.md":
        fields = skill_fields(contents)
        if spec:
            check_specification(fields, path.parent)
        elif not {"name", "description"} <= fields.keys():
            raise ValueError("Expected YAML strings for name and description")
    else:
        # Compose every document to check YAML syntax and alias resolution.
        for _ in yaml.compose_all(contents, Loader=yaml.SafeLoader):
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", action="store_true", help="Require the official Agent Skills validator")
    args = parser.parse_args()
    try:
        manifests = [directory / "SKILL.md" for directory in skills.skill_directories()]
        if not manifests:
            raise skills.SkillError("No skill directories found")
        result = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--",
             "*.yaml", "*.yml"],
            check=True, stdout=subprocess.PIPE,
        )
    except (OSError, skills.SkillError, subprocess.CalledProcessError) as error:
        print(f"ERROR: Could not enumerate repository YAML files: {error}", file=sys.stderr)
        return 1

    paths = {Path(os.fsdecode(entry)) for entry in result.stdout.split(b"\0") if entry}
    paths.update(path.relative_to(skills.REPOSITORY) for path in manifests)
    failures = []
    for path in sorted(paths):
        try:
            validate_file(path, spec=args.spec)
        except (OSError, skills.SkillError, ValueError, yaml.YAMLError) as error:
            failures.append(f"{path}: {error}")
    if failures:
        print("\n".join(f"FAIL: {failure}" for failure in failures), file=sys.stderr)
        return 1
    print(f"PASS: parsed YAML in {len(paths)} repository files")
    if args.spec:
        print(f"PASS: Agent Skills specification validation for {len(manifests)} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
