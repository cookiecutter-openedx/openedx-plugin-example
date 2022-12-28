"""
written by:     Lawrence McDaniel
                https://lawrencemcdaniel.com

date:           dec-2022

usage:          Create custom Waffle Switch to use as feature toggles
                https://waffle.readthedocs.io/en/stable/
"""
from edx_toggles.toggles import WaffleSwitch

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
    API_META: is_enabled(API_META_WAFFLE),
    API_USERS: is_enabled(API_USERS_WAFFLE),
    API_TOKEN: is_enabled(API_TOKEN_WAFFLE),
    API_ENROLLMENT: is_enabled(API_ENROLLMENT_WAFFLE),
    API_ASSOCIATE: is_enabled(API_PERMISSIONS_WAFFLE),
    API_PERMISSIONS: is_enabled(API_PERMISSIONS_WAFFLE),
    API_COURSE: is_enabled(API_COURSE_WAFFLE),
    API_STUDENT: is_enabled(API_STUDENT_WAFFLE),
}
