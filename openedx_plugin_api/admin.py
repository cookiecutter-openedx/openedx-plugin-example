from django.contrib import admin
from .models import CoursePoints


class CoursePointsAdmin(admin.ModelAdmin):
    pass


admin.site.register(CoursePoints, CoursePointsAdmin)
