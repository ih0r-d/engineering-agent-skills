#!/usr/bin/env python3
"""Generate or check the catalog block in the repository README."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
BEGIN = "<!-- BEGIN GENERATED SKILL CATALOG -->"
END = "<!-- END GENERATED SKILL CATALOG -->"


def markdown_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ").strip()


def render_catalog(catalog: dict[str, Any], descriptions: dict[str, str], inventory: dict[str, int]) -> str:
    script_label = "script" if inventory["scripts"] == 1 else "scripts"
    lines = [
        f"**Inventory:** {inventory['skills']} skills · {inventory['categories']} categories · "
        f"{inventory['references']} references · {inventory['assets']} assets · "
        f"{inventory['scripts']} {script_label} · "
        f"{inventory['evaluation_cases']} evaluation cases.",
        "",
    ]
    for category in catalog["categories"]:
        lines.extend((f"### {category['name']}", "", "| Skill | Purpose |", "| --- | --- |"))
        for skill in category["skills"]:
            description = markdown_cell(descriptions[skill])
            target = f"skills/{category['id']}/{skill}/SKILL.md"
            lines.append(f"| [`{skill}`]({target}) | {description} |")
        lines.append("")
    return "\n".join(lines).rstrip()


def replace_generated_section(readme: str, generated: str) -> str:
    if readme.count(BEGIN) != 1 or readme.count(END) != 1:
        raise ValueError("README must contain exactly one generated catalog begin/end marker pair")
    start = readme.index(BEGIN) + len(BEGIN)
    end = readme.index(END)
    if end < start:
        raise ValueError("README generated catalog markers are out of order")
    return readme[:start] + "\n\n" + generated + "\n\n" + readme[end:]


def load_catalog_content() -> tuple[dict[str, Any], dict[str, str], dict[str, int]]:
    try:
        catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
        if not isinstance(catalog, dict) or not isinstance(catalog.get("categories"), list):
            raise ValueError("catalog.json must contain a categories list")
        sys.path.insert(0, str(ROOT / ".scripts"))
        import skills
        import validate_yaml
        skill_fields = validate_yaml.skill_fields

        locations = skills.discover_skill_locations()
        issues = skills.validate_catalog(
            ROOT / "catalog.json", {location.name for location in locations}, locations,
        )
        if issues:
            raise ValueError("catalog validation failed: " + "; ".join(issues))

        descriptions: dict[str, str] = {}
        for category in catalog["categories"]:
            category_id = category["id"]
            for skill in category["skills"]:
                manifest = ROOT / "skills" / category_id / skill / "SKILL.md"
                try:
                    fields = skill_fields(manifest.read_text(encoding="utf-8"))
                except (OSError, skills.SkillError, validate_yaml.yaml.YAMLError, ValueError) as error:
                    raise ValueError(f"{manifest}: cannot parse skill metadata: {error}") from error
                if fields.get("name") != skill:
                    raise ValueError(f"{manifest}: frontmatter name does not match catalog ID {skill!r}")
                description = fields.get("description")
                if not isinstance(description, str) or not description.strip():
                    raise ValueError(f"{manifest}: description must be a non-empty YAML string")
                descriptions[skill] = description

        package = skills.skill_directories()

        def resource_count(kind: str) -> int:
            return sum(1 for directory in (ROOT / "skills").glob(f"*/*/{kind}")
                       for path in directory.rglob("*") if path.is_file())

        evaluation_cases = 0
        for path in sorted((ROOT / "evals/cases").rglob("*.json")):
            cases = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(cases, list):
                raise ValueError(f"{path}: evaluation file must contain a JSON array")
            evaluation_cases += len(cases)
        inventory = {
            "skills": len(package),
            "categories": len(catalog["categories"]),
            "references": resource_count("references"),
            "assets": resource_count("assets"),
            "scripts": resource_count("scripts"),
            "evaluation_cases": evaluation_cases,
        }
        if len(descriptions) != inventory["skills"]:
            raise ValueError("Catalog skill IDs are not globally unique or metadata is incomplete")
        return catalog, descriptions, inventory
    except (OSError, KeyError, TypeError, json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"cannot generate catalog from repository metadata: {error}") from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check freshness without modifying README.md")
    args = parser.parse_args()
    try:
        catalog, descriptions, inventory = load_catalog_content()
        generated = render_catalog(catalog, descriptions, inventory)
        current = README.read_text(encoding="utf-8")
        updated = replace_generated_section(current, generated)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.check:
        if updated != current:
            print("STALE: README skill catalog differs from catalog.json or SKILL.md metadata; run `task docs:generate`.",
                  file=sys.stderr)
            return 1
        print("PASS: generated README skill catalog is current")
        return 0

    if updated != current:
        README.write_text(updated, encoding="utf-8")
    print("WROTE: README skill catalog updated" if updated != current else "OK: README skill catalog is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
