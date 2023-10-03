# RentCrawler

Crawlers para sites de aluguel com persistência em banco de dados não relacional e deduplicação de itens usando banco em memória. 

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

## Execução

Os crawlers usam o Redis para fazer o controle da extração, então é necessário configurar o acesso ao banco antes de executar.
As informações necessárias para realizar a requisição para cada site estão mapeadas em JSON na pasta `data`.
Esse mapeamento é utilizado na extração dos dados de cada site e pode ser atualizado conforme a necessidade, de acordo com o seguinte formato:

```json
{
  "data": {
    "method": "",
    "url": "",
    "headers": {
    },
    "body": ""
  },
  "params": {
    "page_start": 1,
    "total_pages": 10,
    "page_size": 10
  }
}
```

Os valores no campo `data` serão repassados para um [`scrapy.Request`](https://docs.scrapy.org/en/latest/topics/request-response.html#request-objects), então é possível adicionar qualquer parâmetro que a classe aceita via esse arquivo JSON.
O campo `params` define os seguintes parâmetros de paginação:

- **`page_start`**
  - Número da página que a extração do crawler deve partir.
- **`total_pages`**
  - Quantidade máxima de páginas processadas pelo crawler.
- **`page_size`**
  - Número de propriedades que será retornado na requisição. 

Os crawlers usam as urls internas de cada site para extrair os dados ao invés de acessar a página de busca. 
Atualmente as urls estão apontando para a cidade de **São Paulo**, para atualizar o local é preciso descobrir essa url interna ou o payload de dados enviado na requisição de cada site para a cidade desejada e atualizar o arquivo com os dados de requisição na pasta `data` com os valores desejados. 

Mais informações em:
- https://docs.scrapy.org/en/latest/topics/developer-tools.html#the-network-tool
- https://docs.scrapy.org/en/latest/topics/dynamic-content.html

## Docker

Para subir uma instância local do Redis/MongoDB e salvar o resultado do crawler, configure os parâmetros necessários via arquivo `.env`:

```sh
MONGO_INITDB_DATABASE: rent
MONGO_INITDB_ROOT_USERNAME: root
MONGO_INITDB_ROOT_PASSWORD: pass

ME_CONFIG_MONGODB_SERVER: mongodb
ME_CONFIG_MONGODB_ADMINUSERNAME: root
ME_CONFIG_MONGODB_ADMINPASSWORD: pass

REDIS_PASSWORD: root
```

Depois execute:

```sh
docker-compose up -d
```

Após essa configuração os seguintes endpoints estarão disponíveis:

- MongoDB: `mongodb://root:pass@localhost:27017`
- Redis:  `redis://root@localhost:9001/0`
- Mongo Express: `http://localhost:8082`

## Rodar

```
python run_spider vr
```

### Dependências

```
poetry install --with=dev
```

# License

Distributed under the GNU License. See LICENSE for more information.
