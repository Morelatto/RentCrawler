from rent_crawler.items import PricesLoader, DetailsLoader, VivaRealApartmentLoader, VivaRealAddressLoader

import scrapy


class VivaRealSpider(scrapy.Spider):
    name = 'vivareal'
    start_urls = ['https://www.vivareal.com.br/aluguel/sp/sao-paulo/apartamento_residencial/']
    code_search_url = 'https://www.vivareal.com.br/busca-por-codigo/?id='

    def parse(self, response):
        for apartment in response.css('.results-list article'):
            loader = VivaRealApartmentLoader(selector=apartment)
            loader.add_value('address', self.get_address(apartment))
            loader.add_value('details', self.get_details(apartment))
            loader.add_value('prices', self.get_prices(apartment))
            loader.add_css('description', 'div.js-property-description::text')
            loader.add_css('code', 'a.js-card-title::attr(href)')

            item = loader.load_item()
            total = item['prices']['rent'] + item['prices'].get('condo', 0)
            if item['address']['district'] in self.settings['DISTRICTS_TO_DOWNLOAD'] \
                    and total < self.settings['MAX_PRICE']:
                yield scrapy.Request(self.code_search_url + item['code'], callback=self.parse_apartment,
                                     meta={'item': item})
            else:
                yield item

        next_page = response.css('a.js-change-page::attr(data-page)')[-1].extract()
        if next_page and int(next_page) <= 10:
            next_page = '{url}?pagina={page}'.format(url=self.start_urls[0], page=next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_apartment(self, response):
        item = response.meta['item']
        prices_loader = PricesLoader(item=item['prices'], selector=response)
        prices_loader.add_css('iptu', '.js-detail-iptu-price::text')

        loader = VivaRealApartmentLoader(item=item, selector=response)
        loader.add_xpath('img_urls', '//div[contains(@class, "H")]//img[contains(@class, "hK")]/@data-src')
        loader.add_css('characteristics', '.qn li::text')
        loader.add_value('prices', prices_loader.load_item())
        yield loader.load_item()

    @classmethod
    def get_address(cls, response):
        address_loader = VivaRealAddressLoader(selector=response)
        address_loader.add_css('street', 'h2 span::text')
        address_loader.add_css('district', 'h2 span::text')
        address_loader.add_css('city', 'h2 span::text')
        return address_loader.load_item()

    @classmethod
    def get_prices(cls, response):
        prices_loader = PricesLoader(selector=response)
        prices_loader.add_css('rent', '.property-card__values div::text')
        prices_loader.add_css('condo', '.js-condo-price::text')
        return prices_loader.load_item()

    @classmethod
    def get_details(cls, response):
        details_loader = DetailsLoader(selector=response)
        details_loader.add_css('size', 'li.property-card__detail-area span::text')
        details_loader.add_css('rooms', 'li.js-property-detail-rooms span::text')
        details_loader.add_css('bathrooms', 'li.js-property-detail-bathroom span::text')
        details_loader.add_css('garages', 'li.js-property-detail-garages span::text')
        return details_loader.load_item()
