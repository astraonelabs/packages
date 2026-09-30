#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
repo_root="$PWD"
config_path="$(realpath "${1:-satis.json}")"
output_path="$(realpath -m "${2:-public}")"

case "$config_path" in "$repo_root/"*) ;; *) echo 'Configuration must be inside this checkout.' >&2; exit 1 ;; esac
case "$output_path" in "$repo_root/public"|"$repo_root/.build/"*) ;; *) echo 'Output must be public/ or inside .build/.' >&2; exit 1 ;; esac
if [ -d "$output_path" ] && [ -n "$(ls -A "$output_path")" ]; then
    echo 'Use a new empty output directory to avoid exporting stale metadata.' >&2
    exit 1
fi
mkdir -p "$output_path"
composer_directory="${COMPOSER_HOME:-$repo_root/.build/composer}"
mkdir -p "$composer_directory" "$repo_root/.build"
export COMPOSER_HOME="$composer_directory"
selection_directory="$(mktemp -d "$repo_root/.build/selection-XXXXXX")"
python3 scripts/select-releases.py "$config_path" "$selection_directory"
selected_config="$selection_directory/satis.selected.json"
docker run --rm --init \
    --user "$(id -u):$(id -g)" \
    --volume "$repo_root:/build" \
    --volume "$composer_directory:/composer" \
    composer/satis@sha256:6262eb4a007086b5589b7558789caf3d3e78c570481c5e0638398c00c4661df1 \
    build --no-interaction "/build/${selected_config#"$repo_root/"}" "/build/${output_path#"$repo_root/"}"
python3 scripts/validate-catalog.py "$config_path" "$output_path"
printf 'Selection evidence: %s/selection.json\n' "$selection_directory"
