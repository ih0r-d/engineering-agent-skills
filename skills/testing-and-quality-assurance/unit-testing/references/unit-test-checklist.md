# Unit Test Checklist

## Test design

| Concern | Guidance |
| --- | --- |
| Boundaries | Cover empty, invalid, minimum, maximum, and representative inputs as applicable. |
| Assertions | Check observable results, errors, and contractually relevant side effects. |
| Isolation | Control clocks, randomness, filesystem, and external dependencies when needed. |
| Test doubles | Stub external behavior; verify interactions only when part of the contract. |
| Regression | Demonstrate that a focused test detects the original defect when feasible. |

## Maintainability

- Use descriptive names and local fixture conventions.
- Avoid asserting private implementation details or duplicating production logic in assertions.
- Avoid shared mutable test state, sleeps, and order-dependent tests.
- Preserve intentional exception and mutation contracts.
- Do not weaken assertions or skip failing tests to obtain a green suite.
- Reuse existing framework and dependency configuration unless changes are approved.
