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
"""
Workspace app rules.

The order of rules follows the ordering of models.
"""
import logging
from typing import (
    Literal,
    Union,
)

import rules

from projectify.corporate.services.customer import (
    customer_check_active_for_workspace,
)
from projectify.corporate.types import WorkspaceFeatures
from projectify.user.models import User
from projectify.workspace.models.chat_message import ChatMessage
from projectify.workspace.models.const import WorkspaceUserRoles
from projectify.workspace.models.label import Label
from projectify.workspace.models.sub_task import SubTask
from projectify.workspace.models.task import Task
from projectify.workspace.models.task_label import TaskLabel
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.workspace_board_section import (
    WorkspaceBoardSection,
)
from projectify.workspace.selectors.workspace_user import (
    workspace_user_find_for_workspace,
)

logger = logging.getLogger(__name__)


def check_permissions_for(
    role: WorkspaceUserRoles, user: User, target: Workspace
) -> bool:
    """Check whether a user has required role for target."""
    workspace = target
    workspace_user = workspace_user_find_for_workspace(
        workspace=workspace,
        user=user,
    )
    if workspace_user is None:
        return False
    return workspace.has_at_least_role(workspace_user, role)


# Role predicates
# Observer < Member < Maintainer < Owner
@rules.predicate
def is_at_least_observer(user: User, target: Workspace) -> bool:
    """Return True if a user is at least an observer of workspace parent."""
    return check_permissions_for(
        WorkspaceUserRoles.OBSERVER,
        user,
        target,
    )


@rules.predicate
def is_at_least_member(user: User, target: Workspace) -> bool:
    """Return True if a user is at least a member of workspace parent."""
    return check_permissions_for(
        WorkspaceUserRoles.MEMBER,
        user,
        target,
    )


@rules.predicate
def is_at_least_maintainer(user: User, target: Workspace) -> bool:
    """Return True if a user is at least a maintainer of workspace parent."""
    return check_permissions_for(
        WorkspaceUserRoles.MAINTAINER,
        user,
        target,
    )


@rules.predicate
def is_at_least_owner(user: User, target: Workspace) -> bool:
    """Return True if a user is at least an owner of workspace parent."""
    return check_permissions_for(
        WorkspaceUserRoles.OWNER,
        user,
        target,
    )


# It is perhaps not necessary to check if the workspace exists,
# or we can cache it as part of the predicate invocation
def check_available_features(
    features: WorkspaceFeatures, user: User, target: Workspace
) -> bool:
    """Return True if a workspace has a feature set active."""
    workspace = target
    workspace_user = workspace_user_find_for_workspace(
        workspace=workspace,
        user=user,
    )
    if workspace_user is None:
        logger.warning("No workspace user found for user %s", user)
        return False
    return customer_check_active_for_workspace(workspace=workspace) == features


@rules.predicate
def belongs_to_full_workspace(user: User, target: Workspace) -> bool:
    """
    Return True if target belongs to a full workspace.

    Also returns True if target is an active workspace itself.
    """
    return check_available_features("full", user, target)


@rules.predicate
def belongs_to_trial_workspace(user: User, target: Workspace) -> bool:
    """Return True if target belongs to a workspace."""
    return check_available_features("trial", user, target)


CreateWhat = Literal[
    "ChatMessage",
    "Label",
    "SubTask",
    "Task",
    "TaskLabel",
    "WorkspaceBoard",
    "WorkspaceBoardSection",
    "WorkspaceUserAndInvite",
]


Limitation = Union[None, int]
trial_conditions: dict[CreateWhat, Limitation] = {
    "ChatMessage": 0,
    "Label": 10,
    "SubTask": 1000,
    "Task": 1000,
    "TaskLabel": None,
    "WorkspaceBoard": 10,
    "WorkspaceBoardSection": 100,
    "WorkspaceUserAndInvite": 2,
}


