# coding=utf-8
"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2021

CMS App urls
"""
from django.conf import settings
from django.conf.urls import url

from .views.change_log import plugin_cms_change_log, plugin_cms_change_csv
from .views.course_audit import (
    plugin_cms_course_audit,
    plugin_cms_course_audit_csv,
    plugin_cms_course_audit_refresh,
)
from .views.course_audit_html import (
    plugin_cms_course_audit_html,
    plugin_cms_course_audit_html_csv,
)
from .waffle import waffle_switches, AUDIT_REPORT

urlpatterns = []

if waffle_switches[AUDIT_REPORT]:
    urlpatterns += [
        # Log paginated UI
        url(r"^log/$", plugin_cms_change_log, name="plugin_cms_change_log"),
        url(
            rf"^courses/{settings.COURSE_ID_PATTERN}/log/$",
            plugin_cms_change_log,
            name="plugin_cms_change_log",
        ),
        url(
            rf"^courses/{settings.COURSE_ID_PATTERN}/log/(?P<offset>[0-9]+)$",
            plugin_cms_change_log,
            name="plugin_cms_change_log",
        ),
        # Log paginated CSV download file
        url(r"^log/csv/$", plugin_cms_change_csv, name="plugin_cms_change_csv"),
        url(
            rf"^courses/{settings.COURSE_ID_PATTERN}/log/csv/$",
            plugin_cms_change_csv,
            name="plugin_cms_change_csv",
        ),
        url(
            rf"^courses/{settings.COURSE_ID_PATTERN}/log/csv/(?P<offset>[0-9]+)$",
            plugin_cms_change_csv,
            name="plugin_cms_change_csv",
        ),
        # Course Audit - refresh
        url(
            rf"^courses/{settings.COURSE_ID_PATTERN}/audit/refresh/$",
            plugin_cms_course_audit_refresh,
            name="plugin_cms_course_audit_refresh",
        ),
        # Course Audit paginated UI
        url(
            rf"^courses/{settings.COURSE_ID_PATTERN}/audit/$",
            plugin_cms_course_audit,
            name="plugin_cms_course_audit",
        ),
        url(
            rf"^courses/{settings.COURSE_ID_PATTERN}/audit/(?P<offset>[0-9]+)$",
            plugin_cms_course_audit,
            name="plugin_cms_course_audit",
        ),
        # Course Audit CSV download file
        url(
            rf"^courses/{settings.COURSE_ID_PATTERN}/audit/csv/$",
            plugin_cms_course_audit_csv,
            name="plugin_cms_course_audit_csv",
        ),
        url(
            rf"^courses/{settings.COURSE_ID_PATTERN}/audit/csv/(?P<offset>[0-9]+)$",
            plugin_cms_course_audit_csv,
            name="plugin_cms_course_audit_csv",
        ),
        # Course Audit HTML paginated UI
        url(
            rf"^courses/{settings.COURSE_ID_PATTERN}/audit/html/$",
            plugin_cms_course_audit_html,
            name="plugin_cms_course_audit_html",
        ),
        url(
            rf"^courses/{settings.COURSE_ID_PATTERN}/audit/html/(?P<offset>[0-9]+)$",
            plugin_cms_course_audit_html,
            name="plugin_cms_course_audit_html",
        ),
        # Course Audit HTML CSV download file
        url(
            rf"^courses/{settings.COURSE_ID_PATTERN}/audit/html/csv/$",
            plugin_cms_course_audit_html_csv,
            name="plugin_cms_course_audit_html_csv",
        ),
        url(
            rf"^courses/{settings.COURSE_ID_PATTERN}/audit/html/csv/(?P<offset>[0-9]+)$",
            plugin_cms_course_audit_html_csv,
            name="plugin_cms_course_audit_html_csv",
        ),
    ]
