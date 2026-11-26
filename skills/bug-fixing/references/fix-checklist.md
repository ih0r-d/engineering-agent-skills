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
