---
name: container-quality
description: Review or fix Dockerfiles, build contexts, container runtime settings, and Docker Compose projects. Use to diagnose image reproducibility, secret handling, startup, health, shutdown, or local development behavior.
---

# Container Quality

## Operating Modes

| Mode | Responsibility |
| --- | --- |
| Review | Inspect and report findings without changing files, building images or starting services. |
| Fix | Change the smallest affected stage or service setting when authorized. |
| Verification | Prefer configured lint and quiet Compose validation with the expected files and safe fixture values. |

## Workflow

1. Identify the actual Dockerfile, context root, target stage and platform, Compose file order, profiles and production or development contract.
2. Start with changed services or stages and trace their build inputs and runtime dependencies. Inventory other images only for a full audit.
3. Load relevant references according to the task.
4. Inspect pulls, network calls, credentials, volumes and daemon effects before running builds or services.
5. Perform applicable checks or authorized fixes within the selected operating mode. Use an isolated project for authorized runtime probes.
6. Establish correctness and security before considering image-size or cache optimizations.
7. Keep complete non-sensitive logs locally.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Image builds](references/container-review.md) | Reviewing Dockerfiles, build contexts or image-size issues. |
| [Compose and runtime](references/compose-runtime.md) | Investigating lifecycle, storage, privileges or local development workflows. |
| [Cache and platform builds](references/cache-and-platforms.md) | Investigating cache behavior, multi-platform output, or reproducibility. |

## Constraints

- Preserve entrypoint arguments, mounted-data and permission contracts, signal behavior, ports and supported platforms.
- Keep resolved credential values out of logs and reports.
- Base-image pinning and runtime privileges should reflect the project's update process and actual workload.
- Use the release workflow for promotion, signing and publication.

## Expected Output

For each finding, report:

- Severity and file location.
- Triggering context or runtime configuration.
- Practical impact.
- Smallest applicable fix.
- Verification outcome.
