# Agent and installer compatibility

The repository's deterministic tests verify installer behavior against the two supported destination layouts. The agent discovery and invocation details below come from client documentation. Live routing and invocation depend on the client version, settings, and session. Use the live evaluation protocol when verifying a specific client. [Evaluation protocol](../evals/README.md#run-live-evaluations)

| Agent | Project scope | User scope | Client documentation |
| --- | --- | --- | --- |
| Codex | `.agents/skills/` | `~/.agents/skills/` | Documents these paths, symlinked skill folders, and explicit `$skill-name` invocation. [Codex skills](https://learn.chatgpt.com/docs/build-skills) |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | Documents these paths, symlinked skill folders, and explicit `/skill-name` invocation. [Claude Code skills](https://code.claude.com/docs/en/skills) |
| GitHub Copilot | Depends on the client surface | Depends on the client surface | Documents Agent Skills across CLI, IDE, and hosted surfaces. The installer targets Codex and Claude Code. Live Copilot discovery is unverified. [Copilot Agent Skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) |

The offline CLI is `.scripts/skills.py`, with Bash wrappers for installation, removal, and validation. Historical `scripts/` paths forward to the same implementation. `--agent all` selects Codex and Claude Code. Vercel's Skills CLI tracks installations separately. Use the installation method that owns the installed instance when updating or removing it. [Consumer installation and updates](../README.md#installation)

## Recovering from a partial operation

Install and uninstall check known ownership conflicts for the full selection before they begin applying changes. A later failure can leave earlier destinations installed or removed. Review the reported paths, fix the underlying error, and preview the same selection and mode with `--dry-run` before retrying. An install skips verified destinations already installed in the requested mode, and an uninstall skips absent destinations.

A process interruption can leave a copy without a complete ownership marker. A copied skill with local changes or unverifiable ownership requires manual inspection. Preserve any local changes before deciding how to recover that path. [Updating and uninstalling](../README.md#updating-and-uninstalling)
