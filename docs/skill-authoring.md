# Skill Authoring Guide

This guide defines recommended authoring and Markdown conventions for Engineering Agent Skills. The [Agent Skills specification](https://agentskills.io/specification) remains the authoritative format specification.

## Design principles

| Principle | Guidance |
| --- | --- |
| Single responsibility | Address one recurring engineering task. |
| Portability | Keep canonical instructions independent of agent implementations. |
| Composability | Use complementary skills without duplicating their responsibilities. |
| Progressive disclosure | Load additional resources only when relevant. |
| Evidence-based execution | Establish findings from observable behavior, contracts, and verification. |
| Context efficiency | Avoid redundant instructions and unnecessary detail. |
| Maintainability | Prefer clear, focused, and reusable instructions. |

## Directory structure

Use the canonical skill layout:

    skills/<skill-id>/
    ├── SKILL.md
    ├── references/
    ├── scripts/
    └── assets/

Only `SKILL.md` is required. Add resource directories when they serve a concrete purpose. Do not create empty directories.

## Frontmatter

Use standard fields defined by the Agent Skills specification.

| Field | Status |
| --- | --- |
| `name` | Required |
| `description` | Required |
| `license` | Optional |
| `compatibility` | Optional |
| `metadata` | Optional |
| `allowed-tools` | Experimental |

Write descriptions around the skill's responsibility, observable inputs, and activation conditions.

Avoid proprietary required fields and unnecessary client-specific metadata.

## Markdown structure

Use meaningful sections to separate distinct instruction types.

| Section | Purpose |
| --- | --- |
| Scope | Define responsibilities and boundaries. |
| Operating Modes | Distinguish supported execution modes. |
| Workflow | Describe the execution sequence. |
| Reference Selection | Explain when additional resources are relevant. |
| Constraints | Define restrictions and compatibility requirements. |
| Verification | Establish how results should be checked. |
| Expected Output | Describe the required deliverable. |
| Examples | Illustrate relevant behavior and edge cases. |

These sections are recommendations, not mandatory headings. Include only sections that improve the skill's clarity and execution.

## Markdown conventions

| Element | Usage |
| --- | --- |
| Level-one heading | Skill title |
| Level-two heading | Main instruction section |
| Level-three heading | Subsection within a complex workflow |
| Ordered list | Sequential execution steps |
| Unordered list | Independent requirements or constraints |
| Table | Operating modes, decision criteria, or reference selection |
| Bold text | Critical instructions and restrictions |
| Inline code | Identifiers, paths, commands, and technical terms |
| Fenced code block | Executable examples and structured snippets |
| Relative link | Skill-local resources |

Use tables for information that benefits from comparison or explicit selection criteria. Avoid tables when a short paragraph or list communicates the same instruction more clearly.

## Workflow design

Workflows should establish the task scope, identify relevant evidence, perform authorized actions, verify results, and communicate the outcome.

Use ordered steps when execution order matters. Separate conditional behavior from unconditional requirements.

Keep authorization boundaries explicit. Loading a supporting skill does not authorize actions outside the user's request.

## Skill composition

Select the primary skill according to the requested outcome.

Use supporting skills when their specialized guidance contributes relevant evidence or verification.

For example, a Java pull request review uses `code-review` as the primary workflow and `java-quality` for language-specific contracts and behavior.

Do not duplicate supporting skill instructions or assume that clients automatically load other skills.

## Progressive disclosure

Keep the entrypoint sufficient for common tasks.

Move substantial specialist guidance into focused resources and link them directly from `SKILL.md`.

| Resource | Purpose |
| --- | --- |
| `references/` | Detailed guidance, decision criteria, and technical examples |
| `scripts/` | Repeatable executable procedures |
| `assets/` | Static templates, schemas, and other supporting resources |

Explain when each reference should be loaded. Keep resource paths relative to the skill directory and avoid deeply nested reference chains.

Follow the specification's recommended instruction size limits. Prefer the smallest instruction set that preserves reliable task execution.

## Verification and evaluation

Validate every skill using the repository's existing quality gates.

Cover positive activation, plausible near misses, responsibility boundaries, and expected behavior through evaluation cases.

Distinguish deterministic fixture checks from live agent evaluations.

Formatting-only changes must preserve existing responsibilities, authorization boundaries, reference selection conditions, and expected behavior.

See the [evaluation protocol](../evals/README.md) and [contribution standards](../CONTRIBUTING.md).

## Authoring checklist

- The skill follows the official Agent Skills specification.
- The description identifies the intended task and activation conditions.
- Responsibilities do not unnecessarily overlap with adjacent skills.
- Markdown structure supports clear instruction execution.
- References have explicit selection conditions.
- Instructions preserve authorization and compatibility boundaries.
- Verification requirements are actionable.
- Examples and evaluation cases cover relevant behavior.
- Content avoids unnecessary repetition.
- Repository quality gates pass.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Repository architecture](architecture.md)
- [Contribution standards](../CONTRIBUTING.md)
- [Evaluation protocol](../evals/README.md)