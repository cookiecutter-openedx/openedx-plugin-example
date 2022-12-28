"""
written by:     Lawrence McDaniel
                https://lawrencemcdaniel.com

date:           feb-2022

usage:          custom Waffle Switches to use as feature toggles
                for openedx_plugin.
                see https://waffle.readthedocs.io/en/stable/
"""
from edx_toggles.toggles import WaffleSwitch

WAFFLE_NAMESPACE = "openedx_plugin"

# .. toggle_name: openedx_plugin.marketing_redirector
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: adds language-specific marketing site urls based on a language parameter added to the http request
# .. toggle_warnings: depends on settings.MKTG_URL_OVERRIDES
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
SIMPLE_REST_API = f"{WAFFLE_NAMESPACE}.simple_rest_api"
SIMPLE_REST_API_WAFFLE = WaffleSwitch(SIMPLE_REST_API, module_name=__name__)


# .. toggle_name: openedx_plugin.override_lms_django_admin_login
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: This toggle will revert the Django Admin login page to the original Django default
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
OVERRIDE_OPENEDX_DJANGO_LOGIN = f"{WAFFLE_NAMESPACE}.override_lms_django_admin_login"
OVERRIDE_OPENEDX_DJANGO_LOGIN_WAFFLE = WaffleSwitch(OVERRIDE_OPENEDX_DJANGO_LOGIN, module_name=__name__)

# .. toggle_name: openedx_plugin.automated_enrollment
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: reads and processes http request parameters 'language' (ie es-419) and 'enroll' (an escaped course key)
# .. toggle_warnings: ensure that you add the languages to your open edx build.
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
AUTOMATED_ENROLLMENT = f"{WAFFLE_NAMESPACE}.automated_enrollment"
AUTOMATED_ENROLLMENT_WAFFLE = WaffleSwitch(OVERRIDE_OPENEDX_DJANGO_LOGIN, module_name=__name__)

# .. toggle_name: openedx_plugin.marketing_redirector
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: adds language-specific marketing site urls based on a language parameter added to the http request
# .. toggle_warnings: depends on settings.MKTG_URL_OVERRIDES
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
MARKETING_REDIRECTOR = f"{WAFFLE_NAMESPACE}.marketing_redirector"
MARKETING_REDIRECTOR_WAFFLE = WaffleSwitch(MARKETING_REDIRECTOR, module_name=__name__)

# .. toggle_name: openedx_plugin.signals
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: adds hooks for Django signals
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
SIGNALS = f"{WAFFLE_NAMESPACE}.signals"
SIGNALS_WAFFLE = WaffleSwitch(SIGNALS, module_name=__name__)


def is_ready():
    """
    try to get the status of any arbitrary WaffleSwitch. If it doesn't raise an
    error then we're ready.

    This is intended to be used as a way to reduce console logging output during
    application startup, when WaffleSwitch states cannot yet be read, as the
    db service is not yet up.
    """
    try:
        SIGNALS_WAFFLE.is_enabled()
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
    SIMPLE_REST_API: is_enabled(SIMPLE_REST_API_WAFFLE),
    OVERRIDE_OPENEDX_DJANGO_LOGIN: is_enabled(OVERRIDE_OPENEDX_DJANGO_LOGIN_WAFFLE),
    AUTOMATED_ENROLLMENT: is_enabled(AUTOMATED_ENROLLMENT_WAFFLE),
    MARKETING_REDIRECTOR: is_enabled(MARKETING_REDIRECTOR_WAFFLE),
    SIGNALS: is_enabled(SIGNALS_WAFFLE),
}
