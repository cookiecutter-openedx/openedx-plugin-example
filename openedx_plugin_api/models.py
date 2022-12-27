from django.db import models


class CoursePoints(models.Model):
    course_id = models.CharField(max_length=250, null=False, blank=False)
    points = models.PositiveSmallIntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.course_id}: {self.points} points"
