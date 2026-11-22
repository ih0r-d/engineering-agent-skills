---
name: build-automation-quality
description: Review or repair Maven and Gradle build configuration, Makefiles, and Taskfiles. Use for task dependencies, incremental builds, local and CI parity, reproducibility, or command-runner failures.
---

# Build Automation Quality

1. Identify the entrypoint actually used by developers and CI, the wrapper or runner version, selected modules, profiles and environment. Start with changed targets and their prerequisites and consumers. Inventory the whole graph for a requested full audit.
2. Read [Maven and Gradle](references/jvm-builds.md) for JVM builds or [Make and Task](references/build-system-review.md) for task runners. Apply rules for the tool and version actually in use.
3. Trace command arguments, working directories and input-to-output edges. Compare a fresh run, an unchanged run and a run after a meaningful input change if safe. Diagnose whether a failure comes from the build graph, a child command, missing cache, or environment differences. Inspect parse and configuration effects before running even help or dry-run commands.
4. Review without editing. For verification, prefer existing non-publishing targets in an isolated workspace with the required local caches and versions. Apply the smallest authorized graph, quoting or configuration fix. Preserve entrypoints, artifact contracts, supported platforms and intentional environment overrides.
5. Report severity, configuration location, triggering command and condition, what gets skipped or fails, the smallest correction and its verification. Record workspace, profiles and versions for reproduced failures. Keep complete non-sensitive output locally and reuse unchanged checks.

Keep source-level Java concerns with Java review, and production publishing or deployment changes with release preparation. Resist replacement runners or new pipeline layers for a defect in one existing edge.
