---
name: build-automation-quality
description: Review or repair Maven and Gradle build configuration, Makefiles, and Taskfiles. Use for task dependencies, incremental builds, local and CI parity, reproducibility, or command-runner failures.
---

# Build Automation Quality

## Operating Modes

| Mode | Responsibility |
| --- | --- |
| Review | Inspect build configuration and report findings without editing. |
| Fix | Apply the smallest authorized graph, quoting or configuration fix. |
| Verification | Prefer existing non-publishing targets in an isolated workspace with the required local caches and versions. |

## Workflow

1. Identify the entrypoint actually used by developers and CI, the wrapper or runner version, selected modules, profiles and environment.
2. Start with changed targets and their prerequisites and consumers. Inventory the whole graph for a requested full audit.
3. Load relevant references and apply rules for the tool and version actually in use.
4. Trace command arguments, working directories and input-to-output edges.
5. Compare a fresh run, an unchanged run and a run after a meaningful input change if safe.
6. Diagnose whether a failure comes from the build graph, a child command, missing cache, or environment differences.
7. Keep complete non-sensitive output locally and reuse unchanged checks.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Maven](references/maven.md) | `pom.xml`, Maven Wrapper, plugins, profiles, or reactor builds are involved. |
| [Gradle](references/gradle.md) | `build.gradle[.kts]`, Gradle Wrapper, task graph, or dependency resolution is involved. |
| [GNU Make](references/make.md) | A Makefile, target dependency graph, or recipe execution is involved. |
| [Taskfile](references/taskfile.md) | `Taskfile.yml`, `task` dependencies, status checks, or variable expansion is involved. |
| [Build reproducibility](references/reproducibility.md) | Diagnosing stale outputs, cache misses, non-hermetic builds, or cross-platform drift. |

## Constraints

- Inspect parse and configuration effects before running even help or dry-run commands.
- Preserve entrypoints, artifact contracts, supported platforms and intentional environment overrides.
- Keep source-level Java concerns with Java review.
- Keep production publishing or deployment changes with release preparation.
- Resist replacement runners or new pipeline layers for a defect in one existing edge.

## Expected Output

For each finding, report:

- Severity and configuration location.
- Triggering command and condition.
- What gets skipped or fails.
- Smallest applicable correction.
- Verification.

Record workspace, profiles and versions for reproduced failures.
