"""
Written by: Lawrence McDaniel
            https://lawrencemcdaniel.com

Date:   Feb-2022

Usage:  To enhance the behavior of the life cycle of the user session
"""
import json
import logging
from attr import asdict

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out

from openedx.core.djangoapps.user_authn.views.register import REGISTER_USER
from .utils import serialize_course_key, PluginJSONEncoder, masked_dict
from .waffle import waffle_switches, SIGNALS


log = logging.getLogger(__name__)
log.info("openedx_plugin.signals loaded")


def signals_enabled() -> bool:
    try:
        return waffle_switches[SIGNALS]
    except Exception:
        # to resolve a race condition during application launch.
        # the waffle_switches are inspected before the db service
        # has initialized.
        return False


"""
-------------------------------------------------------------------------------
------------------------------- LEGACY RECEIVERS ------------------------------
-------------------------------------------------------------------------------
"""


@receiver(user_logged_in, dispatch_uid="example_user_logged_in")
def post_login(sender, request, user, **kwargs):  # lint-amnesty, pylint: disable=unused-argument
    if not signals_enabled():
        return

    log.info("openedx_plugin received user_logged_in signal for {username}".format(username=user.username))


@receiver(user_logged_out, dispatch_uid="example_user_logged_out")
def post_logout(sender, request, user, **kwargs):  # lint-amnesty, pylint: disable=unused-argument
    if not signals_enabled():
        return

    log.info("openedx_plugin received user_logged_out signal for {username}".format(username=user.username))


@receiver(REGISTER_USER, dispatch_uid="example_REGISTER_USER")
def register_user(sender, user, registration, **kwargs):  # pylint: disable=unused-argument
    if not signals_enabled():
        return

    log.info("openedx_plugin received REGISTER_USER signal for {username}".format(username=user.username))


"""
-------------------------------------------------------------------------------
--------------------------- NEW STYLE OF RECEIVER -----------------------------
-------------------- https://github.com/openedx/openedx-events ----------------
-------------------------------------------------------------------------------

    Reference:  edx-platform/docs/guides/hooks/
                https://github.com/openedx/openedx-events

    I scaffolded these from https://github.com/eduNEXT/openedx-events-2-zapier

"""


def student_registration_completed(user, **kwargs):  # pylint: disable=unused-argument
    """

    see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
    signal_path: openedx_events.learning.signals.STUDENT_REGISTRATION_COMPLETED
    https://github.com/openedx/openedx-events/blob/main/openedx_events/learning/signals.py#L25

    event_type: org.openedx.learning.student.registration.completed.v1
    event_name: STUDENT_REGISTRATION_COMPLETED
    event_description: emitted when the user registration process in the LMS is completed.
    event_data: UserData

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
    if not signals_enabled():
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


def session_login_completed(user, **kwargs):
    """
    see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
    signal_path: openedx_events.learning.signals.SESSION_LOGIN_COMPLETED
    https://github.com/openedx/openedx-events/blob/main/openedx_events/learning/signals.py#L37

    event_type: org.openedx.learning.auth.session.login.completed.v1
    event_name: SESSION_LOGIN_COMPLETED
    event_description: emitted when the user's login process in the LMS is completed.
    event_data: UserData

    """
    if not signals_enabled():
        return

    user_info = asdict(user)
    event_metadata = asdict(kwargs.get("metadata"))
    payload = {
        "user": user_info,
        "event_metadata": event_metadata,
    }

    log.info(
        "openedx_plugin received SESSION_LOGIN_COMPLETED signal for {payload}".format(
            payload=json.dumps(masked_dict(payload), cls=PluginJSONEncoder, indent=4)
        )
    )


def course_enrollment_created(enrollment, **kwargs):
    """

    see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
    signal_path: openedx_events.learning.signals.COURSE_ENROLLMENT_CREATED
    https://github.com/openedx/openedx-events/blob/main/openedx_events/learning/signals.py#L49

    event_type: org.openedx.learning.course.enrollment.created.v1
    event_name: COURSE_ENROLLMENT_CREATED
    event_description: emitted when the user's enrollment process is completed.
    event_data: CourseEnrollmentData

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
    if not signals_enabled():
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


def course_enrollment_changed(enrollment, **kwargs):
    """

    see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
    signal_path: openedx_events.learning.signals.COURSE_ENROLLMENT_CHANGED
    https://github.com/openedx/openedx-events/blob/main/openedx_events/learning/signals.py#L61

    event_type: org.openedx.learning.course.enrollment.changed.v1
    event_name: COURSE_ENROLLMENT_CHANGED
    event_description: emitted when the user's enrollment update process is completed.
    event_data: CourseEnrollmentData

    """
    if not signals_enabled():
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


def course_unenrollment_completed(enrollment, **kwargs):
    """
    see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
    signal_path: openedx_events.learning.signals.COURSE_UNENROLLMENT_COMPLETED
    https://github.com/openedx/openedx-events/blob/main/openedx_events/learning/signals.py#L73

    event_type: org.openedx.learning.course.unenrollment.completed.v1
    event_name: COURSE_UNENROLLMENT_COMPLETED
    event_description: emitted when the user's unenrollment process is completed.
    event_data: CourseEnrollmentData

    """
    if not signals_enabled():
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
        "openedx_plugin received COURSE_UNENROLLMENT_COMPLETED signal for {payload}".format(
            payload=json.dumps(masked_dict(payload), cls=PluginJSONEncoder, indent=4)
        )
    )


