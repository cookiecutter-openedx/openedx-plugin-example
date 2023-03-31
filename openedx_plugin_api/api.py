# coding=utf-8
"""
written by:     Lawrence McDaniel
                https://lawrencemcdaniel.com

date:           sep-2021

usage:          Example custom REST API leveraging misc functionality from
                Open edX repos.
"""
# python stuff
import os
import json

# django stuff
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseNotFound
from openedx.core.djangoapps.oauth_dispatch.jwt import create_jwt_for_user
from openedx.core.lib.api.view_utils import view_auth_classes

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from social_django.models import UserSocialAuth

# open edx stuff
from opaque_keys.edx.keys import CourseKey
from openedx.core.djangoapps.enrollments import api
from common.djangoapps.student.models import CourseEnrollment
from common.djangoapps.student.roles import CourseDataResearcherRole
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from common.djangoapps.course_modes.models import CourseMode
from lms.djangoapps.certificates.models import CertificateGenerationCourseSetting
from lms.djangoapps.bulk_email.models import CourseAuthorization
from lms.djangoapps.courseware.models import StudentModule
from lms.djangoapps.grades.models import PersistentCourseGrade
from openedx.core.djangoapps.django_comment_common.models import (
    FORUM_ROLE_MODERATOR,
    Role,
)
import openedx.core.djangoapps.django_comment_common.comment_client as cc
import lms.djangoapps.discussion.django_comment_client.utils as utils

try:
    # for olive and later
    from xmodule.modulestore.django import (
        modulestore,
    )  # lint-amnesty, pylint: disable=wrong-import-order
    from xmodule.course_module import DEFAULT_START_DATE, CourseFields
except ImportError:
    # for backward compatibility with nutmeg and earlier
    from common.lib.xmodule.xmodule.modulestore.django import (
        modulestore,
    )  # lint-amnesty, pylint: disable=wrong-import-order
    from common.lib.xmodule.xmodule.course_module import (
        DEFAULT_START_DATE,
        CourseFields,
    )

# our stuff
from .utils import get_course_info
from .models import CoursePoints
from .version import __version__

User = get_user_model()


class ResponseSuccess(Response):
    def __init__(self, data=None, http_status=None, content_type=None):
        _status = http_status or status.HTTP_200_OK
        data = data or {}
        reply = {"response": {"success": True}}
        reply["response"].update(data)
        super().__init__(data=reply, status=_status, content_type=content_type)


@view_auth_classes(is_authenticated=True)
class UsersAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        results = [{"id": user.id, "name": user.username} for user in users]
        return Response(results, content_type="application/json")


@view_auth_classes(is_authenticated=True)
class UnenrollUserAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        course_id = request.data.get("course_id")
        try:
            enrollment = CourseEnrollment.objects.get(user__username=username, course__id=course_id)
            enrollment.is_active = False
            enrollment.save()
        except CourseEnrollment.DoesNotExist:
            return HttpResponseNotFound()
        return ResponseSuccess(content_type="application/json")


@view_auth_classes(is_authenticated=True)
class EnrollUserAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        course_id = request.data.get("course_id")
        course_mode_slug = request.data.get("course_mode")
        course = CourseOverview.objects.get(id=course_id)
        try:
            course_mode = CourseMode.objects.get(course=course, mode_slug=course_mode_slug)
        except CourseMode.DoesNotExist:
            course_mode = CourseMode.objects.create(
                course=course,
                mode_slug=course_mode_slug,
                mode_display_name=course_mode_slug.capitalize(),
            )
        response = api.add_enrollment(username, course_id, mode=course_mode.mode_slug)
        return Response(response, content_type="application/json")


@view_auth_classes(is_authenticated=True)
class AssociateUserOAuthAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()

        UserSocialAuth.objects.create(
            user=user,
            uid=email,
            provider="custom-oauth",
        )

        return ResponseSuccess(content_type="application/json")


@view_auth_classes(is_authenticated=True)
class CourseChangeModeAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        course_id = request.data.get("course_id")
        mode_slug = request.data.get("mode")
        enrollment = CourseEnrollment.objects.get(user__username=username, course__id=course_id)
        try:
            course_mode = CourseMode.objects.get(course=enrollment.course, mode_slug=mode_slug)
        except CourseMode.DoesNotExist:
            course_mode = CourseMode.objects.create(
                course=enrollment.course,
                mode_slug=mode_slug,
                mode_display_name=mode_slug.capitalize(),
            )
        enrollment.mode = course_mode.mode_slug
        enrollment.save()
        return ResponseSuccess(content_type="application/json")


@view_auth_classes(is_authenticated=True)
class CourseGrantRoleAccessAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        course_id = request.data.get("course_id")
        moderator_role = Role.objects.get(name=FORUM_ROLE_MODERATOR, course_id=course_id)
        try:
            user = User.objects.get(username=username)
            course = CourseOverview.objects.get(id=course_id)
        except (User.DoesNotExist, CourseOverview.DoesNotExist):
            return HttpResponseNotFound

        CourseDataResearcherRole(course.id).add_users(user)
        moderator_role.users.add(user)
        return ResponseSuccess(content_type="application/json")


