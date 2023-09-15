# -*- coding: utf-8 -*-
BOT_NAME = "rent_crawler"

SPIDER_MODULES = ["rent_crawler.spiders"]
NEWSPIDER_MODULE = "rent_crawler.spiders"

CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 2

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2.5
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_DEBUG = True

COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False

SCRAPY_POET_PROVIDERS = {
    "rent_crawler.providers.BodyJsonProvider": 500,
}

DOWNLOADER_MIDDLEWARES = {
    # "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    # "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
    # "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
    # "scrapy_fake_useragent.middleware.RetryUserAgentMiddleware": 401,
    'scrapy_poet.InjectionMiddleware': 543,
}

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 "
    "Safari/601.3.9"
)

# FAKEUSERAGENT_PROVIDERS = [
#     "scrapy_fake_useragent.providers.FakeUserAgentProvider",
#     "scrapy_fake_useragent.providers.FakerProvider",
#     "scrapy_fake_useragent.providers.FixedUserAgentProvider",
# ]

# Use Scrapy-Redis's scheduler and dupefilter
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "rent_crawler.dupefilter.RedisDupeFilter"
DUPEFILTER_DEBUG = True

# Don't cleanup Redis queues, allows pause/resume crawls
SCHEDULER_PERSIST = True

# Schedule requests using a priority queue (FIFO by default)
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

ITEM_PIPELINES = {
    "rent_crawler.pipelines.MongoDBPipeline": 100
}

MONGODB_URI = 'mongodb://root:pass@localhost:27017'
MONGODB_DATABASE = 'rent'
MONGODB_UNIQUE_KEY = 'code'
MONGODB_ADD_TIMESTAMP = True
MONGODB_SEPARATE_COLLECTIONS = True

REDIS_HOST = "localhost"
REDIS_PORT = 6379
#REDIS_PASSWORD = "root"

LOG_FORMATTER = "rent_crawler.loggers.SpiderLogFormatter"
# LOG_FILE = 'spider_log.txt'
# LOG_STDOUT = True
LOG_LEVEL = 'DEBUG'

# HTTPERROR_ALLOW_ALL = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'

FEED_EXPORT_ENCODING = 'utf-8'
