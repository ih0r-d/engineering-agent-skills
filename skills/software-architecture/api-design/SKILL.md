---
name: api-design
description: Design and evolve API contracts for services and components. Use for REST, RPC, event interfaces, request and response schemas, error semantics, versioning, and backward compatibility.
---

# API Design

## Scope

Define consumer-facing contracts. Keep system boundaries, architecture assessments, and implementation reviews in their specialized workflows.

## Workflow

1. Identify consumers, use cases, existing contracts, and protocol constraints.
2. Define operations, resource semantics, request and response schemas, validation, errors, and authorization.
3. Load relevant protocol and compatibility guidance before resolving contract details.
4. Evaluate pagination, concurrency, idempotency, retries, and asynchronous processing where applicable.
5. Assess consumer compatibility, migration, and versioning requirements.
6. Validate representative interactions, failure scenarios, and edge cases.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [API contracts](references/api-contracts.md) | Selecting interface semantics, schemas, errors, or compatibility strategies. |

## Constraints

- Prefer existing protocols and project conventions; justify new abstractions.
- Keep contracts independent of implementation details unless deliberately exposed.
- Preserve consumer contracts unless breaking changes are explicitly approved.
- Distinguish proposed contracts from implemented or verified behavior.
- Do not edit implementation or publish changes without authorization.

## Expected Output

Provide operations, schemas, error and authorization contracts, examples, compatibility and migration considerations, verification criteria, assumptions, and unresolved decisions.
