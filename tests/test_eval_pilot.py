"""Validate pilot plans and graders using only local synthetic sources."""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".scripts"))

import eval_pilot
import evaluation_cases
import skills


class PilotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = eval_pilot.scenarios()

    def test_pilot_preserves_case_prompts_and_routing_expectations(self) -> None:
        originals = {case["id"]: case for case in evaluation_cases.load_cases()}
        self.assertEqual(6, len(self.cases))
        for name, scenario in self.cases.items():
            with self.subTest(scenario=name):
                self.assertTrue(scenario.fixture.is_dir())
                if name in originals:
                    original = originals[name]
                    self.assertEqual(original["prompt"], scenario.prompt)
                    self.assertEqual(original["skill"], scenario.skill)
                    self.assertEqual(tuple(original["avoid_skills"]), scenario.avoided_skills)
                    self.assertEqual(tuple(original["expected"]), scenario.expected)
                for reference in scenario.references:
                    self.assertTrue((skills.skill_path(scenario.skill) / "references" / reference).is_file())

    def test_default_and_selected_plans_need_no_environment_or_subprocess(self) -> None:
        for args, expected in (
            ([], "6 comparisons (12 separate sessions)"),
            (["--scenario", "java-feature", "--details"], "1 comparison (2 separate sessions)"),
        ):
            with self.subTest(args=args), patch.dict(os.environ, clear=True), patch.object(
                subprocess, "Popen", side_effect=AssertionError("planning must remain offline")
            ), redirect_stdout(StringIO()) as output:
                self.assertEqual(0, eval_pilot.main(args))
                self.assertIn(expected, output.getvalue())
                if args:
                    case = self.cases["java-feature"]
                    self.assertIn(case.prompt, output.getvalue())
                    for criterion in case.expected:
                        self.assertNotIn(criterion, output.getvalue())
                else:
                    self.assertNotIn("Prompt:", output.getvalue())

    def test_planner_rejects_execution_args_and_duplicate_cases(self) -> None:
        for args in (["--live"], ["run"], ["--scenario", "java-feature", "--scenario", "java-feature"]):
            with self.subTest(args=args), redirect_stderr(StringIO()), patch.object(
                subprocess, "Popen", side_effect=AssertionError("unexpected subprocess")
            ), self.assertRaises(SystemExit) as error:
                eval_pilot.main(args)
            self.assertEqual(2, error.exception.code)

    def check_grader(self, case_id, tools, before, replace_source):
        case = self.cases[case_id]
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "workspace"
            grading = Path(temporary) / "grading"
            shutil.copytree(case.fixture, workspace)
            grading.mkdir()

            def execute(name, command, *, expected_output=None):
                result = subprocess.run(
                    [tools[command[0]], *command[1:]], cwd=grading, env={"PATH": os.defpath},
                    capture_output=True, text=True, timeout=15, check=False,
                )
                passed = result.returncode == 0 and (
                    expected_output is None or result.stdout.strip() == expected_output
                )
                return {"name": name, "status": "passed" if passed else "failed"}

            original = eval_pilot.grade_behavior(case, workspace, grading, execute)
            self.assertEqual(before, [check["status"] for check in original], original)
            source = workspace / case.editable
            source.write_text(replace_source(source.read_text(encoding="utf-8")), encoding="utf-8")
            updated = eval_pilot.grade_behavior(case, workspace, grading, execute)
            self.assertEqual(["passed"] * len(before), [check["status"] for check in updated], updated)

    def test_python_grader_detects_shared_defaults_and_checks_regressions(self) -> None:
        def fix(source):
            return source.replace("tags: list[str] = []", "tags: list[str] | None = None").replace(
                "    tags.append(tag)", "    if tags is None:\n        tags = []\n    tags.append(tag)", 1
            )

        self.check_grader("code-review-near-miss-python-fix", {"python3": sys.executable},
                          ["passed", "failed", "passed"], fix)

    def test_java_grader_checks_overload_and_existing_contract(self) -> None:
        jdk = os.environ.get("JAVA_HOME")
        jdk_bin = str(Path(jdk) / "bin") + os.pathsep if jdk else ""
        path = jdk_bin + os.environ.get("PATH", os.defpath)
        tools = {name: shutil.which(name, path=path) for name in ("java", "javac")}
        if not all(tools.values()):
            self.skipTest("An installed Java 11+ JDK is optional")
        version = subprocess.run([tools["javac"], "-version"], capture_output=True, text=True,
                                 env={"PATH": os.defpath}, timeout=5, check=False)
        match = re.search(r"\bjavac (\d+)", version.stdout + version.stderr)
        if version.returncode or not match or int(match[1]) < 11:
            self.skipTest("An installed Java 11+ JDK is optional")

        def implement(source):
            end = source.rindex("}")
            return source[:end] + """
    public static String label(String name, String fallback) {
        if (name == null) return fallback;
        String value = label(name);
        return value.isEmpty() ? fallback : value;
    }
}
"""

        self.check_grader("java-feature", tools, ["passed", "passed", "failed", "passed"], implement)

    def test_shell_reproducer_masks_failure_as_expected(self) -> None:
        scenario = self.cases["shell-quality-trap-status"]
        result = subprocess.run(["sh", "cleanup.sh"], cwd=scenario.fixture, text=True, capture_output=True,
                                env={"PATH": os.defpath}, timeout=5, check=False)
        self.assertEqual(0, result.returncode)
        self.assertEqual("cleanup complete\n", result.stdout)
