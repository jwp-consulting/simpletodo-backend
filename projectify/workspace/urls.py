# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
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
"""Workspace url patterns."""
from django.urls import (
    include,
    path,
)

from projectify.workspace.views.label import LabelCreate, LabelUpdateDelete
from projectify.workspace.views.workspace_board import (
    WorkspaceBoardArchive,
    WorkspaceBoardArchivedList,
    WorkspaceBoardCreate,
    WorkspaceBoardReadUpdateDelete,
)
from projectify.workspace.views.workspace_board_section import (
    WorkspaceBoardSectionCreate,
    WorkspaceBoardSectionMove,
    WorkspaceBoardSectionReadUpdateDelete,
)

from .views.task import (
    TaskCreate,
    TaskMoveAfterTask,
    TaskMoveToWorkspaceBoardSection,
    TaskRetrieveUpdateDelete,
)
from .views.workspace import (
    InviteUserToWorkspace,
    WorkspaceCreate,
    WorkspaceList,
    WorkspacePictureUploadView,
    WorkspaceReadUpdate,
)
from .views.workspace_user import (
    WorkspaceUserReadUpdateDelete,
)

app_name = "workspace"

workspace_patterns = (
    # Read + Update
    path(
        "<uuid:workspace_uuid>",
        WorkspaceReadUpdate.as_view(),
        name="read-update",
    ),
    # Archived workspace boards
    path(
        "<uuid:workspace_uuid>/archived-workspace-boards/",
        WorkspaceBoardArchivedList.as_view(),
        name="archived-workspace-boards",
    ),
)

workspace_user_patterns = (
    # Read + Update + Destroy
    path(
        "<uuid:workspace_user_uuid>",
        WorkspaceUserReadUpdateDelete.as_view(),
        name="read-update-delete",
    ),
)

workspace_board_patterns = (
    # Create
    path(
        "",
        WorkspaceBoardCreate.as_view(),
        name="create",
    ),
    # Read + Update + Delete
    path(
        "<uuid:workspace_board_uuid>",
        WorkspaceBoardReadUpdateDelete.as_view(),
        name="read-update-delete",
    ),
    # RPC
    path(
        "<uuid:workspace_board_uuid>/archive",
        WorkspaceBoardArchive.as_view(),
        name="archive",
    ),
)

workspace_board_section_patterns = (
    # Create
    path(
        "",
        WorkspaceBoardSectionCreate.as_view(),
        name="create",
    ),
    # Read + Update + Delete
    path(
        "<uuid:workspace_board_section_uuid>",
        WorkspaceBoardSectionReadUpdateDelete.as_view(),
        name="read-update-delete",
    ),
    # RPC
    path(
        "<uuid:workspace_board_section_uuid>/move",
        WorkspaceBoardSectionMove.as_view(),
        name="move",
    ),
)

task_patterns = (
    # Create
    path(
        "",
        TaskCreate.as_view(),
        name="create",
    ),
    # Read, Update, Delete
    path(
        "<uuid:task_uuid>",
        TaskRetrieveUpdateDelete.as_view(),
        name="read-update-delete",
    ),
    # RPC
    path(
        "<uuid:task_uuid>/move-to-workspace-board-section",
        TaskMoveToWorkspaceBoardSection.as_view(),
        name="move-to-workspace-board-section",
    ),
    path(
        "<uuid:task_uuid>/move-after-task",
        TaskMoveAfterTask.as_view(),
        name="move-after-task",
    ),
)

label_patterns = (
    # Create
    path(
        "",
        LabelCreate.as_view(),
        name="create",
    ),
    # Read
    # Update
    path(
        "<uuid:label_uuid>",
        LabelUpdateDelete.as_view(),
        name="update-delete",
    ),
    # Delete
)

# TODO Rename all views to use standard CRUD terminology
urlpatterns = (
    # Workspace
    path(
        "workspace/",
        include((workspace_patterns, "workspaces")),
    ),
    # TODO put the below paths into workspace_patterns as well
    # Create
    path(
        "workspaces/",
        WorkspaceCreate.as_view(),
        name="workspace-create",
    ),
    # Read
    path(
        "user/workspaces/",
        WorkspaceList.as_view(),
        name="workspace-list",
    ),
    # Update
    # Delete
    # RPC
    path(
        "workspace/<uuid:uuid>/picture-upload",
        WorkspacePictureUploadView.as_view(),
        name="workspace-picture-upload",
    ),
    path(
        "workspace/<uuid:uuid>/invite-user",
        InviteUserToWorkspace.as_view(),
        name="workspace-invite-user",
    ),
    # WorkspaceUser
    path(
        "workspace-user/",
        include((workspace_user_patterns, "workspace-users")),
    ),
    # WorkspaceBoard
    path(
        "workspace-board/",
        include((workspace_board_patterns, "workspace-boards")),
    ),
    # WorkspaceBoardSection
    path(
        "workspace-board-section/",
        include(
            (workspace_board_section_patterns, "workspace-board-sections")
        ),
    ),
    # Task
    path(
        "task/",
        include((task_patterns, "tasks")),
    ),
    # TODO put into task_patterns
    # Create
    # Label
    path("label/", include((label_patterns, "labels"))),
)
