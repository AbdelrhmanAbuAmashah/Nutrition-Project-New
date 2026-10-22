# Repository cleanup record

Verified 22 October 2026 at 08:34 Asia/Amman (05:34 UTC), authenticated as `AbdelrhmanAbuAmashah`. The owner explicitly authorized deleting older copies of this nutrition project. The account inventory contained six owned repositories: three for this project and three unrelated repositories.

| Repository | GitHub repository ID | Result |
| --- | --- | --- |
| `AbdelrhmanAbuAmashah/Nutrition-project` | `1429079145` | Deleted: API returned HTTP 204; authenticated follow-up returned HTTP 404. |
| `AbdelrhmanAbuAmashah/Nutrition-Project-New-history-backup` | `1429243261` | Deleted: API returned HTTP 204; authenticated follow-up returned HTTP 404. |
| [AbdelrhmanAbuAmashah/Nutrition-Project-New](https://github.com/AbdelrhmanAbuAmashah/Nutrition-Project-New) | `1429261171` | Preserved and verified as the only remaining repository for this project. |

- [x] Enumerate all owned repositories, including private repositories, with pagination.
- [x] Verify the owner account, administrative access and exact repository IDs before deletion.
- [x] Verify both old default branches' commit `5503900dface65ae564d37c5f842581cac704442` exists in the local Git backup before deletion.
- [x] Confirm fetch and push origin both equal `https://github.com/AbdelrhmanAbuAmashah/Nutrition-Project-New.git`.
- [x] Confirm active main and local HEAD match `68ac7d0850521f63fc38273a8c36bcaccfbeebd7` before cleanup documentation.
- [x] Delete only the two identified older project repositories and verify each is absent.
- [x] Re-enumerate the account: four repositories remain, including all three unrelated repositories with their original IDs.
- [x] Verify the active repository's contributor list contains only `AbdelrhmanAbuAmashah` and main still enforces administrator-inclusive PR and strict `verify` checks.

The name remains `Nutrition-Project-New`; the optional rename to `Nour` was not requested. No application source, database records, environment files or secrets were changed by cleanup. The product milestone count remains one, with foundation tasks N1–N7 complete (7/7).

Prior Git metadata remains locally at `local-data/backups/git-before-owner-only-cdg_zy4o/previous.git`, excluded from Git. For example, `git --git-dir=local-data/backups/git-before-owner-only-cdg_zy4o/previous.git log --oneline -5` reads that history without importing it. This backup preserves Git history; it does not preserve GitHub-hosted PR conversations, Actions logs, issues or repository settings. Legacy checkpoint/run numbers elsewhere in the report are historical observations, not live hosted evidence. Current validation is linked in [verification](verification.md).

This record and the related progress updates use `chore/repository-cleanup-report` and the normal protected PR workflow. Deletion itself was an explicitly authorized repository administration operation.
