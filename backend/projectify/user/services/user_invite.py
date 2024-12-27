# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""User invite services."""

from typing import Optional

from django.db import transaction
from django.utils.timezone import now

from projectify.user.models import User, UserInvite
from projectify.user.selectors.user import user_find_by_email
from projectify.workspace.models.const import TeamMemberRoles
from projectify.workspace.models.team_member_invite import TeamMemberInvite
from projectify.workspace.services.workspace import workspace_add_user


@transaction.atomic
def user_invite_create(*, email: str) -> Optional[UserInvite]:
    """Invite a user by email address."""
    user = user_find_by_email(email=email)
    if user:
        return None
    # TODO make this a selector
    invite_qs = UserInvite.objects.by_email(email).is_redeemed(False)
    if invite_qs.exists():
        return invite_qs.get()
    return UserInvite.objects.create(email=email)


@transaction.atomic
def user_invite_redeem(*, user_invite: UserInvite, user: User) -> None:
    """Redeem a UserInvite."""
    assert not user_invite.redeemed
    user_invite.redeemed = True
    user_invite.user = user
    user_invite.save()

    # Add user to workspaces for any outstanding invites
    qs = TeamMemberInvite.objects.filter(
        # This plausibly keeps us from redeeming the same invite twice
        user_invite__user=user,
        redeemed=False,
    )
    for invite in qs:
        workspace = invite.workspace
        workspace_add_user(
            workspace=workspace, user=user, role=TeamMemberRoles.OBSERVER
        )
        invite.redeemed = True
        invite.redeemed_when = now()
        invite.save()


@transaction.atomic
def user_invite_redeem_many(*, user: User) -> None:
    """Redeem all invites for a user."""
    invites = UserInvite.objects.is_redeemed(False).by_email(user.email)
    for invitation in invites.iterator():
        user_invite_redeem(user_invite=invitation, user=user)
