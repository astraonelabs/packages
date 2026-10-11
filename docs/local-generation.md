# Local generation and version strategy

This guide verifies catalog preparation without publishing and without waiting
for a newly named release. Run commands from the Packages checkout.

## Existing versions and the rename boundary

The independent Access Control checkout was inspected at
`048b4f07d38c4b5148a75acfa8c1f13d5c5d49c1`. Its existing tags are `v0.1.32`,
`v1.0.0`, `v1.1.0`, `v1.1.1`, `v1.1.2` and `v1.1.3`. Every tagged manifest
names `masterix/identity-access`. None is a release of `astraone/access-control`.

Preserve these tags as historical references; do not retag them or give them
compatibility aliases. The runtime rename is a breaking contract change.
A tarefa11 definiu 2.0.0 e `^2.0` após reinspecionar as tags reais. Consulte
[distribuição local](local-distribution.md) para a prova consumível sem tags.
A projeção abaixo conserva seu papel histórico de preparação10. O catálogo real seleciona `^2.0`; a projeção histórica abaixo usa `*`
somente no input ignorado para admitir sua versão sintética0.0.0, sem mudar a
constraint2.0 do consumidor ou do catálogo de distribuição. A synthetic `v0.0.0` below is a test input only and reserves no
release number in the original repository.

Composer's Git VCS driver can normalize every version to the package name from
the default branch. A name-only Satis requirement therefore cannot prove that
old tags were excluded after that branch is renamed. The shared build reads
each stable tag's actual manifest and SHA first, excludes old-named manifests,
and supplies explicit package versions to Satis. The real Satis check asserts
that only the synthetic version and its projected revision are present.

## Preparatory fixture and verification

```sh
python3 tests/catalog-cli.py
bash scripts/check-local-catalog.sh ../access-control .build/preflight
```

Choose a new `.build/<name>` if that output already exists. The script refuses
to overwrite fixtures. It clones the current package and its real tags into
`legacy/` and `projected/`, changes only the projected manifest name and
preparatory description, and commits/tags in that ignored clone. Original
package files, branch and tags remain unchanged. Fixed fixture commit dates
make the projection reproducible for the same input revision.

The package's old namespaces remain in the projection. It is deliberately not
a functioning new package or a substitute for task 11's installation test.

Artifacts in the chosen fixture directory:

- `provenance.json`: input revision, real tag identities, projected revision
  and the explicit preparatory marker.
- `projected.json` and `legacy.json`: local generation inputs.
- `projected-output/`: real Satis metadata, HTML index and Composer p2 data.
- `projected-build.log`: successful generation and validation.
- `legacy-output/` and `legacy-build.log`: real generation with no new releases
  and the expected validation rejection.

Each build also retains its tag inventory at
`.build/selection-*/selection.json`, including which tagged manifests were
selected and their immutable revisions. The original source checkout, fixture
clones, inventory and logs are never part of `public/` or the Pages upload.

The validator CLI tests exercise approved metadata, missing releases, old
identities (including a replacement entry), development versions, source files,
archives, archive configuration and an old destination. The actual generation
crosses Git selection and the pinned Satis CLI, not mocked metadata generation.

## Build from real released sources

The same script runs in the workflow and locally:

```sh
bash scripts/build-catalog.sh satis.json public
```

The output must be empty to prevent stale files from a previous catalog being
published. Alternative outputs must live under `.build/`. Use a fresh output
path instead of deleting another developer's artifacts.

The workflow provides a short-lived GitHub App reader credential through
Composer's ignored authentication file. For local private-source generation,
use an already authorized reader credential in an external `COMPOSER_HOME`.
The Git askpass helper reads that file without placing its value in command
arguments, source URLs, metadata or documentation. Do not commit or print it.
The local projection requires no remote package credential.

Satis is pinned to the existing image digest in `scripts/build-catalog.sh`.
Source downloads during selection remain in `.build/`; no Satis archive
configuration exists and the uploaded output is metadata only.

References: [Satis selection and archives](https://composer.github.io/satis/using)
and [Composer repository types](https://getcomposer.org/doc/05-repositories.md).
