# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021-2024 JWP Consulting GK
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
"""Workspace board model."""
import uuid
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Self,
    cast,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.db import (
    models,
)
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import (
    TitleDescriptionModel,
)

from projectify.lib.models import BaseModel

from .workspace import (
    Workspace,
)
from .workspace_board_section import (
    WorkspaceBoardSection,
)

# TODO Here we could be using __all__


if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager  # noqa: F401

    from .types import (
        GetOrder,
        SetOrder,
    )


class WorkspaceBoardQuerySet(models.QuerySet["WorkspaceBoard"]):
    """WorkspaceBoard Manager."""

    def filter_by_workspace(self, workspace: Workspace) -> Self:
        """Filter by workspace."""
        return self.filter(workspace=workspace)

    def filter_by_user(self, user: AbstractBaseUser) -> Self:
        """Filter by user."""
        return self.filter(workspace__users=user)


class WorkspaceBoard(TitleDescriptionModel, BaseModel):
    """Workspace board."""

    workspace = models.ForeignKey["Workspace"](
        Workspace,
        on_delete=models.PROTECT,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    archived = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Archival timestamp of this workspace board."),
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Due date for this workspace board"),
    )

    objects: ClassVar[WorkspaceBoardQuerySet] = cast(  # type: ignore[assignment]
        WorkspaceBoardQuerySet, WorkspaceBoardQuerySet.as_manager()
    )

    if TYPE_CHECKING:
        # Related managers
        workspaceboardsection_set: RelatedManager["WorkspaceBoardSection"]

        # For ordering
        get_workspaceboardsection_order: GetOrder
        set_workspaceboardsection_order: SetOrder

    def __str__(self) -> str:
        """Return title."""
        return self.title

    class Meta:
        """Order by created, descending."""

        ordering = ("-created",)
