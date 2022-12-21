from django.urls import path

from . import api
from .views import EdxApiFragmentView

urlpatterns = [
    path("meta/", api.APIInfoView.as_view(), name="edxapi_meta"),
    path("users/", api.UsersAPIView.as_view(), name="edxapi_users"),
    path("token/", api.RefreshToken.as_view(), name="edxapi_token"),
    path("unenroll/", api.UnenrollUserAPIView.as_view(), name="edxapi_unenroll"),
    path("enroll/", api.EnrollUserAPIView.as_view(), name="edxapi_enroll"),
    path("associate/", api.AssociateUserOAuthAPIView.as_view(), name="edxapi_associate"),
    path("roles/grant/", api.CourseGrantRoleAccessAPIView.as_view(), name="edxapi_grant_permissions"),
    path("roles/revoke/", api.CourseRevokeRoleAccessAPIView.as_view(), name="edxapi_revoke_permissions"),
    path("course-mode/", api.CourseChangeModeAPIView.as_view(), name="edxapi_set_course_mode"),
    path(
        "student/<str:username>/course/<str:course_key>/modules/",
        api.StudentHistoryAPIView.as_view(),
        name="edxapi_student_modules",
    ),
    path(
        "student/<str:username>/course/<str:course_key>/grade/",
        api.StudentCourseGradeAPIView.as_view(),
        name="edxapi_student_course_grade",
    ),
    path(
        "course/<str:course_key>/users/active/",
        api.CourseActiveStudentsAPIView.as_view(),
        name="edxapi_active_student_count",
    ),
    path(
        "api_fragment_view",
        EdxApiFragmentView.as_view(),
        name="api_fragment_view",
    ),
    path(
        "course/rerun/",
        api.CourseRerunAPIView.as_view(),
        name="rerun_course",
    ),
    path(
        "course/<str:course_key>/info/",
        api.CourseInfoAPIView.as_view(),
        name="edxapi_course_info",
    ),
    path(
        "course/<str:course_key>/points/",
        api.CoursePointsAPIView.as_view(),
        name="edxapi_course_points",
    ),
    path("course/<str:course_id>/certificate/", api.CourseCertificateAPIView.as_view(), name="edxapi_certificate"),
    path(
        "course/<str:course_id>/bulkemail/",
        api.CourseBulkEmailAPIView.as_view(),
        name="edxapi_bulk_email",
    ),
    path(
        "course/<str:course_id>/discussion/",
        api.DiscussionForum.as_view(),
        name="edxapi_discussion",
    ),
]
