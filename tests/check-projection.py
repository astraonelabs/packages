#!/usr/bin/env python3
"""The preparatory CLI must select one synthetic release, never old tags."""
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
provenance = json.loads((root / "provenance.json").read_text())
packages = {}
for path in (root / "projected-output/include").glob("*.json"):
    packages.update(json.loads(path.read_text())["packages"])
assert set(packages) == {"astraone/access-control"}, packages.keys()
versions = packages["astraone/access-control"]
assert set(versions) == {"0.0.0"}, versions.keys()
assert versions["0.0.0"]["source"]["reference"] == provenance["projected_revision"]
assert all(name == "masterix/identity-access" for name in provenance["existing_tags"].values())
print("PASS: only the synthetic v0.0.0 projection was selected; all real old-named tags were excluded.")
