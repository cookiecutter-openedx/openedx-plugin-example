"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2021

CMS App
"""
from __future__ import absolute_import, unicode_literals
import logging

from django.apps import AppConfig

from openedx.core.djangoapps.plugins.constants import PluginURLs, PluginSettings, ProjectType, SettingsType

from ..version import __version__

log = logging.getLogger(__name__)

log.info("openedx_plugin_cms %s", __version__)


class CustomPluginCMSConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "openedx_plugin_cms"
    label = "openedx_plugin_cms"
    verbose_name = "Course Change Audit Log"

    # See: https://edx.readthedocs.io/projects/edx-django-utils/en/latest/edx_django_utils.plugins.html
    plugin_app = {
        # mcdaniel oct-2021
        # this is how you inject a python list of urls into lms.urls.py
        #
        # The three dict attributes literally equate to the following
        # lines of code being injected into edx-platform/lms/urls.py:
        #
        # import openedx_plugin_cms.urls.py
        # url(r"^openedx_plugin/cms", include((urls, "openedx_plugin_cms"), namespace="openedx_plugin_cms")),
        PluginURLs.CONFIG: {
            ProjectType.CMS: {
                PluginURLs.NAMESPACE: name,
                PluginURLs.REGEX: "^openedx_plugin/cms/",
                PluginURLs.RELATIVE_PATH: "urls",
            }
        },
        # mcdaniel oct-2021
        # this is how you inject settings into lms.envs.common.py and lms.envs.production.py
        # relative_path == a python module in this repo
        #
        # This dict causes all constants defined in this settings/common.py and settings.production.py
        # to be injected into edx-platform/lms/envs/common.py and edx-platform/lms/envs/production.py
        # Refer to settings/common.py and settings.production.py for example implementation patterns.
        PluginSettings.CONFIG: {
            ProjectType.CMS: {
                SettingsType.PRODUCTION: {PluginSettings.RELATIVE_PATH: "settings.production"},
                SettingsType.COMMON: {PluginSettings.RELATIVE_PATH: "settings.common"},
            }
        },
    }

    def ready(self):
        """
        Connect handlers to signals.
        """
        from . import signals  # pylint: disable=unused-import

        log.info(
            "openedx_plugin_cms.apps.CustomPluginCMSConfig app {label} version: {version} is ready".format(
                label=self.label, version=__version__
            )
        )
