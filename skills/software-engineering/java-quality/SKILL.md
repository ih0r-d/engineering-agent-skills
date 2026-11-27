---
name: java-quality
description: Review Java source or generated Java for correctness, API compatibility, resource ownership, concurrency, or framework behavior. Use for Java code audits, targeted fixes, and triage of compiler or Java analyzer findings.
---

# Java Quality

## Operating Modes

| Mode | Responsibility |
| --- | --- |
| Review (default) | Inspect and report findings without editing files. |
| Fix | Address requested defects with the smallest compatible change and a focused regression test where it would establish behavior. |
| Verification | Run applicable existing checks without editing sources or configuration. |

## Workflow

1. Establish the diff or requested component, then trace changed declarations to their callers, tests and generated inputs. Expand to the repository only for a full audit.
2. Read the Maven or Gradle configuration and CI to identify the compiler JDK, target release, source sets, annotation processors and test boundaries.
3. Reproduce the relevant failure on a supported JDK or establish it from the language and caller contracts. Inspect state ownership, exceptional paths, nullability, compatibility and lifecycle behavior before assessing style.
4. Load relevant references according to the task.
5. Prefer the configured module test, compiler or compatibility check. Inspect wrappers, profiles and goals before running them.
6. Keep complete non-sensitive logs outside the checkout and reuse results for identical inputs, tool versions and configuration.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Language and API review](references/quality-rubric.md) | Reviewing source behavior, JavaDoc or public contracts. |
| [Module and framework boundaries](references/boundaries.md) | Investigating generated code, proxies or class loading. |
| [Concurrency](references/concurrency.md) | Tracing a race, stale read, deadlock, executor failure, or cancellation bug. |
| [JVM diagnostics](references/runtime-diagnostics.md) | Investigating heap growth, GC pauses, thread starvation, native memory, or class-loader retention. |
| [Spring transactions](references/spring-transactions.md) | Debugging missing transaction boundaries, rollback behavior, or proxy-based advice. |
| [Virtual threads](references/virtual-threads.md) | Reviewing Java 21+ blocking concurrency or pinning symptoms. |
| [Java type and value contracts](references/type-contracts.md) | Reviewing equality, hashing, ordering, records, sealed hierarchies, or generics. |
| [Persistence](references/persistence.md) | Investigating JPA/Hibernate query counts, entity state, lazy loading, locking, or transaction scope. |
| [Native Image](references/native-image.md) | Diagnosing GraalVM native-image failures, reflection metadata, resources, or class initialization. |
| [Static analysis](references/static-analysis.md) | Choosing checks or investigating analyzer diagnostics. |
| [Minimal-change examples](references/anti-overengineering.md) | Evaluating duplication or cleanup findings with competing fixes. |

## Constraints

- Follow repository rules for build files and dependencies.
- Preserve source, binary and behavioral compatibility, including generated APIs and reflective consumers, unless the requested change permits a break.
- Use language features supported by the target release.
- Keep build-graph and task wiring reviews with the build automation workflow.

## Expected Output

For each finding, report:

- Severity and file location.
- Reachable failure and affected callers.
- Smallest compatible correction.
- How the correction was or can be verified.

Label uncertain risks and skipped checks. Group diagnostics with the same cause.
