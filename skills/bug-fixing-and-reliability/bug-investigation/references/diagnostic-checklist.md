# Bug Investigation Checklist

Apply selectively to the task and available evidence.

## Evidence and checks

| Signal | Diagnostic use |
| --- | --- |
| Failing input | Minimize while retaining the symptom. |
| Stack trace | Trace the failing operation and caller; distinguish symptom from cause. |
| Logs and metrics | Correlate events using consistent time windows and identifiers. |
| Recent changes | Compare relevant revisions or configuration with a known baseline. |
| Intermittent failure | Record frequency, seed, timing, concurrency and environment where available. |

- Compare the affected and an unaffected revision or environment under equivalent inputs. Record runtime, dependency, configuration, locale, timezone, filesystem, and concurrency differences that are evidenced rather than guessed.
- Follow the smallest failing boundary from observable symptom through caller and dependency. Reduce an input only while the failure remains representative; a minimized case that removes the triggering ordering or state is misleading.
- Correlate logs, metrics, and traces by time window and request or operation identity where available. Preserve source timestamps and clock uncertainty; redact secrets and personal data before sharing evidence.
- If the defect cannot be reproduced, distinguish absent prerequisites or missing telemetry from evidence against a hypothesis. Report confidence and the next observation that would discriminate competing explanations.

## Hypothesis testing

- State what each hypothesis predicts and what would disprove it.
- Compare a failing case with a known good case using equivalent conditions.
- Record commands, versions, outputs and limitations. Avoid uncontrolled production experiments.
- If reproduction fails, distinguish missing prerequisites from evidence that contradicts the report.
- Stop when the available evidence supports a bounded diagnosis and further checks would require unavailable access, alter production state, or exceed the requested investigation. Hand off an evidence-backed correction proposal; do not implement it under investigation-only authorization.
