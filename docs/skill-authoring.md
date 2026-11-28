# Skill Authoring Standard

This is the canonical repository guide for creating and changing portable Agent Skills. The [Agent Skills specification](https://agentskills.io/specification) defines format requirements; this guide adds repository recommendations. Consumer project policy remains with the consumer.

## Format requirements

Every skill directory contains `SKILL.md` with YAML frontmatter and Markdown instructions. Required `name` must match the directory, be 1–64 lowercase letters, digits, or hyphens, have no leading/trailing or consecutive hyphens. Required `description` must be non-empty and no more than 1024 characters, and describe both capability and use conditions. Optional standard fields are `license`, `compatibility` (up to 500 characters), `metadata` (string keys and values), and experimental `allowed-tools`. Use no non-standard fields as requirements. The official body format does not require particular headings.

## Repository recommendations

- A new workflow may justify a skill when it has a distinct engineering objective, activation boundary, and observable outcome. Define these before adding a package. Keep every package usable on its own.
- A new language, framework, build tool, or platform normally extends the owning workflow with a reference. Organize expertise by the responsibility that uses it, such as implementation patterns, review criteria, runtime diagnostics, or test isolation. Avoid copying full technology guides between workflows. See the [toolkit scope](../SCOPE.md).
- Ground guidance in real tasks, project artifacts, documented behavior, and observed failure modes. Prefer actionable procedures, a clear default, and justified alternatives. Match instruction specificity to operational risk and preserve authorization boundaries.
- Describe user intent and activation conditions, using realistic terminology and scenarios. Avoid broad catch-all triggers and keyword stuffing. Test positive prompts, near misses, and legitimate composition.
- Aim for 30–100 lines and fewer than 1,500 tokens in most entrypoints; these are advisory targets, not gates. Do not enforce a minimum or remove necessary guidance to meet them. The official best-practice recommendation is under 500 lines and 5,000 tokens. Keep critical gotchas in the entrypoint when a reliable reference trigger is unlikely.

## Progressive disclosure

Keep `SKILL.md` sufficient for the common workflow. Identify explicit user technology requirements first. Inspect the relevant source, manifests, dependencies and configuration to establish the language, framework, tool, and version where possible. If evidence is insufficient or no matching reference exists, follow the generic workflow and project conventions. Claim specialized coverage only for actual bundled guidance.

Put specialized guidance in small `references/` files. Group substantial technical content under technology-specific directories that reflect existing material. Link each file directly from `SKILL.md` using a portable relative path and state the task, evidence, or symptom that warrants reading it. Select only the files the current task needs through native client capabilities. Keep reference targets within the owning package and validate nested links. Note version-sensitive behavior and cite the authoritative source.

For workflows with multiple modes, state which mode allows edits and what requires separate authorization. Where native subagents can help, make their use optional. Specify bounded work, inherited authorization, ownership of any edits, primary-agent verification, and a sequential fallback.

### Scripts, assets, and hooks

- A bundled script is justified for a repeatable, deterministic operation that adds value beyond an obvious existing command. Prefer Python standard library for structured work, keep it independent of the source checkout, accept explicit inputs, and define useful output, exit codes, dependencies, and side effects. Prefer read-only behavior; never silently overwrite or perform destructive actions. Avoid hidden network access and shell interpolation of user input. Add automated tests for executable scripts.
- An asset is justified when a reusable template or data file improves a recurring deliverable. Keep it focused, adapt it to the consuming project's conventions, and identify in `SKILL.md` when to use it. Do not add decorative or duplicate templates.
- Link each script or asset by a portable relative path and load or run it only for its stated task. Keep essential safety constraints in `SKILL.md`; do not force agents to inspect every resource.
- Skills describe procedures, references hold technical knowledge, scripts perform deterministic operations, and assets provide reusable deliverables. Hooks are separate event-driven callers. Scripts may be designed for future hook invocation, but a skill package must not install hooks, edit client configuration, or change global Git settings automatically.
- Repository maintenance tools belong in `.scripts/`, not inside portable skill packages. Bundled scripts and assets must work when the owning skill is installed alone.

## Workflow and resources

1. Identify the requested outcome and whether the user asked for review, planning, or implementation. Inspect only relevant skills, project conventions, and source material; expand scope when findings require it.
2. Confirm the capability is recurring and distinct. Review adjacent descriptions for overlap, define what belongs here, and preserve IDs and contracts when revising. Extend an existing workflow's references when the objective and outcome already fit.
3. Draft activation conditions and an operational workflow with concrete defaults, risks, gotchas, authorization, and observable success criteria.
4. Add references only for specialized detail with a clear loading trigger. Add scripts only for reusable deterministic work; ensure predictable exit codes, useful errors, non-interactive use, documented dependencies and side effects, and dry-run support when appropriate. Test bundled scripts. Add assets only when a reusable template or data file has practical value.
5. Review for correctness, portability, clarity, duplication, and context cost. Inspect only task-relevant files; preserve unrelated changes; reuse tooling; do not install dependencies without justification. Stop when evidence is sufficient and report uncertainty rather than inventing results.
6. Verify format and links with repository checks. Add focused regression coverage for changed behavior. Evaluate activation and output behavior separately from structural validation.

## Evaluation

Define observable success, relevant edge cases, positive and negative activation, and responsibility boundaries. For specialized references, include cases with relevant technology evidence and cases with misleading, absent, or unsupported technology signals. Compare agent runs with and without the skill (or against the previous version) on equivalent tasks. Judge correctness first, then context, latency, or cost. Offline schema and fixture checks do not demonstrate behavioral effectiveness; never claim effectiveness without execution evidence. Follow the [evaluation protocol](../evals/README.md).

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
