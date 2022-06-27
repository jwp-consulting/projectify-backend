"""Test workspace models."""
from django import (
    db,
)
from django.contrib.auth import (
    get_user_model,
)
from django.utils import (
    timezone,
)

import pytest

from .. import (
    factory,
    models,
)


@pytest.mark.django_db
class TestWorkspaceManager:
    """Test Workspace manager."""

    def test_get_for_user(self, workspace_user, user, other_user):
        """Test getting workspaces for user."""
        workspace = workspace_user.workspace
        factory.WorkspaceFactory(add_users=[other_user])
        assert list(models.Workspace.objects.get_for_user(user)) == [workspace]

    def test_get_for_user_and_uuid(self, workspace_user, workspace, user):
        """Test getting workspace for user and uuid."""
        assert (
            models.Workspace.objects.get_for_user_and_uuid(
                user,
                workspace.uuid,
            )
            == workspace
        )


@pytest.mark.django_db
class TestWorkspace:
    """Test Workspace."""

    def test_factory(self, workspace):
        """Assert that the creates."""
        assert workspace

    def test_add_workspace_board(self, workspace):
        """Test adding a workspace board."""
        assert workspace.workspaceboard_set.count() == 0
        board = workspace.add_workspace_board("foo", "bar")
        assert workspace.workspaceboard_set.count() == 1
        board2 = workspace.add_workspace_board("foo", "bar")
        assert workspace.workspaceboard_set.count() == 2
        assert list(workspace.workspaceboard_set.all()) == [
            board,
            board2,
        ]

    def test_add_user(self, workspace, user):
        """Test adding a user."""
        assert workspace.users.count() == 0
        workspace.add_user(user)
        assert workspace.users.count() == 1

    def test_add_user_twice(self, workspace, workspace_user, user):
        """Test that adding a user twice won't work."""
        with pytest.raises(db.IntegrityError):
            workspace.add_user(user)

    def test_remove_user(self, workspace, workspace_user, user):
        """Test remove_user."""
        assert workspace.users.count() == 1
        workspace.remove_user(user)
        assert workspace.users.count() == 0

    def test_remove_user_when_assigned(
        self,
        workspace,
        task,
        workspace_user,
        user,
    ):
        """Assert that the user is removed when removing the workspace user."""
        task.assign_to(user)
        workspace.remove_user(user)
        task.refresh_from_db()
        assert task.assignee is None

    def test_invite_user(self, workspace, mailoutbox):
        """Test inviting a user."""
        workspace_user_invite = workspace.invite_user("hello@example.com")
        assert workspace_user_invite.workspace == workspace
        assert len(mailoutbox) == 1

    def test_inviting_twice(self, workspace):
        """Test that inviting twice won't work."""
        workspace.invite_user("hello@example.com")
        with pytest.raises(ValueError):
            workspace.invite_user("hello@example.com")

    def test_inviting_workspace_user(self, workspace, workspace_user):
        """Test that inviting a pre-existing user won't work."""
        with pytest.raises(ValueError):
            workspace.invite_user(workspace_user.user.email)

    def test_inviting_user(self, workspace, user):
        """
        Test that inviting a user won't work.

        This is already tested in user/test/test_models.py
        """
        with pytest.raises(ValueError):
            workspace.invite_user(user.email)

    def test_uninviting_user(self, workspace):
        """Test uninviting a user."""
        workspace.invite_user("hello@example.com")
        assert workspace.workspaceuserinvite_set.count() == 1
        workspace.uninvite_user("hello@example.com")
        assert workspace.workspaceuserinvite_set.count() == 0

    def test_increment_highest_task_number(self, workspace):
        """Test set_highest_task_number."""
        num = workspace.highest_task_number
        new = workspace.increment_highest_task_number()
        assert new == num + 1
        workspace.refresh_from_db()
        assert workspace.highest_task_number == new

    def test_has_at_least_role(self, workspace, workspace_user):
        """Test has_at_least_role."""
        assert workspace.has_at_least_role(
            workspace_user,
            models.WorkspaceUserRoles.OWNER,
        )
        workspace_user.assign_role(models.WorkspaceUserRoles.OBSERVER)
        assert workspace.has_at_least_role(
            workspace_user,
            models.WorkspaceUserRoles.OBSERVER,
        )
        assert not workspace.has_at_least_role(
            workspace_user,
            models.WorkspaceUserRoles.OWNER,
        )

    def test_has_at_least_role_other_workspace(
        self, other_workspace, workspace_user
    ):
        """Test has_at_least_role with a different workspace."""
        assert not other_workspace.has_at_least_role(
            workspace_user,
            models.WorkspaceUserRoles.OBSERVER,
        )

    def test_workspace(self, workspace):
        """Test workspace property."""
        assert workspace.workspace == workspace


