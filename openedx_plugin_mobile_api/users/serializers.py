# coding=utf-8
"""
Serializer for user API
"""

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.reverse import reverse

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Scaffolded from https://github.com/openedx/edx-platform/blob/open-release/nutmeg.master/lms/djangoapps/mobile_api/users/serializers.py#L130  # noqa: B950

    you'll need to do the following:
    # -----------------------------------------
      1.) implement your custom api fields
      2.) implement your custom getters
      3.) implement your custom field definitions
    """

    name = serializers.ReadOnlyField(source="profile.name")
    course_enrollments = serializers.SerializerMethodField()

    # 1.) implement your custom api fields here ...
    # -----------------------------------------
    custom_api_field1 = serializers.SerializerMethodField()
    custom_api_field2 = serializers.SerializerMethodField()

    def get_course_enrollments(self, model):
        request = self.context.get("request")
        api_version = self.context.get("api_version")

        return reverse(
            "courseenrollment-detail",
            kwargs={"api_version": api_version, "username": model.username},
            request=request,
        )

    # 2.) implement your custom getters here ....
    # -----------------------------------------
    def get_custom_api_field1(self, model):
        return "implement-me-please"

    def get_custom_api_field2(self, model):
        return "implement-me-please"

    class Meta:
        model = User
        # 3.) implement your custom field definitions here ....
        # -----------------------------------------
        fields = ("id", "username", "email", "name", "course_enrollments", "custom_api_field1", "custom_api_field2")
        lookup_field = "username"
        # For disambiguating within the drf-yasg swagger schema
        ref_name = "openedx_plugin_mobile_api.User"
