import base64
import zlib

from raven.utils.json import json, BetterJSONEncoder
from raven.contrib.tornado import AsyncSentryClient as _Client
from bson.objectid import ObjectId

class PBBJSONEncoder(BetterJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(PBBJSONEncoder, self).default(obj)


class AsyncSentryClient(_Client):
    def encode(self, data):
        """
        Serializes ``data`` into a raw string.
        """
        s = json.dumps(data, cls=PBBJSONEncoder).encode('utf8')
        return base64.b64encode(zlib.compress(s))
