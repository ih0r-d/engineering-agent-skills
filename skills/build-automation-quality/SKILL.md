---
name: build-automation-quality
description: Audit and improve Maven, Gradle, Makefile, and Taskfile workflows for correctness, reproducibility, portable commands, and developer experience.
---

# Build Automation Quality

1. Identify the build system, its version, wrapper, modules, task entrypoints, and CI contract. Read-only review is default.
2. Read [build-system-review.md](references/build-system-review.md) for the relevant Maven, Gradle, Make, or Taskfile guidance only.
3. Evaluate dependencies, task ordering, reproducibility, incremental builds, local-versus-CI parity, cross-platform assumptions and destructive operations.
4. Prefer existing wrappers and available `--dry-run`, `--list`, help, validation or safe targets. Never run deployment, publishing, cleaning user data, or network-dependent tasks by default.
5. Fix only when explicitly requested, preserving build behavior and compatibility. Avoid modifying build files solely to integrate optional analyzers.
6. Report evidence, commands run, meaningful failures, and any blocked verification. Never auto-commit or push.
