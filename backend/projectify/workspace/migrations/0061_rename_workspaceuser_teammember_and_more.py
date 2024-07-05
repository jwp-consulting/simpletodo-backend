# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2024 JWP Consulting GK
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
"""Rename WorkspaceUser models, update foreign key in task."""

# Generated by Django 4.2.10 on 2024-03-18 18:35
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("user", "0013_user_unconfirmed_email_previousemailaddress"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("workspace", "0060_alter_workspaceuser_role"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="WorkspaceUser",
            new_name="TeamMember",
        ),
        migrations.RenameModel(
            old_name="WorkspaceUserInvite",
            new_name="TeamMemberInvite",
        ),
        migrations.AlterField(
            model_name="task",
            name="assignee",
            field=models.ForeignKey(
                blank=True,
                help_text="Team member this task is assigned to.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="workspace.teammember",
            ),
        ),
    ]
