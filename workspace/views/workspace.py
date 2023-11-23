"""Workspace CRUD views."""
import uuid
from typing import (
    Any,
    Optional,
)

from django.db.models import (
    Prefetch,
)
from django.shortcuts import (
    get_object_or_404,
)

from rest_framework import (
    generics,
    parsers,
    views,
)
from rest_framework.request import (
    Request,
)
from rest_framework.response import (
    Response,
)

from workspace.services.workspace import (
    workspace_create,
    workspace_update,
)

from .. import (
    models,
)
from ..models.workspace import (
    Workspace,
    WorkspaceQuerySet,
)
from ..serializers.base import (
    WorkspaceBaseSerializer,
)
from ..serializers.workspace import (
    InviteUserToWorkspaceSerializer,
    WorkspaceDetailSerializer,
)


# Create
class WorkspaceCreate(
    generics.CreateAPIView[
        models.Workspace,
        models.WorkspaceQuerySet,
        WorkspaceBaseSerializer,
    ]
):
    """Create a workspace."""

    serializer_class = WorkspaceBaseSerializer

    def perform_create(self, serializer: WorkspaceBaseSerializer) -> None:
        """Create the workspace and add this user."""
        workspace = workspace_create(
            **serializer.validated_data, owner=self.request.user
        )
        # Kind of hacky, CreateAPIView relies on this being set when
        # serializing the result
        serializer.instance = workspace


# Read
class WorkspaceList(
    generics.ListAPIView[
        models.Workspace,
        models.WorkspaceQuerySet,
        WorkspaceBaseSerializer,
    ]
):
    """List all workspaces for a user."""

    queryset = models.Workspace.objects.all()
    serializer_class = WorkspaceBaseSerializer

    def get_queryset(self) -> models.WorkspaceQuerySet:
        """Filter by user."""
        user = self.request.user
        return self.queryset.get_for_user(user)


# Read + Update
class WorkspaceReadUpdate(
    generics.RetrieveUpdateAPIView[
        models.Workspace,
        models.WorkspaceQuerySet,
        WorkspaceDetailSerializer,
    ]
):
    """Workspace retrieve view."""

    queryset = models.Workspace.objects.prefetch_related(
        "label_set",
    ).prefetch_related(
        Prefetch(
            "workspaceboard_set",
            queryset=models.WorkspaceBoard.objects.filter_by_archived(False),
        ),
        Prefetch(
            "workspaceuser_set",
            queryset=models.WorkspaceUser.objects.select_related(
                "user",
            ),
        ),
    )
    serializer_class = WorkspaceDetailSerializer

    def get_object(self) -> models.Workspace:
        """Return queryset with authenticated user in mind."""
        user = self.request.user
        qs = self.get_queryset()
        qs = qs.filter_for_user_and_uuid(
            user,
            self.kwargs["workspace_uuid"],
        )
        workspace: models.Workspace = get_object_or_404(qs)
        return workspace

    def perform_update(self, serializer: WorkspaceDetailSerializer) -> None:
        """Perform update."""
        instance = serializer.instance
        # This should not happen -- the point of updating is that we already
        # have an instance present
        if instance is None:
            raise ValueError("perform_update was called without instance")
        data = serializer.validated_data
        workspace_update(
            workspace=instance,
            title=data["title"],
            description=data.get("description"),
            who=self.request.user,
        )


# Delete


# RPC
# TODO the following two views are candidates for a GenericViewSet
class WorkspacePictureUploadView(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    def post(
        self,
        request: Request,
        uuid: uuid.UUID,
        format: Optional[str] = None,
    ) -> Response:
        """Handle POST."""
        user = request.user
        file_obj = request.data["file"]
        qs = models.Workspace.objects.filter_for_user_and_uuid(
            user,
            uuid,
        )
        workspace = get_object_or_404(qs)
        workspace.picture = file_obj
        workspace.save()
        return Response(status=204)


class InviteUserToWorkspace(
    generics.CreateAPIView[
        Workspace, WorkspaceQuerySet, InviteUserToWorkspaceSerializer
    ]
):
    """Invite a user to a workspace."""

    lookup_field = "uuid"
    queryset = Workspace.objects.all()
    serializer_class = InviteUserToWorkspaceSerializer

    # A given TypedDict is a bit hard to override...
    def get_serializer_context(self) -> Any:
        """Enrich serializer context with workspace."""
        context = super().get_serializer_context()
        return {
            **context,
            "workspace": self.get_object(),
        }

    def get_queryset(self) -> WorkspaceQuerySet:
        """Search for workspace belonging to this user."""
        return models.Workspace.objects.filter_for_user_and_uuid(
            self.request.user,
            # We can look up by the uuid separately, I guess...
            # XXX this queryset will only have 0 or 1 results.
            self.kwargs["uuid"],
        )
