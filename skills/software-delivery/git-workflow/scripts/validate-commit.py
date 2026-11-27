#!/usr/bin/env python3
"""Validate a Conventional Commit header without changing repository state."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

HEADER = re.compile(r"^(?P<type>[^\s():!]+)(?:\((?P<scope>[^()\r\n]+)\))?(?P<breaking>!)?: (?P<subject>\S.*)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the header and breaking-change footer of a Conventional Commit message."
    )
    parser.add_argument(
        "message_file", nargs="?", help="commit message file (Git commit-msg hook compatible)"
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--message", help="commit message text")
    source.add_argument("--message-file", dest="message_path", help="path to a commit message file")
    parser.add_argument(
        "--allowed-types", help="optional comma-separated project policy; defaults to any non-empty type"
    )
    parser.add_argument(
        "--task-id-regex",
        help="optional regex required to match the first subject token, e.g. '[A-Z]+-[0-9]+'",
    )
    return parser.parse_args()


def read_message(args: argparse.Namespace) -> str:
    if args.message_file and args.message_path:
        raise ValueError("provide the message file either positionally or with --message-file, not both")
    if args.message is not None:
        if args.message_file or args.message_path:
            raise ValueError("--message cannot be combined with a message file")
        return args.message
    path = args.message_file or args.message_path
    if path:
        try:
            return Path(path).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise ValueError(f"cannot read commit message file {path!r}: {error}") from error
    if sys.stdin.isatty():
        raise ValueError("provide a message argument, message file, or piped standard input")
    try:
        message = sys.stdin.read()
        if not message:
            raise ValueError("standard input is empty; provide a commit message")
        return message
    except (OSError, UnicodeError) as error:
        raise ValueError(f"cannot read standard input: {error}") from error


def validate(message: str, allowed_types: Optional[str], task_id_regex: Optional[str]) -> list[str]:
    errors: list[str] = []
    lines = message.splitlines()
    if not lines or not lines[0].strip():
        return ["commit message must start with a non-empty Conventional Commit header"]

    match = HEADER.fullmatch(lines[0])
    if not match:
        errors.append("header must use '<type>(optional-scope)[!]: <non-empty subject>'")
    else:
        if allowed_types is not None:
            types = {item.strip() for item in allowed_types.split(",") if item.strip()}
            if not types:
                errors.append("--allowed-types must contain at least one non-empty type")
            elif match.group("type") not in types:
                errors.append(
                    f"type {match.group('type')!r} is not allowed; expected one of: {', '.join(sorted(types))}"
                )
        if task_id_regex is not None:
            try:
                task_pattern = re.compile(task_id_regex)
            except re.error as error:
                errors.append(f"invalid --task-id-regex: {error}")
            else:
                first_token = match.group("subject").split(maxsplit=1)[0]
                task_id = first_token[:-1] if first_token.endswith(":") else first_token
                if not task_pattern.fullmatch(task_id) or not first_token.endswith(":"):
                    errors.append(
                        "subject must begin with a task identifier matching --task-id-regex followed by ':'"
                    )

    for number, line in enumerate(lines[1:], start=2):
        if line.startswith("BREAKING-CHANGE:"):
            errors.append(f"line {number}: use the Conventional Commits footer token 'BREAKING CHANGE:'")
        elif line.startswith("BREAKING CHANGE:") and not line[len("BREAKING CHANGE:"):].strip():
            errors.append(f"line {number}: BREAKING CHANGE: must include a description")
    return errors


def main() -> int:
    args = parse_args()
    try:
        message = read_message(args)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    errors = validate(message, args.allowed_types, args.task_id_regex)
    if errors:
        for error in errors:
            print(f"invalid commit message: {error}", file=sys.stderr)
        return 1
    print("valid Conventional Commit message")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
