# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022 JWP Consulting GK
"""Add redeemed field to user invite."""
# Generated by Django 4.0.2 on 2022-03-09 07:52

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("user", "0008_userinvite"),
    ]

    operations = [
        migrations.AddField(
            model_name="userinvite",
            name="redeemed",
            field=models.BooleanField(
                default=False, help_text="Has this invite been redeemed?"
            ),
        ),
    ]
