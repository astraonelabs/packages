# Manual publication

Catalog generation and publication are separate operations. A plugin release
never dispatches the Packages workflow automatically. Review admission and
confirm a real stable `astraone/access-control` release with the integrated
package. A preparatory projection is never eligible for publication.

## Generate and inspect without publishing

After review and merge to `main`, run the existing workflow with publication
disabled (the default). This uses the configured GitHub App reader on the
runner; no local source credential is required:

```sh
gh workflow run publish.yml --repo astraonelabs/packages --ref main -f publish=false
```

In Actions, select the resulting run and confirm its `head_sha` is the intended
integrated revision. Wait for `build` to succeed; `deploy` and `verify-consumer`
are skipped in this mode. Download that run's `github-pages` artifact before it
expires and unpack its catalog metadata into a new directory for inspection.
Record the run ID, SHA and metadata inventory. Follow every include and p2 path
announced by `packages.json`, verify advertised hashes and `/packages/` URLs,
and check the admitted package name, stable version, HTTPS source URL and
release commit reference against the real tag. Reject legacy identities,
credentials, source files or distribution archives. A successful validator
alone does not prove the exact expected source URL/reference or advertised
hashes. Source clones and `selection.json` are not in this artifact.

[Local generation](local-generation.md) remains an option when an authorized
reader is already available locally; it is not required for this GitHub path.
A successful generation-only run does not complete publication or consumer
verification.

## Publish after inspection

Before a separately authorized publication, recheck `main`, the real release
tag and its dereferenced commit, and relevant source changes against the
inspected run. Confirm the catalog configuration, scripts and pinned actions
are unchanged. If inputs changed materially, generate and inspect again first.
Then explicitly enable publication:

```sh
gh workflow run publish.yml --repo astraonelabs/packages --ref main -f publish=true
```

The second run **regenerates** the catalog; it does not promote the earlier
artifact or guarantee identical bytes. Pinned inputs and tag-based source
references support comparison, but remote tags and the release set can change
between runs. The publication run validates its new catalog before deployment.
The `publish` input controls deployment, not mandatory human approval: follow
the inspection procedure before selecting `true`. Dispatches from a branch
other than trusted `main` are refused in either mode.

Wait for `build`, `deploy` and `verify-consumer` to succeed at the intended SHA.
Inspect the catalog actually served by Pages, following its announced metadata
paths and hashes and checking name/version/source reference against the real
release. Record the run and deployed URL. A successful generation-only run or
an HTTP 200 response alone is not publication evidence.

The build uses `scripts/build-catalog.sh satis.json public`, the same entry point
used locally. It selects Git tags by their own manifests, produces real Satis
metadata and rejects missing releases, the old package identity, unexpected
packages and archive/source output. The workflow uploads only `public/`.
Source clones and selection inventories stay outside the upload directory.

Deployment targets GitHub Pages at `https://astraonelabs.github.io/packages/`.
The consumer job fetches the deployed `packages.json`, configures Composer
with the deployed URL and installs the admitted packages with authenticated
read-only source access. This deployed verification has not been run as part
of preparatory task 10; it requires an authorized later publication.

## Reader access and verification boundary

The reader-auth action scopes a token to current `astraonelabs` repository URLs
from `satis.json`. Confirm the GitHub App has reader access to those repositories
before dispatch; do not infer operational access from configuration alone.
The existing secret names are preserved in the
[credential inventory](credential-inventory.md).

Successful publication means deployed metadata and consumer verification pass.
It does not make private source public or transfer consumer authentication to
Packages. Do not paste credentials into workflow inputs, logs or documentation.
