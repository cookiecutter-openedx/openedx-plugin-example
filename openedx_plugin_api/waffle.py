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


waffle_switches = {
    OVERRIDE_MOBILE_USER_API_URL: OVERRIDE_MOBILE_USER_API_URL_WAFFLE.is_enabled(),
    API_META: API_META_WAFFLE.is_enabled(),
    API_USERS: API_USERS_WAFFLE.is_enabled(),
    API_TOKEN: API_TOKEN_WAFFLE.is_enabled(),
    API_ENROLLMENT: API_ENROLLMENT_WAFFLE.is_enabled(),
    API_ASSOCIATE: API_PERMISSIONS_WAFFLE.is_enabled(),
    API_PERMISSIONS: API_PERMISSIONS_WAFFLE.is_enabled(),
    API_COURSE: API_COURSE_WAFFLE.is_enabled(),
    API_STUDENT: API_STUDENT_WAFFLE.is_enabled(),
}
