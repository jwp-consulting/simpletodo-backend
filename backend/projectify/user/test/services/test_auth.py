# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2024 JWP Consulting GK
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
"""Test user app auth services."""
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.test import RequestFactory

import pytest
from faker import Faker
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ...models import User
from ...services.auth import (
    user_confirm_email,
    user_confirm_password_reset,
    user_log_in,
    user_log_out,
    user_request_password_reset,
    user_sign_up,
)
from ...services.internal import Token, user_make_token

pytestmark = pytest.mark.django_db


def test_user_sign_up_no_agree(faker: Faker) -> None:
    """Test signing up a new user."""
    assert User.objects.count() == 0
    with pytest.raises(serializers.ValidationError):
        user_sign_up(
            email=faker.email(),
            password=faker.password(),
            tos_agreed=False,
            privacy_policy_agreed=False,
        )
    with pytest.raises(serializers.ValidationError) as error:
        user_sign_up(
            email=faker.email(),
            password=faker.password(),
            tos_agreed=False,
            privacy_policy_agreed=True,
        )
    assert error.match("terms of service")
    with pytest.raises(serializers.ValidationError) as error:
        user_sign_up(
            email=faker.email(),
            password=faker.password(),
            tos_agreed=True,
            privacy_policy_agreed=False,
        )
    assert error.match("privacy policy")
    assert User.objects.count() == 0


def test_user_sign_up(faker: Faker) -> None:
    """Test signing up a new user."""
    assert User.objects.count() == 0
    user_sign_up(
        email=faker.email(),
        password=faker.password(),
        tos_agreed=True,
        privacy_policy_agreed=True,
    )
    user = User.objects.get()
    assert user.privacy_policy_agreed is not None
    assert user.tos_agreed is not None


def test_user_sign_up_weak_password(faker: Faker) -> None:
    """Test signing up a new user, and choose a weak passsword."""
    assert User.objects.count() == 0
    with pytest.raises(ValidationError):
        user_sign_up(
            email=faker.email(),
            password="asd123",
            tos_agreed=True,
            privacy_policy_agreed=True,
        )
    assert User.objects.count() == 0


def test_user_confirm_email(user: User, inactive_user: User) -> None:
    """Test activating an active and inactive user."""
    assert user.is_active
    user_confirm_email(
        email=user.email,
        token=user_make_token(user=user, kind="confirm_email_address"),
    )
    user.refresh_from_db()
    assert user.is_active

    assert not inactive_user.is_active
    user_confirm_email(
        email=inactive_user.email,
        token=user_make_token(
            user=inactive_user, kind="confirm_email_address"
        ),
    )
    inactive_user.refresh_from_db()
    assert inactive_user.is_active


@pytest.fixture
def session_middleware() -> SessionMiddleware:
    """Create a session middlware instance."""
    return SessionMiddleware(lambda _: HttpResponse())


@pytest.fixture
def session_request(
    session_middleware: SessionMiddleware, rf: RequestFactory
) -> HttpRequest:
    """Return a request containing a session needed to test auth."""
    request = rf.get("/")
    session_middleware.process_request(request)
    request.session.save()
    request.user = AnonymousUser()
    return request


def test_user_log_in(
    user: User,
    password: str,
    session_request: HttpRequest,
) -> None:
    """Test logging in."""
    assert "_auth_user_id" not in session_request.session.keys()
    user_log_in(email=user.email, password=password, request=session_request)
    assert "_auth_user_id" in session_request.session.keys()


def test_user_log_in_wrong_password(
    user: User,
    session_request: HttpRequest,
) -> None:
    """Test logging in with wrong password."""
    # First with active user
    assert "_auth_user_id" not in session_request.session.keys()
    with pytest.raises(ValidationError) as error:
        user_log_in(
            email=user.email,
            password="wrongpassword",
            request=session_request,
        )
    assert "password is incorrect" in error.exconly()
    assert "_auth_user_id" not in session_request.session.keys()


