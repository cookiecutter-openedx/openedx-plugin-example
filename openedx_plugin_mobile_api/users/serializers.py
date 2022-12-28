"""
Serializer for user API
"""

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.reverse import reverse

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes User models
    """

    name = serializers.ReadOnlyField(source="profile.name")
    course_enrollments = serializers.SerializerMethodField()
    dob = serializers.SerializerMethodField()
    yob = serializers.SerializerMethodField()

    def get_course_enrollments(self, model):
        request = self.context.get("request")
        api_version = self.context.get("api_version")

        return reverse(
            "courseenrollment-detail", kwargs={"api_version": api_version, "username": model.username}, request=request
        )

    def get_dob(self, model):
        try:
            return model.ttb_profile.dob.strftime("%Y-%m-%d")
        except Exception:
            return None

    def get_yob(self, model):
        try:
            return model.ttb_profile.yob
        except Exception:
            return None

    class Meta:
        model = User
        fields = ("id", "username", "email", "name", "course_enrollments", "dob", "yob")
        lookup_field = "username"
        # For disambiguating within the drf-yasg swagger schema
        ref_name = "mobile_api.User"
