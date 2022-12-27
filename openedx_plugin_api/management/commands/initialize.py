import os
import logging
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from oauth2_provider.models import Application
from openedx.core.djangoapps.api_admin.models import (
    ApiAccessConfig,
    ApiAccessRequest,
)

logger = logging.getLogger(__name__)
PLUGIN_API_USER_NAME = os.environ.get("PLUGIN_API_USER_NAME")
PLUGIN_API_USER_EMAIL = os.environ.get("PLUGIN_API_USER_EMAIL")
PLUGIN_API_USER_PASSWORD = os.environ.get("PLUGIN_API_USER_PASSWORD")
OPENEDX_CLIENT_ID = os.environ.get("OPENEDX_CLIENT_ID")
OPENEDX_CLIENT_SECRET = os.environ.get("OPENEDX_CLIENT_SECRET")
OPENEDX_COMPLETE_DOMAIN_NAME = os.environ.get("OPENEDX_COMPLETE_DOMAIN_NAME")


class Command(BaseCommand):
    help = "Bootstrap the Plugin API"

    def handle(self, *args, **options):
        if not all(
            [
                PLUGIN_API_USER_EMAIL,
                PLUGIN_API_USER_NAME,
                PLUGIN_API_USER_PASSWORD,
                OPENEDX_COMPLETE_DOMAIN_NAME,
            ]
        ):
            raise Exception("Missing required parameters")
        logger.info("Assert API user")
        user, created = get_user_model().objects.get_or_create(
            username=PLUGIN_API_USER_NAME, defaults={"email": PLUGIN_API_USER_EMAIL}
        )
        user.set_password(PLUGIN_API_USER_PASSWORD)
        user.save()

        logger.info("Assert API access")
        self.api_access()

        logger.info("Retrieve the client id and secret via the Admin")

    def api_access(self):
        site, _ = Site.objects.get_or_create(domain=OPENEDX_COMPLETE_DOMAIN_NAME)
        config = ApiAccessConfig.objects.filter(enabled=True).first()
        if not config:
            config = ApiAccessConfig(enabled=True)
            config.save()
        user = User.objects.get(username=PLUGIN_API_USER_NAME)
        try:
            access = ApiAccessRequest.objects.get(user=user)
        except ApiAccessRequest.DoesNotExist:
            access = ApiAccessRequest()
        access.user = user
        access.status = ApiAccessRequest.APPROVED
        access.website = OPENEDX_COMPLETE_DOMAIN_NAME
        access.site = site
        access.reason = "Created from bootsrap script"
        access.save()
        application, _ = Application.objects.get_or_create(
            user=user,
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
            client_type=Application.CLIENT_CONFIDENTIAL,
        )
        if OPENEDX_CLIENT_ID and OPENEDX_CLIENT_SECRET:
            application.client_id = OPENEDX_CLIENT_ID
            application.client_secret = OPENEDX_CLIENT_SECRET
        application.save()
