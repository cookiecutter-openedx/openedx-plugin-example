"""
written by: Lawrence McDaniel
            https://lawrencemcdaniel.com

date:       dec-2022

usage:      Override select url end points defined in lms.urls.py
"""
import logging

from django.shortcuts import redirect

from .waffle import waffle_switches, OVERRIDE_MOBILE_USER_API_URL

log = logging.getLogger(__name__)

MOBILE_USER_API_URL = "/api/mobile/v1/users"


class MobileApiRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith(MOBILE_USER_API_URL) and waffle_switches[OVERRIDE_MOBILE_USER_API_URL]:
            log.info(
                "openedx_plugin_api.middleware.APIRedirectMiddleware.__call__() redirecting host: {host} path: {path}".format(
                    host=request.META["HTTP_HOST"], path=request.path
                )
            )
            return redirect("/openedx_plugin/api/mobile/user")

        # add more redirects here ...

        # the default response is whatever originally arrived to us
        return self.get_response(request)
