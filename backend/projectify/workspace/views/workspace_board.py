# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
"""Workspace board views."""
from uuid import UUID

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from projectify.workspace.models import WorkspaceBoard
from projectify.workspace.selectors.workspace import (
    workspace_find_by_workspace_uuid,
)
from projectify.workspace.selectors.workspace_board import (
    WorkspaceBoardDetailQuerySet,
    workspace_board_find_by_workspace_board_uuid,
    workspace_board_find_by_workspace_uuid,
)
from projectify.workspace.serializers.base import WorkspaceBoardBaseSerializer
from projectify.workspace.serializers.workspace_board import (
    WorkspaceBoardDetailSerializer,
)
from projectify.workspace.services.workspace_board import (
    workspace_board_archive,
    workspace_board_create,
    workspace_board_delete,
    workspace_board_update,
)


# Create
class WorkspaceBoardCreate(APIView):
    """Create a workspace board."""

    class InputSerializer(serializers.ModelSerializer[WorkspaceBoard]):
        """Parse workspace board creation input."""

        workspace_uuid = serializers.UUIDField()

        class Meta:
            """Restrict to the bare minimum needed for creation."""

            model = WorkspaceBoard
            fields = "title", "description", "workspace_uuid", "due_date"

    def post(self, request: Request) -> Response:
        """Create a workspace board."""
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workspace_uuid: UUID = serializer.validated_data.pop("workspace_uuid")
        workspace = workspace_find_by_workspace_uuid(
            workspace_uuid=workspace_uuid,
            who=user,
        )
        if workspace is None:
            raise serializers.ValidationError(
                {"workspace_uuid": _("No workspace found for this UUID")}
            )
        workspace_board = workspace_board_create(
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description"),
            due_date=serializer.validated_data.get("due_date"),
            who=user,
            workspace=workspace,
        )

        output_serializer = WorkspaceBoardDetailSerializer(
            instance=workspace_board
        )
        return Response(data=output_serializer.data, status=201)


# Read + Update + Delete
class WorkspaceBoardReadUpdateDelete(APIView):
    """Workspace board retrieve view."""

    def get(self, request: Request, workspace_board_uuid: UUID) -> Response:
        """Handle GET."""
        workspace_board = workspace_board_find_by_workspace_board_uuid(
            who=request.user,
            workspace_board_uuid=workspace_board_uuid,
            qs=WorkspaceBoardDetailQuerySet,
        )
        if workspace_board is None:
            raise NotFound(_("No workspace board found for this uuid"))
        serializer = WorkspaceBoardDetailSerializer(
            instance=workspace_board,
        )
        return Response(serializer.data)

    def put(self, request: Request, workspace_board_uuid: UUID) -> Response:
        """Handle PUT."""
        workspace_board = workspace_board_find_by_workspace_board_uuid(
            who=request.user,
            workspace_board_uuid=workspace_board_uuid,
        )
        if workspace_board is None:
            raise NotFound(_("No workspace board found for this uuid"))
        serializer = WorkspaceBoardBaseSerializer(
            instance=workspace_board,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        workspace_board_update(
            who=self.request.user,
            workspace_board=workspace_board,
            title=data["title"],
            description=data.get("description"),
            due_date=data.get("due_date"),
        )
        return Response(data, status.HTTP_200_OK)

    def delete(self, request: Request, workspace_board_uuid: UUID) -> Response:
        """Handle DELETE."""
        workspace_board = workspace_board_find_by_workspace_board_uuid(
            who=request.user,
            workspace_board_uuid=workspace_board_uuid,
        )
        if workspace_board is None:
            raise NotFound(_("No workspace board found for this uuid"))
        workspace_board_delete(
            who=self.request.user,
            workspace_board=workspace_board,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


# List
class WorkspaceBoardArchivedList(APIView):
    """List archived workspace boards inside a workspace."""

    def get(self, request: Request, workspace_uuid: UUID) -> Response:
        """Get queryset."""
        workspace = workspace_find_by_workspace_uuid(
            workspace_uuid=workspace_uuid, who=request.user
        )
        if workspace is None:
            raise NotFound(_("No workspace found for this UUID"))
        workspace_boards = workspace_board_find_by_workspace_uuid(
            who=request.user,
            workspace_uuid=workspace_uuid,
            archived=True,
        )
        serializer = WorkspaceBoardBaseSerializer(
            instance=workspace_boards,
            many=True,
        )
        return Response(serializer.data)


# RPC
# TODO surely this can all be refactored
class WorkspaceBoardArchive(APIView):
    """Toggle the archived status of a board on or off."""

    class InputSerializer(serializers.Serializer):
        """Accept the desired archival status."""

        archived = serializers.BooleanField()

    def post(self, request: Request, workspace_board_uuid: UUID) -> Response:
        """Process request."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        workspace_board = workspace_board_find_by_workspace_board_uuid(
            workspace_board_uuid=workspace_board_uuid,
            who=request.user,
            include_archived=True,
        )
        if workspace_board is None:
            raise NotFound(_("No workspace board found for this UUID"))
        workspace_board_archive(
            workspace_board=workspace_board,
            archived=data["archived"],
            who=request.user,
        )
        workspace_board.refresh_from_db()
        output_serializer = WorkspaceBoardDetailSerializer(
            instance=workspace_board,
        )
        return Response(output_serializer.data, status=status.HTTP_200_OK)
