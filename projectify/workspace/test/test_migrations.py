# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022 JWP Consulting GK
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
"""Test migrations in workspace app."""
import pytest


@pytest.mark.django_db
class Test0043:
    """Test migration 0043."""

    def test(self, migrator, settings):
        """Test that assignee_workspace_user is populated correctly."""
        old_state = migrator.apply_initial_migration(
            ("workspace", "0042_task_assignee_workspace_user")
        )
        Workspace = old_state.apps.get_model("workspace", "Workspace")
        WorkspaceBoard = old_state.apps.get_model(
            "workspace", "WorkspaceBoard"
        )
        WorkspaceBoardSection = old_state.apps.get_model(
            "workspace", "WorkspaceBoardSection"
        )
        Task = old_state.apps.get_model("workspace", "Task")
        WorkspaceUser = old_state.apps.get_model("workspace", "WorkspaceUser")
        User = old_state.apps.get_model(settings.AUTH_USER_MODEL)
        workspace = Workspace.objects.create(
            title="",
            description="",
        )
        workspace_board = WorkspaceBoard.objects.create(
            title="",
            description="",
            workspace=workspace,
        )
        workspace_board_section = WorkspaceBoardSection.objects.create(
            title="",
            description="",
            workspace_board=workspace_board,
        )
        user = User.objects.create(
            email="hello@example.com",
            is_staff=False,
            is_superuser=False,
            is_active=False,
        )
        WorkspaceUser.objects.create(
            user=user,
            workspace=workspace,
        )
        task = Task.objects.create(
            title="",
            description="",
            workspace_board_section=workspace_board_section,
            workspace=workspace,
            assignee=user,
            number=1,
        )

        # Create a task with user, but no workspace user
        other_user = User.objects.create(
            email="goodbye@example.com",
            is_staff=False,
            is_superuser=False,
            is_active=False,
        )
        other_task = Task.objects.create(
            title="",
            description="",
            workspace_board_section=workspace_board_section,
            workspace=workspace,
            assignee=other_user,
            number=2,
        )

        new_state = migrator.apply_tested_migration(
            ("workspace", "0043_auto_20220629_0742")
        )
        Task = new_state.apps.get_model("workspace", "Task")
        task = Task.objects.get(pk=task.pk)
        other_task = Task.objects.get(pk=other_task.pk)
        assert task.assignee_workspace_user is not None
        assert task.assignee_workspace_user.user == task.assignee
        assert other_task.assignee_workspace_user is None


@pytest.mark.django_db
class Test0047PopulateChatMessageAuthorWorkspaceUser:
    """Test migration 0047."""

    def test(self, migrator, settings):
        """Test that author_workspace_user is populated correctly."""
        old_state = migrator.apply_initial_migration(
            ("workspace", "0046_chatmessage_author_workspace_user")
        )
        Workspace = old_state.apps.get_model("workspace", "Workspace")
        WorkspaceBoard = old_state.apps.get_model(
            "workspace", "WorkspaceBoard"
        )
        WorkspaceBoardSection = old_state.apps.get_model(
            "workspace", "WorkspaceBoardSection"
        )
        Task = old_state.apps.get_model("workspace", "Task")
        WorkspaceUser = old_state.apps.get_model("workspace", "WorkspaceUser")
        User = old_state.apps.get_model(settings.AUTH_USER_MODEL)
        ChatMessage = old_state.apps.get_model("workspace", "ChatMessage")
        workspace = Workspace.objects.create(
            title="",
            description="",
        )
        workspace_board = WorkspaceBoard.objects.create(
            title="",
            description="",
            workspace=workspace,
        )
        workspace_board_section = WorkspaceBoardSection.objects.create(
            title="",
            description="",
            workspace_board=workspace_board,
        )
        user = User.objects.create(
            email="hello@example.com",
            is_staff=False,
            is_superuser=False,
            is_active=False,
        )
        WorkspaceUser.objects.create(
            user=user,
            workspace=workspace,
        )
        task = Task.objects.create(
            title="",
            description="",
            workspace_board_section=workspace_board_section,
            workspace=workspace,
            number=1,
        )
        chat_message = ChatMessage.objects.create(
            text="",
            task=task,
            author=user,
        )

        # Create a chat message with user, but no workspace user
        other_user = User.objects.create(
            email="goodbye@example.com",
            is_staff=False,
            is_superuser=False,
            is_active=False,
        )
        other_chat_message = ChatMessage.objects.create(
            text="",
            task=task,
            author=other_user,
        )

        new_state = migrator.apply_tested_migration(
            ("workspace", "0047_populate_chatmessage_author_workspace_user")
        )
        ChatMessage = new_state.apps.get_model("workspace", "ChatMessage")
        chat_message = ChatMessage.objects.get(pk=chat_message.pk)
        other_chat_message = ChatMessage.objects.get(pk=other_chat_message.pk)
        assert chat_message.author_workspace_user is not None
        assert chat_message.author_workspace_user.user == chat_message.author
        assert other_chat_message.author_workspace_user is None
