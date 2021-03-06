"""Create task."""
# Generated by Django 3.2.10 on 2021-12-16 05:28

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)

import django_extensions.db.fields


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0007_alter_workspaceboardsection_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
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
                    "order",
                    models.PositiveIntegerField(
                        db_index=True, editable=False, verbose_name="order"
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
                    "title",
                    models.CharField(max_length=255, verbose_name="title"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="description"
                    ),
                ),
                (
                    "workspace_board_section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="workspace.workspaceboardsection",
                    ),
                ),
            ],
            options={
                "ordering": ("workspace_board_section", "order"),
            },
        ),
    ]
