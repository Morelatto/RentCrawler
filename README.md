# RentCrawler

Crawlers para sites de aluguel com persistência de dados em banco não relacional e deduplicação de itens usando banco em memória. 

O projeto visa agregar as informações disponíveis em sites de aluguel em um único local para facilitar a busca de um novo apartamento e ter mais parâmetros de busca além dos que os sites disponibilizam.

## Sites de aluguel

- [VivaReal](https://vivareal.com.br/)
- [ZAP Imóveis](https://www.zapimoveis.com.br/)
- [QuintoAndar](https://www.quintoandar.com.br/)

## Requisitos

- Python 3.8+
- Poetry
- MongoDB
- Redis

## Parâmetros

- **Start Page**
  - Número da página que a extração do crawler deve partir
- **Total Pages**
  - Quantidade máxima de páginas processadas pelo `start_requests` do crawler 

Os crawlers usam as urls internas de cada site para extrair os dados ao invés de acessar a página de busca. Atualmente as urls estão apontando para a cidade de **São Paulo**, para atualizar o local é preciso descobrir essa url interna ou o payload de dados enviado na requisição de cada site para a cidade desejada e atualizar a variável _start_url_ ou o payload com esse valor. 

Mais informações em:
- https://docs.scrapy.org/en/latest/topics/developer-tools.html#the-network-tool
- https://docs.scrapy.org/en/latest/topics/dynamic-content.html

## Docker

Para subir uma instância local MongoDB e um Redis e salvar o resultado do crawler, execute na pasta do projeto:

```sh
cat `
MONGO_INITDB_DATABASE: rent
MONGO_INITDB_ROOT_USERNAME: root
MONGO_INITDB_ROOT_PASSWORD: pass

ME_CONFIG_MONGODB_SERVER: mongodb
ME_CONFIG_MONGODB_ADMINUSERNAME: root
ME_CONFIG_MONGODB_ADMINPASSWORD: pass

REDIS_PASSWORD: root
` > .env

docker-compose up -d
```

Após essa configuração os seguintes endpoints estarão disponíveis:

- MongoDB: `mongodb://root:pass@localhost:27017`
- Redis:  `redis://root:root@localhost:9001/0`
- Mongo Express: `http://localhost:8082`

## Rodar

```
poetry run scrapy crawl <spider_name> -a <spider_parameter>=<spider_parameter_value>
```

### Dependências

```
poetry install --with=dev
```

### Salvar em JSON

```
poetry run scrapy crawl <spider_name> -o output.json
```

# License

Distributed under the GNU License. See LICENSE for more information.
