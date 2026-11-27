# Make and Task review

## Make

- Determine GNU Make or another implementation, the default target and entry directory. File targets need prerequisites that affect outputs. Phony targets represent actions. For GNU Make, an order-only prerequisite such as an output directory can establish ordering without rebuilding artifacts on each directory timestamp change.
- Check automatic variables (`$@`, `$<`) and escaped shell dollars (`$$`). Most recipes run each logical line in its own shell. A line containing only `cd app` leaves the next recipe line in the original directory. Use a checked `cd app && command` or an existing working-directory mechanism.
- Verify required failures reach Make. Review ignored errors via recipe prefixes, shell sequencing, and parallel work on shared paths. Establish explicit dependencies for `make -j`; ordering in a serial run can hide a race.
- Review included Makefiles, `$(shell ...)` and recursive recipe lines before `make -n`. Some commands still execute during expansion, include remakes or recursive recipe handling. Verify with a harmless named goal in an isolated fixture.

## Task (Taskfile)

- Check version and schema, includes and their directories, task-level `dir`, dotenv files and variable precedence. Inspect templated arguments and dynamic `sh:` variables for effects, including during list or dry runs. Confirm whether a particular command invokes Bash explicitly and whether any external utility is installed on every supported platform.
- Multiple `deps` can run concurrently. When generation must finish before consumption, express the edge in the dependency graph or invoke tasks serially through `cmds`. Deleting the dependency and relying on array order leaves the race intact.
- Inspect `sources`, `generates`, fingerprint method and `status`. Verify skipped runs only when outputs are valid, and that deletion of an output or change of an input triggers the expected work. Use `preconditions` for prerequisites that should fail the invocation; an up-to-date status check serves a different purpose.
- After inspecting dynamic variables and includes, select the project's appropriate `task --list`, `task --dry goal` or a safe execution. Review `ignore_error`, deferred cleanup and subtask failure propagation. Use controlled fixtures for platform branches and user-supplied arguments.

Prefer a reproduced stale output, wrong directory or lost status over a claim based on style. Test baseline and fix with the same input and runner.

References. [GNU Make manual](https://www.gnu.org/software/make/manual/html_node/), [Task guide](https://taskfile.dev/docs/guide/), [Task CLI](https://taskfile.dev/docs/reference/cli/)
