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
"""Test workspace user services."""
import pytest
from rest_framework.exceptions import PermissionDenied

from projectify.user.models import User
from projectify.workspace.models.const import WorkspaceUserRoles
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.workspace_user import WorkspaceUser
from projectify.workspace.services.workspace import workspace_add_user
from projectify.workspace.services.workspace_user import (
    workspace_user_delete,
    workspace_user_update,
)

pytestmark = pytest.mark.django_db


def test_workspace_user_update(workspace_user: WorkspaceUser) -> None:
    """Test updating a workspace user."""
    # First, we update ourselves
    workspace_user_update(
        who=workspace_user.user,
        workspace_user=workspace_user,
        role=WorkspaceUserRoles.OBSERVER,
    )
    # Now we have demoted ourselves and we can't do it again
    with pytest.raises(PermissionDenied):
        workspace_user_update(
            who=workspace_user.user,
            workspace_user=workspace_user,
            role=WorkspaceUserRoles.OWNER,
        )


def test_workspace_user_delete(
    workspace_user: WorkspaceUser,
    workspace: Workspace,
    unrelated_user: User,
) -> None:
    """Test deleting a workspace user after adding them."""
    count = workspace.users.count()
    new_workspace_user = workspace_add_user(
        workspace=workspace,
        # TODO perm check missing in workspace_add_user
        # E who=workspace_user.user,
        user=unrelated_user,
        role=WorkspaceUserRoles.OBSERVER,
    )
    assert workspace.users.count() == count + 1
    workspace_user_delete(
        workspace_user=new_workspace_user, who=workspace_user.user
    )
    assert workspace.users.count() == count
