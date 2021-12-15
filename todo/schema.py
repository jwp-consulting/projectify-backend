"""Todo Schema."""
from django.core.paginator import Paginator

import graphene
from graphene_django import DjangoObjectType

from todo import models


class PageType(graphene.ObjectType):
    """Page type."""

    entries_count = graphene.Int(required=True)
    number = graphene.Int(required=True)
    per_page = graphene.Int(required=True)


class TodoItemFolder(DjangoObjectType):
    """TodoItemFolder."""

    class Meta:
        """Meta."""
        model = models.TodoItemFolder


class TodoItemFolderPage(PageType):
    """TodoItemFolder page."""

    object_list = graphene.List(TodoItemFolder)


class TodoItem(DjangoObjectType):
    """TodoItem."""

    class Meta:
        """Meta."""

        model = models.TodoItem


class TodoItemPage(PageType):
    """A page of todo items."""

    object_list = graphene.List(TodoItem)


pagination_kwargs = {
    "page": graphene.Int(required=True),
    "size": graphene.Int(required=True),
}


def paginate(queryset, page, size):
    """Paginate a queryset."""
    return Paginator(queryset, size).page(page)


class Query:
    """Query object."""

    todo_items = graphene.Field(TodoItemPage, **pagination_kwargs)
    todo_item_folders = graphene.Field(TodoItemFolderPage, **pagination_kwargs)

    def resolve_todo_item_folders(self, info, page, size):
        """Resolve a page of todo item folders."""
        
        qs = info.context.user.todoitemfolder_set.all()
        print(qs)
        return paginate(qs, page, size)

    def resolve_todo_items(self, info, page, size):
        """Resolve a page of todo items."""
        qs = info.context.user.todoitem_set.all()
        return paginate(qs, page, size)


    