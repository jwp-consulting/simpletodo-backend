# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Test team member selectors."""
import pytest

from projectify.user.models import User
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.selectors.team_member import (
    team_member_find_for_workspace,
)


@pytest.mark.django_db
def test_team_member_find_for_workspace(
    workspace: Workspace,
    user: User,
    team_member: TeamMember,
) -> None:
    """Test get_by_workspace_and_user."""
    assert (
        team_member_find_for_workspace(
            workspace=workspace,
            user=user,
        )
        == team_member
    )
