"""
written by:     Lawrence McDaniel
                https://lawrencemcdaniel.com

date:           sep-2021

usage:          Django app and Open edX plugin configuration for
                openedx_plugin_api plugin
"""
import logging

from django.apps import AppConfig
from django.conf import settings

from edx_django_utils.plugins import PluginSettings, PluginURLs
from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType

log = logging.getLogger(__name__)
IS_READY = False


class CustomPluginAPIConfig(AppConfig):
    name = "openedx_plugin_api"
    label = "openedx_plugin_api"

    # See: https://edx.readthedocs.io/projects/edx-django-utils/en/latest/edx_django_utils.plugins.html
    plugin_app = {
        # mcdaniel Sep-2021
        # this is how you inject a python list of urls into lms.urls.py
        #
        # The three dict attributes literally equate to the following
        # lines of code being injected into edx-platform/lms/urls.py:
        #
        # import openedx_plugin_api.urls.py
        # url(r"^openedx_plugin/api/", include((urls, "openedx_plugin_api"), namespace="openedx_plugin_api")),
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: name,
                PluginURLs.REGEX: "^openedx_plugin/api/",
                PluginURLs.RELATIVE_PATH: "urls",
            },
        },
        # mcdaniel Sep-2021
        # this is how you inject settings into lms.envs.common.py and lms.envs.production.py
        # relative_path == a python module in this repo
        #
        # This dict causes all constants defined in this settings/common.py and settings.production.py
        # to be injected into edx-platform/lms/envs/common.py and edx-platform/lms/envs/production.py
        # Refer to settings/common.py and settings.production.py for example implementation patterns.
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.PRODUCTION: {PluginSettings.RELATIVE_PATH: "settings.production"},
            },
        },
    }

    def ready(self):
        global IS_READY

        if IS_READY:
            return

        from . import signals  # pylint: disable=unused-import
        from .version import __version__
        from .waffle import waffle_init

        log.info("{label} {version} is ready.".format(label=self.label, version=__version__))
        waffle_init()
        IS_READY = True
