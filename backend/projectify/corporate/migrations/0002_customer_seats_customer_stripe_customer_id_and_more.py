# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022 JWP Consulting GK
"""Generated by Django 4.0.2 on 2022-05-27 18:50."""

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("corporate", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="seats",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="customer",
            name="stripe_customer_id",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="customer",
            name="subscription_status",
            field=models.CharField(
                choices=[
                    ("ACT", "Active"),
                    ("UNP", "Unpaid"),
                    ("CAN", "Canceled"),
                ],
                default="UNP",
                max_length=3,
            ),
        ),
        migrations.AddField(
            model_name="customer",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True
            ),
        ),
    ]
