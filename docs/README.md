# Packages guides

Astra One Labs Packages publishes public Composer metadata for approved private
packages. Package code and authenticated source retrieval remain on GitHub.

| Need | Guide |
| --- | --- |
| Generate before a new release and inspect version strategy | [Local generation](local-generation.md) |
| Hand a real stable release to catalog publication | [Release handoff](release-handoff.md) |
| Review the source and package allowlist | [Plugin admission](admission.md) |
| Publish manually after authorization | [Manual publication](publication.md) |
| Consume metadata or integrate a local checkout | [Consumer integration](consumer-integration.md) |
| Review credential names and workflow references | [Credential inventory](credential-inventory.md) |

Packages owns admission, tag selection, metadata generation and publication.
[Access Control](https://github.com/astraonelabs/access-control) owns the package
and its releases; [Foundation](https://github.com/astraonelabs/foundation) owns
the consumer and local overrides. The fixture projection used by task 10 is
preparation evidence and must not be published.

The guides record no credential values, keys, tokens or installation identifiers.
