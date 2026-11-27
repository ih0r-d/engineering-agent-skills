---
name: test-strategy
description: Define risk-based software testing strategies, coverage goals, test levels, and quality gates. Use for test planning, coverage gaps, and verification priorities across a system or change.
---

# Test Strategy

## Workflow

1. Identify critical user journeys, business invariants, supported environments, change scope, and failure impact.
2. Inspect existing tests, defects, CI checks, and available coverage evidence. Distinguish measured gaps from assumptions.
3. Map risks to the lowest test level that can establish the required behavior; reserve broader tests for cross-boundary risks.
4. Define representative positive, negative, boundary, failure, and recovery scenarios with observable acceptance criteria.
5. Prioritize scenarios by impact, likelihood, cost, and feedback speed. Define quality gates, test data needs, ownership, and remaining risks.
6. Hand off authorized implementation to unit-testing or integration-testing as appropriate.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/strategy-checklist.md) | Additional guidance on test or review decisions is needed. |

## Constraints

- Default to planning without modifying files unless requested.
- Do not invent coverage percentages or successful test runs.
- Do not prescribe fixed coverage targets or test ratios without project evidence.
- Keep dedicated security assessment and implementation debugging in their own workflows.

## Expected Output

Report risk priorities, test levels, scenario matrix, quality gates, prerequisites, and unresolved coverage gaps.
