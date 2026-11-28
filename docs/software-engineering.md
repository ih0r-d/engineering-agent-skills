# Software Engineering skill boundaries

Choose the workflow by the requested outcome. Use repository evidence and explicit user requirements to identify the relevant language, framework, and version. Read the references that match both the task and the technology.

| Workflow | When to use it | Observable outcome |
| --- | --- | --- |
| [Implement](../skills/software-engineering/implement/SKILL.md) | Implement a feature or make an intentional change to behavior. | An authorized source change verified against its acceptance criteria. |
| [Review Code](../skills/software-engineering/review-code/SKILL.md) | Assess a pull request, patch, or scoped implementation. | Findings with a triggering condition, practical impact, and a verification step. Review stays read-only. |
| [Refactor Code](../skills/software-engineering/refactor-code/SKILL.md) | Improve structure within an observable behavior baseline. | A structural change with verification of preserved caller contracts. |
| [Debug](../skills/bug-fixing-and-reliability/debug/SKILL.md) | Investigate a failure or apply an authorized defect correction. | Supported cause and next check or a scoped fix with regression evidence. |

A read-only Java pull request review uses Java compatibility or runtime criteria where relevant. An authorized Python defect correction uses the guidance in Debug when it applies to the affected caller contract. A shell failure investigation starts with the actual interpreter and uses runtime references when they explain the symptom. For uncovered technologies, the workflow still applies using local conventions and checks.

A structural change preserves observable behavior at public entrypoints. Report any discovered defect that would require a separately authorized behavior change. [Definition of refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html)
