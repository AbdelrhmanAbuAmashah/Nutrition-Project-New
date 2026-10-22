# Feature branches and protected main

Effective from the owner's workflow instruction on 22 October 2026. The existing verified foundation is the starting baseline. Every new milestone, including this workflow setup, is developed on a separate branch and delivered through a PR.

## Delivery sequence

1. Start with a clean working tree and fetch `origin/main`. Create a descriptive feature branch from that revision; preserve other work rather than resetting it.
2. Implement one reviewable milestone. Update its TODOs, evidence and remaining limits in the progress report on the same branch.
3. Run local verification before publishing. For the full stack, use `bash scripts/setup.sh`, then `bash scripts/test.sh`. Review the relevant API/UI behavior and resulting diff. Never present an earlier revision's checks as current evidence.
4. Push only the feature branch and open a PR targeting `main`. Include the problem/result, scope, exact test results and any migration/configuration considerations. The repository provides a PR template.
5. GitHub runs the `Application checks` workflow on every PR to `main`, including documentation-only PRs. Its required job is `verify`, provided by GitHub Actions. It builds the production app, applies/checks migrations, runs lint and the PostgreSQL/API and bilingual browser checks.
6. Before merging, require successful checks for the current revision, an up-to-date branch and resolved review conversations. If `main` advanced, merge the latest `origin/main` into the feature branch, resolve any conflicts there, rerun affected local checks, push and wait for fresh CI. Do not force-push `main` or use an administrator bypass.
7. Use the normal GitHub squash merge once all requirements pass and merging is authorized. Verify the merged revision and post-merge CI, then use a new feature branch for the next milestone. Branch cleanup is optional and follows successful merge verification.

Example start and publication, after local verification:

```bash
git fetch origin main
git switch --no-track --create feature/clinical-review-queue origin/main
# Implement, review the diff and run local checks before the following commands.
git add <explicit-files>
git commit -m "feat: add clinical review queue"
git push --set-upstream origin feature/clinical-review-queue
gh pr create --base main --head feature/clinical-review-queue --title "Add clinical review queue" --body-file /tmp/nutrition-pr.md
```

The PR body file must contain actual newlines and the exact reviewable description. Never include secrets or real patient information. Milestone completion records should distinguish implemented, locally verified, PR checks passed and merged states.

## Main branch protection policy

- PRs required; direct changes to `main` prohibited, including for administrators.
- Required check `verify` must come from the GitHub Actions app that supplies the project's checks.
- Strict status checking: the feature branch must be current with `main`.
- Review conversations must be resolved; stale approvals are dismissed on new code.
- Force pushes and deletion of `main` are blocked.
- Linear history required; squash merging is the default delivery method.
- Solo-developer mode: zero independent approving reviews required. This does not mean peer review occurred. Add an approval requirement when another code reviewer is assigned.

Branch protection is GitHub repository configuration, not something enforced by a Markdown file. Its actual applied state and this setup PR/checkpoint are recorded in the progress report. Existing stronger rules must be preserved.

The reviewed API payload is versioned in [main-branch-protection.json](../.github/main-branch-protection.json). GitHub Actions app ID `15368` was read from this repository's successful `verify` check. Applying this file is a separate, authorized repository-administration operation; normal application setup does not change GitHub settings. Inspect existing protections/rulesets first and preserve any stronger policy rather than blindly replaying the payload.

## CI behavior

CI runs for PRs to `main` and for updates to `main` after merges. Feature-branch publication is followed by PR creation, which triggers pre-merge verification. Duplicate push/PR builds for each feature commit are avoided. New pushes cancel obsolete runs for the same PR; post-merge checks are not canceled by later PR activity.

There are no path exclusions on the required workflow. Do not add a CI-skip marker to a commit that must pass the merge gate. GitHub documents that skipping a required workflow can leave its status pending and block merging: [required-check troubleshooting](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks).

The [branch-protection documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) describes strict checks, administrator enforcement and linear history. Repository administrators can change GitHub settings, so retaining these protections remains an operational responsibility.
