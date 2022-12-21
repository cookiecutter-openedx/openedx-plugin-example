"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2021

Management command to force evaluation of a course, to log any recent
changes to the change log.
"""
# python
import logging

# django
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

# open edx
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey

# this repo
from openedx_plugin_cms.auditor import eval_course_block_changes

User = get_user_model()
log = logging.getLogger(__name__)


class Command(BaseCommand):
    """
        Management command to force evaluation of a course, to log any recent
        changes to the change log.

    Example usage:
    ./manage.py cms eval_course -c course-v1:edX+DemoX+Demo_Course
    """

    help = """
    evaluate a course to log any recent changes to the change log.
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
        if not course_key:
            raise CommandError("You must specify a course-key")

        # Parse the serialized course key into a CourseKey
        try:
            course_key = CourseKey.from_string(course_key)
        except InvalidKeyError as e:
            raise CommandError("You must specify a valid course-key") from e

        eval_course_block_changes(course_key, user=None)
