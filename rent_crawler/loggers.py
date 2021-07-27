# -*- coding: utf-8 -*-
import logging

from scrapy.logformatter import LogFormatter


class QuietLogFormatter(LogFormatter):
    def scraped(self, item, response, spider):
        return {
            'level': logging.DEBUG,
            'msg': "Scraped: New item code=%(code)s item_id=%(item_id)s",
            'args': {
                'code': item['code'],
                'item_id': item['item_id'],
            }
        }

    def dropped(self, item, exception, response, spider):
        return {
            'level': logging.WARNING,
            'msg': "Dropped: %(exception)s code=%(code)s item_id=%(item_id)s",
            'args': {
                'code': item['code'],
                'item_id': item['item_id'],
            }
        }
