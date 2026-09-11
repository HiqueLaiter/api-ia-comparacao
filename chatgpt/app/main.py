from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.auth import verificar_token
from app.models import (
    ClassificacaoClienteRequest,
    ClassificacaoClienteResponse,
    ClassificacaoSentimentoRequest,
    ClassificacaoSentimentoResponse,
    PredicaoDemandaRequest,
    PredicaoDemandaResponse,
    PredicaoVendaRequest,
    PredicaoVendaResponse,
)
from app.services import (
    executar_classificacao_cliente,
    executar_classificacao_sentimento,
    executar_predicao_demanda,
    executar_predicao_venda,
)


app = FastAPI(
    title="API de Ciência de Dados e IA",
    description=(
        "API acadêmica para demonstração da disponibilização "
        "de modelos de Ciência de Dados e Inteligência Artificial "
        "como serviços REST."
    ),
    version="1.0.0",
)


# ============================================================
# TRATAMENTO DE ERROS DE VALIDAÇÃO
# ============================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "erro": "Erro de validação",
            "mensagem": "Os dados enviados são inválidos.",
            "detalhes": exc.errors()
        }
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get(
    "/health",
    tags=["Monitoramento"],
    summary="Verifica se a API está funcionando"
)
def health():
    return {
        "status": "ok",
        "mensagem": "API de Ciência de Dados e IA está funcionando."
    }


# ============================================================
# 1. PREDIÇÃO DE VENDA
# ============================================================

@app.post(
    "/predicaoVenda",
    response_model=PredicaoVendaResponse,
    tags=["Modelos de IA"],
    summary="Realiza previsão de vendas",
    dependencies=[Depends(verificar_token)]
)
def predicao_venda(
    dados: PredicaoVendaRequest
):
    return executar_predicao_venda(
        mes=dados.mes,
        ano=dados.ano
    )


# ============================================================
# 2. CLASSIFICAÇÃO DE CLIENTE
# ============================================================

@app.post(
    "/classificacaoCliente",
    response_model=ClassificacaoClienteResponse,
    tags=["Modelos de IA"],
    summary="Classifica o risco de crédito de um cliente",
    dependencies=[Depends(verificar_token)]
)
def classificacao_cliente(
    dados: ClassificacaoClienteRequest
):
    return executar_classificacao_cliente(
        cpf=dados.cpf
    )


# ============================================================
# 3. PREDIÇÃO DE DEMANDA
# ============================================================

@app.post(
    "/predicaoDemanda",
    response_model=PredicaoDemandaResponse,
    tags=["Modelos de IA"],
    summary="Realiza previsão de demanda",
    dependencies=[Depends(verificar_token)]
)
def predicao_demanda(
    dados: PredicaoDemandaRequest
):
    return executar_predicao_demanda(
        id_produto=dados.id_produto,
        periodo=dados.periodo
    )


# ============================================================
# 4. CLASSIFICAÇÃO DE SENTIMENTO
# ============================================================

@app.post(
    "/classificacaoSentimento",
    response_model=ClassificacaoSentimentoResponse,
    tags=["Modelos de IA"],
    summary="Classifica o sentimento de um texto",
    dependencies=[Depends(verificar_token)]
)
def classificacao_sentimento(
    dados: ClassificacaoSentimentoRequest
):
    return executar_classificacao_sentimento(
        texto=dados.texto
    )