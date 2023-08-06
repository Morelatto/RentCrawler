# -*- coding: utf-8 -*-
import logging

from scrapy.logformatter import LogFormatter


class SpiderLogFormatter(LogFormatter):
    def scraped(self, item, response, spider):
        log_params = {
            'level': logging.DEBUG,
            'msg': "Scraped: New item code=%(code)s",
            'args': {
                'code': item['code'],
            }
        }
        if 'item_id' in item:
            log_params['msg'] += ' item_id=%(item_id)s'
            log_params['args']['item_id'] = item['item_id']
        return log_params

    def dropped(self, item, exception, response, spider):
        log_params = {
            'level': logging.WARNING,
            'msg': "Dropped: %(exception)s code=%(code)s",
            'args': {
                'code': item['code'],
                'exception': exception
            }
        }
        if 'item_id' in item:
            log_params['msg'] += ' item_id=%(item_id)s'
            log_params['args']['item_id'] = item['item_id']
        return log_params
