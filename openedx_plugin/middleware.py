# coding=utf-8
"""
written by: Lawrence McDaniel
            https://lawrencemcdaniel.com

date:       dec-2022

usage:      scaffolding to override the Django Admin login page defined in
            lms.urls.py Nutmeg releases and later remove the Django admin
            login page, redirecting the user to the unified openedx
            logistration page instead.

            This middleware reverts to the default Django Admin login
            screen by intercepting requests to the path 'admin/login' and
            forcefully redering and returning the original Django login
            page template.
"""
import logging

from django.http import HttpResponse
from django.template import loader, Context

from .waffle import waffle_switches, OVERRIDE_OPENEDX_DJANGO_LOGIN

log = logging.getLogger(__name__)

WAFFLE_NAMESPACE = "openedx_plugin"
# .. toggle_name: openedx_plugin.override_lms_django_admin_login
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: This toggle will revert the Django Admin login page to the original Django default
# .. toggle_warnings:
# .. toggle_use_cases:
# .. toggle_creation_date: 2022-12-27
OPENEDX_DJANGO_LOGIN_URL = "/admin/login"


class RedirectDjangoAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # require a Waffle flag to enable overrides of the stock openedx api functionality
        if request.path.startswith(OPENEDX_DJANGO_LOGIN_URL) and waffle_switches[OVERRIDE_OPENEDX_DJANGO_LOGIN]:
            log.info(
                "openedx_plugin.middleware.RedirectDjangoAdminMiddleware.__call__() redirecting host: {host} path: {path}".format(
                    host=request.META["HTTP_HOST"], path=request.path
                )
            )
            template = loader.get_template("admin/login.html")
            context = Context({})
            return HttpResponse(template.render(context, request))
        return self.get_response(request)
