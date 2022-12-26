import logging

from django.apps import AppConfig
from django.conf import settings

from edx_django_utils.plugins import PluginSettings, PluginURLs
from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType

from ..version import __version__


log = logging.getLogger(__name__)


log.info("openedx_plugin_api %s", __version__)


class CustomPluginAPIConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
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
            ProjectType.CMS: {
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
                SettingsType.COMMON: {PluginSettings.RELATIVE_PATH: "settings.common"},
            },
            ProjectType.CMS: {
                SettingsType.PRODUCTION: {PluginSettings.RELATIVE_PATH: "settings.production"},
                SettingsType.COMMON: {PluginSettings.RELATIVE_PATH: "settings.common"},
            },
        },
    }

    def ready(self):
        from openedx_plugin_api.receivers import listen_for_passing_grade

        log.info("{label} is ready.".format(label=self.label))
