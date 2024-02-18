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
"""Workspace board services."""
from datetime import datetime
from typing import Optional

from django.utils.timezone import (
    now,
)

from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models import WorkspaceBoard
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.services.signals import (
    send_workspace_board_change_signal,
    send_workspace_change_signal,
)


# Create
# TODO atomic
def workspace_board_create(
    *,
    who: User,
    workspace: Workspace,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
) -> WorkspaceBoard:
    """Create a workspace board inside a given workspace."""
    validate_perm("workspace.create_workspace_board", who, workspace)
    workspace_board = workspace.workspaceboard_set.create(
        title=title,
        description=description,
        due_date=due_date,
    )
    send_workspace_change_signal(workspace_board)
    return workspace_board


# Update
# TODO atomic
def workspace_board_update(
    *,
    who: User,
    workspace_board: WorkspaceBoard,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
) -> WorkspaceBoard:
    """Update a workspace board."""
    validate_perm(
        "workspace.update_workspace_board", who, workspace_board.workspace
    )
    workspace_board.title = title
    workspace_board.description = description
    if due_date and due_date.tzinfo is None:
        raise ValueError(f"tzinfo must be specified, got {due_date}")
    workspace_board.due_date = due_date
    workspace_board.save()
    send_workspace_change_signal(workspace_board)
    send_workspace_board_change_signal(workspace_board)
    return workspace_board


# Delete
# TODO atomic
def workspace_board_delete(
    *,
    who: User,
    workspace_board: WorkspaceBoard,
) -> None:
    """Delete a workspace board."""
    validate_perm(
        "workspace.delete_workspace_board",
        who,
        workspace_board.workspace,
    )
    workspace_board.delete()
    send_workspace_change_signal(workspace_board)
    send_workspace_board_change_signal(workspace_board)


# RPC
# TODO atomic
def workspace_board_archive(
    *,
    who: User,
    workspace_board: WorkspaceBoard,
    archived: bool,
) -> WorkspaceBoard:
    """Archive a workspace board, or not."""
    validate_perm(
        "workspace.update_workspace_board",
        who,
        workspace_board.workspace,
    )
    if archived:
        workspace_board.archived = now()
    else:
        workspace_board.archived = None
    workspace_board.save()
    send_workspace_change_signal(workspace_board)
    send_workspace_board_change_signal(workspace_board)
    return workspace_board
