---
name: code-review
description: Review a pull request, patch, or scoped code change for actionable defects, regressions, and missing verification. Use for a findings-first review of proposed or existing changes.
---

# Code Review

## Workflow

1. Identify the intended change, the baseline or diff, and the review boundary. Start with changed behavior, then inspect the surrounding implementation, callers, contracts, and tests needed to judge its effect. For a scoped review without a diff, state which implementation and expectations you used.
2. Trace representative inputs and failure paths through the changed code. Look for correctness, compatibility, security, or reliability regressions where the change reaches those boundaries.
3. Check state ownership, concurrent access, resource cleanup, and partial failures when relevant. Use available language-specific guidance for semantics and idioms that affect the finding.
4. Check whether existing tests would detect the observed failure or protect the changed contract. Prefer a focused, safe reproduction with the project's existing tools when it resolves a material uncertainty.
5. Distinguish reproduced behavior, findings established from source and contracts, and risks that still need evidence. Treat missing tests as actionable when they leave a concrete behavior at risk.

## Constraints

- Review without editing. Apply fixes only when the user explicitly authorizes them.
- Keep architecture assessments, dedicated security audits, incident investigation, formatting, and language standards in their own workflows.
- Report maintainability issues when they have a concrete cost or make a defect more likely.
- Keep stylistic preferences subordinate to defects.

## Expected Output

Lead with actionable findings ordered by impact.

For each finding, report:

- Severity.
- File and line when available.
- Triggering condition.
- Affected caller or outcome.
- Practical correction or verification step.

Group duplicate symptoms by cause.

If there are no actionable findings, say so and identify any limits on the review. Report only checks actually run as executed.