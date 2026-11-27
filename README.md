# Engineering Agent Skills

**Reusable engineering workflows for AI coding agents. Review with evidence, make minimal changes, and verify results.**

[![Validate skills](https://github.com/ih0r-d/engineering-agent-skills/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/ih0r-d/engineering-agent-skills/actions/workflows/validate.yml)
[![Agent Skills](https://img.shields.io/badge/standard-Agent%20Skills-57534e)](https://agentskills.io/specification)
[![Skills](https://img.shields.io/badge/skills-35-2563eb)](#skill-catalog)
[![Codex & Claude Code](https://img.shields.io/badge/agents-Codex%20%7C%20Claude%20Code-0f766e)](#supported-agents)
[![Python 3.10+](https://img.shields.io/badge/offline%20installer-Python%203.10%2B-3776ab)](#offline-installation)
[![Stand with Ukraine](https://img.shields.io/badge/Stand%20with-Ukraine-0057b7)](https://u24.gov.ua/)

[**Skills**](#skill-catalog) · [**Install from GitHub**](#install-from-github) · [**Offline installation**](#offline-installation) · [**Git submodule**](#git-submodule-integration) · [**Validation**](#validation-and-evaluations) · [**Contributing**](CONTRIBUTING.md)

> 🇺🇦 **Слава Україні! Героям слава!**
>
> Stand with Ukraine.

## Overview

Engineering Agent Skills is a portable collection of [Agent Skills](https://agentskills.io/specification) for **Codex** and **Claude Code**. It provides focused workflows for reviewing code, diagnosing defects, preparing safe fixes, and validating engineering changes.

Designed for personal, commercial, and open-source projects, the toolkit follows the consuming repository's conventions rather than imposing a framework or build configuration.

**Core principles:**

- **Evidence-based findings:** describe the affected code, observed impact, and how to reproduce or verify a problem.
- **Review first:** review requests are read-only; changes require explicit authorization.
- **Minimal fixes:** preserve public contracts, behavior, and existing architecture unless a change is justified.
- **Selective context:** short `SKILL.md` entrypoints load topic-specific references only when needed.
- **Portable tooling:** reuse available project analyzers; do not force dependencies or build-file changes.
- **Installation choice:** install directly from GitHub or from a local checkout without network access.

For project-specific rules and agent instruction templates, see the [Context Engineering Architecture](docs/context-architecture.md).

## Skill Catalog

| Skill | Engineering focus |
| --- | --- |
| [`code-review`](skills/code-review/SKILL.md) | Findings-first review of diffs, regressions, and missing verification |
| [`java-quality`](skills/java-quality/SKILL.md) | Java API compatibility, concurrency, resource lifecycle, generated code, classloaders, proxies, and static-analysis findings |
| [`python-quality`](skills/python-quality/SKILL.md) | Python typing, import behavior, packaging, exceptions, lifecycle, concurrency, and tests |
| [`refactoring`](skills/refactoring/SKILL.md) | Scoped structural improvements with a verified behavior baseline |
| [`shell-quality`](skills/shell-quality/SKILL.md) | POSIX `sh` and Bash correctness, quoting, exit codes, cleanup, and portability |
| [`system-design`](skills/system-design/SKILL.md) | System boundaries, component responsibilities, data flows, scalability, reliability, and architectural trade-offs |
| [`build-automation-quality`](skills/build-automation-quality/SKILL.md) | Maven, Gradle, Makefile, and Taskfile correctness, dependency graphs, and reproducibility |
| [`container-quality`](skills/container-quality/SKILL.md) | Dockerfile and Compose builds, secrets, image and container lifecycle, and runtime behavior |
| [`documentation-quality`](skills/documentation-quality/SKILL.md) | README, Quick Start, consumer and maintainer guides, API documentation, and documentation drift |
| [`engineering-handoff`](skills/engineering-handoff/SKILL.md) | Engineering context transfer, verified state, blockers, and next actions |
| [`task-decomposition`](skills/task-decomposition/SKILL.md) | Verifiable work items, dependency ordering, and delivery slices |
| [`implementation-planning`](skills/implementation-planning/SKILL.md) | Scoped implementation sequencing, verification, and change risks |
| [`requirements-analysis`](skills/requirements-analysis/SKILL.md) | Requirements, business rules, scope, and verifiable acceptance criteria |
| [`release-engineering`](skills/release-engineering/SKILL.md) | Release readiness, versioning, artifacts, CI/CD, release notes, and recovery planning |
| [`token-optimization`](skills/token-optimization/SKILL.md) | Measured token efficiency, concise output, and correctness-preserving optimization |
| [`context-engineering`](skills/context-engineering/SKILL.md) | Context selection, progressive disclosure, evidence preservation, and compaction |
| [`prompt-engineering`](skills/prompt-engineering/SKILL.md) | Prompt design, output contracts, ambiguity, and instruction boundaries |
| [`skill-evaluation`](skills/skill-evaluation/SKILL.md) | Behavioral evaluations, routing, controlled comparisons, and regression evidence |
| [`skill-authoring`](skills/skill-authoring/SKILL.md) | Portable skill authoring, activation boundaries, and specification compliance |
| [`dependency-management`](skills/dependency-management/SKILL.md) | Dependency resolution, compatibility, lockfiles, and scoped upgrades |
| [`deployment`](skills/deployment/SKILL.md) | Rollout planning, environment verification, migration compatibility, and recovery |
| [`git-workflow`](skills/git-workflow/SKILL.md) | Atomic commits, Conventional Commits, task identifiers, branching, and safe Git operations |
| [`ci-cd`](skills/ci-cd/SKILL.md) | Pipeline design, quality gates, workflow security, and CI reliability |
| [`architecture-review`](skills/architecture-review/SKILL.md) | Architecture assessment, component boundaries, coupling, quality attributes, and architectural risk identification |
| [`incident-analysis`](skills/incident-analysis/SKILL.md) | Incident impact, timelines, response review, and postmortem follow-up |
| [`security-review`](skills/security-review/SKILL.md) | Defensive security assessment, access control, sensitive data, and vulnerability mitigation |
| [`integration-testing`](skills/integration-testing/SKILL.md) | Integration and contract tests, real collaborator behavior, and isolated environments |
| [`unit-testing`](skills/unit-testing/SKILL.md) | Focused unit tests, test doubles, deterministic isolation, and regression coverage |
| [`test-strategy`](skills/test-strategy/SKILL.md) | Risk-based test planning, coverage gaps, test levels, and quality gates |
| [`performance-analysis`](skills/performance-analysis/SKILL.md) | Performance baselines, profiling, bottleneck evidence, and benchmark design |
| [`root-cause-analysis`](skills/root-cause-analysis/SKILL.md) | Causal chains, contributing factors, evidence quality, and recurrence prevention |
| [`bug-fixing`](skills/bug-fixing/SKILL.md) | Scoped defect correction, regression tests, and compatibility verification |
| [`bug-investigation`](skills/bug-investigation/SKILL.md) | Defect reproduction, diagnostic evidence, hypothesis testing, and fault isolation |
| [`architecture-decision`](skills/architecture-decision/SKILL.md) | Architecture decision records, alternatives, decision drivers, trade-offs, and consequences |
| [`api-design`](skills/api-design/SKILL.md) | API contracts, protocol semantics, schemas, error handling, versioning, and consumer compatibility |
Skills are independently installable. Load optional `references/` only when relevant to the task. [Engineering categories](docs/architecture.md#categories), [Software Engineering skill boundaries](docs/software-engineering.md)

For creating or revising skills, use the [repository Skill Authoring Standard](docs/skill-authoring.md). It distinguishes official format requirements from local recommendations and evaluation practices.

## Installation

Choose the method that fits your project:

| Method | Best for | Requirements |
| --- | --- | --- |
| **[GitHub / `npx skills`](#install-from-github)** | Quick installation without a manual clone; project or user scope | Node.js 22.20+, network access |
| **[Local / offline](#offline-installation)** | Private or restricted environments; controlled installation from an existing checkout | Python 3.10+, local toolkit directory |
| **[Git submodule](#git-submodule-integration)** | Pinning a known toolkit revision inside a Git repository | Git, Python 3.10+, initialized submodule |

### Install from GitHub

Use the [Skills CLI](https://github.com/vercel-labs/skills) to install selected Skills directly from this repository. **No manual `git clone` or Git submodule is required.** Run commands from the consuming project's directory.

List available Skills:

```bash
npx skills add ih0r-d/engineering-agent-skills --list
```

Install `java-quality` for Codex:

```bash
npx skills add ih0r-d/engineering-agent-skills \
  --skill java-quality \
  --agent codex
```

Install Java and documentation Skills for both agents:

```bash
npx skills add ih0r-d/engineering-agent-skills \
  --skill java-quality \
  --skill documentation-quality \
  --agent codex \
  --agent claude-code
```

Install a Skill for your user account, across projects:

```bash
npx skills add ih0r-d/engineering-agent-skills \
  --skill documentation-quality \
  --agent codex \
  --global
```

The CLI may prompt for confirmation or installation mode. It retrieves skills over the network and manages its own installation metadata.

For reproducible installations, the CLI supports a repository tag or full commit SHA as a source revision. See the [Skills CLI installation reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add).

### Offline installation

The built-in installer uses **Python 3.10+ and the standard library only**. It performs no network requests. A local toolkit checkout must already exist (for example, a previously downloaded archive, a Git checkout, or an initialized submodule).

From the toolkit directory, preview a project installation:

```bash
python3 .scripts/skills.py list
python3 .scripts/skills.py install \
  --agent codex \
  --target /path/to/project \
  --skill java-quality \
  --dry-run
```

Install after reviewing the preview:

```bash
python3 .scripts/skills.py install \
  --agent codex \
  --target /path/to/project \
  --skill java-quality
```

For both agents and multiple Skills:

```bash
python3 .scripts/skills.py install \
  --agent all \
  --target /path/to/project \
  --skill java-quality,documentation-quality
```

Use `--scope user` for user-level installation, `--mode copy` when symlinks are unsuitable, or `--all` to select the entire catalog. `--dry-run` previews changes without applying them.

The local installer manages only entries it installed. It does not change consumer build files, `AGENTS.md`, `CLAUDE.md`, or the Git index.

The `.scripts/` paths are the maintained entrypoints. Historical paths under `scripts/` continue to work. [Installer compatibility](docs/compatibility.md)

### Git submodule integration

A submodule lets a consuming repository pin the toolkit to a specific revision. From the **consumer repository root**:

```bash
git submodule add \
  https://github.com/ih0r-d/engineering-agent-skills.git \
  .tooling/engineering-agent-skills

./.tooling/engineering-agent-skills/.scripts/install.sh \
  --agent all \
  --skill java-quality,documentation-quality \
  --dry-run

./.tooling/engineering-agent-skills/.scripts/install.sh \
  --agent all \
  --skill java-quality,documentation-quality
```

The built-in installer creates relative symlinks by default:

```text
.agents/skills/java-quality -> ../../.tooling/engineering-agent-skills/skills/java-quality
.claude/skills/java-quality -> ../../.tooling/engineering-agent-skills/skills/java-quality
```

The links remain valid when the project and initialized submodule move together. After a fresh clone, initialize the submodule before using the installed Skills:

```bash
git submodule update --init --recursive
```

Adding or updating a submodule changes the consuming repository's Git metadata. The installer itself performs no Git operations.

## Supported Agents

| Agent | Project scope | User scope | Explicit invocation |
| --- | --- | --- | --- |
| **Codex** | `.agents/skills/` | `~/.agents/skills/` | `$java-quality` |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` | `/java-quality` |

After installation, open the consuming project in your agent and request a focused review:

> Review the changed Java code for concurrency and public API regressions. Provide evidence and verification steps. Do not modify files.

Invoke a skill explicitly when needed. If a new skill is missing, start a fresh agent session and check the installed links and client settings. The installer layouts are covered by deterministic tests. The [compatibility guide](docs/compatibility.md) records the documented client behavior and the scope of verification.

The toolkit's root `AGENTS.md` and `CLAUDE.md` govern **toolkit maintenance only**; the installers do not copy them into consuming repositories.

## Updating and Uninstalling

Use the tool that originally installed the Skill. **Do not mix the Skills CLI's installation management with the built-in Python installer's ownership checks.**

**GitHub / Skills CLI:**

```bash
npx skills check
npx skills update java-quality
npx skills remove java-quality
```

**Local / built-in installer:**

```bash
python3 .scripts/skills.py uninstall \
  --agent codex \
  --target /path/to/project \
  --skill java-quality \
  --dry-run

python3 .scripts/skills.py uninstall \
  --agent codex \
  --target /path/to/project \
  --skill java-quality
```

- **Local symlink mode:** installed Skills follow the selected checkout; updating the pinned submodule revision updates their content.
- **Local copy mode:** uninstall the managed copy and reinstall to refresh it.
- **Safety:** the local installer refuses unrelated destinations and protects modified installed copies from automatic deletion. It rejects symlinked agent parent directories that could redirect writes outside the target.

If a batch stops partway through, inspect the reported paths and preview the same selection before retrying. [Partial-operation recovery](docs/compatibility.md#recovering-from-a-partial-operation)

## Validation and Evaluations

Run the dependency-free checks from the toolkit root.

```bash
python3 -B .scripts/skills.py validate
python3 -B -m unittest discover -s tests -v
bash .scripts/check.sh syntax
```

Run `task ci` for the complete maintainer suite, including the mandatory Agent Skills specification gate, regression tests, static checks, and Markdown links. The maintainer gate requires Python 3.11+ and uses a locked version of the official reference validator. GitHub Actions exercises the offline installer on Linux and macOS. [Maintainer prerequisites and commands](CONTRIBUTING.md#verify-changes)

| Verification | Covers | AI model required? |
| --- | --- | --- |
| **Offline tests** | Skill structure, installer safety, symlinks, fixtures, and links | No |
| **Live evaluations** | Skill discovery, routing, finding accuracy, false positives, and agent behavior | Yes |

The live evaluation procedure measures review behavior in the client. [Evaluation guidance](evals/README.md)

## Repository Layout

`skills/<skill-id>/SKILL.md` is the canonical entrypoint. `catalog.json` groups the skills by engineering category. Implementation, validation, and compatibility entrypoints are described in the [architecture guide](docs/architecture.md).

## Contributing

Contributions should improve real engineering outcomes, not just add longer checklists. Keep Skill activation boundaries clear, add representative evidence or evaluation scenarios, and preserve compatibility with the [Agent Skills specification](https://agentskills.io/specification).

See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and required checks.

## License

A repository-owner licensing decision is required before future redistribution. A license has yet to be selected.
