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

## Hypothesis testing

- State what each hypothesis predicts and what would disprove it.
- Compare a failing case with a known good case using equivalent conditions.
- Record commands, versions, outputs and limitations. Avoid uncontrolled production experiments.
- If reproduction fails, distinguish missing prerequisites from evidence that contradicts the report.
