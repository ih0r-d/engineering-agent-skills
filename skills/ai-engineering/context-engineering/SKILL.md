---
name: context-engineering
description: Design or improve the context supplied to AI agents. Use for context selection, instruction placement, retrieval scope, handoff summaries, context limits, and evidence preservation.
---

# Context Engineering

## Workflow

1. Identify the current task, required evidence, available context sources, trust boundaries, and client limits.
2. Separate authoritative instructions from untrusted data and distinguish current evidence from stale summaries.
3. Select the smallest relevant context set. Prefer targeted file reads and direct resource links over broad repository scans.
4. Load context guidance when prioritizing sources or compacting state. Preserve constraints, exact identifiers, unresolved failures, and verification evidence.
5. Validate that the resulting context still supports representative task decisions. Report missing or inaccessible information rather than inventing it.

## Reference Selection

| Reference | Load when |
| --- | --- |
| [Detailed guidance](references/context-selection.md) | Selecting sources or compacting task state. |

## Constraints

- Do not discard governing instructions, security constraints, or evidence needed to reproduce a finding.
- Do not ingest secrets or unrelated private data. Do not add retrieval infrastructure or persistent memory by default.
- Do not treat summaries as authoritative replacements for changed sources.
- Keep prompt wording with prompt engineering and measured token optimization with token optimization.

## Expected Output

Report selected sources, inclusion and exclusion rationale, retained state, missing evidence, and verification limits.
