# Agent and installer compatibility

The repository's deterministic tests verify installer behavior against the two supported destination layouts. The agent discovery and invocation details below come from client documentation. Live routing and invocation depend on the client version, settings, and session. Use the live evaluation protocol when verifying a specific client. [Evaluation protocol](../evals/README.md#run-live-evaluations)

| Agent | Installer support | Documented locations | Verification boundary |
| --- | --- | --- | --- |
| Codex | Yes; project and user scope. | `.agents/skills/`, `~/.agents/skills/` | Installer destination behavior is tested. The client documents discovery and `$skill-name`; live routing is version/configuration dependent. [Codex skills](https://developers.openai.com/codex/skills) |
| Claude Code | Yes; project and user scope. | `.claude/skills/`, `~/.claude/skills/` | Installer destination behavior is tested. The client documents discovery and `/skill-name`; live routing is version/configuration dependent. [Claude Code skills](https://code.claude.com/docs/en/skills) |
| GitHub Copilot | No. The built-in CLI accepts only Codex and Claude Code. | Surface-specific project locations include `.github/skills/`, `.claude/skills/`, or `.agents/skills/`; personal locations include `~/.copilot/skills/` or `~/.agents/skills/`. | Copilot documents Agent Skills support and locations. Use its current surface instructions for manual installation; this repository does not test Copilot discovery or invocation. [Copilot Agent Skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) |

Agent Skills is an open format, not a guarantee that every client implements the same discovery, resource-loading, or invocation behavior. Specification-compatible clients may use packages through their own documented paths, but they are not managed by this installer unless listed above.

The offline CLI is `.scripts/skills.py`, with Bash wrappers for installation, removal, and validation. Historical `scripts/` paths forward to the same implementation. `--agent all` selects Codex and Claude Code. Vercel's Skills CLI tracks installations separately. Use the installation method that owns the installed instance when updating or removing it. [Consumer installation and updates](../README.md#installation-modes)

## Migrating to v2

1. With the installed revision still at the original toolkit path, identify the IDs you are replacing. Use the migration map and the approved catalog to choose their successors. [V2 migration map](../SCOPE.md#workflow-boundaries-and-v2-migration)
2. Preview uninstall for those IDs with the original installer, agent, and scope. Re-run without `--dry-run` after checking the selected paths. For example, for a Codex project with `java-quality` and `code-review` installed, run the command below from that project.
3. Update the toolkit revision, install the selected v2 IDs, and update explicit skill invocations. Reinstall copied skills with retained IDs when you want to refresh their contents.

```bash
python3 /path/to/current-toolkit/.scripts/skills.py uninstall \
  --agent codex --target "$PWD" --skill java-quality,code-review --dry-run
```

If the checkout was already upgraded and a retired symlink is now dangling, use the earlier revision at the original toolkit path so the installer can verify its target. Preserve local edits and inspect ownership conflicts before retrying removal.

## Recovering from a partial operation

Install and uninstall check known ownership conflicts for the full selection before they begin applying changes. A later failure can leave earlier destinations installed or removed. Review the reported paths, fix the underlying error, and preview the same selection and mode with `--dry-run` before retrying. An install skips verified destinations already installed in the requested mode, and an uninstall skips absent destinations.

A process interruption can leave a copy without a complete ownership marker. A copied skill with local changes or unverifiable ownership requires manual inspection. Preserve any local changes before deciding how to recover that path. [Updating and uninstalling](../README.md#installation-modes)
