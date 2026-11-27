# Phase 2.8 catalog audit

This record tracks the Phase 2.8 inspection and the changes made so far. All 35 entrypoints were reviewed for frontmatter, trigger clarity, scope, workflow, authorization, reference selection, and verification. Existing workflows were retained when they already gave task-specific steps and boundaries; the audit did not impose shared headings or blanket rewrites.

| Category | Skills reviewed | Findings and decisions |
| --- | --- | --- |
| Software Engineering | `code-review`, `java-quality`, `python-quality`, `refactoring`, `shell-quality` | Existing scopes and review/edit boundaries were useful. Java now includes concurrency, runtime diagnostics, type contracts, Spring transactions/Boot, Quarkus, Native Image, persistence, virtual threads, and design trade-offs. Python now covers async lifecycle, typing, object/runtime concurrency, FastAPI, Pydantic, and SQLAlchemy. Shell guidance distinguishes Bash-only process substitution and options from POSIX intent; official POSIX wording remains partially inaccessible (see limitations). |
| Software Architecture | `api-design`, `architecture-decision`, `architecture-review`, `system-design` | Kept separate deliverables for contracts, decisions, assessment, and proposed design. Added bounded consistency guidance for modular monoliths, dual writes/outbox, idempotency, retries, and schema evolution without prescribing distributed services. |
| Bug Fixing and Reliability | `bug-fixing`, `bug-investigation`, `incident-analysis`, `performance-analysis`, `root-cause-analysis` | Kept correction separate from diagnosis and systemic analysis. Added environment comparison, smallest failing boundary, mitigation versus correction, multi-line hotfix follow-through, evidence confidence, recovery verification, optional causal methods, and SLI/SLO-aware alerting without inventing targets. |
| Testing and Quality Assurance | `integration-testing`, `security-review`, `test-strategy`, `unit-testing` | Kept risk planning, unit behavior, cross-boundary behavior, and defensive assessment distinct. Added conditional JUnit Jupiter, Mockito, pytest, and Testcontainers guidance for fixture/lifecycle isolation, assertion boundaries, container readiness, and runtime prerequisites. Added defensive SSRF, authorization, and path-traversal review cues. |
| Software Delivery | `build-automation-quality`, `ci-cd`, `container-quality`, `dependency-management`, `deployment`, `git-workflow`, `release-engineering` | Kept build graph, pipeline, runtime image, dependency graph, rollout, repository history, and release artifact responsibilities distinct. Added release lifecycle and hotfix/backport guidance; conditional GitHub Actions, GitLab CI/CD, and Jenkins references; Kubernetes/Helm rollout references; and separate Maven, Gradle, GNU Make, and Taskfile references. Existing build reproducibility and container cache/platform references remain. |
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

The reference expansion is incremental, not exhaustive. Fifteen evaluation cases were added for release/backport, deployment failure, provider-specific CI artifact flow, framework/runtime failure boundaries, test lifecycle isolation, SLO target selection, and architecture/security risks. Structural validation does not establish agent behavior; no model evaluations were run.

### Remaining high-priority work

- Add Flask, Django, and broader Python framework coverage only when concrete repository patterns justify separate references; FastAPI, Pydantic, and SQLAlchemy now have conditional references.
- Add JUnit API-specific guidance only after the repository's pinned JUnit version and its version-matched official documentation can be verified; current guidance is deliberately limited to stable lifecycle, discovery, and isolation practices.
- Deepen security and architecture topics from authoritative use cases. Do not add generic technology catalogs or duplicate framework mechanics across skills.

### Deferred and unverified

- Micronaut, Jakarta EE, additional Python web frameworks, Terraform/GitOps platforms, and other CI providers were deferred as lower priority.
- GNU Bash 5.3 official manual search results were accessible for command/process substitution; direct manual retrieval timed out. A local behavior probe on macOS Bash 3.2 confirmed that a failing process substitution does not make the enclosing `diff` fail. The POSIX specification endpoint returned HTTP 403 and targeted searches returned no indexed excerpts. Beyond identifying process substitution and `pipefail` as Bash-specific, no new POSIX-specific behavior claims were added; verify the related existing portability guidance against the relevant published clauses when access is available.
- The current JUnit User Guide endpoint timed out. JUnit guidance remains limited to version-qualified test discovery, lifecycle, parameterization, and assertion practices; confirm exact APIs/defaults against the repository's pinned Jupiter version.
- Framework defaults and command flags are version-sensitive. References instruct agents to inspect the repository's pinned framework/tool versions before applying them.
