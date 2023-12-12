# coding=utf-8
"""
written by:     Lawrence McDaniel
                https://lawrencemcdaniel.com

date:           sep-2021

usage:          custom LMS url endpoints for
                openedx_plugin_api plugin
"""
from django.urls import path

from . import api
from .waffle import (
    waffle_switches,
    API_META,
    API_USERS,
    API_TOKEN,
    API_ENROLLMENT,
    API_ASSOCIATE,
    API_PERMISSIONS,
    API_COURSE,
    API_STUDENT,
)

urlpatterns = []

if waffle_switches[API_META]:
    urlpatterns += [
        path("meta/", api.APIInfoView.as_view(), name="openedx_plugin_api_meta"),
    ]

if waffle_switches[API_USERS]:
    urlpatterns += [
        path("users/", api.UsersAPIView.as_view(), name="openedx_plugin_api_users"),
        path("users/update/", api.UsersProfileUpdateView.as_view(), name="openedx_plugin_api_users_update"),
    ]

if waffle_switches[API_TOKEN]:
    urlpatterns += [
        path("token/", api.RefreshToken.as_view(), name="openedx_plugin_api_token"),
    ]

if waffle_switches[API_ENROLLMENT]:
    urlpatterns += [
        path(
            "unenroll/",
            api.UnenrollUserAPIView.as_view(),
            name="openedx_plugin_api_unenroll",
        ),
        path("enroll/", api.EnrollUserAPIView.as_view(), name="openedx_plugin_api_enroll"),
    ]

if waffle_switches[API_ASSOCIATE]:
    urlpatterns += [
        path(
            "associate/",
            api.AssociateUserOAuthAPIView.as_view(),
            name="openedx_plugin_api_associate",
        ),
    ]

if waffle_switches[API_PERMISSIONS]:
    urlpatterns += [
        path(
            "roles/grant/",
            api.CourseGrantRoleAccessAPIView.as_view(),
            name="openedx_plugin_api_grant_permissions",
        ),
        path(
            "roles/revoke/",
            api.CourseRevokeRoleAccessAPIView.as_view(),
            name="openedx_plugin_api_revoke_permissions",
        ),
    ]

if waffle_switches[API_COURSE]:
    urlpatterns += [
        path(
            "course-mode/",
            api.CourseChangeModeAPIView.as_view(),
            name="openedx_plugin_api_set_course_mode",
        ),
        path(
            "course/<str:course_key>/users/active/",
            api.CourseActiveStudentsAPIView.as_view(),
            name="openedx_plugin_api_active_student_count",
        ),
        path(
            "course/rerun/",
            api.CourseRerunAPIView.as_view(),
            name="rerun_course",
        ),
        path(
            "course/<str:course_key>/info/",
            api.CourseInfoAPIView.as_view(),
            name="openedx_plugin_api_course_info",
        ),
        path(
            "course/<str:course_key>/points/",
            api.CoursePointsAPIView.as_view(),
            name="openedx_plugin_api_course_points",
        ),
        path(
            "course/<str:course_id>/certificate/",
            api.CourseCertificateAPIView.as_view(),
            name="openedx_plugin_api_certificate",
        ),
        path(
            "course/<str:course_id>/bulkemail/",
            api.CourseBulkEmailAPIView.as_view(),
            name="openedx_plugin_api_bulk_email",
        ),
        path(
            "course/<str:course_id>/discussion/",
            api.DiscussionForum.as_view(),
            name="openedx_plugin_api_discussion",
        ),
    ]

if waffle_switches[API_STUDENT]:
    urlpatterns += [
        path(
            "student/<str:username>/course/<str:course_key>/modules/",
            api.StudentHistoryAPIView.as_view(),
            name="openedx_plugin_api_student_modules",
        ),
        path(
            "student/<str:username>/course/<str:course_key>/grade/",
            api.StudentCourseGradeAPIView.as_view(),
            name="openedx_plugin_api_student_course_grade",
        ),
    ]
