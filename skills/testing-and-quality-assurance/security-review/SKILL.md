---
name: security-review
description: Review software changes, architecture boundaries, and configuration for security vulnerabilities and exposure risks. Use for authorized defensive assessments, access control, sensitive data handling, and evidence-based remediation advice.
---

# Security Review

## Workflow

1. Establish the authorized review scope, assets, trust boundaries, actors, and security requirements.
2. Inspect relevant source, configuration, dependencies, and data flows for reachable security weaknesses.
3. Trace untrusted input, identity, authorization, sensitive data, and privileged operations to observable outcomes.
4. Use existing approved static or dependency checks and safe local reproductions when they establish evidence; verify tool findings against actual reachability and configuration.
5. Prioritize findings by demonstrated impact, exploitability conditions, exposure, and confidence. Separate confirmed defects from unverified risks.
6. Recommend minimal mitigations and defensive regression checks; apply changes only when explicitly authorized.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/security-checklist.md) | Additional guidance on test or review decisions is needed. |

When producing a security review report, use [the report template](assets/security-report-template.md). Record only evidence-backed findings and state scope limitations.

## Constraints

- Default to read-only defensive assessment within the authorized scope.
- Do not access real secrets, probe external targets, or run destructive tests without specific authorization.
- Never expose credentials or sensitive data in reports.
- Keep general change review and broad architecture assessment in their respective workflows.

## Expected Output

Lead with prioritized findings, affected locations, evidence, prerequisites, impact, confidence, mitigation, and verification limits.
