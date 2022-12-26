"""
Common Pluggable Django App settings
"""
import os


def plugin_settings(settings):
    """
    Injects local settings into django settings
    """

    middleware = getattr(settings, "MIDDLEWARE", None)
    if middleware:
        settings.MIDDLEWARE.append("plugin_api.middleware.APIRedirectMiddleware")

    settings.OAUTH_HOST_BASE_URL = getattr(settings, "OAUTH_HOST_BASE_URL", "http://YOURDOMAIN.EDU")
