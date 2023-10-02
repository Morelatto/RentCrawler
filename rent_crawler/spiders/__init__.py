import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import scrapy
from scrapy_redis.spiders import RedisSpider

from rent_crawler.pages import VRZapListPage


@dataclass
class PageCrawlParams:
    request_data: dict
    page_data: dict

    @property
    def body(self) -> dict:
        return json.loads(self.request_data.get('body'))

    @body.setter
    def body(self, new_body):
        self.request_data['body'] = json.dumps(new_body)

    @property
    def url(self) -> str:
        return self.request_data.get('url')

    @url.setter
    def url(self, new_url):
        self.request_data['url'] = new_url

    def is_api(self):
        return 'api' in self.request_data.get('url')


class PageCrawlSpider(RedisSpider, ABC):

    def make_request_from_data(self, data):
        params = self._decode_data_from_redis(data)
        self.logger.info('Crawl params: %s', params)
        if params.is_api():
            yield from self.start_request(params)
        else:
            yield self.page_request(params)

    def _decode_data_from_redis(self, redis_data) -> PageCrawlParams:
        text = redis_data.decode(encoding=self.redis_encoding)
        params = json.loads(text)

        return PageCrawlParams(
            request_data=params.get('data'),
            page_data=params.get('params'),
        )

    @abstractmethod
    def start_request(self, params):
        pass

    @abstractmethod
    def page_request(self, params):
        pass

    # noinspection PyMethodOverriding
    @abstractmethod
    def parse(self, response, page, **kwargs):
        pass

    @abstractmethod
    def parse_page(self, response, page, **kwargs):
        pass


class BaseVrZapSpider(PageCrawlSpider):

    @classmethod
    def _build_url_for_request(cls, url: str, page_index: int, page_size: int):
        url_parts = urlparse(url)
        query_params = parse_qs(url_parts.query)
        query_params['from'] = [str(page_size * page_index)]
        query_params['size'] = [str(page_size)]
        final_url_parts = url_parts._replace(query=urlencode(query_params, doseq=True))
        final_url = urlunparse(final_url_parts)
        return final_url

    def start_request(self, params: PageCrawlParams):
        start, total = params.page_data.get('page_start'), params.page_data.get('total_pages')
        for page in range(start, start + total):
            params.url = self._build_url_for_request(
                url=params.request_data.get('url'),
                page_index=page,
                page_size=params.page_data.get('page_size')
            )
            yield scrapy.Request(
                **params.request_data,
                dont_filter=True,
                cb_kwargs={'page_number': page + 1, 'total_pages': total}
            )

    def parse(self, response, page: VRZapListPage, **kwargs):
        self.logger.info('Scraping page %d/%d', kwargs['page_number'], kwargs['total_pages'])
        yield from page.to_item()

    def page_request(self, params):
        raise NotImplementedError()

    def parse_page(self, response, page, **kwargs):
        raise NotImplementedError()