@view_auth_classes(is_authenticated=True)
class CourseRevokeRoleAccessAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        course_id = request.data.get("course_id")
        moderator_role = Role.objects.get(name=FORUM_ROLE_MODERATOR, course_id=course_id)
        try:
            user = User.objects.get(username=username)
            course = CourseOverview.objects.get(id=course_id)
        except (User.DoesNotExist, CourseOverview.DoesNotExist):
            return HttpResponseNotFound

        CourseDataResearcherRole(course.id).remove_users(user)
        moderator_role.users.remove(user)
        return ResponseSuccess(content_type="application/json")


@view_auth_classes(is_authenticated=True)
class StudentHistoryAPIView(APIView):
    def get(self, request, username, course_key):
        user = User.objects.get(username=username)
        student_modules = StudentModule.objects.filter(student=user, course_id=course_key).order_by("created")
        results = [
            {
                "id": sm.id,
                "grade": sm.grade,
                "max_grade": sm.max_grade,
                "done": sm.done,
                "module_type": sm.module_type,
            }
            for sm in student_modules
        ]
        return Response(results, content_type="application/json")


@view_auth_classes(is_authenticated=True)
class CourseActiveStudentsAPIView(APIView):
    def get(self, request, course_key):
        exclude_removed = request.query_params.get("exclude_removed", "true") == "true"
        active_user_ids = StudentModule.objects.filter(course_id=course_key).filter(
            student__courseenrollment__mode="honor"
        )
        if exclude_removed:
            active_user_ids = active_user_ids.filter(student__courseenrollment__is_active=True)
        active_user_ids = active_user_ids.values_list("student", flat=True).distinct()
        active_users = User.objects.filter(id__in=active_user_ids)
        results = {
            "total": active_users.count(),
            "users": [
                {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                }
                for user in active_users
            ],
        }
        return Response(results, content_type="application/json")


@view_auth_classes(is_authenticated=True)
class StudentCourseGradeAPIView(APIView):
    def get(self, request, username, course_key):
        user = User.objects.get(username=username)
        try:
            grade = PersistentCourseGrade.objects.get(user_id=user.id, course_id=course_key)
            response = {
                "has_final_grade": True,
                "percent_grade": grade.percent_grade,
                "letter_grade": grade.letter_grade,
            }
        except PersistentCourseGrade.DoesNotExist:
            response = {"has_final_grade": False}
        return ResponseSuccess(response)


@view_auth_classes(is_authenticated=True)
class CourseInfoAPIView(APIView):
    def get(self, request, course_key):
        response = {}
        try:
            key = CourseKey.from_string(course_key)
            response = get_course_info(key)
        except Exception as exc:  # noqa: B902
            response["error"] = str(exc)
        finally:
            return ResponseSuccess(response)  # noqa: B012


@view_auth_classes(is_authenticated=True)
class CoursePointsAPIView(APIView):
    def get(self, request, course_key):
        response = {"points": None}
        try:
            points = CoursePoints.objects.get(course_id=course_key)
            response["points"] = points.points
        except CoursePoints.DoesNotExist:
            response["error"] = "This course does not define points"
        finally:
            return ResponseSuccess(response)  # noqa: B012

    def post(self, request, course_key):
        response = {}
        points = int(request.data.get("points"))
        try:
            course_points = CoursePoints.objects.get(course_id=course_key)
            if course_points:
                response["points"] = points
                if points.points != course_points and request.data.get("force"):
                    course_points.points = points
                    course_points.save()
                    response["updated"] = True
                else:
                    response["exists"] = True
        except CoursePoints.DoesNotExist:
            course_points = CoursePoints.objects.create(course_id=course_key, points=points)
            response["created"] = True
            response["points"] = points
        return ResponseSuccess(response)


@view_auth_classes(is_authenticated=True)
class CourseRerunAPIView(APIView):
    def post(self, request):
        from cms.djangoapps.contentstore.views.course import rerun_course

        source_course_key = request.POST.get("source_course_key")
        username = request.POST.get("user")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            PLUGIN_API_USER_NAME = os.environ.get("PLUGIN_API_USER_NAME") or "pluginservice"
            user = User.objects.get(username=PLUGIN_API_USER_NAME)
        source_course_key = CourseKey.from_string(source_course_key)
        org = request.POST.get("org")
        number = request.POST.get("number")
        run = request.POST.get("run")
        display_name = request.POST.get("display_name")
        wiki_slug = f"{org}.{number}.{run}"
        fields = {
            "start": CourseFields.start.default,
            "wiki_slug": wiki_slug,
            "display_name": display_name,
        }
        destination_course_key = rerun_course(user, source_course_key, org, number, run, fields)
        return ResponseSuccess({"key": str(destination_course_key)})


