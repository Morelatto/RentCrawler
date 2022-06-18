# -*- coding: utf-8 -*-
import hashlib
import json
import logging

import redis as redis
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapyelasticsearch.scrapyelasticsearch import ElasticSearchPipeline

logging.getLogger('elasticsearch').setLevel(logging.ERROR)


class RentCrawlerPipeline:
    def process_item(self, item, spider):
        item_hash = hashlib.sha1()
        item_dict = ItemAdapter(item).asdict()
        item_json = json.dumps(item_dict, sort_keys=True)
        item_hash.update(item_json.encode('utf-8'))
        item['item_id'] = item_hash.hexdigest()
        return item


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


class ElasticSearchAdapterPipeline(ElasticSearchPipeline):
    def process_item(self, item, spider):
        item = ItemAdapter(item).asdict()
        return super().process_item(item, spider)
