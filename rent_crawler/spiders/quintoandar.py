import scrapy

from rent_crawler.pages import QuintoAndarPropertyHit, QuintoAndarListPage, QuintoAndarPropertyPage
from rent_crawler.spiders import PageCrawlSpider, PageCrawlParams


class QuintoAndarSpider(PageCrawlSpider):
    name = 'quinto_andar'
    url = 'https://quintoandar.com.br'

    @classmethod
    def _build_body_for_request(cls, body: dict, page_index: int, page_size: int):
        page_offset = (page_index - 1) * page_size
        body['filters']['page_size'] = page_size
        body['filters']['offset'] = page_offset
        return body

    def start_request(self, params: PageCrawlParams):
        start, total = params.page_data.get('page_start'), params.page_data.get('total_pages')
        for page in range(start, start + total):
            params.body = self._build_body_for_request(
                body=params.body,
                page_index=page,
                page_size=params.page_data.get('page_size')
            )
            yield scrapy.Request(
                **params.request_data,
                dont_filter=True,
                cb_kwargs={'page_number': page, 'total_pages': total}
            )

    def page_request(self, params):
        page = QuintoAndarPropertyHit(**params.request_data.get('hit'))
        return scrapy.Request(
            url=self.url + params.request_data.get('url'),
            callback=self.parse_page,
            meta=page.to_item(),
            cb_kwargs=params.page_data
        )

    def parse(self, response, page: QuintoAndarListPage, **kwargs):
        self.logger.info('Scraping page %d/%d', kwargs['page_number'], kwargs['total_pages'])
        for i, (url, hit) in enumerate(zip(page.property_urls, page.properties), start=1):
            yield {
                'data': {
                    'url': url,
                    'hit': hit
                },
                'params': {
                    'page_size': len(page.property_urls),
                    'page_number': kwargs['page_number'],
                    'total_pages': kwargs['total_pages'],
                }
            }

    def parse_page(self, response, page: QuintoAndarPropertyPage, **kwargs):
        try:
            return page.to_item()
        except Exception as e:
            self.logger.exception("An error occurred for url %s", response.url, e)
