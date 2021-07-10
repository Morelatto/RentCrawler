# -*- coding: utf-8 -*-
import hashlib
import json
import logging
from datetime import datetime
try:
    import zoneinfo
except ImportError:
    # noinspection PyUnresolvedReferences
    from backports import zoneinfo

import redis as redis
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy_dynamodb import DynamoDbPipeline


logging.getLogger('boto3').setLevel(logging.ERROR)
logging.getLogger('botocore').setLevel(logging.ERROR)


class RentCrawlerPipeline:
    def process_item(self, item, spider):
        m = hashlib.md5()
        j = json.dumps(ItemAdapter(item).asdict(), sort_keys=True)
        m.update(j.encode('utf-8'))
        item['item_id'] = m.hexdigest()
        item['scrapped_at'] = datetime.now(zoneinfo.ZoneInfo("America/Sao_Paulo")).isoformat()
        return item


class RedisDuplicatePipeline:
    def __init__(self, redis_host, redis_port):
        if redis_host is not None:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        redis_host = settings.get('REDIS_HOST')
        redis_port = settings.get('REDIS_PORT', default=6379)
        return cls(redis_host, redis_port)

    def process_item(self, item, spider):
        if self.redis_client is None:
            return item

        if 'item_id' in item:
            item_id = item['item_id']
            existing_id = self.redis_client.get(item_id)
            if existing_id is not None:
                raise DropItem(f"Duplicate item found: {item}")
            self.redis_client.set(item_id, 'SEEN')

        return item


class AwsDynamoDbPipeline(DynamoDbPipeline):
    pass
