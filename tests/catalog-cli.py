#!/usr/bin/env python3
"""Exercise the catalog validator through its CLI, with independent examples."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CONFIG = {
    "name": "astraone/packages",
    "homepage": "https://astraonelabs.github.io/packages/",
    "require": {"astraone/access-control": "*"},
    "minimum-stability": "stable",
}
PACKAGE = {
    "name": "astraone/access-control",
    "version": "0.0.0",
    "source": {"type": "git", "url": "https://github.com/astraonelabs/access-control.git", "reference": "a" * 40},
}


def run_case(name, mutate, expected):
    with tempfile.TemporaryDirectory(prefix="astraone-catalog-test-") as directory:
        root = Path(directory)
        config = copy.deepcopy(CONFIG)
        package = copy.deepcopy(PACKAGE)
        catalog = {"available-packages": ["astraone/access-control"], "packages": {}}
        included = {"packages": {"astraone/access-control": {"0.0.0": package}}}
        (root / "include").mkdir()
        mutate(root, config, catalog, included)
        (root / "config.json").write_text(json.dumps(config))
        (root / "packages.json").write_text(json.dumps(catalog))
        (root / "include/packages.json").write_text(json.dumps(included))
        result = subprocess.run(
            ["python3", str(ROOT / "scripts/validate-catalog.py"), str(root / "config.json"), str(root)],
            text=True, capture_output=True,
        )
        assert result.returncode == expected, f"{name}: {result.stdout}{result.stderr}"
        if expected == 0:
            assert "astraone/access-control" in result.stdout
        else:
            assert "Catalog rejected:" in result.stderr
        print(f"PASS: {name}")


run_case("approved stable metadata", lambda *args: None, 0)
run_case("empty catalog before new release", lambda root, config, catalog, included: included.update(packages={}), 1)
run_case("old named tag must not be exported", lambda root, config, catalog, included: included["packages"].update({"masterix/identity-access": {"1.1.3": {"name": "masterix/identity-access", "version": "1.1.3"}}}), 1)
run_case("development version must not be exported", lambda root, config, catalog, included: included["packages"]["astraone/access-control"]["0.0.0"].update(version="dev-main"), 1)
run_case("archive output must not be exported", lambda root, *args: (root / "source.zip").write_bytes(b"source"), 1)
run_case("package source must not be exported", lambda root, *args: (root / "source.php").write_text("<?php"), 1)
run_case("old identity in metadata must not be exported", lambda root, config, catalog, included: included["packages"]["astraone/access-control"]["0.0.0"].update(replace={"masterix/identity-access": "*"}), 1)
run_case("old destination must not pass", lambda root, config, *args: config.update(homepage="https://masterix-sistemas.github.io/composer-registry"), 1)
run_case("archive configuration must not pass", lambda root, config, *args: config.update(archive={"directory": "dist"}), 1)
