---
name: bug-fixing
description: Fix an authorized software defect with a scoped correction and regression verification. Use when expected behavior and a reported failure require an implementation change.
---

# Bug Fixing

## Workflow

1. Confirm the requested behavior change, affected contract, and edit authorization.
2. Establish the failure using source, caller contracts, or a safe reproduction. Use bug investigation or language-specific guidance when needed.
3. Identify the smallest correction that addresses the supported cause rather than masking symptoms.
4. Add or identify a focused regression test that detects the defect; establish its pre-fix result when practical.
5. Apply the correction within scope and preserve unrelated behavior and public contracts.
6. Rerun focused tests and applicable existing checks; compare results with the baseline.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed checklist](references/fix-checklist.md) | Additional guidance is needed for scoped defect correction, regression tests, and compatibility verification. |

## Constraints

- Do not edit when the request is investigation or review only.
- Avoid unrelated refactoring, dependencies, configuration changes, and broad exception suppression.
- Do not weaken tests to obtain a passing result.
- If the cause or intended behavior is unclear, report missing evidence before making speculative changes.

## Expected Output

Report the defect, supporting evidence, localized correction, preserved contracts, executed checks and outcomes, and residual risks.
