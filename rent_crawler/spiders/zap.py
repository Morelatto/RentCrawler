from rent_crawler.spiders import BaseVrZapSpider


class ZapSpider(BaseVrZapSpider):
    name = 'zap'
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 5,
        'RETRY_ENABLED': False
    }
