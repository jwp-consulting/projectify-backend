"""
Update sub task.

1) Add order_with_respect_to option.
2) Add unique order constraint.
3) Remove order field
"""
# Generated by Django 4.0.2 on 2022-05-27 02:17

import django.db.models.constraints
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0030_alter_task_assignee"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subtask",
            options={},
        ),
        migrations.AlterOrderWithRespectTo(
            name="subtask",
            order_with_respect_to="task",
        ),
        migrations.AddConstraint(
            model_name="subtask",
            constraint=models.UniqueConstraint(
                deferrable=django.db.models.constraints.Deferrable["DEFERRED"],
                fields=("task", "_order"),
                name="unique_sub_task_order",
            ),
        ),
        migrations.RemoveField(
            model_name="subtask",
            name="order",
        ),
    ]
