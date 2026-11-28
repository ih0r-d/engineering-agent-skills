"""Plan, run, and report the native Codex behavioral pilot."""

from __future__ import annotations

import argparse
from contextlib import suppress
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time

import eval_auth
import eval_observations as events
import eval_pilot
import evaluation_cases
import skills

ROOT = evaluation_cases.ROOT
LOCAL_RESULTS = ROOT / ".eval-results"
SUPPORTED_VERSION = "codex-cli 0.172.0"
PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
PROFILE = "behavioral-eval"
DEFAULT_LIMIT = 12
INSTRUCTIONS = (
    "# Project instructions\n\n"
    "Work within the requested scope. Use local tools and verification. "
    "Keep external services and registries outside the task.\n"
)
ISOLATION_NOTE = (
    "Local discovery inputs and native sandbox probes checked. "
    "Effective in-session discovery and reference use are only partially observable."
)


class EvalError(Exception):
    """An evaluation could not safely proceed."""


def positive(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return number


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_process(command: list[str], *, cwd: Path, env: dict, timeout: int,
                stdout, stderr, prompt: str | None = None) -> dict:
    started = time.monotonic()
    output = error_output = None
    with subprocess.Popen(command, cwd=cwd, env=env, start_new_session=True,
                          stdin=subprocess.PIPE if prompt is not None else subprocess.DEVNULL,
                          stdout=stdout, stderr=stderr) as process:
        timed_out = False
        interrupted = False
        try:
            output, error_output = process.communicate(
                prompt.encode("utf-8") if prompt is not None else None, timeout=timeout)
        except subprocess.TimeoutExpired as error:
            timed_out = True
            output, error_output = error.output, error.stderr
        except KeyboardInterrupt:
            interrupted = True
        finally:
            # Reap the primary process and stop children left in its process group.
            with suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        if (timed_out or interrupted) and (stdout == subprocess.PIPE or stderr == subprocess.PIPE):
            with suppress(subprocess.TimeoutExpired):
                output, error_output = process.communicate(timeout=2)
    result = {"exit_status": process.returncode, "timed_out": timed_out, "interrupted": interrupted,
              "wall_seconds": round(time.monotonic() - started, 4)}
    if stdout == subprocess.PIPE:
        result["stdout"] = output or b""
    if stderr == subprocess.PIPE:
        result["stderr"] = error_output or b""
    return result


def snapshot(root: Path) -> dict[str, dict]:
    """Describe files without following a path created by the agent."""
    entries = {}
    for index, path in enumerate(root.rglob("*")):
        if index >= 4096:
            raise EvalError("Workspace has too many entries to snapshot safely.")
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            value = {"kind": "symlink", "target": os.readlink(path)}
        elif stat.S_ISREG(info.st_mode):
            if info.st_size > 8 * 1024 * 1024:
                raise EvalError("Workspace contains a file too large to snapshot safely.")
            with path.open("rb") as data:
                digest = hashlib.sha256()
                for block in iter(lambda: data.read(65536), b""):
                    digest.update(block)
            value = {"kind": "file", "size": info.st_size, "sha256": digest.hexdigest(),
                     "mode": stat.S_IMODE(info.st_mode)}
        elif stat.S_ISDIR(info.st_mode):
            value = {"kind": "directory", "mode": stat.S_IMODE(info.st_mode)}
        else:
            value = {"kind": "special"}
        entries[path.relative_to(root).as_posix()] = value
    return entries


def manifest_digest(tree: dict) -> str:
    return hashlib.sha256(json.dumps(tree, sort_keys=True).encode("utf-8")).hexdigest()


def prepare_workspace(workspace: Path, scenario: eval_pilot.Scenario, config: str) -> tuple[dict, str]:
    fixture_tree = snapshot(scenario.fixture)
    reserved = {".agents", ".codex", ".git", "AGENTS.md", "AGENTS.override.md"}
    if any(reserved.intersection(Path(path).parts) or entry["kind"] not in {"file", "directory"}
           for path, entry in fixture_tree.items()):
        raise EvalError("Fixture contains local agent configuration or non-regular resources.")
    shutil.copytree(scenario.fixture, workspace)
    (workspace / "AGENTS.md").write_text(INSTRUCTIONS, encoding="utf-8")
    base = manifest_digest(snapshot(workspace))
    if config == "B":
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / ".scripts/skills.py"), "install",
             "--agent", "codex", "--target", str(workspace), "--all", "--mode", "copy"],
            capture_output=True, text=True, check=False, timeout=30,
        )
        if result.returncode:
            raise EvalError(f"Disposable skill installation failed: {result.stderr.strip()}")
        installed = workspace / ".agents/skills"
        catalog_names = evaluation_cases.catalog_skills()
        if {path.name for path in installed.iterdir()} != catalog_names:
            raise EvalError("Installed skills do not exactly match the catalog.")
        for name in catalog_names:
            tree = snapshot(installed / name)
            tree.pop(skills.MARKER, None)
            if tree != snapshot(skills.skill_path(name)):
                raise EvalError(f"Installed skill differs from source: {name}")
    before = snapshot(workspace)
    common = {path: entry for path, entry in before.items()
              if path != ".agents" and not path.startswith(".agents/")}
    if manifest_digest(common) != base:
        raise EvalError("Skill installation changed common project inputs.")
    return before, base


