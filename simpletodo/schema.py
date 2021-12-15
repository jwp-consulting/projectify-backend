import graphene

import todo.schema
import user.schema

class Query(todo.schema.Query, user.schema.Query, graphene.ObjectType):
    """Query object."""


class Mutation(user.schema.Mutation, graphene.ObjectType):
    """Mutation object."""

schema = graphene.Schema(query=Query, mutation=Mutation)
