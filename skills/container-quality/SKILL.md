---
name: container-quality
description: Review or fix Dockerfiles, build contexts, container runtime settings, and Docker Compose projects. Use to diagnose image reproducibility, secret handling, startup, health, shutdown, or local development behavior.
---

# Container Quality

1. Identify the actual Dockerfile, context root, target stage and platform, Compose file order, profiles and production or development contract. Start with changed services or stages and trace their build inputs and runtime dependencies. Inventory other images only for a full audit.
2. Read [image builds](references/container-review.md) for Dockerfile, context and size issues, and [Compose and runtime](references/compose-runtime.md) for lifecycle, storage, privileges and local workflows.
3. Review without changing files, building images or starting services. For verification, prefer configured lint and quiet Compose validation with the expected files and safe fixture values. Inspect pulls, network calls, credentials, volumes and daemon effects before running builds or services. Use an isolated project for authorized runtime probes.
4. In fix mode, change the smallest affected stage or service setting. Preserve entrypoint arguments, mounted-data and permission contracts, signal behavior, ports and supported platforms. Establish correctness and security before considering image-size or cache optimizations.
5. Report severity, file and line, triggering context or runtime configuration, impact, a small fix and the verification outcome. Keep complete non-sensitive logs locally. Keep resolved credential values out of logs and reports.

Use the release workflow for promotion, signing and publication. Base-image pinning and runtime privileges should reflect the project's update process and actual workload.