def check_trial_conditions(create_what: CreateWhat, target: Workspace) -> bool:
    """
    Return True if for a target type, something can still be created.

    Limitations for trial plan:
    Be able to create 10 boards and up to 100 sections across all boards
    Be able to create 1000 tasks in that workspace
    Be able to create 10 * 100 sub tasks
    Be able to add one more user, therefore that workspace being limited to having
    2 workspace users in total.
    Be able to create 10 labels, assign them to all tasks
    Limitations for a trial workspace are
    - ChatMessage: 0 chat messages,
    - Label: 10 labels
    - SubTask: 1000 sub tasks,
    - Task: 1000 tasks,
    - TaskLabel: unlimited,
    - WorkspaceBoard: 10,
    - WorkspaceBoardSection: 100,
    - WorkspaceUser + WorkspaceUserInivite(unredeemed): 2
    """
    workspace = target
    limit = trial_conditions[create_what]
    # Short circuit
    if limit is None:
        return True
    match create_what:
        case "ChatMessage":
            # XXX At the moment, chat messages are not supported
            return (
                ChatMessage.objects.filter(task__workspace=workspace).count()
                < limit
            )
        case "Label":
            return Label.objects.filter(workspace=workspace).count() < limit
        case "SubTask":
            return (
                SubTask.objects.filter(task__workspace=workspace).count()
                < limit
            )
        case "Task":
            return (
                Task.objects.filter(
                    workspace_board_section__workspace_board__workspace=workspace
                ).count()
                < limit
            )
        case "TaskLabel":
            return (
                TaskLabel.objects.filter(label__workspace=workspace).count()
                < limit
            )
        case "WorkspaceBoard":
            return workspace.workspaceboard_set.count() < limit
        case "WorkspaceBoardSection":
            return (
                WorkspaceBoardSection.objects.filter(
                    workspace_board__workspace=workspace
                ).count()
                < limit
            )
        case "WorkspaceUserAndInvite":
            user_count = workspace.users.count()
            invite_count = workspace.workspaceuserinvite_set.filter(
                redeemed=False
            ).count()
            return user_count + invite_count < limit


@rules.predicate
def within_trial_chat_message_quota(user: User, target: Workspace) -> bool:
    """Return True if a chat message can be created for workspace."""
    return check_trial_conditions("ChatMessage", target)


@rules.predicate
def within_trial_label_quota(user: User, target: Workspace) -> bool:
    """Return True if a label can be created for workspace."""
    return check_trial_conditions("Label", target)


@rules.predicate
def within_trial_sub_task_quota(user: User, target: Workspace) -> bool:
    """Return True if a sub task can be created in workspace."""
    return check_trial_conditions("SubTask", target)


@rules.predicate
def within_trial_task_quota(user: User, target: Workspace) -> bool:
    """Return True if a task can be created in workspace."""
    return check_trial_conditions("Task", target)


@rules.predicate
def within_trial_task_label_quota(user: User, target: Workspace) -> bool:
    """Return True if a task label can be created for a task."""
    return check_trial_conditions("TaskLabel", target)


@rules.predicate
def within_trial_workspace_board_quota(user: User, target: Workspace) -> bool:
    """Return True if a workspace board can be created in workspace."""
    return check_trial_conditions("WorkspaceBoard", target)


@rules.predicate
def within_trial_workspace_board_section_quota(
    user: User, target: Workspace
) -> bool:
    """Return True if a section can be created in a workspace."""
    return check_trial_conditions("WorkspaceBoardSection", target)


@rules.predicate
def within_trial_workspace_user_quota(user: User, target: Workspace) -> bool:
    """Return True if a workspace user can be added to a workspace."""
    return check_trial_conditions("WorkspaceUserAndInvite", target)


@rules.predicate
def within_trial_workspace_user_invite_quota(
    user: User, target: Workspace
) -> bool:
    """Return True if a workspace user invite can be sent for a workspace."""
    return check_trial_conditions("WorkspaceUserAndInvite", target)


# TODO rules should be of the format
# <app>.<action>_<resource>
# and not as currently
# <app>.can_<action>_<resource>
# Going here by the django-rules guide:
# https://github.com/dfunckt/django-rules#setting-up-rules

# Workspace
# Anyone should be able to create a workspace
rules.add_perm(
    "workspace.can_create_workspace",
    # TODO use this instead:
    # rules.is_active,
    is_at_least_owner,
)
rules.add_perm(
    "workspace.can_read_workspace",
    is_at_least_observer,
)
rules.add_perm(
    "workspace.can_update_workspace",
    is_at_least_owner,
)
rules.add_perm(
    "workspace.can_delete_workspace",
    is_at_least_owner,
)

# Workspace user invite
workspace_user_invite_usable = (
    belongs_to_full_workspace  # type: ignore[operator]
    | (belongs_to_trial_workspace & within_trial_workspace_user_invite_quota)
)
rules.add_perm(
    "workspace.can_create_workspace_user_invite",
    is_at_least_owner & workspace_user_invite_usable,
)
rules.add_perm(
    "workspace.can_read_workspace_user_invite",
    is_at_least_owner & workspace_user_invite_usable,
)
rules.add_perm(
    "workspace.can_update_workspace_user_invite",
    is_at_least_owner & workspace_user_invite_usable,
)
rules.add_perm(
    "workspace.can_delete_workspace_user_invite",
    is_at_least_owner & workspace_user_invite_usable,
)

# Workspace user
workspace_user_usable = (
    belongs_to_full_workspace  # type: ignore[operator]
    | (belongs_to_trial_workspace & within_trial_workspace_user_quota)
)
rules.add_perm(
    "workspace.can_create_workspace_user",
    is_at_least_owner & workspace_user_usable,
)
rules.add_perm(
    "workspace.can_read_workspace_user",
    is_at_least_observer & workspace_user_usable,
)
rules.add_perm(
    "workspace.can_update_workspace_user",
    is_at_least_owner & workspace_user_usable,
)
rules.add_perm(
    "workspace.can_delete_workspace_user",
    is_at_least_owner & workspace_user_usable,
)

