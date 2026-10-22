"""Publication guard for future clinical routes. No AI/provider or publishing endpoint is enabled."""

from app.models import ClinicalApproval, ClinicalDraft, Profile


def approval_allows_publication(
    draft: ClinicalDraft, approval: ClinicalApproval | None, profile: Profile
) -> bool:
    return bool(
        approval
        and draft.checks_passed
        and draft.status == "approved"
        and approval.decision == "approved"
        and approval.reviewer_id is not None
        and approval.draft_id == draft.id
        and approval.draft_version == draft.version
        and approval.content_hash == draft.content_hash
        and approval.profile_revision == draft.profile_revision == profile.revision
    )
