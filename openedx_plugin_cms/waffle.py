import logging

from edx_toggles.toggles import WaffleSwitch

log = logging.getLogger(__name__)
WAFFLE_NAMESPACE = "openedx_plugin_cms"

# .. toggle_name: openedx_plugin_api.OVERRIDE_MOBILE_USER_API_URL_WAFFLE
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: This toggle will override the openedx mobile api url endpoint
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
AUDIT_REPORT = f"{WAFFLE_NAMESPACE}.audit_report"
AUDIT_REPORT_WAFFLE = WaffleSwitch(AUDIT_REPORT, module_name=__name__)


def is_ready():
    """
    try to get the status of any arbitrary WaffleSwitch. If it doesn't raise an
    error then we're ready.

    This is intended to be used as a way to reduce console logging output during
    application startup, when WaffleSwitch states cannot yet be read, as the
    db service is not yet up.
    """
    try:
        AUDIT_REPORT_WAFFLE.is_enabled()
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
    AUDIT_REPORT: is_enabled(AUDIT_REPORT_WAFFLE),
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

    To inspect the state of our WaffleSwitch objects we need to go directly
    to the django-waffle objects which edx-toggles imports to implement WaffleSwitch.
    """
    from django.core.exceptions import ObjectDoesNotExist, AppRegistryNotReady

    try:
        # django_waffle 3.x and later
        from waffle import get_waffle_model

        Switch = get_waffle_model("SWITCH_MODEL")
    except AppRegistryNotReady:
        log.error("django_waffle app is not ready. Cannot continue")
        return None
    except ImportError:
        # for older versions of django-waffle
        # in nutmeg.2 we're running django-waffle=2.4.1
        #
        # assumption: edX guys have not and will not subclass Switch
        log.warning("get_waffle_model() not found. Importing Switch class directly from waffle.models")
        from waffle.models import Switch

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
        try:
            this_switch = Switch.objects.get(name=switch_name)
        except ObjectDoesNotExist:
            this_switch = None
            pass

        if this_switch:
            # note: edx_toggles.toggles.WaffleSwitch.is_enabled() is derived from
            # waffle.models.Switch.active  (a boolean)
            # see
            #  - https://github.com/django-waffle/django-waffle/blob/master/waffle/models.py#L438
            #  - https://github.com/openedx/edx-toggles/blob/master/edx_toggles/toggles/internal/waffle/switch.py#L19
            log.info(
                "WaffleSwitch {switch_name} was previously initialized {and_is_or_is_not} enabled.".format(
                    switch_name=switch_name, and_is_or_is_not="and is" if this_switch.active else "but is not"
                )
            )
        else:
            Switch.objects.create(name=switch_name, active=False)
            log.info("Initialized WaffleSwitch object {switch_name}".format(switch_name=switch_name))
