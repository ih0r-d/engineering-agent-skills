# Build reproducibility and cache correctness

Load when results differ across machines, builds are unexpectedly skipped or repeated, or caching is being introduced.

- Define the artifact and inputs first: source files, generated sources, toolchain, environment, dependency graph, locale/time zone, network-fetched data, and relevant system properties.
- A cache key is correct only when it represents every input that can change output. Missing inputs create stale results; unstable timestamps, absolute paths, or undeclared environment create misses or non-reproducible artifacts.
- For Gradle, wire task outputs to consumer inputs using providers where appropriate. `mustRunAfter` orders tasks that are both selected; it does not add the producer to the task graph. Avoid overlapping outputs and verify relocatability before enabling remote caching.
- For Make, ensure file targets list every file prerequisite and keep action targets `.PHONY`. Order-only prerequisites are useful for output directories whose timestamps should not cause rebuilds.
- For Task, verify `sources`, `generates`, status logic, variables, and preconditions together. A status command should test whether work is current; a precondition should enforce a requirement.
- Compare a clean build, unchanged rerun, and one-input-change rerun. Inspect resulting artifacts or public behavior, not only task selection or log messages.
- Avoid cache configuration changes that affect unrelated builds. Establish correctness with caches disabled or empty before measuring cache benefits.

Sources: [Gradle build lifecycle](https://docs.gradle.org/current/userguide/build_lifecycle.html), [Gradle incremental builds](https://docs.gradle.org/current/userguide/incremental_build.html), [Maven build lifecycle](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html), [GNU Make manual](https://www.gnu.org/software/make/manual/), [Task documentation](https://taskfile.dev/docs/).
