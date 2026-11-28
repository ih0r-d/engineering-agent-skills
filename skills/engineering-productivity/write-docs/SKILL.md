---
name: write-docs
description: Write, review, or verify READMEs, quick starts, consumer guides, architecture and contributor docs, API reference, JavaDoc, Python docstrings, and examples. Use to investigate documentation drift or broken instructions.
---

# Write Documentation

## Operating Modes

| Mode | Responsibility |
| --- | --- |
| Review | Inspect documentation and report findings without editing. |
| Draft or Fix | Change the requested material and follow its existing terminology. |
| Verification | Run applicable checks without rewriting documentation. |

## Workflow

1. Identify the audience, task and supported release or branch.
2. For drift review, start with changed commands, API signatures, defaults or setup and trace them to the affected pages. Inventory the documentation only for a requested audit.
3. Load relevant references according to the documentation type.
4. Verify claims against the consuming repository's actual CLI, API, tests and release or CI configuration.
5. Check local links and rendered anchors with the repository's documentation tools when available.
6. Exercise safe commands and snippets with the stated prerequisites and working directory, using an isolated environment.
7. Record claims and links that could only be inspected.
8. Keep complete non-sensitive check logs locally.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Consumer documentation](references/consumer-docs.md) | Writing or reviewing READMEs, quick starts or how-to guides. |
| [Maintainer documentation](references/technical-docs.md) | Writing or reviewing architecture and contribution documentation. |
| [API and examples](references/api-and-examples.md) | Reviewing contract prose, JavaDoc, docstrings or code snippets. |

## Constraints

- Keep one canonical explanation per contract and add links from other contexts.
- Use direct task steps for consumers.
- Record trade-offs and invariants where maintainers need them.
- Prioritize broken user journeys and misleading contracts over stylistic preferences.
- Keep proposed features and supported behavior distinct.
- Use the language review workflow for API implementation changes.
- Use the release workflow for publication.

## Expected Output

For each actionable documentation finding, report:

- Severity and location.
- Conflicting behavior or output.
- Smallest applicable correction.
- Verification result.

Distinguish verified claims from claims that could only be inspected.
