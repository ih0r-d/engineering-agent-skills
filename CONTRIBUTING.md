# Contributing

Skills must solve a recognizable, recurring engineering task and have clear activation criteria.

1. Create `skills/<skill-name>/SKILL.md` with `name` and `description` frontmatter.
2. Keep `SKILL.md` focused; put specialized checks into `references/` and deterministic work in `scripts/`.
3. Separate read-only review from fixes, and prevent implicit commit, push, deploy, or publishing.
4. Never assume a project's build tool, language version, CI system, or available executables.
5. Use evidence from tests, call sites, and relevant repository instructions. Minimize token-heavy logs.
6. Run `python3 scripts/skills.py validate` and `python3 -m unittest discover -s tests -v`.

New skills should include at least one positive and one negative evaluation scenario under `evals/` when behavior is nontrivial.
