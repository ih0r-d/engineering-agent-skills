# Behavioral baseline with Codex

Configuration A starts Codex with no toolkit skills. Configuration B installs a copy of the complete catalog using the offline installer. Both arms use the same prompt, fixture, project instructions, configured model, reasoning effort, authentication method, permissions, and wall timeout for a scenario. Every invocation gets a new disposable project and a separate home. Alternate A/B and B/A order across consecutive pairs to reduce order effects. The method can later accommodate Caveman and combined arms as separate experiments.

The harness uses native `codex exec --json` and standard-library Python. The event parser and isolation options target Codex CLI **0.172.0**. Recheck the schema and isolation before supporting another version. [Non-interactive Codex](https://learn.chatgpt.com/docs/non-interactive-mode) · [Pinned event definitions](https://github.com/openai/codex/blob/rust-v0.172.0/codex-rs/exec/src/exec_events.rs)

## Authentication and usage

Select the mode explicitly for a live batch. Both A and B use the same mode and login.

| Mode | Setup and usage |
| --- | --- |
| `--auth chatgpt` | Run in a private interactive terminal. Enable device code login in ChatGPT security settings, or have the workspace administrator enable it where required. Follow Codex’s native `login --device-auth` instructions once per batch and select the intended account or workspace. The evaluations then run non-interactively. Usage draws from the account’s Codex allowance and any applicable credits or workspace charges. An API key is unnecessary. |
| `--auth api-key` | Supply `CODEX_API_KEY` through your environment or secret manager. The harness passes it only to the Codex client. Usage is billed through the corresponding OpenAI Platform project at API rates. |

ChatGPT mode requires device sign-in and Codex file-based OAuth storage. If these are unavailable or disallowed, the harness stops. It never switches to API-key mode after an authentication or quota failure. Use this workflow locally on a trusted machine and keep sign-in prompts out of recordings and shared logs. [Codex authentication](https://learn.chatgpt.com/docs/auth) · [Codex plan usage and billing](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)

## Pilot

| Scenario | Observable result |
| --- | --- |
| `java-feature` | Add a Java 11 overload to a minimal pilot fixture. A hidden probe verifies the requested output and existing behavior. The fixture follows the repository’s existing feature-implementation and Java cases. |
| `code-review-near-miss-python-fix` | Fix Python shared defaults. Check independent omitted arguments and existing explicit list mutation. |
| `code-review-selection-regression` | Report the sparse-match regression with evidence and keep the fixture unchanged. |
| `shell-quality-trap-status` | Diagnose an exit status lost through cleanup and propose a safe test. The pilot supplies a minimal POSIX sh reproducer and keeps it read-only. |
| `make-recipe-directory` | Explain the GNU Make recipe working-directory failure and leave files unchanged. |
| `review-code-unsupported-language` | Review an explicitly Go 1.22 task while the available workspace contains a Java example. Check the generic review result and any evidence of irrelevant reference access. |

Five prompts are reused verbatim from the evaluation catalog. The additional pilot fixture and fixture selections leave the original evaluation cases intact. Prompts leave skill selection to the agent.

## Plan and run

Work from a committed revision so the recorded Git hash describes the inputs. Use the same CLI, tool versions, model, effort, and timeout for repeats. Java requires a JDK that can compile for Java 11, the Python case uses Python 3, and the Make case requires GNU Make. The runner uses common system and Homebrew binary locations. A valid `JAVA_HOME` selects a specific installed JDK for the Java case.

```sh
task eval:plan
task eval:run -- --scenario java-feature --max-runs 2
```

The first command plans 12 invocations. The second plans a two-invocation pair. Both start zero Codex processes and do not sign in. Select a subset by repeating `--scenario`, choose an arm with `--configuration A|B|AB`, and set `--repetitions`, `--timeout`, and `--output` as needed. Live execution requires explicit `--auth`, `--max-runs`, `--model`, and `--reasoning-effort`. The examples use GPT-6.2 Sol at medium effort. Use a model and effort available to your account. [Codex models](https://learn.chatgpt.com/docs/models)

First paired smoke test using ChatGPT sign-in:

```sh
task eval:run -- --live --auth chatgpt --scenario java-feature --configuration AB --model gpt-6.2-sol --reasoning-effort medium --repetitions 1 --max-runs 2 --timeout 180
```

Complete pilot, one pair per scenario:

```sh
task eval:run -- --live --auth chatgpt --configuration AB --model gpt-6.2-sol --reasoning-effort medium --repetitions 1 --max-runs 12 --timeout 180
```

For API-key execution, use `--auth api-key` and provide the environment variable. The budget counts model invocations of the CLI. Codex can issue multiple internal requests in a single invocation. The runner never retries an invocation and stops the batch on execution failure, including authentication and quota failures, or timeout. The report shows unstarted slots. These limits do not predict billing.

## Isolation

Only the selected fixture and fixed `AGENTS.md` are copied into the disposable project. The runner verifies the common input digest, checks for inherited project and system discovery paths, and verifies the copied catalog in B. A fresh home excludes the caller's user skills, sessions, and configuration. The run disables bundled skills, hooks, plugins, memories, web search, dependency MCP installation, and delegation features. Codex runs without user config or exec rules and with no approvals. The native profile grants edit tasks workspace writes and a disposable scratch directory. Review and diagnosis workspaces stay read-only. Commands have no network access. The harness uses a native sandbox probe before each invocation and stops if it can read the private checkout or result sentinel or if the tested workspace permissions differ. The prompt and grader inputs remain separate.

Native probes verify local prerequisites without an agent turn. They do not prove every property of an effective runtime session or an administrator-managed environment. Use a dedicated unmanaged environment for controlled comparisons. If CLI settings, managed policies, or tool evidence show contamination, treat the comparison as inconclusive. Run graders for edited source in a separate native sandbox after the agent exits. [Permission profiles](https://learn.chatgpt.com/docs/permissions) · [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills)

ChatGPT device sign-in creates its credential cache inside a private temporary directory. Only that file moves between fresh Codex homes, one invocation at a time, to carry forward native token refreshes. Project workspaces, session history, login-home configuration, and installed skills stay separate. Sandbox policy blocks access to the credential directories, and a probe tests a synthetic file in each run home. Normal cleanup removes the temporary homes, including the cache. If the runner is forcibly killed, remove its abandoned private `/tmp/eas-eval-*` directory. The runner leaves the existing user Codex home untouched. [Codex credential storage](https://learn.chatgpt.com/docs/auth#credential-storage)

## Results and grading

A batch under `.eval-results/` contains a manifest, per-run JSON records, the JSONL stream, stderr, and final response. Available file deltas include paths, digests, modes, and up to 1 MiB of small changed files. Execution failures retain partial traces. The batch is private, and repository-local output must be ignored and free of tracked files. Model streams are redacted for known credentials before being saved, including tokens refreshed during a run. Native sign-in prompts stay in the terminal. The manifest records the authentication mode. Review any captured output before sharing it.

```sh
task eval:report
task eval:report -- --output .eval-results/pilot-REPLACE-WITH-BATCH-ID
```

The first command selects the newest batch by recorded start time among batches in `.eval-results/` whose planned model invocations all completed. Failed grades and pending manual grades still appear. Use `--output` for a batch that stopped early, timed out, or was stored elsewhere.

- **Correctness.** The independent probes use executable assertions and the Java 11 target. Every scenario checks unexpected workspace changes and observed forbidden tool use. Review and diagnosis content requires human assessment. Read-only workspace snapshots detect net changes, and successful structured patch events can show changes later undone. Shell writes that are undone and omitted from events remain unobserved.
- **Task completion.** Use the case criteria and actual evidence to judge the final response, mode, and technology. After reviewing, optionally add `manual.json` next to a result with `{"status":"passed","notes":"<evidence>"}`, or use `failed` or `unavailable`. Manual grading can resolve a pending qualitative result and cannot replace a deterministic failure or execution error.
- **Activation and reference selection.** The pinned exec stream has no direct semantic activation or mode event. Successful recognizable shell reads with absolute paths provide access evidence. Relative paths are possible matches since the command event lacks a working directory. The harness retains the commands and distinguishes expected paths from other observed reads. Other commands, agent-internal loading, interpretation, and unobserved access require separate evidence. Installed package counts are exposure checks.
- **Efficiency.** The runner records input, cached input, output, and separately reported reasoning output. Cached input and reasoning output are subsets. Total is input plus output when both are available. The CLI may emit zero defaults when usage is missing. Tool count uses unique recognized tool item IDs. Duration is client wall time, including initialization and model/tool execution, with fixture setup and grading outside it.
- **Limits.** Reports show case-level statuses, observed medians, and paired differences with sample counts alongside failures and unstarted slots. Execution errors, timeouts, unavailable evidence, and pending manual grades remain distinct. One paired run is a smoke test. Compare repeated pairs under equivalent conditions before drawing behavioral conclusions.

Normal CI validates only offline fixtures, harness behavior, and the skill specification. The predicted pilot budget and fixture assertions do not establish an observed baseline.

## Method sources

- [OpenAI Codex documentation](https://developers.openai.com/codex/)
- [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills)
- [Agent Skills specification](https://agentskills.io/specification)
- [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
