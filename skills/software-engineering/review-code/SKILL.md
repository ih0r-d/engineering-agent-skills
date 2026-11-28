---
name: review-code
description: Review a pull request, patch, or scoped code change for actionable defects, regressions, and missing verification. Use for a findings-first review of proposed or existing changes.
---

# Review Code

## Workflow

1. Identify the intended change, the baseline or diff, and the review boundary. Read the applicable specification, acceptance criteria, project coding standards, and relevant callers and tests. For a scoped review without a diff, state which implementation and expectations you used.
2. Follow explicit user technology requirements first. Inspect the changed source, manifests, dependencies, and configuration for the applicable language, framework, and version. Load only references that match the evidence and review concern. Use the generic workflow and project conventions where specialized guidance or evidence is missing.
3. Trace representative inputs and failure paths. Check specification compliance, correctness, compatibility, and relevant security and reliability boundaries. Include state ownership, concurrent access, resource cleanup, and partial failure where they affect behavior.
4. Assess applicable coding standards and maintainability. Check potential code smells against actual responsibilities, duplication of rules, control flow, and change impact. Use the review criteria reference when a finding depends on these distinctions or on ambiguous specification evidence.
5. Check whether existing tests would detect the observed failure or protect the changed contract. Prefer a focused, safe reproduction with the project's existing tools when it resolves a material uncertainty.
6. Distinguish reproduced behavior, findings established from source and contracts, and risks that still need evidence. Treat missing tests as actionable when they leave a concrete behavior at risk.

## Reference selection

| Reference | Load when |
| --- | --- |
| [Review criteria](references/review-criteria.md) | Evaluating specification compliance, coding standards, a code smell, or long-term change costs. |
| [Java correctness and compatibility](references/java/quality-rubric.md) | Java language behavior, JavaDoc, concurrency, or caller compatibility affects the change. |
| [Java module and framework boundaries](references/java/boundaries.md) | Generated code, framework proxies, class loading, or module boundaries affect a finding. |
| [Java static analysis](references/java/static-analysis.md) | A Java analyzer result or project gate needs verification. |
| [Java minimal changes](references/java/anti-overengineering.md) | Judging duplication, cohesion, or a proposed cleanup in Java. |
| [Python correctness and compatibility](references/python/quality-rubric.md) | A Python change affects object ownership, exceptions, imports, or public contracts. |
| [FastAPI review](references/fastapi/review.md) | A FastAPI change affects request dependencies, resource ownership, or blocking operations. |
| [Quarkus review](references/quarkus/review.md) | A Quarkus change affects REST dispatch, CDI scope, or configuration phase. |
| [Shell behavior and portability](references/shell/shell-review.md) | Bash or POSIX sh argument expansion, exit status, cleanup, or interpreter compatibility is in scope. |

## Constraints

- Review without editing. A finding or proposed fix does not authorize remediation. Use the implementation workflow only when edits are explicitly requested.
- Keep architecture assessments, dedicated security audits, incident investigation, and standalone formatting in their own workflows.
- Report maintainability issues when they have a concrete cost or make a defect more likely.
- Keep stylistic preferences subordinate to defects.

## Optional delegation

When the client provides subagents and the task permits delegation, split independent read-only work by component or review concern. Give each reviewer the relevant change, governing requirements, limits on file and tool access, and a request for file-level evidence and verification. Keep shared contracts and cross-component findings with the primary reviewer. Recheck claims against the diff and governing requirements, reconcile disagreements, and deduplicate before reporting. Use the same review steps sequentially when delegation is unavailable, unauthorized, or adds unnecessary coordination.

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
