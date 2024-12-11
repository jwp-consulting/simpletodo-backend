# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022 JWP Consulting GK
"""Make color an integer."""
# Generated by Django 4.0.2 on 2022-03-09 07:05

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0022_label_tasklabel_task_labels"),
    ]

    operations = [
        migrations.AlterField(
            model_name="label",
            name="color",
            field=models.PositiveBigIntegerField(
                default=0, help_text="Color index"
            ),
        ),
    ]
