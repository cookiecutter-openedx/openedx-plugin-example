# coding=utf-8
"""
written by:     Lawrence McDaniel
                https://lawrencemcdaniel.com

date:           dec-2022

usage:          Create custom Waffle Switch to use as feature toggles
                https://waffle.readthedocs.io/en/stable/
"""
import logging

from edx_toggles.toggles import WaffleSwitch

log = logging.getLogger(__name__)
WAFFLE_NAMESPACE = "openedx_plugin_api"


# .. toggle_name: openedx_plugin_api.API_META
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: enables the /meta Mobile REST API url endpoint
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
API_META = f"{WAFFLE_NAMESPACE}.meta"
API_META_WAFFLE = WaffleSwitch(API_META, module_name=__name__)

# .. toggle_name: openedx_plugin_api.API_USERS
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: enables the /users Mobile REST API url endpoint
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
API_USERS = f"{WAFFLE_NAMESPACE}.users"
API_USERS_WAFFLE = WaffleSwitch(API_USERS, module_name=__name__)

# .. toggle_name: openedx_plugin_api.API_TOKEN
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: enables the /token Mobile REST API url endpoint
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
API_TOKEN = f"{WAFFLE_NAMESPACE}.token"
API_TOKEN_WAFFLE = WaffleSwitch(API_TOKEN, module_name=__name__)

# .. toggle_name: openedx_plugin_api.API_ENROLLMENT
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: enables the /enrollment Mobile REST API url endpoint
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
API_ENROLLMENT = f"{WAFFLE_NAMESPACE}.enrollment"
API_ENROLLMENT_WAFFLE = WaffleSwitch(API_ENROLLMENT, module_name=__name__)

# .. toggle_name: openedx_plugin_api.API_ASSOCIATE
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: enables the /associate Mobile REST API url endpoint
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
API_ASSOCIATE = f"{WAFFLE_NAMESPACE}.associate"
API_ASSOCIATE_WAFFLE = WaffleSwitch(API_ASSOCIATE, module_name=__name__)

# .. toggle_name: openedx_plugin_api.API_PERMISSIONS
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: enables the /permissions Mobile REST API url endpoint
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
API_PERMISSIONS = f"{WAFFLE_NAMESPACE}.permissions"
API_PERMISSIONS_WAFFLE = WaffleSwitch(API_PERMISSIONS, module_name=__name__)

# .. toggle_name: openedx_plugin_api.API_COURSE
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: enables the /course Mobile REST API url endpoint
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
API_COURSE = f"{WAFFLE_NAMESPACE}.course"
API_COURSE_WAFFLE = WaffleSwitch(API_COURSE, module_name=__name__)

# .. toggle_name: openedx_plugin_api.API_STUDENT
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: enables the /student Mobile REST API url endpoint
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
API_STUDENT = f"{WAFFLE_NAMESPACE}.student"
API_STUDENT_WAFFLE = WaffleSwitch(API_STUDENT, module_name=__name__)


def is_ready():
    """
    try to get the status of any arbitrary WaffleSwitch. If it doesn't raise an
    error then we're ready.

    This is intended to be used as a way to reduce console logging output during
    application startup, when WaffleSwitch states cannot yet be read, as the
    db service is not yet up.
    """
    try:
        API_STUDENT_WAFFLE.is_enabled()
        return True
    except Exception:  # noqa: B902
        return False


def is_enabled(switch: WaffleSwitch) -> bool:
    """
    To resolve a race condition during application launch. The waffle_switches
    are inspected before the db service has initialized.
    """
    try:
        return switch.is_enabled()
    except Exception:  # noqa: B902
        return False


waffle_switches = {
    API_META: is_enabled(API_META_WAFFLE),
    API_USERS: is_enabled(API_USERS_WAFFLE),
    API_TOKEN: is_enabled(API_TOKEN_WAFFLE),
    API_ENROLLMENT: is_enabled(API_ENROLLMENT_WAFFLE),
    API_ASSOCIATE: is_enabled(API_PERMISSIONS_WAFFLE),
    API_PERMISSIONS: is_enabled(API_PERMISSIONS_WAFFLE),
    API_COURSE: is_enabled(API_COURSE_WAFFLE),
    API_STUDENT: is_enabled(API_STUDENT_WAFFLE),
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
        log.warning("django_waffle app is not ready. waffle_init() cannot continue")
        return None
    except ImportError:
        # for older versions of django-waffle
        # in nutmeg.2 we're running django-waffle=2.4.1
        #
        # assumption: edX guys have not and will not subclass Switch
        log.warning(
            "{django_app}: get_waffle_model() not found. Importing Switch class directly from waffle.models".format(
                django_app=WAFFLE_NAMESPACE
            )
        )
        from waffle.models import Switch

    log.info(
        "{plugin} {waffle_switches} waffle switches detected".format(
            plugin=WAFFLE_NAMESPACE, waffle_switches=len(waffle_switches.keys())
        )
    )

    if not is_ready():
        log.warning(
            "{django_app}: unable to verify initialization status of waffle \
            switches. Try running manage.py lms {django_app}_init".format(
                django_app=WAFFLE_NAMESPACE
            )
        )
        return

    for switch_name, _switch_object in waffle_switches.items():
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
