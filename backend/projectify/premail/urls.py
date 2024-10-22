# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2023 JWP Consulting GK
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
"""Premail urlpatterns."""

from django.urls import (
    path,
)

from .views import (
    EmailList,
    EmailPreview,
)

app_name = "premail"


urlpatterns = (
    path(r"", EmailList.as_view(), name="email-list"),
    path(
        r"<slug:slug>",
        EmailPreview.as_view(),
        name="email-preview",
    ),
)
