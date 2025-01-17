# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Contains task model / qs / manager."""

import logging
import uuid
from typing import TYPE_CHECKING, Any, Optional, cast

from django.db import models
from django.utils.translation import gettext_lazy as _

import pgtrigger

from projectify.lib.models import BaseModel, TitleDescriptionModel

from .types import GetOrder, SetOrder

logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager  # noqa: F401

    from . import (  # noqa: F401
        ChatMessage,
        Label,
        Section,
        SubTask,
        TaskLabel,
        TeamMember,
        Workspace,
    )


class Task(TitleDescriptionModel, BaseModel):
    """Task, belongs to section."""

    workspace = models.ForeignKey["Workspace"](
        "workspace.Workspace",
        on_delete=models.CASCADE,
    )

    section = models.ForeignKey["Section"]("Section", on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    assignee = models.ForeignKey["TeamMember"](
        "TeamMember",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Team member this task is assigned to."),
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Due date for this task"),
    )
    labels = models.ManyToManyField(
        "workspace.Label",
        through="workspace.TaskLabel",
    )  # type: models.ManyToManyField["Label", "TaskLabel"]

    number = models.PositiveIntegerField()

    if TYPE_CHECKING:
        # Related fields
        subtask_set: RelatedManager["SubTask"]
        chatmessage_set: RelatedManager["ChatMessage"]
        tasklabel_set: RelatedManager["TaskLabel"]

        # Order related
        get_subtask_order: GetOrder
        set_subtask_order: SetOrder
        _order: int
        id: int

    def get_next_section(self) -> "Section":
        """Return instance of the next section."""
        next_section: "Section" = self.section.get_next_in_order()
        return next_section

    # TODO we can probably do better than any here
    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save to add task number."""
        if cast(Optional[int], self.number) is None:
            self.number = self.workspace.increment_highest_task_number()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return title."""
        return self.title

    class Meta:
        """Meta."""

        order_with_respect_to = "section"
        constraints = [
            models.UniqueConstraint(
                fields=["section", "_order"],
                name="unique_task_order",
                deferrable=models.Deferrable.DEFERRED,
            ),
            models.UniqueConstraint(
                fields=["workspace", "number"],
                name="unique_task_number",
                deferrable=models.Deferrable.DEFERRED,
            ),
        ]

        triggers = (
            pgtrigger.Trigger(
                name="read_only_task_number",
                when=pgtrigger.Before,
                operation=pgtrigger.Update,
                func="""
              BEGIN
                IF NEW.number != OLD.number THEN
                    RAISE EXCEPTION 'invalid number: Task number \
                        cannot be modified after inserting Task.';
                END IF;
                RETURN NEW;
              END;""",
            ),
            pgtrigger.Trigger(
                name="ensure_correct_workspace",
                when=pgtrigger.Before,
                operation=pgtrigger.Insert | pgtrigger.Update,
                func="""
                      DECLARE
                        correct_workspace_id   INTEGER;
                      BEGIN
                        SELECT "workspace_workspace"."id" INTO correct_workspace_id
                        FROM "workspace_workspace"
                        INNER JOIN "workspace_project"
                            ON ("workspace_workspace"."id" = \
                            "workspace_project"."workspace_id")
                        INNER JOIN "workspace_section"
                            ON ("workspace_project"."id" = \
                                 "workspace_section"."project_id")
                        INNER JOIN "workspace_task"
                            ON ("workspace_section"."id" = \
                                "workspace_task"."section_id")
                        WHERE "workspace_task"."id" = NEW.id
                        LIMIT 1;
                        IF correct_workspace_id != NEW.workspace_id THEN
                            RAISE EXCEPTION 'invalid workspace_id: workspace being \
                                inserted does not match correct derived workspace.';
                        END IF;
                        RETURN NEW;
                      END;""",
            ),
        )
