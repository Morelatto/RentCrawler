import scrapy

from vr_crawler.items import ApartmentLoader


class QuotesSpider(scrapy.Spider):
    name = 'vivareal'
    start_url = 'https://www.vivareal.com.br/aluguel/sp/sao-paulo/apartamento_residencial/'

    def start_requests(self):
        return [scrapy.Request(url=self.start_url, headers={'Referer': 'https://www.vivareal.com.br'})]

    def parse(self, response):
        for res in response.css('.results-list article'):
            loader = ApartmentLoader(selector=res)
            loader.add_css('name', 'h2 a::text')
            loader.add_css('address', 'h2 span::text')

            details_loader = loader.nested_css('ul.property-card__details')
            details_loader.add_css('size', 'li.property-card__detail-area span::text')
            details_loader.add_css('rooms', 'li.js-property-detail-rooms span::text')
            details_loader.add_css('bathrooms', 'li.js-property-detail-bathroom span::text')
            details_loader.add_css('garages', 'li.js-property-detail-garages span::text')

            loader.add_css('rent', 'div.js-property-card__price-small::text')
            loader.add_css('condo', 'strong.js-condo-price::text')

            loader.add_css('description', 'div.js-property-description::text')
            yield loader.load_item()

        next_page = response.css('a.js-change-page::attr(data-page)')[-1].extract()
        if next_page:
            next_page = '{url}?pagina={page}'.format(url=self.start_url, page=next_page)
            yield scrapy.Request(next_page, callback=self.parse)
