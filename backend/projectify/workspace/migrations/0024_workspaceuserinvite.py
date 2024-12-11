# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022 JWP Consulting GK
"""Create workspace user invite."""
# Generated by Django 4.0.2 on 2022-03-09 07:38

import django.db.models.deletion
from django.db import migrations, models

import projectify.lib.models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("user", "0008_userinvite"),
        ("workspace", "0023_alter_label_color"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkspaceUserInvite",
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
                    "user_invite",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.userinvite",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspace.workspace",
                    ),
                ),
            ],
            options={
                "unique_together": {("user_invite", "workspace")},
            },
        ),
    ]
