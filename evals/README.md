# Skill evaluations

[cases](cases/) contains one JSON array per catalog skill at `cases/<category-id>/<skill-id>.json`, plus [unrelated.json](cases/unrelated.json) for requests with no primary skill. Each case records the prompt, expected skill, skills to avoid, optional fixture, and observable acceptance criteria. The 148 cases cover both expected activations and plausible near misses.

## Offline validation

Run `task eval:check` to validate the case schema, catalog coverage, routing expectations, and fixture paths. The same task checks fixture behavior and exercises the deterministic pilot graders with known source. The Java grader check runs when a local Java 11+ JDK is available. [Evaluation cases and fixtures](cases/) · [Deterministic pilot graders](../.scripts/eval_pilot.py)

These checks establish fixture ground truth and package consistency. Claims about skill selection, reference use, authorization adherence, or engineering outcomes require observations from an actual agent session. Evaluation commands work offline and have no credential or model requirements.

## Manual skill verification

Use ordinary engineering work to verify behavior. Choose an actual task or a matching case, then record what the agent does under the project's conventions.

1. Identify the expected workflow, plausible near misses, and success criteria before starting. For routing questions, send the task prompt without naming the expected skill.
2. In the session, check whether the agent selects the expected workflow, uses task-relevant evidence, and respects edit and verification boundaries. Record which skills or references were read only when observable. Skill installation provides evidence of availability.
3. Verify the outcome independently. Run the appropriate project checks, inspect the diff and affected callers, and confirm read-only tasks left project files unchanged. Treat missing observations as `UNOBSERVED`.
4. Record the skill revision, client and model, task scope, checks, and outcome in private notes. Use observed behavior and verified artifacts to support conclusions.

| Case or engineering task | Expected workflow | Observed workflow and references | Scope and verification evidence | Result |
| --- | --- | --- | --- | --- |
| Task description and revision | Expected skill and mode | Observed activity or `UNOBSERVED` | Diff, commands, assertions, and effects | `PASS`, `FAIL`, or `UNOBSERVED` |

## Pilot scenarios

The pilot offers six reusable scenarios for optional manual comparisons. Planning lists the fixtures without launching a client. Use `--details` to get the exact prompt for a selected case.

```sh
task eval:plan
task eval:plan -- --scenario java-feature --details
```

For an A/B comparison, use independently authenticated agent sessions under your control. Create two disposable projects from the same fixture and use the same prompt, project instructions, client, model, tools, and permissions. Keep evaluation criteria and graders outside the agent workspaces.

- **A** uses the project without the toolkit.
- **B** uses the project with the complete catalog installed. From the toolkit checkout, run `python3 -B .scripts/skills.py install --agent codex --target /path/to/disposable-b --all --mode copy`. Use the installer option appropriate for the chosen client.
- Check for unrelated skills, plugins, hooks, and inherited instructions in both sessions. Record any differences that make the comparison inconclusive.
- Grade each outcome independently and record it in the table above. Treat a single pair as a smoke test.

The Java and Python graders in [eval_pilot.py](../.scripts/eval_pilot.py) accept an isolated command executor supplied by the caller. Run candidate code only in a disposable test environment without network or credentials. The automated checks use known fixture and test sources.

Keep private observations outside the repository. Any legacy local artifacts under `.eval-results/` remain ignored by Git.
