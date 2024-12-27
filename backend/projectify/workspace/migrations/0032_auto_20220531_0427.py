# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Ensure SubTask _order is unique."""
# Generated by Django 4.0.2 on 2022-05-31 04:27

from typing import TYPE_CHECKING, cast

from django.apps.registry import Apps
from django.db import migrations

if TYPE_CHECKING:
    from projectify.workspace.models import Task as _Task


def ensure_correct_order(apps: Apps, schema_editor: object) -> None:
    """Correct _order field."""
    Task = cast("_Task", apps.get_model("workspace", "Task"))
    for task in Task.objects.all():
        for i, sub_task in enumerate(task.subtask_set.all()):
            sub_task._order = i
            sub_task.save()
            task.save()


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0031_alter_subtask_options_and_more"),
    ]

    operations = [
        migrations.RunPython(ensure_correct_order),
    ]
