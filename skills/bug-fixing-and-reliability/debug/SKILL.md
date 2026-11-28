---
name: debug
description: Diagnose software failures, analyze recurring causes, or apply an authorized defect fix. Use for intermittent failures, runtime diagnostics, environment differences, and verified corrections that restore expected behavior.
---

# Debug

## Workflow

Choose diagnosis for an investigation, causal analysis for a recurring or systemic failure, or Fix mode when the user authorizes correcting a defect. A request to investigate, review, or plan keeps the source unchanged.

1. Establish expected and observed behavior, affected inputs, relevant versions, and the failing environment. Start with the smallest useful failing boundary.
2. Identify the runtime, framework, and version from explicit user requirements first, then logs, source, manifests, dependencies, and configuration for the affected environment. Load only references that match both the evidenced technology and the symptom. Use the generic workflow and project conventions when evidence or matching guidance is missing.
3. Compare failing and healthy cases under equivalent conditions. Reproduce in a disposable fixture where safe. Keep missing telemetry and unavailable prerequisites distinct from evidence against a hypothesis.
4. Form competing hypotheses and choose checks that would distinguish them. Change one relevant variable at a time. Follow relevant callers and dependencies, keeping logs free of credentials and personal data.
5. Trace the failure mechanism and distinguish triggers, contributing factors, and systemic weaknesses as the task warrants. Document which causal links are observed, inferred, or unknown. Propose a focused regression check and, for a recurring issue, preventive actions with verification criteria.

## Fix mode

1. Confirm the expected contract, supported cause, and scope of the authorized correction. When those are already established, verify the relevant evidence without repeating a broader investigation. Stop before speculative edits when the cause or intended behavior is unresolved.
2. Add or identify a focused regression check. Establish that it detects the original defect when practical and preserve a baseline for unaffected callers.
3. Apply the smallest compatible correction that addresses the supported cause. Keep mitigation and permanent correction distinct. Preserve unrelated behavior, tests, dependencies, and configuration.
4. Inspect the diff and rerun the focused regression and relevant existing checks. Compare results with the baseline and report actual evidence and remaining risks.

## Reference selection

| Reference | Load when |
| --- | --- |
| [Diagnostic checklist](references/diagnostic-checklist.md) | A failure is intermittent or environment-specific, or you need to isolate the failing boundary. |
| [Causal analysis](references/causal-analysis.md) | A recurring failure requires causal links, contributing factors, and prevention criteria. |
| [Defect correction](references/fix-checklist.md) | Planning or applying a scoped fix, separating mitigation from permanent correction, or verifying a regression. |
| [Java values and resources](references/java/values-and-resources.md) | A Java defect involves immutable values, resource ownership, or exception paths. |
| [JVM diagnostics](references/java/runtime-diagnostics.md) | Investigating JVM heap, GC, starvation, native memory, or class-loader retention. |
| [Virtual threads](references/java/virtual-threads.md) | Investigating virtual-thread pinning, resource exhaustion, or thread-local behavior on the evidenced JDK. |
| [Spring Boot](references/spring-boot/spring-boot.md) | Diagnosing Boot auto-configuration, property binding, Actuator, or test-slice context behavior. |
| [JPA/Hibernate](references/jpa-hibernate/persistence.md) | Tracing entity state, query counts, lazy loading, locks, or transaction scope. |
| [GraalVM Native Image](references/graalvm/native-image.md) | Triaging native-only reflection, resources, or class initialization behavior. |
| [Python runtime](references/python/runtime-and-concurrency.md) | Tracing Python aliasing, memory retention, scheduling, or thread, process, or asyncio behavior. |
| [Python state ownership](references/python/state-ownership.md) | A Python defect involves defaults, mutable state, or caller-visible mutations. |
| [SQLAlchemy](references/sqlalchemy/sqlalchemy.md) | Tracing evidenced SQLAlchemy session ownership, lazy state, loading, or transactions. |
| [Shell lifecycle](references/shell/process-lifecycle.md) | Diagnosing Bash or POSIX sh status loss, traps, background processes, or cleanup. |

## Boundaries and result

Keep fault isolation and systemic causal analysis read-only and use disposable local probes. Fix authorization covers the scoped defect correction and its regression verification. Production probes or state changes, access to sensitive data, and dependency or build changes require separate authorization. Report the cause, confidence, evidence, and next check or verified correction. For systemic analysis include preventive actions and their verification criteria.

When native subagents are available and the task permits delegation, isolate independent evidence checks or authorized fixes with disjoint edit scope. Keep shared findings and final verification with the primary agent. Work sequentially when delegation is unavailable, unauthorized, or the work overlaps.