@pytest.mark.django_db
class TestWorkspaceUserInviteQuerySet:
    """Test WorkspaceUserInviteQuerySet."""

    def test_filter_by_workspace_pks(self, workspace, workspace_user_invite):
        """Test filter_by_workspace_pks."""
        qs = models.WorkspaceUserInvite.objects.filter_by_workspace_pks(
            [workspace.pk],
        )
        assert list(qs) == [workspace_user_invite]

    def test_filter_by_redeemed(self, workspace, workspace_user_invite):
        """Test filter_by_redeemed."""
        qs = models.WorkspaceUserInvite.objects.filter_by_redeemed(False)
        assert qs.count() == 1
        workspace_user_invite.redeem()
        assert qs.count() == 0
        qs = models.WorkspaceUserInvite.objects.filter_by_redeemed(True)
        assert qs.count() == 1


@pytest.mark.django_db
class TestWorkspaceUserInvite:
    """Test workspace user invite."""

    def test_factory(self, workspace_user_invite):
        """Test factory."""
        assert workspace_user_invite

    def test_redeem(self, workspace_user_invite):
        """Test redeeming."""
        workspace_user_invite.redeem()
        assert workspace_user_invite.redeem

    def test_redeeming_twice(self, workspace_user_invite):
        """Test redeeming twice."""
        workspace_user_invite.redeem()
        with pytest.raises(AssertionError):
            workspace_user_invite.redeem()

    def test_workspace(self, workspace_user_invite, workspace):
        """Test workspace property."""
        assert workspace_user_invite.workspace == workspace


@pytest.mark.django_db
class TestWorkspaceUserManager:
    """Test workspace user manager."""

    def test_filter_by_workspace_pks(self, workspace_user, workspace):
        """Test filter_by_workspace_pks."""
        qs = models.WorkspaceUser.objects.filter_by_workspace_pks(
            [workspace.pk],
        )
        assert list(qs) == [workspace_user]

    def test_get_by_workspace_and_user(self, workspace, user, workspace_user):
        """Test get_by_workspace_and_user."""
        assert (
            models.WorkspaceUser.objects.get_by_workspace_and_user(
                workspace,
                user,
            )
            == workspace_user
        )


@pytest.mark.django_db
class TestWorkspaceUser:
    """Test WorkspaceUser."""

    def test_factory(self, workspace_user):
        """Test that the default rule is observer."""
        assert workspace_user.role == models.WorkspaceUserRoles.OWNER

    def test_workspace(self, workspace, workspace_user):
        """Test workspace property."""
        assert workspace_user.workspace == workspace

    def test_assign_role(self, workspace_user):
        """Test assign_role."""
        workspace_user.assign_role(models.WorkspaceUserRoles.OWNER)
        workspace_user.refresh_from_db()
        assert workspace_user.role == models.WorkspaceUserRoles.OWNER


@pytest.mark.django_db
class TestWorkspaceBoardManager:
    """Test WorkspaceBoard manager."""

    def test_filter_by_workspace_pks(self, workspace, workspace_board):
        """Test filter_by_workspace_pks."""
        qs = models.WorkspaceBoard.objects.filter_by_workspace_pks(
            [workspace.pk],
        )
        assert list(qs) == [workspace_board]

    def test_get_for_user_and_uuid(
        self,
        workspace,
        workspace_board,
        workspace_user,
    ):
        """Test that the workspace board is retrieved correctly."""
        factory.WorkspaceUserFactory(
            workspace=workspace,
        )
        assert workspace_board.workspace.users.count() == 2
        actual = models.WorkspaceBoard.objects.get_for_user_and_uuid(
            workspace_user.user,
            workspace_board.uuid,
        )
        assert actual == workspace_board

    def test_filter_by_archived(self, workspace_board):
        """Test filter_by_archived."""
        qs_archived = models.WorkspaceBoard.objects.filter_by_archived(True)
        qs_unarchived = models.WorkspaceBoard.objects.filter_by_archived(False)
        assert qs_archived.count() == 0
        assert qs_unarchived.count() == 1
        workspace_board.archive()
        assert qs_archived.count() == 1
        assert qs_unarchived.count() == 0
        workspace_board.unarchive()
        assert qs_archived.count() == 0
        assert qs_unarchived.count() == 1