def test_user_log_in_inactive(
    inactive_user: User,
    password: str,
    session_request: HttpRequest,
) -> None:
    """Test logging in as an inactive user."""
    # First with active user
    assert "_auth_user_id" not in session_request.session.keys()
    with pytest.raises(ValidationError) as error:
        user_log_in(
            email=inactive_user.email,
            password=password,
            request=session_request,
        )
    assert "not been confirmed" in error.exconly()
    assert "_auth_user_id" not in session_request.session.keys()


# - user_log_out
def test_user_log_out(
    session_request: HttpRequest, user: User, password: str
) -> None:
    """Test logging a user out."""
    # First we log in
    user_log_in(email=user.email, password=password, request=session_request)
    assert "_auth_user_id" in session_request.session.keys()
    user_log_out(request=session_request)
    assert "_auth_user_id" not in session_request.session.keys()


def test_user_log_out_not_logged_in(
    session_request: HttpRequest,
) -> None:
    """Test logging when not logged in."""
    assert "_auth_user_id" not in session_request.session.keys()
    with pytest.raises(ValidationError) as error:
        user_log_out(request=session_request)
    assert "no logged in user" in error.exconly()
    assert "_auth_user_id" not in session_request.session.keys()


def test_request_password_reset(
    user: User, faker: Faker, mailoutbox: list[object]
) -> None:
    """Test pw reset requests."""
    assert len(mailoutbox) == 0
    user_request_password_reset(email=user.email)
    assert len(mailoutbox) == 1
    with pytest.raises(ValidationError) as error:
        user_request_password_reset(email=faker.email())
    assert error.match("No user could be found")
    assert len(mailoutbox) == 1


@pytest.fixture
def reset_token(user: User) -> Token:
    """Create reset token for user."""
    return user_make_token(user=user, kind="reset_password")


@pytest.fixture
def new_password(password: str, faker: Faker) -> str:
    """Return new password for user."""
    new_password: str = faker.password()
    assert password != new_password
    return new_password


def test_confirm_password_reset_wrong_token(
    user: User, password: str, new_password: str
) -> None:
    """Test password reset confirmation with right email, wrong token."""
    with pytest.raises(ValidationError) as error:
        user_confirm_password_reset(
            email=user.email,
            new_password=new_password,
            token=Token("wrong token"),
        )
    assert error.match("token is invalid")
    user.refresh_from_db()
    assert user.check_password(password)


def test_confirm_password_reset_wrong_email(
    user: User,
    password: str,
    new_password: str,
    faker: Faker,
    reset_token: Token,
) -> None:
    """Test reset with right token, wrong email."""
    with pytest.raises(ValidationError) as error:
        user_confirm_password_reset(
            email=faker.email(),
            new_password=new_password,
            token=reset_token,
        )
    assert error.match("email is not recognized")
    user.refresh_from_db()
    assert user.check_password(password)


def test_confirm_password_reset_right_email(
    user: User,
    new_password: str,
    reset_token: Token,
) -> None:
    """Test reset with right token, right email."""
    user_confirm_password_reset(
        email=user.email,
        new_password=new_password,
        token=reset_token,
    )
    user.refresh_from_db()
    assert user.check_password(new_password)


def test_confirm_password_reset_reuse_token(
    user: User,
    new_password: str,
    faker: Faker,
    reset_token: Token,
) -> None:
    """Test reset when reusing old token."""
    user_confirm_password_reset(
        email=user.email,
        new_password=new_password,
        token=reset_token,
    )
    # Then reuse old token, right email
    new_new_password = faker.password()
    with pytest.raises(ValidationError) as error:
        user_confirm_password_reset(
            email=user.email,
            new_password=new_new_password,
            token=reset_token,
        )
    assert error.match("token is invalid")
    user.refresh_from_db()
    assert user.check_password(new_password)
