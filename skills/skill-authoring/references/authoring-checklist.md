# Authoring quality review

Use this checklist when making scope, disclosure, size, script, or evaluation decisions. The repository's [canonical standard](../../../docs/skill-authoring.md) distinguishes format requirements from local recommendations.

## Review the skill

- **Capability:** one useful recurring outcome, grounded in real expertise, documented behavior, project artifacts, or execution evidence.
- **Boundary:** clear ownership and useful composition with neighboring skills; no broad overlap or unnecessary duplication.
- **Activation:** description states what it enables and when it applies, centered on user intent. Include useful terminology and realistic trigger conditions without stuffing keywords.
- **Procedure:** actionable ordered steps where order matters, concrete defaults, justified alternatives, non-obvious gotchas, and checks that expose success or failure.
- **Risk and permission:** specificity matches operational risk; review, planning, and implementation are distinguished; destructive or externally visible actions require authorization.
- **Context:** aim for 30–100 lines and under 1,500 tokens for most entrypoints. These are local advisory targets. The official best-practice ceiling is under 500 lines and 5,000 tokens. Never delete necessary instructions to meet a target. Keep task-specific detail in directly linked, conditionally loaded resources.
- **Resources:** every reference has a purpose and loading condition; no all-reference default, dead links, deep chains, or copied external pages. Scripts solve repeatable work, run predictably and non-interactively, explain prerequisites and side effects, and are tested. Assets have a reusable purpose.
- **Portability:** use standard frontmatter and avoid relying on undocumented client behavior. Link authoritative sources for version-sensitive behavior.
- **Evidence:** define expected output, edge cases, and observable checks. Structural validity is not proof of useful routing or results.

## Practical gotchas

- Similar vocabulary can hide different intent. Use near-miss prompts that share terms but need another skill, alongside true composition cases.
- A reference cannot protect the common workflow if its loading trigger is hard to recognize. Keep that gotcha in the entrypoint.
- A short skill can still be vague; a longer one can be justified by operational risk. Optimize for reliable execution, not line count.
- A bundled script may be invoked from a different working directory. Resolve paths predictably and document the invocation location.
- Evaluation prompts and rubrics must not be copied into consumer instructions or fixtures.

## Sources

- [Agent Skills specification](https://agentskills.io/specification) for format requirements.
- [Best practices](https://agentskills.io/skill-creation/best-practices) for expertise, context use, detail, and workflow patterns.
- [Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) for activation and routing tests.
- [Using scripts](https://agentskills.io/skill-creation/using-scripts) for bundled executable design.
- [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills) for behavioral comparisons.
