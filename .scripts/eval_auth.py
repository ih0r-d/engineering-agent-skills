"""Keep the pilot's native Codex login separate from user and run state."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import json
from pathlib import Path
import stat
import subprocess
import sys


class AuthenticationError(Exception):
    """Authentication could not safely proceed."""


def chatgpt_secrets(path: Path) -> set[bytes]:
    """Check the pinned CLI's OAuth file and collect known secrets for redaction."""
    try:
        info = path.lstat()
        if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
                or info.st_mode & 0o077 or info.st_size > 1024 * 1024):
            raise AuthenticationError("Expected a private Codex OAuth cache in the temporary home.")
        data = json.loads(path.read_bytes())
    except (OSError, ValueError):
        raise AuthenticationError("Codex did not leave a readable OAuth cache in the temporary home.") from None

    if not isinstance(data, dict) or data.get("auth_mode") != "chatgpt" or data.get("OPENAI_API_KEY"):
        raise AuthenticationError("Expected a native ChatGPT login with no saved API key.")
    tokens = data.get("tokens")
    keys = ("access_token", "refresh_token", "id_token")
    if not isinstance(tokens, dict) or any(
        not isinstance(tokens.get(key), str) or not tokens[key] for key in keys
    ):
        raise AuthenticationError("The temporary ChatGPT OAuth cache is incomplete.")
    return {tokens[key].encode("utf-8") for key in keys}


def redact(data: bytes, secrets: set[bytes]) -> bytes:
    # Cover both literal output and tokens encoded as JSON strings.
    encoded = {json.dumps(secret.decode("utf-8"))[1:-1].encode("ascii") for secret in secrets}
    for secret in sorted(secrets | encoded, key=len, reverse=True):
        data = data.replace(secret, b"[REDACTED]")
    return data


@dataclass(repr=False)
class Authentication:
    mode: str
    key: str | None = None
    cache: Path | None = None

    @property
    def options(self) -> list[str]:
        method = "chatgpt" if self.mode == "chatgpt" else "api"
        return ["-c", f'forced_login_method="{method}"', "-c", 'cli_auth_credentials_store="file"']

    def login(self, binary: str, env: dict[str, str]) -> None:
        if not sys.stdin.isatty() or not sys.stderr.isatty():
            raise AuthenticationError("ChatGPT sign-in requires a private interactive terminal.")
        command = [binary, "login", "--device-auth", *self.options]
        print("Complete the native Codex ChatGPT device sign-in for this batch.", flush=True)
        result = subprocess.run(command, cwd=env["HOME"], env=env, timeout=300, check=False)
        if result.returncode:
            raise AuthenticationError("ChatGPT sign-in failed. No model run was started.")
        cache = Path(env["CODEX_HOME"]) / "auth.json"
        chatgpt_secrets(cache)
        self.cache = cache

    @contextmanager
    def for_run(self, env: dict[str, str]):
        if self.mode == "api-key":
            if not self.key:
                raise AuthenticationError("API-key mode requires CODEX_API_KEY in the environment.")
            yield {**env, "CODEX_API_KEY": self.key}, {self.key.encode("utf-8")}, None
            return
        if self.cache is None:
            raise AuthenticationError("ChatGPT sign-in has not completed for this batch.")
        secrets = chatgpt_secrets(self.cache)
        local = Path(env["CODEX_HOME"]) / "auth.json"
        if local.exists() or local.is_symlink():
            raise AuthenticationError("The disposable run home already contains a credential cache.")
        self.cache.rename(local)
        try:
            yield env, secrets, local
        finally:
            # Carry forward native refreshes without running two copies of the session.
            if local.exists():
                local.rename(self.cache)
