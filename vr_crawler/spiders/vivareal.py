import scrapy
from scrapy import Request

from vr_crawler.items import ApartmentLoader


class QuotesSpider(scrapy.Spider):
    name = 'vivareal'
    start_urls = ['https://www.vivareal.com.br/aluguel/sp/sao-paulo/apartamento_residencial/']

    def start_requests(self):
        requests = []
        for url in self.start_urls:
            requests.append(Request(url=url, headers={'Referer': 'https://www.vivareal.com.br'}))
        return requests

    def parse(self, response):
        for res in response.css('.results-list article'):
            loader = ApartmentLoader(selector=res)
            loader.add_css('name', 'h2 a::text')
            loader.add_css('address', 'h2 span::text')

            # details = res.css('ul.property-card__details')
            # loader.add_css('size', details.css('li.property-card__detail-area span::text').extract())
            # loader.add_css('rooms', details.css('li.js-property-detail-rooms span::text').extract())
            # loader.add_css('bathrooms', details.css('li.js-property-detail-bathroom" span::text').extract())
            # loader.add_css('garages', details.css('li.js-property-detail-garages" span::text').extract())

            loader.add_css('rent', 'div.js-property-card__price-small::text')
            loader.add_css('condo', 'strong.js-condo-price::text')

            loader.add_css('description', 'div.js-property-description::text')
            return loader.load_item()
