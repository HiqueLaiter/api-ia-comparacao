# API de Ciência de Dados e IA

API REST desenvolvida em Python com FastAPI para simular a disponibilização
de modelos de Ciência de Dados e Inteligência Artificial como serviços web.

## Serviços

- predicaoVenda
- classificacaoCliente
- predicaoDemanda
- classificacaoSentimento

## Autenticação

Os serviços utilizam Bearer Token.

O token deve ser configurado através da variável de ambiente:

API_TOKEN

## Execução

Criar ambiente virtual:

python -m venv .venv

Ativar no Windows PowerShell:

.\.venv\Scripts\Activate.ps1

Instalar dependências:

pip install -r requirements.txt

Executar:

uvicorn app.main:app --reload

Swagger:

http://127.0.0.1:8000/docs