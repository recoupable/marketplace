# Recoupable Plugins

Registry repo for Recoupable agent plugins.

This repo is a curated plugin marketplace for Claude Code, Codex, and Cursor.
Each plugin lives as its own Git submodule so it can be developed, versioned,
and distributed independently.

## Plugins

| Plugin | Purpose |
| ------ | ------- |
| `music-catalog-diligence` | Review royalties, rights, valuation, and deal materials for music catalog transactions. |

## Install with Claude Code

Add the marketplace, then install the plugin you need:

```bash
/plugin marketplace add recoupable/plugins
/plugin install music-catalog-diligence@recoupable-plugins
```

Claude Code reads the marketplace from
`.claude-plugin/marketplace.json`. Plugin entries use relative `source` paths
that resolve from this registry repo.

## Install with Codex

Codex reads the repo-scoped marketplace from
`.agents/plugins/marketplace.json`. Each listed plugin points to a folder that
contains a `.codex-plugin/plugin.json` manifest.

The current Codex surface for `music-catalog-diligence` packages the bundled
`skills/` directory. Claude-specific `commands/` and `agents/` remain available
through Claude Code, but they are not advertised as Codex features until Codex
supports that packaging path.

## Install with Cursor

Cursor reads the marketplace from `.cursor-plugin/marketplace.json`. Each listed
plugin points to a folder that contains a `.cursor-plugin/plugin.json` manifest.

## Release checklist

Before adding or updating a plugin in this registry, verify these requirements:

- Add or update `.claude-plugin/plugin.json`.
- Add or update `.codex-plugin/plugin.json` when the plugin supports Codex.
- Add or update `.cursor-plugin/plugin.json` when the plugin supports Cursor.
- Keep all manifest paths relative to the plugin root.
- Use semantic versions and bump the version for release updates.
- Include a `README.md`, `LICENSE`, and support contact.
- Keep secrets out of plugin content and reference environment variables
  instead.
- Document required external tools and make scripts work across macOS and Linux
  when possible.
- Run plugin-specific tests, fixture checks, and JSON validation before release.