@pytest.mark.django_db
class TestWorkspaceBoard:
    """Test WorkspaceBoard."""

    def test_factory(self, workspace, workspace_board):
        """Test workspace board creation works."""
        assert workspace_board.workspace == workspace

    def test_add_workspace_board_section(self, workspace_board):
        """Test workspace board section creation."""
        assert workspace_board.workspaceboardsection_set.count() == 0
        section = workspace_board.add_workspace_board_section(
            "hello",
            "world",
        )
        assert workspace_board.workspaceboardsection_set.count() == 1
        section2 = workspace_board.add_workspace_board_section(
            "hello",
            "world",
        )
        assert workspace_board.workspaceboardsection_set.count() == 2
        assert list(workspace_board.workspaceboardsection_set.all()) == [
            section,
            section2,
        ]

    def test_archive(self, workspace_board):
        """Test archive method."""
        assert workspace_board.archived is None
        workspace_board.archive()
        assert workspace_board.archived is not None

    def test_unarchive(self, workspace_board):
        """Test unarchive method."""
        assert workspace_board.archived is None
        workspace_board.archive()
        assert workspace_board.archived is not None
        workspace_board.unarchive()
        assert workspace_board.archived is None

    def test_workspace(self, workspace, workspace_board):
        """Test workspace property."""
        assert workspace_board.workspace == workspace


@pytest.mark.django_db
class TestWorkspaceBoardSectionManager:
    """Test WorkspaceBoardSection manager."""

    def test_filter_by_workspace_board_pks(
        self,
        workspace_board,
        workspace_board_section,
    ):
        """Test filter_by_workspace_board_pks."""
        objects = models.WorkspaceBoardSection.objects
        qs = objects.filter_by_workspace_board_pks(
            [workspace_board.pk],
        )
        assert list(qs) == [workspace_board_section]

    def test_get_for_user_and_uuid(
        self,
        workspace,
        workspace_board_section,
        workspace_user,
    ):
        """Test getting for user and uuid."""
        factory.WorkspaceUserFactory(
            workspace=workspace,
        )
        actual = models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
            workspace_user.user,
            workspace_board_section.uuid,
        )
        assert actual == workspace_board_section


@pytest.mark.django_db
class TestWorkspaceBoardSection:
    """Test WorkspaceBoardSection."""

    def test_factory(self, workspace_board_section, workspace_board):
        """Test workspace board section creation works."""
        assert workspace_board_section.workspace_board == workspace_board

    def test_add_task(self, workspace_board_section):
        """Test adding tasks to a workspace board."""
        assert workspace_board_section.task_set.count() == 0
        task = workspace_board_section.add_task(title="foo", description="bar")
        assert workspace_board_section.task_set.count() == 1
        task2 = workspace_board_section.add_task(
            title="foo2",
            description="bar2",
        )
        assert workspace_board_section.task_set.count() == 2
        assert list(workspace_board_section.task_set.all()) == [task, task2]

    def test_add_task_deadline(self, workspace_board_section):
        """Test adding a task with a deadline."""
        task = workspace_board_section.add_task(
            title="foo",
            description="bar",
            deadline=timezone.now(),
        )
        assert task.deadline is not None

    def test_moving_section(self, workspace_board, workspace_board_section):
        """Test moving a section around."""
        other_section = factory.WorkspaceBoardSectionFactory(
            workspace_board=workspace_board,
        )
        other_other_section = factory.WorkspaceBoardSectionFactory(
            workspace_board=workspace_board,
        )
        assert list(workspace_board.workspaceboardsection_set.all()) == [
            workspace_board_section,
            other_section,
            other_other_section,
        ]
        workspace_board_section.move_to(0)
        assert list(workspace_board.workspaceboardsection_set.all()) == [
            workspace_board_section,
            other_section,
            other_other_section,
        ]
        workspace_board_section.move_to(2)
        assert list(workspace_board.workspaceboardsection_set.all()) == [
            other_section,
            other_other_section,
            workspace_board_section,
        ]
        workspace_board_section.move_to(1)
        assert list(workspace_board.workspaceboardsection_set.all()) == [
            other_section,
            workspace_board_section,
            other_other_section,
        ]

    def test_moving_empty_section(
        self,
        workspace_board,
        workspace_board_section,
    ):
        """Test moving when there are no other sections."""
        assert list(workspace_board.workspaceboardsection_set.all()) == [
            workspace_board_section,
        ]
        workspace_board_section.move_to(1)
        assert list(workspace_board.workspaceboardsection_set.all()) == [
            workspace_board_section,
        ]
        assert workspace_board_section._order == 0

    def test_workspace(self, workspace, workspace_board_section):
        """Test workspace property."""
        assert workspace_board_section.workspace == workspace


