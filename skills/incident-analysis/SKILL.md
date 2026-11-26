---
name: incident-analysis
description: Analyze an operational incident and prepare an evidence-based incident report or blameless postmortem. Use for impact, incident timelines, response effectiveness, recovery, and follow-up actions.
---

# Incident Analysis

## Workflow

1. Establish incident scope, affected consumers, known impact, status, and available evidence.
2. Build a timeline from logs, alerts, changes, and response records with consistent time zones; mark uncertain times.
3. Identify detection, escalation, mitigation, recovery, and verification milestones.
4. Examine failure mechanisms and contributing factors; use root-cause analysis when deeper causal evaluation is needed.
5. Assess response effectiveness, observability gaps, and residual risks without assigning personal blame.
6. Propose prioritized follow-up actions with suggested ownership, verification criteria, and unresolved questions.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed checklist](references/postmortem-checklist.md) | Additional guidance is needed for incident impact, timelines, response review, and postmortem follow-up. |

## Constraints

- Do not invent incident times, impact numbers, owners, or recovery status.
- Do not declare recovery without evidence; distinguish mitigation from verified recovery.
- Do not perform production operations, publish reports, or disclose sensitive data without authorization.
- Keep incident analysis separate from live operational command execution.

## Expected Output

Provide an incident summary, impact, evidence-backed timeline, response and recovery assessment, causal findings or unknowns, and actionable follow-up items.
