from django.core.management.commands.runserver import Command as BaseCommand

from labeltree.management.commands.gbif_api import GBIF
from labeltree.management.commands.gbif_api import GBIFEntry

class Command(BaseCommand):
    help = "search for a specific"

    def add_arguments(self, parser):
        parser.add_argument("name")

    def handle(self, *args,
        name: str,
        **kwargs):

        entries = GBIF.entries_by_name(name, query=dict(rank="SPECIES"))
        print(entries)
