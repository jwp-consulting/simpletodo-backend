# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test team member services."""

import pytest
from rest_framework.exceptions import PermissionDenied

from projectify.user.models import User
from projectify.workspace.models.const import TeamMemberRoles
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.services.team_member import (
    team_member_delete,
    team_member_update,
)
from projectify.workspace.services.workspace import workspace_add_user

pytestmark = pytest.mark.django_db


def test_team_member_update(team_member: TeamMember) -> None:
    """Test updating a team member."""
    # First, we update ourselves
    team_member_update(
        who=team_member.user,
        team_member=team_member,
        role=TeamMemberRoles.OBSERVER,
    )
    # Now we have demoted ourselves and we can't do it again
    with pytest.raises(PermissionDenied):
        team_member_update(
            who=team_member.user,
            team_member=team_member,
            role=TeamMemberRoles.OWNER,
        )


def test_team_member_delete(
    team_member: TeamMember,
    workspace: Workspace,
    unrelated_user: User,
) -> None:
    """Test deleting a team member after adding them."""
    count = workspace.users.count()
    new_team_member = workspace_add_user(
        workspace=workspace,
        # TODO perm check missing in workspace_add_user
        # E who=team_member.user,
        user=unrelated_user,
        role=TeamMemberRoles.OBSERVER,
    )
    assert workspace.users.count() == count + 1
    team_member_delete(team_member=new_team_member, who=team_member.user)
    assert workspace.users.count() == count
