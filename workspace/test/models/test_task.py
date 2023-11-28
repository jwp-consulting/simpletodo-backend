"""Test task model and manager."""
from django import (
    db,
)
from django.contrib.auth.models import (
    AbstractUser,
)

import pytest

from ... import (
    factory,
    models,
)


@pytest.mark.django_db
class TestTaskManager:
    """Test TaskManager."""

    def test_filter_by_workspace_board_section_pks(
        self,
        workspace_board_section: models.WorkspaceBoardSection,
        task: models.Task,
    ) -> None:
        """Test filter_by_workspace_board_section_pks."""
        qs = models.Task.objects.filter_by_workspace_board_section_pks(
            [workspace_board_section.pk],
        )
        assert list(qs) == [task]

    def test_filter_for_user_and_uuid(
        self,
        workspace: models.Workspace,
        task: models.Task,
        workspace_user: models.WorkspaceUser,
    ) -> None:
        """Test filter_for_user_and_uuid."""
        factory.WorkspaceUserFactory(
            workspace=workspace,
        )
        actual = models.Task.objects.filter_for_user_and_uuid(
            workspace_user.user,
            task.uuid,
        ).get()
        assert actual == task

    def test_duplicate_task(self, task: models.Task) -> None:
        """Test task duplication."""
        new_task = models.Task.objects.duplicate_task(task)
        assert new_task.workspace_board_section == task.workspace_board_section
        assert new_task.title == task.title
        assert new_task.description == task.description


@pytest.mark.django_db
class TestTask:
    """Test Task."""

    def test_factory(
        self,
        workspace_board_section: models.WorkspaceBoardSection,
        workspace_user: models.WorkspaceUser,
        task: models.Task,
        user: AbstractUser,
    ) -> None:
        """Test that workspace_board_section is assigned correctly."""
        assert task.workspace_board_section == workspace_board_section
        assert task.deadline is not None

    def test_assign_to(
        self,
        workspace: models.Workspace,
        task: models.Task,
        other_workspace_user: models.WorkspaceUser,
    ) -> None:
        """Test assigning to a different workspace's user."""
        task.assign_to(other_workspace_user)
        assert task.assignee == other_workspace_user

    def test_assign_then_delete_user(
        self, task: models.Task, workspace_user: models.WorkspaceUser
    ) -> None:
        """Assert that nothing happens to the task if the user is gone."""
        task.assign_to(workspace_user)
        workspace_user.user.delete()
        task.refresh_from_db()
        assert task.assignee is None

    def test_assign_outside_of_workspace(
        self,
        workspace: models.Workspace,
        task: models.Task,
        other_workspace_workspace_user: models.WorkspaceUser,
    ) -> None:
        """Test assigning to a different workspace's user."""
        # This time do not create a workspace_user
        with pytest.raises(models.WorkspaceUser.DoesNotExist):
            task.assign_to(other_workspace_workspace_user)

    def test_assign_none(
        self,
        workspace: models.Workspace,
        task: models.Task,
        workspace_user: models.WorkspaceUser,
    ) -> None:
        """Test assigning to no user."""
        task.assign_to(workspace_user)
        task.assign_to(None)
        task.refresh_from_db()
        assert task.assignee is None

    def test_assign_remove_workspace_user(
        self,
        user: AbstractUser,
        workspace: models.Workspace,
        workspace_user: models.WorkspaceUser,
        task: models.Task,
    ) -> None:
        """Test what happens if a workspace user is removed."""
        assert task.assignee == workspace_user
        workspace.remove_user(user)
        task.refresh_from_db()
        assert task.assignee is None

    def test_get_next_section(
        self, workspace_board: models.WorkspaceBoard, task: models.Task
    ) -> None:
        """Test getting the next section."""
        section = factory.WorkspaceBoardSectionFactory.create(
            workspace_board=workspace_board,
        )
        assert task.get_next_section() == section

    def test_get_next_section_no_next_section(
        self, workspace_board: models.WorkspaceBoard, task: models.Task
    ) -> None:
        """Test getting the next section when there is none."""
        with pytest.raises(models.WorkspaceBoardSection.DoesNotExist):
            task.get_next_section()

    def test_set_labels(
        self, workspace: models.Workspace, task: models.Task
    ) -> None:
        """Test setting labels."""
        assert task.labels.count() == 0
        a, b, c, d, e = factory.LabelFactory.create_batch(
            5,
            workspace=workspace,
        )
        task.set_labels([a, b])
        assert task.labels.count() == 2
        assert list(task.labels.values_list("id", flat=True)) == [a.id, b.id]
        task.set_labels([c, d, e])
        assert task.labels.count() == 3
        assert list(task.labels.values_list("id", flat=True)) == [
            c.id,
            d.id,
            e.id,
        ]
        task.set_labels([])
        assert task.labels.count() == 0
        assert list(task.labels.values_list("id", flat=True)) == []

        unrelated = factory.LabelFactory.create()
        task.set_labels([unrelated])
        assert task.labels.count() == 0
        assert list(task.labels.values_list("id", flat=True)) == []

    def test_add_label(self, task: models.Task, label: models.Label) -> None:
        """Test adding a label."""
        assert task.tasklabel_set.count() == 0
        task.add_label(label)
        assert task.tasklabel_set.count() == 1
        # This is idempotent
        task.add_label(label)
        assert task.tasklabel_set.count() == 1

    def test_remove_label(
        self, task: models.Task, label: models.Label
    ) -> None:
        """Test removing a label."""
        task.add_label(label)
        assert task.tasklabel_set.count() == 1
        task.remove_label(label)
        assert task.tasklabel_set.count() == 0
        # This is idempotent
        task.remove_label(label)
        assert task.tasklabel_set.count() == 0

    def test_task_number(
        self, task: models.Task, other_task: models.Task
    ) -> None:
        """Test unique task number."""
        other_task.refresh_from_db()
        task.refresh_from_db()
        assert other_task.number == task.number + 1
        task.workspace.refresh_from_db()
        assert task.workspace.highest_task_number == other_task.number

    def test_save(self, task: models.Task) -> None:
        """Test saving and assert number does not change."""
        num = task.number
        task.save()
        assert task.number == num

    def test_save_no_number(
        self, task: models.Task, workspace: models.Workspace
    ) -> None:
        """Test saving with no number."""
        with pytest.raises(db.InternalError):
            task.number = None  # type: ignore[assignment]
            task.save()
            workspace.refresh_from_db()

    def test_save_different_number(self, task: models.Task) -> None:
        """Test saving with different number."""
        with pytest.raises(db.InternalError):
            task.number = 154785787
            task.save()

    def test_task_workspace_pgtrigger(
        self, task: models.Task, other_workspace: models.Workspace
    ) -> None:
        """Test database trigger for wrong workspace assignment."""
        with pytest.raises(db.InternalError):
            task.workspace = other_workspace
            task.save()
