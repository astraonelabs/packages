> Adendo operacional — 08/10/2026: as tabelas abaixo são o snapshot histórico
> de 02/08/2026 e não descrevem as entradas vigentes. O workflow CI01 usa
> `vars.ACCESS_CONTROL_READER_CLIENT_ID` para `client-id` e
> `secrets.ACCESS_CONTROL_READER_PRIVATE_KEY` para `private-key`, nos jobs build
> e verify-consumer. Os mesmos valores do App reader são disponibilizados em
> Foundation e Packages; instalação/token continuam somente em Access Control,
> Contents read. Nenhuma configuração remota foi auditada ou alterada por este
> adendo. As referências legadas abaixo são preservadas como evidência histórica.

# Actions credential inventory

This is a metadata-only audit of the Packages repository's configured
GitHub Actions credentials. It is intentionally limited to names, observed
workflow references, and non-sensitive purpose.

Audit snapshot: 2026-08-02.

Historical owning repository at that audit: `Masterix-Sistemas/composer-registry`.
Current configured repository and destination: `astraonelabs/packages` and
`https://astraonelabs.github.io/packages/`. The task 10 change preserves the
existing secret names; their current operational configuration and installation
access were not re-audited. The reader-auth action now derives `astraonelabs`
repository names from the reviewed Satis sources.

## Configured repository secret names

| Secret name | Non-sensitive purpose | Observed status |
| --- | --- | --- |
| `COMPOSER_REGISTRY_READER_APP_ID` | Supplies the read-only reader-auth action with the app identifier it needs to mint workflow access. | Configured name observed; referenced by both publication jobs. |
| `COMPOSER_REGISTRY_READER_PRIVATE_KEY` | Supplies the read-only reader-auth action with its signing credential. | Configured name observed; referenced by both publication jobs. |

No repository-level Actions variables were observed at audit time.

## Observed workflow references

The configured names are referenced by the public workflow as follows:

| Workflow | Job | Reference | Action input |
| --- | --- | --- | --- |
| [`publish.yml`](../.github/workflows/publish.yml) | `build` | `secrets.COMPOSER_REGISTRY_READER_APP_ID` | `app-id` |
| [`publish.yml`](../.github/workflows/publish.yml) | `build` | `secrets.COMPOSER_REGISTRY_READER_PRIVATE_KEY` | `private-key` |
| [`publish.yml`](../.github/workflows/publish.yml) | `verify-consumer` | `secrets.COMPOSER_REGISTRY_READER_APP_ID` | `app-id` |
| [`publish.yml`](../.github/workflows/publish.yml) | `verify-consumer` | `secrets.COMPOSER_REGISTRY_READER_PRIVATE_KEY` | `private-key` |

The workflow uses these inputs to configure authenticated read-only source
access for catalog building and consumer verification. The names in the first
table are configured repository metadata; the second table records where the
workflow references those names. Neither table is a record of secret values.

## Excluded from this inventory

Never add any of the following to this repository or its documentation:

- secret values, private key material, or access tokens;
- GitHub App installation identifiers or installation details;
- unverified identity or ownership claims about the GitHub App;
- local credential files, shell exports, or developer machine paths.

Repeat this names-only comparison when the workflow or credential integration
changes.
