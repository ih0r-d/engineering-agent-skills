# GitLab CI/CD pipeline review

Load when `.gitlab-ci.yml`, included GitLab templates, or GitLab runner behavior is in scope. Confirm GitLab and Runner versions and whether the project is GitLab.com or self-managed before relying on tier- or version-specific features.

- Trace `workflow:rules`, job `rules`, stages, `needs`, `include`, and `extends` to determine which jobs exist for the actual event. `rules` are evaluated in order; inspect the first matching rule and whether a job can be omitted from a required dependency.
- Treat `needs` as both scheduling and artifact-flow configuration. Verify the exact producer jobs a consumer downloads from; a DAG edge does not guarantee every artifact from earlier stages is present.
- Use cache for reusable dependencies and artifacts for build/test outputs that downstream jobs consume. Check cache keys, protected/non-protected branch separation, artifact expiry, and upload/download paths. Never rely on a cache as the only copy of a release artifact.
- Check runner tags, executor, protected variables, protected branches, and environment approvals. A masked variable is not a security boundary against code that can print or exfiltrate it; keep untrusted merge-request jobs away from publishing credentials and privileged runners.
- Review `interruptible` and auto-cancel behavior against non-idempotent jobs. Cancellation is appropriate for superseded validation only when the job cannot leave external effects or strand required artifacts.
- For deployment jobs, bind environment identity and protection to the actual target, restrict credentials, and preserve the artifact digest from build through deploy.

Sources: [GitLab CI/CD YAML reference](https://docs.gitlab.com/ci/yaml/), [Caching](https://docs.gitlab.com/ci/caching/), [Job artifacts](https://docs.gitlab.com/ci/jobs/job_artifacts/), [Protected environments](https://docs.gitlab.com/ci/environments/protected_environments/)
