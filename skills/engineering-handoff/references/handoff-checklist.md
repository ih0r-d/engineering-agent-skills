# Engineering Handoff Checklist

| Concern | Include |
| --- | --- |
| State | Branch, revision, clean or dirty tree when verified. |
| Changes | Outcome, affected paths, relevant contracts. |
| Decisions | Rationale, alternatives, and unresolved choices. |
| Checks | Commands, actual outcomes, skipped or unavailable checks. |
| Recovery | Partial operations, blockers, and safe next steps. |

## Gotchas

- A local commit does not imply a merged pull request or successful hosted CI.
- Passing fixture checks do not imply live agent behavior was evaluated.
- Report dirty files and partial operations rather than suggesting destructive cleanup.
- Link non-sensitive evidence instead of embedding complete logs.
