# Repository instructions

This repository contains portable, offline-first engineering skills for AI coding agents.

- Use English for Skill files, source code, comments, documentation, and commit messages.
- Follow the Agent Skills format: one concise `SKILL.md` per skill, with optional references and scripts.
- Keep skill descriptions focused on the actual trigger; do not add universal or always-on instructions.
- Keep project-specific policies out of general skills. The consuming repository's instructions take precedence.
- Never change consuming projects, dependencies, build files, tags, or remote state without explicit authorization.
- Be evidence-based; treat tool findings as signals to verify, not mandatory refactoring instructions.
- Prefer small, reversible local operations, standard-library tools, no network calls, and short reports.
- Before editing installer behavior, run `python3 scripts/skills.py validate` and `python3 -m unittest discover -s tests -v`.
- Protect unrelated user changes. Never auto-commit or push.
