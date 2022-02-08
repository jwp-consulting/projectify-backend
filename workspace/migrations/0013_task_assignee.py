"""Add assignee field to Task."""
# Generated by Django 3.2.11 on 2022-02-08 02:21

import django.db.models.deletion
from django.conf import (
    settings,
)
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("workspace", "0012_auto_20220128_1034"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="assignee",
            field=models.ForeignKey(
                blank=True,
                help_text="User this task is assigned to.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]