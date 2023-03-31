# coding=utf-8
"""
Common Pluggable Django App settings
"""

from ..waffle import waffle_switches, OVERRIDE_OPENEDX_DJANGO_LOGIN


def plugin_settings(settings):
    """
    Injects local settings into django settings
    """
    if waffle_switches[OVERRIDE_OPENEDX_DJANGO_LOGIN]:
        middleware = getattr(settings, "MIDDLEWARE", None)
        if middleware:
            settings.MIDDLEWARE.append("openedx_plugin.middleware.RedirectDjangoAdminMiddleware")
