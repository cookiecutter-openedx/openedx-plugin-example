# coding=utf-8
"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Feb-2022

https://lms.yourdomain.edu/openedx_plugin/api/v1/configuration
https://lms.yourdomain.edu/openedx_plugin/dashboard
https://lms.yourdomain.edu/openedx_plugin/dashboard?language=es-419
"""
# Django
from django.conf.urls import url

# this repo
from openedx_plugin.dashboard.views import student_dashboard
from openedx_plugin.locale.views import marketing_redirector
from openedx_plugin.api.urls import urlpatterns as api_urlpatterns
from .waffle import waffle_switches, AUTOMATED_ENROLLMENT, MARKETING_REDIRECTOR

app_name = "openedx_plugin"

urlpatterns = []

if waffle_switches[AUTOMATED_ENROLLMENT]:
    urlpatterns += [
        url(r"^dashboard/?$", student_dashboard, name="example_dashboard"),
    ]

if waffle_switches[MARKETING_REDIRECTOR]:
    urlpatterns += [
        url(
            r"^marketing-redirector/?$",
            marketing_redirector,
            name="example_marketing_redirector",
        ),
    ]

urlpatterns += api_urlpatterns
