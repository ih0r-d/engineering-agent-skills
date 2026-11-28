---
name: debug
description: Diagnose software failures and explain supported causes. Use for reproducible or intermittent defects, runtime diagnostics, environment differences, and analysis of recurring failure mechanisms.
---

# Debug

## Workflow

1. Establish expected and observed behavior, affected inputs, relevant versions, and the failing environment. Start with the smallest useful failing boundary.
2. Identify the runtime, framework, and version from explicit user requirements first, then logs, source, manifests, dependencies, and configuration for the affected environment. Load only references that match both the evidenced technology and the symptom. Use the generic workflow and project conventions when evidence or matching guidance is missing.
3. Compare failing and healthy cases under equivalent conditions. Reproduce in a disposable fixture where safe. Keep missing telemetry and unavailable prerequisites distinct from evidence against a hypothesis.
4. Form competing hypotheses and choose checks that would distinguish them. Change one relevant variable at a time. Follow relevant callers and dependencies, keeping logs free of credentials and personal data.
5. Trace the failure mechanism and distinguish triggers, contributing factors, and systemic weaknesses as the task warrants. Document which causal links are observed, inferred, or unknown. Propose a focused regression check and, for a recurring issue, preventive actions with verification criteria.

## Reference selection

| Reference | Load when |
| --- | --- |
| [Diagnostic checklist](references/diagnostic-checklist.md) | A failure is intermittent or environment-specific, or you need to isolate the failing boundary. |
| [Causal analysis](references/causal-analysis.md) | A recurring failure requires causal links, contributing factors, and prevention criteria. |
| [JVM diagnostics](references/java/runtime-diagnostics.md) | Investigating JVM heap, GC, starvation, native memory, or class-loader retention. |
| [Virtual threads](references/java/virtual-threads.md) | Investigating virtual-thread pinning, resource exhaustion, or thread-local behavior on the evidenced JDK. |
| [Spring Boot](references/spring-boot/spring-boot.md) | Diagnosing Boot auto-configuration, property binding, Actuator, or test-slice context behavior. |
| [JPA/Hibernate](references/jpa-hibernate/persistence.md) | Tracing entity state, query counts, lazy loading, locks, or transaction scope. |
| [GraalVM Native Image](references/graalvm/native-image.md) | Triaging native-only reflection, resources, or class initialization behavior. |
| [Python runtime](references/python/runtime-and-concurrency.md) | Tracing Python aliasing, memory retention, scheduling, or thread, process, or asyncio behavior. |
| [SQLAlchemy](references/sqlalchemy/sqlalchemy.md) | Tracing evidenced SQLAlchemy session ownership, lazy state, loading, or transactions. |
| [Shell lifecycle](references/shell/process-lifecycle.md) | Diagnosing Bash or POSIX sh status loss, traps, background processes, or cleanup. |

## Boundaries and result

Keep fault isolation and systemic causal analysis read-only and use disposable local probes. Source edits, production probes or state changes, and access to sensitive data require separate authorization. Report the actual evidence and commands, supported cause and confidence, rejected hypotheses, and the next discriminating check or proposed correction. For systemic analysis include actions tied to the supported mechanisms and how to verify them.