@pytest.mark.django_db
class TestTaskManager:
    """Test TaskManager."""

    def test_filter_by_workspace_board_section_pks(
        self, workspace_board_section, task
    ):
        """Test filter_by_workspace_board_section_pks."""
        qs = models.Task.objects.filter_by_workspace_board_section_pks(
            [workspace_board_section.pk],
        )
        assert list(qs) == [task]

    def test_get_for_user_and_uuid(self, workspace, task, workspace_user):
        """Test get_for_user_and_uuid."""
        factory.WorkspaceUserFactory(
            workspace=workspace,
        )
        actual = models.Task.objects.get_for_user_and_uuid(
            workspace_user.user,
            task.uuid,
        )
        assert actual == task

    def test_duplicate_task(self, task):
        """Test task duplication."""
        new_task = models.Task.objects.duplicate_task(task)
        assert new_task.workspace_board_section == task.workspace_board_section
        assert new_task.title == task.title
        assert new_task.description == task.description


@pytest.mark.django_db
class TestTask:
    """Test Task."""

    def test_factory(
        self,
        workspace_board_section,
        workspace_user,
        task,
        user,
    ):
        """Test that workspace_board_section is assigned correctly."""
        assert task.workspace_board_section == workspace_board_section
        assert task.assignee == user
        assert task.deadline is not None

    def test_moving_task_within_section(
        self,
        workspace_board_section,
        task,
    ):
        """Test moving a task around within the same section."""
        other_task = factory.TaskFactory(
            workspace_board_section=workspace_board_section
        )
        assert list(workspace_board_section.task_set.all()) == [
            task,
            other_task,
        ]
        task.move_to(workspace_board_section, 1)
        assert list(workspace_board_section.task_set.all()) == [
            other_task,
            task,
        ]

    def test_moving_task_to_other_section(
        self, workspace_board, workspace_board_section, task
    ):
        """Test moving a task around to another section."""
        other_task = factory.TaskFactory(
            workspace_board_section=workspace_board_section
        )
        assert list(workspace_board_section.task_set.all()) == [
            task,
            other_task,
        ]
        other_section = factory.WorkspaceBoardSectionFactory(
            workspace_board=workspace_board
        )
        other_section_task = factory.TaskFactory(
            workspace_board_section=other_section,
        )
        assert list(other_section.task_set.all()) == [
            other_section_task,
        ]
        task.move_to(other_section, 0)
        assert list(other_section.task_set.all()) == [
            task,
            other_section_task,
        ]

    def test_moving_task_to_empty_section(
        self, workspace_board, workspace_board_section, task
    ):
        """
        Test what happens if we move it into an empty section.

        We also see what happens when the id is set too high.
        """
        other_section = factory.WorkspaceBoardSectionFactory(
            workspace_board=workspace_board
        )
        task.move_to(other_section, 1)
        assert list(other_section.task_set.all()) == [
            task,
        ]
        task.refresh_from_db()
        assert task._order == 0

    def test_add_sub_task(self, task):
        """Test adding a sub task."""
        assert task.subtask_set.count() == 0
        task.add_sub_task("foo", "bar")
        assert task.subtask_set.count() == 1

    def test_add_chat_message(self, task, user, workspace_user):
        """Test adding a chat message."""
        assert task.chatmessage_set.count() == 0
        task.add_chat_message("Hello", user)
        assert task.chatmessage_set.count() == 1

    def test_assign_to(
        self,
        workspace,
        task,
        other_user,
        other_workspace_user,
    ):
        """Test assigning to a different workspace's user."""
        task.assign_to(other_user)
        assert task.assignee == other_user

    def test_assign_then_delete_user(self, task, workspace_user):
        """Assert that nothing happens to the task if the user is gone."""
        task.assign_to(workspace_user.user)
        workspace_user.user.delete()
        task.refresh_from_db()
        assert task.assignee is None

    def test_assign_outside_of_workspace(self, workspace, task, other_user):
        """Test assigning to a different workspace's user."""
        # This time do not create a workspace_user
        with pytest.raises(get_user_model().DoesNotExist):
            task.assign_to(other_user)

    def test_assign_none(self, workspace, task, workspace_user, user):
        """Test assigning to no user."""
        task.assign_to(user)
        task.assign_to(None)
        task.refresh_from_db()
        assert task.assignee is None

    def test_get_next_section(self, workspace_board, task):
        """Test getting the next section."""
        section = factory.WorkspaceBoardSectionFactory(
            workspace_board=workspace_board,
        )
        assert task.get_next_section() == section

    def test_get_next_section_no_next_section(self, workspace_board, task):
        """Test getting the next section when there is none."""
        with pytest.raises(models.WorkspaceBoardSection.DoesNotExist):
            task.get_next_section()

    def test_add_label(self, task, label):
        """Test adding a label."""
        assert task.tasklabel_set.count() == 0
        task.add_label(label)
        assert task.tasklabel_set.count() == 1
        # This is idempotent
        task.add_label(label)
        assert task.tasklabel_set.count() == 1

    def test_remove_label(self, task, label):
        """Test removing a label."""
        task.add_label(label)
        assert task.tasklabel_set.count() == 1
        task.remove_label(label)
        assert task.tasklabel_set.count() == 0
        # This is idempotent
        task.remove_label(label)
        assert task.tasklabel_set.count() == 0

    def test_task_number(self, task, other_task):
        """Test unique task number."""
        assert other_task.number == task.number + 1
        task.workspace.refresh_from_db()
        assert task.workspace.highest_task_number == other_task.number

    def test_save(self, task):
        """Test saving and assert number does not change."""
        num = task.number
        task.save()
        assert task.number == num

    def test_save_no_number(self, task, workspace):
        """Test saving with no number."""
        task.number = None
        task.save()
        workspace.refresh_from_db()
        assert task.number == workspace.highest_task_number


