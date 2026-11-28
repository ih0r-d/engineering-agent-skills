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

Implementation, refactoring, debugging, and code review may delegate independent work when the client supports subagents and the task permits it. The primary agent owns integration and verification. Each workflow also runs sequentially.

## Workflow boundaries and v2 migration

The [catalog](catalog.json) lists the approved IDs and their category assignments. This table maps all 35 original IDs to their v2 destinations.

| v2 workflow | Responsibility and observable outcome | Original IDs |
| --- | --- | --- |
| `implement` | Make an authorized feature or intentional behavior change and verify its acceptance criteria. | Shared implementation guidance from `java-quality`, `python-quality`, and `shell-quality`. |
| `review-code` | Assess a patch or scoped code change and report read-only, evidence-backed findings. | `code-review` and review guidance from the former language skills. |
| `refactor-code` | Improve code structure and verify that callers observe the same behavior. | `refactoring` and minimal-change guidance from `java-quality`. |
| `design-system` | Propose a system design or interface contract, or evaluate and record an architectural decision. | `system-design`, `api-design`, `architecture-decision`, and Java design guidance from `java-quality`. |
| `review-architecture` | Assess the existing system against its requirements and report supported risks and trade-offs. | `architecture-review`. |
| `debug` | Diagnose failures or systemic causes, or apply and verify a scoped defect correction in authorized Fix mode. | `bug-investigation`, `root-cause-analysis`, `bug-fixing`, and diagnostic and correction guidance from `java-quality`, `python-quality`, and `shell-quality`. |
| `analyze-performance` | Measure or characterize performance and report evidence about bottlenecks or efficiency. | `performance-analysis`. |
| `analyze-incident` | Establish incident impact, response, recovery, and follow-up in an evidence-based report. | `incident-analysis`. |
| `test-code` | Produce a risk-based test plan, authorized test changes, or verification evidence. | `test-strategy`, `unit-testing`, `integration-testing`, and shell verification guidance from `shell-quality`. |
| `review-security` | Conduct a defensive assessment and report actionable security findings. | `security-review`. |
| `maintain-build` | Review or repair build graphs, artifacts, and dependency resolution. | `build-automation-quality`, `dependency-management`, and packaging guidance from `python-quality`. |
| `maintain-containers` | Review or repair a container image build, runtime configuration, or local service orchestration. | `container-quality`. |
| `manage-ci-cd` | Design, review, or repair pipeline triggers, jobs, artifacts, and gates. | `ci-cd`. |
| `manage-git` | Plan or execute authorized repository history operations and validate commit messages. | `git-workflow`. |
| `release-software` | Assess release readiness, prepare artifacts and notes, or carry out authorized publication. | `release-engineering`. |
| `deploy` | Plan or review a rollout or recovery, or execute and verify an authorized deployment. | `deployment`. |
| `clarify-requirements` | Resolve or record stakeholder ambiguities, priorities, and blocking decisions. | `requirements-analysis` for elicitation and clarification. |
| `write-spec` | Draft, review, or update a durable specification with traceable acceptance criteria. | Requirements and acceptance-criteria guidance from `requirements-analysis`. |
| `plan-work` | Sequence a scoped implementation or split a delivery objective into independently verifiable work items. | `implementation-planning`, `task-decomposition`. |
| `write-docs` | Write, review, or verify engineering documentation against current behavior. | `documentation-quality`. |
| `handoff` | Transfer verified state, decisions, open issues, and next steps. | `engineering-handoff`. |
| `author-skills` | Create, review, or improve a portable skill and its resources. | `skill-authoring`. |
| `evaluate-skills` | Define or assess controlled evaluation of skill behavior. | `skill-evaluation`. |
| `manage-agent-context` | Select and preserve context, refine a prompt, or measure token efficiency. | `context-engineering`, `prompt-engineering`, `token-optimization`. |

For an installed revision with replaced IDs, use the [upgrade and uninstall guidance](docs/compatibility.md#migrating-to-v2).