def certificate_created(certificate, **kwargs):
    """
    see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
    signal_path: openedx_events.learning.signals.COURSE_UNENROLLMENT_COMPLETED
    https://github.com/openedx/openedx-events/blob/main/openedx_events/learning/signals.py#L85

    event_type: org.openedx.learning.certificate.created.v1
    event_name: CERTIFICATE_CREATED
    event_description: emitted when the user's certificate creation process is completed.
    event_data: CertificateData

    """
    if not signals_enabled():
        return

    certificate_info = asdict(
        certificate,
        value_serializer=serialize_course_key,
    )
    event_metadata = asdict(kwargs.get("metadata"))
    payload = {
        "certificate": certificate_info,
        "event_metadata": event_metadata,
    }

    log.info(
        "openedx_plugin received CERTIFICATE_CREATED signal for {payload}".format(
            payload=json.dumps(masked_dict(payload), cls=PluginJSONEncoder, indent=4)
        )
    )


def certificate_changed(certificate, **kwargs):
    """
    see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
    signal_path: openedx_events.learning.signals.CERTIFICATE_CHANGED
    https://github.com/openedx/openedx-events/blob/main/openedx_events/learning/signals.py#L97

    event_type: org.openedx.learning.certificate.changed.v1
    event_name: CERTIFICATE_CHANGED
    event_description: emitted when the user's certificate update process is completed.
    event_data: CertificateData
    """
    if not signals_enabled():
        return

    certificate_info = asdict(
        certificate,
        value_serializer=serialize_course_key,
    )
    event_metadata = asdict(kwargs.get("metadata"))
    payload = {
        "certificate": certificate_info,
        "event_metadata": event_metadata,
    }

    log.info(
        "openedx_plugin received CERTIFICATE_CHANGED signal for {payload}".format(
            payload=json.dumps(masked_dict(payload), cls=PluginJSONEncoder, indent=4)
        )
    )


def certificate_revoked(certificate, **kwargs):
    """

    see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
    signal_path: openedx_events.learning.signals.CERTIFICATE_REVOKED
    https://github.com/openedx/openedx-events/blob/main/openedx_events/learning/signals.py#L109

    event_type: org.openedx.learning.certificate.revoked.v1
    event_name: CERTIFICATE_REVOKED
    event_description: emitted when the user's certificate annulation process is completed.
    event_data: CertificateData
    """
    if not signals_enabled():
        return

    certificate_info = asdict(
        certificate,
        value_serializer=serialize_course_key,
    )
    event_metadata = asdict(kwargs.get("metadata"))
    payload = {
        "certificate": certificate_info,
        "event_metadata": event_metadata,
    }

    log.info(
        "openedx_plugin received CERTIFICATE_REVOKED signal for {payload}".format(
            payload=json.dumps(masked_dict(payload), cls=PluginJSONEncoder, indent=4)
        )
    )


def persistent_grade_summary_changed(grade, **kwargs):
    """

    see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
    signal_path: openedx_events.learning.signals.PERSISTENT_GRADE_SUMMARY_CHANGED
    https://github.com/openedx/openedx-events/blob/main/openedx_events/learning/signals.py#L145

    event_type: org.openedx.learning.course.persistent_grade.summary.v1
    event_name: PERSISTENT_GRADE_SUMMARY_CHANGED
    event_description: emitted when a grade changes in the course
    event_data: PersistentCourseGradeData

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
    if not signals_enabled():
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


def cohort_membership_changed(cohort, **kwargs):
    """

    see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
    signal_path: openedx_events.learning.signals.COHORT_MEMBERSHIP_CHANGED
    https://github.com/openedx/openedx-events/blob/main/openedx_events/learning/signals.py#L121

    event_type: org.openedx.learning.cohort_membership.changed.v1
    event_name: COHORT_MEMBERSHIP_CHANGED
    event_description: emitted when the user's cohort update is completed.
    event_data: CohortData

    """
    if not signals_enabled():
        return

    cohort_info = asdict(
        cohort,
        value_serializer=serialize_course_key,
    )
    event_metadata = asdict(kwargs.get("metadata"))
    payload = {
        "cohort": cohort_info,
        "event_metadata": event_metadata,
    }

    log.info(
        "openedx_plugin received COHORT_MEMBERSHIP_CHANGED signal for {payload}".format(
            payload=json.dumps(masked_dict(payload), cls=PluginJSONEncoder, indent=4)
        )
    )


def course_discussions_changed(configuration, **kwargs):  # lint-amnesty, pylint: disable=unused-argument
    """
    see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
    signal_path: openedx_events.learning.signals.COHORT_MEMBERSHIP_CHANGED
    https://github.com/openedx/openedx-events/blob/main/openedx_events/learning/signals.py#L145

    event_type: org.openedx.learning.discussions.configuration.changed.v1
    event_name: COURSE_DISCUSSIONS_CHANGED
    event_description: emitted when the configuration for a course's discussions changes in the course
                       Warning: This event is currently incompatible with the event bus, list/dict cannot be serialized yet
    event_data: CourseDiscussionConfigurationData

    """
    if not signals_enabled():
        return

    log.info("openedx_plugin received COURSE_DISCUSSIONS_CHANGED signal")
