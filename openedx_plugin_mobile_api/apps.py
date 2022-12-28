"""
Configuration for the mobile_api Django application.
"""
import logging

from django.apps import AppConfig

log = logging.getLogger(__name__)


class MobileApiConfig(AppConfig):
    """
    Lawrence McDaniel
    https://lawrencemcdaniel.com

    Configuration class for the Turn The Bus customized mobile_api Django application.
    Spawned from https://github.com/openedx/edx-platform/tree/master/lms/djangoapps/mobile_api
    """

    name = "openedx_plugin_mobile_api"
    verbose_name = "Modified LMS Mobile REST API Endpoint"

    def ready(self):
        from .version import __version__
        from .waffle import waffle_switches, is_ready

        log.info("{label} version {version} is ready.".format(label=self.label, version=__version__))
        log.info(
            "{label} {waffle_switches} waffle switches detected.".format(
                label=self.label, waffle_switches=len(waffle_switches.keys())
            )
        )
        if is_ready():
            for switch in waffle_switches:
                if waffle_switches[switch]:
                    log.info("WaffleSwitch {switch} is enabled.".format(switch=switch))
                else:
                    log.warning("WaffleSwitch {switch} is not enabled.".format(switch=switch))
