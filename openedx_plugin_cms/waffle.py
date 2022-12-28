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
