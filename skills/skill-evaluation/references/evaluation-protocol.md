# Evaluation Protocol

| Dimension | Evidence |
| --- | --- |
| Routing | Observed primary skill and relevant supporting resources. |
| Correctness | Fixture ground truth and independently checked outputs. |
| Authorization | Before/after workspace and tool side effects. |
| Efficiency | Comparable token, tool call, time, or cost measurements where available. |

Use identical tasks, fixture revisions, model settings, permissions and tool access for controlled comparisons. Vary the skill condition only, or use explicitly defined factorial conditions when testing optimizers. Separate discovery from explicit invocation. Mark missing signals UNOBSERVED and repeat unstable results. Do not expose hidden scoring criteria to evaluated agents.

## Gotchas

- A passing fixture test does not evaluate the agent.
- A shorter answer can omit required evidence; score correctness first.
- A single run cannot establish a stable regression or improvement.
- Model-graded criteria need calibration against independently checkable evidence.

## Official guidance

- [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills)
