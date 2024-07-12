# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2022 JWP Consulting GK
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
"""Create ChatMessage model."""
# Generated by Django 3.2.11 on 2022-01-27 13:31

import uuid

import django.db.models.deletion
from django.conf import (
    settings,
)
from django.db import (
    migrations,
    models,
)

import projectify.lib.models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("workspace", "0010_auto_20211223_0634"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChatMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    projectify.lib.models.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    projectify.lib.models.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("text", models.TextField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="workspace.task",
                    ),
                ),
            ],
            options={
                "ordering": ("created",),
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
    ]
