---
name: test-code
description: Plan risk-based verification or write, review, and run unit, integration, and contract tests. Use for coverage decisions, test isolation, regression checks, and cross-component behavior.
---

# Test Code

## Workflow

1. Identify the requested scope, observable behavior, risks, and acceptance criteria. For test strategy, prioritize risks and assign test levels, prerequisites, quality gates, and exit criteria.
2. Identify the test framework, runtime, collaborator versions, and configured commands. Follow explicit user requirements first, then inspect the affected tests, manifests, dependencies, and CI. Load only references matching the evidenced stack and scenario. Use project conventions and the generic workflow if no specialized guidance applies.
3. Select success, boundary, error, and recovery cases based on the intended contract. For unit tests, use deterministic inputs and isolate external effects where necessary. For integration and contract tests, use representative collaborators where their behavior matters and record what simulations omit.
4. Inspect imports, setup hooks, credentials, network effects, readiness, data ownership and teardown before running tests. Use synthetic data and isolated, disposable environments. Make test setup, assertions and cleanup deterministic.
5. For authorized test changes, write focused assertions against the public result. In a test-first workflow, establish the expected failure before the correction. For regression coverage, show that the test detects the original defect where safely possible.
6. Run applicable targeted tests and relevant broader checks. Report the commands, outcomes, tested boundaries, and gaps. Connect strategy, coverage and test assertions to the risks they address.

## Reference selection

| Reference | Load when |
| --- | --- |
| [Test strategy](references/strategy-checklist.md) | Selecting risk-based test levels, gates, or acceptance criteria. Use the [test plan template](assets/test-plan-template.md) when a reusable plan is requested. |
| [Unit tests](references/unit-test-checklist.md) | Choosing unit cases, doubles, assertions, or isolation. |
| [Integration tests](references/integration-checklist.md) | Choosing real collaborators, contract scenarios, readiness, or teardown. |
| [JUnit Jupiter](references/junit-jupiter/junit-jupiter.md) | Jupiter discovery, extensions, or instance lifecycle is involved. |
| [Mockito](references/mockito/mockito.md) | Mockito stubs, spies, matchers, captors, or interaction assertions are involved. |
| [pytest](references/pytest/pytest.md) | pytest fixture scopes, parametrization, plugins, or monkeypatching is involved. |
| [Testcontainers](references/testcontainers/testcontainers.md) | The tests use Testcontainers and the container lifecycle or runtime prerequisites matter. |
| [Shell verification](references/shell/verification.md) | Verifying Bash or POSIX sh argument boundaries, exit status, or fixture side effects. |

## Boundaries

Planning, review, and verification-only requests leave repository files untouched. Edit tests only when requested. Production code, configuration, or dependency changes require separate authorization, as do starting external services and pulling images. Keep verification away from production and real customer data. Use measured coverage and project constraints when setting thresholds.
