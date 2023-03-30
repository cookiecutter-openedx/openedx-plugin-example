# coding=utf-8
"""
URLs for mobile API
"""


from django.urls import include, path
from .waffle import waffle_switches, OVERRIDE_MOBILE_USER_API_URL

urlpatterns = []

if waffle_switches[OVERRIDE_MOBILE_USER_API_URL]:
    urlpatterns += [
        path("users/", include("openedx_plugin_mobile_api.users.urls")),
    ]
