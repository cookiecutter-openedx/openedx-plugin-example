# coding=utf-8
"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2021

Admin registration for openedx_plugin_cms
"""


from django.contrib import admin

from .models import CourseChangeLog, CourseAudit


class CourseAuditAdmin(admin.ModelAdmin):
    """Admin for Audit Report data"""

    ordering = ("-id",)
    search_fields = [
        "course_id",
        "s_changed_by__username",
        "b_course",
        "c_module",
        "d_section",
        "e_unit",
        "e2_block_type",
    ]
    list_display = (
        "id",
        "course_id",
        "a_order",
        "created",
        "modified",
        "b_course",
        "c_module",
        "d_section",
        "e_unit",
        "e2_block_type",
        "r_publication_date",
        "s_changed_by",
        "t_change_made",
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CourseChangeLogAdmin(admin.ModelAdmin):
    """Admin for course email."""

    # readonly_fields = ('sender',)
    # list_display = ('user', 'course_id')
    pass


admin.site.register(CourseChangeLog, CourseChangeLogAdmin)
admin.site.register(CourseAudit, CourseAuditAdmin)
