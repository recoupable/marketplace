# Recoup Plugins

Official plugin marketplace for Recoup's AI agent platform. Each plugin gives AI agents (Claude Code, Codex, Cursor) direct access to Recoup's music business infrastructure.

## Plugins

Install **recoup-platform-plugin** first — it validates your setup and discovers capabilities. Then add domain plugins based on your workflow.

| Plugin | Skills | What it does |
| ------ | ------ | ------------ |
| `recoup-platform-plugin` | 2 | **Start here.** Onboarding, health checks, and cross-cutting helpers for the Recoup API and agent ecosystem. |
| `recoup-research-plugin` | 7 | Artist analytics, audience insights, playlist intelligence, competitive analysis, trend detection, and outreach. |
| `recoup-content-plugin` | 3 | End-to-end content workflows — short-form music videos, captions, images, and publishing for artists. |
| `music-catalog-diligence` | 9 | Catalog diligence — data-room ingestion, royalty normalization, rights checks, valuation, and deal packaging. |

**Total: 4 plugins, 21 skills.**

## Install

### Claude Code

Add the marketplace, then install what you need:

```bash
/plugin marketplace add recoupable/plugins

# Install the platform plugin first
/plugin install recoup-platform-plugin@recoupable-plugins

# Then add domain plugins
/plugin install recoup-research-plugin@recoupable-plugins
/plugin install recoup-content-plugin@recoupable-plugins
/plugin install music-catalog-diligence@recoupable-plugins
```

### Codex

```bash
codex plugin install https://github.com/recoupable/recoup-platform-plugin
codex plugin install https://github.com/recoupable/recoup-research-plugin
codex plugin install https://github.com/recoupable/recoup-content-plugin
codex plugin install https://github.com/recoupable/music-catalog-diligence
```

### Cursor

1. Cursor → Settings → Plugins → **Add custom plugin**.
2. Paste the GitHub URL for each plugin.
3. Restart Cursor so manifests load.

## Quick start

After installing `recoup-platform-plugin`, set your API key and run the onboarding:

```bash
export RECOUP_API_KEY="recoup_sk_..."   # https://developers.recoupable.com/agents
```

Then in a new chat:

> **Get me started with Recoup**

The agent validates your key, discovers available capabilities, runs a demo query, and recommends which domain plugins to install next.

## Plugin details

### recoup-platform-plugin (v0.2.0)

The entry point. Two skills:
- `recoup-getting-started` — first-run onboarding, API validation, capability discovery, demo query
- `recoup-health-check` — diagnostics for API connectivity, auth, credit balance, plugin status

### recoup-research-plugin (v0.1.0)

Seven research skills:
- `recoup-artist-research` — deep-dive artist analytics
- `recoup-audience-analysis` — demographic and psychographic audience insights
- `recoup-competitive-analysis` — benchmark against competitors
- `recoup-playlist-intelligence` — scout and analyze playlists for pitching
- `recoup-trend-detection` — emerging trends in music data
- `recoup-people-outreach` — industry contact outreach generation
- `recoup-web-intelligence` — web-based research and intelligence gathering

### recoup-content-plugin (v0.3.0)

Three content skills:
- `recoup-content-create` — front-door command: artist name → finished 9:16 social-ready clip
- `short-video` — end-to-end playbook for producing short-form music videos
- `content-creation` — atomic primitives for images, videos (6 modes), captions, transcription, editing

### music-catalog-diligence (v0.1.0)

Nine diligence skills:
- `diligence-kickoff` — start a new catalog diligence project
- `catalog-ingest` — ingest and normalize data room files
- `catalog-analysis` — analyze catalog composition and performance
- `royalty-audit` — audit royalty statements and flag anomalies
- `rights-diligence` — chain-of-title and rights verification
- `financing-underwrite` — build underwriting models for catalog financing
- `ic-memo-package` — generate investment committee memo packages
- `seller-prep` — prepare seller-side diligence materials
- `post-close-admin` — post-acquisition administrative workflows

## Structure

```text
plugins/
├── .claude-plugin/marketplace.json     # Claude Code marketplace registry
├── .agents/plugins/marketplace.json    # Codex marketplace registry
├── recoup-platform-plugin/             # Platform onboarding + health
├── recoup-research-plugin/             # Research & analytics
├── recoup-content-plugin/              # Content creation & publishing
├── music-catalog-diligence/            # Catalog diligence (submodule)
├── AGENTS.md                           # Agent guidance
├── CLAUDE.md                           # Claude Code guidance
└── README.md
```

## Support

- Docs: [developers.recoupable.com](https://developers.recoupable.com)
- Email: support@recoupable.com
- Website: [recoupable.com](https://recoupable.com)

## License

[Apache-2.0](./LICENSE)
