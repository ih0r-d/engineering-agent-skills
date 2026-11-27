# Phase 2.8 catalog audit

This record tracks the Phase 2.8 inspection and the changes made so far. All 35 entrypoints were reviewed for frontmatter, trigger clarity, scope, workflow, authorization, reference selection, and verification. Existing workflows were retained when they already gave task-specific steps and boundaries; the audit did not impose shared headings or blanket rewrites.

| Category | Skills reviewed | Findings and decisions |
| --- | --- | --- |
| Software Engineering | `code-review`, `java-quality`, `python-quality`, `refactoring`, `shell-quality` | Existing scopes and review/edit boundaries were useful. Java needed concrete concurrency, runtime diagnostic, type-contract, Spring transaction, virtual-thread, and persistence selection paths. Python needed async lifecycle and typing contract references. Shell needed explicit process/trap lifecycle guidance. |
| Software Architecture | `api-design`, `architecture-decision`, `architecture-review`, `system-design` | Kept separate by deliverable: contract, one decision record, assessment of existing architecture, and proposed design. Existing references provide criteria and avoid prescriptive architecture patterns. |
| Bug Fixing and Reliability | `bug-fixing`, `bug-investigation`, `incident-analysis`, `performance-analysis`, `root-cause-analysis` | Kept implementation correction separate from diagnosis and systemic/incident analysis. Existing checklists cover evidence confidence, reproduction, measurement, and follow-up; no overlapping workflow rewrite was justified. |
| Testing and Quality Assurance | `integration-testing`, `security-review`, `test-strategy`, `unit-testing` | Kept risk planning, unit behavior, cross-boundary behavior, and defensive assessment distinct. Existing authorization and environment constraints are concrete; retain them. |
| Software Delivery | `build-automation-quality`, `ci-cd`, `container-quality`, `dependency-management`, `deployment`, `git-workflow`, `release-engineering` | Kept build graph, pipeline, runtime image, dependency graph, rollout, repository history, and release artifact responsibilities distinct. Added explicit build reproducibility and container cache/platform references. |
| Engineering Productivity | `documentation-quality`, `engineering-handoff`, `implementation-planning`, `requirements-analysis`, `task-decomposition` | Kept authoring, handoff, implementation sequence, requirement definition, and work-item decomposition distinct. Existing observable deliverables and stop boundaries are adequate. |
| AI Engineering | `context-engineering`, `prompt-engineering`, `skill-authoring`, `skill-evaluation`, `token-optimization` | Kept context selection, prompt construction, reusable skill design, behavioral evaluation, and measured efficiency separate. Composition is conditional; none requires loading another skill. |

## Cross-skill routing decisions

- Code review owns findings about a proposed change; language-quality skills provide technical evidence without authorizing edits.
- Bug investigation establishes symptoms and hypotheses; bug fixing changes behavior; root-cause analysis examines causal and systemic factors; incident analysis owns the incident record.
- Performance analysis owns measurement design; language-specific skills contribute runtime diagnostics when the implementation language matters.
- System design proposes a system, architecture review assesses an existing one, and architecture decision records one bounded choice. API design owns consumer-facing interface semantics.
- Test strategy chooses risk coverage; unit and integration testing implement or verify at their respective boundaries.
- CI/CD owns pipeline graphs; build automation owns build-tool semantics. Release engineering verifies artifacts; deployment owns rollout and runtime recovery.
- Implementation planning sequences a scoped change; task decomposition creates independently verifiable work items.
- Prompt engineering edits prompts; context engineering chooses evidence and instructions; token optimization reports only measured efficiency.
- Skill authoring defines the reusable workflow; skill evaluation measures its observed behavior.

## Remaining depth work

The reference expansion is incremental, not a claim that every requested topic has been exhaustively documented. Java static-analysis and performance details are currently covered by focused existing references and can be deepened with concrete project needs. Python packaging, testing, and static-analysis expertise is concentrated in existing references and can be split when task-driven depth requires it. Broader security standards, deployment systems, and framework-specific cases should be added from concrete use cases rather than generic keyword coverage.
