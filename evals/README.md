# Skill evaluations

[cases](cases/) stores one JSON array per catalog Skill plus [unrelated.json](cases/unrelated.json) for requests with no primary Skill. Each case records its prompt, expected primary Skill, nearby Skills to avoid, optional fixture, and observable acceptance criteria. Every non-null fixture refers to a directory under [fixtures](fixtures/). The examples mix defects with legitimate decisions.

## Deterministic checks

Run `task eval:check` from the repository root. The standard-library loader in `.scripts/evaluation_cases.py` loads all cases, selects a skill's positive cases, finds cases that avoid a named skill, and provides the unrelated subset. Validation checks per-skill files, schema, global IDs, catalog references, fixture paths, positive coverage, and near-miss coverage. The full offline suite exercises the Python, shell, Make, documentation, code review, and refactoring fixtures. These tests establish fixture ground truth. Routing, instruction following, and reference use are evaluated in live sessions.

Additional local checks are optional.

- With a JDK available, compile `evals/fixtures/java/Names.java` into a temporary directory. Running `Names` should reach the normalization assertion after the membership checks pass.
- With the Compose CLI installed, validate the local fixture with `docker compose -f evals/fixtures/container/compose.yaml config --quiet`. Config validation covers parsing and wiring. The fixture's startup argument depends on the API contract in its README. Keep it offline and avoid starting services.
- Inspect the release fixture as text. The workflow excerpt depicts a tag-triggered publish and its Maven command is for analysis only.

## Run live evaluations

1. Pick the changed Skill's positive case and the cases that name it under `avoid_skills`. Include the unrelated-request case for changes to descriptions or discovery. A null `skill` expects no toolkit Skill. A null `fixture` means the prompt can stand on its own.
2. Create a fresh disposable project per run and copy only the case's fixture. Keep case files and scoring criteria outside the project. Use synthetic inputs and keep publishing, deployment, credentials, and real registries unavailable.
3. Install all skills from the revision under test. Check discovery from the project root, then send the prompt without a skill name in a fresh session. Record the primary skill, any observable supporting skills, and any named skill that should have been avoided. For positive cases, run a separate fresh session with explicit invocation to measure whether the agent follows the skill.
4. Grade the evidence, proposed or actual change scope, and the verification result. Compare the tree before and after read-only runs and mark unauthorized edits or external actions as failures. Record loaded reference paths and token counts when the client exposes them. Check whether reference reads served the task and flag unrelated reads. Use `UNOBSERVED` for client signals you cannot inspect.
5. Repeat against a known baseline revision with the same prompts, fixtures, client, model, permissions, and tool access. Change only the installed Skill revision. Use fresh sessions for each run, compare the per-case outcomes, and repeat inconsistent results before calling a regression.

## Record results

Keep the run record outside consumer repositories. Record the baseline and candidate Git revisions, agent and model versions, and relevant settings once per batch. Use one row per case, revision and invocation mode.

| Case and revision | Mode | Selection and evidence | Findings and verification | Change scope and safety | Reference paths and tokens | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Case ID and Git revision | Automatic or explicit | Skill or `UNOBSERVED`, with trace if available | Reproduced behavior and criterion results | File changes and side effects | Paths and counts if exposed | `PASS`, `FAIL`, or `UNOBSERVED` |

Live evaluations are manual and separate from CI. Use an existing authorized client session when available.
