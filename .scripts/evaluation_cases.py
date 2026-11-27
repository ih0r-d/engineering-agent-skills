"""Load and validate the repository's modular skill routing cases."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CASE_DIR = ROOT / "evals" / "cases"
FIXTURES = ROOT / "evals" / "fixtures"
FIELDS = {"id", "skill", "fixture", "prompt", "expected", "avoid_skills"}


def catalog_skills() -> set[str]:
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    return {skill for category in catalog["categories"] for skill in category["skills"]}


def catalog_case_paths() -> dict[str, Path]:
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    return {skill: CASE_DIR / category["id"] / f"{skill}.json"
            for category in catalog["categories"] for skill in category["skills"]}


def load_cases(skill: str | None = None) -> list[dict[str, Any]]:
    """Load all cases, one skill's cases, or unrelated cases in stable order."""
    if skill is not None:
        if skill not in catalog_skills():
            raise ValueError(f"Unknown evaluation skill {skill!r}")
        path = catalog_case_paths().get(skill)
        if path is None:
            raise ValueError(f"Unknown evaluation skill {skill!r}")
        if not path.is_file():
            raise ValueError(f"No evaluation case file for skill {skill!r}")
        paths = [path]
    else:
        paths = sorted(CASE_DIR.rglob("*.json"))
    cases: list[dict[str, Any]] = []
    for path in paths:
        try:
            values = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise ValueError(f"{path.relative_to(ROOT)}: invalid JSON: {error}") from error
        if not isinstance(values, list):
            raise ValueError(f"{path.relative_to(ROOT)}: expected a JSON array")
        cases.extend(values)
    return cases


def load_unrelated_cases() -> list[dict[str, Any]]:
    return _load_file(CASE_DIR / "unrelated.json")


def _load_file(path: Path) -> list[dict[str, Any]]:
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise ValueError(f"{path.relative_to(ROOT)}: invalid JSON: {error}") from error
    if not isinstance(result, list):
        raise ValueError(f"{path.relative_to(ROOT)}: expected a JSON array")
    return result


def cases_avoiding(skill: str) -> list[dict[str, Any]]:
    return [case for case in load_cases() if skill in case.get("avoid_skills", [])]


def relevant_cases(skill: str) -> list[dict[str, Any]]:
    """Select positive, explicit-avoidance, and unrelated routing examples."""
    return load_cases(skill) + cases_avoiding(skill) + load_unrelated_cases()


def validate_cases(skills: set[str] | None = None) -> list[str]:
    skills = catalog_skills() if skills is None else skills
    issues: list[str] = []
    skill_files = catalog_case_paths()
    expected_files = {path.relative_to(CASE_DIR).as_posix() for path in skill_files.values()} | {"unrelated.json"}
    if not CASE_DIR.is_dir():
        return ["evals/cases: missing case directory"]
    allowed_directories = {path.parent.relative_to(CASE_DIR).as_posix() for path in skill_files.values()}
    actual_paths = {path.relative_to(CASE_DIR).as_posix() for path in CASE_DIR.rglob("*")}
    actual_files = {relative for relative in actual_paths if (CASE_DIR / relative).is_file()}
    for name in sorted(expected_files - actual_files):
        issues.append(f"evals/cases/{name}: missing evaluation file")
    for name in sorted(actual_paths - expected_files - allowed_directories):
        issues.append(f"evals/cases/{name}: unexpected evaluation file")
    ids: set[str] = set()
    positive: set[str] = set()
    near_miss: set[str] = set()
    for path in sorted(CASE_DIR.rglob("*")):
        relative_path = path.relative_to(CASE_DIR).as_posix()
        if relative_path not in expected_files or path.suffix != ".json" or not path.is_file():
            continue
        try:
            filename = path.relative_to(ROOT).as_posix()
        except ValueError:
            filename = f"evals/cases/{path.name}"
        if path.is_symlink() or not path.resolve().is_relative_to(CASE_DIR.resolve()):
            issues.append(f"{filename}: evaluation file must be a regular file within evals/cases")
            continue
        try:
            cases = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            issues.append(f"{filename}: invalid JSON: {error}")
            continue
        if not isinstance(cases, list):
            issues.append(f"{filename}: expected a JSON array")
            continue
        for index, case in enumerate(cases):
            label = f"{filename}[{index}]"
            if not isinstance(case, dict):
                issues.append(f"{label}: expected an object")
                continue
            case_id = case.get("id")
            label = f"{filename} case {case_id!r}" if case_id is not None else label
            if set(case) != FIELDS:
                issues.append(f"{label}: expected fields {sorted(FIELDS)}")
            if not isinstance(case_id, str) or not case_id.strip():
                issues.append(f"{label}: id must be a non-empty string")
            elif case_id in ids:
                issues.append(f"{label}: duplicate case id")
            else:
                ids.add(case_id)
            skill = case.get("skill")
            expected_skill = None if relative_path == "unrelated.json" else path.stem
            if skill != expected_skill:
                issues.append(f"{label}: skill must match filename ({expected_skill!r})")
            if skill is not None and skill not in skills:
                issues.append(f"{label}: unknown primary skill {skill!r}")
            elif skill is not None:
                positive.add(skill)
            prompt = case.get("prompt")
            if not isinstance(prompt, str) or not prompt.strip():
                issues.append(f"{label}: prompt must be a non-empty string")
            expected = case.get("expected")
            if (not isinstance(expected, list) or not expected
                    or any(not isinstance(item, str) or not item.strip() for item in expected)):
                issues.append(f"{label}: expected must contain non-empty strings")
            avoided = case.get("avoid_skills")
            if not isinstance(avoided, list) or any(not isinstance(item, str) for item in avoided):
                issues.append(f"{label}: avoid_skills must be a list of skill IDs")
                avoided = []
            if len(set(avoided)) != len(avoided):
                issues.append(f"{label}: avoid_skills contains duplicates")
            for item in avoided:
                if item not in skills:
                    issues.append(f"{label}: unknown avoided skill {item!r}")
                near_miss.add(item)
            if skill in avoided:
                issues.append(f"{label}: primary skill appears in avoid_skills")
            fixture = case.get("fixture")
            if fixture is not None:
                if not isinstance(fixture, str) or not fixture.strip():
                    issues.append(f"{label}: fixture must be null or a relative path")
                else:
                    target = (FIXTURES / fixture).resolve()
                    if (not target.is_relative_to(FIXTURES.resolve()) or not target.is_dir()
                            or not any(target.iterdir())):
                        issues.append(f"{label}: invalid or unsafe fixture {fixture!r}")
    for skill in sorted(skills - positive):
        issues.append(f"{skill_files[skill].relative_to(ROOT)}: no positive case for {skill}")
    for skill in sorted(skills - near_miss):
        issues.append(f"evals/cases: no case avoids skill {skill}")
    return issues
