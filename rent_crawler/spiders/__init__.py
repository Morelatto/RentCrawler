import scrapy

from rent_crawler.items import VRZapProperty
from rent_crawler.pages import VRZapListPage


class BaseVrZapSpider(scrapy.Spider):
    def __init__(self, start=1, pages=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_page = int(start)
        self.pages_to_crawl = int(pages)

    def parse(self, response: scrapy.http.Response, page: VRZapListPage, **kwargs) -> VRZapProperty:
        self.logger.info('Scraping page %d/%d', kwargs['page_number'], kwargs['total_pages'])
        yield from page.to_item()
