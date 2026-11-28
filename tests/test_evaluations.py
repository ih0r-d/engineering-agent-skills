"""Validate evaluation inputs and reproduce sample behavior without an AI agent."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".scripts"))

import evaluation_cases
import skills
EVALS = Path(__file__).resolve().parents[1] / "evals"
FIXTURES = EVALS / "fixtures"


def run_fixture(fixture: str, *command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=FIXTURES / fixture, capture_output=True, text=True,
                          check=False, timeout=10)


class EvaluationTests(unittest.TestCase):
    def test_routing_cases_cover_catalog_and_resolve_fixtures(self) -> None:
        cases = evaluation_cases.load_cases()
        catalog = set(skills.available_skills())
        names = {case["skill"] for case in cases}
        self.assertEqual(catalog | {None}, names)
        identifiers = [case["id"] for case in cases]
        self.assertEqual(len(set(identifiers)), len(cases))
        near_miss_skills = set()
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["prompt"].strip())
                avoided = case["avoid_skills"]
                if case["skill"] is not None:
                    near_miss_skills.update(avoided)
        self.assertEqual(catalog, near_miss_skills)
        self.assertEqual([], evaluation_cases.validate_cases(catalog))

    def test_loader_selects_skill_avoided_and_unrelated_cases(self) -> None:
        review = evaluation_cases.load_cases("review-code")
        self.assertTrue(review)
        self.assertTrue(all(case["skill"] == "review-code" for case in review))
        self.assertEqual(
            [case for case in evaluation_cases.load_cases() if "review-code" in case["avoid_skills"]],
            evaluation_cases.cases_avoiding("review-code"),
        )
        unrelated = evaluation_cases.load_unrelated_cases()
        self.assertTrue(unrelated)
        self.assertTrue(all(case["skill"] is None for case in unrelated))
        self.assertEqual(
            review + evaluation_cases.cases_avoiding("review-code") + unrelated,
            evaluation_cases.relevant_cases("review-code"),
        )

    def test_validation_reports_case_and_filename_for_malformed_case(self) -> None:
        original_dir = evaluation_cases.CASE_DIR
        try:
            evaluation_cases.CASE_DIR = EVALS / "cases"
            case_file = evaluation_cases.catalog_case_paths()["review-code"]
            cases = json.loads(case_file.read_text())
            cases[0]["prompt"] = " "
            # The validator operates on the real catalog and files. Exercise its diagnostic
            # formatting through a copied temporary case tree, without changing repository data.
            import tempfile
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                for path in evaluation_cases.CASE_DIR.rglob("*.json"):
                    destination = root / path.relative_to(evaluation_cases.CASE_DIR)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
                destination = root / case_file.relative_to(evaluation_cases.CASE_DIR)
                destination.write_text(json.dumps(cases), encoding="utf-8")
                evaluation_cases.CASE_DIR = root
                issues = evaluation_cases.validate_cases()
                self.assertTrue(any("review-code.json case '" in issue and "prompt" in issue for issue in issues), issues)
        finally:
            evaluation_cases.CASE_DIR = original_dir

    def test_python_default_shares_state_and_explicit_mutation_is_scoped(self) -> None:
        program = """
from tags import add_tag, add_to_explicit_list

first = add_tag("one")
second = add_tag("two")
explicit = ["original"]
add_to_explicit_list("one", explicit)
print(first is second, first, explicit)
"""
        result = run_fixture("python", sys.executable, "-B", "-c", program)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("True ['one', 'two'] ['original', 'one']\n", result.stdout)

    @unittest.skipUnless(os.name == "posix", "POSIX sh is required")
    def test_shell_argument_boundaries(self) -> None:
        for mode, expected in (("unsafe", "<two>\n<words>\n"), ("safe", "<two words>\n")):
            with self.subTest(mode=mode):
                result = run_fixture("shell", "sh", "./print-path.sh", mode, "two words")
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(expected, result.stdout)

    @unittest.skipUnless(shutil.which("make"), "Make is unavailable")
    def test_make_directory_scope(self) -> None:
        bad = run_fixture("build", "make", "bad")
        good = run_fixture("build", "make", "good")
        self.assertNotEqual(0, bad.returncode, bad.stdout)
        self.assertEqual(0, good.returncode, good.stderr)

    def test_quickstart_examples_match_cli_ground_truth(self) -> None:
        guide = (FIXTURES / "docs/README.md").read_text(encoding="utf-8")
        examples = re.findall(r"```sh\npython3 cli.py ([^\n]+)\n```", guide)
        self.assertEqual(2, len(examples))
        text_example = run_fixture("docs", sys.executable, "cli.py", *examples[0].split())
        stale_example = run_fixture("docs", sys.executable, "cli.py", *examples[1].split())
        corrected = run_fixture("docs", sys.executable, "cli.py", "--format", "json")
        for result in (text_example, corrected):
            self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("ok\n", text_example.stdout)
        self.assertEqual(2, stale_example.returncode)
        self.assertIn("--json", stale_example.stderr)
        self.assertEqual({"status": "ok"}, json.loads(corrected.stdout))

    def test_code_review_fixture_passes_existing_tests_but_underfills_sparse_matches(self) -> None:
        existing = run_fixture("code-review", sys.executable, "-B", "-m", "unittest", "-v",
                               "test_first_matches")
        self.assertEqual(0, existing.returncode, existing.stderr)

        program = """
import after
import before

items = ['bronze', 'amber', 'azure']
print(before.first_matches(items, 'a', 2))
print(after.first_matches(items, 'a', 2))
"""
        result = run_fixture("code-review", sys.executable, "-B", "-c", program)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("['amber', 'azure']\n['amber']\n", result.stdout)

    def test_clean_review_fixture_preserves_observable_results(self) -> None:
        program = """
from itertools import product
from before import first_matches as baseline
from clean import first_matches as candidate

for items, prefix, limit in product(
    ([], ['bronze', 'amber', 'azure'], ['amber', 'amber', 'bronze']),
    ('a', 'b', '', 'z'),
    (-1, 0, 1, 2, 5),
):
    assert candidate(items, prefix, limit) == baseline(items, prefix, limit), (items, prefix, limit)
"""
        result = run_fixture("code-review", sys.executable, "-B", "-c", program)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_refactoring_fixture_has_public_behavior_baseline(self) -> None:
        result = run_fixture("refactoring", sys.executable, "-B", "-m", "unittest", "-v",
                             "test_summary")
        self.assertEqual(0, result.returncode, result.stderr)