@pytest.mark.django_db
class TestLabelManager:
    """Test Label queryset/manager."""

    def test_filter_by_workspace_pks(self, label, workspace):
        """Test filter_by_workspace_pks."""
        qs = models.Label.objects.filter_by_workspace_pks([workspace.pk])
        labels = [label]
        assert list(qs) == labels

    def test_get_for_user_and_uuid(self, label, workspace_user):
        """Test get_for_user_and_uuid."""
        assert (
            models.Label.objects.get_for_user_and_uuid(
                workspace_user.user,
                label.uuid,
            )
            == label
        )


@pytest.mark.django_db
class TestLabel:
    """Test Label model."""

    def test_factory(self, label):
        """Test factory."""
        assert label.color

    def test_workspace(self, workspace, label):
        """Test workspace property."""
        assert label.workspace == workspace


@pytest.mark.django_db
class TestLabelQuerySet:
    """Test LabelQuerySet."""

    def test_filter_by_task_pks(self, label, task):
        """Test filter_by_task_pks."""
        task_label = task.add_label(label)
        qs = models.TaskLabel.objects.filter_by_task_pks([task.pk])
        task_labels = [task_label]
        assert list(qs) == task_labels


@pytest.mark.django_db
class TestTaskLabel:
    """Test TaskLabel model."""

    def test_factory(self, task_label, task, label):
        """Test factory."""
        assert task_label.task == task
        assert task_label.label == label

    def test_workspace(self, workspace, task_label):
        """Test workspace property."""
        assert task_label.workspace == workspace


