# Contributing

Start with the toolkit's maintenance instructions. In the change description, name the task or defect, summarize the evidence, and report checks and limits. [AGENTS.md](AGENTS.md)

## Author and review Skills

- Give each Skill one recurring engineering responsibility that works across repositories. Check adjacent descriptions and document the boundary when their triggers could overlap.
- Write descriptions around observable inputs, user intent and tasks. Add a positive scenario and a plausible request that should route elsewhere. Keep examples and expected findings with the evaluations. [Evaluation procedure](evals/README.md)
- Every skill must pass the official Agent Skills specification gate. Use the flat `skills/<skill-id>/SKILL.md` layout and register the ID once in `catalog.json`. Use portable resources and standard frontmatter. Identify the client version and settings when reporting client-specific behavior. [Agent Skills specification](https://agentskills.io/specification), [Repository architecture](docs/architecture.md), [Client compatibility](docs/compatibility.md)
- Keep `SKILL.md` usable on its own for common tasks. Link topic-specific references with a reason to load each one. Reuse relevant evidence and link upstream details for specialist tools. Keep examples and domain rules in the narrowest applicable reference.
- Give the agent a practical way to confirm each finding. State the relevant input, expected behavior and observed impact. Separate defects and compatibility regressions from preferences, and prefer small changes that preserve intentional behavior and use existing tools.
- Default to read-only review. Make only explicitly requested changes within the task scope. Keep consumer instructions and build configuration intact unless the user explicitly requests their modification. Protect private code and credentials, and inspect commands for network or write effects before running them.

## Verify changes

Run `task ci` from the root with Python 3.11+, Task, uv, Bash, ShellCheck, actionlint, zizmor, and Lychee available. Add a focused regression test for changed behavior and exercise installation and removal for installer changes. Verify discovery and activation in the affected clients before making live compatibility claims. [Local validation](README.md#validation-and-evaluations), [Live evaluations](evals/README.md#run-live-evaluations)

Use the focused tasks during development.

```sh
task validate
task test
task eval:check
task syntax:check
task quality
task docs:check
```

`task validate:spec` runs the specification gate and its deterministic tests. uv installs the official reference validator at a full upstream commit SHA and resolves its dependencies from the checked-in lock. The first setup requires access to GitHub and PyPI or a populated uv cache. With dependencies cached, `UV_OFFLINE=1 task ci` runs the complete suite offline. GitHub Actions retains its Linux and macOS installer matrix, uses checksum-verified analyzer downloads, and checks the wrappers with ShellCheck. The shell evaluation fixture deliberately contains the expansion exercised by the tests. [Maintainer configuration](.scripts/spec/pyproject.toml), [Workflow](.github/workflows/validate.yml), [Dependabot configuration](.github/dependabot.yml)
