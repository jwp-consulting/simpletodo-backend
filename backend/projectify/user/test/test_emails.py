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
"""Test user emails."""

import re

from django.core.mail import EmailMessage

import pytest

from projectify.user.services.internal import (
    Token,
    user_check_token,
)

from ..emails import (
    UserEmailConfirmationEmail,
    UserPasswordResetEmail,
)
from ..models import User


@pytest.mark.django_db
class TestUserEmailConfirmationEmail:
    """Test UserEmailConfirmationEmail."""

    def test_send(self, user: User, mailoutbox: list[EmailMessage]) -> None:
        """Test send."""
        user.email = "space@example.com"
        user.save()
        mail = UserEmailConfirmationEmail(receiver=user, obj=user)
        mail.send()
        assert len(mailoutbox) == 1
        m = mailoutbox[0]
        assert "space%40example.com" in m.body
        match = re.search("/user/confirm-email/.+/(.+)\n", m.body)
        assert match
        token = Token(match.group(1))
        assert user_check_token(
            token=token, user=user, kind="confirm_email_address"
        )


@pytest.mark.django_db
class TestUserPasswordResetEmail:
    """Test UserPasswordResetEmail."""

    def test_send(self, user: User, mailoutbox: list[EmailMessage]) -> None:
        """Test send."""
        mail = UserPasswordResetEmail(receiver=user, obj=user)
        mail.send()
        assert len(mailoutbox) == 1
        m = mailoutbox[0]
        match = re.search("/user/confirm-password-reset/.+/(.+)\n", m.body)
        assert match
        token = Token(match.group(1))
        assert user_check_token(token=token, user=user, kind="reset_password")
