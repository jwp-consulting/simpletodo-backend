# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test section services."""

import pytest

from projectify.workspace.models import Project
from projectify.workspace.models.section import (
    Section,
)
from projectify.workspace.models.task import Task
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.services.section import (
    section_delete,
    section_move,
)


@pytest.mark.django_db
def test_delete_non_empty_section(
    team_member: TeamMember,
    section: Section,
    # Make sure there is a task
    task: Task,
) -> None:
    """Assert we can delete a non-empty section."""
    count = Section.objects.count()
    task_count = Task.objects.count()
    section_delete(
        section=section,
        who=team_member.user,
    )
    assert Section.objects.count() == count - 1
    assert Task.objects.count() == task_count - 1


@pytest.mark.django_db
def test_moving_section(
    project: Project,
    section: Section,
    other_section: Section,
    other_other_section: Section,
    team_member: TeamMember,
) -> None:
    """Test moving a section around."""
    assert list(project.section_set.all()) == [
        section,
        other_section,
        other_other_section,
    ]
    section_move(
        section=section,
        order=0,
        who=team_member.user,
    )
    assert list(project.section_set.all()) == [
        section,
        other_section,
        other_other_section,
    ]
    section_move(
        section=section,
        order=2,
        who=team_member.user,
    )
    assert list(project.section_set.all()) == [
        other_section,
        other_other_section,
        section,
    ]
    section_move(
        section=section,
        order=1,
        who=team_member.user,
    )
    assert list(project.section_set.all()) == [
        other_section,
        section,
        other_other_section,
    ]


@pytest.mark.django_db
def test_moving_empty_section(
    project: Project,
    section: Section,
    team_member: TeamMember,
) -> None:
    """Test moving when there are no other sections."""
    assert list(project.section_set.all()) == [
        section,
    ]
    section_move(
        section=section,
        order=1,
        who=team_member.user,
    )
    assert list(project.section_set.all()) == [
        section,
    ]
    assert section._order == 0
