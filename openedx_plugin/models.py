from __future__ import absolute_import
from django.db import models
from django.utils.translation import ugettext as _

from model_utils.models import TimeStampedModel

LMS_LANGUAGES = (
    ("en", "English"),
    ("es-419", "Español (Latinoamérica)"),  # Spanish (Latin America)
    ("pt-pt", "Português (Portugal)"),  # Portuguese (Portugal)
)

ALL_LANGUAGES = (
    ("en", "English"),
    ("es-419", "Español (Latinoamérica)"),  # Spanish (Latin America)
    ("pt-br", "Português (Brasil)"),  # Portuguese (Brazil)
    ("pt-pt", "Português (Portugal)"),  # Portuguese (Portugal)
    ("it-it", "Italiano (Italia)"),  # Italian (Italy)
    ("fr", "Français"),  # French
)


class MarketingSites(TimeStampedModel):
    """
    Registers a marketing site by language code.
    Examples:
    -------------------
    es-419  maps to https://example.org
    es-MX   maps to https://example.org
    en      maps to https://example.org
    en-US   maps to https://example.org
    """

    class Meta:
        unique_together = ("language", "province")

    language = models.CharField(
        blank=False,
        choices=ALL_LANGUAGES,
        max_length=20,
        help_text=_(u"A language code. Examples: en, en-US, es, es-419, es-MX"),
    )
    province = models.CharField(
        max_length=20,
        blank=True,
        help_text=_(
            u"A sub-region for the language code. Example: for language code en-US valid possibles include TX, FL, CA, DC, KY, etc."
        ),
    )
    site_url = models.URLField(
        default="https://example.org",
        blank=False,
        help_text=_(u"URL for for anchor tag for this language. Example: https://example.org/contact/"),
    )

    def __str__(self):
        return self.language + "-" + self.province


class Locale(TimeStampedModel):
    """
    Stores localized urls and translated html tag element values by language code
    Used in conjunction with Mako templates to localize example specific page content
    such as footer links.
    """

    class Meta:
        unique_together = ("element_id", "language")

    element_id = models.CharField(
        blank=False,
        max_length=255,
        help_text=_(u"An html element id. Example: example-locale-contact"),
    )
    language = models.CharField(
        blank=False,
        choices=LMS_LANGUAGES,
        max_length=20,
        help_text=_(u"A language code. Examples: en, en-US, es, es-419, es-MX"),
    )
    url = models.URLField(
        blank=False,
        help_text=_(u"URL for for anchor tag for this language. Example: https://example.org/contact/"),
    )
    value = models.CharField(
        blank=False,
        max_length=255,
        help_text=_(u"The text value of this html element. Example: Contacto"),
    )

    def __str__(self):
        return self.element_id + "-" + self.language


class Configuration(TimeStampedModel):
    u"""
    Creates the Rover Stepwise configuration table for api settings.
    """
    DEVELOP = u"dev"
    TEST = u"test"
    PRODUCTION = u"prod"

    configuration_type = (
        (DEVELOP, _(u"Development")),
        (TEST, _(u"Testing / QA")),
        (PRODUCTION, _(u"Production")),
    )
    type = models.CharField(
        max_length=24,
        blank=False,
        primary_key=True,
        choices=configuration_type,
        default=DEVELOP,
        unique=True,
        help_text=_(u"Type of Open edX environment in which this configuration will be used."),
    )
    example_host = models.URLField(
        max_length=255, blank=True, help_text=_(u"the URL pointing to some server.")
    )

    def __str__(self):
        return self.type
