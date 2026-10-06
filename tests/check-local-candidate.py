#!/usr/bin/env python3
"""Check real Satis output against the independent source commit and tags."""
import json
from pathlib import Path
import subprocess
import sys

source = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
provenance = json.loads((work / 'provenance.json').read_text())
assert provenance['input_revision'] == revision
assert provenance['version'] == '2.0.0'
assert provenance['tags_created'] is False and provenance['published'] is False
source_tags = subprocess.check_output(['git', 'tag', '--list'], cwd=source, text=True)
clone_tags = subprocess.check_output(['git', 'tag', '--list'], cwd=work / 'source.git', text=True)
assert clone_tags == source_tags
versions = []
for path in (work / 'catalog').rglob('*.json'):
    document = json.loads(path.read_text())
    packages = document.get('packages') or {}
    assert set(packages) <= {'astraone/access-control'}
    for entries in packages.values():
        versions.extend(entries.values() if isinstance(entries, dict) else entries)
assert versions, 'No consumable candidate metadata'
for package in versions:
    assert package['name'] == 'astraone/access-control'
    assert package['version'] == '2.0.0'
    assert package['source'] == {'type': 'git', 'url': str(work / 'source.git'), 'reference': revision}
    assert 'dist' not in package
    assert 'replace' not in package and 'provide' not in package
print(f'PASS: Satis exports only 2.0.0 at {revision}; no tags created and no source archives.')
