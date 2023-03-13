"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Nov-2021

CMS App - Course Audit views
see: https://co-digitallearning.atlassian.net/browse/CODLT-383
     https://docs.google.com/spreadsheets/d/1v08r5KEarvsMiqHSlELWnFNqBwgdkofDvgj4ogyGmiw/edit#gid=0
     https://co-digitallearning.atlassian.net/wiki/spaces/CODLT/pages/2326536/Course+Inventory

also: https://docs.djangoproject.com/en/2.2/topics/pagination/
"""
# Python
import time
import csv
import logging
from datetime import datetime
from typing import Dict, List
from contextlib import contextmanager
from hashlib import md5

# Django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.db.utils import DatabaseError
from django.core.exceptions import ValidationError
from django.core.cache import cache

# Celery
try:
    # mcdaniel aug-2022: deprecated sometime after Lilac.
    # see: https://docs.celeryq.dev/en/stable/internals/deprecation.html
    from celery.task import task
except ImportError:
    from celery import shared_task as task

from celery.exceptions import SoftTimeLimitExceeded
from celery_utils.persist_on_failure import LoggedPersistOnFailureTask

# Open edX
from common.djangoapps.util.views import ensure_valid_course_key
from openedx.core.lib.cache_utils import request_cached
from common.djangoapps.edxmako.shortcuts import render_to_response

# Open edX course content
from cms.djangoapps.models.settings.course_grading import CourseGradingModel
from opaque_keys.edx.keys import CourseKey
from xblock.core import XBlock
from xmodule.modulestore.django import modulestore  # lint-amnesty, pylint: disable=wrong-import-order
from xmodule.modulestore import ModuleStoreEnum  # lint-amnesty, pylint: disable=wrong-import-order
from xmodule.course_module import CourseBlock  # lint-amnesty, pylint: disable=wrong-import-order
from xmodule.seq_module import SequenceBlock, SectionBlock  # lint-amnesty, pylint: disable=wrong-import-order
from xmodule.vertical_block import VerticalBlock  # lint-amnesty, pylint: disable=wrong-import-order
from xmodule.unit_block import UnitBlock  # Units are verticals.

# This repo
from openedx_plugin_cms.models import CourseAudit


from openedx_plugin_cms.utils import (
    get_user,
    xblock_edit_dates,
    get_url,
    get_problem_type,
    get_xml_filename,
    get_grade_weight,
    asset_extractor,
    link_extractor,
)

User = get_user_model()
log = logging.getLogger(__name__)

MAX_ROWS_PER_PAGE = 200
CACHE_NAMESPACE = "plugin.cms.CourseAudit.cache."

# Celery tasks constants
LOCK_EXPIRE = 60 * 15
KNOWN_RETRY_ERRORS = (  # Errors we expect occasionally, should be resolved on retry
    DatabaseError,
    ValidationError,
    SoftTimeLimitExceeded,
)
RETRY_DELAY_SECONDS = 60
TASK_TIME_LIMIT = LOCK_EXPIRE  # Task hard time limit in seconds. The worker processing the task will be killed and replaced with a new one when this is exceeded.
TASK_SOFT_TIME_LIMIT = (
    None  # https://docs.celeryproject.org/en/stable/userguide/configuration.html#std-setting-task_soft_time_limit
)
MAX_RETRIES = 1


@contextmanager
def task_lock(oid, course_id):
    """
    mcdaniel dec-2021

    Simple locking strategy to prevent the Course Audit refresh task
    from being called repeatedly. This will limit invocations
    of the refresh to once every LOCK_EXPIRE seconds.

    See: https://docs.celeryproject.org/en/latest/tutorials/task-cookbook.html#cookbook-task-serial
    """

    course_id_hexdigest = md5(course_id.encode("utf-8")).hexdigest()
    lock_id = "{0}-lock-{1}".format(course_id, course_id_hexdigest)
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    # cache.add fails if the key already exists
    status = cache.add(lock_id, oid, LOCK_EXPIRE)

    try:
        yield status
    except Exception as e:
        log.error("error while attempting lock: {err}".format(err=e))
    finally:
        if time.monotonic() < timeout_at and status:
            # don't release the lock if we exceeded the timeout
            # to lessen the chance of releasing an expired lock
            # owned by someone else.
            #
            # also don't release the lock if we didn't acquire it
            cache.delete(lock_id)


def get_csv_url(course_key, page_number=None):
    url = "/plugin/cms/courses/{course_id}/audit/csv/".format(course_id=str(course_key))
    if page_number:
        url += "?page={page_number}".format(page_number=page_number)
    return url


def get_refresh_url(course_key):
    url = "/plugin/cms/courses/{course_id}/audit/refresh/".format(course_id=str(course_key))
    return url


def get_blank_dict() -> Dict:
    """
    doing this as a means of documenting what the final output looks
    like which we'll send to the Mako template.
    """
    row = {}
    row["a_order"] = ""
    row["b_course"] = ""
    row["c_module"] = ""
    row["d_section"] = ""
    row["e_unit"] = ""
    row["e2_block_type"] = ""
    row["f_graded"] = "False"
    row["g_section_weight"] = ""
    row["h_number_graded_sections"] = ""
    row["i_component_type"] = ""
    row["j_non_standard_element"] = ""
    row["k_problem_weight"] = ""
    row["m_iframe_external_url"] = ""
    row["m_external_links"] = ""
    row["n_asset_type"] = ""
    row["o_unit_url"] = ""
    row["p_studio_url"] = ""
    row["q_xml_filename"] = ""
    row["r_publication_date"] = ""
    row["s_changed_by"] = ""
    row["t_change_made"] = ""

    return row


def get_chapter_dict(i: int, course: CourseBlock, chapter: SectionBlock) -> Dict:
    row = get_blank_dict()
    row["a_order"] = str(i)
    row["b_course"] = course.display_name
    row["c_module"] = chapter.display_name
    row["e2_block_type"] = chapter.location.block_type
    row["o_unit_url"] = get_url(chapter, "lms")
    row["p_studio_url"] = get_url(chapter, "cms")
    return row


def get_sequence_dict(
    i: int,
    course: CourseBlock,
    chapter: SectionBlock,
    sequence: SequenceBlock,
) -> Dict:

    row = get_chapter_dict(i, course, chapter)
    row["d_section"] = sequence.display_name
    # e_unit -- skip. handled in get_vertical_dict()
    row["e2_block_type"] = sequence.location.block_type
    row["f_graded"] = sequence.graded if sequence.graded else ""
    row["o_unit_url"] = get_url(sequence, "lms")
    row["p_studio_url"] = get_url(sequence, "cms")
    return row


def get_vertical_dict(
    i: int,
    course: CourseBlock,
    chapter: SectionBlock,
    sequence: SequenceBlock,
    vertical: VerticalBlock,
) -> Dict:

    row = get_sequence_dict(i, course, chapter, sequence)
    row["e_unit"] = vertical.display_name
    row["e2_block_type"] = vertical.location.block_type
    row["f_graded"] = vertical.graded
    # g_section_weight - skip. handled in parent loop, get_sequence_dict()
    # h_number_graded_sections - skip. handled in parent loop, get_sequence_dict()
    row["o_unit_url"] = get_url(vertical, "lms")
    row["p_studio_url"] = get_url(vertical, "cms")
    return row


def get_vertical_child_dict(
    i: int,
    course: CourseBlock,
    chapter: SectionBlock,
    sequence: SequenceBlock,
    vertical: VerticalBlock,
    child: XBlock,
    advanced_component_types: list,
) -> Dict:
    """
    Note that all of these parameters are descendants of XBlock, including child.

    child can be any of ProblemBlock, DiscussionXBlock, HtmlBlock (or some kind of specialized XBlock).
    Ideally we'd cast these after introspecting their type, but, we only need to extract a couple of pieces
    of data and so we'll defer that indefinitely until a real neeed arises.
    """
    edited_on, published_on = xblock_edit_dates(child)
    row = get_vertical_dict(i, course, chapter, sequence, vertical)
    row["e2_block_type"] = child.location.block_type

    if hasattr(child, "data"):
        row["f_xblock_customized_html"] = child.data

    if child.location.block_type == "problem" and sequence.graded:
        row["g_section_weight"], row["h_number_graded_sections"] = get_grade_weight(sequence, course)
        row["k_problem_weight"] = str(child.weight or 1)

        component_type = get_problem_type(child)
        row["i_component_type"] = component_type
        row["j_non_standard_element"] = component_type if component_type in advanced_component_types else ""

    if child.location.block_type == "html" and hasattr(child, "data"):
        row["n_asset_type"] = asset_extractor(child.data)
        row["m_external_links"] = link_extractor(child.data)

    if hasattr(child, "html_file"):
        row["m_iframe_external_url"] = child.html_file

    row["o_unit_url"] = get_url(child, "lms")
    row["p_studio_url"] = get_url(child, "cms")
    row["q_xml_filename"] = get_xml_filename(child)
    row["r_publication_date"] = published_on.strftime("%d-%b-%Y, %H:%M")
    row["s_changed_by"] = get_user(child.edited_by) if child.edited_by > 0 else ""
    row["t_change_made"] = edited_on.strftime("%d-%b-%Y, %H:%M")

    return row


def get_analyzed_course(course_key: CourseKey) -> List:
    """
    Iterate the course blocks, in order of presentation, as you'd see in the
    Course Outline page in CMS.

    The get_children() iterators in this def each return instantiated
    XBlock-derivative objects that vary in type depending on which level
    of the nested loop we're in.

    The inner-most iteration of the vertical
    objects returns any of a wide variety of XBlock derivatives. A common
    authoring pattern for graded problems is to create a
    series of html, problem, and discussion objects.
    """
    log.debug("get_context - Start: {course_key}".format(course_key=course_key))

    store = modulestore()
    retval = []
    i = 0

    # since we're auditing changes to published course content, we can
    # optimize the entire traversal by filtering for published content
    # at the onset.
    with store.branch_setting(ModuleStoreEnum.Branch.published_only, course_key):
        # The optional param "depth=4" causes get_course() to prefetch all of the
        # xblock objects that we're going to inspect.
        course = store.get_course(course_key, depth=4)
        STANDARD_COMPONENT_TYPES = [
            "about",
            "chapter",
            "course",
            "course_info",
            "discussion",
            "html",
            "image",
            "library",
            "library_content",
            "library_sourced",
            "lti",
            "lti_consumer",
            "openassessment",
            "sequential",
            "unit",
            "vertical",
            "video",
            "wrapper",
        ]
        ADVANCED_COMPONENT_TYPES = sorted(
            {name for name, class_ in XBlock.load_classes()}
            - set(STANDARD_COMPONENT_TYPES)
            - set(course.advanced_modules)
        )

        for chapter in course.get_children():
            # chapter is a SectionBlock
            i += 1
            row = get_chapter_dict(i, course, chapter)
            retval.append(row)
            for sequence in chapter.get_children():
                # sequence is a SequenceBlock
                i += 1
                row = get_sequence_dict(i, course, chapter, sequence)
                retval.append(row)
                for vertical in sequence.get_children():
                    # vertical is a VerticalBlock
                    i += 1
                    row = get_vertical_dict(i, course, chapter, sequence, vertical)
                    retval.append(row)
                    for child in vertical.get_children():
                        # child is any of ProblemBlock, DiscussionXBlock, HtmlBlock
                        # or an object that descends from one of these.
                        #
                        # it might also be something more esoteric like AnnotatableBlock, etc.
                        i += 1
                        print("Analyzing content block: {course_key} - {i}".format(course_key=course_key, i=i))
                        row = get_vertical_child_dict(
                            i,
                            course,
                            chapter,
                            sequence,
                            vertical,
                            child,
                            ADVANCED_COMPONENT_TYPES,
                        )
                        retval.append(row)

    log.debug("get_context - End: {course_key}".format(course_key=course_key))

    return retval


def persist_analyzed_course(course_key: CourseKey) -> None:
    """
    write all records of an analyzed course to the database.
    """
    try:
        CourseAudit.objects.filter(course_id=course_key).delete()
    except ObjectDoesNotExist:
        log.info("No persisted records to replace for course_key: {course_key}".format(course_key=course_key))

    course_audit = get_analyzed_course(course_key)
    for row in course_audit:
        user = User.objects.get(username=row["s_changed_by"]) if row["s_changed_by"] != "" else None

        rec = CourseAudit.objects.create(
            course_id=course_key,
            a_order=int(row["a_order"]),
            b_course=row["b_course"][-255:] if row["b_course"] is not None else None,
            c_module=row["c_module"][-255:] if row["c_module"] is not None else None,
            d_section=row["d_section"][-255:] if row["d_section"] is not None else None,
            e_unit=row["e_unit"][-255:] if row["e_unit"] is not None else None,
            e2_block_type=row["e2_block_type"][-255:] if row["e2_block_type"] is not None else None,
            f_graded=row["f_graded"],
            g_section_weight=float(row["g_section_weight"]) if row["g_section_weight"] != "" else None,
            h_number_graded_sections=int(row["h_number_graded_sections"])
            if row["h_number_graded_sections"] != ""
            else None,
            i_component_type=row["i_component_type"][-255:] if row["i_component_type"] is not None else None,
            j_non_standard_element=row["j_non_standard_element"][-255:]
            if row["j_non_standard_element"] is not None
            else None,
            k_problem_weight=float(row["k_problem_weight"]) if row["k_problem_weight"] != "" else None,
            m_iframe_external_url=row["m_iframe_external_url"],
            n_asset_type=row["n_asset_type"],
            o_unit_url=row["o_unit_url"],
            p_studio_url=row["p_studio_url"],
            q_xml_filename=row["q_xml_filename"][-255:] if row["q_xml_filename"] is not None else None,
            r_publication_date=datetime.strptime(row["r_publication_date"], "%d-%b-%Y, %H:%M")
            if row["r_publication_date"] != ""
            else None,
            s_changed_by=user,
            t_change_made=datetime.strptime(row["t_change_made"], "%d-%b-%Y, %H:%M")
            if row["t_change_made"] != ""
            else None,
        )
        rec.save()
        print("persisted row: {i}".format(i=rec.a_order))


def get_context(course_key: CourseKey, page_number=None, cached=True, report_message="") -> Dict:
    """
    write all records of an analyzed course to the database.
    """

    report_as_of = ""
    if cached:
        course_audit = CourseAudit.objects.filter(course_id=course_key).order_by("id")
        try:
            report_as_of = course_audit[0].created.strftime("%d-%b-%Y, %H:%M")
        except ObjectDoesNotExist:
            pass
    else:
        course_audit = get_analyzed_course(course_key)
        report_as_of = datetime.today().strftime("%d-%b-%Y, %H:%M")
    paginator = Paginator(course_audit, MAX_ROWS_PER_PAGE)
    page = paginator.get_page(page_number)

    # mcdaniel nov-2021
    # this is a workaround to buggy behavior with the paginator object.
    page_number = int(page_number or 1)
    page_next = page_number + 1 if page_number < page.paginator.num_pages else -1
    page_previous = page_number - 1 if page_number > 1 else -1

    context = {
        "course_id": str(course_key),
        "report_as_of": report_as_of,
        "page_obj": page,
        "page_previous": page_previous,
        "page_next": page_next,
        "uses_bootstrap": True,
        "csv_url": get_csv_url(course_key, page_number),
        "refresh_url": get_refresh_url(course_key),
    }

    return context


@login_required
@request_cached(CACHE_NAMESPACE)
@ensure_valid_course_key
def plugin_cms_course_audit(request, course_id: str, **kwargs):
    """
    mcdaniel nov-2021
    """
    page_number = request.GET.get("page")
    template_name = "course_audit.html"
    course_key = CourseKey.from_string(course_id)
    report_message = kwargs.get("report_message")

    context = get_context(course_key, page_number, cached=True, report_message=report_message)

    return render_to_response(template_name=template_name, dictionary=context, request=request)


@login_required
@ensure_valid_course_key
@request_cached(CACHE_NAMESPACE)
def plugin_cms_course_audit_csv(request, course_id: str, **kwargs):
    """
    mcdaniel oct-2021

    Generate a csv download of CMS change log data
    """
    course_key = CourseKey.from_string(course_id)
    output = CourseAudit.objects.filter(course_id=course_key).order_by("id")
    filename = "openedx_plugin_cms_course_audit-{course_id}.csv".format(course_id=course_id)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename={filename}".format(filename=filename)

    writer = csv.writer(response)
    writer.writerow(
        [
            "a_order",
            "b_course",
            "c_module",
            "d_section",
            "e_unit",
            "e2_block_type",
            "f_graded",
            "g_section_weight",
            "h_number_graded_sections",
            "i_component_type",
            "j_non_standard_element",
            "k_problem_weight",
            "m_iframe_external_url",
            "m_external_links",
            "n_asset_type",
            "o_unit_url",
            "p_studio_url",
            "q_xml_filename",
            "r_publication_date",
            "s_changed_by",
            "t_change_made",
        ]
    )
    for row in output:
        writer.writerow(
            [
                row.a_order,
                row.b_course,
                row.c_module,
                row.d_section,
                row.e_unit,
                row.e2_block_type,
                row.f_graded,
                row.g_section_weight,
                row.h_number_graded_sections,
                row.i_component_type,
                row.j_non_standard_element,
                row.k_problem_weight,
                row.m_iframe_external_url,
                row.m_external_links,
                row.n_asset_type,
                row.o_unit_url,
                row.p_studio_url,
                row.q_xml_filename,
                row.r_publication_date,
                row.s_changed_by,
                row.t_change_made,
            ]
        )

    return response


@login_required
@ensure_valid_course_key
def plugin_cms_course_audit_refresh(request, course_id: str, **kwargs):
    """
    mcdaniel dec-2021.

    wrapper method to force serialization of calls to persist_analyzed_course()
    """
    message = "An unknown error occurred."
    status = 500
    with task_lock(oid="plugin_cms_course_audit_refresh", course_id=course_id) as acquired:
        if acquired:
            _plugin_cms_course_audit_refresh(course_id=course_id)
            message = "Report data refresh process was successfully initiated for course_key: {course_id}".format(
                course_id=course_id
            )
            status = 204
        else:
            message = "Refresh process is currently locked for course_key: {course_id}".format(course_id=course_id)
            status = 403

    content = {"description": message}
    return JsonResponse(data=content, status=status)


@task(
    bind=True,
    base=LoggedPersistOnFailureTask,
    max_retries=MAX_RETRIES,
    default_retry_delay=RETRY_DELAY_SECONDS,
    routing_key=settings.DEFAULT_PRIORITY_QUEUE,  # 'edx.core.default'
    acks_late=True,
    task_time_limit=TASK_TIME_LIMIT,
    task_soft_time_limit=TASK_SOFT_TIME_LIMIT,
)
def _plugin_cms_course_audit_refresh(self, course_id: str) -> None:
    """
    mcdaniel dec-2021.

    launch a background task to refresh report data for course_key
    """
    course_key = CourseKey.from_string(course_id)
    if course_key:
        log.info("refreshing report data for course_key: {course_id}".format(course_id=course_id))
        persist_analyzed_course(course_key)
