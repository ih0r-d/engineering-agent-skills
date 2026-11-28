---
name: manage-ci-cd
description: Design, review, or repair continuous integration and delivery pipelines. Use for workflow triggers, job dependencies, quality gates, caching, permissions, and pipeline reliability.
---

# Manage CI/CD

## Workflow

1. Identify the workflow trigger, trust boundary, job graph, and required checks. Follow the user's provider requirements first, then inspect the active pipeline files, runner settings, and pinned actions, plugins, or provider versions where available.
2. Trace a representative change through validation, artifact generation, and delivery gates. Inspect existing logs and configuration before proposing edits.
3. Identify redundant jobs, incorrect dependencies, unsafe permissions, cache assumptions, and missing failure propagation. Separate measured delays from hypotheses.
4. Load the pipeline checklist for security, artifact, or optimization decisions that need it. Select provider guidance only when the provider and relevant behavior are evidenced. Use generic pipeline checks and project conventions for unsupported or undetermined providers.
5. Propose the smallest compatible change. For authorized edits, use existing workflow validation and safe local checks; inspect hosted results only when available.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/pipeline-checklist.md) | Task-specific decisions require additional guidance. |
| [GitHub Actions](references/github-actions/github-actions.md) | `.github/workflows/` or GitHub-hosted workflow behavior is in scope. |
| [GitLab CI/CD](references/gitlab-ci/gitlab-ci.md) | `.gitlab-ci.yml`, GitLab runners, or GitLab environment behavior is in scope. |
| [Jenkins Pipeline](references/jenkins/jenkins-pipeline.md) | `Jenkinsfile`, shared libraries, Jenkins agents, or credential binding is in scope. |

## Constraints

- Keep design proposals and reviews read-only. Edit local pipeline files only when requested. Triggering remote workflows, publishing artifacts, and changing hosted settings or branch protection require explicit authorization.
- Never expose secrets to untrusted code or weaken required checks to improve speed.
- Preserve supported triggers, required check names, and artifact identity unless a change is approved.
- Leave build-tool internals to build automation, release readiness to release engineering, and runtime rollout to deployment workflows.
- Reuse unchanged evidence; do not scan unrelated pipelines.

## Expected Output

Report the affected job, trigger, evidence, impact, smallest correction, and validation result. Separate local checks from hosted execution and unverified performance estimates.
