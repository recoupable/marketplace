# Recoup Plugins

Registry repo for Recoup agent plugins.

This repo is a curated plugin marketplace for Claude Code, Claude Cowork, and Codex. Each plugin lives in its own GitHub repo (referenced from the marketplace files in this registry) so it can be developed, versioned, and distributed independently.

## Plugins

| Plugin | Purpose |
| ------ | ------- |
| `recoup-catalog-deals` | Music catalog deals: data-room ingestion, royalty normalization, rights checks, and valuation analysis for buy-side, seller-prep, financing, and post-close. |
| `recoup-platform-plugin` | Recoup platform helpers: cross-cutting skills, commands, and workflows for AI agents working with Recoup's chat, API, and platform surface. |
| `recoup-content-plugin` | Recoup content workflows: skills and commands for AI agents to draft, edit, and publish content for artists across Recoup's surfaces. |
| `recoup-research-plugin` | Recoup research workflows: skills and commands for AI agents to run artist research, audience analysis, trend scans, and market intelligence. |

## Install with Claude Code

Add the marketplace, then install the plugin you need:

```bash
/plugin marketplace add recoupable/marketplace
/plugin install recoup-catalog-deals@recoup-marketplace
```

Claude Code reads the marketplace from `.claude-plugin/marketplace.json`. Each plugin entry uses a `github` source object so the plugin is fetched from its own repo, independent of any submodule the registry uses internally.

## Install with Claude Cowork

In Claude Desktop's **Cowork** tab:

1. **Customize → Plugins → + → Create plugin → Add marketplace**
2. Paste `https://github.com/recoupable/marketplace`
3. Click **Sync**

The plugin appears in your Personal plugins list and its slash commands are available immediately. Cowork plugins require a paid Claude plan (Pro, Max, Team, or Enterprise).

## Install with Codex

Add the registry as a marketplace via the CLI:

```bash
codex plugin marketplace add recoupable/marketplace
```

Then open the plugin directory inside Codex and install:

```bash
codex /plugins
```

Codex reads the marketplace from `.agents/plugins/marketplace.json`. Each plugin entry uses a `url` source so Codex pulls the plugin's repo directly.

## Plugin sources: no relative paths

The lesson learned the hard way: **don't reference plugin folders by relative path** if the folder lives in a Git submodule. Marketplace consumers (Cowork, Claude Code's URL-based install, Codex `marketplace add`) clone the registry repo without recursing submodules — relative paths resolve to empty folders and the install fails silently or with a "marketplace sync failed" error.

Use the explicit per-runtime source object instead:

**`.claude-plugin/marketplace.json`:**

```json
{
  "source": {
    "source": "github",
    "repo": "recoupable/<plugin-repo-name>"
  }
}
```

**`.agents/plugins/marketplace.json` (Codex):**

```json
{
  "source": {
    "source": "url",
    "url": "https://github.com/recoupable/<plugin-repo-name>.git",
    "ref": "main"
  }
}
```

Both formats let consumers pull the plugin's actual repo independently of any submodule resolution.

## Release checklist

Before adding or updating a plugin in this registry, verify these requirements:

- Add or update `.claude-plugin/plugin.json` in the plugin's own repo.
- Add or update `.codex-plugin/plugin.json` in the plugin's own repo (when the plugin supports Codex).
- Add the plugin entry to **both** `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json` in this registry, using the per-runtime source schemas above (never a relative path).
- Verify the install end-to-end on at least one runtime (Cowork is the fastest to test — paste the marketplace URL into Add marketplace).
- Use semantic versions and bump the version for release updates.
- Include a `README.md`, `LICENSE`, and support contact in the plugin repo.
- Keep secrets out of plugin content and reference environment variables instead.
- Document required external tools and make scripts work across macOS and Linux when possible.
- Run plugin-specific tests, fixture checks, and JSON validation before release.
