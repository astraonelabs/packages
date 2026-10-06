#!/usr/bin/env python3
"""Build local-only release-candidate metadata from an immutable commit, without tags."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.0.0"


def git(*args, cwd=None):
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def build(source, work):
    if not work.is_relative_to(ROOT / ".build") or work == ROOT / ".build" or work.exists():
        raise ValueError("Use a new output directory inside .build/.")
    if git("status", "--porcelain", "--untracked-files=no", cwd=source):
        raise ValueError("Candidate source must have no tracked changes.")
    revision = git("rev-parse", "HEAD", cwd=source)
    manifest = json.loads(git("show", f"{revision}:composer.json", cwd=source))
    if manifest["name"] != "astraone/access-control":
        raise ValueError("Candidate must implement the new package identity.")
    tags = []
    for tag in git("tag", "--list", cwd=source).splitlines():
        reference = git("rev-parse", f"{tag}^{{commit}}", cwd=source)
        name = json.loads(git("show", f"{reference}:composer.json", cwd=source))["name"]
        tags.append({"tag": tag, "reference": reference, "name": name})
    work.mkdir(parents=True)
    checkout = work / "source.git"
    git("clone", "--bare", "--no-local", str(source), str(checkout))
    manifest.pop("dist", None)
    manifest["version"] = VERSION
    manifest["source"] = {"type": "git", "url": str(checkout), "reference": revision}
    config = json.loads((ROOT / "satis.json").read_text())
    config["repositories"] = [{"type": "package", "package": [manifest]}]
    config["output-dir"] = str(work / "catalog")
    config_path = work / "candidate.json"
    config_path.write_text(json.dumps(config, indent=4) + "\n")
    provenance = {"local_candidate_only": True, "version": VERSION, "input_revision": revision,
                  "source_tree": git("rev-parse", "HEAD^{tree}", cwd=source), "existing_tags": tags,
                  "source_url": str(checkout), "tags_created": False, "published": False}
    (work / "provenance.json").write_text(json.dumps(provenance, indent=4) + "\n")
    subprocess.run(["docker", "run", "--rm", "--init", "--user", git_user(),
                    "--volume", f"{ROOT}:{ROOT}", "--workdir", str(ROOT),
                    "composer/satis@sha256:6262eb4a007086b5589b7558789caf3d3e78c570481c5e0638398c00c4661df1",
                    "build", "--no-interaction", str(config_path), str(work / "catalog")], check=True)
    subprocess.run(["python3", str(ROOT / "scripts/validate-catalog.py"), str(config_path), str(work / "catalog")], check=True)
    print(f"Local candidate {VERSION} from {revision}: {work}; never publish this output.")


def git_user():
    import os
    return f"{os.getuid()}:{os.getgid()}"


if __name__ == "__main__":
    try:
        build(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
    except (IndexError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        sys.exit(f"Local candidate failed: {error}")
