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

# .. toggle_name: openedx_plugin.receivers
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: adds hooks for Django receivers (ie Signals)
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
RECEIVERS = f"{WAFFLE_NAMESPACE}.receivers"
RECEIVERS_WAFFLE = WaffleSwitch(RECEIVERS, module_name=__name__)


waffle_switches = {
    SIMPLE_REST_API: SIMPLE_REST_API_WAFFLE.is_enabled,
    OVERRIDE_OPENEDX_DJANGO_LOGIN: OVERRIDE_OPENEDX_DJANGO_LOGIN_WAFFLE.is_enabled,
    AUTOMATED_ENROLLMENT: AUTOMATED_ENROLLMENT_WAFFLE.is_enabled,
    MARKETING_REDIRECTOR: MARKETING_REDIRECTOR_WAFFLE.is_enabled,
    RECEIVERS: RECEIVERS_WAFFLE.is_enabled,
}
