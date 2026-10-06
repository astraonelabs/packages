#!/usr/bin/env python3
"""Select stable tags by their own manifest, before Composer normalizes VCS names."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def git(*arguments, cwd=None):
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_ASKPASS": str(ROOT / "scripts/git-reader.sh")}
    return subprocess.check_output(
        ["git", "-c", "credential.helper=", *arguments], cwd=cwd, env=env, text=True,
    ).strip()


def select(config_path, directory):
    config = json.loads(config_path.read_text())
    required = set(config["require"])
    if required != {"astraone/access-control"} or "archive" in config:
        raise ValueError("unexpected allowlist or source archive configuration")
    packages = []
    inventory = []
    seen = set()
    for index, repository in enumerate(config["repositories"]):
        if repository["type"] != "vcs":
            raise ValueError("selection requires Git VCS sources")
        source = repository["url"]
        checkout = directory / f"source-{index}.git"
        git("clone", "--bare", "--no-local", source, str(checkout))
        for tag in git("tag", "--list", cwd=checkout).splitlines():
            if not re.fullmatch(r"v?\d+\.\d+\.\d+", tag):
                continue
            revision = git("rev-parse", f"{tag}^{{commit}}", cwd=checkout)
            manifest = json.loads(git("show", f"{revision}:composer.json", cwd=checkout))
            name = manifest.get("name")
            entry = {"tag": tag, "reference": revision, "name": name, "selected": name in required}
            inventory.append(entry)
            if name not in required:
                continue
            version = tag.removeprefix("v")
            if (name, version) in seen:
                raise ValueError("duplicate selected package version")
            seen.add((name, version))
            manifest["version"] = version
            manifest["source"] = {"type": "git", "url": source, "reference": revision}
            manifest.pop("dist", None)
            packages.append(manifest)
    config["repositories"] = [{"type": "package", "package": packages}] if packages else []
    (directory / "satis.selected.json").write_text(json.dumps(config, indent=4) + "\n")
    (directory / "selection.json").write_text(json.dumps(inventory, indent=4) + "\n")
    print(f"Selected {len(packages)} stable releases by tagged manifest; skipped {sum(not entry['selected'] for entry in inventory)} old-named tags.")


if __name__ == "__main__":
    try:
        select(Path(sys.argv[1]), Path(sys.argv[2]))
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f"Release selection failed: {error}", file=sys.stderr)
        sys.exit(1)
