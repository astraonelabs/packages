#!/usr/bin/env python3
"""Validate the metadata-only catalog before it can be uploaded to Pages."""
import json
from pathlib import Path
import re
import sys


def validate(config_path, output):
    config = json.loads(config_path.read_text())
    required = set(config["require"])
    if config.get("name") != "astraone/packages" or config.get("homepage") != "https://astraonelabs.github.io/packages/":
        raise ValueError("unexpected catalog identity or destination")
    if required != {"astraone/access-control"}:
        raise ValueError("unexpected package allowlist")
    if "archive" in config or any(config.get(key, False) for key in ("require-all", "require-dependencies", "require-dev-dependencies")):
        raise ValueError("source archives or unselected packages are enabled")
    if config.get("minimum-stability") != "stable":
        raise ValueError("only stable releases may be exported")
    main = json.loads((output / "packages.json").read_text())
    if set(main.get("available-packages", [])) != required:
        raise ValueError("available packages differ from the allowlist")
    packages = {}
    for path in output.rglob("*"):
        if path.is_symlink():
            raise ValueError("symlinks are not catalog artifacts")
        if path.is_dir():
            if path.name in {"dist", "downloads", "vendor", ".git", "src"}:
                raise ValueError("source or archive directory found")
            continue
        if path.suffix not in {".json", ".html"}:
            raise ValueError("non-metadata artifact found")
        content = path.read_text()
        if "masterix/identity-access" in content:
            raise ValueError("old package identity found")
        if path.suffix == ".json":
            document = json.loads(content)
            for name, versions in (document.get("packages") or {}).items():
                packages.setdefault(name, []).extend(versions.values() if isinstance(versions, dict) else versions)
    if set(packages) != required or any(not versions for versions in packages.values()):
        raise ValueError("missing stable releases or unselected package metadata")
    for name, versions in packages.items():
        for version in versions:
            if version.get("name") != name or not re.fullmatch(r"v?\d+\.\d+\.\d+(?:\.\d+)?(?:\+[-0-9A-Za-z.]+)?", version.get("version", "")):
                raise ValueError("invalid identity or non-stable version")
            if not version.get("source", {}).get("reference"):
                raise ValueError("missing source revision")
    print("Catalog valid: " + ", ".join(sorted(packages)) + "; stable metadata only; no old identity or source archives.")


if __name__ == "__main__":
    try:
        validate(Path(sys.argv[1]), Path(sys.argv[2]))
    except (IndexError, OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        print(f"Catalog rejected: {error}", file=sys.stderr)
        sys.exit(1)
