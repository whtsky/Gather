import base64
import zlib

import bson.json_util as json

from raven.contrib.tornado import AsyncSentryClient as _Client


class AsyncSentryClient(_Client):
    def encode(self, data):
        """
        Serializes ``data`` into a raw string.
        """
        return base64.b64encode(zlib.compress(json.dumps(data).encode('utf8')))
