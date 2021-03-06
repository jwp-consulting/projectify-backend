"""Populate chat message author_workspace_user field."""
# Generated by Django 4.0.4 on 2022-06-30 04:28

from django.db import (
    migrations,
)


def add_author_workspace_user_to_chat_message(apps, schema_editor):
    """Populate author_workspace_user field in chat messages."""
    ChatMessage = apps.get_model("workspace", "ChatMessage")
    WorkspaceUser = apps.get_model("workspace", "WorkspaceUser")
    for chat_message in ChatMessage.objects.all():
        try:
            ws_user = WorkspaceUser.objects.get(
                workspace=chat_message.task.workspace,
                user=chat_message.author,
            )
        except WorkspaceUser.DoesNotExist:
            ws_user = None
        chat_message.author_workspace_user = ws_user
        chat_message.save()


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0046_chatmessage_author_workspace_user"),
    ]

    operations = [
        migrations.RunPython(add_author_workspace_user_to_chat_message),
    ]
