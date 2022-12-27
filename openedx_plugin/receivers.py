"""
Written by: Lawrence McDaniel
            https://lawrencemcdaniel.com

Date:   Feb-2022

Usage:  To enhance the behavior of the life cycle of the user session
"""
import json
import logging

import requests
from attr import asdict

from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out

from openedx.core.djangoapps.user_authn.views.register import REGISTER_USER

from .utils import serialize_course_key, PluginJSONEncoder, masked_dict
from .waffle import waffle_switches, RECEIVERS

log = logging.getLogger(__name__)

# coming in Maple
# from openedx_events.learning.signals import SESSION_LOGIN_COMPLETED


"""
-------------------------------------------------------------------------------
------------------------------- LEGACY RECEIVERS ------------------------------
-------------------------------------------------------------------------------
"""


@receiver(user_logged_in, dispatch_uid="example_user_logged_in")
def post_login(sender, request, user, **kwargs):  # lint-amnesty, pylint: disable=unused-argument
    if not waffle_switches[RECEIVERS]:
        return

    log.info("openedx_plugin received user_logged_in signal for {username}".format(username=user.username))


@receiver(user_logged_out, dispatch_uid="example_user_logged_out")
def post_logout(sender, request, user, **kwargs):  # lint-amnesty, pylint: disable=unused-argument
    if not waffle_switches[RECEIVERS]:
        return

    log.info("openedx_plugin received user_logged_out signal for {username}".format(username=user.username))


@receiver(REGISTER_USER, dispatch_uid="example_REGISTER_USER")
def register_user(sender, user, registration, **kwargs):  # pylint: disable=unused-argument
    if not waffle_switches[RECEIVERS]:
        return

    log.info("openedx_plugin received REGISTER_USER signal for {username}".format(username=user.username))


"""
-------------------------------------------------------------------------------
--------------------------- NEW STYLE OF RECEIVER -----------------------------
-------------------------------------------------------------------------------

    Reference:  edx-platform/docs/guides/hooks/

    I scaffolded these from https://github.com/eduNEXT/openedx-events-2-zapier

"""


def student_registration_completed(user, **kwargs):  # pylint: disable=unused-argument
    """

    see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
    signal_path: openedx_events.learning.signals.STUDENT_REGISTRATION_COMPLETED

    example user and kwargs data:
    'user_id': 39,
    'user_is_active': True,
    'user_pii_username': 'test',
    'user_pii_email': 'test@example.com',
    'user_pii_name': 'test',
    'event_metadata_id': UUID('b1be2fac-1af1-11ec-bdf4-0242ac12000b'),
    'event_metadata_event_type': 'org.openedx.learning.student.registration.completed.v1',
    'event_metadata_minorversion': 0,
    'event_metadata_source': 'openedx/lms/web',
    'event_metadata_sourcehost': 'lms.devstack.edx',
    'event_metadata_time': datetime.datetime(2021, 9, 21, 15, 36, 31, 311506),
    'event_metadata_sourcelib': [0, 6, 0]

    """
    if not waffle_switches[RECEIVERS]:
        return

    user_info = asdict(user)
    event_metadata = asdict(kwargs.get("metadata"))
    payload = {
        "user": user_info,
        "event_metadata": event_metadata,
    }

    log.info(
        "openedx_plugin received STUDENT_REGISTRATION_COMPLETED signal for {payload}".format(
            payload=json.dumps(masked_dict(payload), cls=PluginJSONEncoder, indent=4)
        )
    )


def course_enrollment_created(enrollment, **kwargs):
    """

    see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
    signal_path: openedx_events.learning.signals.COURSE_ENROLLMENT_CREATED

    example enrollment and kwargs data:
    'enrollment_user_id': 42,
    'enrollment_user_is_active': True,
    'enrollment_user_pii_username': 'test',
    'enrollment_user_pii_email': 'test@example.com',
    'enrollment_user_pii_name': 'test',
    'enrollment_course_course_key': 'course-v1:edX+100+2021',
    'enrollment_course_display_name':'Demonstration Course',
    'enrollment_course_start': None,
    'enrollment_course_end': None,
    'enrollment_mode':
    'audit', 'enrollment_is_active': True,
    'enrollment_creation_date': datetime.datetime(2021, 9, 21, 17, 40, 27, 401427, tzinfo=<UTC>),
    'enrollment_created_by': None,
    'event_metadata_id': UUID('02672f60-1b03-11ec-953b-0242ac12000b'),
    'event_metadata_event_type': 'org.openedx.learning.course.enrollment.created.v1',
    'event_metadata_minorversion': 0,
    'event_metadata_source': 'openedx/lms/web',
    'event_metadata_sourcehost': 'lms.devstack.edx',
    'event_metadata_time': datetime.datetime(2021, 9, 21, 17, 40, 28, 81160),
    'event_metadata_sourcelib': [0, 6, 0]

    """
    if not waffle_switches[RECEIVERS]:
        return

    enrollment_info = asdict(
        enrollment,
        value_serializer=serialize_course_key,
    )
    event_metadata = asdict(kwargs.get("metadata"))
    payload = {
        "enrollment": enrollment_info,
        "event_metadata": event_metadata,
    }

    log.info(
        "openedx_plugin received COURSE_ENROLLMENT_CREATED signal for {payload}".format(
            payload=json.dumps(masked_dict(payload), cls=PluginJSONEncoder, indent=4)
        )
    )


def persistent_grade_summary_changed(grade, **kwargs):
    """

    see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
    signal_path: openedx_events.learning.signals.PERSISTENT_GRADE_SUMMARY_CHANGED

    example grade and kwargs data:
    'grade_user_id': 42,
    'grade_course_course_key': 'course-v1:edX+100+2021',
    'grade_course_display_name': 'Demonstration Course',
    'grade_course_edited_timestamp': datetime.datetime(2021, 9, 21, 17, 40, 27),
    'grade_course_version': '',
    'grade_grading_policy_hash': '',
    'grade_percent_grade': 80,
    'grade_letter_grade': 'Great',
    'grade_passed_timestamp': datetime.datetime(2021, 9, 21, 17, 40, 27),
    'event_metadata_id': UUID('b1be2fac-1af1-11ec-bdf4-0242ac12000b'),
    'event_metadata_event_type': 'org.openedx.learning.student.registration.completed.v1',
    'event_metadata_minorversion': 0,
    'event_metadata_source': 'openedx/lms/web',
    'event_metadata_sourcehost': 'lms.devstack.edx',
    'event_metadata_time': datetime.datetime(2021, 9, 21, 15, 36, 31, 311506),
    'event_metadata_sourcelib': [0, 6, 0]

    """
    if not waffle_switches[RECEIVERS]:
        return

    grade_info = asdict(
        grade,
        value_serializer=serialize_course_key,
    )
    event_metadata = asdict(kwargs.get("metadata"))
    payload = {
        "grade": grade_info,
        "event_metadata": event_metadata,
    }
    log.info(
        "openedx_plugin received COURSE_ENROLLMENT_CREATED signal for {payload}".format(
            payload=json.dumps(masked_dict(payload), cls=PluginJSONEncoder, indent=4)
        )
    )
