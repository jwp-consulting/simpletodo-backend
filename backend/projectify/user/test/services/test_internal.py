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
"""Test user app internal services."""

from datetime import datetime

from django.contrib.auth.tokens import PasswordResetTokenGenerator

import pytest

from ...models.user import User
from ...services.internal import (
    Token,
    TokenKind,
    user_check_token,
    user_create,
    user_create_superuser,
    user_make_token,
)

pytestmark = pytest.mark.django_db


def test_user_create() -> None:
    """Test creating a normal user."""
    u = user_create(email="hello@localhost")
    assert u.is_active is False


def test_user_create_superuser() -> None:
    """Test creating a superuser. A superuser should be active."""
    u = user_create_superuser(email="hello@localhost")
    assert u.is_active is True


@pytest.fixture
def deterministic_user() -> User:
    """Return user with predictable fields for token fn checking."""
    user = User(pk=1, last_login=None, email="hello@example", password="abc")
    return user


def now(_self: object) -> datetime:
    """Return fixed datetime for PasswordResetTokenGenerator."""
    return datetime(2024, 2, 15)


tokens: list[tuple[TokenKind, Token]] = [
    (
        "confirm_email_address",
        Token("c2ew00-a4662d1b9eaf0ed73d8ea4595b57fdf5"),
    ),
    ("reset_password", Token("c2ew00-8c001f3e5576f8df15f416d5a93ba55b")),
    ("update_email_address", Token("c2ew00-9991c260d5933cbd003f7655f775a2a6")),
]


@pytest.mark.parametrize("kind,token", tokens)
def test_user_make_token(
    deterministic_user: User,
    kind: TokenKind,
    token: Token,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test token making."""
    monkeypatch.setattr(PasswordResetTokenGenerator, "_now", now)
    assert user_make_token(user=deterministic_user, kind=kind) == token


@pytest.mark.parametrize(
    "kind", ["confirm_email_address", "reset_password", "update_email_address"]
)
def test_user_make_token_with_unconfirmed_email(
    deterministic_user: User,
    monkeypatch: pytest.MonkeyPatch,
    kind: TokenKind,
) -> None:
    """Test token making when unconfirmed_email changes."""
    monkeypatch.setattr(PasswordResetTokenGenerator, "_now", now)
    token1 = user_make_token(user=deterministic_user, kind=kind)
    deterministic_user.unconfirmed_email = "abc@example.com"
    token2 = user_make_token(user=deterministic_user, kind=kind)
    assert token1 != token2
    # Make sure we can repeat this
    token3 = user_make_token(user=deterministic_user, kind=kind)
    assert token2 == token3


@pytest.mark.parametrize("kind,token", tokens)
def test_user_check_token(
    deterministic_user: User,
    kind: TokenKind,
    token: Token,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test token checking."""
    monkeypatch.setattr(PasswordResetTokenGenerator, "_now", now)
    assert (
        user_check_token(
            user=deterministic_user,
            kind=kind,
            token=token,
        )
        is True
    )
    # We substring the token and test that it won't validate
    wrong_token = Token(token[:-1])
    assert (
        user_check_token(user=deterministic_user, kind=kind, token=wrong_token)
        is False
    )
