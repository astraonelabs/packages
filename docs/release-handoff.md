# Release handoff

An Access Control release and a Packages publication are separate events.
Releasing the package never dispatches or deploys the catalog automatically.

1. Complete Access Control's package-native implementation and release checks.
2. Confirm authorized reader access to `astraonelabs/access-control`.
3. Review catalog admission and [local generation](local-generation.md).
4. Confirm the consumable new package version and Foundation constraint during
   task 11; historical old-named tags do not satisfy the new identity.
5. After reviewed integration, create a real stable package release through its
   own authorized lifecycle.
6. Obtain publication authorization and manually run [publish](publication.md).

Access Control owns its Composer name and release lifecycle. Packages owns
admission, tagged-manifest selection and catalog publication. Foundation owns
its consumer constraint, credentials and local overrides. See Foundation's
[release guide](https://github.com/astraonelabs/foundation/blob/main/docs/release-and-consumption.md)
and [E2E integration guide](https://github.com/astraonelabs/foundation/blob/main/docs/e2e.md).

The synthetic projection from the local check is preparation evidence only.
It must never be pushed, tagged in the source repository or uploaded to Pages.
