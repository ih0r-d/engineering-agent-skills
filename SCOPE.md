# Engineering Agent Skills scope

Engineering Agent Skills is a toolkit of portable, technology-agnostic workflows. A skill addresses an engineering task and guides the agent from scope and evidence through execution and verification. Focused references provide the technical details needed for that task. The [catalog](catalog.json) records the 24 v2 skill IDs and their categories.

## Extension policy

| Proposed addition | Default home |
| --- | --- |
| Programming language, framework, build tool, or platform | A focused reference in the workflow that uses the expertise. |
| Distinct engineering workflow | A skill when it has a distinct objective, activation boundary, and observable outcome. |
| Repeatable automation | A script when deterministic execution materially helps the workflow. |
| Reusable deliverable | An asset when a template or data file helps produce a recurring outcome. |

A skill's entrypoint identifies the requested outcome and respects explicit user technology requirements. It uses relevant repository evidence to determine the technology and version where possible. Each substantial reference has a direct link and a task-specific loading condition. When the evidence or a matching guide is unavailable, the agent follows the generic workflow and project conventions. Each package contains the resources it needs when installed alone.

Keep guidance focused on its owning workflow. Add a language's compatibility criteria to code review, its runtime diagnostics to debugging, and its test framework guidance to test code. Use nested directories where they help discover substantial technical material. The client selects skills and reads resources using its native capabilities. [Skill authoring standard](docs/skill-authoring.md)

Implementation and code review may delegate independent work when the client supports subagents and the task permits it. The primary agent owns integration and verification. Each workflow also runs sequentially.

## Workflow boundaries and v2 migration

| v2 skill | Activation and observable outcome | Earlier skill IDs |
| --- | --- | --- |
| `implement` | A scoped source change, confirmed defect fix, or behavior-preserving refactor. Produces an authorized change and verification against acceptance criteria and affected contracts. | `refactoring`, `bug-fixing`. Language implementation guidance from `java-quality`, `python-quality`, and `shell-quality`. |
| `review-code` | A PR, patch, or scoped source review. Produces read-only findings on specification compliance, coding standards, correctness, code smells, and maintainability. | `code-review`. Review guidance from `java-quality`, `python-quality`, and `shell-quality`. |
| `debug` | A failure or recurring problem whose cause needs evidence. Produces a bounded diagnosis, confidence level, and verification or prevention criteria. | `bug-investigation`, `root-cause-analysis`. Runtime guidance from `java-quality`, `python-quality`, and `shell-quality`. |
| `test-code` | A test strategy, test change, test review, or verification request. Produces a risk-based plan or tests and measured results where executed. | `test-strategy`, `unit-testing`, `integration-testing`. Shell verification guidance from `shell-quality`. |
| `maintain-build` | A build, package, or resolution problem. Produces verified graph, artifact, or dependency findings and changes within scope. | `build-automation-quality`, `dependency-management`. Packaging guidance from `python-quality`. |
| `design-system` | A system proposal, architecture assessment, interface contract, or ADR. Produces the requested design or decision artifact with evidence and validation criteria. | `system-design`, `architecture-review`, `api-design`, `architecture-decision`. Design guidance from `java-quality`. |
| `manage-ci-cd` | A pipeline design, review, or repair. Produces verified workflow changes or findings about triggers, jobs, artifacts, and gates. | `ci-cd`. |
| `deploy` | A rollout or recovery plan, review, or explicitly authorized deployment. Produces rollout gates and recovery criteria, with runtime evidence when executed. | `deployment`. |

The following original skills retain their IDs.

| Category | Original and v2 skill IDs |
| --- | --- |
| Bug Fixing and Reliability | `incident-analysis`, `performance-analysis` |
| Testing and Quality Assurance | `security-review` |
| Software Delivery | `container-quality`, `git-workflow`, `release-engineering` |
| Engineering Productivity | `documentation-quality`, `engineering-handoff`, `implementation-planning`, `requirements-analysis`, `task-decomposition` |
| AI Engineering | `context-engineering`, `prompt-engineering`, `skill-authoring`, `skill-evaluation`, `token-optimization` |

`requirements-analysis` also owns drafting, reviewing, and updating specifications. `implementation-planning` sequences the work against those requirements. `implement` verifies authorized changes against the specification, and `review-code` checks the resulting change for compliance. [Upgrade and uninstall guidance](docs/compatibility.md#migrating-to-v2)
