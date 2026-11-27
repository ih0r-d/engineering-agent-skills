# Skill Authoring Standard

This is the canonical repository guide for creating and changing portable Agent Skills. The [Agent Skills specification](https://agentskills.io/specification) defines format requirements; this guide adds repository recommendations. Consumer project policy remains with the consumer.

## Format requirements

Every skill directory contains `SKILL.md` with YAML frontmatter and Markdown instructions. Required `name` must match the directory, be 1–64 lowercase letters, digits, or hyphens, have no leading/trailing or consecutive hyphens. Required `description` must be non-empty and no more than 1024 characters, and describe both capability and use conditions. Optional standard fields are `license`, `compatibility` (up to 500 characters), `metadata` (string keys and values), and experimental `allowed-tools`. Use no non-standard fields as requirements. The official body format does not require particular headings.

## Repository recommendations

- Design one coherent engineering capability with explicit responsibility boundaries. Compose with adjacent skills when their expertise helps; do not copy their procedures.
- Ground guidance in real tasks, project artifacts, documented behavior, and observed failure modes. Prefer actionable procedures, a clear default, and justified alternatives. Match instruction specificity to operational risk and preserve authorization boundaries.
- Describe user intent and activation conditions, using realistic terminology and scenarios. Avoid broad catch-all triggers and keyword stuffing. Test positive prompts, near misses, and legitimate composition.
- Aim for 30–100 lines and fewer than 1,500 tokens in most entrypoints; these are advisory targets, not gates. Do not enforce a minimum or remove necessary guidance to meet them. The official best-practice recommendation is under 500 lines and 5,000 tokens. Keep critical gotchas in the entrypoint when a reliable reference trigger is unlikely.

## Progressive disclosure

Keep `SKILL.md` sufficient for the common path. Put substantial specialized guidance in focused `references/` files and link each directly with a task- or symptom-based loading condition. Never require all references by default; avoid deep reference chains and copied external pages. Note version-sensitive behavior and link its authoritative source. Scripts and assets are optional; include them only when they make a reusable task materially easier.

## Workflow and resources

1. Identify the requested outcome and whether the user asked for review, planning, or implementation. Inspect only relevant skills, project conventions, and source material; expand scope when findings require it.
2. Confirm the capability is recurring and distinct. Review adjacent descriptions for overlap, define what belongs here, and preserve IDs and contracts when revising.
3. Draft activation conditions and an operational workflow with concrete defaults, risks, gotchas, authorization, and observable success criteria.
4. Add references only for specialized detail with a clear loading trigger. Add scripts only for reusable deterministic work; ensure predictable exit codes, useful errors, non-interactive use, documented dependencies and side effects, and dry-run support when appropriate. Test bundled scripts. Add assets only when a reusable template or data file has practical value.
5. Review for correctness, portability, clarity, duplication, and context cost. Inspect only task-relevant files; preserve unrelated changes; reuse tooling; do not install dependencies without justification. Stop when evidence is sufficient and report uncertainty rather than inventing results.
6. Verify format and links with repository checks. Add focused regression coverage for changed behavior. Evaluate activation and output behavior separately from structural validation.

## Evaluation

Define observable success, relevant edge cases, positive and negative activation, and responsibility boundaries. Compare agent runs with and without the skill (or against the previous version) on equivalent tasks. Judge correctness first, then context, latency, or cost. Offline schema and fixture checks do not demonstrate behavioral effectiveness; never claim effectiveness without execution evidence. Follow the [evaluation protocol](../evals/README.md).

## Repository resources

- [Repository architecture](architecture.md): catalog, validation, and portability conventions.
- [Context architecture](context-architecture.md): separation of reusable skills from project instructions and evidence.
- [Skill template](../templates/SKILL.md): adaptable starting point, not a required heading structure.
- [Contribution guide](../CONTRIBUTING.md): repository maintenance and quality gates.

## Official sources

- [Specification](https://agentskills.io/specification)
- [Best practices](https://agentskills.io/skill-creation/best-practices)
- [Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Using scripts](https://agentskills.io/skill-creation/using-scripts)
- [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills)
