# encoding: UTF-8
# python stuff
import re
from secure_logger.decorators import secure_logger

# django stuff
from django.shortcuts import redirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

# our stuff
from .waffle import waffle_switches, OVERRIDE_MOBILE_USER_API_URL
from .const import PLUGIN_URL_PREFIX

# r'^/api/mobile/(?P<api_version>v(1|0.5))/users/(?P<username>[\\w .@_+-]+)(.+)$'
MOBILE_API_USER_DETAIL_PATTERN = (
    r"^/api/mobile/(?P<api_version>v(1|0.5))/" + "users/" + settings.USERNAME_PATTERN + "(.+)$"
)


class MobileApiRedirectMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        redirect a request from edx-platform to this app
        see: https://stackoverflow.com/questions/42614172/how-to-redirect-from-a-view-to-another-view-in-django
        """
        request_path = request.get_full_path()

        if re.match(MOBILE_API_USER_DETAIL_PATTERN, request_path) and waffle_switches[OVERRIDE_MOBILE_USER_API_URL]:
            # original path:                 /api/mobile/v1/users/admin?custom_param='foo'
            # redirect path:  /openedx_plugin/api/mobile/v1/users/admin?custom_param='foo'
            redirect_path = "/" + PLUGIN_URL_PREFIX + request_path
            response = self.redirector(request_path=request_path, redirect_path=redirect_path)
            return response

        response = self.get_response(request)
        return response

    @secure_logger()
    def redirector(self, request_path, redirect_path):
        """
        Notes: creating a 'permanent' redirect so that we return a 301 response which
        might help to reduce the actual number of times this gets called.

        see tests/command_line.sh for sample usage of curl with these endpoints
        """
        response = redirect(redirect_path, permanent=True)
        return response