@pytest.mark.django_db
class TestSubTaskManager:
    """Test SubTask manager."""

    def test_filter_by_task_pks(self, task, sub_task):
        """Test filter_by_task_pks."""
        qs = models.SubTask.objects.filter_by_task_pks([task.pk])
        assert list(qs) == [sub_task]

    def test_get_for_user_and_uuid(self, sub_task, workspace_user):
        """Test get_for_user_and_uuid."""
        assert (
            models.SubTask.objects.get_for_user_and_uuid(
                workspace_user.user,
                sub_task.uuid,
            )
            == sub_task
        )


@pytest.mark.django_db
class TestSubTask:
    """Test SubTask."""

    def test_factory(self, task, sub_task):
        """Test that sub task correctly belongs to task."""
        assert sub_task.task == task

    def test_moving_sub_task(self, task, sub_task):
        """Test moving a sub task around."""
        other_sub_task = factory.SubTaskFactory(
            task=task,
        )
        other_other_sub_task = factory.SubTaskFactory(
            task=task,
        )
        assert list(task.subtask_set.all()) == [
            sub_task,
            other_sub_task,
            other_other_sub_task,
        ]
        sub_task.move_to(0)
        assert list(task.subtask_set.all()) == [
            sub_task,
            other_sub_task,
            other_other_sub_task,
        ]
        sub_task.move_to(2)
        assert list(task.subtask_set.all()) == [
            other_sub_task,
            other_other_sub_task,
            sub_task,
        ]
        sub_task.move_to(1)
        assert list(task.subtask_set.all()) == [
            other_sub_task,
            sub_task,
            other_other_sub_task,
        ]

    def test_moving_within_empty_task(
        self,
        task,
        sub_task,
    ):
        """Test moving when there are no other sub tasks."""
        assert list(task.subtask_set.all()) == [
            sub_task,
        ]
        sub_task.move_to(1)
        assert list(task.subtask_set.all()) == [
            sub_task,
        ]
        assert sub_task._order == 0

    def test_workspace(self, workspace, sub_task):
        """Test workspace property."""
        assert sub_task.workspace == workspace


@pytest.mark.django_db
class TestChatMessageManager:
    """Test ChatMessage Manager."""

    def test_filter_by_task_pks(self, chat_message, task):
        """Test filter_by_task_pks."""
        qs = models.ChatMessage.objects.filter_by_task_pks([task.pk])
        assert list(qs) == [chat_message]

    def test_get_for_user_and_uuid(self, chat_message, workspace_user):
        """Test get_for_user_and_uuid."""
        assert (
            models.ChatMessage.objects.get_for_user_and_uuid(
                workspace_user.user,
                chat_message.uuid,
            )
            == chat_message
        )


@pytest.mark.django_db
class TestChatMessage:
    """Test ChatMessage."""

    def test_factory(self, workspace_user, chat_message):
        """Test that chat message belongs to user."""
        assert chat_message.author == workspace_user.user

    def test_workspace(self, workspace, chat_message):
        """Test workspace property."""
        assert chat_message.workspace == workspace


@pytest.mark.django_db
class TestNotifications:
    """Test notifications."""

    def test_task_assigned_notification(
        self, task, workspace_user, other_workspace_user
    ):
        """Test sending assignment notification."""
        # Use setter method to trigger notification
        task.assign_to(workspace_user.user, actor=other_workspace_user.user)
        notification = workspace_user.user.notifications.last().verb
        assert "assigned" in notification
        assert other_workspace_user.user.full_name in notification

    def test_task_moved_to_notification(
        self, workspace_board, task, workspace_user, other_workspace_user
    ):
        """Test notification for moving a task to another section."""
        other_section = factory.WorkspaceBoardSectionFactory(
            workspace_board=workspace_board
        )
        task.move_to(other_section, 0, actor=other_workspace_user.user)
        notification = workspace_user.user.notifications.last().verb
        assert "moved" in notification
        assert other_workspace_user.user.full_name in notification

    def test_deleted_task_notification(
        self, task, workspace_user, other_workspace_user
    ):
        """Test deleted task notification."""
        task.delete(actor=other_workspace_user.user)
        notification = workspace_user.user.notifications.last().verb
        assert "deleted" in notification
        assert other_workspace_user.user.full_name in notification
