---
name: container-quality
description: Review or improve Dockerfiles and Compose configurations for safe images, reproducible builds, lifecycle correctness, and local developer experience.
---

# Container Quality

1. Identify Dockerfile, Compose, build context, target platform, runtime privileges, environment variables, and deployment expectations.
2. Follow [container-review.md](references/container-review.md) for relevant image and Compose checks.
3. Review-only mode: never build or start services unexpectedly, access secrets, or publish images.
4. Run locally available `docker compose config` or Dockerfile linting only when safe, with careful attention to variable substitution and environment files.
5. Apply requested minimal fixes while preserving volume semantics, health checks, ports, networking, entrypoints and user-visible behavior.
6. Report concrete evidence and available verification; don't auto-commit, push images or deploy.
