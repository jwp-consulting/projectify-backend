"""User schema."""
from django.contrib import auth
import graphene
import graphene_django


class User(graphene_django.DjangoObjectType):
    """User."""

    class Meta:
        """Meta."""

        model = auth.get_user_model()


class LoginMutation(graphene.Mutation):
    """Login mutation."""

    class Arguments:
        """Arguments required."""

        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(User)

    @classmethod
    def mutate(cls, root, info, email, password):
        """Mutate."""
        user = auth.get_user_model().objects.get_by_natural_key(email)
        if not user.check_password(password):
            return
        auth.login(info.context, user)
        return cls(user=user)


class LogoutMutation(graphene.Mutation):
    """Logout mutation."""

    class Arguments:
        """No arguments required."""

    user = graphene.Field(User)

    @classmethod
    def mutate(cls, root, info):
        """Mutate."""
        user = info.context.user
        if user.is_anonymous:
            raise ValueError("User not logged in")
        auth.logout(info.context)
        return cls(user=user)


class Query:
    """Query."""

    user = graphene.Field(User)

    def resolve_user(self, info):
        """Resolve user field."""
        return info.context.user


class Mutation:
    """Mutation."""

    login = LoginMutation.Field()
    logout = LogoutMutation.Field()
 