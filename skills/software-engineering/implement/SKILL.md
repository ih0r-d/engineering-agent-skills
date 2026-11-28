---
name: implement
description: Implement an approved feature or intentional change to software behavior. Use for scoped source changes against requirements, acceptance criteria, and existing caller contracts.
---

# Implement

## Workflow

1. Confirm edit authorization, the requested behavior, and the affected public entrypoints. Trace acceptance criteria to the authoritative specification or user requirements and identify existing contracts that must remain compatible.
2. Inspect the relevant source, manifests, dependencies, and configuration to identify the language, framework, and supported versions. Follow explicit user technology requirements first. If evidence is insufficient or no matching reference exists, follow the generic steps and project conventions.
3. Load only references whose technology and stated concern match the change. Inspect relevant callers, tests, generated inputs, and runtime constraints before choosing an approach.
4. Resolve material gaps or conflicts between the specification, existing behavior, and tests before editing. Establish a baseline and choose the smallest change that meets the acceptance criteria. Identify focused checks for new behavior and affected existing callers.
5. Implement through the normal entrypoints in small, verifiable steps. Reuse existing contracts, types, and control flow. Account for applicable failure paths, existing data, and compatibility. Keep dependency, build, and unrelated changes outside the edit scope unless authorized.
6. Inspect the final diff and verify each relevant acceptance criterion and preserved contract at the same boundaries. Run existing targeted checks on supported versions and expand coverage where affected callers warrant it. Distinguish regressions, baseline failures, and unverified conditions.

## Reference selection

| Reference | Load when |
| --- | --- |
| [Java type contracts](references/java/type-contracts.md) | Changing equality, hashing, ordering, records, sealed types, or generics. |
| [Java concurrency](references/java/concurrency.md) | Changing shared-state invariants, synchronization, executors, or cancellation. |
| [Spring transactions](references/spring-boot/spring-transactions.md) | Changing an advised Spring transaction boundary or rollback behavior. |
| [Quarkus](references/quarkus/quarkus.md) | Changing evidenced Quarkus configuration, CDI wiring, REST dispatch, or native behavior. |
| [Python typing](references/python/typing.md) | Changing generic APIs, protocols, narrowing, or overloaded signatures. |
| [Asyncio](references/python/asyncio.md) | Changing asyncio task ownership, cancellation, timeouts, or event-loop execution. |
| [FastAPI](references/fastapi/fastapi.md) | Changing FastAPI routes, dependencies, validation, or ASGI lifecycle. |
| [Pydantic](references/pydantic/pydantic.md) | Changing Pydantic validation, settings, or serialization. |
| [Shell scripting](references/shell/arguments-and-status.md) | Changing Bash or POSIX sh argument handling, command status, or cleanup. |

## Boundaries and result

Keep proposal, review-only, and diagnosis-only requests read-only. Preserve source, binary, and behavioral compatibility within the authorized scope, including generated and reflective consumers where applicable. Inspect command effects before execution. Keep staging, commits, deployment, and other external effects outside implementation authorization.

Use the defect workflow for restoring expected behavior and the refactoring workflow for structural changes that preserve behavior.

If the client supports subagents and the task permits delegation, delegate only bounded, independent work with clear inputs, scope, and verification. Give edit tasks disjoint file ownership and keep shared contracts and integration with the primary agent. Review each contribution against the specification and run integrated checks. If work overlaps or delegation is unavailable or unauthorized, carry out the same steps sequentially.

Report the change, acceptance criteria verified, preserved contracts, executed checks and results, and unresolved risks.
