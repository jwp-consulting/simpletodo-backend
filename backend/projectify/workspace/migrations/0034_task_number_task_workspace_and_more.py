# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Generated by Django 4.0.2 on 2022-06-16 21:42."""

import django.db.models.constraints
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0033_subtask_unique_sub_task_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="number",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name="task",
            name="workspace",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="workspace.workspace",
            ),
        ),
        migrations.AddField(
            model_name="workspace",
            name="highest_task_number",
            field=models.IntegerField(default=0),
        ),
        migrations.AddConstraint(
            model_name="task",
            constraint=models.UniqueConstraint(
                deferrable=django.db.models.constraints.Deferrable["DEFERRED"],
                fields=("workspace", "number"),
                name="unique_task_number",
            ),
        ),
    ]
