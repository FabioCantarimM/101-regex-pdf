# PDF Data Extractor

Este projeto processa arquivos PDF carregados no Amazon S3, extrai informações em formato de tabela ou texto e armazena os dados em um banco de dados PostgreSQL. A solução é automatizada, utilizando triggers do Amazon SQS para detectar novos arquivos e processá-los a cada 2 minutos.

## Funcionalidades

- **Extração de Tabelas**: Utiliza a biblioteca [camelot-py](https://camelot-py.readthedocs.io/en/master/) para extrair tabelas de arquivos PDF e salvar os dados em um banco de dados PostgreSQL.
- **Extração de Texto**: Utiliza a biblioteca [PyPDF2](https://pypdf2.readthedocs.io/) para transformar o conteúdo do PDF em texto simples, que também é salvo no PostgreSQL.
- **Integração com S3 e SQS**: O projeto é integrado com o Amazon S3 para o upload dos arquivos PDF e com o Amazon SQS para a detecção de novos arquivos, que dispara o processo de extração.

## Fluxo da Aplicação

1. O usuário faz upload de um arquivo PDF para um bucket do Amazon S3.
2. Uma trigger é ativada, enviando uma mensagem para o Amazon SQS.
3. A aplicação checa novas mensagens no SQS a cada 2 minutos.
4. Quando uma nova mensagem é encontrada:
   - A função de extração de tabelas com `camelot-py` é executada.
   - A função de extração de texto com `PyPDF2` também é executada.
5. Os dados extraídos são armazenados em um banco de dados PostgreSQL.

## Requisitos

- Python 3.x
- Bibliotecas:
  - `camelot-py`
  - `PyPDF2`
  - `boto3` (para interagir com S3 e SQS)
  - `psycopg2` (para conexão com PostgreSQL)
- PostgreSQL

## Configuração

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu_usuario/pdf-data-extractor.git
   cd pdf-data-extractor

2. **Instale as dependências**:
    ```bash
    poetry install

3. **Configuração do banco de dados: Configure as variáveis de ambiente para a conexão com o banco de dados PostgreSQL**:
    ```bash
    export DB_NAME=my_database
    export DB_USER=my_user
    export DB_PASSWORD=my_password
    export DB_HOST=my_host

4. **Configuração da AWS: Defina as variáveis de ambiente para o acesso ao S3 e SQS**:
    ```bash
    export AWS_ACCESS_KEY_ID=my_access_key_id
    export AWS_SECRET_ACCESS_KEY=my_secret_access_key
    export AWS_REGION=my_region
    export QUEUE_NAME=my_queue

##Execução
A aplicação pode ser executada manualmente para verificar novas mensagens no SQS e processar os arquivos:
```bash
    python3 __init__.py

##Conteúdo Adicional
Este projeto inclui um arquivo regex.md com conteúdo básico sobre expressões regulares (Regex), utilizado para processar textos semi-estruturados extraídos dos PDFs.