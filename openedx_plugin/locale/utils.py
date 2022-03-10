"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Feb-2022

example theming utility functions
"""

import logging
from ast import Str

from openedx.core.djangoapps.lang_pref import LANGUAGE_KEY
from openedx.core.djangoapps.user_api.preferences.api import get_user_preference
from openedx.core.djangoapps.lang_pref.api import get_closest_released_language

from openedx_plugin.models import Locale, MarketingSites

log = logging.getLogger(__name__)


def get_marketing_site(request):
    """
    Returns the url to the marketing site for the user
    based on informatin that can be gleaned from the request object.

    First, determine the best possible language code for the user
    taking into account all available information and meta data we have about the user.

    Then, map the language code to a marketing site url based on data we've
    persisted to MarketingSites.

    example return value: https://example.org/
    """
    language = language_from_request(request)
    marketing_site = MarketingSites.objects.filter(language=language).first()
    return marketing_site.site_url


def language_from_request(request):
    """
    A robust effort to determine the most appropriate language code to use
    for purposes of determining the user's geographic region.

    This gets called a lot. Try to keep this a non-cached, order-1 operation!!
    """
    preferred_language = None

    # 1.) try to get the Open edX language setting chosen explicitely by the user
    #     using the language drop-down in the LMS site header.
    try:
        if request.user and request.user.is_authenticated:
            preferred_language = get_user_preference(request.user, LANGUAGE_KEY)
            log.info(
                "language_from_request() found an existing language preference of {preferred_language} for username {username}".format(
                    preferred_language=preferred_language, username=request.user.username
                )
            )
    except Exception:
        # is the user is not authenticated or if the user is logging out
        # then this is prone to raising an exception.
        pass

    # 2.) Look for a language code parameter in the request
    #     the marketing sites include CTA links such as
    #     https://lms.example.edu/example/dashboard?language=es-419
    if not preferred_language:
        preferred_language = request.GET.get("language")
        if preferred_language:
            # if necessary, reduce the language setting to the most closely installed language
            closest_released_language = get_closest_released_language(preferred_language)
            log.info(
                "language_from_request() found language param of {preferred_language} in the request params. Closest released language is {closest_released_language}".format(
                    preferred_language=preferred_language, closest_released_language=closest_released_language
                )
            )
            return closest_released_language

    # 3.) Try to grab the language code from Django middleware, if its installed
    # see: https://stackoverflow.com/questions/3356964/how-can-i-get-the-current-language-in-django
    if not preferred_language:
        try:
            if request.LANGUAGE_CODE:
                return request.LANGUAGE_CODE
        except Exception:
            pass

    # 4.) Try to grab the Django-assigned default language code, if its assigned.
    if not preferred_language:
        try:
            # the Django default language
            if request.LANGUAGE:
                return request.LANGUAGE
        except Exception:
            pass

    # 5.) All possible methods failed, so use the system default of English.
    if not preferred_language:
        # we should never make it this far ...
        # belt & suspenderes stop-gap
        preferred_language = "en"

    # -------------------------------------------------------------------------
    # some language codes are more general that we'd prefer for marketing purposes
    # In these cases we'll attempt to gather additional information about the
    # user from their profile.
    #
    # stuff that we can try:
    # - the Country setting in the user profile, if it's there
    # - an inspection of the email domain suffix of their user email address.
    #   example: yahoo.com.mx
    # - referrer data from the request headers
    # -------------------------------------------------------------------------
    if preferred_language == "es-419":
        # this is a generic Latin America setting (and the system default for Spanish)
        # that merits further inspection of the user's profile data in order to further
        # narrow down the appropriate region.

        # do yadda yadda to get the user's country setting from their profile

        return preferred_language

    return preferred_language


def anchor(element_id: Str, prefered_language="en"):
    """
    id: an html anchor tag id value
    example: example-about

    returns the URL and anchor element value based on the user's
    example
    """

    locale = Locale.objects.filter(element_id=element_id, language=prefered_language).first()
    if not locale:
        # try a simpler variation of the language code.
        prefered_language = prefered_language[:2]
        locale = Locale.objects.filter(element_id=element_id, language=prefered_language).first()

    if not locale:
        # try to grab the element in English.
        locale = Locale.objects.filter(element_id=element_id, language="en").first()

    if not locale:
        return {}

    return {"url": locale.url, "value": locale.value}
