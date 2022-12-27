"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Dec-2021

CMS App - Course Audit Custom HTML view

see: https://co-digitallearning.atlassian.net/browse/CODLT-383
     https://docs.google.com/spreadsheets/d/1v08r5KEarvsMiqHSlELWnFNqBwgdkofDvgj4ogyGmiw/edit#gid=0
     https://co-digitallearning.atlassian.net/wiki/spaces/CODLT/pages/2326536/Course+Inventory

also: https://docs.djangoproject.com/en/2.2/topics/pagination/
"""
# Python
import csv
import logging
from typing import Dict

# Django
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse

# Open edX
from common.djangoapps.util.views import ensure_valid_course_key
from common.djangoapps.edxmako.shortcuts import render_to_response

# Open edX course content
from opaque_keys.edx.keys import CourseKey
from xblock.core import XBlock

# This repo
from openedx_plugin_cms.models import CourseAudit

log = logging.getLogger(__name__)

MAX_ROWS_PER_PAGE = 200


def get_csv_url(course_key, page_number=None):
    url = "/plugin/cms/courses/{course_id}/audit/html/csv/".format(course_id=str(course_key))
    if page_number:
        url += "?page={page_number}".format(page_number=page_number)
    return url


def get_context(course_key: CourseKey, page_number=None) -> Dict:
    """
    mcdaniel nov-2021
    """

    course_audit = CourseAudit.objects.filter(course_id=course_key).order_by("id")

    paginator = Paginator(course_audit, MAX_ROWS_PER_PAGE)
    page = paginator.get_page(page_number)

    # mcdaniel nov-2021
    # this is a workaround to buggy behavior with the paginator object.
    page_number = int(page_number or 1)
    page_next = page_number + 1 if page_number < page.paginator.num_pages else -1
    page_previous = page_number - 1 if page_number > 1 else -1

    context = {
        "course_id": str(course_key),
        "page_obj": page,
        "page_previous": page_previous,
        "page_next": page_next,
        "uses_bootstrap": True,
        "csv_url": get_csv_url(course_key, page_number),
    }

    return context


@login_required
@ensure_valid_course_key
def plugin_cms_course_audit_html(request, course_id: str, **kwargs):
    """
    mcdaniel nov-2021
    """
    page_number = request.GET.get("page")
    template_name = "course_audit_html.html"
    course_key = CourseKey.from_string(course_id)
    context = get_context(course_key, page_number)
    return render_to_response(template_name=template_name, dictionary=context, request=request)


@login_required
@ensure_valid_course_key
def plugin_cms_course_audit_html_csv(request, course_id: str, **kwargs):
    """
    mcdaniel oct-2021

    Generate a csv download of CMS change log data
    """
    course_key = CourseKey.from_string(course_id)
    output = CourseAudit.objects.filter(course_id=course_key).order_by("id")
    filename = "plugin/cms_cms_course_html_audit-{course_id}.csv".format(course_id=course_id)

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
            "f_xblock_customized_html",
            "o_unit_url",
            "p_studio_url",
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
                row.f_xblock_customized_html,
                row.o_unit_url,
                row.p_studio_url,
                row.r_publication_date,
                row.s_changed_by,
                row.t_change_made,
            ]
        )

    return response
