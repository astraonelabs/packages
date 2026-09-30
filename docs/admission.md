# Plugin admission

Admission is a reviewed Packages change. It does not publish automatically.

Before requesting a change, confirm the plugin owns a package-native release
lifecycle and that the Packages GitHub App has authorized read-only access.
Add its current `https://github.com/astraonelabs/<repository>.git` VCS URL and
Composer name to `satis.json`. Review the matching selector and validator
allowlist before broadening the catalog. The current reviewed scope admits only
`astraone/access-control` from `astraonelabs/access-control`.

Read each release's tagged manifest rather than trusting the default branch's
name. Historical tags naming the previous package must not be exported under
the new identity. Run [local generation](local-generation.md) and inspect its
selection inventory and resulting metadata before publication.

A merged allowlist change and a stable source release are separate prerequisites
for the manually authorized [publication](publication.md). Do not edit generated
`public/` files to admit a package or bypass reader-access review.

The catalog contains metadata only. Package code stays in its GitHub repository;
consumer authentication is still required and source archives are not proxied.
