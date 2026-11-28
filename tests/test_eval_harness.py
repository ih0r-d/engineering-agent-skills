"""Exercise the pilot without invoking the Codex CLI or any model."""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
from types import SimpleNamespace
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".scripts"))

import eval_auth
import eval_harness as harness
import eval_observations as observations
import eval_pilot
import evaluation_cases


def strings(*events: dict) -> list[str]:
    return [json.dumps(event) for event in events]


def fake_oauth(path: Path, access: str = "old-access-token", mode: str = "chatgpt") -> None:
    path.write_text(json.dumps({"auth_mode": mode, "OPENAI_API_KEY": None, "tokens": {
        "access_token": access, "refresh_token": "test-refresh-token", "id_token": "test-id-token",
    }}))
    path.chmod(0o600)


class EventTests(unittest.TestCase):
    def test_cumulative_usage_and_observed_reads(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            skill = ".agents/skills/debug/SKILL.md"
            reference = ".agents/skills/debug/references/python/state-ownership.md"
            shell = {"type": "command_execution", "id": "a", "command": f"cat {root / skill}"}
            result = observations.parse_events(strings(
                {"type": "thread.started", "thread_id": "synthetic"},
                {"type": "item.started", "item": shell},
                {"type": "item.updated", "item": shell},
                {"type": "item.completed", "item": {**shell, "status": "completed", "exit_code": 0}},
                {"type": "item.completed", "item": {**shell, "id": "b", "command": f"cat {reference}",
                                                    "status": "completed", "exit_code": 0}},
                {"type": "item.completed", "item": {"type": "agent_message", "id": "c", "text": "Final"}},
                {"type": "turn.completed", "usage": {"input_tokens": 80, "cached_input_tokens": 60,
                                                    "output_tokens": 20, "reasoning_output_tokens": 9}},
            ), root, {skill, reference})
        self.assertEqual(2, result["observed_tool_calls"])
        self.assertEqual(100, result["usage"]["total_tokens"])
        self.assertEqual(60, result["usage"]["cached_input_tokens"])
        self.assertEqual(9, result["usage"]["reasoning_output_tokens"])
        self.assertEqual([skill], result["observed_skill_manifests"])
        self.assertEqual([], result["observed_references"])
        self.assertEqual([reference], result["possible_relative_skill_reads"])
        self.assertEqual("Final", result["final_response"])
        self.assertIsNone(result["direct_skill_activation"])

    def test_missing_malformed_or_defaulted_metrics(self) -> None:
        trace = ["{", "null", "{}", '{"type":"item.completed","item":false}',
                 '{"type":"turn.completed","usage":{"input_tokens":0,"output_tokens":0}}']
        result = observations.parse_events(trace, Path("/tmp"), set())
        self.assertEqual(4, result["malformed_lines"])
        self.assertTrue(all(value is None for value in result["usage"].values()))
        self.assertIsNone(observations.parse_events([], Path("/tmp"), set())["observed_tool_calls"])
        partial = observations.parse_events(strings(
            {"type": "turn.completed", "usage": {"input_tokens": 7, "cached_input_tokens": 8,
                                                "output_tokens": True}},
        ), Path("/tmp"), set())
        self.assertIsNone(partial["usage"]["cached_input_tokens"])
        self.assertIsNone(partial["usage"]["total_tokens"])

    def test_errors_delegation_and_patch_are_reported_from_structured_items(self) -> None:
        trace = strings(
            {"type": "turn.failed", "error": {"message": "synthetic quota error"}},
            {"type": "item.completed", "item": {"type": "collab_tool_call", "id": "spawn",
                                                "tool": "spawn_agent", "status": "failed"}},
            {"type": "item.completed", "item": {"type": "file_change", "id": "patch",
                                                "status": "completed", "changes": [{"path": "before.py"}]}},
        )
        record = observations.parse_events(trace, Path("/tmp"), set())
        self.assertEqual(["synthetic quota error"], record["errors"])
        self.assertEqual("spawn_agent", record["delegation"][0]["tool"])
        self.assertEqual(["before.py"], record["patch_paths"])

    def test_only_concrete_read_commands_count(self) -> None:
        path = "/tmp/x/references/guide.md"
        self.assertEqual([path], observations.literal_read_paths(f"/bin/sh -lc \"sed -n '1,60p' {path}\""))
        self.assertEqual([], observations.literal_read_paths(f"echo cat {path}"))
        self.assertEqual([], observations.literal_read_paths(f"cat {path} && echo done"))
        self.assertEqual([], observations.literal_read_paths("cat $UNRESOLVED_PATH"))


class HarnessTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        self.cases = eval_pilot.scenarios()

    def test_original_case_prompts_are_reused(self) -> None:
        originals = {case["id"]: case for case in evaluation_cases.load_cases()}
        self.assertEqual(6, len(self.cases))
        for name, scenario in self.cases.items():
            if name != "java-feature":
                self.assertEqual(originals[name]["prompt"], scenario.prompt)
            self.assertNotIn(f"${scenario.skill}", scenario.prompt)

    def test_dry_run_does_not_invoke_codex_or_create_output(self) -> None:
        output = self.root / "new-results"
        stdout = io.StringIO()
        with patch.object(harness.subprocess, "Popen", side_effect=AssertionError("unexpected subprocess")):
            with redirect_stdout(stdout):
                status = harness.main(["run", "--auth", "chatgpt", "--output", str(output)])
        self.assertEqual(0, status)
        self.assertIn("12 / 12", stdout.getvalue())
        self.assertFalse(output.exists())

    def test_explicit_budget_is_checked_before_live_setup(self) -> None:
        stderr = io.StringIO()
        with patch.object(harness.shutil, "which", side_effect=AssertionError("unexpected live setup")):
            with redirect_stdout(io.StringIO()), redirect_stderr(stderr):
                code = harness.main(["run", "--live", "--scenario", "java-feature", "--repetitions", "2",
                                     "--max-runs", "3", "--model", "example", "--reasoning-effort", "low"])
        self.assertEqual(2, code)
        self.assertIn("Planned 4 runs", stderr.getvalue())

    def test_repeated_pairs_alternate_order(self) -> None:
        args = SimpleNamespace(scenario=["java-feature"], configuration="AB", repetitions=2, max_runs=4)
        self.assertEqual([("A", 1), ("B", 1), ("B", 2), ("A", 2)],
                         [(config, index) for _, config, index in harness.selected_runs(args)])

    def test_copy_installation_is_the_only_workspace_difference(self) -> None:
        case = self.cases["code-review-near-miss-python-fix"]
        home = self.root / "user"
        home.mkdir()
        user_config = home / ".codex/config.toml"
        user_config.parent.mkdir()
        user_config.write_text("keep user settings", encoding="utf-8")
        unrelated = home / ".agents/skills/unrelated/SKILL.md"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text("keep unrelated skill", encoding="utf-8")
        prior = harness.snapshot(home)
        with patch.dict(os.environ, {"HOME": str(home), "CODEX_HOME": str(user_config.parent),
                                     "CODEX_API_KEY": "synthetic-key", "GIT_CONFIG_COUNT": "1"}):
            env = harness.process_environment(self.root / "isolated")
            a, digest_a = harness.prepare_workspace(self.root / "a", case, "A")
            b, digest_b = harness.prepare_workspace(self.root / "b", case, "B")
        self.assertEqual(prior, harness.snapshot(home))
        self.assertNotIn("CODEX_API_KEY", env)
        self.assertNotIn("GIT_CONFIG_COUNT", env)
        self.assertNotEqual(str(user_config.parent), env["CODEX_HOME"])
        self.assertEqual([], list(Path(env["CODEX_HOME"]).iterdir()))
        self.assertEqual(digest_a, digest_b)
        self.assertEqual(a, {k: v for k, v in b.items() if k != ".agents" and not k.startswith(".agents/")})
        self.assertEqual(evaluation_cases.catalog_skills(), {p.name for p in (self.root / "b/.agents/skills").iterdir()})
        self.assertFalse((self.root / "b/tags.py").is_symlink())
        (self.root / "b/tags.py").write_text("isolated edit", encoding="utf-8")
        self.assertEqual(a, harness.snapshot(self.root / "a"))

    def test_ancestor_discovery_and_snapshot_symlinks(self) -> None:
        project = self.root / "project"
        project.mkdir()
        (self.root / "AGENTS.override.md").touch()
        with self.assertRaisesRegex(harness.EvalError, "Ancestor"):
            harness.verify_local_discovery(project)
        (project / "escape").symlink_to(self.root, target_is_directory=True)
        self.assertEqual({"escape": {"kind": "symlink", "target": str(self.root)}}, harness.snapshot(project))

    def test_read_only_violation_includes_restored_patches(self) -> None:
        case = self.cases["code-review-selection-regression"]
        self.assertEqual(["before.py", "extra.txt"], harness.violations(
            case, self.root, {"extra.txt": {}}, {"patch_paths": [str(self.root / "before.py")]}))

    def test_process_timeout_keeps_partial_output_for_redaction(self) -> None:
        execution = harness.run_process(
            [sys.executable, "-c", "import time; print('started', flush=True); time.sleep(20)"],
            cwd=self.root, env={}, timeout=1, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
        self.assertTrue(execution["timed_out"])
        self.assertLess(execution["wall_seconds"], 5)
        self.assertEqual(b"started\n", execution["stdout"])

    def test_python_hidden_grades_fail_before_fix_and_preserve_regressions(self) -> None:
        case = self.cases["code-review-near-miss-python-fix"]
        project = self.root / "project"
        shutil.copytree(case.fixture, project)
        grading = self.root / "grades"
        grading.mkdir()

        def execute(name, command, *, expected_output):
            done = subprocess.run([sys.executable, *command[1:]], cwd=grading,
                                  capture_output=True, text=True, env={}, check=False, timeout=5)
            passed = done.returncode == 0 and done.stdout.strip() == expected_output
            return {"name": name, "status": "passed" if passed else "failed"}

        results = eval_pilot.grade_behavior(case, project, grading, execute)
        self.assertEqual(["passed", "failed", "passed"], [check["status"] for check in results])
        source = project / "tags.py"
        code = source.read_text(encoding="utf-8")
        code = code.replace("tags: list[str] = []", "tags: list[str] | None = None").replace(
            "    tags.append(tag)", "    if tags is None:\n        tags = []\n    tags.append(tag)", 1)
        source.write_text(code, encoding="utf-8")
        results = eval_pilot.grade_behavior(case, project, grading, execute)
        self.assertTrue(all(check["status"] == "passed" for check in results))

    def test_shell_reproducer_preserves_reported_failure(self) -> None:
        scenario = self.cases["shell-quality-trap-status"]
        result = subprocess.run(["sh", "cleanup.sh"], cwd=scenario.fixture, text=True, capture_output=True,
                                env={"PATH": "/usr/bin:/bin"}, timeout=5, check=False)
        self.assertEqual(0, result.returncode)
        self.assertEqual("cleanup complete\n", result.stdout)

    def test_successful_invocation_captures_redacted_output_and_qualitative_status(self) -> None:
        scenario = self.cases["code-review-selection-regression"]
        batch = self.root / "private" / "batch"
        folder = batch / "001-A"
        folder.mkdir(parents=True)
        private = batch / "manifest.json"
        private.touch()
        scratch = self.root / "scratch"
        scratch.mkdir()
        args = SimpleNamespace(model="synthetic", reasoning_effort="medium", timeout=20)
        event_lines = strings(
            {"type": "thread.started", "thread_id": "isolated"},
            {"type": "item.completed", "item": {"type": "agent_message", "id": "a",
                                               "text": "Evidence in a synthetic response"}},
            {"type": "turn.completed", "usage": {"input_tokens": 12, "output_tokens": 4}},
        )

        def fake_process(command, *, cwd, env, timeout, stdout, stderr, prompt):
            self.assertIn("--ignore-user-config", command)
            self.assertIn("--strict-config", command)
            self.assertEqual("synthetic-token", env["CODEX_API_KEY"])
            self.assertEqual(scenario.prompt, prompt)
            self.assertFalse((cwd / ".agents").exists())
            self.assertNotIn("synthetic-token", " ".join(command))
            self.assertIn('forced_login_method="api"', command)
            self.assertEqual(subprocess.PIPE, stdout)
            self.assertEqual(subprocess.PIPE, stderr)
            self.assertFalse((folder / "stderr.log").exists())
            return {"exit_status": 0, "timed_out": False, "interrupted": False, "wall_seconds": 1,
                    "stdout": "\n".join(event_lines).encode(), "stderr": b"synthetic-token"}

        with (patch.object(harness, "verify_local_discovery"),
              patch.object(harness, "sandbox_probe"),
              patch.object(harness, "run_process", side_effect=fake_process)):
            result = harness.run_one("/fake-codex", scenario, {"configuration": "A"}, args, folder,
                                     scratch, eval_auth.Authentication("api-key", key="synthetic-token"), private)
        self.assertEqual(b"[REDACTED]", (folder / "stderr.log").read_bytes())
        self.assertEqual("Evidence in a synthetic response", (folder / "response.txt").read_text())
        self.assertEqual("manual_review_required", result["status"])
        self.assertEqual(16, result["observations"]["usage"]["total_tokens"])
        self.assertEqual({}, result["workspace_changes"])

    def test_stop_on_execution_error_and_report_unstarted_pair(self) -> None:
        output = self.root / "results"
        stdout = io.StringIO()

        def fake_run(_binary, _scenario, record, *_args):
            record.update(execution="execution_error", status="execution_error", reason="synthetic auth error")
            return record

        with (patch.dict(os.environ, {"CODEX_API_KEY": "synthetic-key"}),
              patch.object(harness.shutil, "which", return_value="/isolated/fake-codex"),
              patch.object(harness.subprocess, "check_output",
                           side_effect=[harness.SUPPORTED_VERSION, "test-revision", b""]),
              patch.object(harness, "run_one", side_effect=fake_run) as run,
              redirect_stdout(stdout)):
            status = harness.main(["run", "--live", "--output", str(output), "--scenario", "java-feature",
                                   "--model", "test", "--reasoning-effort", "low", "--max-runs", "2",
                                   "--auth", "api-key"])
        self.assertEqual(1, status)
        self.assertEqual(1, run.call_count)
        self.assertIn("unstarted", stdout.getvalue())
        self.assertIn("execution_error", stdout.getvalue())
        self.assertEqual(1, len(list(output.rglob("result.json"))))
        self.assertNotIn("synthetic-key", (next(output.glob("*/manifest.json"))).read_text())

    def test_manual_grade_cannot_override_deterministic_failure(self) -> None:
        (self.root / "manual.json").write_text('{"status":"passed","notes":"checked rubric"}', encoding="utf-8")
        self.assertEqual("failed", harness.result_status({"status": "failed"}, self.root))
        self.assertEqual("passed", harness.result_status({"status": "manual_review_required"}, self.root))
        self.assertEqual("timeout", harness.outcome([{"status": "passed"}], "timeout"))

    def test_live_auth_must_be_explicit_and_api_mode_has_no_global_fallback(self) -> None:
        args = ["run", "--live", "--scenario", "java-feature", "--model", "test",
                "--reasoning-effort", "medium", "--max-runs", "2"]
        errors = io.StringIO()
        with (patch.dict(os.environ, {"OPENAI_API_KEY": "unrelated"}, clear=True),
              patch.object(harness.shutil, "which", side_effect=AssertionError("no CLI allowed")),
              redirect_stdout(io.StringIO()), redirect_stderr(errors)):
            self.assertEqual(2, harness.main(args))
            self.assertEqual(2, harness.main([*args, "--auth", "api-key"]))
        self.assertIn("explicit --auth", errors.getvalue())
        self.assertIn("requires CODEX_API_KEY", errors.getvalue())
        self.assertNotIn("unrelated", errors.getvalue())

    def test_chatgpt_login_uses_native_device_auth_and_separate_home(self) -> None:
        auth = eval_auth.Authentication("chatgpt")
        global_config = self.root / "global-config.toml"
        global_config.write_text("unchanged")
        with patch.dict(os.environ, {"CODEX_HOME": str(self.root), "CODEX_API_KEY": "unrelated"}):
            isolated = harness.process_environment(self.root / "isolated")

        def login(command, *, cwd, env, **kwargs):
            self.assertIn("--device-auth", command)
            self.assertIn('forced_login_method="chatgpt"', command)
            self.assertIn('cli_auth_credentials_store="file"', command)
            self.assertNotIn("CODEX_API_KEY", env)
            self.assertEqual(isolated["HOME"], cwd)
            fake_oauth(Path(env["CODEX_HOME"]) / "auth.json")
            return subprocess.CompletedProcess(command, 0)

        with (patch.object(eval_auth.sys.stdin, "isatty", return_value=True),
              patch.object(eval_auth.sys.stderr, "isatty", return_value=True),
              patch.object(eval_auth.subprocess, "run", side_effect=login),
              redirect_stdout(io.StringIO())):
            auth.login("/fake-codex", isolated)
        self.assertEqual(Path(isolated["CODEX_HOME"]) / "auth.json", auth.cache)
        self.assertEqual("unchanged", global_config.read_text())
        self.assertFalse((self.root / "auth.json").exists())

    def test_chatgpt_cache_is_relayed_with_refresh_but_no_other_state(self) -> None:
        login = harness.process_environment(self.root / "login")
        login_home = Path(login["CODEX_HOME"])
        cache = login_home / "auth.json"
        fake_oauth(cache)
        (login_home / "config.toml").write_text("unrelated configuration")
        auth = eval_auth.Authentication("chatgpt", cache=cache)
        for arm, expected_access in (("A", b"old-access-token"), ("B", b"refreshed-access-token")):
            env = harness.process_environment(self.root / arm)
            with auth.for_run(env) as (child, secrets, local):
                self.assertNotIn("CODEX_API_KEY", child)
                self.assertEqual({"auth.json"}, {path.name for path in local.parent.iterdir()})
                self.assertFalse(cache.exists())
                self.assertIn(expected_access, secrets)
                fake_oauth(local, access="refreshed-access-token")
                secrets.update(eval_auth.chatgpt_secrets(local))
                self.assertEqual(b"[REDACTED] [REDACTED]", eval_auth.redact(
                    b"old-access-token refreshed-access-token" if arm == "A" else
                    b"refreshed-access-token refreshed-access-token", secrets))
            self.assertFalse(local.exists())
            self.assertTrue(cache.exists())
        self.assertEqual("unrelated configuration", (login_home / "config.toml").read_text())

    def test_chatgpt_rejects_other_modes_and_nonprivate_caches(self) -> None:
        cache = self.root / "auth.json"
        fake_oauth(cache, mode="apikey")
        with self.assertRaisesRegex(eval_auth.AuthenticationError, "native ChatGPT"):
            eval_auth.chatgpt_secrets(cache)
        fake_oauth(cache)
        cache.chmod(0o644)
        with self.assertRaisesRegex(eval_auth.AuthenticationError, "private Codex OAuth cache"):
            eval_auth.chatgpt_secrets(cache)

    def test_chatgpt_run_redacts_both_token_versions_before_writing_outputs(self) -> None:
        scenario = self.cases["code-review-selection-regression"]
        login = harness.process_environment(self.root / "login")
        cache = Path(login["CODEX_HOME"]) / "auth.json"
        fake_oauth(cache)
        batch = self.root / "outputs" / "batch"
        folder = batch / "run"
        folder.mkdir(parents=True)
        scratch = self.root / "scratch"
        scratch.mkdir()
        args = SimpleNamespace(model="synthetic", reasoning_effort="medium", timeout=20)

        def fake_process(command, *, env, **kwargs):
            self.assertIn('forced_login_method="chatgpt"', command)
            self.assertNotIn("CODEX_API_KEY", env)
            self.assertNotIn("OPENAI_API_KEY", env)
            self.assertIn(str(cache.parent), " ".join(command))
            self.assertFalse((folder / "events.jsonl").exists())
            self.assertFalse(cache.exists())
            fake_oauth(Path(env["CODEX_HOME"]) / "auth.json", access="refreshed-access-token")
            return {"exit_status": 0, "timed_out": False, "interrupted": False, "wall_seconds": 1,
                    "stdout": "\n".join(strings(
                        {"type": "thread.started", "thread_id": "synthetic"},
                        {"type": "item.completed", "item": {"id": "a", "type": "agent_message",
                                                           "text": "old-access-token refreshed-access-token"}},
                        {"type": "turn.completed"},
                    )).encode(), "stderr": b"test-refresh-token"}

        auth = eval_auth.Authentication("chatgpt", cache=cache)
        with (patch.dict(os.environ, {"CODEX_API_KEY": "unused", "OPENAI_API_KEY": "unused"}),
              patch.object(harness, "verify_local_discovery"),
              patch.object(harness, "sandbox_probe"),
              patch.object(harness, "run_process", side_effect=fake_process)):
            result = harness.run_one("/fake-codex", scenario, {"configuration": "A"}, args, folder,
                                     scratch, auth, batch / "manifest.json")
        self.assertEqual("completed", result["execution"])
        self.assertEqual("[REDACTED] [REDACTED]", (folder / "response.txt").read_text())
        self.assertEqual(b"[REDACTED]", (folder / "stderr.log").read_bytes())
        self.assertIn(b"refreshed-access-token", eval_auth.chatgpt_secrets(cache))


class ReportTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def batch(self, name: str, day: int, *, execution: str | None = "completed") -> Path:
        batch = self.root / name
        result = batch / "001-A-fixture"
        result.mkdir(parents=True)
        entry = {"directory": result.name, "configuration": "A", "repetition": 1, "scenario": "fixture"}
        harness.write_json(batch / "manifest.json", {
            "schema_version": 1, "started_utc": f"2026-11-{day:02}T12:00:00+00:00",
            "planned_runs": 1, "schedule": [entry],
        })
        if execution is not None:
            harness.write_json(result / "result.json", {
                **entry, "execution": execution, "status": "failed" if execution == "completed" else execution,
            })
        return batch

    def test_default_report_selects_newest_complete_batch_and_keeps_failed_grades(self) -> None:
        self.batch("pilot-older", 1)
        newest = self.batch("pilot-complete", 2)
        self.batch("pilot-timeout", 3, execution="timeout")
        self.batch("pilot-incomplete", 4, execution=None)
        malformed = self.batch("pilot-invalid", 5)
        (malformed / "manifest.json").write_text("{")
        forged = self.batch("pilot-traversal", 6)
        manifest = json.loads((forged / "manifest.json").read_text())
        manifest["schedule"][0]["directory"] = "../pilot-complete/001-A-fixture"
        harness.write_json(forged / "manifest.json", manifest)
        linked = self.batch("external-batch", 7)
        (self.root / "pilot-link").symlink_to(linked, target_is_directory=True)
        output = io.StringIO()
        with patch.object(harness, "LOCAL_RESULTS", self.root), redirect_stdout(output):
            self.assertEqual(0, harness.main(["report"]))
        self.assertIn(str(newest), output.getvalue())
        self.assertIn("failed", output.getvalue())
        self.assertNotIn("pilot-link", output.getvalue())

    def test_explicit_report_keeps_partial_batch_available(self) -> None:
        partial = self.batch("external-partial", 3, execution=None)
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(0, harness.main(["report", "--output", str(partial)]))
        self.assertIn("unstarted", output.getvalue())

    def test_no_results_explains_next_commands_and_creates_nothing(self) -> None:
        absent = self.root / "absent"
        errors = io.StringIO()
        with patch.object(harness, "LOCAL_RESULTS", absent), redirect_stderr(errors):
            self.assertEqual(2, harness.main(["report"]))
        self.assertIn("No completed batch", errors.getvalue())
        self.assertIn("task eval:plan", errors.getvalue())
        self.assertIn("--output <batch-directory>", errors.getvalue())
        self.assertFalse(absent.exists())


if __name__ == "__main__":
    unittest.main()
