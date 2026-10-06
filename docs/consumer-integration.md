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

The intended package name is `astraone/access-control`. Its first consumable
release and the Foundation constraint are confirmed in task 11. No existing
old-named tag or preparatory projection is a consumable release of this contract.
The public updated catalog and installation from it remain unverified until
an authorized publication.

Foundation owns its tracked dependency selection and ignored local path
integration. Follow the [Foundation E2E guide](https://github.com/astraonelabs/foundation/blob/main/docs/e2e.md)
for the task 01 setup. That setup temporarily uses the independent package's
actual current name; task 02 owns the runtime rename. Local paths, `@dev`
constraints, mounts and credentials remain ignored Foundation overrides.

For a metadata-generation check before a new release, follow
[local generation](local-generation.md). Its temporary projection cannot replace
an integrated installation and does not belong in a consumer manifest.
