"""
Views for user API
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.decorators import api_view

from ..decorators import mobile_view
from .serializers import UserSerializer

User = get_user_model()


@mobile_view(is_user=True)
class UserDetail(generics.RetrieveAPIView):
    """
    **Use Case**

        Get information about the specified user and access other resources
        the user has permissions for.

        Users are redirected to this endpoint after they sign in.

        You can use the **course_enrollments** value in the response to get a
        list of courses the user is enrolled in.

    **Example Request**

        GET /api/mobile/{version}/users/{username}

    **Response Values**

        If the request is successful, the request returns an HTTP 200 "OK" response.

        The HTTP 200 response has the following values.

        * course_enrollments: The URI to list the courses the currently signed
          in user is enrolled in.
        * email: The email address of the currently signed in user.
        * id: The ID of the user.
        * name: The full name of the currently signed in user.
        * username: The username of the currently signed in user.
    """

    queryset = User.objects.all().select_related("profile")
    serializer_class = UserSerializer
    lookup_field = "username"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["api_version"] = self.kwargs.get("api_version")
        return context


@api_view(["GET"])
@mobile_view()
def my_user_info(request, api_version):
    """
    Redirect to the currently-logged-in user's info page
    """
    # update user's last logged in from here because
    # updating it from the oauth2 related code is too complex
    user_logged_in.send(sender=User, user=request.user, request=request)
    return redirect("user-detail", api_version=api_version, username=request.user.username)
