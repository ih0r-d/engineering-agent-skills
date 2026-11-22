---
name: python-quality
description: Review and improve Python correctness, typing, APIs, maintainability, tests, and project tooling. Use for Python code audits or requested focused cleanup.
---

# Python Quality

1. Identify Python version, packaging metadata, lint/type/test tooling, repository rules, and requested scope. Preserve unrelated work.
2. For read-only review, inspect imports, control flow, error handling, async behavior, resources, security boundaries, typing, performance hot spots, and tests; do not edit.
3. Read [quality-rubric.md](references/quality-rubric.md) when evaluating Python-specific patterns or tools.
4. When changes are authorized, apply the smallest correctness-first fix and focused tests. Avoid introducing frameworks or type scaffolding without value.
5. Prefer installed Ruff, Pyright/mypy, pytest, and existing project commands, without changing project dependencies or tool config just to complete an audit.
6. Report evidence with path:line, impact, verification and any unrun tools. Never auto-commit or push.
