# Skill evaluations

[cases.json](cases.json) records prompts, expected routing and observable acceptance criteria. Each non-null fixture refers to a directory under [fixtures](fixtures/). The examples intentionally mix defects with legitimate decisions.

## Deterministic checks

Run `python3 -B -m unittest discover -s tests -v` from the repository root. The suite verifies case IDs, catalog coverage and fixture paths. It reproduces the Python default-state leak, shell argument splitting, Make recipe directory behavior when Make is available, and the actual CLI outputs for the documentation example. These tests establish fixture ground truth.

Additional local checks are optional.

- With a JDK available, compile `evals/fixtures/java/Names.java` into a temporary directory. Running `Names` should reach the normalization assertion after the membership checks pass.
- With the Compose CLI installed, validate the local fixture with `docker compose -f evals/fixtures/container/compose.yaml config --quiet`. Config validation covers parsing and wiring. The fixture's startup argument depends on the API contract in its README. Keep it offline and avoid starting services.
- Inspect the release fixture as text. The workflow excerpt depicts a tag-triggered publish and its Maven command is for analysis only.

## Optional agent evaluation

1. Create a fresh disposable project per case. Copy only that case's fixture, or use a harmless synthetic excerpt for a case with a null fixture. Inspect it before granting tool access. Keep the case JSON and expected answers outside the agent's project.
2. Install all seven skills into the project for the agent under test. Confirm discovery from the project root. Start a fresh session and send the case prompt without a Skill name to measure automatic routing. Use the client's skill trace or loaded paths when available. Mark activation unknown if selection cannot be observed.
3. In a separate fresh session, explicitly invoke the expected Skill for positive cases to evaluate following the workflow independently of routing. For a null expected Skill, evaluate only automatic routing.
4. Grade each criterion against actual steps and output. Require the finding's evidence and smallest fix, preserve intentional behavior, and compare the project before and after review-only requests. Record unauthorized edits or external actions as failures. Keep publishing, deployments, secrets and registries unavailable in the release fixture.
5. Record the client and model versions, selection evidence, findings, verification and failures. Repeat borderline routing cases in fresh sessions and compare with a run without the skills if attribution matters.

Model-based runs are separate from CI and can require service access. Use synthetic or approved inputs and avoid supplying credentials to evaluation projects.
