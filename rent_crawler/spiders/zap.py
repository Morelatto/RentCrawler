from rent_crawler.items import ApartmentLoader, ZapAddressLoader, PricesLoader, DetailsLoader, ZapDetails, ZapPrices

import re
import scrapy


class ZapSpider(scrapy.Spider):
    name = 'zap'
    start_urls = [
        'https://www.zapimoveis.com.br/aluguel/apartamentos/sp+sao-paulo/#{"precomaximo":"2500","parametrosautosuggest":[{"Bairro":"","Zona":"","Cidade":"SAO PAULO","Agrupamento":"","Estado":"SP"}],"pagina":"1","paginaOrigem":"Home","formato":"Lista"}']

    def parse(self, response):
        for apartment in response.xpath('..//div[@class="card-view"]/article'):
            loader = ApartmentLoader(selector=apartment)
            loader.add_value('address', self.get_address(apartment))
            loader.add_value('characteristics', self.get_characteristics(apartment))
            loader.add_value('prices', self.get_prices(apartment))
            loader.add_css('description', '.endereco p::text')
            loader.add_css('code', '::attr(data-id)')
            yield loader.load_item()

        # current_page, max_page = re.findall('\d+', response.css('#proximaPagina::attr(onclick)').extract_first())
        # if current_page and int(current_page) < int(max_page):
        #     next_page = '{url}#{{"pagina":"{page}"}}'.format(url=self.start_url, page=str(int(current_page) + 1))
        #     yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)

    @classmethod
    def get_address(cls, response):
        address_loader = ZapAddressLoader(selector=response)
        address_loader.add_xpath('street', './/h2/span[@itemprop="streetAddress"]/text()')
        address_loader.add_css('district', 'h2 strong::text')
        address_loader.add_xpath('city', './/h2/span[@itemprop="addressLocality"]/text()')
        return address_loader.load_item()

    @classmethod
    def get_characteristics(cls, response):
        details_loader = DetailsLoader(item=ZapDetails(), selector=response)
        details_loader.add_css('size', '.icone-area::text')
        details_loader.add_css('rooms', '.icone-quartos::text')
        details_loader.add_css('suite', '.icone-suites::text')
        details_loader.add_css('garages', '.icone-vagas::text')
        return details_loader.load_item()

    @classmethod
    def get_prices(cls, response):
        prices_loader = PricesLoader(item=ZapPrices(), selector=response)
        prices_loader.add_css('rent', '.preco strong::text')
        prices_loader.add_xpath('condo', './/div[@class="preco"][contains(span, "Condomínio")]/span/text()')
        prices_loader.add_xpath('total', './/div[@class="preco"][contains(span, "Valor Total")]/span/text()')
        return prices_loader.load_item()
