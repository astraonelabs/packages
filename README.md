# Astra One Labs Packages

Packages is the public Composer metadata catalog for approved Astra One Labs
private packages. The configured Pages destination is
`https://astraonelabs.github.io/packages/`. Source stays in its GitHub repository;
the catalog does not publish package contents, source archives or credentials.

The reviewed catalog identifies itself as `astraone/packages` and admits
`astraone/access-control` from
`https://github.com/astraonelabs/access-control.git`. A versão planejada é **2.0.0**, com constraint `^2.0` no catálogo e Foundation.
A candidata local foi validada antes de qualquer release/publicação. Consulte
[distribuição local](docs/local-distribution.md).

## Generate and verify locally

Git, Python 3, Bash and Docker are required. Before a new release exists, run the
explicitly preparatory check against the independent local checkout:

```sh
python3 tests/catalog-cli.py
bash scripts/check-local-catalog.sh ../access-control .build/preflight
```

This creates an ignored Git projection with a synthetic `v0.0.0` tag, invokes
real pinned Satis and checks that old-named tags cannot enter the new catalog.
It also generates from the unchanged source and proves that a catalog without
new releases fails validation. It does not change or tag the original package.
The fixture changes only the Composer name and preparatory description;
runtime namespaces and contracts remain the original ones. Never upload this
projection or treat it as a consumable release.

For actual released metadata, configure your authorized read-only source access
locally and run the same command used by the publication workflow:

```sh
bash scripts/build-catalog.sh satis.json public
```

Use a new empty output directory for each run. The build clones sources into
ignored `.build/` directories, reads each stable tag's own `composer.json`,
selects only the admitted name and passes those immutable revisions to Satis.
Selecting solely by the default branch's name is insufficient: Composer's VCS
normalization can relabel old tags with that name. Validation checks exact
package membership, stable versions, source revisions, absence of the old
identity and absence of source/archive files. Generation never deploys.

## Publish after review and release

Publication remains manual through `workflow_dispatch`. The workflow builds
with `scripts/build-catalog.sh`, uploads only `public/`, deploys to Pages and
verifies an authenticated consumer. Neither releasing a plugin nor generating
locally dispatches publication. Publication has not been performed by this
preparatory change.

O reader usa a variable `ACCESS_CONTROL_READER_CLIENT_ID` e o secret
`ACCESS_CONTROL_READER_PRIVATE_KEY`, do mesmo App, disponíveis em Foundation e
Packages. A instalação e o token continuam limitados a Access Control com
Contents read. Os nomes de entradas legados foram substituídos; o inventário
preserva o snapshot histórico e registra a configuração vigente em adendo.
O acesso operacional precisa ser configurado antes da publicação.

## Guides and ownership

- [Local generation and version strategy](docs/local-generation.md).
- [Manual publication](docs/publication.md).
- [Plugin admission](docs/admission.md).
- [Release handoff](docs/release-handoff.md).
- [Consumer and local integration](docs/consumer-integration.md).
- [Credential inventory](docs/credential-inventory.md).

[Access Control](https://github.com/astraonelabs/access-control) owns the package
contract and release lifecycle. [Foundation](https://github.com/astraonelabs/foundation)
owns its Composer constraints and local development overrides. Packages owns
admission, tagged-manifest selection, metadata generation and publication.
