# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline

import logging
import os
import scrapy
import sqlite3

INFO_FILE_NAME = 'info'
MAX_PRICE = 2000
DISTRICTS_TO_DOWNLOAD = ['Jardim Paulistano', 'Pinheiros', 'Jardim Europa', 'Jardins', 'Jardim América',
                         'Cerqueira César', 'Jardim Paulista', 'Bela Vista', 'Consolação', 'Paraíso', 'Vila Mariana',
                         'Chácara Klabin', 'Higienópolis', 'Aclimação']


# TODO debug with zap
class ApartmentPicturesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        return '{}/{}/{}.jpg'.format(request.meta['district'], request.meta['code'], request.meta['index'])

    def get_media_requests(self, item, info):
        item_prices = item['prices']
        total = item_prices.get('rent', 0) + item_prices.get('condo', 0) + item_prices.get('iptu', 0)
        if item['address']['district'] in DISTRICTS_TO_DOWNLOAD and total < MAX_PRICE:
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
