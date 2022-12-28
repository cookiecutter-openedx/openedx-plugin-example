"""
Lawrence McDaniel - https://lawrencemcdaniel.com
oct-2021

CMS App edxapp signal receivers.

refer to docstring notes in common.lib.xmodule.xmodule.modulestore.django.SignalHandler
for best practices on setting these up.

Also see: https://docs.djangoproject.com/en/3.2/topics/signals/
"""
# Python
import logging

# Django
from django.dispatch import receiver
from celery import shared_task
from edx_django_utils.monitoring import set_code_owner_attribute

# Open edX
# see: https://discuss.openedx.org/t/django-plugin-app-works-with-some-django-signals-but-not-others/5949/3
from xmodule.modulestore.django import SignalHandler
from opaque_keys.edx.keys import CourseKey
from common.lib.xmodule.xmodule.modulestore.django import modulestore

# this repo
from .auditor import (
    eval_course_block_changes,
    write_log_delete_course,
    write_log_delete_item,
)
from .utils import get_user

log = logging.getLogger(__name__)
log.info("openedx_plugin_cms.signals loaded")


@shared_task()
@set_code_owner_attribute
def _course_publisher_hander(course_key_str):
    """
    asynchronous task launcher
    """
    course_key = CourseKey.from_string(course_key_str)
    eval_course_block_changes(course_key)


@receiver(SignalHandler.course_published, dispatch_uid="plugin_course_publish")
def _plugin_listen_for_course_publish(sender, course_key, **kwargs):  # pylint: disable=unused-argument
    """
    Receives publishing signal and logs block meta data and the user
    """
    user_id = kwargs.get("user_id")
    eval_course_block_changes(course_key, get_user(user_id))
    return


@receiver(SignalHandler.course_deleted, dispatch_uid="plugin_course_delete")
def _plugin_listen_for_course_delete(sender, course_key, **kwargs):  # pylint: disable=unused-argument
    """
    Catches the signal that a course has been deleted
    and logs the course_key and user
    """
    user_id = kwargs.get("user_id")
    write_log_delete_course(course_key, get_user(user_id))
    return


@receiver(SignalHandler.item_deleted, dispatch_uid="plugin_item_deleted")
def _plugin_handle_item_deleted(**kwargs):
    """
    Receives the item_deleted signal sent by Studio when an XBlock is removed from
    the course structure and logs the block_id and user

    Arguments:
        kwargs (dict): Contains the content usage key of the item deleted

    Returns:
        None
    """
    usage_key = kwargs.get("usage_key")
    if usage_key:

        # Strip branch info
        usage_key = usage_key.for_branch(None)
        user_id = kwargs.get("user_id")

        write_log_delete_item(usage_key, get_user(user_id))
    return


@receiver(SignalHandler.library_updated, dispatch_uid="plugin_library_update")
def _plugin_listen_for_library_update(sender, library_key, **kwargs):  # pylint: disable=unused-argument
    """
    Receives signal and ...
    """
    library_key_str = str(library_key)
    log.info(
        "course_key: {library_key_str}, sender: {sender}, kwargs: {kwargs}".format(
            sender=type(sender), library_key_str=library_key_str, kwargs=kwargs
        )
    )
    return
