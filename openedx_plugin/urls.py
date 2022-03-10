"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Feb-2022

https://lms.example.edu/example/api/v1/configuration
https://lms.example.edu/example/dashboard
https://lms.example.edu/example/dashboard?language=es-419
"""
# Django
from django.conf.urls import url

# this repo
from openedx_plugin.dashboard.views import student_dashboard
from openedx_plugin.locale.views import marketing_redirector
from openedx_plugin.api.urls import urlpatterns as api_urlpatterns

app_name = "openedx_plugin"

urlpatterns = [
    url(r"^dashboard/?$", student_dashboard, name="example_dashboard"),
    url(r"^marketing-redirector/?$", marketing_redirector, name="example_marketing_redirector"),
] + api_urlpatterns
