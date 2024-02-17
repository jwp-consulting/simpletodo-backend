# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2022, 2023 JWP Consulting GK
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
"""Top level conftest module."""
import base64
import random

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)
from django.test import (
    client,
)

import pytest
from faker import Faker
from rest_framework.test import (
    APIClient,
)

from projectify.user import models as user_models
from projectify.user.services.internal import (
    user_create,
    user_create_superuser,
)
from projectify.user.services.user_invite import (
    user_invite_create,
    user_invite_redeem,
)


@pytest.fixture
def password(faker: Faker) -> str:
    """Set default password."""
    pw: str = faker.password(length=20)
    return pw


@pytest.fixture
def user(faker: Faker, password: str) -> user_models.User:
    """Return a db user."""
    user = user_create(email=faker.email(), password=password)
    user.is_active = True
    user.preferred_name = faker.name()
    user.save()
    return user


@pytest.fixture
def superuser(faker: Faker) -> user_models.User:
    """Return a db super user."""
    return user_create_superuser(email=faker.email())


@pytest.fixture
def other_user(faker: Faker) -> user_models.User:
    """Return another db user."""
    return user_create(email=faker.email())


@pytest.fixture
def unrelated_user(faker: Faker) -> user_models.User:
    """Return unrelated user normally not in the same workspace."""
    return user_create(email=faker.email())


@pytest.fixture
def meddling_user(faker: Faker, password: str) -> user_models.User:
    """Create a canary user to check permissions."""
    user = user_create(email=faker.email(), password=password)
    user.is_active = True
    user.preferred_name = faker.name()
    user.save()
    return user


@pytest.fixture
def inactive_user(faker: Faker, password: str) -> user_models.User:
    """Return an inactive db user."""
    return user_create(email=faker.email(), password=password)


@pytest.fixture
def user_invite(faker: Faker) -> user_models.UserInvite:
    """Return a user invite."""
    user_invite = user_invite_create(email=faker.email())
    if user_invite is None:
        raise ValueError("Expected user_invite")
    return user_invite


@pytest.fixture
def redeemed_user_invite(faker: Faker) -> user_models.UserInvite:
    """Return a redeemed user invite."""
    email = faker.email()
    user_invite = user_invite_create(email=email)
    if user_invite is None:
        raise AssertionError("Expected user_invite")
    user = user_create(email=email)
    user_invite_redeem(user=user, user_invite=user_invite)
    return user_invite


@pytest.fixture
def user_client(
    client: client.Client, user: AbstractBaseUser
) -> client.Client:
    """Return logged in client."""
    client.force_login(user)
    return client


@pytest.fixture
def superuser_client(
    client: client.Client, superuser: AbstractBaseUser
) -> client.Client:
    """Return logged in super user client."""
    client.force_login(superuser)
    return client


# XXX same as rest_client
@pytest.fixture
def test_client() -> APIClient:
    """Return a client that we can use to test DRF views."""
    return APIClient()


@pytest.fixture
def rest_client() -> APIClient:
    """Return a logged-out client to test DRF views."""
    return APIClient()


@pytest.fixture
def rest_user_client(user: AbstractBaseUser) -> APIClient:
    """Return a logged in client that we can use to test DRF views."""
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def rest_meddling_client(meddling_user: AbstractBaseUser) -> APIClient:
    """Return a test client to check third party logged in access."""
    client = APIClient()
    client.force_authenticate(meddling_user)
    return client


@pytest.fixture
def png_image() -> bytes:
    """Return a simple png file."""
    return base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgAgAAAAAcoT2JAAAABGdBTUEAAYagMeiWX\
        wAAAB9JREFUeJxjYAhd9R+M8TCIUMIAU4aPATMJH2OQuQcAvUl/gYsJiakAAAAASUVORK5\
        CYII="
    )


@pytest.fixture
def uploaded_file(png_image: bytes) -> SimpleUploadedFile:
    """Return an UploadFile instance of the above png file."""
    return SimpleUploadedFile("test.png", png_image)


@pytest.fixture(scope="session", autouse=True)
def faker_seed() -> int:
    """Return a random seed every session."""
    return random.randint(0, 2**16)
