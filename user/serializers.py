"""User app serializers."""
from rest_framework import (
    serializers,
)

from projectify import (
    utils,
)

from . import (
    models,
)


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    profile_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, obj):
        """Return profile picture."""
        return utils.crop_image(obj.profile_picture, 100, 100)

    class Meta:
        """Meta."""

        model = models.User
        fields = (
            "email",
            "full_name",
            "profile_picture",
        )
