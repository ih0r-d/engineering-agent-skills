# Maintaining Engineering Agent Skills

These instructions govern maintenance of this toolkit, including when it is checked out as a submodule. Installed Skills follow the consuming project's instructions. `skills/` contains the shared definitions, `.scripts/` contains the installer and validation tooling, and `scripts/` preserves historical entrypoints. `tests/` and `evals/` cover deterministic checks and agent behavior.

## Develop Skills

- Write Skills, code, comments, documentation and commit messages in English.
- Every skill must pass the mandatory Agent Skills specification gate. Use one `skills/<skill-id>/SKILL.md` with a matching frontmatter name and a description keyed to the actual task. Use standard fields and register the skill in one category in `catalog.json`. [Agent Skills specification](https://agentskills.io/specification), [Repository architecture](docs/architecture.md)
- Keep the entrypoint operational and concise. The repository targets 30–100 lines and fewer than 1,500 tokens as advisory goals; the official recommendation is under 500 lines and 5,000 tokens. Do not remove necessary guidance to meet a target. Follow the [canonical authoring standard](docs/skill-authoring.md); keep consumer policy with the consumer.
- State review, edit and verification boundaries. Start with the relevant changes, verify tool signals against behavior, and prefer the smallest supported change. Load only relevant references, reuse checks when inputs are unchanged, and summarize useful evidence.
- Use [templates/SKILL.md](templates/SKILL.md) as an adaptable starting point; headings, references, scripts, and assets are conditional choices, not requirements.

## Maintain installation and verification

- Keep the installer offline and standard-library-only. Require an explicit Skill selection, preserve both agents' project and user paths, and keep relative directory links, copy mode, dry runs and ownership checks working. Preserve consumer instructions, build files and unrelated paths. Use disposable targets and synthetic data for integration checks.
- Run `python3 .scripts/skills.py validate` and `python3 -B -m unittest discover -s tests -v` before changing installer behavior and after relevant changes. Run `task ci` before completing a change. It includes the pinned specification gate and deterministic regression tests. Add focused coverage for changed behavior. Use positive and misleading cases when skill routing changes, and keep model evaluations separate from offline tests. [Evaluation protocol](evals/README.md)
- Inspect Git status before editing and review the final diff and check results. Preserve unrelated work. Require explicit authorization for consumer project changes, dependency or build changes, staging, commits, tags, pushes and other remote actions.
