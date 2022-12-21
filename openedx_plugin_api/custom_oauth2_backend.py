import requests
from social_core.backends.oauth import BaseOAuth2
from django.conf import settings


class CustomOAuth2(BaseOAuth2):

    name = "custom-oauth"
    BASE_URL = getattr(settings, "OAUTH_HOST_BASE_URL", "http://YOURDOMAIN.EDU")
    AUTHORIZATION_URL = f"{BASE_URL}/o/authorize/"
    ACCESS_TOKEN_URL = f"{BASE_URL}/o/token/"
    ACCESS_TOKEN_METHOD = "POST"
    SCOPE_SEPARATOR = ","
    EXTRA_DATA = []
    ID_KEY = "original_email"

    def get_user_details(self, response):
        return {
            "username": response.get("username"),
            "email": response.get("email"),
            "first_name": response.get("first_name"),
            "last_name": response.get("last_name"),
            "fullname": response.get("full_name"),
        }

    def user_data(self, access_token, *args, **kwargs):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{self.BASE_URL}/api/user-details/", headers=headers)
        return response.json()
