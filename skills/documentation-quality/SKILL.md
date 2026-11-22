---
name: documentation-quality
description: Create or review concise, accurate developer documentation, user guides, architecture docs, JavaDoc, Python docstrings, and working examples.
---

# Documentation Quality

1. Identify the audience and artifact type; do not load all references automatically.
2. For README, setup, configuration and troubleshooting, use [consumer-docs.md](references/consumer-docs.md).
3. For architecture, lifecycle, design decisions, operational constraints and contributor guides, use [technical-docs.md](references/technical-docs.md).
4. For JavaDoc, Python docstrings, API contract notes and executable examples, use [api-and-examples.md](references/api-and-examples.md).
5. Verify facts against code, actual CLI/API contracts, configuration, tests, and available examples. Fix dead links and contradictions, not merely style.
6. In review-only requests, report actionable gaps without editing. Write or update docs only when requested; minimize duplication and avoid invented guarantees.
7. Prefer short, scannable, task-oriented explanations for consumers and precise tradeoffs for maintainers. Never auto-commit or push.
