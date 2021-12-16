"""Workspace schema."""
import graphene
import graphene_django

from . import (
    models,
)


class Workspace(graphene_django.DjangoObjectType):
    """Workspace."""

    users = graphene.List("user.schema.User")
    boards = graphene.List("workspace.schema.WorkspaceBoard")

    def resolve_users(self, info):
        """Resolve workspace users."""
        return self.users.all()

    def resolve_boards(self, info):
        """Resolve workspace boards."""
        return self.workspaceboard_set.all()

    class Meta:
        """Meta."""

        fields = ("users", "created", "modified", "title", "description")
        model = models.Workspace


class WorkspaceBoard(graphene_django.DjangoObjectType):
    """WorkspaceBoard."""

    sections = graphene.List("workspace.schema.WorkspaceBoardSection")

    def resolve_sections(self, info):
        """Resolve workspace board sections."""
        return self.workspaceboardsection_set.all()

    class Meta:
        """Meta."""

        fields = ("created", "modified", "title", "description")
        model = models.WorkspaceBoard


class WorkspaceBoardSection(graphene_django.DjangoObjectType):
    """WorkspaceBoardSection."""

    class Meta:
        """Meta."""

        fields = ("created", "modified", "title", "description")
        model = models.WorkspaceBoardSection


class Query:
    """Query."""

    workspaces = graphene.List(Workspace)

    def resolve_workspaces(self, info):
        """Resolve user's workspaces."""
        return models.Workspace.objects.get_for_user(info.context.user)
