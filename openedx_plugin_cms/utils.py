"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2021

App Models
"""

# python stuff
import datetime as dt
import logging
from re import X
from lxml.html import fromstring
from os.path import basename
from urllib.parse import urlparse

# django
from django.conf import settings
from django.contrib.auth import get_user_model

# common libs
from xblock.fields import Boolean, String
from xblock.core import XBlock
from opaque_keys.edx.keys import UsageKey


# open edx stuff
from xmodule.modulestore.django import modulestore
from xmodule.course_module import CourseBlock  # lint-amnesty, pylint: disable=wrong-import-order
from cms.djangoapps.contentstore.utils import get_lms_link_for_item

# this repo
from .models import CourseChangeLog

User = get_user_model()
log = logging.getLogger(__name__)


def link_extractor(html: str):
    """
    receives ´html´ from xblock.data
    finds and returns a list of all external urls.
    """
    try:
        doc = fromstring(html)
    except Exception:
        return ""

    retval = []
    for _, _, link, _ in doc.iterlinks():
        url = str(link).lower()
        parsed_url = urlparse(url)
        domain = str(parsed_url.netloc).lower()
        if domain != "" and domain != settings.SITE_NAME.lower() and url not in retval:
            retval.append(url)

    return ",\r\n".join(retval)


def asset_extractor(html: str):
    """
    receives ´html´ from xblock.data
    finds and returns a list of Studio CMS assets.
    """
    try:
        doc = fromstring(html)
    except Exception:
        return ""

    retval = []
    for img in doc.xpath("//img"):
        filename_and_path = img.attrib["src"]
        filename = basename(filename_and_path)
        retval.append(filename)
    return ",\r\n".join(retval)


def get_grade_weight(xblock: XBlock, course: CourseBlock):
    """
    retreive the problem weight from the grading policy
    based on Xblock type.

    raw_grader: [
            {'min_count': 3, 'weight': 0.75, 'type': 'Homework', 'drop_count': 1, 'short_label': 'Ex'},
            {'short_label': '', 'min_count': 1, 'type': 'Exam', 'drop_count': 0, 'weight': 0.25}
        ]
    """
    if not hasattr(xblock, "format"):
        return ""

    grade_type = xblock.format
    for grade_type_dict in course.raw_grader:
        if grade_type_dict["type"] == grade_type:
            return grade_type_dict["weight"], grade_type_dict["min_count"]


def get_ordinal_position(block_key: UsageKey, parent_key: UsageKey) -> int:
    """
    returns the ordinal position of the  chile block_key within the parent parent_key.
    returns -1 if not found within the parent_key xblock.
    """
    log.debug(
        "get_ordinal_position() block_key: {block_key}, parent_key: {parent_key}".format(
            block_key=block_key, parent_key=parent_key
        )
    )
    i = 0
    xblock_parent = modulestore().get_item(parent_key)
    if xblock_parent:
        children = xblock_parent.get_children()
        for child_block in children:
            i += 1
            if child_block.location == block_key:
                return i
    return -1


def get_parent_block(category: String, block_key: UsageKey) -> UsageKey:
    """
    Returns the XBlock for one of the following: course, chapter, sequential, vertical.
    These equate to:
        course: CourseSummary
        chapter is a "Section"
        sequential is a "Subsection"
        vertical is a "Unit"

    Returns None if nothing is found.
    """
    category = category or ""
    category = category.lower()

    while True:
        xblock = modulestore().get_item(block_key)

        if xblock.category.lower() == category:
            return xblock

        parent = xblock.get_parent()
        if not parent:
            return None

        block_key = parent.location


def get_parent_location(category: String, block_key: UsageKey) -> UsageKey:
    """
    Returns the UsageKey (location) for one of the following: course, chapter, sequential, vertical.
    These equate to:
        course: CourseSummary
        chapter is a "Section"
        sequential is a "Subsection"
        vertical is a "Unit"

    Returns None if nothing is found.
    """
    parent = get_parent_block(category, block_key)
    return parent.location if parent else None


def get_problem_type(xblock: XBlock) -> str:
    """
    Xblock accomodates multiple problem types,
    but in our use case we are only interested
    in the first of these.
    """
    if hasattr(xblock, "problem_types"):
        for t in xblock.problem_types:
            return t
    return None


def get_host_url(app="cms") -> str:
    scheme = "https" if settings.HTTPS == "on" else "http"
    if app == "cms":
        # https://cms.dev.engineplatform.co.uk
        return f"{scheme}://{settings.CMS_BASE}"
    else:
        # https://dev.engineplatform.co.uk
        return f"{scheme}://{settings.LMS_BASE}"


def get_user(user_id):

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return ""


def get_xblock_attribute(usage_key: UsageKey, attr: String):

    if usage_key:
        try:
            xblock = modulestore().get_item(usage_key)
            return xblock.__getattribute__(attr)
        except Exception:
            return None
    return None


def get_xml_filename(xblock: XBlock) -> str:
    if hasattr(xblock, "xml_attributes"):
        if "filename" in xblock.xml_attributes:
            # Xblock maintains the xml filename in a list
            # in our use case the filename that we want
            # is duplicated in this list (no idea why.)
            # we'll grab the first of these, and move on.
            filenames = xblock.xml_attributes["filename"]
            for f in filenames:
                return f
    return ""


def get_url(xblock: XBlock, app="cms") -> str:
    """
    returns the application url to the corresponding
    page in the LMS/CMS for the xblock.
    """
    parent = modulestore().get_item(xblock.parent)
    host_url = get_host_url(app)
    course_key = str(xblock.location.course_key)
    if app == "cms":
        if parent.category == "vertical":
            # https://cms.dev.engineplatform.co.uk/container/block-v1:edX+DemoX+Demo_Course+type@vertical+block@867dddb6f55d410caaa9c1eb9c6743ec
            return host_url + "/container/" + str(parent.location)
        else:
            # https://cms.dev.engineplatform.co.uk/course/course-v1:edX+DemoX+Demo_Course
            return host_url + "/course/" + course_key
    if app == "lms":
        return "https:" + get_lms_link_for_item(xblock.location)


def make_url(location, category=""):
    """
    build a url string of the form
    https://dev.engineplatform.co.uk/courses/course-v1:edX+DemoX+Demo_Course/jump_to_id/651e0945b77f42e0a4c89b8c3e6f5b3b

    FIX NOTE: this should be deprecated and replaced with get_url() above.
    """
    scheme = "https" if settings.HTTPS == "on" else "http"
    fully_qualified_domain = scheme + "://" + settings.LMS_BASE

    if location:
        course_key_str = str(location.course_key)
        block_id_str = str(location.block_id)
        url = fully_qualified_domain + "/courses/" + course_key_str
        if category != "course":
            url += "/jump_to_id/" + block_id_str
        return url
    return None


def is_xblock(obj) -> Boolean:
    """
    Returns True if the object instance if of type XBlock
    or if its class inherits XBlock
    """
    return isinstance(obj, XBlock) or issubclass(obj, XBlock)


def is_dirty(xblock: XBlock) -> Boolean:
    """
    Returns true if all of the following are true:
    1. the block state has not already been logged.
    2. the block is published
    3. modifications exist
    4. the modifications have not yet been logged.
    """

    publication_date = xblock_publication_date(xblock)

    if not publication_date:
        log.debug("is_dirty() returning False. No publication date: {location}".format(location=xblock.location))
        return False

    # we do not consider an XBlock to be dirty (to have changes)
    # until it has actually been published.
    #
    # evaluate this first, as we're assuming that it's the most performant
    # test that's being made in this def.
    if not modulestore().has_published_version(xblock):
        log.debug("is_dirty() returning False. not published: {location}".format(location=xblock.location))
        return False

    # we do not consider an XBlock to be dirty if
    # we already logged its state.
    course_change_log = CourseChangeLog.objects.filter(location=xblock.location, publication_date=publication_date)
    if course_change_log:
        log.debug("is_dirty() returning False. already logged: {location}".format(location=xblock.location))
        return False

    log.debug("is_dirty() {location}".format(location=xblock.location))
    return True

    # FIX NOTE: verify whether we really need this fallback option.
    # see: https://github.com/edx/XBlock/blob/master/xblock/fields.py#L410
    # return len(xblock._dirty_fields.keys()) > 0


def log_date(log_record):
    """
    normalized business rules for generating the "log date"
    """
    if log_record.edited_on:
        return round_seconds(log_record.edited_on)

    if log_record.published_on:
        return round_seconds(log_record.published_on)

    return round_seconds(dt.datetime.now())


def round_seconds(obj: dt.datetime) -> dt.datetime:
    """
    helper function to round a date object instance value
    to the nearest 1 second.
    """
    if not obj:
        return

    if obj.microsecond >= 500_000:
        obj += dt.timedelta(seconds=1)

    return obj.replace(microsecond=0)


def xblock_publication_date(xblock: XBlock) -> dt.datetime:
    """
    Might be redundant, but, we want to ensure that
    we use consistent logic for the publication_date
    of an XBlock instance bc we use this as part of the
    primary key in CourseChangeLog
    """
    edited_on, published_on = xblock_edit_dates(xblock)
    return edited_on or published_on


def xblock_edit_dates(xblock: XBlock):
    """
    helper function that returns the ´edit´ date
    of the xblock. falls back on the ´published_on´ date
    if the edit date is missing.
    """
    edited_on = None
    published_on = None

    if hasattr(xblock, "edited_on"):
        edited_on = round_seconds(xblock.edited_on)

    if hasattr(xblock, "published_on"):
        published_on = round_seconds(xblock.published_on)

    return edited_on, published_on
