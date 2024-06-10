# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021-2024 JWP Consulting GK
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
"""User model in user app."""
from typing import (
    Any,
    ClassVar,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import (
    models,
)
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import BaseModel

EMAIL_CONFIRMATION_TOKEN_SALT = "email-confirmation-token-salt"
PASSWORD_RESET_TOKEN_SALT = "password-reset-token-salt"


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """User class."""

    email = models.EmailField(
        verbose_name=_("Email"),
        unique=True,
    )
    unconfirmed_email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_(
            "If update email address requested, new, unconfirmed email"
        ),
    )
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()
    is_active = models.BooleanField(
        verbose_name=_("Is active"),
        default=False,
    )
    profile_picture = models.ImageField(
        upload_to="profile_picture/",
        blank=True,
        null=True,
    )
    preferred_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    tos_agreed = models.DateTimeField(
        verbose_name=_("Terms of service agreed"),
        help_text=_("Date and time user has agreed to terms of service"),
        blank=True,
        null=True,
    )
    privacy_policy_agreed = models.DateTimeField(
        verbose_name=_("Privacy Policy agreed"),
        help_text=_("Date and time user has agreed to privacy policy"),
        blank=True,
        null=True,
    )
    objects: ClassVar[BaseUserManager["User"]] = BaseUserManager()

    USERNAME_FIELD = "email"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save and call full_clean."""
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return printable user name."""
        if self.preferred_name is not None:
            return f"{self.preferred_name} ({self.email})"
        return self.email

    class Meta(BaseModel.Meta, AbstractBaseUser.Meta):
        """Add constraints."""

        constraints = (
            models.CheckConstraint(
                name="preferred_name",
                # Match period, colon followed by space, or not period
                # or period, colon at end of word
                check=models.Q(
                    preferred_name__regex=r"^([.:]\s|[^.:])*[.:]?$"
                ),
                violation_error_message=_(
                    "Preferred name can only contain '.' or ':' if followed "
                    "by whitespace or if located at the end."
                ),
            ),
        )
