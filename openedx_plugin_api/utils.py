from datetime import datetime
from pytz import UTC
import re

from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from openedx.core.djangoapps.user_api.accounts.utils import (
    retrieve_last_sitewide_block_completed,
)
from opaque_keys.edx.keys import CourseKey
from common.djangoapps.util.date_utils import get_default_time_display
from common.lib.xmodule.xmodule.modulestore.django import modulestore


def get_course_info(course_key: CourseKey):
    """
    Generate a verbose json object of course
    descriptive and meta data.

    editorial comment: you can create a course key in
    Django shell as follows:
    ----------------
    from opaque_keys.edx.keys import CourseKey
    course_key_str = "course-v1:edX+DemoX+Demo_Course"
    course_key = CourseKey.from_string(course_key_str)

    """
    store = modulestore()
    course_module = store.get_course(course_key)

    published = store.has_published_version(course_module)

    course_json = {
        "id": str(course_module.location),
        "language": course_module.fields["language"].to_json(course_module.language),
        "display_name": course_module.display_name_with_default,
        "published": published,
        "published_on": get_default_time_display(course_module.published_on)
        if published and course_module.published_on
        else None,
        "edited_on": get_default_time_display(course_module.subtree_edited_on)
        if course_module.subtree_edited_on
        else None,
        "released_to_students": datetime.now(UTC) > course_module.start,
        "has_explicit_staff_lock": course_module.fields["visible_to_staff_only"].is_set_on(course_module),
        "start": course_module.fields["start"].to_json(course_module.start),
        "has_changes": store.has_changes(course_module),
        "group_access": course_module.group_access,
        "certificate_available_date": course_module.certificate_available_date,
    }

    return course_json


def grade_book_course_for_user(user):
    course_link = retrieve_last_sitewide_block_completed(user)
    course_key = None
    if course_link:
        course_key = re.search(r"courses/(.*)/jump_to", course_link).group(1)
    return course_key
