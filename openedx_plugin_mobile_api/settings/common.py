"""
Common Pluggable Django App settings

Handling of environment variables, see: https://django-environ.readthedocs.io/en/latest/
to convert .env to yml see: https://django-environ.readthedocs.io/en/latest/tips.html#docker-style-file-based-variables
"""
from path import Path as path
import environ
import os

# path to this file.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


APP_ROOT = (
    path(__file__).abspath().dirname().dirname()
)  # /blah/blah/blah/.../openedx-plugin-example/openedx_plugin_mobile_api
REPO_ROOT = APP_ROOT.dirname()  # /blah/blah/blah/.../openedx-plugin-example


def plugin_settings(settings):
    """
    Injects local settings into django settings

    see: https://stackoverflow.com/questions/56129708/how-to-force-redirect-uri-to-use-https-with-python-social-app
    """
    middleware = getattr(settings, "MIDDLEWARE", None)
    if middleware:
        settings.MIDDLEWARE.append("openedx_plugin_mobile_api.middleware.MobileApiRedirectMiddleware")
