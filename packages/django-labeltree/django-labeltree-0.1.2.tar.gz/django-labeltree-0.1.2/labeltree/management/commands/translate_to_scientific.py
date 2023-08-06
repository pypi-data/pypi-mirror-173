import logging
import numpy as np
import requests
import typing as T

from django.core.management.commands.runserver import Command as BaseCommand
from tqdm.auto import tqdm
from urllib.parse import quote
from urllib.parse import urlencode

from labeltree.management.commands.gbif_api import GBIF

class Command(BaseCommand):
    help = "Translates a list of vernacular names to a list of scientific names"
    URL = "https://api.gbif.org/v1/"


    def add_arguments(self, parser):
        parser.add_argument('file_name')
        parser.add_argument('--sep', default=";")
        parser.add_argument('--output')


    def handle(self, *args,
        file_name: str,
        sep: str,
        output: str,
        skip_by_name: bool = False,
        **kwargs):

        content = np.loadtxt(file_name,
            dtype=[("name", "U255"), ("kr_nr", "U255")],
            delimiter=sep,)

        result = []
        for i, entry in enumerate(tqdm(content)):
            name, kr_nr = entry["name"], entry["kr_nr"]

            entries = GBIF.entries_by_name(name, query={
                "rank": "SPECIES", "class": "Aves"
            })

            if len(entries) == 1:
                result.append(list(entries.keys())[0])

            elif len(entries) == 0:
                print(name)

            elif len(entries) != 1:
                print(name, entries)


        if output is None:
            print(result)
            return

        with open(output, "w") as f:
            for res, entry in zip(result, content):
                f.write(f"{res};{entry['kr_nr']}\n")



    @classmethod
    def _is_valid(cls, speciesID: int) -> bool:
        response = cls._get(f"species/{speciesID}")
        # either a synonym or has issues
        return response["synonym"] or len(response.get("issues", [])) != 0
