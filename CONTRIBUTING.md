# Contributing

Start with the toolkit's maintenance instructions. In the change description, name the task or defect, summarize the evidence, and report checks and limits. [AGENTS.md](AGENTS.md)

## Author and review Skills

- Give each Skill one recurring engineering responsibility that works across repositories. Check adjacent descriptions and document the boundary when their triggers could overlap.
- Write descriptions around observable inputs, user intent and tasks. Add a positive scenario and a plausible request that should route elsewhere. Keep examples and expected findings with the evaluations. [Evaluation procedure](evals/README.md)
- Follow the Agent Skills specification and the catalog's frontmatter conventions. Keep shared Skill definitions usable in Codex and Claude Code. Identify the client version and settings when documenting client-specific behavior or limits. [Agent Skills specification](https://agentskills.io/specification), [Supported clients](README.md#supported-agents)
- Keep `SKILL.md` usable on its own for common tasks. Link topic-specific references with a reason to load each one. Reuse relevant evidence and link upstream details for specialist tools. Keep examples and domain rules in the narrowest applicable reference.
- Give the agent a practical way to confirm each finding. State the relevant input, expected behavior and observed impact. Separate defects and compatibility regressions from preferences, and prefer small changes that preserve intentional behavior and use existing tools.
- Default to read-only review. Make only explicitly requested changes within the task scope. Keep consumer instructions and build configuration intact unless the user explicitly requests their modification. Protect private code and credentials, and inspect commands for network or write effects before running them.

## Verify changes

Run the offline suite from the root. Add a focused test for changed behavior, exercise installation and removal for installer changes, and keep examples and documentation current. Verify discovery and activation in the affected clients before claiming that compatibility works live. [Local validation](README.md#validation-and-evaluations), [Live evaluations](evals/README.md#run-live-evaluations)

With the CI tools installed, run the same static checks locally.

```sh
uv run --no-build --no-python-downloads scripts/ci/validate_yaml.py
shellcheck scripts/*.sh
actionlint
zizmor --offline --collect=all .
lychee --offline --include-fragments --no-progress './*.md' './skills/**/*.md' './evals/**/*.md'
```

The YAML check uses uv to install a pinned parser in an isolated script environment. The workflow reuses runner-provided ShellCheck and verifies analyzer downloads against pinned SHA-256 digests. ShellCheck covers the maintained wrappers. The shell evaluation fixture deliberately contains the bad expansion exercised by the unit tests. Review Dependabot's weekly updates and retain full commit SHA pins. [Workflow and tool versions](.github/workflows/validate.yml), [Dependabot configuration](.github/dependabot.yml)
