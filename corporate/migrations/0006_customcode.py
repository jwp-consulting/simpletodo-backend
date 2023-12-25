# Generated by Django 4.2.7 on 2023-12-25 00:27
"""Create CustomCode model."""

import django.db.models.deletion
from django.db import migrations, models

import django_extensions.db.fields


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("corporate", "0005_alter_customer_subscription_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        db_index=True, max_length=200, unique=True
                    ),
                ),
                (
                    "used",
                    models.DateTimeField(
                        blank=True, editable=False, null=True
                    ),
                ),
                ("seats", models.PositiveIntegerField()),
                (
                    "customer",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="corporate.customer",
                    ),
                ),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
    ]
