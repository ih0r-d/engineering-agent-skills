# Contributing

Start with the toolkit's maintenance instructions. In the change description, name the task or defect, summarize the evidence, and report checks and limits. [AGENTS.md](AGENTS.md)

## Author and review Skills

- Follow the [canonical Skill Authoring Standard](docs/skill-authoring.md) for format requirements and repository recommendations. It covers scope, descriptions, references, scripts, size targets, and evaluation.
- Keep `SKILL.md` sufficient for common tasks; load linked specialist references only when their stated condition applies. Register each skill in one category and use portable resources. [Repository architecture](docs/architecture.md), [Client compatibility](docs/compatibility.md)
- Give the agent a practical way to confirm each finding. State the relevant input, expected behavior and observed impact. Separate defects and compatibility regressions from preferences, and prefer small changes that preserve intentional behavior and use existing tools.
- Default to read-only review. Make only explicitly requested changes within the task scope. Keep consumer instructions and build configuration intact unless the user explicitly requests their modification. Protect private code and credentials, and inspect commands for network or write effects before running them.
- Use [templates/SKILL.md](templates/SKILL.md) as an adaptable starting point. Preserve existing behavior during formatting-only changes.

## Verify changes

Run `task ci` from the root with Python 3.11+, Task, uv, Bash, ShellCheck, actionlint, zizmor, and Lychee available. Add a focused regression test for changed behavior and exercise installation and removal for installer changes. Verify discovery and activation in the affected clients before making live compatibility claims. [Local validation](README.md#quality-assurance-and-evaluation), [Live evaluations](evals/README.md#run-live-evaluations)

Use the focused tasks during development.

```sh
task validate
task test
task eval:check
task syntax:check
task quality
task docs:generate
task docs:check
```

`task docs:generate` updates the marked README catalog from `catalog.json` and the parsed skill frontmatter. `task docs:check` fails when that generated block is stale, then checks local Markdown links and anchors.

`task validate:spec` runs the specification gate and its deterministic tests. uv installs the official reference validator at a full upstream commit SHA and resolves its dependencies from the checked-in lock. The first setup requires access to GitHub and PyPI or a populated uv cache. With dependencies cached, `UV_OFFLINE=1 task ci` runs the complete suite offline. GitHub Actions retains its Linux and macOS installer matrix, uses checksum-verified analyzer downloads, and checks the wrappers with ShellCheck. The shell evaluation fixture deliberately contains the expansion exercised by the tests. [Maintainer configuration](.scripts/spec/pyproject.toml), [Workflow](.github/workflows/validate.yml), [Dependabot configuration](.github/dependabot.yml)
