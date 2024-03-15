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
"""Test section services."""
import pytest

from projectify.workspace.models import WorkspaceBoard
from projectify.workspace.models.section import (
    Section,
)
from projectify.workspace.models.task import Task
from projectify.workspace.models.workspace_user import WorkspaceUser
from projectify.workspace.services.section import (
    section_delete,
    section_move,
)


@pytest.mark.django_db
def test_delete_non_empty_section(
    workspace_user: WorkspaceUser,
    section: Section,
    # Make sure there is a task
    task: Task,
) -> None:
    """Assert we can delete a non-empty section."""
    count = Section.objects.count()
    task_count = Task.objects.count()
    section_delete(
        section=section,
        who=workspace_user.user,
    )
    assert Section.objects.count() == count - 1
    assert Task.objects.count() == task_count - 1


@pytest.mark.django_db
def test_moving_section(
    workspace_board: WorkspaceBoard,
    section: Section,
    other_section: Section,
    other_other_section: Section,
    workspace_user: WorkspaceUser,
) -> None:
    """Test moving a section around."""
    assert list(workspace_board.section_set.all()) == [
        section,
        other_section,
        other_other_section,
    ]
    section_move(
        section=section,
        order=0,
        who=workspace_user.user,
    )
    assert list(workspace_board.section_set.all()) == [
        section,
        other_section,
        other_other_section,
    ]
    section_move(
        section=section,
        order=2,
        who=workspace_user.user,
    )
    assert list(workspace_board.section_set.all()) == [
        other_section,
        other_other_section,
        section,
    ]
    section_move(
        section=section,
        order=1,
        who=workspace_user.user,
    )
    assert list(workspace_board.section_set.all()) == [
        other_section,
        section,
        other_other_section,
    ]


@pytest.mark.django_db
def test_moving_empty_section(
    workspace_board: WorkspaceBoard,
    section: Section,
    workspace_user: WorkspaceUser,
) -> None:
    """Test moving when there are no other sections."""
    assert list(workspace_board.section_set.all()) == [
        section,
    ]
    section_move(
        section=section,
        order=1,
        who=workspace_user.user,
    )
    assert list(workspace_board.section_set.all()) == [
        section,
    ]
    assert section._order == 0
