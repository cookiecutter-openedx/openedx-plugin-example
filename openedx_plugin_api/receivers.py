"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

Listen for signals published by edxapp.
"""

# Python
import logging
import requests

# Django
from django.dispatch import receiver
from django.conf import settings

# Open edX
from openedx.core.djangoapps.signals.signals import COURSE_GRADE_NOW_PASSED

# this repo

log = logging.getLogger(__name__)


@receiver(COURSE_GRADE_NOW_PASSED, dispatch_uid="plugin_passing_learner")
def listen_for_passing_grade(sender, user, course_id, **kwargs):  # pylint: disable=unused-argument
    """
    Listen for a signal indicating that the user has passed a course run.
    """
    log.info(
        "Enrolled student {username} has achieved a passing grade in the course {course_id} [{kwargs}]".format(
            username=user.username, course_id=course_id, kwargs=kwargs
        )
    )
    headers = {"Authorization": f"Token {settings.CUSTOM_API_USER_API_KEY}"}
    response = requests.post(
        f"{settings.OAUTH_HOST_BASE_URL}/api/course/{course_id}/user/{user.username}/grade/yes/", headers=headers
    )

    try:
        log.info(f"-> Recorded: {response.json()}")
    except Exception as e:
        log.error("error while attempting to write to the app log: {err}".format(err=e))
