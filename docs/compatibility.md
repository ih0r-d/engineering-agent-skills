# Agent and installer compatibility

The repository's deterministic tests verify installer behavior against the two supported destination layouts. The agent discovery and invocation details below come from client documentation. Live routing and invocation depend on the client version, settings, and session. Use the live evaluation protocol when verifying a specific client. [Evaluation protocol](../evals/README.md#run-live-evaluations)

| Agent | Installer support | Documented locations | Verification boundary |
| --- | --- | --- | --- |
| Codex | Yes; project and user scope. | `.agents/skills/`, `~/.agents/skills/` | Installer destination behavior is tested. The client documents discovery and `$skill-name`; live routing is version/configuration dependent. [Codex skills](https://developers.openai.com/codex/skills) |
| Claude Code | Yes; project and user scope. | `.claude/skills/`, `~/.claude/skills/` | Installer destination behavior is tested. The client documents discovery and `/skill-name`; live routing is version/configuration dependent. [Claude Code skills](https://code.claude.com/docs/en/skills) |
| GitHub Copilot | No. The built-in CLI accepts only Codex and Claude Code. | Surface-specific project locations include `.github/skills/`, `.claude/skills/`, or `.agents/skills/`; personal locations include `~/.copilot/skills/` or `~/.agents/skills/`. | Copilot documents Agent Skills support and locations. Use its current surface instructions for manual installation; this repository does not test Copilot discovery or invocation. [Copilot Agent Skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) |

Agent Skills is an open format, not a guarantee that every client implements the same discovery, resource-loading, or invocation behavior. Specification-compatible clients may use packages through their own documented paths, but they are not managed by this installer unless listed above.

The offline CLI is `.scripts/skills.py`, with Bash wrappers for installation, removal, and validation. Historical `scripts/` paths forward to the same implementation. `--agent all` selects Codex and Claude Code. Vercel's Skills CLI tracks installations separately. Use the installation method that owns the installed instance when updating or removing it. [Consumer installation and updates](../README.md#installation-modes)

## Recovering from a partial operation

Install and uninstall check known ownership conflicts for the full selection before they begin applying changes. A later failure can leave earlier destinations installed or removed. Review the reported paths, fix the underlying error, and preview the same selection and mode with `--dry-run` before retrying. An install skips verified destinations already installed in the requested mode, and an uninstall skips absent destinations.

A process interruption can leave a copy without a complete ownership marker. A copied skill with local changes or unverifiable ownership requires manual inspection. Preserve any local changes before deciding how to recover that path. [Updating and uninstalling](../README.md#installation-modes)
