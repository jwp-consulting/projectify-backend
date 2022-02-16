"""Workspace schema mutations."""
from django.contrib.auth import (
    get_user_model,
)

import graphene

from .. import (
    models,
)
from . import (
    types,
)


class AddWorkspaceBoardInput(graphene.InputObjectType):
    """Add workspace board input."""

    workspace_uuid = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)


class AddWorkspaceBoardMutation(graphene.Mutation):
    """Add workspace board mutation."""

    class Arguments:
        """Arguments."""

        input = AddWorkspaceBoardInput(required=True)

    workspace_board = graphene.Field(types.WorkspaceBoard)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        workspace = models.Workspace.objects.get_for_user_and_uuid(
            info.context.user,
            input.workspace_uuid,
        )
        workspace_board = workspace.add_workspace_board(
            title=input.title,
            description=input.description,
        )
        return cls(workspace_board)


class AddWorkspaceBoardSectionInput(graphene.InputObjectType):
    """Add workspace board section input."""

    workspace_board_uuid = graphene.ID(required=True)
    title = graphene.ID(required=True)
    description = graphene.ID(required=True)


class AddWorkspaceBoardSectionMutation(graphene.Mutation):
    """Add workspace board section mutation."""

    class Arguments:
        """Arguments."""

        input = AddWorkspaceBoardSectionInput(required=True)

    workspace_board_section = graphene.Field(types.WorkspaceBoardSection)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        workspace_board = models.WorkspaceBoard.objects.get_for_user_and_uuid(
            info.context.user,
            input.workspace_board_uuid,
        )
        workspace_board_section = workspace_board.add_workspace_board_section(
            title=input.title,
            description=input.description,
        )
        return cls(workspace_board_section)


class AddTaskMutationInput(graphene.InputObjectType):
    """Add task mutation input."""

    workspace_board_section_uuid = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)


class AddTaskMutation(graphene.Mutation):
    """Add task mutation."""

    class Arguments:
        """Arguments."""

        input = AddTaskMutationInput(required=True)

    task = graphene.Field(types.Task)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        workspace_board_section = (
            models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
                info.context.user,
                input.workspace_board_section_uuid,
            )
        )
        task = workspace_board_section.add_task(
            input.title,
            input.description,
        )
        return cls(task)


class AddSubTaskInput(graphene.InputObjectType):
    """Add sub task mutation input."""

    task_uuid = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)


class AddSubTaskMutation(graphene.Mutation):
    """Add subtask mutation."""

    class Arguments:
        """Arguments."""

        input = AddSubTaskInput(required=True)

    sub_task = graphene.Field(types.SubTask)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.task_uuid,
        )
        sub_task = task.add_sub_task(
            input.title,
            input.description,
        )
        return cls(sub_task)


class AddChatMessageInput(graphene.InputObjectType):
    """AddChatMessageMutation input."""

    task_uuid = graphene.ID(required=True)
    text = graphene.String(required=True)


class AddChatMessageMutation(graphene.Mutation):
    """Add ChatMessage mutation."""

    class Arguments:
        """Arguments."""

        input = AddChatMessageInput(required=True)

    chat_message = graphene.Field(types.ChatMessage)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.task_uuid,
        )
        chat_message = task.add_chat_message(
            text=input.text,
            author=info.context.user,
        )
        return cls(chat_message)


class ChangeSubTaskDoneInput(graphene.InputObjectType):
    """ChangeSubTaskDoneMutation input."""

    sub_task_uuid = graphene.ID(required=True)
    done = graphene.Boolean(required=True)


class ChangeSubTaskDoneMutation(graphene.Mutation):
    """Change sub task done state Mutation."""

    class Arguments:
        """Arguments."""

        input = ChangeSubTaskDoneInput(required=True)

    sub_task = graphene.Field(types.SubTask)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        sub_task = models.SubTask.objects.get_for_user_and_uuid(
            info.context.user,
            input.sub_task_uuid,
        )
        sub_task.done = input.done
        sub_task.save()
        return cls(sub_task)


class MoveWorkspaceBoardSectionInput(graphene.InputObjectType):
    """MoveWorkspaceBoardSectionMutation input."""

    workspace_board_section_uuid = graphene.ID(required=True)
    order = graphene.Int(required=True)


class MoveWorkspaceBoardSectionMutation(graphene.Mutation):
    """Move workspace board section mutation."""

    class Arguments:
        """Arguments."""

        input = MoveWorkspaceBoardSectionInput(required=True)

    workspace_board_section = graphene.Field(types.WorkspaceBoardSection)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        workspace_board_section = (
            models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
                info.context.user,
                input.workspace_board_section_uuid,
            )
        )
        workspace_board_section.move_to(input.order)
        return cls(workspace_board_section)


class MoveTaskInput(graphene.InputObjectType):
    """MoveTask mutation input."""

    task_uuid = graphene.ID(required=True)
    workspace_board_section_uuid = graphene.ID(required=True)
    order = graphene.Int(required=True)


