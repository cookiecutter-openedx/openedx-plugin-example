"""
Written by: Lawrence McDaniel
            https://lawrencemcdaniel.com

Date:   Feb-2022

Usage:  To enhance the behavior of the life cycle of the user session
"""
import logging

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

AUDIT_LOG = logging.getLogger("audit")

# coming in Maple
# from openedx_events.learning.signals import SESSION_LOGIN_COMPLETED


@receiver(user_logged_in, dispatch_uid="example_user_logged_in")
def post_login(sender, request, user, **kwargs):  # lint-amnesty, pylint: disable=unused-argument
    AUDIT_LOG.info("openedx_plugin received user_logged_in signal for {username}".format(username=user.username))


@receiver(user_logged_out, dispatch_uid="example_user_logged_out")
def post_logout(sender, request, user, **kwargs):  # lint-amnesty, pylint: disable=unused-argument
    AUDIT_LOG.info("openedx_plugin received user_logged_out signal for {username}".format(username=user.username))
