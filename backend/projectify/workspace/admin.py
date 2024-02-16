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
"""Workspace admin."""
from django.contrib import (
    admin,
)
from django.utils.translation import gettext_lazy as _

from . import (
    models,
)


class WorkspaceUserInline(admin.TabularInline[models.WorkspaceUser]):
    """WorkspaceUser Inline."""

    model = models.WorkspaceUser
    extra = 0


class WorkspaceBoardInline(admin.TabularInline[models.WorkspaceBoard]):
    """WorkspaceBoard Inline."""

    model = models.WorkspaceBoard
    extra = 0


@admin.register(models.Workspace)
class WorkspaceAdmin(admin.ModelAdmin[models.Workspace]):
    """Workspace Admin."""

    inlines = (WorkspaceUserInline, WorkspaceBoardInline)
    list_display = (
        "title",
        "description",
        "created",
        "modified",
    )
    readonly_fields = ("uuid",)


@admin.register(models.WorkspaceUserInvite)
class WorkspaceUserInviteAdmin(admin.ModelAdmin[models.WorkspaceUserInvite]):
    """Workspace user invite admin."""

    list_display = ("workspace_title",)
    list_select_related = ("workspace",)

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.WorkspaceUserInvite) -> str:
        """Return the workspace's title."""
        return instance.workspace.title


@admin.register(models.WorkspaceUser)
class WorkspaceUserAdmin(admin.ModelAdmin[models.WorkspaceUser]):
    """WorkspaceUser Admin."""

    list_display = (
        "workspace_title",
        "user_email",
        "created",
        "modified",
    )
    list_select_related = (
        "workspace",
        "user",
    )
    search_fields = (
        "workspace__title",
        "user__email",
        "user__preferred_name",
    )
    search_help_text = _(
        "You can seach by workspace title, user email and preferred name"
    )

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.WorkspaceUser) -> str:
        """Return the workspace's title."""
        return instance.workspace.title

    @admin.display(description=_("User email"))
    def user_email(self, instance: models.WorkspaceUser) -> str:
        """Return the workspace's title."""
        return instance.user.email


class WorkspaceBoardSectionInline(
    admin.TabularInline[models.WorkspaceBoardSection]
):
    """WorkspaceBoardSection inline admin."""

    model = models.WorkspaceBoardSection
    extra = 0


@admin.register(models.WorkspaceBoard)
class WorkspaceBoardAdmin(admin.ModelAdmin[models.WorkspaceBoard]):
    """WorkspaceBoard Admin."""

    inlines = (WorkspaceBoardSectionInline,)
    list_display = (
        "title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = ("workspace",)
    readonly_fields = ("uuid",)

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.WorkspaceBoard) -> str:
        """Return the workspace's title."""
        return instance.workspace.title


class TaskInline(admin.TabularInline[models.Task]):
    """Task inline admin."""

    model = models.Task
    extra = 0
    readonly_fields = ("assignee",)


@admin.register(models.WorkspaceBoardSection)
class WorkspaceBoardSectionAdmin(
    admin.ModelAdmin[models.WorkspaceBoardSection]
):
    """WorkspaceBoardSection Admin."""

    inlines = (TaskInline,)
    list_display = (
        "title",
        "workspace_board_title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = ("workspace_board__workspace",)
    readonly_fields = ("uuid",)

    @admin.display(description=_("Workspace board title"))
    def workspace_board_title(
        self, instance: models.WorkspaceBoardSection
    ) -> str:
        """Return the workspace board's title."""
        return instance.workspace_board.title

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.WorkspaceBoardSection) -> str:
        """Return the workspace's title."""
        return instance.workspace_board.workspace.title


class SubTaskInline(admin.TabularInline[models.SubTask]):
    """SubTask inline admin."""

    model = models.SubTask
    extra = 0


class TaskLabelInline(admin.TabularInline[models.TaskLabel]):
    """TaskLabel inline admin."""

    model = models.TaskLabel
    extra = 0


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin[models.Task]):
    """Task Admin."""

    inlines = (SubTaskInline, TaskLabelInline)
    list_display = (
        "title",
        "workspace_board_section_title",
        "workspace_board_title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = (
        "workspace_board_section__workspace_board__workspace",
    )
    readonly_fields = ("uuid", "assignee")

    @admin.display(description=_("Workspace board section title"))
    def workspace_board_section_title(self, instance: models.Task) -> str:
        """Return the workspace board's title."""
        return instance.workspace_board_section.title

    @admin.display(description=_("Workspace board title"))
    def workspace_board_title(self, instance: models.Task) -> str:
        """Return the workspace board's title."""
        return instance.workspace_board_section.workspace_board.title

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.Task) -> str:
        """Return the workspace's title."""
        return instance.workspace_board_section.workspace_board.workspace.title


@admin.register(models.Label)
class LabelAdmin(admin.ModelAdmin[models.Label]):
    """Label admin."""

    list_display = (
        "name",
        "color",
        "workspace_title",
    )
    list_select_related = ("workspace",)
    readonly_fields = ("uuid",)

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.Label) -> str:
        """Return the workspace's title."""
        return instance.workspace.title


@admin.register(models.SubTask)
class SubTaskAdmin(admin.ModelAdmin[models.SubTask]):
    """SubTask Admin."""

    list_display = (
        "title",
        "task_title",
        "workspace_board_section_title",
        "workspace_board_title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = (
        "task__workspace_board_section__workspace_board__workspace",
    )
    readonly_fields = ("uuid",)

    @admin.display(description=_("Task title"))
    def task_title(self, instance: models.SubTask) -> str:
        """Return the task's title."""
        return instance.task.title

    @admin.display(description=_("Workspace board section title"))
    def workspace_board_section_title(self, instance: models.SubTask) -> str:
        """Return the workspace board's title."""
        return instance.task.workspace_board_section.title

    @admin.display(description=_("Workspace board title"))
    def workspace_board_title(self, instance: models.SubTask) -> str:
        """Return the workspace board's title."""
        return instance.task.workspace_board_section.workspace_board.title

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.SubTask) -> str:
        """Return the workspace's title."""
        workspace_board = instance.task.workspace_board_section.workspace_board
        return workspace_board.workspace.title


@admin.register(models.ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin[models.ChatMessage]):
    """ChatMessage admin."""

    list_display = (
        "task_title",
        "workspace_board_section_title",
        "workspace_board_title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = (
        "task__workspace_board_section__workspace_board__workspace",
    )
    readonly_fields = ("uuid", "author")

    @admin.display(description=_("Task title"))
    def task_title(self, instance: models.ChatMessage) -> str:
        """Return the task's title."""
        return instance.task.title

    @admin.display(description=_("Workspace board section title"))
    def workspace_board_section_title(
        self, instance: models.ChatMessage
    ) -> str:
        """Return the workspace board's title."""
        return instance.task.workspace_board_section.title

    @admin.display(description=_("Workspace board title"))
    def workspace_board_title(self, instance: models.ChatMessage) -> str:
        """Return the workspace board's title."""
        return instance.task.workspace_board_section.workspace_board.title

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.ChatMessage) -> str:
        """Return the workspace's title."""
        workspace_board = instance.task.workspace_board_section.workspace_board
        return workspace_board.workspace.title
