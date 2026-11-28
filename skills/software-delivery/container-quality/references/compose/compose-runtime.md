# Docker Compose and runtime review

## Configuration and privileges

- Inspect file order, project directory, profile and environment precedence, including shell, `.env`, explicit env files, service `env_file` and `environment`. Interpolation occurs before merge on a per-file basis. Distinguish host interpolation from runtime expansion (for example, Compose `$$` for a literal dollar sign). Validate the actual command and merged service settings with safe values.
- Use quiet validation with local inputs, for example `docker compose --env-file fixture.env -f compose.yaml -f compose.dev.yaml config --quiet` after inspecting includes and file dependencies. Avoid dumping the full resolved configuration when it contains sensitive values. Config validation does not check runtime readiness.
- Trace runtime UID/GID and required writes, including bind mounts, named volumes and read-only roots. A non-root image can fail if a mounted directory hides the image's ownership. Check capabilities, privileged mode, host sockets and host ports against the actual need. An internal service can often use the Compose network without publishing a host port. Preserve a documented local-development port if that is the intended workflow.
- Document portable mount paths and lifecycle for local data. Test with fresh and existing state when changing volumes, permissions, initialization or migration. Treat `down -v` as destructive and exclude it from routine verification.

## Startup and shutdown

- Inspect the primary process and the effective entrypoint and command. Exec-form entrypoints, or a wrapper ending with `exec "$@"` when appropriate, let the application receive signals directly. Check reaping needs and realistic grace periods for a process tree, and stop through the actual supported runtime.
- Short `depends_on` orders startup and may still allow a dependency to be unready. If startup needs a ready dependency, check that the probe tests the right operation, exists in the runtime image and uses the intended user. Use a health-conditioned dependency where compatible and keep application retries for runtime outages. A one-shot dependency may need successful completion instead.
- Validate readiness and graceful shutdown in an authorized fixture with a unique project name and isolated ports and volumes. Inspect external volumes, explicit container names, host mounts and shared resources first. Preserve real development behavior such as live reload rather than applying production settings indiscriminately.

References. [Compose config](https://docs.docker.com/reference/cli/docker/compose/config/), [Interpolation](https://docs.docker.com/reference/compose-file/interpolation/), [Startup order](https://docs.docker.com/compose/how-tos/startup-order/)
