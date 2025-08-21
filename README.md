# 🚀 Kabum\! Web Scraper de Anúncios de Celulares

[](https://www.google.com/search?q=https://github.com/SEU_USUARIO/SEU_REPOSITORIO)
[](https://opensource.org/licenses/MIT)
[](https://www.python.org/downloads/)

Um projeto de web scraping robusto e containerizado, desenvolvido para extrair, tratar e armazenar dados de anúncios de celulares do e-commerce KaBuM\!. A solução completa utiliza Selenium e BeautifulSoup4 para a coleta de dados, salva os resultados brutos em um arquivo CSV, utiliza um Jupyter Notebook com Pandas e NumPy para o processo de ETL, e por fim, carrega os dados tratados em um banco de dados PostgreSQL. Todo o ambiente é orquestrado com Docker, garantindo simplicidade na configuração e execução.

## 📋 Índice

  - [Visão Geral do Projeto]
  - [✨ Funcionalidades]
  - [🛠️ Tecnologias Utilizadas]
  - [🔧 Pré-requisitos]
  - [⚙️ Instalação e Execução]
  - [📁 Estrutura do Projeto]
  - [🗃️ Schema do Banco de Dados]


## 📖 Visão Geral do Projeto

Este projeto automatiza a coleta de dados de celulares no site da KaBuM\!. O fluxo é dividido em duas etapas principais:

1.  **Extração (`Extract.py`):** Um script Python que navega por aproximadamente 500 páginas do site, coleta os dados brutos dos anúncios e os salva no arquivo `produtos.csv`.
2.  **Transformação e Carga (`Transform Code.ipynb`):** Um Jupyter Notebook que lê os dados brutos do CSV, realiza todo o processo de limpeza, transformação e enriquecimento dos dados (ETL), e por fim, carrega os dados limpos na tabela do banco de dados PostgreSQL.

## ✨ Funcionalidades

  - **Scraping Dinâmico:** Utiliza **Selenium** para navegar por múltiplas páginas, lidando com JavaScript e carregamento dinâmico.
  - **Extração HTML Eficiente:** Emprega **BeautifulSoup4 (bs4)** para fazer o parse do HTML e extrair os dados.
  - **ETL com Jupyter Notebook:** Realiza a limpeza e transformação dos dados de forma interativa e documentada usando **Pandas** e **NumPy**.
  - **Fluxo de Dados Persistido:** Salva os dados brutos (`produtos.csv`) e tratados (`WebScraping-Kabum-Tradados.csv`), permitindo reanálise sem a necessidade de um novo scraping.
  - **Armazenamento Robusto:** Salva os dados finais em um banco de dados **PostgreSQL**.
  - **Ambiente Containerizado:** Todo o projeto é executado em contêineres **Docker**, garantindo um ambiente consistente e isolado.

## 🛠️ Tecnologias Utilizadas

  - **Linguagem:** Python 3.9+
  - **Web Scraping:** `Selenium`, `BeautifulSoup4`
  - **ETL e Análise de Dados:** `Pandas`, `NumPy`, `Jupyter Notebook`
  - **Banco de Dados:** `PostgreSQL`, `Psycopg2-binary`
  - **Containerização:** `Docker`, `Docker Compose`

## 🔧 Pré-requisitos

Para executar este projeto localmente, você precisará ter as seguintes ferramentas instaladas:

  - [Docker](https://www.docker.com/get-started)
  - [Docker Compose](https://docs.docker.com/compose/install/)

## ⚙️ Instalação e Execução

O processo é dividido em três etapas: **configurar o ambiente**, **executar a extração** e **executar a transformação/carga**.

### 1\. Configuração do Ambiente

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/Marcelo2506/WebScraping-Kabum.git
    cd WebScraping-Kabum
    ```

2.  **Crie e configure o arquivo `.env`:**
    Copie o arquivo de exemplo e preencha com suas credenciais do banco de dados.

    ```bash
    cp .env.example .env
    ```

3.  **Construa e inicie os contêineres:**
    Este comando irá iniciar o serviço do banco de dados e o serviço da aplicação (`scraper`).

    ```bash
    docker-compose up --build -d
    ```

### 2\. Executar a Extração

Execute o script `Extract.py` dentro do contêiner para iniciar o web scraping. Ele irá gerar o arquivo `produtos.csv`.

```bash
docker-compose exec scraper python Extract.py
```

### 3\. Executar a Transformação e Carga

Execute o Jupyter Notebook para tratar os dados do `produtos.csv` e carregá-los no PostgreSQL.

```bash
docker-compose exec scraper jupyter nbconvert --to notebook --execute "Transform Code.ipynb"
```

Este comando executa todas as células do notebook do início ao fim. Ao final, os dados estarão no banco de dados e o arquivo `WebScraping-Kabum-Tradados.csv` será gerado.

### Finalizando

  - **Para verificar os dados no banco:** Conecte-se ao PostgreSQL (host `localhost`, porta `5432`) usando as credenciais do seu arquivo `.env`.
  - **Para parar todos os serviços:**
    ```bash
    docker-compose down
    ```

## 📁 Estrutura do Projeto

```
.
├── .dockerignore
├── .env
├── .gitattributes
├── .gitignore
├── Dockerfile
├── Extract.py
├── LICENSE
├── produtos.csv
├── README.md
├── requirements.txt
├── Transform Code.ipynb
└── WebScraping-Kabum-Tradados.csv
```

## 🗃️ Schema do Banco de Dados

Os dados tratados são armazenados em uma tabela chamada `celulares` (ou similar) no banco de dados `kabum_db`.

| Coluna | Tipo de Dado | Descrição |
| :--- | :--- | :--- |
| `id` | `SERIAL PRIMARY KEY`| Identificador único do registro. |
| `nome_produto` | `VARCHAR(255)` | Nome completo do celular anunciado. |
| `preco_atual` | `DECIMAL(10, 2)`| Preço principal do produto. |
| ... | ... | (demais colunas conforme definidas no notebook) |
| `data_coleta` | `TIMESTAMP` | Data e hora em que o dado foi coletado. |

