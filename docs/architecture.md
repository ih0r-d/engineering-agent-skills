# Repository architecture

The repository holds reusable engineering workflows for coding agents. A skill's stable identifier is recorded in `catalog.json`; its source package is `skills/<category-id>/<skill-id>/SKILL.md`. Category containers are organizational only. Installers resolve each package through catalog membership and install it flat as `<agent-skills>/<skill-id>` so existing invocations remain stable.

| Path | Responsibility |
| --- | --- |
| `skills/` | Canonical skill instructions and resources |
| `catalog.json` | Category definitions and unique skill membership by ID |
| `.scripts/` | Offline installer, validators, generated README catalog tooling, repository checks, and locked maintainer dependencies |
| `scripts/` | Compatibility entrypoints for older checkouts and submodule instructions |
| `tests/` | Deterministic installer, catalog, resource, and specification regressions |
| `evals/` | Synthetic evaluation cases, fixtures, and the manual live evaluation protocol |
| `docs/` | Architecture and compatibility guidance |
| `templates/` | Reusable authoring templates excluded from skill discovery and installation |
| `.github/` and `Taskfile.yml` | Hosted and local quality gates |

## Context boundaries

See the [context engineering architecture](context-architecture.md) for the separation of runtime instructions, consumer policy, reusable skills and project evidence. The project instruction templates are opt-in examples, not installer-managed resources.

## Categories

The catalog registers these categories with stable IDs. Each skill belongs to one primary category. The validator compares unique catalog membership with physical category directories, rejecting missing, duplicate, misplaced, and unregistered skill packages. [Catalog and current mappings](../catalog.json)

- Software Engineering
- Software Architecture
- Bug Fixing and Reliability
- Testing and Quality Assurance
- Software Delivery
- Engineering Productivity
- AI Engineering

## Skill contract

Each `SKILL.md` starts with YAML frontmatter containing a `name` that matches the parent directory and a `description` that tells agents what the workflow does and when to use it. Optional standard fields are `license`, `compatibility`, `metadata`, and experimental `allowed-tools`. Agent support for experimental fields varies. Metadata keys and values are YAML strings. Quote values such as `true` or `1.0` when they represent text. [Agent Skills specification](https://agentskills.io/specification)

Keep the main instructions concise and usable for common tasks. The specification recommends keeping the entrypoint under 500 lines and instructions below 5,000 tokens. Link detailed guidance and other resources by portable paths relative to the skill. This repository asks authors to say when to read each substantial reference, to prefer one recurring engineering task per skill, and to add positive and near-miss routing cases. Existing optional client metadata, such as Java's Codex UI metadata, stays outside the portable frontmatter. [Contribution standards](../CONTRIBUTING.md), [Specification recommendations](https://agentskills.io/specification#progressive-disclosure)

Follow the [Skill Authoring Guide](skill-authoring.md) for recommended Markdown conventions and use the [Skill Template](../templates/SKILL.md) as a starting point. These conventions complement the official specification without imposing additional format requirements.

See the [Phase 2.8 catalog audit](skill-audit.md) for reviewed responsibility boundaries, retained workflows, and identified technical depth gaps.

## Validation and installation boundaries

The Python 3.10+ installer uses only the standard library. It resolves package sources through the catalog, installs flat skill directories, and checks bundled Markdown resource paths and ownership before writing. The offline `validate` command also checks category membership and layout. Evaluation cases follow the same catalog categories. The maintainer gate uses PyYAML and the pinned official `skills-ref` metadata validator. Repository checks enforce YAML types and duplicate-key handling; Lychee checks Markdown links and anchors. [Reference implementation](https://github.com/agentskills/agentskills/tree/f130f348f502d9804278a617f86929846896d2e9/skills-ref), [Maintainer dependency lock](../.scripts/spec/uv.lock)

The installer supports project and user scope. A relative symlink follows the checked-out skill while a copied skill is an independently verified snapshot. Existing skill folders, installation scopes, and agent destinations are compatibility boundaries. [Installer compatibility](compatibility.md)

A repository-owner licensing decision is a prerequisite for future redistribution. [License status](../README.md#license)
