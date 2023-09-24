"""Workspace signals."""
import logging
from collections.abc import (
    Mapping,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Type,
    TypeVar,
    cast,
)

from django.db import models as django_models
from django.db import (
    transaction,
)
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import (
    receiver,
)

from asgiref.sync import async_to_sync as _async_to_sync
from channels.layers import (
    get_channel_layer,
)
from rest_framework import serializers as drf_serializers

from user.signal_defs import (
    user_invitation_redeemed,
)

from . import (
    models,
    serializers,
    signal_defs,
    types,
)


if TYPE_CHECKING:
    from user.models import (  # noqa: F401
        User,
    )


Unknown = object


logger = logging.getLogger(__name__)

# TODO AsyncToSync is typed in a newer (unreleased) version of asgiref
# which we indirectly install with channels, which has not been
# renewed in a while Justus 2023-05-19
async_to_sync = cast(Any, _async_to_sync)


@receiver(signal_defs.workspace_user_invited)
def send_invitation_email(
    instance: models.WorkspaceUser, **kwargs: object
) -> None:
    """Send email when workspace user is invited."""
    # Avoid circular import
    from . import (
        emails,
    )

    email = emails.WorkspaceUserInviteEmail(instance)
    email.send()


def group_send(destination: str, message: types.Message) -> None:
    """Send message to a channels group."""
    channel_layer = get_channel_layer()
    if not channel_layer:
        raise Exception("Did not get channel layer")
    async_to_sync(channel_layer.group_send)(
        destination,
        message,
    )


M = TypeVar("M", bound=django_models.Model)


def serialize(
    serializer: Type[drf_serializers.ModelSerializer[M]],
    instance: M,
) -> Mapping[str, object]:
    """Serialize a django model instance and then render it to JSON."""
    serialized: Mapping[str, object] = serializer(instance).data
    return serialized


def send_workspace_change_signal(instance: models.Workspace) -> None:
    """Send workspace.change signal to correct group."""
    uuid = str(instance.uuid)
    data = serialize(serializers.WorkspaceDetailSerializer, instance)
    group_send(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": uuid,
            "data": data,
        },
    )


def send_workspace_board_change_signal(
    instance: models.WorkspaceBoard,
) -> None:
    """Send workspace_board.change signal to correct group."""
    uuid = str(instance.uuid)
    data = serialize(serializers.WorkspaceBoardDetailSerializer, instance)
    group_send(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
            "data": data,
        },
    )


def send_task_change_signal(instance: models.Task) -> None:
    """Send task.change signal to correct group."""
    uuid = str(instance.uuid)
    data = serialize(serializers.TaskDetailSerializer, instance)
    group_send(
        f"task-{uuid}",
        {
            "type": "task.change",
            "uuid": uuid,
            "data": data,
        },
    )


@receiver(post_save, sender=models.Workspace)
def workspace_saved(instance: models.Workspace, **kwargs: Unknown) -> None:
    """Broadcast changes."""
    send_workspace_change_signal(instance)


@receiver(post_delete, sender=models.Workspace)
def workspace_deleted(instance: models.Workspace, **kwargs: Unknown) -> None:
    """Broadcast changes upon workspace delete."""
    send_workspace_change_signal(instance)


@receiver(post_save, sender=models.Label)
def label_saved(instance: models.Label, **kwargs: Unknown) -> None:
    """Broadcast changes upon label save."""
    workspace = instance.workspace
    send_workspace_change_signal(workspace)


@receiver(post_delete, sender=models.Label)
def label_deleted(instance: models.Label, **kwargs: Unknown) -> None:
    """Broadcast changes upon label delete."""
    workspace = instance.workspace
    send_workspace_change_signal(workspace)


@receiver(post_save, sender=models.WorkspaceUser)
def workspace_user_saved(
    instance: models.WorkspaceUser, **kwargs: Unknown
) -> None:
    """Broadcast changes."""
    workspace = instance.workspace
    send_workspace_change_signal(workspace)


@receiver(post_delete, sender=models.WorkspaceUser)
def workspace_user_delete(
    instance: models.WorkspaceUser, **kwargs: Unknown
) -> None:
    """Broadcast changes."""
    workspace = instance.workspace
    send_workspace_change_signal(workspace)


@receiver(post_save, sender=models.WorkspaceBoard)
def workspace_board_saved(
    instance: models.WorkspaceBoard, **kwargs: Unknown
) -> None:
    """Broadcast changes."""
    send_workspace_board_change_signal(instance)
    send_workspace_change_signal(instance.workspace)


@receiver(post_delete, sender=models.WorkspaceBoard)
def workspace_board_deleted(
    instance: models.WorkspaceBoard, **kwargs: Unknown
) -> None:
    """Broadcast changes."""
    send_workspace_board_change_signal(instance)
    send_workspace_change_signal(instance.workspace)


@receiver(post_save, sender=models.WorkspaceBoardSection)
def workspace_board_section_saved(
    instance: models.WorkspaceBoardSection, **kwargs: Unknown
) -> None:
    """Broadcast changes."""
    workspace_board = instance.workspace_board
    send_workspace_board_change_signal(workspace_board)


@receiver(post_delete, sender=models.WorkspaceBoardSection)
def workspace_board_section_deleted(
    instance: models.WorkspaceBoardSection, **kwargs: Unknown
) -> None:
    """Broadcast changes."""
    workspace_board = instance.workspace_board
    send_workspace_board_change_signal(workspace_board)


@receiver(post_save, sender=models.Task)
def task_saved(instance: models.Task, **kwargs: Unknown) -> None:
    """Broadcast changes."""
    workspace_board = instance.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(instance)


@receiver(post_delete, sender=models.Task)
def task_deleted(instance: models.Task, **kwargs: Unknown) -> None:
    """Broadcast changes."""
    workspace_board = instance.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(instance)


@receiver(post_save, sender=models.TaskLabel)
def task_label_saved(instance: models.TaskLabel, **kwargs: Unknown) -> None:
    """Broadcast changes upon task label save."""
    task = instance.task
    workspace_board = task.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(task)


@receiver(post_delete, sender=models.TaskLabel)
def task_label_deleted(instance: models.TaskLabel, **kwargs: Unknown) -> None:
    """Broadcast changes upon task label delete."""
    task = instance.task
    workspace_board = task.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(task)


@receiver(post_save, sender=models.SubTask)
def sub_task_saved(instance: models.SubTask, **kwargs: Unknown) -> None:
    """Broadcast changes."""
    task = instance.task
    workspace_board = task.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(task)


@receiver(post_delete, sender=models.SubTask)
def sub_task_deleted(instance: models.SubTask, **kwargs: Unknown) -> None:
    """Broadcast changes."""
    task = instance.task
    workspace_board = task.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(task)


@receiver(post_save, sender=models.ChatMessage)
def chat_message_saved(
    instance: models.ChatMessage, **kwargs: Unknown
) -> None:
    """Broadcast changes."""
    task = instance.task
    send_task_change_signal(task)


@receiver(post_delete, sender=models.ChatMessage)
def chat_message_deleted(
    instance: models.ChatMessage, **kwargs: Unknown
) -> None:
    """Broadcast changes."""
    task = instance.task
    send_task_change_signal(task)


@receiver(user_invitation_redeemed)
@transaction.atomic
def redeem_workspace_invitations(
    user: "User", instance: models.WorkspaceUserInvite, **kwargs: Unknown
) -> None:
    """Redeem workspace invitations."""
    qs = models.WorkspaceUserInvite.objects.filter(
        user_invite__user=user,
    )
    for invite in qs:
        invite.workspace.add_user(user)
        invite.redeem()
