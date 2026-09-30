#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
fixture_directory="${2:-.build/preflight}"
python3 scripts/prepare-local-catalog.py "${1:-../access-control}" "$fixture_directory"
bash scripts/build-catalog.sh "$fixture_directory/projected.json" "$fixture_directory/projected-output" 2>&1 | tee "$fixture_directory/projected-build.log"
if bash scripts/build-catalog.sh "$fixture_directory/legacy.json" "$fixture_directory/legacy-output" >"$fixture_directory/legacy-build.log" 2>&1; then
    echo 'Legacy-only catalog unexpectedly passed validation.' >&2
    exit 1
fi
if ! grep -Eq 'Catalog rejected: (available packages differ|missing stable releases)' "$fixture_directory/legacy-build.log"; then
    cat "$fixture_directory/legacy-build.log" >&2
    echo 'Legacy-only generation failed for an unexpected reason.' >&2
    exit 1
fi
python3 tests/check-projection.py "$fixture_directory"
printf '%s\n' 'PASS: real Satis selected the projected name, excluded old tags and rejected a catalog without new releases.'
