# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test user invite services."""

import pytest
from faker import Faker

from projectify.user.models import User, UserInvite
from projectify.user.services.internal import user_create
from projectify.user.services.user_invite import (
    user_invite_create,
    user_invite_redeem,
    user_invite_redeem_many,
)


@pytest.mark.django_db
def test_invite_user() -> None:
    """Test inviting."""
    invite = user_invite_create(email="hello@example.com")
    assert invite


@pytest.mark.django_db
def test_invite_twice() -> None:
    """Test inviting twice."""
    user_invite_create(email="hello@example.com")
    # Idempotent
    user_invite_create(email="hello@example.com")
    assert UserInvite.objects.count() == 1


@pytest.mark.django_db
def test_invite_existing_user(user: User) -> None:
    """Ensure that inviting an existing user is impossible."""
    assert user_invite_create(email=user.email) is None


@pytest.mark.django_db
def test_redeem(user: User, user_invite: UserInvite) -> None:
    """Test redeeming a user invite."""
    assert user_invite.redeemed is False

    user_invite_redeem(user_invite=user_invite, user=user)
    user_invite.refresh_from_db()

    assert user_invite.user == user
    assert user_invite.redeemed is True


@pytest.mark.django_db
def test_redeem_invites(
    user: User,
    user_invite: UserInvite,
    redeemed_user_invite: UserInvite,
) -> None:
    """Test redeeming invites."""
    user_invite.email = user.email
    user_invite.save()
    assert not user_invite.redeemed
    user_invite_redeem_many(user=user)
    user_invite.refresh_from_db()
    assert user_invite.redeemed


@pytest.mark.django_db
def test_redeem_multiple_invites(faker: Faker) -> None:
    """Create multiple invites. Create a user. Nothing bad happens."""
    email = faker.email()
    user_invite_create(email=email)
    user_invite_create(email=email)
    user = user_create(email=email)
    user_invite_redeem_many(user=user)