class MoveTaskMutation(graphene.Mutation):
    """Move task mutation."""

    class Arguments:
        """Arguments."""

        input = MoveTaskInput(required=True)

    task = graphene.Field(types.Task)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        # Find workspace board section
        workspace_board_section = (
            models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
                info.context.user,
                input.workspace_board_section_uuid,
            )
        )
        # Find task
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.task_uuid,
        )
        # Reorder task
        task.move_to(workspace_board_section, input.order)
        # Return task
        return cls(task)


class AddUserToWorkspaceInput(graphene.InputObjectType):
    """Input for AddUserToWorkspaceMutation."""

    uuid = graphene.ID(required=True)
    email = graphene.String(required=True)


class AddUserToWorkspaceMutation(graphene.Mutation):
    """Mutation for adding users to workspaces."""

    class Arguments:
        """Arguments."""

        input = AddUserToWorkspaceInput(required=True)

    workspace = graphene.Field(types.Workspace)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        # Find workspace
        workspace = models.Workspace.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        # Find user
        User = get_user_model()
        user = User.objects.get_by_natural_key(input.email)
        # Assign user to workspace
        workspace.add_user(user)
        return cls(workspace)


class AssignTaskInput(graphene.InputObjectType):
    """Input for AssignTaskMutation."""

    uuid = graphene.ID(required=True)
    email = graphene.String(required=True)


class AssignTaskMutation(graphene.Mutation):
    """Mutation to assign tasks to users."""

    class Arguments:
        """Arguments."""

        input = AssignTaskInput(required=True)

    task = graphene.Field(types.Task)

    @classmethod
    def mutate(cls, root, info, input):
        """Assign task to user."""
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        User = get_user_model()
        assignee = User.objects.get_by_natural_key(input.email)
        task.assign_to(assignee)
        return cls(task)


class DuplicateTaskInput(graphene.InputObjectType):
    """DuplicateTaskMutation input."""

    uuid = graphene.ID(required=True)


class DuplicateTaskMutation(graphene.Mutation):
    """Duplicate task mutation."""

    class Arguments:
        """Arguments."""

        input = DuplicateTaskInput(required=True)

    task = graphene.Field(types.Task)

    @classmethod
    def mutate(cls, root, info, input):
        """Duplicate a task."""
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        new_task = models.Task.objects.duplicate_task(task)
        return cls(new_task)


# Update Mutations
class UpdateWorkspaceInput(graphene.InputObjectType):
    """Input for UpdateWorkspaceMutation."""

    uuid = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)


class UpdateWorkspaceMutation(graphene.Mutation):
    """Update workspace board mutation."""

    class Arguments:
        """Arguments."""

        input = UpdateWorkspaceInput(required=True)

    workspace = graphene.Field(types.Workspace)

    @classmethod
    def mutate(cls, root, info, input):
        """Update workspace."""
        workspace = models.Workspace.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        workspace.title = input.title
        workspace.description = input.description
        workspace.save()
        return cls(workspace)


class ArchiveWorkspaceBoardInput(graphene.InputObjectType):
    """Input for ArchiveWorkspaceBoardMutation."""

    uuid = graphene.ID(required=True)
    archived = graphene.Boolean(required=True)


class ArchiveWorkspaceBoardMutation(graphene.Mutation):
    """Archive workspace board."""

    class Arguments:
        """Arguments."""

        input = ArchiveWorkspaceBoardInput(required=True)

    workspace_board = graphene.Field(types.WorkspaceBoard)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        workspace_board = models.WorkspaceBoard.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        if input.archived:
            workspace_board.archive()
        else:
            workspace_board.unarchive()
        return cls(workspace_board)


class UpdateWorkspaceBoardInput(graphene.InputObjectType):
    """Input for UpdateWorkspaceBoardMutation."""

    uuid = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)


class UpdateWorkspaceBoardMutation(graphene.Mutation):
    """Update workspace board."""

    class Arguments:
        """Arguments."""

        input = UpdateWorkspaceBoardInput(required=True)

    workspace_board = graphene.Field(types.WorkspaceBoard)

    @classmethod
    def mutate(cls, root, info, input):
        """Update workspace board."""
        workspace_board = models.WorkspaceBoard.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        workspace_board.title = input.title
        workspace_board.description = input.description
        workspace_board.save()
        return cls(workspace_board)


class UpdateWorkspaceBoardSectionInput(graphene.InputObjectType):
    """Input for UpdateWorkspaceSectionMutation."""

    uuid = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)


class UpdateWorkspaceBoardSectionMutation(graphene.Mutation):
    """Update workspace board section muatation."""

    class Arguments:
        """Arguments."""

        input = UpdateWorkspaceBoardSectionInput(required=True)

    workspace_board_section = graphene.Field(types.WorkspaceBoardSection)

    @classmethod
    def mutate(cls, root, info, input):
        """Update workspace board."""
        workspace_board_section = (
            models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
                info.context.user,
                input.uuid,
            )
        )
        workspace_board_section.title = input.title
        workspace_board_section.description = input.description
        workspace_board_section.save()
        return cls(workspace_board_section)


class UpdateTaskMutationInput(graphene.InputObjectType):
    """Input for UpdateTaskMutationInput."""

    uuid = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    deadline = graphene.DateTime(required=False)


