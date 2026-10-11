# Delivery

## Repository and branch

Code is delivered through `Masterix-Sistemas/composer-registry`. `main` is the default integration branch. Start a short-lived branch from current `origin/main`; current history uses conventional prefixes such as `fix/` and `feature/mas-<number>-<description>`. Keep the Linear MAS identifier in the branch or pull-request description.

## Pull request and validation

PR titles and descriptions must be in English.

Open one squash-merge pull request to `main` for an implementation ticket. Validate the changed workflow, action, documentation, or `satis.json` contract locally where possible. The repository has no pull-request GitHub Actions workflow; the `publish` workflow runs only by manual dispatch. The GitHub connector can inspect this public repository; use local Git plus structured GitHub tools or `gh` for pull requests and workflow status.

Do not treat the lack of a PR workflow as permission to skip review or validation. Repository-content CI or review fixes return to `/implement` for renewed validation and code review.

## Merge, publication, and tracker lifecycle

Move the Linear ticket to `In Progress` when work starts and to `In Review` only after its pull request exists. An authorized maintainer squash-merges after the applicable checks and review are complete. Documentation-only or workflow-maintenance work completes when the pull request is merged and GitHub confirms it.

For work that changes the catalog, its allowlist, or publication behavior, run the manual `publish` workflow after the merge. The terminal delivery event is a successful `build`, `deploy` to GitHub Pages, and `verify-consumer` run for the merged revision. Only then move the linked Linear ticket to `Done`. A failed or unavailable publish run leaves the ticket non-terminal and is handled as a delivery blocker.
