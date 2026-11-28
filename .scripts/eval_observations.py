"""Extract conservative observations from the Codex exec JSONL stream."""

from __future__ import annotations

import json
from pathlib import Path
import re
import shlex
from typing import Iterable

TOOLS = {"command_execution", "file_change", "mcp_tool_call", "collab_tool_call", "web_search"}
USAGE = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens")


def literal_read_paths(command: str) -> list[str]:
    """Recognize simple reads only; compound commands and ambiguous paths are unobserved."""
    try:
        words = shlex.split(command)
        if (len(words) == 3 and Path(words[0]).name in {"sh", "bash", "zsh"}
                and words[1] in {"-c", "-lc"}):
            words = shlex.split(words[2])
    except ValueError:
        return []
    if not words:
        return []
    tool, *paths = words
    if Path(tool).name == "sed" and len(paths) == 3 and paths[0] == "-n":
        paths = paths[2:] if re.fullmatch(r"\d+(,\d+)?p", paths[1]) else []
    elif Path(tool).name in {"cat", "head"}:
        if paths and paths[0] == "--":
            paths = paths[1:]
        elif Path(tool).name == "head" and len(paths) >= 2 and paths[0] == "-n" and paths[1].isdigit():
            paths = paths[2:]
    else:
        return []
    if any(path.startswith("-") or re.search(r"[;&|<>`$*?!{}\[\]~\n]", path) for path in paths):
        return []
    return paths


def workspace_path(raw: str, workspace: Path) -> str | None:
    try:
        path = (workspace / raw).resolve().relative_to(workspace)
    except (ValueError, OSError, RuntimeError):
        return None
    return path.as_posix()


def parse_events(lines: Iterable[str], workspace: Path, skill_files: set[str]) -> dict:
    items: dict[str, dict] = {}
    completed = set()
    errors = []
    invalid = 0
    usage = {}
    turns = 0
    final = None
    thread = None
    count = 0
    for line in lines:
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError:
            invalid += 1
            continue
        if not isinstance(event, dict) or not isinstance(event.get("type"), str):
            invalid += 1
            continue
        count += 1
        kind = event["type"]
        if kind == "thread.started":
            thread = event.get("thread_id")
        elif kind == "turn.completed":
            turns += 1
            usage = event.get("usage")
        elif kind in {"turn.failed", "error"}:
            error = event.get("error", event)
            message = error.get("message") if isinstance(error, dict) else None
            errors.append(message if isinstance(message, str) else kind)
        elif kind in {"item.started", "item.updated", "item.completed"}:
            item = event.get("item")
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                invalid += 1
                continue
            identifier = item["id"]
            if item.get("type") == "agent_message" and kind == "item.completed":
                if isinstance(item.get("text"), str):
                    final = item["text"]
            if item.get("type") == "error" and kind == "item.completed":
                message = item.get("message")
                errors.append(message if isinstance(message, str) else "error item")
            if isinstance(item.get("type"), str) and item["type"] in TOOLS:
                items[identifier] = item
                if kind == "item.completed":
                    completed.add(identifier)

    # The pinned CLI reports cumulative turn totals, including cache/reasoning subsets.
    numbers = {key: usage.get(key) if isinstance(usage, dict) else None for key in USAGE}
    numbers = {key: value if type(value) is int and value >= 0 else None
               for key, value in numbers.items()}
    if not any(numbers.values()):  # The CLI emits an all-zero default when usage was absent.
        numbers = dict.fromkeys(USAGE)
    for subset, total in (("cached_input_tokens", "input_tokens"), ("reasoning_output_tokens", "output_tokens")):
        if numbers[subset] is not None and numbers[total] is not None and numbers[subset] > numbers[total]:
            numbers[subset] = None
    primary = [numbers["input_tokens"], numbers["output_tokens"]]
    numbers["total_tokens"] = sum(primary) if None not in primary else None

    commands, patches, attempts, delegation, reads, inferred = [], [], [], [], set(), set()
    for identifier, item in items.items():
        if item["type"] == "command_execution" and isinstance(item.get("command"), str):
            commands.append({key: item.get(key) for key in ("command", "exit_code", "status")})
            if (identifier in completed and item.get("exit_code") == 0
                    and item.get("status") == "completed"):
                for raw in literal_read_paths(item["command"]):
                    path = workspace_path(raw, workspace)
                    if path in skill_files:
                        (reads if Path(raw).is_absolute() else inferred).add(path)
        elif item["type"] == "file_change" and item.get("status") in ("completed", "failed"):
            changes = item.get("changes")
            if isinstance(changes, list):
                paths = patches if item["status"] == "completed" else attempts
                paths.extend(change["path"] for change in changes
                             if isinstance(change, dict) and isinstance(change.get("path"), str))
        elif item["type"] == "collab_tool_call":
            delegation.append({key: item.get(key) for key in ("tool", "status", "receiver_thread_ids")})

    return {
        "thread_id": thread, "completed_turns": turns, "errors": errors,
        "malformed_lines": invalid, "events": count, "final_response": final,
        "usage": numbers, "observed_tool_calls": len(items) if count else None,
        "commands": commands, "patch_paths": patches, "failed_patch_paths": attempts, "delegation": delegation,
        "tool_kinds": sorted({item["type"] for item in items.values()}),
        "observed_skill_manifests": sorted(path for path in reads if path.endswith("/SKILL.md") and "/references/" not in path),
        "observed_references": sorted(path for path in reads if "/references/" in path),
        "possible_relative_skill_reads": sorted(inferred - reads),
        "direct_skill_activation": None, "direct_workflow_mode": None,
    }
