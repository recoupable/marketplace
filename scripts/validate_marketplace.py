"""Check registry entries against indexed gitlinks and exact child manifests, offline."""
import argparse
import configparser
import json
from pathlib import Path
import re
import subprocess


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def entries(path):
    plugins = json.loads(path.read_text())["plugins"]
    result = {}
    for entry in plugins:
        name = entry.get("name")
        if not isinstance(name, str) or name in result:
            raise ValueError(f"{path}: missing or duplicate plugin name")
        result[name] = entry
    return result


def validate(root, plugin_root=None):
    root = Path(root)
    plugin_root = Path(plugin_root) if plugin_root else root
    claude = entries(root / ".claude-plugin/marketplace.json")
    codex = entries(root / ".agents/plugins/marketplace.json")
    links = {}
    for record in git(root, "ls-files", "--stage", "-z").split("\0"):
        if not record:
            continue
        metadata, path = record.split("\t", 1)
        mode, commit, stage = metadata.split()
        if stage != "0":
            raise ValueError(f"Unmerged index entry: {path}")
        if mode == "160000":
            links[path] = commit
    if not links or set(claude) != set(codex) or set(claude) != set(links):
        raise ValueError("Plugin names must match both marketplaces and gitlink paths")
    modules = configparser.ConfigParser()
    modules.read(root / ".gitmodules")
    urls = {}
    for section in modules.sections():
        path = modules[section]["path"]
        if path in urls:
            raise ValueError(f"Duplicate submodule path: {path}")
        urls[path] = modules[section]["url"]
    if set(urls) != set(links):
        raise ValueError("Submodule paths must match indexed gitlinks")
    for name, commit in links.items():
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
            raise ValueError(f"Invalid plugin path/name: {name}")
        repository = f"recoupable/{name}"
        url = f"https://github.com/{repository}.git"
        if urls[name] != url:
            raise ValueError(f"{name}: submodule repository does not match plugin name")
        for entry, kind, key, manifest in (
            (claude[name], "github", "sha", ".claude-plugin/plugin.json"),
            (codex[name], "url", "ref", ".codex-plugin/plugin.json"),
        ):
            source = entry.get("source", {})
            if not isinstance(source, dict):
                raise ValueError(f"{name}: source must be an object")
            pin = source.get(key, "")
            if not isinstance(pin, str) or not re.fullmatch(r"[0-9a-f]{40}", pin):
                raise ValueError(f"{name}: {key} must be an immutable 40-character commit")
            if pin != commit:
                raise ValueError(f"{name}: {key} does not match indexed gitlink {commit}")
            if source.get("source") != kind or source.get("repo" if kind == "github" else "url") != (repository if kind == "github" else url):
                raise ValueError(f"{name}: marketplace source repository/type mismatch")
            # Read the selected object, never the child working tree or mutable HEAD.
            child = json.loads(git(plugin_root / name, "show", f"{commit}:{manifest}"))
            if child.get("name") != name:
                raise ValueError(f"{name}: {manifest} name mismatch")
            version = entry.get("version")
            if not isinstance(version, str) or not version or version != child.get("version"):
                raise ValueError(f"{name}: {manifest} version mismatch")
        if claude[name]["version"] != codex[name]["version"]:
            raise ValueError(f"{name}: runtime marketplace versions disagree")
    return len(links)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--plugin-root", type=Path, help="Existing child repositories to read when this worktree has uninitialized submodules")
    args = parser.parse_args()
    try:
        count = validate(args.root, args.plugin_root)
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError, configparser.Error) as error:
        parser.exit(1, f"Marketplace validation failed: {error}\n")
    print(f"Validated {count} plugins against exact gitlinks and both child manifests")
