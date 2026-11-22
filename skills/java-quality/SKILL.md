---
name: java-quality
description: Review Java source or generated Java for correctness, API compatibility, resource ownership, concurrency, or framework behavior. Use for Java code audits, targeted fixes, and triage of compiler or Java analyzer findings.
---

# Java Quality

Default to a read-only review. In fix mode, address the requested defects with the smallest compatible change and a focused regression test where it would establish behavior. In verification mode, run the applicable existing checks without editing sources or configuration. Follow repository rules for build files and dependencies.

1. Establish the diff or requested component, then trace changed declarations to their callers, tests and generated inputs. Expand to the repository only for a full audit. Read the Maven or Gradle configuration and CI to identify the compiler JDK, target release, source sets, annotation processors and test boundaries.
2. Reproduce the relevant failure on a supported JDK or establish it from the language and caller contracts. Inspect state ownership, exceptional paths, nullability, compatibility and lifecycle behavior before assessing style.
3. Read [language and API review](references/quality-rubric.md) for source behavior, JavaDoc and public contracts, [module and framework boundaries](references/boundaries.md) for generated code, proxies or class loading, and [static analysis](references/static-analysis.md) when choosing checks or investigating diagnostics. Use [minimal-change examples](references/anti-overengineering.md) when a duplication or cleanup finding has competing fixes.
4. Prefer the configured module test, compiler or compatibility check. Inspect wrappers, profiles and goals before running them. Keep complete non-sensitive logs outside the checkout and reuse results for identical inputs, tool versions and configuration.
5. Report severity with file and line, reachable failure, affected callers, smallest compatible correction and how it was or can be verified. Label uncertain risks and skipped checks. Group diagnostics with the same cause.

Preserve source, binary and behavioral compatibility, including generated APIs and reflective consumers, unless the requested change permits a break. Use language features supported by the target release. Keep build-graph and task wiring reviews with the build automation workflow.