def jdk_home() -> Path | None:
    value = os.environ.get("JAVA_HOME")
    if not value:
        return None
    candidate = Path(value).expanduser().resolve()
    if not (candidate / "release").is_file() or not all(
        (candidate / "bin" / tool).is_file() for tool in ("java", "javac")
    ):
        return None
    return candidate


def tool_path(jdk: Path | None) -> str:
    return os.pathsep.join((str(jdk / "bin"), PATH)) if jdk is not None else PATH


def process_environment(home: Path, jdk: Path | None = None) -> dict[str, str]:
    home.mkdir(mode=0o700)
    codex = home / ".codex"
    codex.mkdir()
    scratch = home / "tmp"
    scratch.mkdir()
    return {
        "HOME": str(home), "CODEX_HOME": str(codex), "TMPDIR": str(scratch),
        "XDG_CONFIG_HOME": str(home / ".config"), "XDG_DATA_HOME": str(home / ".local/share"),
        "XDG_CACHE_HOME": str(home / ".cache"), "PATH": tool_path(jdk), "LC_ALL": "C", "SHELL": "/bin/sh",
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
    }


def config_arguments(workspace: Path, *, writable: bool, private: Path | None = None,
                     jdk: Path | None = None, temp: Path | None = None,
                     auth_directory: Path | None = None) -> list[str]:
    def quoted(value: str) -> str:
        return json.dumps(value, ensure_ascii=False)

    paths = {":minimal": "read", str(Path.home().resolve()): "deny", str(ROOT): "deny", str(workspace.parent): "deny",
             str(workspace): "write" if writable else "read"}
    if sys.platform.startswith("linux"):
        paths["/proc"] = "deny"
    if os.environ.get("CODEX_HOME"):
        paths[str(Path(os.environ["CODEX_HOME"]).expanduser().resolve())] = "deny"
    if private is not None:
        paths[str(private)] = "deny"
    if auth_directory is not None:
        paths[str(auth_directory)] = "deny"
    # macOS developer tools and Homebrew may resolve outside the minimal runtime paths.
    if sys.platform == "darwin":
        for path in ("/Library/Java/JavaVirtualMachines", "/Library/Developer/CommandLineTools",
                     "/Library/Frameworks/Python.framework", "/opt/homebrew", "/usr/local"):
            paths[path] = "read"
    if jdk is not None:
        paths[str(jdk)] = "read"
    if temp is not None:
        paths[str(temp)] = "write"
    for name in ("AGENTS.md", ".agents"):
        paths[str(workspace / name)] = "read"
    fs = ", ".join(f"{quoted(path)} = {quoted(access)}" for path, access in paths.items())
    shell = {"PATH": tool_path(jdk), "LC_ALL": "C", "HOME": str(workspace.parent / "home"),
             "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}
    if temp is not None:
        shell["TMPDIR"] = str(temp)
    variables = ", ".join(f"{name} = {quoted(value)}" for name, value in shell.items())
    settings = [
        f'default_permissions="{PROFILE}"', f"permissions.{PROFILE}.filesystem={{ {fs} }}",
        f"permissions.{PROFILE}.network.enabled=false", 'approval_policy="never"',
        'web_search="disabled"', "allow_login_shell=false", "skills.bundled.enabled=false",
        "memories.generate_memories=false", "memories.use_memories=false",
        'shell_environment_policy.inherit="none"',
        f"shell_environment_policy.set={{ {variables} }}",
        "analytics.enabled=false",
    ]
    for feature in ("hooks", "plugins", "remote_plugin", "skill_mcp_dependency_install",
                    "multi_agent", "multi_agent_v2", "shell_snapshot"):
        settings.append(f"features.{feature}=false")
    return [part for setting in settings for part in ("-c", setting)]


def verify_local_discovery(workspace: Path) -> None:
    # A standalone project and clean ancestors avoid repository and parent discovery.
    for parent in workspace.parents:
        for marker in ("AGENTS.md", "AGENTS.override.md", ".agents", ".codex", ".git"):
            if os.path.lexists(parent / marker):
                raise EvalError(f"Ancestor has discoverable configuration: {parent / marker}")
    admin = Path("/etc/codex")
    if os.path.lexists(admin) and (not admin.is_dir() or any(admin.iterdir())):
        raise EvalError("System Codex configuration is present. Use an isolated machine or account environment.")
    if sys.platform == "darwin" and Path("/Library/Managed Preferences/com.openai.codex.plist").exists():
        raise EvalError("Managed Codex configuration is present. Use an isolated machine or account environment.")


def sandbox_command(binary: str, workspace: Path, options: list[str], command: list[str]) -> list[str]:
    return [binary, "sandbox", "--include-managed-config", "-P", PROFILE,
            "-C", str(workspace), *options, "--", *command]


def sandbox_probe(binary: str, workspace: Path, options: list[str], env: dict,
                  private_file: Path, scenario: eval_pilot.Scenario, log: Path) -> None:
    writable = scenario.editable is not None
    script = """
set -eu
cat AGENTS.md >/dev/null
for private in "$1" "$2" "$3"; do
    if cat "$private" >/dev/null 2>&1; then
        printf '%s\n' "Sandbox can read a private input" >&2
        exit 1
    fi
done
test -z "${CODEX_API_KEY-}${OPENAI_API_KEY-}${CODEX_ACCESS_TOKEN-}"
if [ "$4" = write ]; then
    : > .eval-write-probe
    rm .eval-write-probe
else
    if ( : > .eval-write-probe ) 2>/dev/null; then
        rm .eval-write-probe
        exit 1
    fi
fi
shift 4
for tool do
    if ! command -v "$tool" >/dev/null; then
        printf '%s\n' "Required tool unavailable: $tool" >&2
        exit 1
    fi
    case "$tool" in
        java) java -version ;;
        javac) javac -version ;;
        python3) python3 --version ;;
        make) make --version ;;
    esac
done
"""
    sentinel = Path(env["CODEX_HOME"]) / "sandbox-sentinel"
    sentinel.write_text("private\n", encoding="utf-8")
    try:
        command = ["/bin/sh", "-c", script, "eval-probe", str(ROOT / "catalog.json"), str(private_file),
                   str(sentinel), "write" if writable else "read", *scenario.tools]
        with log.open("wb") as output:
            result = run_process(sandbox_command(binary, workspace, options, command),
                                 cwd=workspace, env=env, timeout=15, stdout=output, stderr=output)
    finally:
        sentinel.unlink()
    if result["exit_status"] != 0:
        raise EvalError("Native isolation or tool preflight failed. See sandbox-probe.log.")


def violations(scenario: eval_pilot.Scenario, workspace: Path, changes: dict, observations: dict) -> list[str]:
    paths = set(changes)
    for value in observations["patch_paths"]:
        paths.add(events.workspace_path(value, workspace) or "[path outside workspace]")
    return sorted(path for path in paths if path != scenario.editable)


def preserve_changes(workspace: Path, after: dict, changes: dict, path: Path, secrets: set[bytes]) -> None:
    budget = 1024 * 1024
    for name in changes:
        entry = after.get(name, {})
        if entry.get("kind") != "file" or entry["size"] > min(budget, 256 * 1024):
            continue
        source = workspace / name
        target = path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(eval_auth.redact(source.read_bytes(), secrets))
        budget -= entry["size"]


def grade_command(binary, workspace, options, env, directory, name, command, expected_output=None) -> dict:
    key = name.lower().replace(" ", "-")
    stdout = directory / f"{key}.stdout"
    stderr = directory / f"{key}.stderr"
    with stdout.open("wb") as out, stderr.open("wb") as err:
        result = run_process(sandbox_command(binary, workspace, options, command),
                             cwd=workspace, env={**env, "TMPDIR": str(workspace / "tmp")},
                             timeout=15, stdout=out, stderr=err)
    passed = result["exit_status"] == 0
    if expected_output is not None:
        passed = passed and stdout.read_text(encoding="utf-8", errors="replace").strip() == expected_output
    state = "timeout" if result["timed_out"] else ("passed" if passed else "failed")
    return {"name": name, "status": state, **result, "stdout": stdout.name, "stderr": stderr.name}


def outcome(checks: list[dict], execution: str) -> str:
    if execution != "completed":
        return execution
    states = {check["status"] for check in checks}
    for state in ("failed", "execution_error", "timeout", "unavailable", "manual_review_required"):
        if state in states:
            return state
    return "passed"


def execution_failure(observations: dict, stderr: str) -> str:
    diagnostic = ("\n".join(observations["errors"]) + "\n" + stderr).lower()
    if any(value in diagnostic for value in ("insufficient_quota", "usage limit", "rate limit", "429 too many")):
        return "usage_limit"
    if any(value in diagnostic for value in ("invalid_api_key", "401 unauthorized", "authentication failed")):
        return "authentication"
    return "codex_execution"


def run_one(binary: str, scenario: eval_pilot.Scenario, record: dict, args, folder: Path,
            scratch: Path, auth: eval_auth.Authentication, private_file: Path,
            expected_digest: str | None = None) -> dict:
    workspace = scratch / "workspace"
    jdk = jdk_home() if "java" in scenario.tools else None
    env = process_environment(scratch / "home", jdk)
    before, common_digest = prepare_workspace(workspace, scenario, record["configuration"])
    if expected_digest is not None and expected_digest != common_digest:
        raise EvalError("Common workspace inputs changed between runs of this scenario.")
    verify_local_discovery(workspace)
    temp = scratch / "command-tmp" if scenario.editable else None
    if temp is not None:
        temp.mkdir()
    auth_directory = auth.cache.parent if auth.cache is not None else None
    options = config_arguments(workspace, writable=scenario.editable is not None,
                               private=private_file.parent.parent, jdk=jdk, temp=temp,
                               auth_directory=auth_directory)
    sandbox_probe(binary, workspace, options, env, private_file, scenario, folder / "sandbox-probe.log")
    if snapshot(workspace) != before:
        raise EvalError("Isolation probe changed fixture inputs.")
    record["initial_workspace_sha256"] = common_digest
    record["isolation"] = ISOLATION_NOTE
    record["prompt_sha256"] = hashlib.sha256(scenario.prompt.encode("utf-8")).hexdigest()
    record["installed_manifest_count"] = sum(path.startswith(".agents/skills/") and path.endswith("/SKILL.md")
                                             for path in before)
    command = [
        binary, "exec", "--json", "--color", "never", "--ephemeral", "--ignore-user-config",
        "--ignore-rules", "--strict-config", "--skip-git-repo-check", "-C", str(workspace),
        "-m", args.model, "-c", "model_reasoning_effort=" + json.dumps(args.reasoning_effort),
        *options, *auth.options, "-",
    ]
    trace, stderr = folder / "events.jsonl", folder / "stderr.log"
    with auth.for_run(env) as (cli_env, secrets, cache):
        process = run_process(command, cwd=workspace, env=cli_env, timeout=args.timeout,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, prompt=scenario.prompt)
        if cache is not None:
            secrets.update(eval_auth.chatgpt_secrets(cache))
        trace.write_bytes(eval_auth.redact(process.pop("stdout"), secrets))
        stderr.write_bytes(eval_auth.redact(process.pop("stderr"), secrets))
    with trace.open(encoding="utf-8", errors="replace") as lines:
        observations = events.parse_events(lines, workspace, {path for path in before if path.startswith(".agents/skills/")})
    record.update(process, observations=observations)
    response = observations.pop("final_response")
    if response is not None:
        (folder / "response.txt").write_text(response, encoding="utf-8")

    after = snapshot(workspace)
    changes = {name: {"before": before.get(name), "after": after.get(name)}
               for name in sorted(before.keys() | after.keys()) if before.get(name) != after.get(name)}
    metadata = json.dumps(changes).encode("utf-8")
    if eval_auth.redact(metadata, secrets) != metadata:
        raise eval_auth.AuthenticationError("A workspace path contains credential material. Changes were withheld.")
    record["workspace_changes"] = changes
    preserve_changes(workspace, after, changes, folder / "changed-files", secrets)
    unauthorized = violations(scenario, workspace, changes, observations)
    failed_patches = {events.workspace_path(path, workspace) or "[path outside workspace]"
                      for path in observations["failed_patch_paths"]}
    unauthorized_attempts = sorted(path for path in failed_patches if path != scenario.editable)
    integrations = sorted(set(observations["tool_kinds"]) & {"web_search", "mcp_tool_call", "collab_tool_call"})
    record["authorization_violations"] = unauthorized + integrations
    record["unauthorized_patch_attempts"] = unauthorized_attempts
    outside_scope = bool(unauthorized or unauthorized_attempts or integrations)
    checks = [{"name": "workspace and tool authorization", "status": "failed" if outside_scope else "passed"}]
    execution = "completed"
    if process["timed_out"]:
        execution = "timeout"
        record["reason"] = "Codex invocation exceeded the wall-clock limit."
    elif (process["exit_status"] != 0 or observations["errors"]
          or observations["completed_turns"] != 1 or not isinstance(observations["thread_id"], str)):
        execution = "execution_error"
        record["reason"] = "Codex execution failed or had no completed turn. Inspect stderr and JSONL events."
        record["failure_kind"] = execution_failure(observations, stderr.read_text(encoding="utf-8", errors="replace"))
    elif not response:
        execution = "execution_error"
        record["reason"] = "Codex emitted no final response."

    prefix = f".agents/skills/{scenario.skill}/references/"
    expected_refs = {prefix + name for name in scenario.references}
    observed_refs = set(observations["observed_references"])
    record["reference_evidence"] = {
        "relevant_reads": sorted(observed_refs & expected_refs),
        "other_reads": sorted(observed_refs - expected_refs),
        "expected_paths": sorted(expected_refs),
        "status": "observed" if observed_refs else "unavailable",
    }
    if integrations:
        record["isolation"] = "Inconclusive: an unexpected integration tool was exposed or used."
        execution = "execution_error" if execution == "completed" else execution
        record.setdefault("reason", "Unexpected web, MCP, or delegation evidence invalidated isolation.")
    if execution == "completed" and not outside_scope:
        if scenario.editable:
            artifact = workspace / scenario.editable
            if not artifact.is_symlink() and artifact.is_file():
                content = artifact.read_bytes()
                if eval_auth.redact(content, secrets) != content:
                    raise eval_auth.AuthenticationError("Source contains credential material. Grading was stopped.")
            grading = scratch / "grade"
            grading.mkdir()
            grade_temp = grading / "tmp"
            grade_temp.mkdir()
            grade_options = config_arguments(grading, writable=True, private=private_file.parent.parent,
                                             jdk=jdk, temp=grade_temp, auth_directory=auth_directory)
            checks.extend(eval_pilot.grade_behavior(
                scenario, workspace, grading,
                lambda name, cmd, **kw: grade_command(binary, grading, grade_options, env, folder, name, cmd, **kw),
            ))
        checks.append({"name": "qualitative acceptance criteria", "status": "manual_review_required"})
    record.update(execution=execution, checks=checks, status=outcome(checks, execution))
    return record


def output_base(path: Path) -> Path:
    target = path.resolve()
    if target.is_relative_to(ROOT):
        if not target.is_relative_to(LOCAL_RESULTS):
            raise EvalError("Repository-local output must be under .eval-results/.")
        relative = target.relative_to(ROOT)
        ignored = subprocess.run(["git", "check-ignore", "--quiet", "--", str(relative / "batch/manifest.json")],
                                 cwd=ROOT, check=False)
        tracked = subprocess.check_output(["git", "ls-files", "--", str(relative)], cwd=ROOT)
        if ignored.returncode != 0 or tracked:
            raise EvalError("Results directory must be ignored and contain no tracked files.")
    else:
        parent = next((part for part in (target, *target.parents) if part.is_dir()), None)
        if parent is not None and subprocess.run(
            ["git", "-C", str(parent), "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
        ).returncode == 0:
            raise EvalError("External results must be outside other Git worktrees.")
    return target


def selected_runs(args):
    available = eval_pilot.scenarios()
    identifiers = args.scenario or list(available)
    if len(set(identifiers)) != len(identifiers) or set(identifiers) - available.keys():
        raise EvalError("Use unique scenario IDs from the pilot list.")
    count = len(identifiers) * len(args.configuration) * args.repetitions
    limit = args.max_runs if args.max_runs is not None else DEFAULT_LIMIT
    if count > limit:
        raise EvalError(f"Planned {count} runs exceed the explicit maximum of {limit}.")
    serial = 0
    for repetition in range(1, args.repetitions + 1):
        for identifier in identifiers:
            order = args.configuration if serial % 2 == 0 else args.configuration[::-1]
            serial += 1
            for config in order:
                yield available[identifier], config, repetition


def benchmark(args) -> int:
    plan = list(selected_runs(args))
    print(f"Planned model runs: {len(plan)} / {args.max_runs or DEFAULT_LIMIT}", flush=True)
    if args.auth is not None:
        print(f"Authentication: {args.auth}", flush=True)
    for scenario, config, index in plan:
        print(f"  {config}  repetition {index}  {scenario.id}", flush=True)
    if not args.live:
        return 0
    if args.max_runs is None:
        raise EvalError("Live mode requires an explicit --max-runs.")
    if not args.model or not args.reasoning_effort:
        raise EvalError("Live mode requires --model and --reasoning-effort.")
    if args.auth is None:
        raise EvalError("Live mode requires an explicit --auth chatgpt or --auth api-key.")
    key = os.environ.get("CODEX_API_KEY", "").strip() if args.auth == "api-key" else None
    if args.auth == "api-key" and not key:
        raise EvalError("API-key mode requires CODEX_API_KEY in the environment.")
    auth = eval_auth.Authentication(args.auth, key=key)
    binary = shutil.which("codex")
    if not binary:
        raise EvalError("Codex CLI was not found.")
    binary = str(Path(binary).resolve())
    base = output_base(args.output)
    base.mkdir(mode=0o700, parents=True, exist_ok=True)
    if not base.is_dir():
        raise EvalError("Expected a results directory.")
    batch = Path(tempfile.mkdtemp(prefix="pilot-", dir=base))
    print(f"Local results: {batch}", flush=True)
    with tempfile.TemporaryDirectory(prefix="eas-eval-", dir="/tmp") as temporary:
        partition = Path(temporary).resolve()
        probe_home = process_environment(partition / "cli-check")
        version = subprocess.check_output([binary, "--version"], cwd=partition, env=probe_home,
                                          text=True, timeout=10).strip()
        if version != SUPPORTED_VERSION:
            raise EvalError(f"The isolation and event interface is pinned to {SUPPORTED_VERSION}. Found {version}.")
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        dirty = bool(subprocess.check_output(["git", "status", "--porcelain=v1", "--untracked-files=normal"],
                                             cwd=ROOT))
        schedule = [{"directory": f"{index:03}-{config}-{scenario.id}", "scenario": scenario.id,
                     "configuration": config, "repetition": repeat}
                    for index, (scenario, config, repeat) in enumerate(plan, 1)]
        write_json(batch / "manifest.json", {
            "schema_version": 1, "started_utc": datetime.now(timezone.utc).isoformat(),
            "revision": revision, "dirty": dirty, "codex": version, "model": args.model,
            "reasoning_effort": args.reasoning_effort, "timeout_seconds": args.timeout,
            "max_runs": args.max_runs, "planned_runs": len(plan), "auth": auth.mode, "schedule": schedule,
        })
        if auth.mode == "chatgpt":
            login_home = partition / "login"
            verify_local_discovery(login_home)
            auth.login(binary, process_environment(login_home))
        private_file = batch / "manifest.json"
        input_digests: dict[str, str] = {}
        for entry, (scenario, config, repeat) in zip(schedule, plan):
            folder = batch / entry["directory"]
            folder.mkdir(mode=0o700)
            record = {"scenario": scenario.id, "configuration": config, "repetition": repeat,
                      "expected_skill": scenario.skill if config == "B" else None,
                      "avoid_skills": scenario.avoided_skills, "expected_mode": scenario.mode,
                      "expected_technology": scenario.technology, "acceptance_criteria": scenario.expected}
            try:
                with tempfile.TemporaryDirectory(prefix="run-", dir=partition) as temporary_run:
                    record = run_one(binary, scenario, record, args, folder, Path(temporary_run), auth,
                                     private_file, input_digests.get(scenario.id))
            except eval_auth.AuthenticationError as error:
                record.update(execution="execution_error", status="execution_error",
                              failure_kind="authentication", reason=str(error))
            except (EvalError, OSError, subprocess.SubprocessError) as error:
                record.update(execution="execution_error", status="execution_error", reason=str(error))
            write_json(folder / "result.json", record)
            # Stop conservatively on any model or infrastructure failure, including auth and quota errors.
            if record["execution"] != "completed" or record.get("interrupted"):
                break
            input_digests[scenario.id] = record["initial_workspace_sha256"]
    print_report(batch)
    return 1 if record["execution"] != "completed" or record.get("interrupted") else 0


def display(value) -> str:
    return "—" if value is None else str(value)


def result_status(result: dict, directory: Path) -> str:
    path = directory / "manual.json"
    if result["status"] != "manual_review_required" or not path.is_file():
        return result["status"]
    decision = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(decision, dict) or decision.get("status") not in {"passed", "failed", "unavailable"}
            or not isinstance(decision.get("notes"), str) or not decision["notes"].strip()):
        raise EvalError(f"Invalid manual review in {directory.name}.")
    return decision["status"]


def summarize(rows: list[dict]) -> str:
    from collections import Counter
    from statistics import median

    measures = ("total_tokens", "wall_seconds", "observed_tool_calls")
    lines = ["| Scenario | Rep | Config | Execution | Task grade | Auth | Assertions | Tokens | Seconds | Tool calls |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    groups = {"A": [], "B": []}
    pairs: dict[tuple[str, int], dict[str, dict]] = {}
    for row in rows:
        groups[row["configuration"]].append(row)
        if row["execution"] == "completed":
            pairs.setdefault((row["scenario"], row["repetition"]), {})[row["configuration"]] = row
        values = [row[key] for key in ("scenario", "repetition", "configuration", "execution", "status",
                                      "authorization", "assertions", *measures)]
        lines.append("| " + " | ".join(map(display, values)) + " |")
    lines.extend(["", "Configuration totals include failed and unstarted slots.",
                  "Medians use observed values from completed executions only (sample count in parentheses).", ""])
    for config, group in groups.items():
        if not group:
            continue
        states = Counter(row["status"] for row in group)
        auth = Counter(row["authorization"] for row in group)
        lines.append(f"**{config}** — {dict(sorted(states.items()))}, authorization {dict(auth)}")
        for measure in (*measures, *events.USAGE):
            values = [row[measure] for row in group if row["execution"] == "completed" and row.get(measure) is not None]
            lines.append(f"- {measure}: {display(median(values) if values else None)} ({len(values)})")
    completed = [pair for pair in pairs.values() if set(pair) == {"A", "B"}]
    if completed:
        lines.extend(["", "Median paired B − A differences (number of measured pairs):"])
        for measure in measures:
            changes = [pair["B"][measure] - pair["A"][measure] for pair in completed
                       if pair["A"][measure] is not None and pair["B"][measure] is not None]
            lines.append(f"- {measure}: {display(median(changes) if changes else None)} ({len(changes)})")
    lines.extend(["", "Missing values are unavailable. A single pair is a smoke test.",
                  "Task correctness and authorization take precedence over efficiency."])
    return "\n".join(lines)


def print_report(batch: Path) -> None:
    manifest = json.loads((batch / "manifest.json").read_text(encoding="utf-8"))
    rows = []
    for entry in manifest["schedule"]:
        directory = batch / entry["directory"]
        path = directory / "result.json"
        result = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
        trace = result.get("observations", {})
        checks = result.get("checks", [])
        deterministic = [check for check in checks if check["name"] not in
                         {"workspace and tool authorization", "qualitative acceptance criteria"}]
        auth = next((check["status"] for check in checks if check["name"] == "workspace and tool authorization"),
                    None)
        passed = sum(check["status"] == "passed" for check in deterministic)
        usage = trace.get("usage", {})
        rows.append({
            **entry, "execution": result.get("execution", "unstarted"),
            "status": result_status(result, directory) if result else "unstarted",
            "authorization": auth, "assertions": f"{passed}/{len(deterministic)}" if deterministic else None,
            **{name: usage.get(name) for name in ("total_tokens", *events.USAGE)},
            "wall_seconds": result.get("wall_seconds"), "observed_tool_calls": trace.get("observed_tool_calls"),
        })
    print(summarize(rows))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command")
    for action in ("plan", "run"):
        command = subcommands.add_parser(action, help="Show budget and scenarios" if action == "plan" else "Plan or explicitly start the pilot")
        command.add_argument("--scenario", action="append", help="Pilot case ID (repeat for a subset)")
        command.add_argument("--configuration", choices=("A", "B", "AB"), default="AB")
        command.add_argument("--auth", choices=("chatgpt", "api-key"), help="Required for live execution")
        command.add_argument("--model")
        command.add_argument("--reasoning-effort")
        command.add_argument("--repetitions", type=positive, default=1)
        command.add_argument("--max-runs", type=positive,
                             help="Maximum invocations (dry-run default: 12; required for live)")
        command.add_argument("--timeout", type=positive, default=180, help="Maximum seconds per Codex invocation")
        command.add_argument("--output", type=Path, default=LOCAL_RESULTS)
        if action == "run":
            command.add_argument("--live", action="store_true", help="Authorize Codex execution and its usage")
        else:
            command.set_defaults(live=False)
    report = subcommands.add_parser("report", help="Summarize an existing private batch")
    report.add_argument("--output", required=True, type=Path, help="An existing pilot batch directory")
    args = parser.parse_args(argv)
    if args.command is None:
        args = parser.parse_args(["plan"])
    try:
        if args.command == "report":
            print_report(args.output.resolve())
            return 0
        return benchmark(args)
    except (EvalError, eval_auth.AuthenticationError, OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"Evaluation stopped: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Evaluation interrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
