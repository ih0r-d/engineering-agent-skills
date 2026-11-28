# Code review criteria

Use these criteria for issues within the requested review scope. Start from the diff and inspect enough surrounding code to establish impact.

| Concern | Evidence to check |
| --- | --- |
| Specification compliance | Trace changed paths to the governing requirements and acceptance criteria. Compare intended and actual results at the normal entrypoints, including negative cases and compatibility commitments. If the contract is ambiguous or unavailable, identify the missing evidence and qualify the conclusion. |
| Coding standards | Read the applicable repository instructions, style guides, and configured checks. Tie a standards finding to a rule that applies to the changed code. Consider analyzer scope and verify its signals before inferring a defect. |
| Code smells | Investigate duplicated policy, hidden side effects, unrelated responsibilities, excessive indirection, and control flow that makes invariants hard to follow. Identify a reachable error or concrete change cost before raising a finding. |
| Correctness | Check representative and boundary inputs, error paths, lifecycle and state, and the behavior callers depend on. Check retries, concurrency, partial failure, or existing data when the change reaches those boundaries. |
| Maintainability | Trace who will need to change the code and what they must keep synchronized. Assess interfaces, testability, cohesion, and compatibility. Prefer the smallest correction that addresses the demonstrated cost. |

Prioritize behavioral regressions and required project gates. Keep uncertain risks and preferences distinct from supported findings. Report a triggering input or condition, the affected caller, the consequence, and what evidence would confirm the proposed correction.
