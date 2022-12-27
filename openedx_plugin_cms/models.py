"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2021

Course Management Studio App Models
"""
from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth import get_user_model

from opaque_keys.edx.django.models import CourseKeyField, UsageKeyField

User = get_user_model()


class CourseAudit(TimeStampedModel):
    def __str__(self):
        return f"{self.a_order}"

    course_id = CourseKeyField(
        max_length=255,
        db_index=True,
        verbose_name="course_id Course Key",
        help_text="Example: course-v1:edX+DemoX+Demo_Course",
    )

    a_order = models.IntegerField(
        verbose_name="Order",
        help_text="the sequence in which this block is presented in the course, based on the outline format in Course Management Studio.",
        blank=True,
        null=True,
    )
    b_course = models.CharField(
        max_length=255,
        verbose_name="Course Display Name",
        help_text="The display name of the course from Course Management Studio.",
        blank=True,
        null=True,
    )
    c_module = models.CharField(
        max_length=255,
        verbose_name="Course Module",
        help_text="The display name of the Course Module (aka Chapter) in Course Management Studio.",
        blank=True,
        null=True,
    )
    d_section = models.CharField(
        max_length=255,
        verbose_name="Course Section",
        help_text="The display name of the Course Section in Course Management Studio.",
        blank=True,
        null=True,
    )
    e_unit = models.CharField(
        max_length=255,
        verbose_name="Course Unit",
        help_text="The display name of the Course Unit (aka Subsection) in Course Management Studio.",
        blank=True,
        null=True,
    )
    e2_block_type = models.CharField(
        max_length=255,
        verbose_name="Block Type",
        help_text="Type of XBlock. Usually chapter, sequential, vertical, html, discussion, or problem.",
        blank=True,
        null=True,
    )
    f_xblock_customized_html = models.TextField(
        max_length=255,
        verbose_name="XBlock Customized HTML",
        help_text="Raw html contents of this block",
        blank=True,
        null=True,
    )
    f_graded = models.CharField(
        max_length=255,
        verbose_name="Graded (Y/N)",
        help_text="True if this block contains graded content.",
        blank=True,
        null=True,
    )
    g_section_weight = models.FloatField(
        verbose_name="Section Weight",
        help_text="The section weight from the grading policy.",
        blank=True,
        null=True,
    )
    h_number_graded_sections = models.IntegerField(
        verbose_name="Number of Graded Sections",
        help_text="The number of graded content blocks within this section.",
        blank=True,
        null=True,
    )
    i_component_type = models.CharField(
        max_length=255,
        verbose_name="Component Type",
        help_text="For problem types only: the kind of Xblock used. Examples: imageresponse, customresponse, optionresponse, formularesponse, numericalresponse.",
        blank=True,
        null=True,
    )
    j_non_standard_element = models.BooleanField(
        verbose_name="Non-standard Element",
        help_text="True if this block contains non-standard content",
        blank=True,
        null=True,
    )
    k_problem_weight = models.FloatField(
        verbose_name="Problem Weight",
        help_text="The point potential of this problem based on the grading policy for the course.",
        blank=True,
        null=True,
    )
    m_iframe_external_url = models.URLField(
        verbose_name="iFrame external url",
        help_text="",
        blank=True,
        null=True,
    )
    m_external_links = models.TextField(
        verbose_name="External Links",
        help_text="A list of all links to sites outside of this Open edX platform installation",
        blank=True,
        null=True,
    )
    n_asset_type = models.TextField(
        max_length=255,
        verbose_name="Asset Type",
        help_text="The kind of file types referenced in any freeform html content in this block. Example: getting-started_x250.png",
        blank=True,
        null=True,
    )
    o_unit_url = models.URLField(
        verbose_name="LMS URL",
        help_text="",
        blank=True,
        null=True,
    )
    p_studio_url = models.URLField(
        verbose_name="Studio URL",
        help_text="",
        blank=True,
        null=True,
    )
    q_xml_filename = models.CharField(
        max_length=255,
        verbose_name="XML Filename",
        help_text="the full path to the xml file for this block, if it exists. Example: html/030e35c4756a4ddc8d40b95fbbfff4d4.xml",
        blank=True,
        null=True,
    )
    r_publication_date = models.DateTimeField(
        verbose_name="Publication Date",
        help_text="The original publication date of this block",
        db_index=True,
        blank=True,
        null=True,
    )
    s_changed_by = models.ForeignKey(
        User,
        verbose_name="Changed By",
        help_text="the username of the person who most recently published or modified this block.",
        on_delete=models.CASCADE,
        db_index=True,
        blank=True,
        null=True,
    )
    t_change_made = models.DateTimeField(
        verbose_name="Change Made",
        help_text="",
        db_index=True,
        blank=True,
        null=True,
    )


class CourseChangeLog(TimeStampedModel):
    class Meta:
        unique_together = ("location", "publication_date")

    def __str__(self):
        return f"{self.course_id}: {self.location}"

    DB_UPSERT = "u"
    DB_DELETE = "d"
    DB_OPERATIONS = [(DB_UPSERT, "Upsert"), (DB_DELETE, "Delete")]

    operation = models.CharField(max_length=1, choices=DB_OPERATIONS, default=DB_UPSERT)

    location = UsageKeyField(
        max_length=255,
        db_index=True,
        verbose_name="Location Usage Key",
        help_text="Example: block-v1:edX+DemoX+Demo_Course+type@vertical+block@vertical_1fef54c2b23b",
    )
    display_name = models.CharField(max_length=255)
    ordinal_position = models.IntegerField(blank=True, null=True)
    publication_date = models.DateTimeField(
        verbose_name="Publication Date",
        help_text="block publication date for this course block",
        blank=True,
        null=True,
    )

    url = models.URLField(
        verbose_name="LMS URL",
        blank=True,
        null=True,
        help_text="Example: https://dev.engineplatform.co.uk/courses/course-v1:edX+DemoX+Demo_Course/jump_to/block-v1:edX+DemoX+Demo_Course+type@vertical+block@vertical_1fef54c2b23b",
    )
    visible = models.BooleanField(default=True, verbose_name="Is Visible to Students")
    category = models.CharField(
        max_length=255,
        verbose_name="Block Category",
        help_text="course, chapter, vertical, sequential, xblock",
    )
    course_id = CourseKeyField(
        max_length=255,
        db_index=True,
        verbose_name="course_id Course Key",
        help_text="Example: course-v1:edX+DemoX+Demo_Course",
    )

    parent_location = UsageKeyField(max_length=255, db_index=True, blank=True, null=True)
    parent_url = models.URLField(
        max_length=255,
        help_text="The Usage Key for the Parent object in which this block is contained.",
        blank=True,
        null=True,
    )
    chapter_location = UsageKeyField(max_length=255, db_index=True, blank=True, null=True)
    chapter_url = models.URLField(
        max_length=255,
        help_text="The Usage Key for the Chapter in which this block is contained. Example: https://dev.engineplatform.co.uk/courses/course-v1:edX+DemoX+Demo_Course/jump_to_id/graded_interactions",
        blank=True,
        null=True,
    )
    sequential_location = UsageKeyField(max_length=255, db_index=True, blank=True, null=True)
    sequential_url = models.URLField(
        max_length=255,
        help_text="The Usage Key for the Section in which this block is contained. Example: https://dev.engineplatform.co.uk/courses/course-v1:edX+DemoX+Demo_Course/jump_to_id/basic_questions",
        blank=True,
        null=True,
    )
    vertical_location = UsageKeyField(max_length=255, db_index=True, blank=True, null=True)
    vertical_url = models.URLField(
        max_length=255,
        help_text="The Usage Key for the Vertical in which this block is contained. Example: https://dev.engineplatform.co.uk/courses/course-v1:edX+DemoX+Demo_Course/jump_to_id/vertical_d32bf9b2242c",
        blank=True,
        null=True,
    )

    #
    # edit_info
    # see: common.lib.xmodule.xmodule.modulestore
    #
    edit_info = models.CharField(
        max_length=255,
        help_text="JSON dict of edit tracking info",
        blank=True,
        null=True,
    )

    source_version = UsageKeyField(max_length=255, blank=True, null=True)
    update_version = UsageKeyField(
        max_length=255,
        help_text="Guid for the structure where this XBlock got its current field values. May point to a structure not in this structure's history (e.g., to a draft branch from which this version was published).",
        blank=True,
        null=True,
    )
    previous_version = UsageKeyField(
        max_length=255,
        help_text="Guid for the structure which previously changed this XBlock. (Will be the previous value of 'update_version'.)",
        blank=True,
        null=True,
    )

    original_usage = UsageKeyField(
        max_length=255,
        help_text="If this block has been copied from a library using copy_from_template, points to the original block in the library",
        null=True,
        blank=True,
    )
    original_usage_version = models.CharField(
        max_length=255,
        help_text="",
        blank=True,
        null=True,
    )

    release_date = models.DateTimeField(blank=True, null=True)
    published_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_published_by",
        blank=True,
        null=True,
    )
    published_on = models.DateTimeField(
        help_text="Datetime when this XBlock was published.",
        blank=True,
        null=True,
    )
    edited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_edited_by",
        blank=True,
        null=True,
    )
    edited_on = models.DateTimeField(
        help_text="Datetime when this XBlock's fields last changed.",
        blank=True,
        null=True,
    )
