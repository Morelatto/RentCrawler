import logging

from rent_crawler.items import QuintoAndarProperty
from scrapy import Request
from scrapy_redis import get_redis_from_settings

logger = logging.getLogger(__name__)


class RedisKeySpiderMiddleware:
    logger = logger

    def __init__(self, server, spider_name, key, debug=False):
        self.server = server
        self.spider_name = spider_name
        self.key = key
        self.debug = debug

    @classmethod
    def from_crawler(cls, crawler):
        spider_name = crawler.spider.name
        return cls.from_settings(crawler.settings, spider_name)

    @classmethod
    def from_settings(cls, settings, spider_name):
        server = get_redis_from_settings(settings)
        key = f'dupefilter:{spider_name}'
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(server, spider_name=spider_name, key=key, debug=debug)

    def _process_spider_output(self, output, response):
        if isinstance(output, Request) and not output.dont_filter:
            exists = self.server.sismember(self.key, output.meta.get('key'))
            if exists:
                self.logger.info("Ignoring page already visited with no changes: %s" % output)
                return None
        elif isinstance(output, (QuintoAndarProperty, dict)):
            added = self.server.sadd(self.key, response.request.meta.get('key'))
            if added and self.debug:
                self.logger.debug('Added page ID to redis for future deduplication')

        return output

    def process_spider_output(self, response, result, _):
        for r in result:
            process_result = self._process_spider_output(r, response)
            if process_result:
                yield process_result

    async def process_spider_output_async(self, response, result, _):
        async for r in result:
            process_result = self._process_spider_output(r, response)
            if process_result:
                yield process_result
