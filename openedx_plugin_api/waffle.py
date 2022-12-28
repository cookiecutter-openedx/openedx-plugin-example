from edx_toggles.toggles import WaffleSwitch

WAFFLE_NAMESPACE = "openedx_plugin_api"
# .. toggle_name: openedx_plugin_api.OVERRIDE_MOBILE_USER_API_URL_WAFFLE
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: This toggle will override the openedx mobile api url endpoint
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
OVERRIDE_MOBILE_USER_API_URL = f"{WAFFLE_NAMESPACE}.override_mobile_user_api_url"
OVERRIDE_MOBILE_USER_API_URL_WAFFLE = WaffleSwitch(OVERRIDE_MOBILE_USER_API_URL, module_name=__name__)


API_META = f"{WAFFLE_NAMESPACE}.meta"
API_META_WAFFLE = WaffleSwitch(API_META, module_name=__name__)

API_USERS = f"{WAFFLE_NAMESPACE}.users"
API_USERS_WAFFLE = WaffleSwitch(API_USERS, module_name=__name__)

API_TOKEN = f"{WAFFLE_NAMESPACE}.token"
API_TOKEN_WAFFLE = WaffleSwitch(API_TOKEN, module_name=__name__)

API_ENROLLMENT = f"{WAFFLE_NAMESPACE}.enrollment"
API_ENROLLMENT_WAFFLE = WaffleSwitch(API_ENROLLMENT, module_name=__name__)

API_ASSOCIATE = f"{WAFFLE_NAMESPACE}.associate"
API_ASSOCIATE_WAFFLE = WaffleSwitch(API_ASSOCIATE, module_name=__name__)

API_PERMISSIONS = f"{WAFFLE_NAMESPACE}.permissions"
API_PERMISSIONS_WAFFLE = WaffleSwitch(API_PERMISSIONS, module_name=__name__)

API_COURSE = f"{WAFFLE_NAMESPACE}.course"
API_COURSE_WAFFLE = WaffleSwitch(API_COURSE, module_name=__name__)

API_STUDENT = f"{WAFFLE_NAMESPACE}.student"
API_STUDENT_WAFFLE = WaffleSwitch(API_STUDENT, module_name=__name__)


def is_ready():
    try:
        # try to get the status of any arbitrary WaffleSwitch
        # if it doesn't raise an error then we're ready.
        API_STUDENT_WAFFLE.is_enabled()
        return True
    except Exception:
        # to resolve a race condition during application launch.
        # the waffle_switches are inspected before the db service
        # has initialized.
        return False


def is_enabled(switch: WaffleSwitch) -> bool:
    try:
        return switch.is_enabled()
    except Exception:
        # to resolve a race condition during application launch.
        # the waffle_switches are inspected before the db service
        # has initialized.
        return False


waffle_switches = {
    OVERRIDE_MOBILE_USER_API_URL: is_enabled(OVERRIDE_MOBILE_USER_API_URL_WAFFLE),
    API_META: is_enabled(API_META_WAFFLE),
    API_USERS: is_enabled(API_USERS_WAFFLE),
    API_TOKEN: is_enabled(API_TOKEN_WAFFLE),
    API_ENROLLMENT: is_enabled(API_ENROLLMENT_WAFFLE),
    API_ASSOCIATE: is_enabled(API_PERMISSIONS_WAFFLE),
    API_PERMISSIONS: is_enabled(API_PERMISSIONS_WAFFLE),
    API_COURSE: is_enabled(API_COURSE_WAFFLE),
    API_STUDENT: is_enabled(API_STUDENT_WAFFLE),
}
