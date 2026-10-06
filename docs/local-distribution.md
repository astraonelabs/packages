# Distribuição local da candidata 2.0.0

As tags reais do Access Control até v1.1.3 declaram `masterix/identity-access`.
A retirada incompatível dos contratos antigos escolhe a próxima major **2.0.0**;
Foundation e Satis selecionam `astraone/access-control:^2.0`. O manifest do pacote
não fixa versão: a tag real será a fonte após autorização. Sem tags novas nesta
validação, o metadado local fixa versão e commit explicitamente.

```sh
python3 tests/catalog-cli.py
python3 scripts/build-local-candidate.py ../access-control .build/candidate-2
python3 tests/check-local-candidate.py ../access-control .build/candidate-2
```

Usar diretório novo; o comando recusa overwrite, fonte rastreada suja ou manifest
com nome antigo. Clona a revisão Git limpa sem criar tag, lê seu manifest real e
invoca Satis pinado ao mesmo digest do workflow. A seleção candidata é **separada**
da seleção de releases reais: o workflow continua lendo tags e seus manifests,
sem admitir desenvolvimento/candidatas locais. Não existe publicação automática.

Artefatos: `candidate.json`, `provenance.json`, `source.git/` e `catalog/` sob
`.build/`, todos ignorados. O catálogo contém somente o nome novo, versão2.0.0
e source Git local na revisão exata; não contém fontes/archives. O checker observa
nome/versão/referência, inventário de tags inalterado e ausência de aliases. Nunca
publicar essa saída ou mover/retaggear referências históricas.

Para consumir, servir `catalog/` no path HTTP `/packages/` e montar `source.git`
no mesmo path absoluto dentro do container PHP8.5. O consumidor usa repositório
Composer HTTP local, sem path de pacote, vendor anterior ou credenciais do pacote.
O override HTTP local com `secure-http:false` é ignorado; a configuração de
produção conserva HTTPS. Packagist serve as outras dependências do lock existente.

A instalação limpa real é documentada no Foundation em
[instalação e distribuição](https://github.com/astraonelabs/foundation/blob/main/docs/release-and-consumption.md).
Ela usa rede/volumes/MySQL/Mailpit e checkout novos; migrations, bootstrap,
login, convite, aceite, leitura200 e escrita403 foram exercitados pela UI/CLI reais.
O mesmo cenário foi repetido por path com `options.versions:2.0.0` e `^2.0`.

Evidência local11: `/tmp/astraone-task11-implementation.md`, incluindo SHAs,
locks, hashes, comandos e relatórios. Isso não afirma que os links remotos já
contenham estas mudanças nem que o catálogo público atualizado tenha sido validado.
Depois da revisão/merge, obter autorização para a tag/release do pacote, regenerar
com `build-catalog.sh satis.json public`, reconciliar o lock Foundation com o SHA
da tag integrada e publicar manualmente somente os metadados de fontes reais.
