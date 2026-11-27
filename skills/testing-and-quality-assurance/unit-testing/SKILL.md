---
name: unit-testing
description: Write, review, or verify focused unit tests for software behavior. Use for boundary cases, deterministic isolation, test doubles, assertions, and regression coverage of individual units.
---

# Unit Testing

## Workflow

1. Identify the unit, observable contract, callers, existing test framework, and supported runtime.
2. Choose representative success, boundary, error, and regression cases. Establish expected behavior independently of the implementation.
3. Use the existing test style and deterministic inputs. Isolate external effects only where needed; prefer real simple collaborators over unnecessary mocks.
4. For authorized changes, add or adjust focused tests with meaningful assertions. Keep production changes outside scope unless separately requested.
5. Run targeted tests and applicable broader checks; for regression tests, establish that the test detects the original defect when safely possible.
6. Report actual results and distinguish skipped or unverified cases.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/unit-test-checklist.md) | Additional guidance on test or review decisions is needed. |
| [JUnit Jupiter](references/junit-jupiter.md) | JUnit Jupiter annotations, extensions, test discovery, or lifecycle callbacks are involved. |
| [Mockito](references/mockito.md) | Mockito stubs, spies, matchers, captors, or interaction assertions are involved. |
| [pytest](references/pytest.md) | pytest fixtures, parametrization, plugins, or monkeypatching are involved. |

## Constraints

- Keep review-only tasks read-only.
- Do not introduce test dependencies or modify production behavior without authorization.
- Use integration-testing when the required evidence depends on real component interactions.

## Expected Output

Report tested contracts, cases, isolation choices, changes, executed commands and results, and coverage limitations.
