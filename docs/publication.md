# Manual publication

Local generation and publication are separate operations. A plugin release
never dispatches the Packages workflow automatically. First validate the
[local generation](local-generation.md), review admission and confirm a real
stable `astraone/access-control` release with the integrated package. A
preparatory projection is never eligible for publication.

## Run the workflow

After review, merge and a separately authorized publication:

1. Open **Actions** in `astraonelabs/packages`.
2. Select the [`publish` workflow](../.github/workflows/publish.yml).
3. Choose **Run workflow** for the intended revision (`workflow_dispatch`).
4. Wait for `build`, `deploy` and `verify-consumer` to succeed.

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
