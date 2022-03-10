"""
Written by: Lawrence McDaniel
            https://lawrencemcdaniel.com

Date:   Feb-2022

Usage:  To intercept http requests so that can do things like:
            - set environment variables, like the language code
            - redirect the user elsewhere, like say, an onboarding page
            - update user profile data
"""
import logging
from urllib.parse import urlparse

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from opaque_keys.edx.keys import CourseKey
from common.djangoapps.student.models import CourseEnrollment
from xmodule.modulestore.django import modulestore


from .utils import set_language_preference

log = logging.getLogger(__name__)


@login_required
@ensure_csrf_cookie
def student_dashboard(request):
    """
    Called from Wordpress marketing sites. Facilitates some preprocessing
    prior to opening the Open edX dashboard view.

    Defined params:
    "language": the default language for this referrer. example: es-419
    "enroll": a CourseKey. we should attempt to enroll the user in this course

    example url:
    https://lms.example.edu/example/dashboard?language=en-US&enroll=course-v1%3AedX%2BDemoX%2BDemo_Course
    """

    enroll_in = request.GET.get("enroll")
    language_param = request.GET.get("language")
    username = request.user.username
    platform = request.META.get("HTTP_SEC_CH_UA_PLATFORM") or request.META.get("HTTP_USER_AGENT")
    referer = urlparse(request.META.get("HTTP_REFERER", "Direct"))
    # host = request.META.get("HTTP_HOST")

    # this is a sneaky way of inferring that the user had to authenticate
    # while en route to this view, due to the @login_required.
    if referer.netloc == "lms.example.edu":
        log.info(
            "student_dashboard() - initiating after user authentication for {username}".format(
                username=request.user.username
            )
        )
    else:
        log.info("student_dashboard() - initiating after referal {referer}".format(referer=referer.netloc))

    log.info(
        "student_dashboard() - user {username} is accessing example via {platform}. Referer is {referer}. Received a language preference of {language_param} and a pre-enrollment course key of {enroll_in}".format(
            username=username,
            platform=platform,
            referer=referer.netloc,
            language_param=language_param,
            enroll_in=enroll_in,
        )
    )

    # should always be true, but it'd potentially be a trainwreck if we called
    # set_language_preference() at scale on the Django anonymous user.
    # so, qualifying the authentication just in case :O
    if request.user and request.user.is_authenticated:
        set_language_preference(request)

    # if there's an ´enroll´ param then parse it and try to enroll the the user in the course
    if enroll_in:
        log.info("student_dashboard() received enroll param of {enroll_in}".format(enroll_in=enroll_in))

        course_key = None
        course = None

        try:
            course_key = CourseKey.from_string(enroll_in)
        except Exception:
            log.warning(
                "student_dashboard() received an invalid CourseKey string in the enroll url param. Ignoring. value was: {enroll_in}".format(
                    enroll_in=enroll_in
                )
            )

        if course_key:
            try:
                course = modulestore().get_course(course_key)
            except Exception as e:
                log.warning(
                    "student_dashboard() encountered a handled exception while attempting to initialize course object for course key {enroll_in}. Exception: {e}".format(
                        enroll_in=enroll_in, e=e
                    )
                )

            try:
                if not CourseEnrollment.is_enrolled(request.user, course_key=course_key):
                    CourseEnrollment.enroll(request.user, course_key=course_key)
                else:
                    log.info(
                        "student_dashboard() user {username} is already enrolled in course {enroll_in}.".format(
                            username=request.user.username, enroll_in=enroll_in
                        )
                    )

                if course.has_started():
                    return redirect(reverse("openedx.course_experience.course_home", kwargs={"course_id": course_key}))
                else:
                    log.info(
                        "student_dashboard() course {enroll_in} has not yet started. Redirecting the user to their dashboard.".format(
                            enroll_in=enroll_in
                        )
                    )

            except Exception as e:
                log.warning(
                    "student_dashboard() encountered a handled exception while attempting to enroll user {username} in the course {enroll_in}. Exception: {e}".format(
                        username=request.user.username, enroll_in=enroll_in, e=e
                    )
                )

    return redirect(reverse("dashboard"))
