# Incident Analysis Checklist

Apply selectively to the task and available evidence.

## Incident record

| Area | Capture |
| --- | --- |
| Impact | Affected services, consumers, duration and measured effects. |
| Timeline | Detection, escalation, mitigation, recovery and verification with sources. |
| Response | Actions taken, rationale, observed results and coordination gaps. |
| Causes | Supported mechanisms, contributing factors and unknowns. |
| Follow-up | Prevention, detection, mitigation and recovery improvements. |

Classify severity and impact using the organization's incident policy rather than inventing a universal scale. Preserve evidence links, data sources, clock assumptions, and whether each statement is observed, estimated, or hypothesized. Mark unknown periods in the timeline instead of filling them with inferred events.

## Postmortem quality

- Use neutral language focused on conditions, decisions and system controls.
- Separate observed facts from estimates and hypotheses.
- Record missing evidence and avoid reconstructing unsupported events.
- Give actions clear acceptance criteria, suggested owners and priority; do not imply assignments are approved.
- Verify recovery against service and consumer signals, not only the absence of alerts.
- Separate the triggering event, technical mechanism, contributing conditions, and response gaps. A postmortem need not force one root cause when multiple conditions contributed or evidence remains incomplete.
- Use Five Whys or fault-tree analysis only when it clarifies causal relationships. Neither method proves causality by itself; keep alternative explanations and evidence visible.
- Track corrective work across prevention, detection, mitigation, and recovery. Prefer actions that change a verified system control, and define how completion will be checked.
