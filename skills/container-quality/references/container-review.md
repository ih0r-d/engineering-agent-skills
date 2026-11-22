# Container review reference

- Image provenance, unnecessary packages, layer/cache efficiency, reproducible versions and multi-stage builds when useful.
- User/group permissions, writable directories, signal propagation, process lifecycle, health checks and correct shutdown.
- Secrets: no credentials in layers, environment dumps, build args or repository files; prefer supported secret mechanisms.
- Compose: dependency conditions, networks, named volumes, resource limits, environment defaults, and correct `config` validation.
- Avoid exposing ports unnecessarily or assuming privileged execution; respect service-specific platform requirements.
- Prefer minimal edits over fashion-driven rewrites. Distinguish development and production needs.
