import hashlib
import json

from scrapy.utils.python import to_unicode
from scrapy_redis.dupefilter import RFPDupeFilter
from w3lib.url import canonicalize_url


class RedisDupeFilter(RFPDupeFilter):

    def request_fingerprint(self, request):
        fingerprint_data = {
            "method": to_unicode(request.method),
            "url": canonicalize_url(request.url),
            "body": request.meta.get('id') or (request.body or b"").hex(),
        }
        fingerprint_json = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.sha1(fingerprint_json.encode("utf-8")).hexdigest()
