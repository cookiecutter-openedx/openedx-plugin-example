from edx_toggles.toggles import WaffleSwitch

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

waffle_switches = {
    AUDIT_REPORT: AUDIT_REPORT_WAFFLE.is_enabled,
}
