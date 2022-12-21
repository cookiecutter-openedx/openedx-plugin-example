"""
Common Pluggable Django App settings
"""
from path import Path as path

APP_ROOT = path(__file__).abspath().dirname().dirname()  # /openedx_plugin_api
REPO_ROOT = APP_ROOT.dirname()  # openedx-plugin-example
TEMPLATES_DIR = APP_ROOT / "templates"


def plugin_settings(settings):
    """
    Injects local settings into django settings
    """
    # Add the template directory for this package to
    # to the search path for Mako.
    settings.MAKO_TEMPLATE_DIRS_BASE.extend([TEMPLATES_DIR])
    settings.INSTALLED_APPS.append("django_extensions")
