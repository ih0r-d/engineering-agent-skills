# Phase 2.8 catalog audit

This record tracks the Phase 2.8 inspection and the changes made so far. All 35 entrypoints were reviewed for frontmatter, trigger clarity, scope, workflow, authorization, reference selection, and verification. Existing workflows were retained when they already gave task-specific steps and boundaries; the audit did not impose shared headings or blanket rewrites.

| Category | Skills reviewed | Findings and decisions |
| --- | --- | --- |
| Software Engineering | `code-review`, `java-quality`, `python-quality`, `refactoring`, `shell-quality` | Existing scopes and review/edit boundaries were useful. Java now includes concurrency, runtime diagnostics, type contracts, Spring transactions/Boot, Quarkus, Native Image, persistence, virtual threads, and design trade-offs. Python now covers async lifecycle, typing, object/runtime concurrency, FastAPI, Pydantic, and SQLAlchemy. Shell guidance distinguishes Bash-only process substitution and options from POSIX intent; official POSIX wording remains partially inaccessible (see limitations). |
| Software Architecture | `api-design`, `architecture-decision`, `architecture-review`, `system-design` | Kept separate by deliverable: contract, one decision record, assessment of existing architecture, and proposed design. Existing references provide criteria and avoid prescriptive architecture patterns. |
| Bug Fixing and Reliability | `bug-fixing`, `bug-investigation`, `incident-analysis`, `performance-analysis`, `root-cause-analysis` | Kept implementation correction separate from diagnosis and systemic/incident analysis. Added environment comparison, smallest failing boundary, mitigation versus correction, multi-line hotfix follow-through, evidence confidence, recovery verification, and optional causal-analysis methods without forcing one root cause. |
| Testing and Quality Assurance | `integration-testing`, `security-review`, `test-strategy`, `unit-testing` | Kept risk planning, unit behavior, cross-boundary behavior, and defensive assessment distinct. Added conditionally loaded JUnit Jupiter, Mockito, pytest, and Testcontainers references covering fixture/lifecycle isolation, assertion boundaries, container readiness, and runtime prerequisites. Existing authorization constraints remain. |
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

The reference expansion is incremental, not exhaustive. Eight evaluation cases were added for release/backport, deployment failure, provider-specific CI artifact flow, Quarkus event-loop blocking, FastAPI dependency ownership, SQLAlchemy session concurrency, and shell portability. Structural validation does not establish agent behavior; no model evaluations were run.

### Remaining high-priority work

- Expand maintenance/reliability guidance with operationally grounded SLI/SLO, observability, and failed-release response material where existing performance and root-cause references leave gaps.
- Add Flask, Django, and broader Python framework coverage only when concrete repository patterns justify separate references; FastAPI, Pydantic, and SQLAlchemy now have conditional references.
- Deepen security and architecture topics from authoritative use cases. Do not add generic technology catalogs or duplicate framework mechanics across skills.

### Deferred and unverified

- Micronaut, Jakarta EE, additional Python web frameworks, Terraform/GitOps platforms, and other CI providers were deferred as lower priority.
- GNU Bash 5.3 official manual search results were accessible for shell expansion behavior, but direct manual retrieval timed out. The POSIX specification endpoint returned HTTP 403 and targeted searches returned no indexed excerpts. POSIX-specific claims should be rechecked against the relevant published clauses before expanding them; no new detailed POSIX semantics were asserted here.
- The current JUnit User Guide endpoint timed out. JUnit guidance remains limited to version-qualified test discovery, lifecycle, parameterization, and assertion practices; confirm exact APIs/defaults against the repository's pinned Jupiter version.
- Framework defaults and command flags are version-sensitive. References instruct agents to inspect the repository's pinned framework/tool versions before applying them.
