# Pipeline Checklist

| Concern | Check |
| --- | --- |
| Triggers | Branch and path filters, fork trust, event payloads, required checks. |
| Dependencies | Explicit job prerequisites, failure propagation, conditional execution. |
| Permissions | Least privilege, trusted inputs, secret availability, pinned third-party actions. |
| Cache | Include tool and dependency identity; do not treat cache hits as verification. |
| Artifacts | Tie build outputs and checks to the same revision and artifact identity. |
| Concurrency | Cancel only superseded work when safe; protect release and deployment jobs. |
| Performance | Measure critical path and queue time before optimizing. |

## Gotchas

- A path filter can leave a required check pending; verify provider behavior before changing triggers.
- A passing local linter does not establish hosted execution success.
- Avoid interpolating untrusted event values directly into shell source.
- Keep trusted publishing steps separate from untrusted pull request execution.

## Official guidance

- [GitHub Actions security hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)
