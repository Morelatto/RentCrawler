# -*- coding: utf-8 -*-
BOT_NAME = "rent_crawler"

SPIDER_MODULES = ["rent_crawler.spiders"]
NEWSPIDER_MODULE = "rent_crawler.spiders"

CONCURRENT_REQUESTS_PER_DOMAIN = 2

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 3
AUTOTHROTTLE_DEBUG = False

COOKIES_ENABLED = True
TELNETCONSOLE_ENABLED = False

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "rent_crawler.dupefilter.RedisDupeFilter"
DUPEFILTER_DEBUG = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
SCHEDULER_PERSIST = True

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
    "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
    "scrapy_fake_useragent.middleware.RetryUserAgentMiddleware": 401,
    'scrapy_poet.InjectionMiddleware': 543,
}

FAKEUSERAGENT_PROVIDERS = [
    "scrapy_fake_useragent.providers.FakeUserAgentProvider",
    "scrapy_fake_useragent.providers.FakerProvider",
]

ITEM_PIPELINES = {
    "rent_crawler.pipelines.RentItemPipeline": 100,
}

MONGODB_URI = 'mongodb://root:pass@localhost:27017'
MONGODB_DATABASE = 'rent'
MONGODB_UNIQUE_KEY = 'code'

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_START_URLS_KEY = '%(name)s:start_urls'

LOG_FORMATTER = "rent_crawler.loggers.SpiderLogFormatter"
LOG_STDOUT = True
LOG_LEVEL = 'DEBUG'

FEED_EXPORT_ENCODING = 'utf-8'

SCRAPY_POET_PROVIDERS = {
    "rent_crawler.providers.BodyJsonProvider": 500,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'

EXTENSIONS = {
    'rent_crawler.extensions.RedisStatsExporter': 500,
}
