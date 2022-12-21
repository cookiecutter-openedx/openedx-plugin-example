import logging

from django.shortcuts import redirect
from django.conf import settings

import urllib.parse

log = logging.getLogger(__name__)


class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            return response

        # mcdaniel aug-2022:
        #   we should only redirect lms logins.
        #   requests from other applications like say, studio or mfe authenticate
        #   via internal oauth to the lms.
        if request.META["HTTP_HOST"] not in [settings.OPENEDX_COMPLETE_DOMAIN_NAME]:
            return response

        if request.path.startswith("/login"):
            log.info(
                "plugin_api.middleware.LoginRedirectMiddleware.__call__() evaluating host: {host} path: {path} next: {next}".format(
                    host=request.META["HTTP_HOST"], path=request.path, next=request.GET.get("next", "")
                )
            )

            if "next" in request.GET:
                # mcdaniel aug-2022:
                # we should avoid logins to the Django admin page. these cause
                # "too many redirects" errors.
                # https://staging.global-communications-academy.com/login?next=/admin
                if request.GET.get("next", "") == "/admin":
                    return response

                return redirect(
                    "/auth/login/custom-oauth/?auth_entry=login&next=" + urllib.parse.quote(request.GET["next"])
                )
            return redirect("/auth/login/custom-oauth/?auth_entry=login&next=/")

        return response
