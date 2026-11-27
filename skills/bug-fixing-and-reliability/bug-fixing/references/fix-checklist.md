# Bug Fixing Checklist

Apply selectively to the task and available evidence.

## Regression strategy

| Situation | Action |
| --- | --- |
| Reproducible failure | Add a test that fails for the established defect before the correction. |
| Existing failing test | Confirm it expresses the intended contract rather than an outdated expectation. |
| Intermittent defect | Prefer a controlled reproduction, deterministic synchronization or recorded inputs where feasible. |
| Missing environment | State which checks are unavailable and use source evidence without claiming runtime verification. |

## Correction review

- Check callers, errors, side effects, ordering and compatibility at affected boundaries.
- Preserve intentional behavior and separate functional changes from structural cleanup.
- Verify the originally failing case, nearby valid cases and relevant failure paths.
- Report pre-existing failures separately. Do not report unexecuted checks as passed.
- Keep a mitigation distinct from a permanent correction. A mitigation may reduce exposure while root cause or complete remediation remains open; state that boundary and the removal condition.
- For a production hotfix, preserve the smallest correction and applicable emergency release gates. Identify supported release lines, backport only the required behavior, and test each target line against its own contracts.
- Avoid combining the defect correction with cleanup or dependency changes that make review, rollback, or backport harder. Do not silently widen a hotfix into unrelated behavior changes.
- After verification, confirm the fix reaches the forward development line and record any branch or environment not covered. Propose recurrence prevention only when evidence supports the contributing mechanism.
