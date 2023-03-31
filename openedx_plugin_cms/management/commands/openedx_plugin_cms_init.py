# coding=utf-8
from django.core.management.base import BaseCommand

from ...waffle import waffle_init


class Command(BaseCommand):
    help = "Verifies initialization records for all Django models in this plugin"

    def handle(self, *args, **options):
        waffle_init()
