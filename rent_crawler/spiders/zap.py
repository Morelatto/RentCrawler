from rent_crawler.items import ApartmentLoader, DetailsLoader, PricesLoader, AddressLoader

import json
import scrapy


class ZapSpider(scrapy.Spider):
    name = 'zap'
    start_url = 'https://www.zapimoveis.com.br/Busca/RetornarBuscaAssincrona/'

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'X-Requested-With': 'XMLHttpRequest'
        },
    }

    form_data = {
        'tipoOferta': '1',
        'ordenacaoSelecionada': '',
        'pathName': '/aluguel/apartamentos/sp+sao-paulo/',
        'hashFragment': '{{"precomaximo":"2147483647",'
                        '"parametrosautosuggest":[{{"Bairro":"","Zona":"","Cidade":"SAO+PAULO","Agrupamento":"","Estado":"SP"}}],'
                        '"pagina":"{page}",'
                        '"ordem":"Relevancia",'
                        '"paginaOrigem":"ResultadoBusca",'
                        '"semente":"108848774",'
                        '"formato":"Lista"}}',
        'formato': 'Lista'
    }

    def format_form_data(self, page):
        post_data = self.form_data.copy()
        post_data['paginaAtual'] = str(page)
        post_data['hashFragment'] = post_data['hashFragment'].format(page=page)
        return post_data

    def start_requests(self):
        post_data = self.format_form_data(1)
        yield scrapy.FormRequest(url=self.start_url, formdata=post_data)

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        for page in range(1, int(json_response['Resultado']['QuantidadePaginas'])):
            post_data = self.format_form_data(page)
            yield scrapy.FormRequest(url=self.start_url, formdata=post_data, callback=self.parse_json_response,
                                     dont_filter=True)

    def parse_json_response(self, response):
        json_response = json.loads(response.body_as_unicode())
        for apartment in json_response['Resultado']['Resultado']:
            loader = ApartmentLoader()
            loader.add_value('code', apartment['ZapID'])
            loader.add_value('address', self.get_address(apartment))
            loader.add_value('details', self.get_details(apartment))
            loader.add_value('prices', self.get_prices(apartment))
            loader.add_value('description', apartment['Observacao'])
            loader.add_value('characteristics', apartment['Caracteristicas'])
            loader.add_value('img_urls', [picture['UrlImagemTamanhoG'] for picture in apartment['Fotos']])
            loader.add_value('source', 'Z')
            yield loader.load_item()

    @classmethod
    def get_address(cls, json_apartment):
        address_loader = AddressLoader()
        address_loader.add_value('street', json_apartment['Endereco'])
        address_loader.add_value('street', json_apartment['Numero'])
        address_loader.add_value('district', json_apartment['BairroOficial'])
        address_loader.add_value('city', json_apartment['CidadeOficial'])
        return address_loader.load_item()

    @classmethod
    def get_details(cls, json_apartment):
        details_loader = DetailsLoader()
        details_loader.add_value('size', json_apartment['Area'])
        details_loader.add_value('rooms', json_apartment['QuantidadeQuartos'])
        details_loader.add_value('suite', json_apartment['QuantidadeSuites'])
        details_loader.add_value('garages', json_apartment['QuantidadeVagas'])
        return details_loader.load_item()

    @classmethod
    def get_prices(cls, json_apartment):
        prices_loader = PricesLoader()
        prices_loader.add_value('rent', json_apartment['Valor'])
        prices_loader.add_value('condo', json_apartment['PrecoCondominio'])
        prices_loader.add_value('iptu', json_apartment['ValorIPTU'])
        return prices_loader.load_item()
