# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK
"""Workspace CRUD views."""

from uuid import UUID

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

from django_ratelimit.decorators import ratelimit
from rest_framework import parsers, serializers, views
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)

from projectify.lib.error_schema import DeriveSchema
from projectify.lib.schema import extend_schema
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view
from projectify.workspace.selectors.project import (
    project_find_by_workspace_uuid,
)
from projectify.workspace.selectors.quota import workspace_get_all_quotas

from ..exceptions import UserAlreadyAdded, UserAlreadyInvited
from ..models import Workspace
from ..selectors.workspace import (
    WorkspaceDetailQuerySet,
    workspace_find_by_workspace_uuid,
    workspace_find_for_user,
)
from ..serializers.base import WorkspaceBaseSerializer
from ..serializers.workspace import WorkspaceDetailSerializer
from ..services.team_member_invite import (
    team_member_invite_create,
    team_member_invite_delete,
)
from ..services.workspace import workspace_create, workspace_update


# HTML
@platform_view
def workspace_list_view(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Show all workspaces."""
    workspaces = workspace_find_for_user(who=request.user)
    context = {"workspaces": workspaces}
    return render(request, "workspace/workspace_list.html", context)


@platform_view
def workspace_view(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Show workspace."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user, workspace_uuid=workspace_uuid
    )
    projects = project_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        archived=False,
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))
    context = {"workspace": workspace, "projects": projects}
    return render(request, "workspace/workspace_detail.html", context)


# Create
class WorkspaceCreate(views.APIView):
    """Create a workspace."""

    class WorkspaceCreateSerializer(serializers.ModelSerializer[Workspace]):
        """Accept title, description."""

        class Meta:
            """Meta."""

            fields = "title", "description"
            model = Workspace

    @extend_schema(
        request=WorkspaceCreateSerializer,
        responses={201: WorkspaceBaseSerializer, 400: DeriveSchema},
    )
    def post(self, request: Request) -> Response:
        """Create the workspace and add this user."""
        serializer = self.WorkspaceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workspace = workspace_create(
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description"),
            owner=self.request.user,
        )
        result = WorkspaceBaseSerializer(instance=workspace)
        return Response(status=HTTP_201_CREATED, data=result.data)


# Read
class UserWorkspaces(views.APIView):
    """List all workspaces for a user."""

    class UserWorkspaceSerializer(serializers.ModelSerializer[Workspace]):
        """Serialize a workspace for overview purposes."""

        class Meta:
            """Return only the bare minimum."""

            fields = ("title", "uuid")
            model = Workspace

    @extend_schema(responses={200: UserWorkspaceSerializer(many=True)})
    def get(self, request: Request) -> Response:
        """Handle GET."""
        workspaces = workspace_find_for_user(who=request.user)
        serializer = self.UserWorkspaceSerializer(
            instance=workspaces, many=True
        )
        return Response(status=HTTP_200_OK, data=serializer.data)


# Read + Update
class WorkspaceReadUpdate(views.APIView):
    """Workspace read and update view."""

    @extend_schema(
        responses={200: WorkspaceDetailSerializer},
    )
    def get(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle GET."""
        workspace = workspace_find_by_workspace_uuid(
            who=request.user,
            workspace_uuid=workspace_uuid,
            qs=WorkspaceDetailQuerySet,
        )
        if workspace is None:
            raise NotFound(_("Could not find workspace with this UUID"))
        workspace.quota = workspace_get_all_quotas(workspace)
        serializer = WorkspaceDetailSerializer(instance=workspace)
        return Response(status=HTTP_200_OK, data=serializer.data)

    class WorkspaceUpdateSerializer(serializers.ModelSerializer[Workspace]):
        """Accept title, description."""

        class Meta:
            """Meta."""

            fields = "title", "description"
            model = Workspace

    @extend_schema(
        request=WorkspaceUpdateSerializer,
        responses={200: WorkspaceUpdateSerializer, 400: DeriveSchema},
    )
    def put(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle PUT."""
        workspace = workspace_find_by_workspace_uuid(
            who=request.user,
            workspace_uuid=workspace_uuid,
            qs=WorkspaceDetailQuerySet,
        )
        if workspace is None:
            raise NotFound(_("Could not find workspace with this UUID"))

        serializer = self.WorkspaceUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workspace_update(
            workspace=workspace,
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description"),
            who=self.request.user,
        )
        return Response(status=HTTP_200_OK, data=serializer.data)


# Delete


# RPC
class WorkspacePictureUploadView(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    class WorkspacePictureUploadSerializer(serializers.Serializer):
        """Deserialize an image attachment."""

        file = serializers.ImageField(required=False)

    @extend_schema(
        request=WorkspacePictureUploadSerializer,
        responses={204: None, 400: DeriveSchema},
    )
    def post(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle POST."""
        workspace = workspace_find_by_workspace_uuid(
            who=request.user, workspace_uuid=workspace_uuid
        )
        if workspace is None:
            raise NotFound(
                _("Could not find workspace with UUID for picture upload")
            )

        serializer = self.WorkspacePictureUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_obj = serializer.validated_data.get("file")
        if file_obj is None:
            workspace.picture.delete()
        else:
            workspace.picture = file_obj
        workspace.save()
        return Response(status=204)


class InviteUserToWorkspace(views.APIView):
    """Invite a user to a workspace."""

    class InviteUserToWorkspaceSerializer(serializers.Serializer):
        """Accept email."""

        email = serializers.EmailField()

    @extend_schema(
        request=InviteUserToWorkspaceSerializer,
        responses={201: InviteUserToWorkspaceSerializer, 400: DeriveSchema},
    )
    @method_decorator(ratelimit(key="user", rate="5/h"))
    def post(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle POST."""
        workspace = workspace_find_by_workspace_uuid(
            workspace_uuid=workspace_uuid, who=request.user
        )
        if workspace is None:
            raise NotFound(_("No workspace found for this UUID"))

        serializer = self.InviteUserToWorkspaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email: str = serializer.validated_data["email"]
        try:
            team_member_invite_create(
                who=request.user, workspace=workspace, email_or_user=email
            )
        except UserAlreadyInvited:
            raise serializers.ValidationError(
                {
                    "email": _(
                        "User with email {email} has already been invited to "
                        "this workspace."
                    ).format(email=email)
                }
            )
        except UserAlreadyAdded:
            raise serializers.ValidationError(
                {
                    "email": _(
                        "User with email {email} has already been added to "
                        "this workspace."
                    ).format(email=email)
                }
            )
        return Response(data=serializer.data, status=HTTP_201_CREATED)


class UninviteUserFromWorkspace(views.APIView):
    """Remove a user invitation."""

    class UninviteUserFromWorkspaceSerializer(serializers.Serializer):
        """Accept email."""

        email = serializers.EmailField()

    @extend_schema(
        request=UninviteUserFromWorkspaceSerializer,
        responses={204: None, 400: DeriveSchema},
    )
    def post(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle POST."""
        workspace = workspace_find_by_workspace_uuid(
            workspace_uuid=workspace_uuid, who=request.user
        )
        if workspace is None:
            raise NotFound(_("No workspace found for this UUID"))
        serializer = self.UninviteUserFromWorkspaceSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        team_member_invite_delete(
            workspace=workspace,
            who=request.user,
            email=serializer.validated_data["email"],
        )
        return Response(data=serializer.data, status=HTTP_204_NO_CONTENT)
