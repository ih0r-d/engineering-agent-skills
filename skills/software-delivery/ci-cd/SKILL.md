---
name: ci-cd
description: Design, review, or repair continuous integration and delivery pipelines. Use for workflow triggers, job dependencies, quality gates, caching, permissions, and pipeline reliability.
---

# CI/CD

## Workflow

1. Identify the actual CI provider, workflow trigger, trust boundary, runner, job graph, and required checks.
2. Trace a representative change through validation, artifact generation, and delivery gates. Inspect existing logs and configuration before proposing edits.
3. Identify redundant jobs, incorrect dependencies, unsafe permissions, cache assumptions, and missing failure propagation. Separate measured delays from hypotheses.
4. Load the pipeline reference when assessing workflow security, artifacts, or optimization.
5. Propose the smallest compatible change. For authorized edits, use existing workflow validation and safe local checks; inspect hosted results only when available.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/pipeline-checklist.md) | Task-specific decisions require additional guidance. |
| [GitHub Actions](references/github-actions.md) | `.github/workflows/` or GitHub-hosted workflow behavior is in scope. |
| [GitLab CI/CD](references/gitlab-ci.md) | `.gitlab-ci.yml`, GitLab runners, or GitLab environment behavior is in scope. |
| [Jenkins Pipeline](references/jenkins-pipeline.md) | `Jenkinsfile`, shared libraries, Jenkins agents, or credential binding is in scope. |

## Constraints

- Review without edits unless authorized. Do not trigger remote workflows, publish artifacts, or alter branch protection without explicit authorization.
- Never expose secrets to untrusted code or weaken required checks to improve speed.
- Preserve supported triggers, required check names, and artifact identity unless a change is approved.
- Leave build-tool internals to build automation, release readiness to release engineering, and runtime rollout to deployment workflows.
- Reuse unchanged evidence; do not scan unrelated pipelines.

## Expected Output

Report the affected job, trigger, evidence, impact, smallest correction, and validation result. Separate local checks from hosted execution and unverified performance estimates.
