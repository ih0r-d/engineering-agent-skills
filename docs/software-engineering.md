# Software Engineering skill boundaries

Choose the primary skill by the requested outcome. A language-specific skill can contribute evidence about the language without changing the outcome or authorizing edits. The primary skill determines the scope and final deliverable.

| Skill | Primary responsibility and positive example | Near miss, exclusion, or composition |
| --- | --- | --- |
| [`code-review`](../skills/code-review/SKILL.md) | Assess a PR or scoped change. Review a changed selection function for regressions and missing coverage. | A request to repair a Python defect belongs to the Python fix workflow. In a PR review, use Python guidance to assess runtime behavior while keeping the review read-only. Repository-wide architecture, incident investigation, dedicated security audits, and formatting have their own scopes. |
| [`java-quality`](../skills/java-quality/SKILL.md) | Resolve Java contracts, runtime and generated-code behavior, and analyzer findings. Investigate an ignored `String` result. | A general Java PR review starts with code review. Java guidance supplies evidence about source, binary, or behavioral compatibility. |
| [`python-quality`](../skills/python-quality/SKILL.md) | Resolve Python runtime, typing, import, packaging, and analyzer issues. Diagnose shared mutable defaults. | A general PR assessment starts with code review. Python guidance helps verify errors, object ownership, and caller behavior. |
| [`shell-quality`](../skills/shell-quality/SKILL.md) | Resolve Bash and POSIX `sh` argument, status, cleanup, and portability issues. Diagnose word splitting in a script. | A general change review starts with code review. Shell guidance checks interpreter behavior where it affects a finding. |

A read-only request stays read-only when a specialist includes a fix mode. Confirm the caller, observable effect, and available evidence before turning a language diagnostic into a review finding. [Evaluation protocol](../evals/README.md), [Google Engineering Practices for reviewers](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
