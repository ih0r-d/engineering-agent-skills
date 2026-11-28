---
name: maintain-build
description: Review, repair, or verify build automation and dependency resolution. Use for build graphs, task runners, reproducibility, package manifests, lockfiles, and scoped dependency upgrades.
---

# Maintain Build

## Workflow

1. Identify the affected entrypoint and its callers, project policy, and artifact contract. Start with explicit user technology requirements, then inspect wrappers, manifests, lockfiles, build settings and CI to find the tool, version, profiles, modules, and supported runtimes actually used.
2. Load only references matching the tool and issue. Use the generic workflow and project conventions when the tool is uncertain or has no specialized reference.
3. For build behavior, trace inputs, outputs, prerequisites, command arguments, working directories and child failures. Compare a fresh run, an unchanged run, and a run after a relevant input change where safe. Separate graph issues from runner, cache, and environment differences.
4. For dependency changes, distinguish direct requests from transitive resolution. Establish the conflict, advisory, or upgrade requirement, and check release notes, compatibility constraints, and affected usage. Choose the smallest supported change and explain manifest and lockfile effects.
5. Apply only authorized changes. Prefer existing non-publishing commands with trusted inputs in an isolated workspace. Inspect parse and configuration effects, hooks, wrapper caches, and network requirements before even dry runs or help commands.
6. Compare resolution, artifacts and affected behavior with the baseline. Report affected commands or coordinates, versions, the smallest correction, checks run, and any registry or environment limits. Keep complete non-sensitive logs locally and reuse checks when inputs are unchanged.

## Reference selection

| Reference | Load when |
| --- | --- |
| [Dependencies](references/dependency-checklist.md) | Resolving dependency conflicts, assessing upgrades, or checking lockfile drift. |
| [Reproducibility](references/reproducibility.md) | Diagnosing stale outputs, cache misses, non-hermetic builds, or platform drift. |
| [Maven](references/maven/maven.md) | Maven POMs, plugins, profiles, or reactor behavior are relevant. |
| [Gradle](references/gradle/gradle.md) | Gradle configuration, wrapper, task graph, or resolution is relevant. |
| [GNU Make](references/make/make.md) | GNU Make targets, prerequisites, or recipe execution are involved. |
| [Taskfile](references/taskfile/taskfile.md) | Task runner dependencies, status checks, or variable evaluation are involved. |
| [Python packaging](references/python/packaging-and-checks.md) | A Python distribution, installed entrypoint, or its configured checks are affected. |

## Boundaries

Keep review and verification-only requests read-only. Edit build configuration only when requested and change dependency versions or resolution only when authorized for that scope. Preserve entrypoints, artifact contracts, supported platforms, and intentional environment overrides. Keep integrity checks intact and avoid lockfile churn outside the approved change. Do not execute unreviewed lifecycle hooks or use untrusted registries. Release publication and dedicated security assessment require their own scope.