# Workspace board
workspace_board_usable = (
    belongs_to_full_workspace  # type: ignore[operator]
    | (belongs_to_trial_workspace & within_trial_workspace_board_quota)
)
rules.add_perm(
    "workspace.can_create_workspace_board",
    is_at_least_maintainer & workspace_board_usable,
)
rules.add_perm(
    "workspace.can_read_workspace_board",
    is_at_least_observer & workspace_board_usable,
)
rules.add_perm(
    "workspace.can_update_workspace_board",
    is_at_least_maintainer & workspace_board_usable,
)
rules.add_perm(
    "workspace.can_delete_workspace_board",
    is_at_least_maintainer & workspace_board_usable,
)

# Workspace board section
workspace_board_section_usable = (
    belongs_to_full_workspace  # type: ignore[operator]
    | (belongs_to_trial_workspace & within_trial_workspace_board_section_quota)
)
rules.add_perm(
    "workspace.can_create_workspace_board_section",
    is_at_least_maintainer & workspace_board_section_usable,
)
rules.add_perm(
    "workspace.can_read_workspace_board_section",
    is_at_least_observer & workspace_board_section_usable,
)
rules.add_perm(
    "workspace.can_update_workspace_board_section",
    is_at_least_maintainer & workspace_board_section_usable,
)
rules.add_perm(
    "workspace.can_delete_workspace_board_section",
    is_at_least_maintainer & workspace_board_section_usable,
)

# Task
task_usable = (
    belongs_to_full_workspace  # type: ignore[operator]
    | (belongs_to_trial_workspace & within_trial_task_quota)
)
rules.add_perm(
    "workspace.can_create_task",
    is_at_least_member & task_usable,
)
rules.add_perm(
    "workspace.can_read_task",
    is_at_least_observer & task_usable,
)
rules.add_perm(
    "workspace.can_update_task",
    is_at_least_member & task_usable,
)
rules.add_perm(
    "workspace.can_delete_task",
    is_at_least_maintainer & task_usable,
)

# Label
label_usable = (
    belongs_to_full_workspace  # type: ignore[operator]
    | (belongs_to_trial_workspace & within_trial_label_quota)
)
rules.add_perm(
    "workspace.can_create_label",
    is_at_least_maintainer & label_usable,
)
rules.add_perm(
    "workspace.can_read_label",
    is_at_least_observer & label_usable,
)
rules.add_perm(
    "workspace.can_update_label",
    is_at_least_maintainer & label_usable,
)
rules.add_perm(
    "workspace.can_delete_label",
    is_at_least_maintainer & label_usable,
)

# Task label
task_label_usable = (
    belongs_to_full_workspace  # type: ignore[operator]
    | (belongs_to_trial_workspace & within_trial_task_label_quota)
)
rules.add_perm(
    "workspace.can_create_task_label",
    is_at_least_member & task_label_usable,
)
rules.add_perm(
    "workspace.can_read_task_label",
    is_at_least_observer & task_label_usable,
)
rules.add_perm(
    "workspace.can_update_task_label",
    is_at_least_member & task_label_usable,
)
rules.add_perm(
    "workspace.can_delete_task_label",
    is_at_least_member & task_label_usable,
)


# Sub task
sub_task_usable = (
    belongs_to_full_workspace  # type: ignore[operator]
    | (belongs_to_trial_workspace & within_trial_sub_task_quota)
)
rules.add_perm(
    "workspace.can_create_sub_task",
    is_at_least_member & sub_task_usable,
)
rules.add_perm(
    "workspace.can_read_sub_task",
    is_at_least_observer & sub_task_usable,
)
rules.add_perm(
    "workspace.can_update_sub_task",
    is_at_least_member & sub_task_usable,
)
rules.add_perm(
    "workspace.can_delete_sub_task",
    is_at_least_member & sub_task_usable,
)

# Chat message
chat_message_usable = (
    belongs_to_full_workspace  # type: ignore[operator]
    | (belongs_to_trial_workspace & within_trial_chat_message_quota)
)
rules.add_perm(
    "workspace.can_create_chat_message",
    is_at_least_member & chat_message_usable,
)
rules.add_perm(
    "workspace.can_read_chat_message",
    is_at_least_observer & chat_message_usable,
)
rules.add_perm(
    "workspace.can_update_chat_message",
    is_at_least_member & chat_message_usable,
)
rules.add_perm(
    "workspace.can_delete_chat_message",
    is_at_least_maintainer & chat_message_usable,
)
