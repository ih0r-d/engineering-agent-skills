---
name: integration-testing
description: Write, review, or verify integration and contract tests across software components, databases, APIs, and messaging boundaries. Use for real collaborator behavior, compatibility, test environments, and cross-component failures.
---

# Integration Testing

## Workflow

1. Identify the integration boundary, participant versions, contracts, existing test tools, and required environment.
2. Choose representative cross-boundary success and failure cases, including serialization, persistence, compatibility, and recovery where relevant.
3. Prefer representative real collaborators when their behavior is the subject of the test. Clearly label simulated dependencies and their limitations.
4. Inspect setup, credentials, network access, data ownership, and cleanup before running tests. Use isolated disposable environments and synthetic data.
5. Implement only authorized tests and configuration changes. Make setup, readiness, assertions, and teardown deterministic.
6. Run applicable checks within approved effects and report the actual integration coverage and remaining gaps.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/integration-checklist.md) | Additional guidance on test or review decisions is needed. |
| [Testcontainers](references/testcontainers.md) | Tests use Testcontainers or depend on a containerized real service. |

## Constraints

- Do not run against production or use real customer data.
- Do not start external services, pull images, or change infrastructure without appropriate authorization.
- Keep unit-level logic checks and system-wide test planning in their own workflows.

## Expected Output

Report tested boundaries, environment, contract scenarios, setup and cleanup, commands and results, and unverified dependencies.
