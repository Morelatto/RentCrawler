import datetime

import scrapy
from scrapy_redis import get_redis_from_settings


class RedisStatsExporter:
    @classmethod
    def from_crawler(cls, crawler):
        redis_conn = get_redis_from_settings(crawler.settings)
        exporter = cls(redis_conn)
        crawler.signals.connect(exporter.spider_closed, signal=scrapy.signals.spider_closed)
        return exporter

    def __init__(self, server):
        self.server = server

    def spider_closed(self, spider, reason):
        timestamp = datetime.datetime.utcnow().isoformat()
        spider_key = f"{spider.name}:{timestamp}"
        stats = spider.crawler.stats.get_stats()
        for key, value in stats.items():
            if isinstance(value, datetime.datetime):
                value = value.isoformat()
            self.server.hset(spider_key, key, value)