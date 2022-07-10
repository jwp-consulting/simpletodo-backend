"""Workspace views."""
from rest_framework import (
    generics,
    parsers,
    response,
    views,
)

from . import (
    models,
    serializers,
)


class WorkspacePictureUploadView(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    def post(self, request, uuid, format=None):
        """Handle POST."""
        file_obj = request.data["file"]
        workspace = models.Workspace.objects.get_for_user_and_uuid(
            request.user,
            uuid,
        )
        workspace.picture = file_obj
        workspace.save()
        return response.Response(status=204)


class WorkspaceBoardRetrieve(generics.RetrieveAPIView):
    """Workspace board retrieve view."""

    queryset = models.WorkspaceBoard.objects.prefetch_related(
        "workspaceboardsection_set",
        "workspaceboardsection_set__task_set",
        "workspaceboardsection_set__task_set__assignee",
        "workspaceboardsection_set__task_set__assignee__user",
        "workspaceboardsection_set__task_set__labels",
    )
    serializer_class = serializers.WorkspaceBoardSerializer

    def get_object(self):
        """Return queryset with authenticated user in mind."""
        user = self.request.user
        workspace_board = self.get_queryset().get_for_user_and_uuid(
            user,
            self.kwargs["workspace_board_uuid"],
        )
        return workspace_board