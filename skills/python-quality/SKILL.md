---
name: python-quality
description: Review Python code, imports, typing, packaging, and tests for runtime or API regressions. Use for focused Python fixes, pytest verification, or Ruff, Pyright and mypy diagnostic triage.
---

# Python Quality

Review mode leaves repository files untouched. Fix mode changes the affected behavior and its tests when requested. Verification mode uses existing commands and reports their actual coverage. Follow local project instructions for dependencies and configuration.

1. Start with the requested diff or module and its callers and tests. For a full audit, inventory packages, entry points and test environments. Determine the supported Python versions from packaging and CI and identify how the project selects its interpreter, environment and dependency groups.
2. Trace the actual import and call paths, including installed-package behavior where relevant. Check failure, cleanup, cancellation, mutation and compatibility at the boundaries the change touches.
3. Use [runtime and API review](references/quality-rubric.md) for language, typing and lifecycle, and [packaging and checks](references/packaging-and-checks.md) for installed artifacts, analyzer configuration and verification. Read the relevant reference as the task requires.
4. Prefer existing Ruff, Pyright or mypy settings and targeted pytest runs. Verify analyzer findings against runtime behavior and supported versions. Keep full non-sensitive logs locally and rerun only when inputs or check conditions change.
5. Give each finding a severity, file and line, failing input or caller, effect, small fix and verification. Identify gaps in the environment or coverage. Treat formatting as a configured check or an explicit formatting task.

Keep public signatures, imports and exception behavior stable during fixes. Prefer direct control flow and existing types over new frameworks, protocols or wrappers introduced for a single diagnostic.
