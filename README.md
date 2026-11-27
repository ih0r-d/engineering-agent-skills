# Engineering Agent Skills

**Portable engineering workflows and technical expertise for AI coding agents.** Use focused skills to review, design, implement, test, debug, release, deploy, and maintain software within the conventions of the project you are working in.

[![CI](https://github.com/ih0r-d/engineering-agent-skills/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/ih0r-d/engineering-agent-skills/actions/workflows/validate.yml) [![Agent Skills specification](https://img.shields.io/badge/format-Agent%20Skills-57534e)](https://agentskills.io/specification)

This repository is a toolkit, not an agent runtime or orchestration framework. It does not replace Codex, Claude Code, Copilot, or another coding agent, and it does not require a particular model provider. Compatible clients discover and use the skill packages they support.

[Quick Start](#quick-start) · [Agent support](#agent-support) · [Skill catalog](#skill-catalog) · [Architecture](#how-the-toolkit-works) · [Contributing](CONTRIBUTING.md)

## What the toolkit provides

- Workflows spanning the software development lifecycle, from requirements through maintenance.
- Specialist engineering capabilities with explicit scopes, practical steps, and verification guidance.
- Focused technical references that are selected when relevant rather than loaded as a catalog-wide manual.
- Self-contained skill packages with optional executable scripts and reusable engineering templates.
- An offline installer and deterministic checks for package structure, resource links, installation safety, and evaluation data.

Context efficiency is a design objective: agents can select one workflow and load only the details its task needs. No measured token savings or behavioral improvements are claimed.

## Quick Start

### Prerequisites

- Git and Python 3.10 or later.
- A Codex or Claude Code project directory where you can add skill files.
- The local installer makes no network requests; cloning this repository does require network access. For restricted environments, provide a checkout or archive through your existing process.

### Install one skill

From a terminal in the project where you want to use a skill:

```bash
git clone https://github.com/ih0r-d/engineering-agent-skills.git /tmp/engineering-agent-skills
python3 /tmp/engineering-agent-skills/.scripts/skills.py list
python3 /tmp/engineering-agent-skills/.scripts/skills.py install \
  --agent codex \
  --target "$PWD" \
  --skill java-quality \
  --mode copy \
  --dry-run
```

Review the preview, then repeat the install command without `--dry-run`. For example, install more than one skill with `--skill java-quality,unit-testing`, select both installer-supported clients with `--agent all`, or select the whole catalog with `--all`.

Project installation paths are `.agents/skills/<skill-id>/` for Codex and `.claude/skills/<skill-id>/` for Claude Code. The installed package is flat even though source skills are grouped by category. Open or reload the project in the agent, then ask a task-specific question such as:

> Review the changed Java code for concurrency and public API compatibility. Show evidence and verification steps; do not modify files.

You can also explicitly invoke a skill using the client’s supported syntax, such as `$java-quality` in Codex or `/java-quality` in Claude Code. Invocation and automatic skill selection depend on the client and its configuration.

## Agent support

The installer and client compatibility are separate: the installer creates directories, while each agent controls skill discovery and invocation.

| Client | Installer target | Documented skill locations | Compatibility status |
| --- | --- | --- | --- |
| Codex | Yes; project and user scope | `.agents/skills/`, `~/.agents/skills/` | Destination layouts are covered by installer tests; live routing is client/version dependent. |
| Claude Code | Yes; project and user scope | `.claude/skills/`, `~/.claude/skills/` | Destination layouts are covered by installer tests; live routing is client/version dependent. |
| GitHub Copilot | No | Surface-specific locations include project `.agents/skills/` and personal skill directories. | Agent Skills support and locations are documented. Use client-specific setup; this installer does not target Copilot, and runtime discovery is not independently verified here. |

Clients that implement the [Agent Skills specification](https://agentskills.io/specification) may be able to use the portable packages through their own discovery paths. The standard does not guarantee that every client implements every capability. Check the client’s current setup documentation before choosing a location.

- [Codex skill documentation](https://developers.openai.com/codex/skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [GitHub Copilot Agent Skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills)
- [Installer and client compatibility notes](docs/compatibility.md)

## Installation modes

The built-in installer is Python 3.10+ and standard-library only. It supports project scope (selected with `--target`) and user scope (selected with `--scope user`; omit `--target`). It manages only verified installations and protects unmanaged or locally modified resources.

| Mode | Behavior | Use when |
| --- | --- | --- |
| **Symlink** (default) | Installs a relative link to the selected source package. Changes in that checkout are immediately reflected in the installed skill. | The source checkout will remain available at its current relative location. |
| **Copy** (`--mode copy`) | Installs a self-contained snapshot and preserves bundled executable permissions. | You need independent files, cannot use symlinks, or want to keep the source checkout elsewhere. |

To update an installation, use the same installer that created it. A symlink follows its source checkout; refresh a copied installation by uninstalling and reinstalling. Use `--dry-run` to preview removal or installation. The installer does not modify project instructions, build files, the Git index, or user-level agent configuration.

```bash
# Install for a user account (omit --target for user scope)
python3 /tmp/engineering-agent-skills/.scripts/skills.py install \
  --agent codex --scope user --skill java-quality --dry-run

# Remove a project installation after reviewing the preview
python3 /tmp/engineering-agent-skills/.scripts/skills.py uninstall \
  --agent codex --target "$PWD" --skill java-quality --dry-run
```

See [compatibility and recovery notes](docs/compatibility.md) for partial operations and ownership limitations.

### Pin a checkout with a Git submodule

For a repository-pinned toolkit revision, add it as a submodule in the consuming repository and install from that checkout:

```bash
git submodule add \
  https://github.com/ih0r-d/engineering-agent-skills.git \
  .tooling/engineering-agent-skills
./.tooling/engineering-agent-skills/.scripts/install.sh \
  --agent all \
  --target "$PWD" \
  --skill java-quality,documentation-quality \
  --dry-run
```

Review the preview, then rerun without `--dry-run`. The installer creates relative symlinks by default; the submodule and project should move together. Initialize the pinned checkout after cloning with `git submodule update --init --recursive`. Adding or updating the submodule changes consumer-repository Git metadata; the skill installer itself does not run Git commands.

## Example engineering tasks

Prompts describe user intent; they do not guarantee that a specific client will select a particular skill automatically. Skills can be invoked explicitly where the client supports it.

- “Review this Java change for data races, `CompletableFuture` cancellation, and binary API compatibility.” — `java-quality` with `code-review` as needed.
- “Investigate this `OutOfMemoryError: Metaspace`; compare classloader activity and available JVM evidence before suggesting tuning.” — `java-quality`, with `performance-analysis` if measurement is needed.
- “Diagnose why the GitHub Actions deploy job cannot retrieve an artifact produced by an earlier job.” — `ci-cd`.
- “Prepare a production hotfix and backport plan. Identify the target release lines and tests; do not push, tag, publish, or deploy.” — `bug-investigation`, `bug-fixing`, `git-workflow`, and `release-engineering` as relevant.
- “Design a Spring Boot service and draft an ADR for the selected persistence boundary. Do not implement it.” — `system-design`, `java-quality`, and `architecture-decision` as relevant.
- “Create a risk-based test strategy for a Spring Boot service that reserves inventory and charges cards.” — `test-strategy`, with `integration-testing` or `unit-testing` if implementation is requested.

Composition is task-dependent. The toolkit does not provide an orchestration runtime or mandatory multi-skill pipeline.

## Skill catalog

The catalog below is generated from `catalog.json` and each skill’s YAML frontmatter. To refresh it, run `task docs:generate`; `task docs:check` and CI verify that it is current.

<!-- BEGIN GENERATED SKILL CATALOG -->

**Inventory:** 35 skills · 7 categories · 77 references · 7 assets · 1 script · 132 evaluation cases.

### Software Engineering

| Skill | Purpose |
| --- | --- |
| [`code-review`](skills/software-engineering/code-review/SKILL.md) | Review a pull request, patch, or scoped code change for actionable defects, regressions, and missing verification. Use for a findings-first review of proposed or existing changes. |
| [`java-quality`](skills/software-engineering/java-quality/SKILL.md) | Review Java source or generated Java for correctness, API compatibility, resource ownership, concurrency, or framework behavior. Use for Java code audits, targeted fixes, and triage of compiler or Java analyzer findings. |
| [`python-quality`](skills/software-engineering/python-quality/SKILL.md) | Review Python code, imports, typing, packaging, and tests for runtime or API regressions. Use for focused Python fixes, pytest verification, or Ruff, Pyright and mypy diagnostic triage. |
| [`refactoring`](skills/software-engineering/refactoring/SKILL.md) | Improve the structure of existing code while preserving observable behavior. Use for scoped simplification, consolidation, or separation of responsibilities with a behavior baseline. |
| [`shell-quality`](skills/software-engineering/shell-quality/SKILL.md) | Review or fix Bash and POSIX sh scripts for unsafe expansions, exit-status handling, cleanup, destructive filesystem operations, and portability. Use for shell diagnostic triage or script verification. |

### Software Architecture

| Skill | Purpose |
| --- | --- |
| [`api-design`](skills/software-architecture/api-design/SKILL.md) | Design and evolve API contracts for services and components. Use for REST, RPC, event interfaces, request and response schemas, error semantics, versioning, and backward compatibility. |
| [`architecture-decision`](skills/software-architecture/architecture-decision/SKILL.md) | Evaluate architectural alternatives and document architecture decision records (ADRs). Use for explicit technical decisions, decision drivers, trade-offs, consequences, and superseding existing decisions. |
| [`architecture-review`](skills/software-architecture/architecture-review/SKILL.md) | Assess existing software architecture against requirements, quality attributes, and operational constraints. Use for architecture audits, component boundaries, coupling, data ownership, scalability, reliability, and architectural risk assessment. |
| [`system-design`](skills/software-architecture/system-design/SKILL.md) | Design software systems, services, and components from functional and non-functional requirements. Use for system boundaries, component responsibilities, data flows, scalability, reliability, and integration design. |

### Bug Fixing and Reliability

| Skill | Purpose |
| --- | --- |
| [`bug-fixing`](skills/bug-fixing-and-reliability/bug-fixing/SKILL.md) | Fix an authorized software defect with a scoped correction and regression verification. Use when expected behavior and a reported failure require an implementation change. |
| [`bug-investigation`](skills/bug-fixing-and-reliability/bug-investigation/SKILL.md) | Investigate reproducible or intermittent software defects using symptoms, logs, tests, and execution traces. Use to isolate failing behavior and identify evidence before proposing a fix. |
| [`incident-analysis`](skills/bug-fixing-and-reliability/incident-analysis/SKILL.md) | Analyze an operational incident and prepare an evidence-based incident report or blameless postmortem. Use for impact, incident timelines, response effectiveness, recovery, and follow-up actions. |
| [`performance-analysis`](skills/bug-fixing-and-reliability/performance-analysis/SKILL.md) | Analyze software performance using measurements, profiling, workload characteristics, and resource usage. Use for latency, throughput, CPU, memory, I/O, contention, and scalability bottlenecks. |
| [`root-cause-analysis`](skills/bug-fixing-and-reliability/root-cause-analysis/SKILL.md) | Analyze causal mechanisms behind recurring defects, failures, or operational problems. Use for evidence-backed causal chains, contributing factors, systemic weaknesses, and recurrence prevention. |

### Testing and Quality Assurance

| Skill | Purpose |
| --- | --- |
| [`integration-testing`](skills/testing-and-quality-assurance/integration-testing/SKILL.md) | Write, review, or verify integration and contract tests across software components, databases, APIs, and messaging boundaries. Use for real collaborator behavior, compatibility, test environments, and cross-component failures. |
| [`security-review`](skills/testing-and-quality-assurance/security-review/SKILL.md) | Review software changes, architecture boundaries, and configuration for security vulnerabilities and exposure risks. Use for authorized defensive assessments, access control, sensitive data handling, and evidence-based remediation advice. |
| [`test-strategy`](skills/testing-and-quality-assurance/test-strategy/SKILL.md) | Define risk-based software testing strategies, coverage goals, test levels, and quality gates. Use for test planning, coverage gaps, and verification priorities across a system or change. |
| [`unit-testing`](skills/testing-and-quality-assurance/unit-testing/SKILL.md) | Write, review, or verify focused unit tests for software behavior. Use for boundary cases, deterministic isolation, test doubles, assertions, and regression coverage of individual units. |

### Software Delivery

| Skill | Purpose |
| --- | --- |
| [`build-automation-quality`](skills/software-delivery/build-automation-quality/SKILL.md) | Review or repair Maven and Gradle build configuration, Makefiles, and Taskfiles. Use for task dependencies, incremental builds, local and CI parity, reproducibility, or command-runner failures. |
| [`ci-cd`](skills/software-delivery/ci-cd/SKILL.md) | Design, review, or repair continuous integration and delivery pipelines. Use for workflow triggers, job dependencies, quality gates, caching, permissions, and pipeline reliability. |
| [`container-quality`](skills/software-delivery/container-quality/SKILL.md) | Review or fix Dockerfiles, build contexts, container runtime settings, and Docker Compose projects. Use to diagnose image reproducibility, secret handling, startup, health, shutdown, or local development behavior. |
| [`dependency-management`](skills/software-delivery/dependency-management/SKILL.md) | Review or update software dependencies, manifests, lockfiles, and transitive resolution. Use for dependency compatibility, version conflicts, upgrade planning, and reproducible dependency changes. |
| [`deployment`](skills/software-delivery/deployment/SKILL.md) | Plan, review, or verify software deployment and rollout procedures. Use for environment promotion, rollout strategies, runtime readiness, migrations, rollback, and deployment verification. |
| [`git-workflow`](skills/software-delivery/git-workflow/SKILL.md) | Plan or perform scoped Git workflows, atomic commits, Conventional Commits, task identifiers, branches, pull requests, and conflict resolution. Use for repository history and change organization. |
| [`release-engineering`](skills/software-delivery/release-engineering/SKILL.md) | Audit release readiness or prepare versions, changelogs, release notes, and artifact and CI validation. Use for compatibility, publishing checks, provenance, or rollback planning before a release. |

### Engineering Productivity

| Skill | Purpose |
| --- | --- |
| [`documentation-quality`](skills/engineering-productivity/documentation-quality/SKILL.md) | Write, review, or verify READMEs, quick starts, consumer guides, architecture and contributor docs, API reference, JavaDoc, Python docstrings, and examples. Use to investigate documentation drift or broken instructions. |
| [`engineering-handoff`](skills/engineering-productivity/engineering-handoff/SKILL.md) | Prepare or review engineering handoffs using verified repository state, completed work, decisions, checks, risks, and next actions. Use for transferring ownership or resuming interrupted technical work. |
| [`implementation-planning`](skills/engineering-productivity/implementation-planning/SKILL.md) | Plan scoped software changes against established requirements and existing repository contracts. Use for implementation sequencing, affected components, verification, migration, and risk planning. |
| [`requirements-analysis`](skills/engineering-productivity/requirements-analysis/SKILL.md) | Analyze stakeholder needs, business rules, constraints, and acceptance criteria before implementation. Use for clarifying ambiguous requirements and defining verifiable scope. |
| [`task-decomposition`](skills/engineering-productivity/task-decomposition/SKILL.md) | Break an established engineering objective into independently verifiable work items with dependencies, scope, and acceptance criteria. Use for backlog slicing, milestones, and sequencing deliverables. |

### AI Engineering

| Skill | Purpose |
| --- | --- |
| [`context-engineering`](skills/ai-engineering/context-engineering/SKILL.md) | Design or improve the context supplied to AI agents. Use for context selection, instruction placement, retrieval scope, handoff summaries, context limits, and evidence preservation. |
| [`prompt-engineering`](skills/ai-engineering/prompt-engineering/SKILL.md) | Design or refine prompts for AI tasks. Use for instruction hierarchy, task framing, examples, output contracts, ambiguity reduction, and prompt failure diagnosis. |
| [`skill-authoring`](skills/ai-engineering/skill-authoring/SKILL.md) | Create, review, or refactor portable Agent Skills. Use when defining skill scope, activation conditions, workflows, references, scripts, or specification compliance; combine with domain skills when their expertise is relevant. |
| [`skill-evaluation`](skills/ai-engineering/skill-evaluation/SKILL.md) | Design or run behavioral evaluations of agent skills. Use for routing, instruction following, task correctness, baseline comparisons, regression analysis, and evaluation rubrics. |
| [`token-optimization`](skills/ai-engineering/token-optimization/SKILL.md) | Measure and reduce avoidable token consumption in AI engineering workflows while preserving task correctness. Use for verbose instructions, repetitive context, tool output, and response efficiency. |

<!-- END GENERATED SKILL CATALOG -->

## Software development lifecycle

The catalog covers each lifecycle stage through focused, composable skills. A project or agent can select the relevant capabilities; the arrows show a common relationship, not an automatic pipeline.

```mermaid
flowchart LR
    R["Requirements<br/>requirements-analysis"] --> A["Architecture<br/>system-design · api-design · architecture-decision"]
    A --> P["Planning<br/>implementation-planning · task-decomposition"]
    P --> I["Implementation<br/>java-quality · python-quality · shell-quality · refactoring"]
    I --> T["Testing<br/>unit-testing · integration-testing · test-strategy"]
    T --> C["Review<br/>code-review · security-review"]
    C --> CI["CI<br/>ci-cd · build-automation-quality"]
    CI --> Rel["Release<br/>release-engineering"]
    Rel --> D["Deployment<br/>deployment"]
    D --> M["Maintenance<br/>incident-analysis · bug-investigation · dependency-management"]
    M --> R
```

## How the toolkit works

Clients differ in how they locate and load instructions. This is a conceptual model, not a guaranteed universal loading order or precedence rule.

```mermaid
flowchart LR
    U[User task] --> Agent[Compatible coding agent]
    Agent --> Policy[Project instructions]
    Agent --> Docs[Project documentation]
    Agent --> Code[Code and tests]
    Agent --> Skill[Relevant skill metadata and SKILL.md]
    Skill --> Result[Engineering result and verification]
    Skill -. only when needed .-> Ref[Focused technical reference]
    Skill -. only when needed .-> Script[Deterministic script]
    Skill -. only when needed .-> Asset[Reusable deliverable template]
    Docs --> Result
    Code --> Result
    Ref --> Result
    Script --> Result
    Asset --> Result
```

Project instructions supply repository-specific policy; the skill supplies a reusable workflow; references contain deeper subject expertise; scripts perform deterministic operations; assets provide reusable output structures. Project documentation, code, and tests supply the evidence. These capabilities are model-provider independent as files, but client discovery, invocation, and tool permissions vary.

### Skill package anatomy

```text
skill-id/
├── SKILL.md       # purpose, activation, workflow, constraints, verification
├── references/    # optional, conditionally loaded technical guidance
├── scripts/       # optional, tested deterministic operations
└── assets/        # optional, reusable templates and data
```

Each skill is a self-contained package; references, scripts, and assets are optional. The source repository groups packages under `skills/<category-id>/<skill-id>/`; the installer places each package flat under its skill ID. This repository recommends roughly 30–100 lines for most entrypoints and prefers fewer than 1,500 tokens. These are local advisory targets, not Agent Skills format requirements; necessary instructions take precedence.

### Repository map

| Path | Role |
| --- | --- |
| `skills/<category>/<skill>/` | Categorized source packages and their optional resources |
| `catalog.json` | Single source for skill IDs and category membership |
| `evals/` | Modular routing cases, fixtures, and evaluation protocol |
| `docs/` | Architecture, compatibility, authoring, audit, and evaluation guidance |
| `templates/` | Adaptable skill and project-instruction examples |
| `tests/` | Offline regression and specification tests |
| `.scripts/` | Installer, validators, documentation generator, and maintainer checks |
| `scripts/` | Historical compatibility entrypoints |
| `.github/workflows/` | GitHub Actions validation workflow |
| `Taskfile.yml` | Local validation and documentation tasks |

## Quality assurance and evaluation

Deterministic checks validate format, catalog membership, resource boundaries, installer behavior in copy and symlink modes, bundled scripts, local Markdown links, evaluation schemas, fixtures, and routing-case coverage. These checks establish repository structure and test tooling behavior.

The evaluation suite describes expected routing and behavior; case inventory is shown above. Cases are not successful model runs. Live evaluation requires an AI agent and the protocol in [evals/README.md](evals/README.md); live behavioral effectiveness has not been established by deterministic checks. Performance, token, latency, and cost comparisons are future measurement work.

## Contributing and development

Maintainer checks require Python 3.11+, Task, uv, Bash, ShellCheck, actionlint, zizmor, and Lychee. End-user installation does not require Task or the maintainer toolchain.

```bash
task validate       # catalog, resources, and specification gate
task test           # deterministic unit and regression tests
task eval:check     # evaluation schema, routing, and fixtures
task docs:generate  # update generated README catalog
task docs:check     # catalog freshness and Markdown links
task ci             # full maintainer quality gates
```

See [CONTRIBUTING.md](CONTRIBUTING.md), the [canonical Skill Authoring Standard](docs/skill-authoring.md), [repository architecture](docs/architecture.md), [context architecture](docs/context-architecture.md), and the [evaluation protocol](evals/README.md).

## Project direction

**Completed foundations:** categorized skill catalog, context architecture, Authoring Standard v2, technical references, modular evaluation cases, standalone package portability, and reusable scripts and assets.

**Possible follow-up work:** establish a live behavioral baseline; measure context and token use; evaluate optional Caveman or Promptfoo integrations; consider independent skill versioning, release automation, marketplace distribution, and opt-in client-specific hooks. These are not current features or commitments. An AI Software Factory or orchestration framework is outside this repository’s scope.

## License

There is no `LICENSE` file in this repository. The source is publicly visible, but a license has not been selected; consult the maintainers before assuming reuse or redistribution permissions.
