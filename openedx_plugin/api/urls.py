# coding=utf-8
"""
written by: Lawrence McDaniel
            https://lawrencemcdaniel.com

date:       jun-2019

usage:      implements a simple REST API using Django RestFramework
"""
from rest_framework.routers import DefaultRouter
from openedx_plugin.api.views import ConfigurationViewSet

from ..waffle import waffle_switches, SIMPLE_REST_API

urlpatterns = []

if waffle_switches[SIMPLE_REST_API]:
    router = DefaultRouter(trailing_slash=False)
    router.register("api/v1/configuration", ConfigurationViewSet)
    urlpatterns += router.urls
