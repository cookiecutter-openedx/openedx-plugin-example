"""
written by:     Lawrence McDaniel
                https://lawrencemcdaniel.com

date:           dec-2022

usage:          custom Waffle Switch to use as feature toggles
                for openedx_plugin_mobile_api.
                see https://waffle.readthedocs.io/en/stable/
"""
from edx_toggles.toggles import WaffleSwitch

WAFFLE_NAMESPACE = "openedx_plugin_mobile_api"
# .. toggle_name: openedx_plugin_api.OVERRIDE_MOBILE_USER_API_URL_WAFFLE
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: This toggle will override the openedx mobile api url endpoint
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
OVERRIDE_MOBILE_USER_API_URL = f"{WAFFLE_NAMESPACE}.override_mobile_user_api_url"
OVERRIDE_MOBILE_USER_API_URL_WAFFLE = WaffleSwitch(OVERRIDE_MOBILE_USER_API_URL, module_name=__name__)


def is_ready():
    """
    try to get the status of any arbitrary WaffleSwitch. If it doesn't raise an
    error then we're ready.

    This is intended to be used as a way to reduce console logging output during
    application startup, when WaffleSwitch states cannot yet be read, as the
    db service is not yet up.
    """
    try:
        OVERRIDE_MOBILE_USER_API_URL_WAFFLE.is_enabled()
        return True
    except Exception:
        return False


def is_enabled(switch: WaffleSwitch) -> bool:
    """
    To resolve a race condition during application launch. The waffle_switches
    are inspected before the db service has initialized.
    """
    try:
        return switch.is_enabled()
    except Exception:
        return False


waffle_switches = {
    OVERRIDE_MOBILE_USER_API_URL: is_enabled(OVERRIDE_MOBILE_USER_API_URL_WAFFLE),
}
