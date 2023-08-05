from datetime import datetime
from dateutil.parser import isoparse
import json
from dataclasses import dataclass, asdict

import dacite
import requests

from spinsrv import spin

SERVE_URL = "https://serve.spinsrv.com"
RFC3339 = "%Y-%m-%dT%H:%M:%S.%f%z"


def key_from_json(j: dict):
    return spin.Key(
        type=spin.KeyType(j["Type"]),
        citizen=spin.CitizenName(j["Citizen"]),
        name=spin.KeyName(j["Name"]),
        data=j["Data"],
        meta=j["Meta"],
        created_at=isoparse(j["CreatedAt"]),
        expires_at=isoparse(j["ExpiresAt"]),
    )


class KeyServerHTTPClient(object):
    def __init__(self):
        self.url = "https://keys.spinsrv.com"

    def which(self, req: spin.KeyWhichRequest):
        url = self.url + "/which"
        j = requests.post(url, json=asdict(req)).json()
        return spin.KeyWhichResponse(
            key=key_from_json(j),
            error=j["Error"],
        )

    def temp(self, req: spin.KeyTempRequest):
        url = self.url + "/temp"
        j = requests.post(url, json=asdict(req)).json()
        print(j)
        return spin.KeyTempResponse(
            key=key_from_json(j["Key"]),
            private=j["Private"],
            error=j["Error"],
        )


class DirServerHTTPClient(object):
    def __init__(self):
        self.url = "https://dir.spinsrv.com"

    def lookup(self, pu, pr, ctzn, path):
        url = self.url + "/tree"
        req = {
            "Public": pu,
            "Private": pr,
            "Citizen": ctzn,
            "Path": path,
        }
        return requests.post(url, json=req).json()

    def list(self, pu, pr, ctzn, path):
        return self.tree(pu, pr, ctzn, path, 1)

    def tree(self, pu, pr, ctzn, path, level):
        url = self.url + "/tree"
        req = {
            "Public": pu,
            "Private": pr,
            "Citizen": ctzn,
            "Path": path,
            "Level": level,
        }
        return requests.post(url, json=req).json()


class BitServerHTTPClient(object):
    def __init__(self):
        self.url = "https://bit.spinsrv.com"

    def apply(self, pu, pr, ctzn, path):
        url = self.url + "/tree"
        req = {
            "Public": pu,
            "Private": pr,
            "Citizen": ctzn,
            "Path": path,
        }
        return requests.post(url, json=req).json()

    def list(self, pu, pr, ctzn, path):
        return self.tree(pu, pr, ctzn, path, 1)

    def tree(self, pu, pr, ctzn, path, level):
        url = self.url + "/tree"
        req = {
            "Public": pu,
            "Private": pr,
            "Citizen": ctzn,
            "Path": path,
            "Level": level,
        }
        return requests.post(url, json=req).json()


"""
    Cache is a simple object cache.
    Uses the fallback, sets the name to the get method.
"""


class Cache(object):
    def __init__(self, fallback, name):
        self.cache = {}
        self.f = fallback
        setattr(self, name, self.get)

    def get(self, name):
        if name in self.cache:
            out = cache[name]
            return cache[name]
        else:
            item = self.f(name)
            self._put(name, item)
            return item

    def _put(self, name, item):
        self.cache[name] = item
