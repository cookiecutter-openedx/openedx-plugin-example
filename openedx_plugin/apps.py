"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Feb-2022

example plugin for Open edX
"""
from __future__ import absolute_import, unicode_literals
import logging

from django.apps import AppConfig

from edx_django_utils.plugins import PluginSettings, PluginURLs
from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType

from .version import __version__
from .waffle import waffle_switches

log = logging.getLogger(__name__)
log.info("openedx_plugin %s", __version__)


class CustomPluginConfig(AppConfig):
    name = "openedx_plugin"
    label = "openedx_plugin"

    # This is the text that appears in the Django admin console in all caps
    # as the title box encapsulating all Django app models that are registered
    # in admin.py.
    verbose_name = "lms.example.edu plugin for Open edX"

    # See: https://edx.readthedocs.io/projects/edx-django-utils/en/latest/edx_django_utils.plugins.html
    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: name,
                PluginURLs.REGEX: "^openedx_plugin/",
                PluginURLs.RELATIVE_PATH: "urls",
            }
        },
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                # uncomment these to activate
                SettingsType.PRODUCTION: {PluginSettings.RELATIVE_PATH: "settings.production"},
                SettingsType.COMMON: {PluginSettings.RELATIVE_PATH: "settings.common"},
            }
        },
        "signals_config": {
            "lms.djangoapp": {
                "relative_path": "receivers",
                "receivers": [
                    {
                        "receiver_func_name": "student_registration_completed",
                        "signal_path": "openedx_events.learning.signals.STUDENT_REGISTRATION_COMPLETED",
                    },
                    {
                        "receiver_func_name": "course_enrollment_created",
                        "signal_path": "openedx_events.learning.signals.COURSE_ENROLLMENT_CREATED",
                    },
                    {
                        "receiver_func_name": "persistent_grade_summary_changed",
                        "signal_path": "openedx_events.learning.signals.PERSISTENT_GRADE_SUMMARY_CHANGED",
                    },
                ],
            }
        },
    }

    def ready(self):
        log.info("{label} version {version} is ready.".format(label=self.label, version=__version__))
        for switch in waffle_switches:
            if waffle_switches[switch]:
                log.info("{label} WaffleSwitch {switch} is enabled.".format(label=self.label, switch=switch))
            else:
                log.warning("{label} WaffleSwitch {switch} is not enabled.".format(label=self.label, switch=switch))
