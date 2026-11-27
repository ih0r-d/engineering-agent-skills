# Gradle lifecycle and task graph

Load when `build.gradle`, `build.gradle.kts`, Gradle Wrapper, task configuration, or dependency resolution is involved. Confirm the Gradle and plugin versions used by the wrapper and CI.

- Separate initialization, configuration, and task execution. Settings and build scripts can execute logic during configuration, so even task listing or dry-run is not a security sandbox for an untrusted build.
- Trace task dependencies, inputs, outputs, and actual execution. `dependsOn` adds work to the graph; `mustRunAfter` only orders tasks already selected. Use providers to wire producer outputs to consumer inputs where the plugin supports them.
- A task is safely up-to-date or cacheable only when declared inputs and outputs represent what affects its result. Check generated files, environment, toolchain, overlapping outputs, relocatability, and external effects before enabling build-cache reuse.
- Distinguish task up-to-date state, build-cache hits, and configuration-cache reuse. Compare a clean run, unchanged rerun, and one-input-change run while inspecting artifacts; task-selection logs alone do not prove correctness.
- Review multi-project settings, project path, included builds, plugin management, and dependency resolution boundaries. Version catalogs centralize declarations but do not by themselves lock resolved transitive versions.
- Use dependency locking or verification according to the repository policy. Check lock update commands and verification metadata before running them because they can change tracked files.
- `--offline` applies to dependency resolution; Wrapper bootstrap happens before Gradle starts. `--dry-run` can still evaluate trusted project configuration. Avoid publish, deploy, and other external-effect tasks during local review.

Sources: [Gradle build lifecycle](https://docs.gradle.org/current/userguide/build_lifecycle.html), [Task dependencies](https://docs.gradle.org/current/userguide/controlling_task_execution.html), [Incremental builds](https://docs.gradle.org/current/userguide/incremental_build.html), [Dependency locking](https://docs.gradle.org/current/userguide/dependency_locking.html)
