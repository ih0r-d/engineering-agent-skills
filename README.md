# Engineering Agent Skills

Seven portable Agent Skills for focused engineering reviews, requested fixes and verification in Codex and Claude Code. Each Skill starts with a short workflow and links to the references relevant to the task. The installer requires Python 3.10+ and uses the standard library. The optional shell wrappers require Bash.

| Skill | Use it for |
| --- | --- |
| [`java-quality`](skills/java-quality/SKILL.md) | Java contracts, concurrency, generated sources, modules, proxies and analyzer triage |
| [`python-quality`](skills/python-quality/SKILL.md) | Python runtime and typing, package boundaries and local checks |
| [`shell-quality`](skills/shell-quality/SKILL.md) | POSIX sh and Bash argument safety, status, cleanup and portability |
| [`build-automation-quality`](skills/build-automation-quality/SKILL.md) | Maven, Gradle, Make and Task dependency graphs and reproducibility |
| [`container-quality`](skills/container-quality/SKILL.md) | Dockerfile, build context, image and Compose lifecycle review |
| [`documentation-quality`](skills/documentation-quality/SKILL.md) | README, quick starts, maintainer docs, API documentation and drift |
| [`release-engineering`](skills/release-engineering/SKILL.md) | Release readiness, version and notes preparation, artifact verification and rollout checks |

## Quick start

From the toolkit checkout, replace `/path/to/project` with an existing project directory.

```sh
python3 scripts/skills.py list
python3 scripts/skills.py install --agent codex --target /path/to/project --skill java-quality --dry-run
python3 scripts/skills.py install --agent codex --target /path/to/project --skill java-quality
```

The preview prints `DRY RUN install`. Installation prints `INSTALLED`, and an identical repeat prints `SKIP`. Use `--agent claude` for Claude Code or `--agent all` for both. Repeat `--skill`, pass a comma-separated list, or use `--all` for the current catalog.

Open the target project in your agent. Ask for a focused review, for example “Review the changed Java code for concurrency regressions. Report evidence and verification. Leave files untouched.” To select the Skill explicitly, use `$java-quality` in Codex or `/java-quality` in Claude Code. Start a fresh session if a newly installed Skill is missing from the picker. Check symlink targets and agent visibility settings if discovery still fails.

| Agent | Project scope | User scope |
| --- | --- | --- |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |

Both agents document discovery of whole-directory symlinks in these locations. [Codex Skills](https://learn.chatgpt.com/docs/build-skills), [Claude Code Skills](https://code.claude.com/docs/en/skills#choose-where-skills-load), [Agent Skills specification](https://agentskills.io/specification)

Both installs use the same Skill folders. The installer requires `--skill` or `--all` and leaves the target's `AGENTS.md`, `CLAUDE.md` and Git index untouched. Start the agent from the consuming project to work under its instructions.

For user scope, omit `--target`. For project scope, it defaults to the current directory.

```sh
python3 scripts/skills.py install --agent all --scope user --skill documentation-quality --mode copy
```

## Install from a local Git submodule

Run from the consuming Git project's root. Set `skills_checkout` to a trusted **local Git checkout**. Git uses its committed revision for the submodule.

```sh
skills_checkout=/absolute/path/to/engineering-agent-skills
git -c protocol.file.allow=always submodule add -- "$skills_checkout" .tooling/engineering-agent-skills
./.tooling/engineering-agent-skills/scripts/install.sh --agent all --skill java-quality,documentation-quality
```

Git's `submodule add` stages the gitlink and `.gitmodules` in the host repository. Initialize an existing submodule before running the installer. Git may contact the configured remote when initializing a submodule from a remote URL. For a trusted local file URL, use `git -c protocol.file.allow=always submodule update --init -- .tooling/engineering-agent-skills`.

The resulting links resolve within the project and survive relocation of the project and its initialized submodule together.

```text
.agents/skills/java-quality -> ../../.tooling/engineering-agent-skills/skills/java-quality
.claude/skills/java-quality -> ../../.tooling/engineering-agent-skills/skills/java-quality
```

## Update or remove

```sh
python3 scripts/skills.py uninstall --agent codex --target /path/to/project --skill java-quality --dry-run
python3 scripts/skills.py uninstall --agent codex --target /path/to/project --skill java-quality
```

- Symlink mode is the default and reads from the selected checkout. Keep that checkout accessible and uninstall before moving it independently. Exact relative links to its skill paths identify toolkit installations, including dangling links at the expected location.
- Copy mode works where symlink creation is unavailable. To refresh or switch modes, remove the managed entry and install again. For a manual installation, copy the entire Skill directory and manage it yourself.
- An installed copy carries a local fingerprint of its paths, contents and executable bits. Edited copies, malformed or missing markers, unrelated destination entries and symlinked agent parent directories are refused. Preserve local edits before manually moving such an entry aside. Legacy copies can be removed automatically when they still match the originating checkout.
- The installer checks the whole selection for known conflicts first. In case of an unexpected filesystem failure, completed entries remain and the command reports the failure. Resolve it and rerun the same selection. If an interrupted copy remains without its marker, inspect and move it aside before retrying.
- Install and uninstall operate on the selected local skill directories. They perform no network access, build execution, project configuration edits or Git operations. Run them from a trusted checkout against a target you control.

## Repository instructions

The toolkit's maintenance rules live in [AGENTS.md](AGENTS.md). Codex reads it directly. Claude Code v2.1.277 and later can read it directly when its instruction settings allow. The one-line [CLAUDE.md](CLAUDE.md) imports it for older clients and sessions that load `CLAUDE.md` in preference to `AGENTS.md`. These files scope their guidance to toolkit maintenance. [Codex project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude Code project instructions](https://code.claude.com/docs/en/memory#agentsmd)

## Validation

```sh
python3 scripts/skills.py validate
python3 -B -m unittest discover -s tests -v
for script in scripts/*.sh; do bash -n "$script" || exit; done
```

The local suite requires no credentials, package downloads or model calls. GitHub Actions runs it on Linux and macOS. A separate job in the same workflow parses YAML, runs ShellCheck and actionlint, audits workflow security with offline zizmor, and checks local Markdown links and anchors with Lychee. The analyzers download once per run and their checks use local files. [Static checks and tool versions](CONTRIBUTING.md#verify-changes), [Evaluation fixtures and agent protocol](evals/README.md), [Initial audit](AUDIT.md)

Offline checks verify the installed layout and links. Check discovery with explicit invocation in the target client, then use a fresh prompt without the Skill name to check automatic activation. Client version, workspace trust and settings can affect discovery.

The Java Skill was adapted from `java-oss-quality`. License selection for public distribution is pending.

```text
skills/              Seven standalone Skills and their topic references
scripts/             Python CLI and Bash wrappers
tests/               Deterministic installer, catalog and fixture tests
evals/               Routing cases, fixtures and optional agent evaluation
.github/workflows/   Linux and macOS validation
```
