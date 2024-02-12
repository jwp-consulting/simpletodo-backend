# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2022, 2023 JWP Consulting GK
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
"""Test workspace models."""
import pytest

from projectify.workspace.models.workspace_user import WorkspaceUser
from projectify.workspace.services.sub_task import sub_task_create

from .. import (
    models,
)


# TODO extract into workspace/test/models/test_label.py
@pytest.mark.django_db
class TestLabelManager:
    """Test Label queryset/manager."""

    def test_filter_by_workspace_pks(
        self, label: models.Label, workspace: models.Workspace
    ) -> None:
        """Test filter_by_workspace_pks."""
        qs = models.Label.objects.filter_by_workspace_pks([workspace.pk])
        labels = [label]
        assert list(qs) == labels

    def test_filter_for_user_and_uuid(
        self, label: models.Label, workspace_user: models.WorkspaceUser
    ) -> None:
        """Test filter_for_user_and_uuid."""
        assert (
            models.Label.objects.filter_for_user_and_uuid(
                workspace_user.user,
                label.uuid,
            ).get()
            == label
        )


# TODO extract into workspace/test/models/test_label.py
@pytest.mark.django_db
class TestLabel:
    """Test Label model."""

    def test_factory(self, label: models.Label) -> None:
        """Test factory."""
        assert label.color is not None


# TODO extract into workspace/test/models/test_sub_task.py
@pytest.mark.django_db
class TestSubTaskManager:
    """Test SubTask manager."""

    def test_filter_by_task_pks(
        self, task: models.Task, sub_task: models.SubTask
    ) -> None:
        """Test filter_by_task_pks."""
        qs = models.SubTask.objects.filter_by_task_pks([task.pk])
        assert list(qs) == [sub_task]

    def test_filter_for_user_and_uuid(
        self, sub_task: models.SubTask, workspace_user: models.WorkspaceUser
    ) -> None:
        """Test filter_for_user_and_uuid."""
        assert (
            models.SubTask.objects.filter_for_user_and_uuid(
                workspace_user.user,
                sub_task.uuid,
            ).get()
            == sub_task
        )


# TODO extract into workspace/test/models/test_sub_task.py
@pytest.mark.django_db
class TestSubTask:
    """Test SubTask."""

    def test_factory(
        self, task: models.Task, sub_task: models.SubTask
    ) -> None:
        """Test that sub task correctly belongs to task."""
        assert sub_task.task == task

    def test_moving_sub_task(
        self,
        task: models.Task,
        sub_task: models.SubTask,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test moving a sub task around."""
        other_sub_task = sub_task_create(
            task=task,
            who=workspace_user.user,
            title="don't care",
            done=False,
        )
        other_other_sub_task = sub_task_create(
            task=task,
            who=workspace_user.user,
            title="don't care",
            done=False,
        )
        assert list(task.subtask_set.all()) == [
            sub_task,
            other_sub_task,
            other_other_sub_task,
        ]
        sub_task.move_to(0)
        assert list(task.subtask_set.all()) == [
            sub_task,
            other_sub_task,
            other_other_sub_task,
        ]
        sub_task.move_to(2)
        assert list(task.subtask_set.all()) == [
            other_sub_task,
            other_other_sub_task,
            sub_task,
        ]
        sub_task.move_to(1)
        assert list(task.subtask_set.all()) == [
            other_sub_task,
            sub_task,
            other_other_sub_task,
        ]

    def test_moving_within_empty_task(
        self,
        task: models.Task,
        sub_task: models.SubTask,
    ) -> None:
        """Test moving when there are no other sub tasks."""
        assert list(task.subtask_set.all()) == [
            sub_task,
        ]
        sub_task.move_to(1)
        assert list(task.subtask_set.all()) == [
            sub_task,
        ]
        assert sub_task._order == 0


# TODO extract into workspace/test/models/test_chat_message.py
@pytest.mark.django_db
class TestChatMessageManager:
    """Test ChatMessage Manager."""

    def test_filter_by_task_pks(
        self, chat_message: models.ChatMessage, task: models.Task
    ) -> None:
        """Test filter_by_task_pks."""
        qs = models.ChatMessage.objects.filter_by_task_pks([task.pk])
        assert list(qs) == [chat_message]

    def test_filter_for_user_and_uuid(
        self,
        chat_message: models.ChatMessage,
        workspace_user: models.WorkspaceUser,
    ) -> None:
        """Test filter_for_user_and_uuid."""
        assert (
            models.ChatMessage.objects.filter_for_user_and_uuid(
                workspace_user.user,
                chat_message.uuid,
            ).get()
            == chat_message
        )


# TODO extract into workspace/test/models/test_chat_message.py
@pytest.mark.django_db
class TestChatMessage:
    """Test ChatMessage."""

    def test_factory(
        self,
        workspace_user: models.WorkspaceUser,
        chat_message: models.ChatMessage,
    ) -> None:
        """Test that chat message belongs to user."""
        assert chat_message.author == workspace_user
