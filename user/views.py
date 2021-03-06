"""User views."""
from rest_framework import (
    generics,
    parsers,
    response,
    views,
)

from . import (
    serializers,
)


class ProfilePictureUploadView(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    def post(self, request, format=None):
        """Handle POST."""
        file_obj = request.data["file"]
        request.user.profile_picture = file_obj
        request.user.save()
        return response.Response(status=204)


class UserRetrieve(generics.RetrieveAPIView):
    """Retrieve user."""

    serializer_class = serializers.UserSerializer

    def get_object(self):
        """Return current user."""
        return self.request.user
