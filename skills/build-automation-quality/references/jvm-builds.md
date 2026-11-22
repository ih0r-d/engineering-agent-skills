# Maven and Gradle build review

Confirm wrapper distribution and checksums, build JDK, compiler toolchain and target runtime. Follow CI's entrypoint, including settings, init scripts, profiles, project directories and dependency caches. Version-locking choices depend on the project's update policy. Verify resolved versions when ranges, snapshots, dynamic versions or plugin defaults affect reproducibility.

## Maven

- Inspect parent POMs, imports, profiles, settings, and effective dependencies and plugins as needed. `dependencyManagement` controls selected versions when dependencies are used. `pluginManagement` supplies defaults to plugins when they are used. Verify actual executions and phase bindings. A plugin configured only in management may never run.
- Compare running the full reactor with scoped builds, such as a reviewed `./mvnw -o -pl :module -am test` where dependencies are cached. `-am` includes required reactor projects. Inspect reactor ordering and duplicate artifact resolution when a cached local SNAPSHOT can hide a missing edge. Run from the reactor root when that is the supported entrypoint.
- Inspect generated-source and test integration at the relevant phases. `test` does not ordinarily run verify-phase integration checks. Check test patterns, skip flags, failsafe verification and profiles before concluding a suite ran. Inspect bound executions before invoking phases.
- Use a trusted, configured `help:effective-pom` or `dependency:tree` only if the required plugins and inputs are available. Keep settings or effective model output with sensitive material out of logs.

## Gradle

- Trace lazy task registration and actual inputs and outputs, including generated directories. Prefer wiring a consumer input to the producer's output provider when suitable. `mustRunAfter` governs ordering when both are selected. A required producer must also be selected through an appropriate task dependency.
- Walk declared inputs for environment variables, files, options and tool versions that affect output. Check overlapping outputs, relative paths and reproducibility across checkouts before enabling caching. Use a clean fixture, an unchanged rerun and a changed-input rerun. Distinguish up-to-date, cache hits and configuration-cache reuse.
- Inspect wrapper, version catalog, platform constraints, dependency locks and artifact verification where present. Avoid rewriting pins or enabling global cache policy for one task defect.
- `./gradlew --offline :module:test --dry-run` can show selected tasks in a trusted configured project. Gradle still evaluates settings, plugins and configuration code, and wrapper bootstrap precedes Gradle's offline option. Avoid deployment and publish tasks during local verification.

References. [Maven lifecycle](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html), [Maven multi-module builds](https://maven.apache.org/guides/mini/guide-multiple-modules.html), [Gradle incremental builds](https://docs.gradle.org/current/userguide/incremental_build.html)
