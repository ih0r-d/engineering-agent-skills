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

from scripts import skills

EVALS = Path(__file__).resolve().parents[1] / "evals"
FIXTURES = EVALS / "fixtures"


def run_fixture(fixture: str, *command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=FIXTURES / fixture, capture_output=True, text=True,
                          check=False, timeout=10)


class EvaluationTests(unittest.TestCase):
    def test_routing_cases_cover_catalog_and_resolve_fixtures(self) -> None:
        cases = json.loads((EVALS / "cases.json").read_text(encoding="utf-8"))
        names = {case["skill"] for case in cases}
        self.assertEqual(set(skills.available_skills()) | {None}, names)
        identifiers = [case["id"] for case in cases]
        self.assertEqual(len(set(identifiers)), len(cases))
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["prompt"].strip())
                self.assertTrue(case["expected"])
                self.assertTrue(all(check.strip() for check in case["expected"]))
                if case["fixture"] is not None:
                    fixture = FIXTURES / case["fixture"]
                    self.assertEqual(FIXTURES, fixture.resolve().parent)
                    self.assertTrue(fixture.is_dir())
                    self.assertTrue(any(fixture.iterdir()))

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
