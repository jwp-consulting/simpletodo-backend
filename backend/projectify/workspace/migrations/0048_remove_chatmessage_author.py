# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022 JWP Consulting GK
"""Remove author field from chat message."""
# Generated by Django 4.0.4 on 2022-06-30 05:30

from django.db import migrations


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0047_populate_chatmessage_author_workspace_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chatmessage",
            name="author",
        ),
    ]
