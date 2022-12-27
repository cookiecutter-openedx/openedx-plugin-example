"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Feb-2022

example plugin for Open edX
"""
from __future__ import absolute_import, unicode_literals
import logging

from django.apps import AppConfig

# see: https://github.com/openedx/edx-django-utils/blob/master/edx_django_utils/plugins/
from edx_django_utils.plugins import PluginSettings, PluginURLs
from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType, PluginSignals

from .version import __version__
from .waffle import waffle_switches

log = logging.getLogger(__name__)
log.info("openedx_plugin %s", __version__)

OPENEDX_SIGNALS = "openedx_events.learning.signals"
STUDENT_REGISTRATION_COMPLETED = "STUDENT_REGISTRATION_COMPLETED"
SESSION_LOGIN_COMPLETED = "SESSION_LOGIN_COMPLETED"
COURSE_ENROLLMENT_CREATED = "COURSE_ENROLLMENT_CREATED"
COURSE_ENROLLMENT_CHANGED = "COURSE_ENROLLMENT_CHANGED"
COURSE_UNENROLLMENT_COMPLETED = "COURSE_UNENROLLMENT_COMPLETED"
PERSISTENT_GRADE_SUMMARY_CHANGED = "PERSISTENT_GRADE_SUMMARY_CHANGED"
CERTIFICATE_CREATED = "CERTIFICATE_CREATED"
CERTIFICATE_CHANGED = "CERTIFICATE_CHANGED"
CERTIFICATE_REVOKED = "CERTIFICATE_REVOKED"
COHORT_MEMBERSHIP_CHANGED = "COHORT_MEMBERSHIP_CHANGED"
COURSE_DISCUSSIONS_CHANGED = "COURSE_DISCUSSIONS_CHANGED"


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
        PluginSignals.CONFIG: {
            ProjectType.LMS: {
                PluginSignals.RELATIVE_PATH: "signals",
                PluginSignals.RECEIVERS: [
                    {
                        PluginSignals.RECEIVER_FUNC_NAME: STUDENT_REGISTRATION_COMPLETED.lower(),
                        PluginSignals.SIGNAL_PATH: OPENEDX_SIGNALS + "." + STUDENT_REGISTRATION_COMPLETED,
                    },
                    {
                        PluginSignals.RECEIVER_FUNC_NAME: SESSION_LOGIN_COMPLETED.lower(),
                        PluginSignals.SIGNAL_PATH: OPENEDX_SIGNALS + "." + SESSION_LOGIN_COMPLETED,
                    },
                    {
                        PluginSignals.RECEIVER_FUNC_NAME: COURSE_ENROLLMENT_CREATED.lower(),
                        PluginSignals.SIGNAL_PATH: OPENEDX_SIGNALS + "." + COURSE_ENROLLMENT_CREATED,
                    },
                    {
                        PluginSignals.RECEIVER_FUNC_NAME: COURSE_ENROLLMENT_CHANGED.lower(),
                        PluginSignals.SIGNAL_PATH: OPENEDX_SIGNALS + "." + COURSE_ENROLLMENT_CHANGED,
                    },
                    {
                        PluginSignals.RECEIVER_FUNC_NAME: COURSE_UNENROLLMENT_COMPLETED.lower(),
                        PluginSignals.SIGNAL_PATH: OPENEDX_SIGNALS + "." + COURSE_UNENROLLMENT_COMPLETED,
                    },
                    # mcdaniel dec-2022: this is missing from nutmeg.2
                    #       COMING SOON?
                    # {
                    #    PluginSignals.RECEIVER_FUNC_NAME: PERSISTENT_GRADE_SUMMARY_CHANGED.lower(),
                    #    PluginSignals.SIGNAL_PATH: OPENEDX_SIGNALS + "." + PERSISTENT_GRADE_SUMMARY_CHANGED,
                    # },
                    {
                        PluginSignals.RECEIVER_FUNC_NAME: CERTIFICATE_CREATED.lower(),
                        PluginSignals.SIGNAL_PATH: OPENEDX_SIGNALS + "." + CERTIFICATE_CREATED,
                    },
                    {
                        PluginSignals.RECEIVER_FUNC_NAME: CERTIFICATE_CHANGED.lower(),
                        PluginSignals.SIGNAL_PATH: OPENEDX_SIGNALS + "." + CERTIFICATE_CHANGED,
                    },
                    {
                        PluginSignals.RECEIVER_FUNC_NAME: CERTIFICATE_REVOKED.lower(),
                        PluginSignals.SIGNAL_PATH: OPENEDX_SIGNALS + "." + CERTIFICATE_REVOKED,
                    },
                    {
                        PluginSignals.RECEIVER_FUNC_NAME: COHORT_MEMBERSHIP_CHANGED.lower(),
                        PluginSignals.SIGNAL_PATH: OPENEDX_SIGNALS + "." + COHORT_MEMBERSHIP_CHANGED,
                    },
                    {
                        PluginSignals.RECEIVER_FUNC_NAME: COURSE_DISCUSSIONS_CHANGED.lower(),
                        PluginSignals.SIGNAL_PATH: OPENEDX_SIGNALS + "." + COURSE_DISCUSSIONS_CHANGED,
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
