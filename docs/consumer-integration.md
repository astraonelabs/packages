# Consumer and local integration

Packages serves Composer metadata at `https://astraonelabs.github.io/packages/`.
A consumer needs its own authorized GitHub access to retrieve private source.

For the resulting released package, the intended consumer configuration is:

```json
{
    "repositories": [
        { "type": "composer", "url": "https://astraonelabs.github.io/packages/" }
    ]
}
```

O pacote consumido é `astraone/access-control:^2.0`; a release planejada é 2.0.0.
Nenhuma tag antiga satisfaz esse nome. O catálogo público atualizado permanece
não verificado até publicação autorizada. A validação anterior à publicação usa
[metadados locais](local-distribution.md) na revisão integrada exata, com
instalação limpa real e o mesmo contrato no override path do Foundation.
