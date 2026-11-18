# Package ownership and maintenance

Recoup keeps two package families: the consolidated `recoup-plugin` authored in
[recoupable/skills](https://github.com/recoupable/skills), and the four standalone
plugins registered here. Both remain maintained in their owning repositories.
The standalone plugins are not generated copies of Skills and are not designated
migration-only or deprecated. Sharing a domain or similar wording does not make
two implementations interchangeable.

This policy identifies source responsibility and release procedure. It adds no
support deadline, response-time promise, automatic update guarantee or new host
compatibility claim. Report a defect in the owning repository with the package
name, source/version, host and reproduction; follow that repository's README for
its existing support contact.

## Choose the owning source

| Capability or change | Owning repository and authoring path | Maintenance and upgrade path |
| --- | --- | --- |
| Broad, reusable Recoup skills; consolidated customer/staff packaging | [recoupable/skills](https://github.com/recoupable/skills): `skills/<skill-name>/SKILL.md` and skill-local support files; root manifests and `scripts/` for packaging | Maintained consolidated distribution. Follow its `AGENTS.md` and `contributing.md`; release from that repository. Generated ZIPs and `claude-directory` are outputs, not places to author fixes. |
| Standalone catalog deal workflow, validators and deal templates | [recoupable/recoup-catalogs-plugin](https://github.com/recoupable/recoup-catalogs-plugin): `skills/`, `scripts/`, `templates/`, `references/`, `agents/` and retained `commands/`/`hooks/` | Maintained standalone distribution. Fix and release in this child, then update its registry gitlink, version and both immutable source pins. Follow its README development checks. |
| Standalone account setup, API access and workspace workflows | [recoupable/recoup-platform-plugin](https://github.com/recoupable/recoup-platform-plugin): `skills/` and each skill's supporting references | Maintained standalone distribution. Fix and release in this child, then update its registry entries and gitlink. |
| Standalone content recipes and primitives | [recoupable/recoup-content-plugin](https://github.com/recoupable/recoup-content-plugin): `skills/`, `references/` and retained `commands/` | Maintained standalone distribution. Fix and release in this child, then update its registry entries and gitlink. |
| Standalone research workflows | [recoupable/recoup-research-plugin](https://github.com/recoupable/recoup-research-plugin): `skills/`, `references/`, `agents/`, `evals/` and retained `commands/` | Maintained standalone distribution. Fix and release in this child, then update its registry entries and gitlink. |
| Discovery metadata, selected child revisions and registry checks | [recoupable/marketplace](https://github.com/recoupable/marketplace): `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, gitlinks and `scripts/validate_marketplace.py` | Maintained registry. It selects child releases; it does not own their implementation or copy their source. |

For a new broad skill, start in Skills. For a change to an existing standalone
workflow, start in that child. A proposed new product-like bundle belongs in a
child repository and must pass this registry's addition process; it is not a new
sub-plugin inside Skills. Do not create a second implementation solely because a
domain appears in both families.

The currently selected child releases provide README guidance, not `AGENTS.md`.
Read the child README, manifests and relevant skills before editing. If a child
later adds its own instructions, follow those too. Skills' skill-local portability,
no-command and hook-free rules govern Skills and its generated distributions;
they do not authorize deleting compatibility files or hooks from a standalone
release. For example, the catalog child retains source-file protection while the
consolidated plugin documents hook-free operation.

## Propagate a shared fix deliberately

1. Identify the failing behavior and its owning implementation. API behavior is
   owned by [recoupable/api](https://github.com/recoupable/api); the maintained API
   reference is owned by [recoupable/docs](https://github.com/recoupable/docs).
   Fix a server defect there before describing the behavior as released in a
   package. A package instruction defect belongs in the package source.
2. Search both Skills and the relevant standalone child for consumers of that
   behavior: endpoint, field, auth flow, command, helper or workflow. Record each
   affected path and owning PR, or why a superficially similar consumer is not
   affected. Domain overlap alone is not a requirement to duplicate a fix.
3. Change each affected source through its own feature branch and PR. Preserve
   that package's actual layout, permissions and supported workflow. Within Skills,
   update canonical files and the copies registered in `scripts/vendored.json`;
   its vendoring checks do not synchronize standalone repositories. Between the
   two families, compare the relevant behavior with focused fixtures or documented
   examples, not whole-tree byte equality. There is no automatic mirror or
   cross-family generation/parity job.
4. Validate in each owner. Skills requires its five gates and applicable package
   checks/builds in `AGENTS.md`. A standalone child requires its documented checks
   and focused regressions for the changed behavior; catalog's README lists its
   Python test scripts. Where a child has only prose/evals, review those examples
   and add a focused executable check when the change is executable. Record any
   untested host/provider behavior explicitly rather than treating JSON parsing
   as runtime acceptance.
5. Release each affected package separately. For standalone content changes,
   follow the README release checklist: choose the appropriate semantic version,
   align Claude/Codex/Cursor child manifests, review and merge the child PR, then
   update both marketplace versions, immutable refs and the registry gitlink to
   that merged commit in a registry PR. Verify all three child manifests; the
   registry CI guard reads Claude/Codex manifests and does not replace the Cursor
   check. A metadata/pin-only registry correction does not invent a child version.
6. For Skills, follow its own source-manifest and generated-release rules. A
   generated artifact version is not a standalone child version. Directory
   submission, administrator distribution and host refresh remain separate from
   source merge or GitHub release. Record the commits, checks, package version and
   outstanding host verification in the owning PRs; update Mono references only
   through its separate repository workflow after the owning changes land.

The contributor making the shared fix owns this impact record until every named
consumer has a reviewed disposition. Each repository's maintainers review and
release their own change; a registry PR cannot release a Skills or child-code fix.

## Compatibility and migration

Keep existing package identifiers, install paths and selected versions unless the
owning release explicitly changes them. None of the four standalone packages is
an alias for `recoup-plugin`. Installing or updating one family does not update,
rename or disable the other; keep an existing install until its operator chooses
a separately verified replacement. Avoid duplicate active copies when diagnosing
host behavior, using the package's existing upgrade instructions.

The old `recoup-skills` to `recoup-plugin` identifier transition is within the
consolidated family; follow the [Skills upgrade instructions](https://github.com/recoupable/skills#readme).
It is not a migration order for the four standalone plugins. Catalog and Content
also document compatibility command files alongside skill entry points. Retain
those files under their child release policy; their legacy format does not make
the entire package migration-only.

Any future retirement or cross-family migration needs a reviewed proposal in the
affected owners naming the replacement, capability gaps, retained support,
installation steps, data/permission implications and host acceptance evidence.
Do not remove, redirect or silently replace a package merely to eliminate overlap.
