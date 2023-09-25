"""Workspace test fixtures."""
from datetime import (
    datetime,
)
from typing import (
    TYPE_CHECKING,
    Type,
    cast,
)

from django.contrib import (
    auth,
)
from django.utils import (
    timezone,
)

import pytest

from corporate.factory import (
    CustomerFactory,
)
from user import models as user_models

from .. import (
    factory,
    models,
)


if TYPE_CHECKING:
    # TODO use AbstractBaseUser instead
    from user.models import User as _User  # noqa: F401


@pytest.fixture
def now() -> datetime:
    """Return now."""
    return timezone.now()


@pytest.fixture
def workspace() -> models.Workspace:
    """Return workspace."""
    workspace = factory.WorkspaceFactory.create()
    CustomerFactory.create(workspace=workspace)
    return workspace


@pytest.fixture
def other_workspace() -> models.Workspace:
    """Return workspace."""
    return factory.WorkspaceFactory.create()


@pytest.fixture
def workspace_user_invite(
    workspace: models.Workspace, user_invite: user_models.UserInvite
) -> models.WorkspaceUserInvite:
    """Return workspace user invite."""
    return factory.WorkspaceUserInviteFactory.create(
        user_invite=user_invite,
        workspace=workspace,
    )


@pytest.fixture
def workspace_user(
    workspace: models.Workspace, user: "_User"
) -> models.WorkspaceUser:
    """Return workspace user with owner status."""
    return factory.WorkspaceUserFactory.create(
        workspace=workspace,
        user=user,
        role=models.WorkspaceUserRoles.OWNER,
    )


@pytest.fixture
def other_workspace_user(
    workspace: models.Workspace, other_user: "_User"
) -> models.WorkspaceUser:
    """Return workspace user for other_user."""
    return factory.WorkspaceUserFactory.create(
        workspace=workspace, user=other_user
    )


@pytest.fixture
def other_workspace_workspace_user(
    other_workspace: models.Workspace, other_user: "_User"
) -> models.WorkspaceUser:
    """Return workspace user for other_user."""
    return factory.WorkspaceUserFactory.create(
        workspace=other_workspace, user=other_user
    )


@pytest.fixture
def workspace_board(workspace: models.Workspace) -> models.WorkspaceBoard:
    """Return workspace board."""
    return factory.WorkspaceBoardFactory.create(workspace=workspace)


@pytest.fixture
def archived_workspace_board(
    workspace: models.Workspace, now: datetime
) -> models.WorkspaceBoard:
    """Return archived workspace board."""
    return factory.WorkspaceBoardFactory.create(
        workspace=workspace, archived=now
    )


@pytest.fixture
def workspace_board_section(
    workspace_board: models.WorkspaceBoard,
) -> models.WorkspaceBoardSection:
    """Return workspace board section."""
    return factory.WorkspaceBoardSectionFactory.create(
        workspace_board=workspace_board,
    )


@pytest.fixture
def task(
    workspace_board_section: models.WorkspaceBoardSection,
    workspace_user: models.WorkspaceUser,
) -> models.Task:
    """Return task."""
    return factory.TaskFactory.create(
        workspace_board_section=workspace_board_section,
        assignee=workspace_user,
    )


@pytest.fixture
def other_task(
    workspace_board_section: models.WorkspaceBoardSection,
) -> models.Task:
    """Return another task belonging to the same workspace board section."""
    return factory.TaskFactory.create(
        workspace_board_section=workspace_board_section,
    )


@pytest.fixture
def label(workspace: models.Workspace) -> models.Label:
    """Return a label."""
    return factory.LabelFactory.create(
        workspace=workspace,
    )


@pytest.fixture
def task_label(task: models.Task, label: models.Label) -> models.TaskLabel:
    """Return a label."""
    return factory.TaskLabelFactory.create(
        task=task,
        label=label,
    )


@pytest.fixture
def sub_task(task: models.Task) -> models.SubTask:
    """Return subtask."""
    return factory.SubTaskFactory.create(
        task=task,
    )


@pytest.fixture
def chat_message(
    task: models.Task, workspace_user: models.WorkspaceUser
) -> models.ChatMessage:
    """Return ChatMessage instance."""
    return factory.ChatMessageFactory.create(
        task=task,
        author=workspace_user,
    )


@pytest.fixture
def user_model() -> Type["_User"]:
    """Return user model class."""
    return cast(Type["_User"], auth.get_user_model())
