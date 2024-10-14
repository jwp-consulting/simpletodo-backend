# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022 JWP Consulting GK
"""Rename task assignee field."""
# Generated by Django 4.0.4 on 2022-06-29 14:47

from django.db import (
    migrations,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0044_remove_task_assignee"),
    ]

    operations = [
        migrations.RenameField(
            model_name="task",
            old_name="assignee_workspace_user",
            new_name="assignee",
        ),
    ]
