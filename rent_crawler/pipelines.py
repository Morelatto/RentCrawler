# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline

import logging
import os
import scrapy
import sqlite3

INFO_FILE_NAME = 'info'

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class ApartmentPipeline:
    def __init__(self):
        self.db = r'apartments.sqlite'
        self.table = 'apartments'
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()
        self.__create_table()

    def process_item(self, item, _):
        self.__upsert(item)
        self.connection.commit()
        return item

    def __upsert(self, item):
        item_address = item['address']
        item_details = item['details']
        item_prices = item['prices']
        values = (item_address.get('street'), item_address.get('district'), item_address.get('city'),
                  item_details.get('size'), item_details.get('rooms'), item_details.get('bathrooms'),
                  item_details.get('garages'), item_prices.get('rent'), item_prices.get('condo'), item.get('iptu'),
                  item.get('characteristics'), item.get('description'), item.get('source'), item.get('updated'),
                  item.get('code'))
        try:
            self.cursor.execute("INSERT INTO {} VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?, ?);".format(self.table), values)
        except sqlite3.IntegrityError:
            logger.debug('Updating item already on db: ' + item.get('code'))
            self.cursor.execute("UPDATE {} SET street = ?, district = ?, city = ?, size = ?, rooms = ?, bathrooms = ?, "
                                "garages = ?, rent = ?, condo = ?, iptu=?, characteristics=?, description = ?, "
                                "source = ?, updated = ? WHERE code = ?;".format(self.table), values)

    def __create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS {} (street TEXT, district TEXT, city TEXT, size INT, rooms INT,"
                            " bathrooms INT, garages INT, rent INT, condo INT, iptu INT, characteristics TEXT,"
                            " description TEXT, source TEXT, updated TEXT, code INT PRIMARY KEY)".format(self.table))
        self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()


class ApartmentPicturesPipeline(ImagesPipeline):
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
