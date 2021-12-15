"""Add timestamps to workspace models."""
# Generated by Django 4.0 on 2021-12-15 06:52

import datetime

from django.db import (
    migrations,
)
from django.utils.timezone import (
    utc,
)

import django_extensions.db.fields


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0003_workspaceboard"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="workspace",
            options={"get_latest_by": "modified"},
        ),
        migrations.AlterModelOptions(
            name="workspaceboard",
            options={"get_latest_by": "modified"},
        ),
        migrations.AlterModelOptions(
            name="workspaceuser",
            options={"get_latest_by": "modified"},
        ),
        migrations.AddField(
            model_name="workspace",
            name="created",
            field=django_extensions.db.fields.CreationDateTimeField(
                auto_now_add=True,
                default=datetime.datetime(
                    2021, 12, 15, 6, 52, 28, 779635, tzinfo=utc
                ),
                verbose_name="created",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="workspace",
            name="modified",
            field=django_extensions.db.fields.ModificationDateTimeField(
                auto_now=True, verbose_name="modified"
            ),
        ),
        migrations.AddField(
            model_name="workspaceboard",
            name="created",
            field=django_extensions.db.fields.CreationDateTimeField(
                auto_now_add=True,
                default=datetime.datetime(
                    2021, 12, 15, 6, 52, 32, 996331, tzinfo=utc
                ),
                verbose_name="created",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="workspaceboard",
            name="modified",
            field=django_extensions.db.fields.ModificationDateTimeField(
                auto_now=True, verbose_name="modified"
            ),
        ),
        migrations.AddField(
            model_name="workspaceuser",
            name="created",
            field=django_extensions.db.fields.CreationDateTimeField(
                auto_now_add=True,
                default=datetime.datetime(
                    2021, 12, 15, 6, 52, 37, 906080, tzinfo=utc
                ),
                verbose_name="created",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="workspaceuser",
            name="modified",
            field=django_extensions.db.fields.ModificationDateTimeField(
                auto_now=True, verbose_name="modified"
            ),
        ),
    ]
