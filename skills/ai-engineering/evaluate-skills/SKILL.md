---
name: evaluate-skills
description: Design or run behavioral evaluations of agent skills. Use for routing, instruction following, task correctness, baseline comparisons, regression analysis, and evaluation rubrics.
---

# Evaluate Skills

## Workflow

1. Identify the skill revision, task contract, available clients, model settings, and observable outcomes.
2. Define representative positive, near-miss, unrelated, and adversarial or failure cases where relevant. Specify measurable acceptance criteria and forbidden side effects.
3. Establish fixture ground truth independently of the model. Load evaluation guidance when designing comparisons or scoring ambiguous results.
4. Compare fresh sessions with and without the skill under equivalent conditions. Record actual activation and resource reads only when observable; repeat inconsistent outcomes.
5. Score task correctness, safety, scope, and verification before comparing cost, tokens, tool calls, or latency.
6. Report case-level evidence, uncertainty, and actionable regressions. Recommend focused changes and rerun affected cases.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/evaluation-protocol.md) | Designing controlled comparisons or scoring criteria. |

## Constraints

- Keep scoring criteria outside agent-visible fixtures. Use synthetic data and isolated workspaces.
- Do not invoke paid providers, send private data, or execute external side effects without authorization.
- Do not confuse deterministic fixture checks with live model behavior or infer activation from output alone.
- Do not change rubrics to conceal failures or claim statistically reliable gains from inadequate samples.

## Expected Output

Report configurations, cases, criteria, observed results, comparison limits, and recommended next checks.
