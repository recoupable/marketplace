# Agent instructions for Recoupable plugins

This repo is a curated marketplace for Recoupable agent plugins. It is not the
home for every skill. Broad, standalone skills live in `recoupable/skills`;
product-like bundles live here as plugins.

## Structure

- `.claude-plugin/marketplace.json`: Claude Code marketplace.
- `.agents/plugins/marketplace.json`: Codex marketplace.
- `{plugin-name}/`: nested submodule for one installable plugin.

Each plugin is its own repository and owns its own `AGENTS.md`, manifests,
skills, commands, agents, scripts, templates, and tests.

## When to create a plugin

Create a plugin when a category becomes an installable bundle: usually three or
more related skills, or any need for commands, agents, scripts, templates, MCP,
fixtures, or marketplace install UX.

Keep a workflow as a skill when it is one broad reusable task and does not need
a full bundle.

## How to add or update a plugin

1. Change the plugin repository first.
2. Verify the plugin in that repository.
3. Update this registry's submodule pointer and marketplace manifests.
4. Verify both marketplace JSON files.
5. Open a PR in `recoupable/plugins`.
6. Update the mono `plugins` submodule pointer only after the registry PR lands.

Do not move existing public skills from `recoupable/skills` into a plugin
without an explicit migration plan. Agents and sandboxes may depend on current
skill names and install paths.

## Naming

Keep these values aligned:

- submodule folder name
- plugin manifest `name`
- marketplace entry `name`
- GitHub repository name
- README install command

If one changes, update all of them in the same PR.
