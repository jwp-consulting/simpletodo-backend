# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022 JWP Consulting GK
"""Add full_name field to user."""
# Generated by Django 3.2.11 on 2022-02-15 07:57

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("user", "0006_user_profile_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="full_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