class UpdateTaskMutation(graphene.Mutation):
    """Update task mutation."""

    class Arguments:
        """Arguments."""

        input = UpdateTaskMutationInput(required=True)

    task = graphene.Field(types.Task)

    @classmethod
    def mutate(cls, root, info, input):
        """Update workspace board."""
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        task.title = input.title
        task.description = input.description
        if input.deadline:
            task.deadline = input.deadline
            assert task.deadline.tzinfo
        task.save()
        return cls(task)


class UpdateSubTaskMutationInput(graphene.InputObjectType):
    """Input for UpdateSubTaskMutationInput."""

    uuid = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)


class UpdateSubTaskMutation(graphene.Mutation):
    """Update subtask mutation."""

    class Arguments:
        """Arguments."""

        input = UpdateSubTaskMutationInput(required=True)

    sub_task = graphene.Field(types.SubTask)

    @classmethod
    def mutate(cls, root, info, input):
        """Update workspace board."""
        sub_task = models.SubTask.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        sub_task.title = input.title
        sub_task.description = input.description
        sub_task.save()
        return cls(sub_task)


# Delete Mutations
class DeleteWorkspaceBoardInput(graphene.InputObjectType):
    """DeleteWorkspaceBoardMutation input."""

    uuid = graphene.ID(required=True)


class DeleteWorkspaceBoardMutation(graphene.Mutation):
    """Delete workspace board mutation."""

    class Arguments:
        """Arguments."""

        input = DeleteWorkspaceBoardInput(required=True)

    workspace_board = graphene.Field(types.WorkspaceBoard)

    @classmethod
    def mutate(cls, root, info, input):
        """Delete workspace board."""
        workspace_board = models.WorkspaceBoard.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        workspace_board.delete()
        return cls(workspace_board)


class DeleteWorkspaceBoardSectionInput(graphene.InputObjectType):
    """DeleteWorkspaceBoardSectionMutation input."""

    uuid = graphene.ID(required=True)


class DeleteWorkspaceBoardSectionMutation(graphene.Mutation):
    """Delete workspace board section mutation."""

    class Arguments:
        """Arguments."""

        input = DeleteWorkspaceBoardSectionInput(required=True)

    workspace_board_section = graphene.Field(types.WorkspaceBoardSection)

    @classmethod
    def mutate(cls, root, info, input):
        """Delete workspace section board."""
        workspace_board_section = (
            models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
                info.context.user,
                input.uuid,
            )
        )
        workspace_board_section.delete()
        return cls(workspace_board_section)


class DeleteTaskInput(graphene.InputObjectType):
    """DeleteTaskMutation input."""

    uuid = graphene.ID(required=True)


class DeleteTaskMutation(graphene.Mutation):
    """Delete task."""

    class Arguments:
        """Arguments."""

        input = DeleteTaskInput(required=True)

    task = graphene.Field(types.Task)

    @classmethod
    def mutate(cls, root, info, input):
        """Delete task."""
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        task.delete()
        return cls(task)


class DeleteSubTaskInput(graphene.InputObjectType):
    """DeleteTaskMutation input."""

    uuid = graphene.ID(required=True)


class DeleteSubTaskMutation(graphene.Mutation):
    """Delete subtask."""

    class Arguments:
        """Arguments."""

        input = DeleteSubTaskInput(required=True)

    sub_task = graphene.Field(types.SubTask)

    @classmethod
    def mutate(cls, root, info, input):
        """Delete task."""
        sub_task = models.SubTask.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        sub_task.delete()
        return cls(sub_task)


class Mutation:
    """Mutation."""

    add_workspace_board = AddWorkspaceBoardMutation.Field()
    add_workspace_board_section = AddWorkspaceBoardSectionMutation.Field()
    add_task = AddTaskMutation.Field()
    add_sub_task = AddSubTaskMutation.Field()
    add_chat_message = AddChatMessageMutation.Field()
    move_workspace_board_section = MoveWorkspaceBoardSectionMutation.Field()
    move_task = MoveTaskMutation.Field()
    add_user_to_workspace = AddUserToWorkspaceMutation.Field()
    assign_task = AssignTaskMutation.Field()
    duplicate_task = DuplicateTaskMutation.Field()
    change_sub_task_done = ChangeSubTaskDoneMutation.Field()
    update_workspace = UpdateWorkspaceMutation.Field()
    archive_workspace_board = ArchiveWorkspaceBoardMutation.Field()
    update_workspace_board = UpdateWorkspaceBoardMutation.Field()
    update_workspace_board_section = (
        UpdateWorkspaceBoardSectionMutation.Field()
    )
    update_task = UpdateTaskMutation.Field()
    update_sub_task = UpdateSubTaskMutation.Field()
    delete_workspace_board = DeleteWorkspaceBoardMutation.Field()
    delete_workspace_board_section = (
        DeleteWorkspaceBoardSectionMutation.Field()
    )
    delete_task = DeleteTaskMutation.Field()
    delete_sub_task = DeleteSubTaskMutation.Field()
