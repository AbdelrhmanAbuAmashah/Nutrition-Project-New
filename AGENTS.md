# Repository workflow

- Active origin: `AbdelrhmanAbuAmashah/Nutrition-Project-New`, the only remaining GitHub repository for this project. The owner explicitly requested a clean history attributed only to `AbdelrhmanAbuAmashah` and deletion of the two older repositories. Prior Git metadata remains in an ignored local backup; do not import its branches into the active history. See `docs/repository-cleanup.md`.
- Before committing, verify both `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` resolve to `AbdelrhmanAbuAmashah <118768074+AbdelrhmanAbuAmashah@users.noreply.github.com>`. Use repository-local identity settings and do not inherit another account's global Git identity.
- Keep `main` stable. Create one dedicated feature branch per milestone from the latest `origin/main`, for example `feature/bilingual-core-setup` or `feature/clinical-review-queue`. Use `fix/` or `chore/` for narrowly scoped fixes or maintenance. Preserve existing uncommitted work when changing branches.
- Never commit or push working changes directly to `main`. Publish only the feature branch and create a PR targeting `main`. Do not rewrite published history, force-push `main`, use an administrator merge bypass, or weaken branch protections to complete a task.
- Verify relevant code, APIs and UI locally before pushing. For a full-stack milestone, run `bash scripts/setup.sh` and `bash scripts/test.sh`; the build checks formatting/TypeScript and the suite checks migrations, backend behavior and both languages at desktop/mobile sizes. Record actual results and any unavailable checks.
- Include the concrete change, milestone reference, test commands/results and material limitations in the PR. Update the progress report through that same feature branch/PR; documentation changes also require CI.
- Merge only when merging is within the authorized task scope and all checks pass for the current PR revision, the branch is up to date with `main`, and review conversations are resolved. Use GitHub's normal protected merge path; prefer squash merging for one milestone per main-branch commit. A later push or base update requires fresh checks.
- The project currently has one developer. A PR and successful automated checks are required; an independent approval is not claimed or required until a second code reviewer is assigned.
- Keep secrets, local test artifacts, backups and real health records outside Git.

<!-- CODEGRAPH_START -->
## CodeGraph

In repositories indexed by CodeGraph (a `.codegraph/` directory exists at the repo root), reach for it BEFORE grep/find or reading files when you need to understand or locate code:

- **MCP tool** (when available): `codegraph_explore` answers most code questions in one call — the relevant symbols' verbatim source plus the call paths between them, including dynamic-dispatch hops grep can't follow. Name a file or symbol in the query to read its current line-numbered source. If it's listed but deferred, load it by name via tool search.
- **Shell** (always works): `codegraph explore "<symbol names or question>"` prints the same output.

If there is no `.codegraph/` directory, skip CodeGraph entirely — indexing is the user's decision.
<!-- CODEGRAPH_END -->
