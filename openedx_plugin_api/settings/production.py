"""
Common Pluggable Django App settings
"""


def plugin_settings(settings):
    """
    Injects local settings into django settings
    """

    middleware = getattr(settings, "MIDDLEWARE", None)
    if middleware:
        settings.MIDDLEWARE.append("openedx_plugin_api.middleware.APIRedirectMiddleware")
