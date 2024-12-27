# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022 JWP Consulting GK
"""Add workspace user author to chat message."""
# Generated by Django 4.0.4 on 2022-06-30 04:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0045_rename_assignee_workspace_user_task_assignee"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatmessage",
            name="author_workspace_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="workspace.workspaceuser",
            ),
        ),
    ]
