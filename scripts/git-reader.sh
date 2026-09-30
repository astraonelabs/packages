#!/usr/bin/env bash
set -euo pipefail
case "${1:-}" in
    *Username*) printf '%s\n' 'x-access-token' ;;
    *Password*) python3 -c 'import json, os, pathlib; print(json.loads((pathlib.Path(os.environ["COMPOSER_HOME"]) / "auth.json").read_text())["github-oauth"]["github.com"])' ;;
    *) exit 1 ;;
esac
