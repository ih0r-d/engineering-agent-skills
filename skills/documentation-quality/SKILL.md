---
name: documentation-quality
description: Write, review, or verify READMEs, quick starts, consumer guides, architecture and contributor docs, API reference, JavaDoc, Python docstrings, and examples. Use to investigate documentation drift or broken instructions.
---

# Documentation Quality

1. Identify the audience, task and supported release or branch. For drift review, start with changed commands, API signatures, defaults or setup and trace them to the affected pages. Inventory the documentation only for a requested audit.
2. Read [consumer documentation](references/consumer-docs.md) for README, quick start or how-to work, [maintainer documentation](references/technical-docs.md) for architecture and contributing, or [API and examples](references/api-and-examples.md) for contract prose, JavaDoc, docstrings and snippets.
3. Verify claims against the consuming repository's actual CLI, API, tests and release or CI config. Check local links and rendered anchors with the repository's docs tools when available. Exercise safe commands and snippets with the stated prerequisites and working directory, using an isolated environment. Record claims and links that could only be inspected.
4. Review mode leaves documents untouched. Draft or fix mode changes the requested material and follows its existing terminology. Verification mode runs applicable checks without rewriting docs. Keep one canonical explanation per contract and add links from other contexts. Use direct task steps for consumers and record trade-offs and invariants where maintainers need them.
5. Report actionable drift with severity, location, the conflicting behavior or output, smallest correction and verification. Prioritize broken journeys and misleading contracts over stylistic preferences. Keep complete non-sensitive check logs locally.

Keep proposed features and supported behavior distinct. Use the language review workflow for API implementation changes and the release workflow for publication.
