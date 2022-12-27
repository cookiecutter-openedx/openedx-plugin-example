"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Feb-2022

example plugin for Open edX
"""
import json
import logging

from django.apps import AppConfig

# see: https://github.com/openedx/edx-django-utils/blob/master/edx_django_utils/plugins/
from edx_django_utils.plugins import PluginSettings, PluginURLs
from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType, PluginSignals

from .version import __version__
from .waffle import waffle_switches
from .signals import OPENEDX_SIGNALS, SIGNALS_RECEIVERS, signals_enabled
from .utils import PluginJSONEncoder

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
        PluginSignals.CONFIG: {
            ProjectType.LMS: {
                PluginSignals.RELATIVE_PATH: "signals",
                PluginSignals.RECEIVERS: SIGNALS_RECEIVERS(),
            }
        },
    }

    def ready(self):
        log.info("{label} version {version} is ready.".format(label=self.label, version=__version__))
        log.info(
            "{label} {waffle_switches} waffle switches detected.".format(
                label=self.label, waffle_switches=waffle_switches.len()
            )
        )
        for switch in waffle_switches:
            if waffle_switches[switch]:
                log.info("{label} WaffleSwitch {switch} is enabled.".format(label=self.label, switch=switch))
            else:
                log.warning("{label} WaffleSwitch {switch} is not enabled.".format(label=self.label, switch=switch))
        if signals_enabled():
            log.info(
                "signals enabled: {signals}".format(
                    signals=json.dumps(OPENEDX_SIGNALS, cls=PluginJSONEncoder, indent=4)
                )
            )

            pass
