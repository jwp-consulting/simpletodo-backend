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
"""Test task CRUD views."""
from django.urls import (
    reverse,
)

import pytest
from rest_framework import status
from rest_framework.response import (
    Response,
)
from rest_framework.test import (
    APIClient,
)

from projectify.workspace.models.section import (
    Section,
)
from projectify.workspace.models.task import (
    Task,
)
from pytest_types import (
    DjangoAssertNumQueries,
)

from ... import (
    models,
)


class UnauthenticatedTestMixin:
    """Test that resource cannot be accessed without authorization."""

    def test_unauthenticated(
        self, resource_url: str, rest_client: APIClient
    ) -> None:
        """Test we cannot access the resource."""
        response: Response = rest_client.options(resource_url)
        # It's not 403, because DRF does not return the www authenticate realm
        # as a response to an API user.
        # See
        # https://github.com/encode/django-rest-framework/blob/605cc4f7367f58002056453d9befd3c1918f6a38/rest_framework/authentication.py#L112
        # there is no "authenticate_header" method. If it existed, we would
        # get a 401 instead. I was confused at first, but by their logic it
        # makes some sense.
        assert response.status_code == 403, response.data


# Create
@pytest.mark.django_db
class TestTaskCreate(UnauthenticatedTestMixin):
    """Test task creation."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to resource."""
        return reverse("workspace:tasks:create")

    @pytest.fixture
    def payload(
        self,
        section: models.Section,
    ) -> dict[str, object]:
        """Return a payload for API."""
        return {
            "title": "bla",
            "labels": [],
            "assignee": None,
            "section": {"uuid": str(section.uuid)},
            "sub_tasks": [
                {"title": "I am a sub task", "done": False},
            ],
        }

    def test_unauthorized(
        self,
        rest_meddling_client: APIClient,
        resource_url: str,
        payload: dict[str, object],
    ) -> None:
        """Test creating when unauthorized."""
        response = rest_meddling_client.post(
            resource_url, payload, format="json"
        )
        # We get 400 and NOT 403. We don't want to tell the user whether a
        # section with the given UUID exists. Instead, we
        # will treat it like a non-existent UUID. That makes sense, because to
        # the user it *really* does not exist and anything else does not
        # matter.
        assert response.status_code == 400, response.data
        assert Task.objects.count() == 0

    def test_authenticated(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        team_member: models.TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
        payload: dict[str, object],
    ) -> None:
        """Test creating when authenticated."""
        # 6 queries just for assigning a user
        # TODO We are going from 34 -> 44 queries. This means an increase of 9
        # queries after we started firing a signal after serializer.save()
        # The increase below for RetrieveUpdate was only 7. Maybe we can look
        # into where the additional 3 queries on top of the 7 come. It could be
        # somethign we failed to select or prefetch.
        # XXX Justus 2024-01-11 went up to 22 now, but since we are refactoring
        # signals, this might change up so I will ignore this for now
        # 25 now
        # 26 now
        # 24 now
        with django_assert_num_queries(22):
            response = rest_user_client.post(
                resource_url,
                {**payload, "assignee": {"uuid": str(team_member.uuid)}},
                format="json",
            )
            assert response.status_code == 201, response.data
        assert Task.objects.count() == 1
        assert Task.objects.get().assignee == team_member


# Read
@pytest.mark.django_db
class TestTaskRetrieveUpdateDestroy(UnauthenticatedTestMixin):
    """Test Task read, update and delete."""

    @pytest.fixture
    def resource_url(self, task: Task) -> str:
        """Return URL to resource."""
        return reverse("workspace:tasks:read-update-delete", args=(task.uuid,))

    @pytest.fixture
    def payload(
        self,
        section: models.Section,
    ) -> dict[str, object]:
        """Create payload."""
        return {
            "title": "Hello world",
            "section": {"uuid": str(section.uuid)},
            "number": 2,
            "labels": [],
            "assignee": None,
        }

    def test_unauthorized(
        self,
        rest_meddling_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace: models.Workspace,
    ) -> None:
        """Test retrieving when logged in, but not authorized."""
        with django_assert_num_queries(1):
            response = rest_meddling_client.get(resource_url)
            assert response.status_code == 404, response.data

    def test_authenticated(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        team_member: models.TeamMember,
        task: Task,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test retrieving when authenticated."""
        with django_assert_num_queries(4):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 200, response.data

        assert response.data["uuid"] == str(task.uuid)

    def test_update(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        team_member: models.TeamMember,
        section: models.Section,
        payload: dict[str, object],
    ) -> None:
        """Test updating a task when logged in correctly."""
        # XXX high query count but ignore for now
        # 29 now
        # 31 now
        # 28 now
        with django_assert_num_queries(25):
            response = rest_user_client.put(
                resource_url,
                {**payload, "assignee": {"uuid": str(team_member.uuid)}},
                format="json",
            )
            assert response.status_code == 200, response.content
        assert response.data["title"] == "Hello world"
        # We get the whole nested thing
        assert response.data["section"]["title"] == section.title

    def test_delete(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test deleting a task."""
        with django_assert_num_queries(10):
            response = rest_user_client.delete(resource_url)
            assert response.status_code == 204, response.content
        # Ensure that the task is gone for good
        with django_assert_num_queries(1):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 404, response.content


# RPC
@pytest.mark.django_db
class TestMoveTaskToSection:
    """Test moving a task to a section."""

    @pytest.fixture
    def resource_url(self, task: Task) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:tasks:move-to-section",
            args=(str(task.uuid),),
        )

    def test_simple(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        section: Section,
        other_section: Section,
        task: Task,
    ) -> None:
        """Test moving a task."""
        assert task.section == section
        with django_assert_num_queries(18):
            response = rest_user_client.post(
                resource_url,
                data={"section_uuid": str(other_section.uuid)},
            )
            assert response.status_code == status.HTTP_200_OK, response.data

        task.refresh_from_db()
        assert task.section == other_section
        assert task._order == 0


@pytest.mark.django_db
class TestTaskMoveAfterTask:
    """Test moving a task."""

    @pytest.fixture
    def resource_url(self, task: Task) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:tasks:move-after-task",
            args=(str(task.uuid),),
        )

    def test_simple(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        other_task: Task,
    ) -> None:
        """Test as an authenticated user."""
        with django_assert_num_queries(17):
            response = rest_user_client.post(
                resource_url,
                data={"task_uuid": str(other_task.uuid)},
            )
            assert response.status_code == status.HTTP_200_OK, response.data
