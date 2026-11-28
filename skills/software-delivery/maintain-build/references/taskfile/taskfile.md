# Taskfile dependency and status behavior

Load when a `Taskfile.yml`, included Taskfile, task dependency, or `task` invocation is involved. Confirm the Task version and schema; task options and template behavior are version-sensitive.

- Inspect `version`, includes and include directories, task `dir`, dotenv loading, and variable precedence before evaluating a command. Template expressions can expand user input into shell commands.
- Multiple `deps` may run concurrently. Use dependency edges for required graph ordering; do not rely on declaration order. Use `cmds` sequencing only when the operations are intentionally serial within one task.
- Distinguish `preconditions` from freshness checks. Preconditions reject an invocation when a requirement is absent; `status` determines whether a task is considered up to date. Check `sources`, `generates`, fingerprints, and status together against a clean, unchanged, and changed-input run.
- Inspect shell selection, argument quoting, environment variables, and cross-platform utilities. A Task command can use a shell or binary that is unavailable on another supported platform.
- Review `ignore_error`, deferred commands, and subtask failure propagation. Confirm that cleanup does not replace the primary failure status and that background work is awaited.
- After inspecting dynamic templates and included files, prefer the project's configured `task --list`, `task --dry <task>`, or safe fixture invocation. Dry-run is not a sandbox if template expansion or included configuration executes code.

Sources: [Task guide](https://taskfile.dev/docs/guide/), [Taskfile schema](https://taskfile.dev/docs/reference/schema), [Task CLI](https://taskfile.dev/docs/reference/cli)
