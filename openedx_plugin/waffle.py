"""
written by:     Lawrence McDaniel
                https://lawrencemcdaniel.com

date:           feb-2022

usage:          custom Waffle Switches to use as feature toggles for
                openedx_plugin. see https://waffle.readthedocs.io/en/stable/
"""
import logging

try:
    # only works for versions 3.x and later
    from waffle import get_waffle_model

    Switch = get_waffle_model("SWITCH_MODEL")
except ImportError:
    # for older versions of django-waffle
    # in nutmeg.2 we're running django-waffle=2.4.1
    #
    # assumption: edX guys have not and will not subclass Switch
    from waffle.models import Switch

from edx_toggles.toggles import WaffleSwitch

log = logging.getLogger(__name__)

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


def waffle_init():
    """
    Bootstrapper for the WaffleSwitch objects defined in this module. Iterate
    all WaffleSwitch objects, create any that are missing. This is called once
    from apps.CustomPluginConfig.ready() during application launch to ensure
    that WaffleSwitch objects exist in Django Admin for all switches.

    Note that django-waffle actually includes a handy setting,
    WAFFLE_CREATE_MISSING_FLAGS, that **could** do this for us automatically.
    However, setting this flag would affect EVERY WaffleSwitch in the entire
    Open edX platform, which would be reckless on our part.
    See https://waffle.readthedocs.io/en/stable/starting/configuring.html
    """
    log.info(
        "{plugin} {waffle_switches} waffle switches detected".format(
            plugin=WAFFLE_NAMESPACE, waffle_switches=len(waffle_switches.keys())
        )
    )
    if not is_ready():
        log.warning(
            "unable to verify initialization status of waffle switches. Try running manage.py lms openedx_plugin_init"
        )
        return

    for switch_name, switch_object in waffle_switches.items():
        this_switch = Switch.objects.get(name=switch_name)
        if this_switch:
            log.info(
                "WaffleSwitch {switch_name} was previously initialized {and_is_or_is_not} enabled.".format(
                    switch_name=switch_name, and_is_or_is_not="and is" if this_switch.is_enabled else "but is not"
                )
            )
        else:
            Switch.objects.create(name=switch_name, active=False)
            log.info("Initialized WaffleSwitch object {switch_name}".format(switch_name=switch_name))
