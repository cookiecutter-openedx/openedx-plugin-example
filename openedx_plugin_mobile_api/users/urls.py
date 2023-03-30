# coding=utf-8
"""
URLs for user API
"""


from django.conf import settings
from django.urls import re_path

from .views import UserDetail

urlpatterns = [
    re_path("^" + settings.USERNAME_PATTERN + "$", UserDetail.as_view(), name="user-detail"),
]
