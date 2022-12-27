"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2021

View to dump log data to a simple row-column paginated layout.
see: https://docs.djangoproject.com/en/2.2/topics/pagination/
"""
# Python
import csv
from typing import List
import logging

# Django
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponse
from six import StringIO


# Open edX
from common.djangoapps.util.views import ensure_valid_course_key
from common.djangoapps.edxmako.shortcuts import render_to_response
from opaque_keys.edx.keys import CourseKey
from xmodule.course_module import CourseSummary

# This repo
from openedx_plugin_cms.models import CourseChangeLog
from openedx_plugin_cms.utils import get_xblock_attribute

log = logging.getLogger(__name__)
# Grade book: max students per page
MAX_ROWS_PER_PAGE = 50


def get_csv_url(course_id=None, page_number=None):

    if course_id:
        url = "/plugin_cms/courses/{course_id}/log/csv/".format(course_id=course_id)
    else:
        url = "/plugin_cms/log/csv/"

    if page_number:
        url += "?page={page_number}".format(page_number=page_number)

    return url


def get_context(course_id=None, page_number=None):
    """
    mcdaniel oct-2021

    """
    if course_id:
        course_key = CourseKey.from_string(course_id)
        change_log = CourseChangeLog.objects.filter(course_id=course_key).order_by("-id")
    else:
        change_log = CourseChangeLog.objects.all().select_related("published_by", "edited_by").order_by("-id")

    paginator = Paginator(change_log, MAX_ROWS_PER_PAGE)
    page = paginator.get_page(page_number)

    # mcdaniel nov-2021
    # this is a workaround to buggy behavior with the paginator object.
    page_number = int(page_number or 1)
    page_next = page_number + 1 if page_number < page.paginator.num_pages else -1
    page_previous = page_number - 1 if page_number > 1 else -1

    context = {
        "course_id": course_id,
        "page_obj": page,
        "page_previous": page_previous,
        "page_next": page_next,
        "uses_bootstrap": True,
        "csv_url": get_csv_url(course_id, page_number),
    }
    return context


@login_required
@ensure_valid_course_key
def plugin_cms_change_log(request, course_id=None, **kwargs):
    """
    mcdaniel oct-2021

    """
    page_number = request.GET.get("page")
    template_name = "course_change_log.html"
    context = get_context(course_id, page_number)

    return render_to_response(template_name=template_name, dictionary=context, request=request)


@login_required
@ensure_valid_course_key
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def plugin_cms_change_csv(request, course_id=None, **kwargs):
    """
    mcdaniel oct-2021

    Generate a csv download of CMS change log data
    """
    if course_id:
        course_key = CourseKey.from_string(course_id)
        change_log = CourseChangeLog.objects.filter(course_id=course_key).order_by("-id")
        course_display_name = CourseSummary(course_key).display_name
    else:
        course_display_name = ""
        change_log = CourseChangeLog.objects.all().select_related("published_by", "edited_by").order_by("-id")

    filename = "openedx_plugin_cms_change_log"
    if course_id:
        filename += "-{course_id}".format(course_id=course_id)
    filename += ".csv"

    output = []

    for log_entry in change_log:
        output.append(
            [
                log_entry.id,
                log_entry.operation,
                log_entry.location,
                log_entry.category,
                log_entry.course_id,
                str(course_display_name if course_id else CourseSummary(log_entry.course_id).display_name).replace(
                    "Empty", ""
                ),
                log_entry.parent_url,
                get_xblock_attribute(log_entry.parent_location, "display_name"),
                log_entry.chapter_url,
                get_xblock_attribute(log_entry.chapter_location, "display_name"),
                log_entry.sequential_url,
                get_xblock_attribute(log_entry.sequential_location, "display_name"),
                log_entry.vertical_url,
                get_xblock_attribute(log_entry.vertical_location, "display_name"),
                log_entry.display_name,
                log_entry.ordinal_position,
                log_entry.publication_date,
                log_entry.published_by,
            ]
        )

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename={filename}".format(filename=filename)

    writer = csv.writer(response)
    writer.writerow(
        [
            "id",
            "operation",
            "location",
            "category",
            "course_id",
            "course_display_name",
            "parent_url",
            "parent_display_name",
            "chapter_url",
            "chapter_display_name",
            "sequential_url",
            "sequential_display_name",
            "vertical_url",
            "vertical_display_name",
            "display_name",
            "ordinal_position",
            "publication_date",
            "published_by",
        ]
    )
    writer.writerows(output)

    return response
