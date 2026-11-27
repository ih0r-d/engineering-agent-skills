---
name: bug-investigation
description: Investigate reproducible or intermittent software defects using symptoms, logs, tests, and execution traces. Use to isolate failing behavior and identify evidence before proposing a fix.
---

# Bug Investigation

## Workflow

1. Establish expected and observed behavior, affected versions, inputs, environment, and reproduction steps.
2. Inspect existing tests, logs, recent changes, and relevant execution paths; redact sensitive data.
3. Reproduce safely with the smallest representative input where possible. Separate pre-existing failures from the reported defect.
4. Form competing hypotheses and choose focused checks that distinguish them. Change one relevant variable at a time.
5. Trace the failing boundary to callers and dependencies. Use language-specific guidance where it supplies evidence.
6. Record supported causes, rejected hypotheses, missing evidence, and a minimal regression-test proposal.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed checklist](references/diagnostic-checklist.md) | Additional guidance is needed for defect reproduction, diagnostic evidence, hypothesis testing, and fault isolation. |

## Constraints

- Default to investigation without implementation edits; use disposable fixtures for diagnostic probes.
- Do not treat correlation, a stack frame, or a passing test as proof of cause.
- Do not restart services, modify production state, or collect sensitive data without authorization.
- Hand off authorized corrections to bug-fixing and systemic causal analysis to root-cause-analysis when available.

## Expected Output

Report expected and observed behavior, reproduction commands and results, affected scope, evidence-backed hypotheses, confidence, and next diagnostic or corrective steps.
