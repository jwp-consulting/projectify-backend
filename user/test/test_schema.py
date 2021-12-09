"""User app schema tests."""
import pytest


@pytest.mark.django_db
class TestSignupMutation:
    """Test Signup Mutation."""

    def test_user_is_created(self, graphql_query, json_loads):
        """Assert that user is created."""
        query = """
mutation {
    signup(email: "hello@example.com", password: "password") {
        user {
            email
        }
    }
}
"""
        result = json_loads(graphql_query(query).content)
        assert result == {
            "data": {
                "signup": {
                    "user": {
                        "email": "hello@example.com",
                    },
                }
            }
        }


@pytest.mark.django_db
class TestLoginMutation:
    """Test LoginMutation."""

    query = """
mutation ($email: String!, $password: String!) {
  login(email: $email, password: $password) {
    user {
      email
    }
  }
}
"""

    def test_login_active_user(self, graphql_query, user, json_loads):
        """Test logging in an active user."""
        result = json_loads(
            graphql_query(
                self.query,
                variables={
                    "email": user.email,
                    "password": "password",
                },
            ).content
        )
        assert result == {
            "data": {
                "login": {
                    "user": {
                        "email": user.email,
                    },
                }
            }
        }

    def test_login_wrong_password(self, graphql_query, user, json_loads):
        """Test logging in with a wrong password."""
        result = json_loads(
            graphql_query(
                self.query,
                variables={
                    "email": user.email,
                    "password": "wrongpassword",
                },
            ).content
        )
        assert result == {"data": {"login": None}}

    def test_login_inactive_user(
        self, graphql_query, inactive_user, json_loads
    ):
        """Test logging in an inactive user."""
        result = json_loads(
            graphql_query(
                self.query,
                variables={
                    "email": inactive_user.email,
                    "password": "password",
                },
            ).content
        )
        assert result == {"data": {"login": None}}
