from datetime import datetime
from dateutil.parser import isoparse
import json
from dataclasses import dataclass, asdict

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
        return spin.KeyWhichResponse.from_json(
            requests.post(url, json=req.to_json()).json()
        )

    def temp(self, req: spin.KeyTempRequest):
        url = self.url + "/temp"
        return spin.KeyTempResponse.from_json(
            requests.post(url, json=req.to_json()).json()
        )


class DirServerHTTPClient(object):
    def __init__(self):
        self.url = "https://dir.spinsrv.com"

    def lookup(self, req: spin.DirLookupRequest):
        url = self.url + "/lookup"
        return spin.DirLookupResponse.from_json(
            requests.post(url, json=req.to_json()).json()
        )

    def tree(self, req: spin.DirTreeRequest):
        url = self.url + "/tree"
        return spin.DirTreeResponse.from_json(
            requests.post(url, json=req.to_json()).json()
        )

    def apply(self, req: spin.DirApplyRequest):
        url = self.url + "/apply"
        return spin.DirApplyResponse.from_json(
            requests.post(url, json=req.to_json()).json()
        )


class BitServerHTTPClient(object):
    def __init__(self):
        self.url = "https://store.spinsrv.com"

    def apply(self, req: spin.BitApplyRequest):
        url = self.url + "/apply"
        print(req.to_json())
        return spin.BitApplyResponse(
            requests.post(url, json=req.to_json()).json()
        )


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
