"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Aug-2021

Tests of the openedx_plugin_api
"""
from django.urls import reverse
from rest_framework.test import APITestCase

from common.djangoapps.course_modes.models import CourseMode
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from xmodule.modulestore.tests.django_utils import SharedModuleStoreTestCase


class TestAPIEndpoints(SharedModuleStoreTestCase, APITestCase):
    """
    Extremely basic Tests.
    Try each url end point, assert that it returns a 200 response code.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # hook for future use.

    def setUp(self):
        super().setUp()

        self.response = self.client.get(reverse("edxapi_meta"))
        assert self.response.status_code == 200

        self.response = self.client.get(reverse("edxapi_users"))
        assert self.response.status_code == 200

        self.response = self.client.get(reverse("edxapi_token"))
        assert self.response.status_code == 200
