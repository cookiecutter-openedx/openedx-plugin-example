# coding=utf-8
"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2021

Log changes to published course content.
"""
# python stuff
from datetime import datetime
import json
import logging

# django stuff
from django.conf import settings
from django.contrib.auth import get_user_model

# open edx common libs
from opaque_keys.edx.keys import CourseKey, UsageKey
from xblock.core import XBlock

# open edx stuff
from cms.djangoapps.contentstore.utils import (
    get_lms_link_for_item,
    is_currently_visible_to_students,
)
from openedx.core.djangoapps.content.block_structure.api import get_course_in_cache

try:
    # for olive and later
    from xmodule.modulestore.django import modulestore  # lint-amnesty, pylint: disable=wrong-import-order
except ImportError:
    # for backward compatibility with nutmeg and earlier
    from common.lib.xmodule.xmodule.modulestore.django import (
        modulestore,
    )  # lint-amnesty, pylint: disable=wrong-import-order

# our stuff
from .utils import (
    round_seconds,
    get_user,
    get_parent_location,
    is_dirty,
    xblock_publication_date,
    make_url,
    get_ordinal_position,
)
from .models import CourseChangeLog

log = logging.getLogger(__name__)
User = get_user_model()


def write_log_delete_course(course_key: CourseKey, user_id: User) -> None:
    """
    Log deletion of a course run.
    """
    course_change_log, created = CourseChangeLog.objects.update_or_create(
        course_id=course_key, operation=CourseChangeLog.DB_DELETE
    )
    course_change_log.edited_by = user_id
    course_change_log.save()


def write_log(course_change_log: CourseChangeLog, usage_key: UsageKey, user: User, xblock=None):
    course_key = usage_key.course_key
    if not xblock:
        xblock = modulestore().get_item(usage_key)

    # for building misc url's
    # ----------------------
    scheme = "https" if settings.HTTPS == "on" else "http"
    # ----------------------

    parent = xblock.get_parent()
    chapter_location = get_parent_location("chapter", xblock.location)
    sequential_location = get_parent_location("sequential", xblock.location)
    vertical_location = get_parent_location("vertical", xblock.location)
    display_name = xblock.display_name if len(str(xblock.display_name)) > 1 else "MISSING"

    # add the log data
    # ----------------------
    course_change_log.url = scheme + ":" + get_lms_link_for_item(xblock.location)
    course_change_log.display_name = display_name
    course_change_log.visible = is_currently_visible_to_students(xblock)
    course_change_log.category = xblock.category
    course_change_log.course_id = xblock.location.course_key or course_key

    if parent:
        course_change_log.ordinal_position = get_ordinal_position(xblock.location, parent.location)
        course_change_log.parent_location = parent.location
        course_change_log.parent_url = make_url(parent.location, parent.category)

    course_change_log.chapter_location = chapter_location
    course_change_log.chapter_url = make_url(chapter_location)
    course_change_log.sequential_location = sequential_location
    course_change_log.sequential_url = make_url(sequential_location)
    course_change_log.vertical_location = vertical_location
    course_change_log.vertical_url = make_url(vertical_location)

    course_change_log.edit_info = json.dumps({})
    course_change_log.source_version = None
    course_change_log.update_version = None
    course_change_log.previous_version = None
    course_change_log.original_usage = None
    course_change_log.original_usage_version = None

    course_change_log.release_date = xblock.start
    course_change_log.published_by = get_user(xblock.published_by) if xblock.published_by > 0 else None
    course_change_log.published_on = round_seconds(xblock.published_on)
    course_change_log.edited_by = get_user(xblock.edited_by) if xblock.edited_by > 0 else user
    course_change_log.edited_on = round_seconds(xblock.edited_on) or round_seconds(datetime.now())
    course_change_log.save()
    # ----------------------

    log.info("write_log() logged block: {location}".format(location=xblock.location))


def write_log_delete_item(usage_key: UsageKey, user: User) -> None:
    """
    Log deletion of a course run.
    """

    publication_date = round_seconds(datetime.now())
    course_change_log, created = CourseChangeLog.objects.update_or_create(
        course_id=usage_key.course_key,
        location=usage_key,
        publication_date=publication_date,
        operation=CourseChangeLog.DB_DELETE,
    )

    write_log(course_change_log, usage_key, user)


def write_log_upsert(xblock: XBlock, user: User) -> None:
    """
    xblock_info: either an XBlockWithMixins or a dict

    Persist the state information of a course block. This is intended to be called immediately
    after course run is published / re-published.

    Note: each edit_info dict key is *supposed* to exist based on a rule that all XBlocks are
    supposed to inherit EditInfoMixin, where each of these keys originates.

    See:
    cms.envs.common -> XBLOCK_MIXINS contains EditInfoMixin and in theory is included in all XBlocks
    common.lib.xmodule.xmodule.modulestore.EditInfo
    common.lib.xmodule.xmodule.modulestore.edit_info.EditInfoMixin

    a potentially good-to-know trick: xblock_orig_key, orig_version = store.get_block_original_usage(block_key)
    """

    publication_date = xblock_publication_date(xblock)
    course_change_log, created = CourseChangeLog.objects.update_or_create(
        location=xblock.location,
        publication_date=publication_date,
        operation=CourseChangeLog.DB_UPSERT,
    )
    write_log(course_change_log, xblock.location, user, xblock)


def eval_course_block_changes(course_key: CourseKey, user: User) -> None:
    """
    Inspect the blocks contained in a course structure.
    Log any blocks whose content has changed since they
    were last inspected.

    course_key:     opaque_keys.edx.keys.CourseKey
                    example course-v1:edX+DemoX+Demo_Course
    """

    store = modulestore()
    has_changes = store.has_changes(modulestore().get_course(course_key, depth=None))
    if has_changes:
        log.info("{course_key} has changes.".format(course_key=course_key))

    # BlockStructureBlockData
    collected_block_structure = get_course_in_cache(course_key)

    # see https://en.wikipedia.org/wiki/Topological_sorting
    # topological_traversal() iterator returns all blocks
    # in the course structure, following the rules of a
    # topological tree traversal.
    #
    # block_key is opaque_keys.edx.locator.BlockUsageLocator
    for block_key in collected_block_structure.topological_traversal():
        # xblock is also a BlockUsageLocator, but it's fully
        # initialized (the data contents at the block location are also initialized)
        xblock = store.get_item(block_key)

        log.debug("auditing {location}.".format(location=xblock.location))

        if is_dirty(xblock):
            write_log_upsert(xblock, user)
