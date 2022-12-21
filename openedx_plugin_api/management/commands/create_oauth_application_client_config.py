from argparse import RawTextHelpFormatter
import os

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings
from common.djangoapps.third_party_auth.models import OAuth2ProviderConfig


class Command(BaseCommand):
    help = """Create Custom OAuth application config

This will create the OAuthProviderConfig for the OAuth provider
it should use the same client ID and secret used when creating the
OAuth application in the authentication host. 

These values will either need to be set in settings or as envs
    EXAMPLE_CLIENT_ID - client ID defined in Host OAuth provider
    EXAMPLE_CLIENT_SECRET - client secret defined in Host OAuth provider
    OPENEDX_COMPLETE_DOMAIN_NAME - the domain (including subdomains) of this Open edX instance
    """

    def create_parser(self, *args, **kwargs):
        parser = super(Command, self).create_parser(*args, **kwargs)
        parser.formatter_class = RawTextHelpFormatter
        return parser

    def handle(self, *args, **options):
        key = getattr(settings, "EXAMPLE_CLIENT_ID", os.environ.get("EXAMPLE_CLIENT_ID"))
        secret = getattr(settings, "EXAMPLE_CLIENT_SECRET", os.environ.get("EXAMPLE_CLIENT_SECRET"))
        domain = getattr(settings, "OPENEDX_COMPLETE_DOMAIN_NAME", os.environ.get("OPENEDX_COMPLETE_DOMAIN_NAME"))

        site, _ = Site.objects.get_or_create(domain=domain)
        OAuth2ProviderConfig.objects.get_or_create(
            enabled=True,
            icon_class="fa-sign-in",
            name="EXAMPLE_HOST",
            slug="default",
            secondary=False,
            site=site,
            skip_hinted_login_dialog=True,
            skip_registration_form=True,
            skip_email_verification=True,
            send_welcome_email=False,
            visible=True,
            send_to_registration_first=False,
            sync_learner_profile_data=True,
            enable_sso_id_verification=True,
            backend_name="custom-oauth",
            key=key,
            secret=secret,
        )
