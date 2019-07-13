from scrapy.loader import ItemLoader
from rent_crawler.items import ApartmentLoader, DetailsLoader, PricesLoader, AddressLoader, TextDetails

import json
import scrapy

ZAP_SOURCE = 'Z'


class ZapSpider(scrapy.Spider):
    MAX_PAGE = None

    name = 'zap'
    start_url = 'https://www.zapimoveis.com.br/Busca/RetornarBuscaAssincrona/'

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'X-Requested-With': 'XMLHttpRequest'
        },
    }

    @staticmethod
    def format_form_data(page):
        page = str(page)
        form_data = {
            'tipoOferta': '1',
            'ordenacaoSelecionada': '',
            'pathName': '/aluguel/apartamentos/sp+sao-paulo/',
            'hashFragment':
                '{{"precomaximo":"2147483647",'
                '"parametrosautosuggest":[{{"Bairro":"","Zona":"","Cidade":"SAO+PAULO","Agrupamento":"","Estado":"SP"}}],'
                '"pagina":"{}",'
                '"ordem":"Relevancia",'
                '"paginaOrigem":"ResultadoBusca",'
                '"semente":"108848774",'
                '"formato":"Lista"}}'.format(page),
            'formato': 'Lista',
            'paginaAtual': page
        }
        return form_data

    def start_requests(self):
        page = 1
        while True:
            yield scrapy.FormRequest(url=self.start_url, formdata=self.format_form_data(page), dont_filter=True)
            page += 1
            if self.MAX_PAGE and page > self.MAX_PAGE:
                break

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        for apartment in json_response['Resultado']['Resultado']:
            loader = ApartmentLoader()
            loader.add_value('code', apartment['ZapID'])
            loader.add_value('address', self.get_address(apartment))
            loader.add_value('prices', self.get_prices(apartment))
            loader.add_value('details', self.get_details(apartment))
            loader.add_value('text_details', self.get_text_details(apartment))
            loader.add_value('img_urls', self.get_img_urls(apartment))
            loader.add_value('source', ZAP_SOURCE)
            yield loader.load_item()

        if not self.MAX_PAGE:
            self.MAX_PAGE = int(json_response['Resultado']['QuantidadePaginas'])

    @classmethod
    def get_address(cls, json_apartment):
        address_loader = AddressLoader()
        address_loader.add_value('street', json_apartment['Endereco'])
        address_loader.add_value('street', json_apartment['Numero'])
        address_loader.add_value('district', json_apartment['BairroOficial'])
        address_loader.add_value('city', json_apartment['CidadeOficial'])
        return address_loader.load_item()

    @classmethod
    def get_prices(cls, json_apartment):
        prices_loader = PricesLoader()
        prices_loader.add_value('rent', json_apartment['Valor'])
        prices_loader.add_value('condo', json_apartment['PrecoCondominio'])
        prices_loader.add_value('iptu', json_apartment['ValorIPTU'])
        return prices_loader.load_item()

    @classmethod
    def get_details(cls, json_apartment):
        details_loader = DetailsLoader()
        details_loader.add_value('size', json_apartment['Area'])
        details_loader.add_value('rooms', json_apartment['QuantidadeQuartos'])
        details_loader.add_value('suite', json_apartment['QuantidadeSuites'])
        details_loader.add_value('garages', json_apartment['QuantidadeVagas'])
        return details_loader.load_item()

    @classmethod
    def get_text_details(cls, json_apartment):
        text_details_loader = ItemLoader(item=TextDetails())
        text_details_loader.add_value('description', json_apartment['Observacao'])
        text_details_loader.add_value('characteristics', json_apartment['Caracteristicas'])
        return text_details_loader.load_item()

    @classmethod
    def get_img_urls(cls, json_apartment):
        return [picture['UrlImagemTamanhoG'] for picture in json_apartment['Fotos']]
