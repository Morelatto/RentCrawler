from rent_crawler.spiders import BaseVrZapSpider


class VivaRealSpider(BaseVrZapSpider):
    name = 'viva_real'
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 5,
    }
