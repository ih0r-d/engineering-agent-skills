# Commit Conventions

Prefer the consuming repository's documented policy. When absent, use Conventional Commits with a concise imperative summary.

| Type | Intent |
| --- | --- |
| feat | New functionality. |
| fix | Defect correction. |
| refactor | Structural change without intended behavior change. |
| perf | Performance improvement. |
| test | Test changes. |
| docs | Documentation changes. |
| chore | Repository maintenance. |
| build | Build system or dependencies. |
| ci | Continuous integration configuration. |
| style | Formatting without behavior changes. |
| revert | Revert a previous change. |

## Formats

```text
feat: add order validation
feat(api): add order validation
fix: ENG-123: preserve retry state
fix(api): ENG-123: preserve retry state
```

The task-ID prefix inside the description is an optional local convention, not a requirement of the Conventional Commits specification. Use only a supplied or verified task ID. Prefer `fix` over `bugfix` when following Conventional Commits.

Use `!` or a `BREAKING CHANGE:` footer for genuine breaking changes according to repository policy. Do not infer a breaking change from a commit type alone.

## Safe operations

- Inspect `git status --short`, `git diff`, and `git diff --cached` before committing.
- Stage explicit paths or reviewed hunks, not unrelated changes.
- Resolve conflicts against intended behavior; do not blindly choose one side.
- Prefer a revert for shared history when appropriate; history rewriting requires separate authorization.

## Official guidance

- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [Git documentation](https://git-scm.com/docs)
