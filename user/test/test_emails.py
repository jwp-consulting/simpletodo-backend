"""Test user emails."""
from django.core.mail import EmailMessage

import pytest

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
        user.email = "contains space@example.com"
        user.save()
        mail = UserEmailConfirmationEmail(user)
        mail.send()
        assert len(mailoutbox) == 1
        m = mailoutbox[0]
        assert "contains%20space%40example.com" in m.body
        assert user.get_email_confirmation_token() in m.body


@pytest.mark.django_db
class TestUserPasswordResetEmail:
    """Test UserPasswordResetEmail."""

    def test_send(self, user: User, mailoutbox: list[EmailMessage]) -> None:
        """Test send."""
        mail = UserPasswordResetEmail(user)
        mail.send()
        assert len(mailoutbox) == 1
        m = mailoutbox[0]
        assert user.get_password_reset_token() in m.body
