from django.core.management.base import BaseCommand

from ...waffle import waffle_init


class Command(BaseCommand):
    help = "Ensure that all WaffleSwitch objects are initialized"

    def handle(self, *args, **options):
        waffle_init()
