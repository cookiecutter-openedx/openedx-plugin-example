import logging
from django.conf import settings
from urllib.parse import urlparse

from openedx.core.djangoapps.lang_pref.api import get_closest_released_language, released_languages
from openedx.core.djangoapps.lang_pref import LANGUAGE_KEY
from openedx.core.djangoapps.user_api.preferences.api import get_user_preference, set_user_preference

log = logging.getLogger(__name__)


def set_language_preference(request):
    """
    Preemptively set a language code preference based on
    1.) a language param that might be passed in the http request
    2.) the 2-character subdomain of the referer. example example.org == 'mx'
    """
    if not request.user or not request.user.is_authenticated:
        log.info("set_language_preference() - anonymous user, exiting.")
        return None

    language_param = request.GET.get("language")
    if language_param:
        log.info(
            "set_language_preference() found language url param of {language_param} in the request object".format(
                language_param=language_param
            )
        )

    preferred_language = get_user_preference(request.user, LANGUAGE_KEY)
    if preferred_language:
        log.info(
            "set_language_preference() found an existing saved language preference for user {username} of {preferred_language}. Ignoring url param.".format(
                username=request.user.username, preferred_language=preferred_language
            )
        )
        return None
    else:
        log.info(
            "set_language_preference() no language preference set for user {username}".format(
                username=request.user.username
            )
        )

    languages = released_languages()
    log.info("set_language_preference() available languages are: {languages}".format(languages=languages))

    # 2.) language code might be passed in as a parameter
    if language_param:
        closest_lang = get_closest_released_language(language_param)
        if not closest_lang:
            log.info("set_language_preference() no available language, exiting.")
            return None
        log.info(
            "openedx_plugin.utils.set_language_preference() (2) detected language param={language_param}. closest installed={closest_lang}".format(
                language_param=language_param, closest_lang=closest_lang
            )
        )
        set_user_preference(request.user, LANGUAGE_KEY, closest_lang)
        return None
    else:
        log.info(
            "set_language_preference() no language param found in the request header for user {username}".format(
                username=request.user.username
            )
        )

    # 3.) try infer a language preference from the referring host
    referer = urlparse(request.META.get("HTTP_REFERER", "Direct"))
    referer_domain = referer.netloc
    log.info(
        "set_language_preference() analyzing http referer {referer} with domain {domain}".format(
            referer=referer, domain=referer_domain
        )
    )
    if referer_domain and referer_domain[:2].lower() == "mx":
        closest_lang = get_closest_released_language("es_MX")
        if not closest_lang:
            log.info("set_language_preference() no available language, quiting.")
            return None
        log.info(
            "openedx_plugin.utils.set_language_preference() (3) detected referer_domain={referer_domain}. closest installed={closest_lang}".format(
                referer_domain=referer_domain, closest_lang=closest_lang
            )
        )
        set_user_preference(request.user, LANGUAGE_KEY, closest_lang)
        return None

    # 4.) defer to the language preference from openedx cookie
    # this case is taken care of by openedx.core.djangoapps.lang_pref.middleware.LanguagePreferenceMiddleware
    # cookie_lang_pref = request.COOKIES.get(settings.LANGUAGE_COOKIE, None)
