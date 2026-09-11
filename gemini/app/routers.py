from fastapi import APIRouter, Depends
from app.security import verify_token
from app.schemas import (
    PredicaoVendaRequest, PredicaoVendaResponse,
    ClassificacaoClienteRequest, ClassificacaoClienteResponse,
    PredicaoDemandaRequest, PredicaoDemandaResponse,
    ClassificacaoSentimentoRequest, ClassificacaoSentimentoResponse
)
from app.services import (
    calcular_predicao_venda,
    calcular_classificacao_cliente,
    calcular_predicao_demanda,
    calcular_analise_sentimento
)

router = APIRouter(dependencies=[Depends(verify_token)])

@router.post("/predicaoVenda", response_model=PredicaoVendaResponse, summary="Predição de Vendas Mensais")
def predicao_venda(payload: PredicaoVendaRequest):
    previsao = calcular_predicao_venda(payload.mes, payload.ano)
    return PredicaoVendaResponse(
        mes=payload.mes,
        ano=payload.ano,
        previsao_vendas=previsao,
        unidade="BRL"
    )

@router.post("/classificacaoCliente", response_model=ClassificacaoClienteResponse, summary="Classificação de Risco de Crédito")
def classificacao_cliente(payload: ClassificacaoClienteRequest):
    classificacao, descricao = calcular_classificacao_cliente(payload.cpf)
    return ClassificacaoClienteResponse(
        cpf=payload.cpf,
        classificacao_credito=classificacao,
        descricao=descricao
    )

@router.post("/predicaoDemanda", response_model=PredicaoDemandaResponse, summary="Predição de Demanda de Produto")
def predicao_demanda(payload: PredicaoDemandaRequest):
    quantidade = calcular_predicao_demanda(payload.produto_id, payload.periodo)
    return PredicaoDemandaResponse(
        produto_id=payload.produto_id,
        periodo=payload.periodo,
        quantidade_prevista=quantidade,
        unidade="unidades"
    )

@router.post("/classificacaoSentimento", response_model=ClassificacaoSentimentoResponse, summary="Análise de Sentimento de Texto")
def classificacao_sentimento(payload: ClassificacaoSentimentoRequest):
    sentimento, confianca = calcular_analise_sentimento(payload.texto)
    return ClassificacaoSentimentoResponse(
        texto_analisado=payload.texto,
        sentimento=sentimento,
        pontuacao_confianca=confianca
    )