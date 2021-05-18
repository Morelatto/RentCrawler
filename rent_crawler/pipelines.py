# -*- coding: utf-8 -*-
import os

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy_dynamodb import DynamoDbPipeline

INFO_FILE_NAME = 'info'


# TODO debug with zap
class ApartmentPicturesPipeline(ImagesPipeline):
    """Pipeline that downloads image urls from item. Also creates a file with information from the item."""

    def file_path(self, request, response=None, info=None):
        return '{}/{}/{}.jpg'.format(request.meta['district'], request.meta['code'], request.meta['index'])

    def get_media_requests(self, item, info):
        if 'img_urls' in item and len(item['img_urls']) > 0:
            for i, img_url in enumerate(item['img_urls']):
                meta = {'code': item['code'], 'index': i, 'district': item['address']['district']}
                yield scrapy.Request(url=img_url, meta=meta)
            self.create_info_file(item)

    @staticmethod
    def create_info_file(item):
        path = 'pictures/{}/{}'.format(item['address']['district'], item['code'])
        os.makedirs(path, exist_ok=True)
        with open('{}/{}.txt'.format(path, INFO_FILE_NAME), 'w+') as f:
            f.write(str(item))


class AwsDynamoDbPipeline(DynamoDbPipeline):
    pass
