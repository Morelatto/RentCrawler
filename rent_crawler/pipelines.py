# -*- coding: utf-8 -*-
import hashlib
import json

import redis as redis
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class RentCrawlerPipeline:
    def process_item(self, item, spider):
        m = hashlib.md5()
        j = json.dumps(ItemAdapter(item).asdict(), sort_keys=True)
        m.update(j.encode('utf-8'))
        item['item_id'] = m.hexdigest()
        return ItemAdapter(item).asdict()


class RedisDuplicatePipeline:
    key_prefix = {
        'vivareal': 'VR',
        'zap': 'ZAP',
        'quintoandar': 'QUINTO',
    }

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
            redis_id = f"{self.key_prefix[spider.name]}:{item['item_id']}"
            existing_id = self.redis_client.get(redis_id)
            if existing_id is not None:
                raise DropItem('Duplicate item found')
            self.redis_client.set(redis_id, 'SEEN')

        return item
