---
name: shell-quality
description: Review or improve Bash and POSIX shell scripts for correctness, quoting, portability, safety, error handling, and maintainability.
---

# Shell Quality

1. Identify the actual shell from the shebang and execution environment (including macOS Bash compatibility); never assume Bash-only syntax is POSIX.
2. Use [shell-review.md](references/shell-review.md) when auditing scripts, installers, or release automation.
3. Read-only review must not execute potentially destructive or network-dependent commands; inspect effects first.
4. Prefer locally available `shellcheck`, `shfmt`, `bash -n`, or `sh -n` as appropriate; report missing tools rather than changing dependencies.
5. Only on request, apply minimal safe corrections, test success and failure paths, and preserve CLI options and exit codes.
6. Never auto-run destructive operations, edit secrets, commit, or push.
