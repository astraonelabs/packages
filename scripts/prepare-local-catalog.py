#!/usr/bin/env python3
"""Create ignored local Satis inputs; the projected tag is never a release."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def git(*args, cwd=None, env=None):
    return subprocess.check_output(["git", *args], cwd=cwd, env=env, text=True).strip()


source = Path(sys.argv[1] if len(sys.argv) > 1 else "../access-control").resolve()
work = Path(sys.argv[2] if len(sys.argv) > 2 else ".build/preflight").resolve()
if not work.is_relative_to(ROOT / ".build") or work == ROOT / ".build":
    sys.exit("Fixture output must be a new directory inside .build/.")
if work.exists():
    sys.exit("Fixture output already exists; choose a new directory.")
revision = git("rev-parse", "HEAD", cwd=source)
tags = {}
for tag in git("tag", "--list", cwd=source).splitlines():
    tags[tag] = json.loads(git("show", f"{tag}:composer.json", cwd=source))["name"]
work.mkdir(parents=True)
for name in ("legacy", "projected"):
    git("clone", "--no-local", "--no-checkout", str(source), str(work / name))
    git("checkout", "-b", "catalog-preflight", revision, cwd=work / name)
manifest_path = work / "projected/composer.json"
manifest = json.loads(manifest_path.read_text())
manifest["name"] = "astraone/access-control"
manifest["description"] = "PREPARATORY projection for local catalog checks; not a consumable release."
manifest.pop("version", None)
manifest_path.write_text(json.dumps(manifest, indent=4) + "\n")
git("add", "composer.json", cwd=manifest_path.parent)
env = {**os.environ, "GIT_AUTHOR_NAME": "Catalog Preflight", "GIT_AUTHOR_EMAIL": "preflight@astraone.test", "GIT_COMMITTER_NAME": "Catalog Preflight", "GIT_COMMITTER_EMAIL": "preflight@astraone.test", "GIT_AUTHOR_DATE": "2000-01-01T00:00:00Z", "GIT_COMMITTER_DATE": "2000-01-01T00:00:00Z"}
git("-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "commit", "-m", "build: project preparatory package identity", cwd=manifest_path.parent, env=env)
git("-c", "tag.gpgsign=false", "tag", "v0.0.0", cwd=manifest_path.parent)
for name in ("legacy", "projected"):
    config = json.loads((ROOT / "satis.json").read_text())
    config["repositories"] = [{"type": "vcs", "url": str(work / name)}]
    config["output-dir"] = str((work / f"{name}-output").relative_to(ROOT))
    (work / f"{name}.json").write_text(json.dumps(config, indent=4) + "\n")
provenance = {"preparatory_only": True, "input_revision": revision, "existing_tags": tags, "projected_revision": git("rev-parse", "HEAD", cwd=manifest_path.parent), "synthetic_tag": "v0.0.0", "changes": ["Composer name and preparatory description only; package runtime contracts are untouched."]}
(work / "provenance.json").write_text(json.dumps(provenance, indent=4) + "\n")
print(f"Prepared local-only projection at {work}; input revision {revision}; never publish this fixture.")
