# coding=utf-8
"""
written by:     Lawrence McDaniel
                https://lawrencemcdaniel.com

date:           sep-2021

usage:          Listen for Django signals published by edxapp
                see https://docs.djangoproject.com/en/4.1/topics/signals/
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
log.info("openedx_plugin_api.signals loaded")


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
