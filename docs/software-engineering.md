# Software Engineering skill boundaries

Choose the workflow by the requested outcome. Use repository evidence and explicit user requirements to identify the relevant language, framework, and version. Read the references that match both the task and the technology.

| Workflow | When to use it | Observable outcome |
| --- | --- | --- |
| [Implement](../skills/software-engineering/implement/SKILL.md) | Change a contract, apply a confirmed fix, or refactor existing code. | A scoped change with evidence for new behavior or a baseline for preserved behavior. |
| [Review Code](../skills/software-engineering/review-code/SKILL.md) | Assess a pull request, patch, or scoped implementation. | Findings with a triggering condition, practical impact, and a verification step. Review stays read-only. |
| [Debug](../skills/bug-fixing-and-reliability/debug/SKILL.md) | Investigate a failure, such as an ignored result or missing runtime resource. | A bounded explanation of the failure with evidence, confidence, and the next check. |

A read-only Java pull request review uses Java compatibility or runtime criteria where relevant. An authorized Python fix uses implementation guidance for the affected caller contract. A shell failure investigation starts with the actual interpreter and uses runtime references when they explain the symptom. For uncovered technologies, the workflow still applies using local conventions and checks.

A structural change preserves observable behavior at public entrypoints. Report any discovered defect that would require a separately authorized behavior change. [Definition of refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html)
