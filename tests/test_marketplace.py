import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("validator", Path(__file__).resolve().parents[1] / "scripts/validate_marketplace.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class MarketplaceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.name = "recoup-fixture-plugin"
        self.child = self.root / self.name
        self.child.mkdir()
        self.git(self.root, "init", "-q")
        self.git(self.child, "init", "-q")
        for runtime in ["claude", "codex"]:
            self.write(self.child / f".{runtime}-plugin/plugin.json", {"name": self.name, "version": "0.3.1"})
        self.git(self.child, "add", ".")
        self.git(self.child, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
        self.pin = self.git(self.child, "rev-parse", "HEAD")
        self.git(self.root, "update-index", "--add", "--cacheinfo", f"160000,{self.pin},{self.name}")
        (self.root / ".gitmodules").write_text(f'[submodule "{self.name}"]\npath = {self.name}\nurl = https://github.com/recoupable/{self.name}.git\n')
        self.paths = [self.root / ".claude-plugin/marketplace.json", self.root / ".agents/plugins/marketplace.json"]
        self.data = [
            {"plugins": [{"name": self.name, "version": "0.3.1", "source": {"source": "github", "repo": f"recoupable/{self.name}", "sha": self.pin}}]},
            {"plugins": [{"name": self.name, "version": "0.3.1", "source": {"source": "url", "url": f"https://github.com/recoupable/{self.name}.git", "ref": self.pin}}]},
        ]
        self.save()

    def git(self, root, *args):
        return subprocess.check_output(["git", "-C", str(root), *args], text=True, stderr=subprocess.PIPE).strip()

    def write(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))

    def save(self):
        for path, value in zip(self.paths, self.data):
            self.write(path, value)

    def test_exact_pin_passes_despite_dirty_child_manifest(self):
        self.write(self.child / ".claude-plugin/plugin.json", {"name": "dirty", "version": "99"})
        self.assertEqual(validator.validate(self.root), 1)

    def test_missing_mutable_and_mismatched_pins_fail(self):
        for index, key in [(0, "sha"), (1, "ref")]:
            for value in [None, "main", "f" * 40]:
                with self.subTest(runtime=index, pin=value):
                    source = self.data[index]["plugins"][0]["source"]
                    if value is None:
                        source.pop(key, None)
                    else:
                        source[key] = value
                    self.save()
                    with self.assertRaisesRegex(ValueError, "immutable|gitlink"):
                        validator.validate(self.root)
                    source[key] = self.pin

    def test_missing_duplicate_and_changed_names_fail(self):
        original = self.data[0]["plugins"]
        for plugins in [[], original * 2, [dict(original[0], name="wrong-name")]]:
            with self.subTest(plugins=plugins):
                self.data[0]["plugins"] = plugins
                self.save()
                with self.assertRaises(ValueError):
                    validator.validate(self.root)

    def test_versions_and_source_repositories_must_match(self):
        for index in [0, 1]:
            entry = self.data[index]["plugins"][0]
            entry["version"] = "0.3.2"
            self.save()
            with self.assertRaisesRegex(ValueError, "version"):
                validator.validate(self.root)
            entry["version"] = "0.3.1"
            key = "repo" if index == 0 else "url"
            original = entry["source"][key]
            entry["source"][key] = "wrong-repository"
            self.save()
            with self.assertRaisesRegex(ValueError, "repository/type"):
                validator.validate(self.root)
            entry["source"][key] = original

    def test_child_manifest_name_mismatch_fails(self):
        self.write(self.child / ".codex-plugin/plugin.json", {"name": "wrong", "version": "0.3.1"})
        self.git(self.child, "add", ".")
        self.git(self.child, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "wrong name")
        pin = self.git(self.child, "rev-parse", "HEAD")
        self.git(self.root, "update-index", "--cacheinfo", f"160000,{pin},{self.name}")
        self.data[0]["plugins"][0]["source"]["sha"] = pin
        self.data[1]["plugins"][0]["source"]["ref"] = pin
        self.save()
        with self.assertRaisesRegex(ValueError, "name mismatch"):
            validator.validate(self.root)


if __name__ == "__main__":
    unittest.main()
