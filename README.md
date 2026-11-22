# Engineering Agent Skills

Reusable, focused engineering quality and release workflows for AI coding agents, across personal, commercial, and open-source projects. **Offline-first, project-agnostic, and conservative about changes.**

## Available skills

| Skill | Purpose |
| --- | --- |
| `java-quality` | Java correctness, API compatibility, code generation, design and static-analysis review |
| `python-quality` | Python correctness, typing, API design and tests |
| `shell-quality` | Bash/sh safety, portability, quoting and CLI behavior |
| `build-automation-quality` | Maven, Gradle, Makefile and Taskfile quality |
| `container-quality` | Dockerfile, Compose and image/runtime concerns |
| `documentation-quality` | Consumer docs, architecture docs, API contracts and examples |
| `release-engineering` | Release readiness, changelog, versioning and controlled execution |

Skills contain short `SKILL.md` entrypoints and load topic-specific references only when needed. They are standards and workflows, not autonomous background services. Any script or analyzer invocation depends on available local tools and the consuming project's policy.

## Prerequisites

- Python 3.10+ for the optional installer/validator (standard library only).
- Codex and/or Claude Code for using the installed skills.
- No Java/Maven/Docker dependencies needed just to install skills.

## Install from a Git submodule

From the root of an existing project, add this repository as a submodule after publishing it:

```bash
git submodule add https://github.com/<owner>/engineering-agent-skills.git .tooling/engineering-agent-skills
git submodule update --init --recursive
```

Install a selection for Codex and Claude Code from the **host project root**:

```bash
./.tooling/engineering-agent-skills/scripts/install.sh \
  --agent all --target . --skill java-quality --skill documentation-quality
```

This creates relative symbolic links:

```text
.agents/skills/java-quality -> ../../.tooling/engineering-agent-skills/skills/java-quality
.claude/skills/java-quality -> ../../.tooling/engineering-agent-skills/skills/java-quality
```

The actual relative link depth is calculated from the location of the target directory. The example above shows the resulting layout conceptually; inspect actual links with `ls -l`.

Existing skill paths are not overwritten. For environments where symlinks cannot be used, choose `--mode copy` (copies must be reinstalled to pick up source updates).

## Manual and global installation

From the toolkit checkout:

```bash
# Review available skills
python3 scripts/skills.py list

# Preview changes
./scripts/install.sh --agent codex --target /path/to/project --skill shell-quality --dry-run

# Install to an arbitrary local project
./scripts/install.sh --agent claude --target /path/to/project --skill shell-quality

# Install to both agents in the current user's home directory
./scripts/install.sh --agent all --scope user --skill documentation-quality

# Install every skill into a project
./scripts/install.sh --agent all --target /path/to/project --all

# Remove only skills managed by this toolkit
./scripts/uninstall.sh --agent all --target /path/to/project --skill shell-quality
```

Agent paths:

| Agent | Project | User |
| --- | --- | --- |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |

Project-specific `AGENTS.md`, `CLAUDE.md`, CI, and build scripts remain in the consuming repository. This toolkit never writes those files.

## Validate and test

```bash
./scripts/validate.sh
python3 -m unittest discover -s tests -v
bash -n scripts/*.sh
```

## Safety and updates

- Installer runs without network requests; it does not execute project build tasks.
- Install/uninstall refuses to replace or remove unmanaged skills. Check `--dry-run` before edits.
- Symlink mode reads updates when the submodule revision changes; commit the new submodule pointer in the host repo to pin the revision.
- Copy mode snapshots the skill. To update a copied skill, remove the toolkit-owned copy using `uninstall.sh` and reinstall it.
- No skill may independently commit, push, publish a release, or deploy without explicit user authorization.
- Skills do not override organizational security controls. Only run code and external analyzers allowed by the consuming project.

## Repository layout

```text
engineering-agent-skills/
├── skills/
│   ├── java-quality/
│   ├── python-quality/
│   ├── shell-quality/
│   ├── build-automation-quality/
│   ├── container-quality/
│   ├── documentation-quality/
│   └── release-engineering/
├── scripts/
│   ├── skills.py
│   ├── install.sh
│   ├── uninstall.sh
│   └── validate.sh
├── tests/
├── evals/
├── .github/workflows/
├── AGENTS.md
└── CONTRIBUTING.md
```

## Status

This is an initial toolkit implementation. The Java Skill was adapted from an existing `java-oss-quality` review package, and other Skills are first-pass workflows. They need validation against real consumer repositories and agents before a stable release. Official documentation and real project contracts take precedence over tool assumptions.

Before publishing as an open-source project, add a license selected by the repository owner.
