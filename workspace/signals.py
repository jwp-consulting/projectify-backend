"""Workspace signals."""
import logging

from django.db import (
    transaction,
)
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import (
    receiver,
)

from asgiref.sync import (
    async_to_sync,
)
from channels.layers import (
    get_channel_layer,
)

from user.signal_defs import (
    user_invitation_redeemed,
)

from . import (
    models,
    signal_defs,
)


logger = logging.getLogger(__name__)


@receiver(signal_defs.workspace_user_invited)
def send_invitation_email(instance, **kwargs):
    """Send email when workspace user is invited."""
    # Avoid circular import
    from . import (
        emails,
    )

    email = emails.WorkspaceUserInviteEmail(instance)
    email.send()


@receiver(post_save, sender=models.Workspace)
def workspace_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": uuid,
        },
    )


@receiver(post_delete, sender=models.Workspace)
def workspace_deleted(sender, instance, **kwargs):
    """Broadcast changes upon workspace delete."""
    uuid = str(instance.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": uuid,
        },
    )


@receiver(post_save, sender=models.Label)
def label_saved(sender, instance, **kwargs):
    """Broadcast changes upon label save."""
    workspace_uuid = str(instance.workspace.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-{workspace_uuid}",
        {
            "type": "workspace.change",
            "uuid": workspace_uuid,
        },
    )


@receiver(post_delete, sender=models.Label)
def label_deleted(sender, instance, **kwargs):
    """Broadcast changes upon label delete."""
    workspace_uuid = str(instance.workspace.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-{workspace_uuid}",
        {
            "type": "workspace.change",
            "uuid": workspace_uuid,
        },
    )


@receiver(post_save, sender=models.WorkspaceUser)
def workspace_user_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.workspace.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": uuid,
        },
    )


@receiver(post_delete, sender=models.WorkspaceUser)
def workspace_user_delete(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.workspace.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": uuid,
        },
    )


@receiver(post_save, sender=models.WorkspaceBoard)
def workspace_board_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.uuid)
    workspace_uuid = str(instance.workspace.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )
    async_to_sync(channel_layer.group_send)(
        f"workspace-{workspace_uuid}",
        {
            "type": "workspace.change",
            "uuid": workspace_uuid,
        },
    )


@receiver(post_delete, sender=models.WorkspaceBoard)
def workspace_board_deleted(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.uuid)
    workspace_uuid = str(instance.workspace.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )
    async_to_sync(channel_layer.group_send)(
        f"workspace-{workspace_uuid}",
        {
            "type": "workspace.change",
            "uuid": workspace_uuid,
        },
    )


@receiver(post_save, sender=models.WorkspaceBoardSection)
def workspace_board_section_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    workspace_board = instance.workspace_board
    uuid = str(workspace_board.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )


@receiver(post_delete, sender=models.WorkspaceBoardSection)
def workspace_board_section_deleted(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.workspace_board.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )


@receiver(post_save, sender=models.Task)
def task_saved(sender, instance, **kwargs):
    # """Broadcast changes."""
    # workspace_board = instance.workspace_board_section.workspace_board
    # uuid = str(workspace_board.uuid)
    # task_uuid = str(instance.uuid)
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_send)(
    #     f"workspace-board-{uuid}",
    #     {
    #         "type": "workspace.board.change",
    #         "uuid": uuid,
    #     },
    # )
    # async_to_sync(channel_layer.group_send)(
    #     f"task-{task_uuid}",
    #     {
    #         "type": "task.change",
    #         "uuid": task_uuid,
    #     },
    # )
    from django_eventstream import send_event

    print("SENDING EVENT")
    send_event("test", "message", {"text": "TASK SAVED"})


@receiver(post_delete, sender=models.Task)
def task_deleted(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.workspace_board_section.workspace_board.uuid)
    task_uuid = str(instance.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"task-{task_uuid}",
        {
            "type": "task.change",
            "uuid": task_uuid,
        },
    )
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )


@receiver(post_save, sender=models.TaskLabel)
def task_label_saved(sender, instance, **kwargs):
    """Broadcast changes upon task label save."""
    task_uuid = str(instance.task.uuid)
    workspace_board_uuid = str(
        instance.task.workspace_board_section.workspace_board.uuid,
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"task-{task_uuid}",
        {
            "type": "task.change",
            "uuid": task_uuid,
        },
    )
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{workspace_board_uuid}",
        {
            "type": "workspace.board.change",
            "uuid": workspace_board_uuid,
        },
    )


@receiver(post_delete, sender=models.TaskLabel)
def task_label_deleted(sender, instance, **kwargs):
    """Broadcast changes upon task label delete."""
    task_uuid = str(instance.task.uuid)
    workspace_board_uuid = str(
        instance.task.workspace_board_section.workspace_board.uuid,
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"task-{task_uuid}",
        {
            "type": "task.change",
            "uuid": task_uuid,
        },
    )
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{workspace_board_uuid}",
        {
            "type": "workspace.board.change",
            "uuid": workspace_board_uuid,
        },
    )


@receiver(post_save, sender=models.SubTask)
def sub_task_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    workspace_board = instance.task.workspace_board_section.workspace_board
    uuid = str(workspace_board.uuid)
    task_uuid = str(instance.task.uuid)
    channel_layer = get_channel_layer()
    logger.info("async_to_sync")
    fn = async_to_sync(channel_layer.group_send)
    logger.info("About to group_send workspace.board.change")
    fn(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )
    logger.info("About to group_send task.change")
    async_to_sync(channel_layer.group_send)(
        f"task-{task_uuid}",
        {
            "type": "task.change",
            "uuid": task_uuid,
        },
    )


@receiver(post_delete, sender=models.SubTask)
def sub_task_deleted(sender, instance, **kwargs):
    """Broadcast changes."""
    task_uuid = str(instance.task.uuid)
    uuid = str(instance.task.workspace_board_section.workspace_board.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"task-{task_uuid}",
        {
            "type": "task.change",
            "uuid": task_uuid,
        },
    )
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )


@receiver(post_save, sender=models.ChatMessage)
def chat_message_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.task.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"task-{uuid}",
        {
            "type": "task.change",
            "uuid": uuid,
        },
    )


@receiver(post_delete, sender=models.ChatMessage)
def chat_message_deleted(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.task.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"task-{uuid}",
        {
            "type": "task.change",
            "uuid": uuid,
        },
    )


@receiver(user_invitation_redeemed)
@transaction.atomic
def redeem_workspace_invitations(user, instance, **kwargs):
    """Redeem workspace invitations."""
    qs = models.WorkspaceUserInvite.objects.filter(
        user_invite__user=user,
    )
    for invite in qs:
        invite.workspace.add_user(user)
        invite.redeem()
