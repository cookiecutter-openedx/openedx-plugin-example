# coding=utf-8
"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Dec-2021

Management command to generate and persist Course Audit records.
"""
# python
import logging

# django
from django.core.management.base import BaseCommand, CommandError

# open edx
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview


# this repo
from openedx_plugin_cms.views.course_audit import persist_analyzed_course

log = logging.getLogger(__name__)


class Command(BaseCommand):
    """
        Management command to generate and persist Course Audit records.

    Example usage:
    ./manage.py cms audit_course -c course-v1:edX+DemoX+Demo_Course
    """

    help = """
    generate and persist/update Course Audit records.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            "--course-key",
            metavar="COURSE_KEY",
            dest="course_key",
            help="course run key. example: course-v1:edX+DemoX+Demo_Course",
        )

    def handle(self, *args, **options):
        course_key = options.get("course_key")
        if course_key:
            # Parse the serialized course key into a CourseKey
            try:
                course_key = CourseKey.from_string(course_key)
            except InvalidKeyError as e:
                raise CommandError("You must specify a valid course-key") from e

            persist_analyzed_course(course_key)
        else:
            courses = CourseOverview.objects.all()
            for course in courses:
                course_key = CourseKey.from_string(str(course))
                print("Analyzing course {course_key}".format(course_key=course_key))
                persist_analyzed_course(course_key)
