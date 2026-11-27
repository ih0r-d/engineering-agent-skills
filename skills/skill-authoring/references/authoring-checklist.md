# Authoring Checklist

| Decision | Default |
| --- | --- |
| Scope | One coherent recurring engineering outcome; merge overlapping responsibilities when justified. |
| Description | Observable user intent and task triggers, not a generic capability list. |
| Instructions | Concrete defaults, non-obvious pitfalls, and a bounded verification loop. |
| References | Direct relative links with explicit loading conditions; no repeated main instructions. |
| Scripts | Deterministic repeated work with clear inputs, errors, and safe defaults. |

## Gotchas

- A valid manifest can still route incorrectly. Compare adjacent descriptions and test near misses.
- Avoid embedding entire reference documents or mandatory boilerplate in every skill.
- Prefer existing tools; scripts should be noninteractive, document dependencies and exit codes, and support preview for risky writes when practical.
- Keep test rubrics outside consumer fixtures.

## Official guidance

- [Specification](https://agentskills.io/specification)
- [Best practices](https://agentskills.io/skill-creation/best-practices)
- [Using scripts](https://agentskills.io/skill-creation/using-scripts)
