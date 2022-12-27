import logging

from django.shortcuts import redirect
from django.conf import settings

from edx_toggles.toggles import WaffleSwitch

log = logging.getLogger(__name__)

# define a Waffle flag for toggling whether to override the stock openedx api functionality
OVERRIDE_OPENEDX_API_SWITCH = WaffleSwitch('openedx_plugin_example.override_openedx_api', "openedx_plugin_api")


class APIRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # require a Waffle flag to enable overrides of the stock openedx api functionality
        if not OVERRIDE_OPENEDX_API_SWITCH.is_enabled:
            return self.get_response(request)

        if request.path.startswith("/path/to/api/endpoint-to-override"):
            log.info(
                "openedx_plugin_api.middleware.APIRedirectMiddleware.__call__() redirecting host: {host} path: {path}".format(
                    host=request.META["HTTP_HOST"], path=request.path
                )
            )
            return redirect("/auth/login/custom-oauth/")
        return self.get_response(request)
