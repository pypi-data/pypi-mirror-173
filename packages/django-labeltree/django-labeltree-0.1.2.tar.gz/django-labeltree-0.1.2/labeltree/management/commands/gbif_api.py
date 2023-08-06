from __future__ import annotations

import requests
import typing as T

from dataclasses import dataclass
from dataclasses import fields
from munch import munchify
from urllib.parse import quote
from urllib.parse import urlencode

def _clean_name(name: str) -> str:
    return name.replace("-", " ").lower()

@dataclass
class GBIFEntry:
    key: int
    canonicalName: str
    rank: str

    parent: str
    parentKey: int

    synonym: bool
    issues: T.List

    vernacularNames: T.List

    vernacularLanguages = ["eng", "deu"]

    def __post_init__(self, *args, **kwargs):
        self.vernacularNames = [
            entry for entry in self.vernacularNames
            if entry["language"] in self.vernacularLanguages]

    def resolve(self):
        resp = GBIF.species(self.key)
        if "nubKey" in resp:
            newResp = GBIF.species(resp.nubKey)
            self.update(newResp)

    def update(self, entries):
        for field in fields(self):
            if field.name in entries:
                setattr(self, field.name, entries[field.name])

    @classmethod
    def new(cls, entries: dict) -> GBIFEntry:
        return cls(**{field.name: entries.get(field.name, None) for field in fields(cls)})

    @property
    def valid(self) -> bool:
        if self.synonym:
            return False
        resp = GBIF.species(self.key)
        backbone_issue = "BACKBONE_MATCH_NONE" in resp.issues

        # if has_issues:
        #     print(self)
        #     print(resp.issues)

        return not (backbone_issue or resp.synonym)

    @property
    def has_issues(self) -> bool:
        return self.issues is not None and len(self.issues) != 0


    def is_called(self, name):
        _ = _clean_name
        return any([_(entry.vernacularName) == _(name)
            for entry in self.vernacularNames])



class GBIF:
    URL = "https://api.gbif.org/v1/"

    @classmethod
    def get(cls, path: str, query: T.Optional = None) -> T.Dict:
        """ generic GET method """

        url = f"{cls.URL}{path}"

        if query is not None:
            query_str = urlencode(query, quote_via=quote)
            url = f"{url}?{query_str}"

        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @classmethod
    def match(cls, query: dict = None) -> dict:
        return munchify(cls.get("species/match", query))

    @classmethod
    def species(cls, speciesID: int, query: dict = None) -> dict:
        return munchify(cls.get(f"species/{speciesID}", query))

    @classmethod
    def search(cls, name: str, query: dict = None) -> dict:
        if query is None:
            query = {"q": name}
        else:
            query["q"] = name
        return munchify(cls.get(f"species/search", query))


    @classmethod
    def entries_by_name(self, name, query) -> GBIFEntry:

        resp = GBIF.search(name, query=query)

        entries = {}
        for result in resp["results"]:
            entry = GBIFEntry.new(result)

            if entry.canonicalName in entries:
                continue

            if not entry.is_called(name):
                continue

            entry.resolve()
            if not entry.valid:
                continue
            entries[entry.canonicalName] = entry


        if any([entry for entry in entries.values() if not entry.has_issues]):
            entries = {key: entry for key, entry in entries.items() if not entry.has_issues}

        return entries

