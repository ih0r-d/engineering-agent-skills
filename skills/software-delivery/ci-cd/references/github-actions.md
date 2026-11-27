# GitHub Actions workflow review

Load when `.github/workflows/` is part of the change or GitHub Actions behavior is under review. Check the repository's runner images and action versions because hosted behavior evolves.

- Trace `on`, job-level `if`, `needs`, matrices, reusable workflows, and concurrency for the event being reviewed. Jobs run independently unless dependencies or other constraints connect them; verify skipped jobs do not leave required checks permanently pending.
- Set the minimum `GITHUB_TOKEN` permissions at workflow or job scope. If permissions are declared, explicitly grant only the required scopes. Keep publishing and deployment permissions out of untrusted pull-request jobs.
- Treat event fields, branch names, titles, and pull-request code as untrusted input. Do not interpolate event text directly into shell source. A privileged workflow that checks out or executes contributor-controlled code can expose write credentials or secrets; inspect checkout ref, token permissions, cache writes, and secret availability together.
- Pin third-party actions according to repository policy, preferably to a reviewed full commit SHA where the policy requires immutable references. Keep an update process so pinning does not freeze vulnerable action versions.
- Use cache for reusable dependencies and artifacts for outputs passed to later jobs or retained for inspection. Key caches on the toolchain and lock inputs that determine their content; a cache hit is not proof the current source was built.
- For reusable workflows, check caller/callee permissions, inputs, secrets, outputs, and ref pinning. Composite actions package steps but do not create a job boundary or runner isolation.
- Keep environment approvals and protected deployment environments on the job that performs the external change. Verify `id-token: write` is scoped only to jobs that need OIDC federation.

Sources: [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [Security hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions), [Reusable workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows)