@view_auth_classes(is_authenticated=True)
class CourseCertificateAPIView(APIView):
    """
    Assert a  course has certificate set up and set it up if it does not
    """

    def post(self, request, course_id):
        from cms.djangoapps.contentstore.views.certificates import (
            CertificateManager,
            Certificate,
        )

        signatory_name = request.POST.get("signatory_name")
        signatory_title = request.POST.get("signatory_title")
        signatory_org = request.POST.get("signatory_org")
        signatory_image_path = request.POST.get("signatory_image")
        PLUGIN_API_USER_NAME = os.environ.get("PLUGIN_API_USER_NAME") or "pluginservice"
        user = User.objects.get(username=PLUGIN_API_USER_NAME)
        course_key = CourseKey.from_string(course_id)
        course_mode = CourseMode.objects.filter(course_id=course_key, mode_slug="honor").first()
        if not course_mode:
            course_mode = CourseMode.objects.create(course_id=course_key, mode_slug="honor")
        cert_config = CertificateGenerationCourseSetting.objects.filter(course_key=course_key).first()
        if not cert_config:
            cert_config = CertificateGenerationCourseSetting.objects.create(
                course_key=course_key,
                self_generation_enabled=True,
                language_specific_templates_enabled=True,
            )
        store = modulestore()
        course = store.get_course(course_key)
        if not course.certificates or not course.certificates["certificates"]:
            certificate_data = CertificateManager.parse(
                json.dumps(
                    {
                        "name": f"{course.display_name}",
                        "description": "",
                        "version": 1,
                        "is_active": True,
                        "editing": True,
                        "signatories": [
                            {
                                "name": signatory_name,
                                "title": signatory_title,
                                "organization": signatory_org,
                                "signature_image_path": signatory_image_path,
                            }
                        ],
                    }
                )
            )
            CertificateManager.assign_id(course, certificate_data)
            certificate = Certificate(course, certificate_data)
            cert = CertificateManager.serialize_certificate(certificate)
            course.certificates["certificates"] = [cert]
            store.update_item(course, user.id)
            return ResponseSuccess(cert)
        return ResponseSuccess(course.certificates["certificates"][0])


@view_auth_classes(is_authenticated=True)
class CourseBulkEmailAPIView(APIView):
    """
    Ensure that the course has bulk email activated
    """

    def post(self, request, course_id):
        course_key = CourseKey.from_string(course_id)
        course_auth, _ = CourseAuthorization.objects.get_or_create(course_id=course_key, email_enabled=True)
        return ResponseSuccess({"enabled": course_auth.email_enabled})


class RefreshToken(APIView):
    def post(self, request):
        token = request.data.get("token")
        username = request.data.get("username")
        user = User.objects.get(username=username)
        token = create_jwt_for_user(user)
        return Response(
            {
                "token": str(token),
            },
            content_type="application/json",
        )


class APIInfoView(APIView):
    def get(self, request):
        return ResponseSuccess({"version": __version__})


@view_auth_classes(is_authenticated=True)
class DiscussionForum(APIView):
    def get_discussion_page(self, course_id, page):
        from lms.djangoapps.discussion.views import THREADS_PER_PAGE

        params = {
            "sort_key": "activity",
            "course_id": course_id,
            "context": "course",
            "per_page": THREADS_PER_PAGE,
            "page": page,
        }
        paginated_results = cc.Thread.search(params)
        return paginated_results.collection, paginated_results.num_pages

    def get_thread(self, thread_id):
        thread = cc.Thread.find(thread_id).retrieve(
            with_responses=True,
            recursive=True,
        )
        return thread

    def base_row(self, thread):
        row = {
            "course_id": thread["course_id"],
            "module": "",
            "section": "",
            "title": thread.get("title"),
            "pinned": "Yes" if thread.get("pinned") else "No",
        }
        return row

    def row(self, row, block):
        if "user_id" in block:
            user = User.objects.get(id=int(block["user_id"]))
            row["email"] = user.email

        row["content"] = block.get("body")
        row["char_count"] = len(row["content"])
        row["votes"] = block.get("votes", {}).get("count")
        row["num_responses"] = block.get("comments_count")
        row["post_type"] = block.get("type")
        row["created_at"] = block.get("created_at")
        return row

    def get(self, request, course_id):
        self.user = request.user
        self.course_id = course_id
        # course_key = CourseKey.from_string(course_id)
        # course = get_course(course_key)
        results = []
        page = total_pages = 1
        while page <= total_pages:
            collection, total_pages = self.get_discussion_page(course_id, page)
            for item in collection:
                thread = self.get_thread(item["id"])
                row = self.row(row=self.base_row(thread), block=item)
                results.append(row)
                for comment in thread.get("children", []):
                    row = self.row(row=self.base_row(thread), block=comment)
                    results.append(row)
            page += 1

        return Response(results, content_type="application/json")
