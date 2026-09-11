import re
from datetime import datetime

from app.models import (
    ClassificacaoClienteResponse,
    PredicaoDemandaResponse,
    PredicaoVendaResponse,
    ClassificacaoSentimentoResponse,
)


# ============================================================
# PREDIÇÃO DE VENDA
# ============================================================

def executar_predicao_venda(
    mes: int,
    ano: int
) -> PredicaoVendaResponse:

    # Fórmula determinística apenas para simulação acadêmica.
    previsao = (
        10000
        + (ano - 2020) * 500
        + mes * 350
    )

    return PredicaoVendaResponse(
        mes=mes,
        ano=ano,
        previsao_vendas=round(previsao, 2),
        unidade="R$"
    )


# ============================================================
# CLASSIFICAÇÃO DE CLIENTE
# ============================================================

def executar_classificacao_cliente(
    cpf: str
) -> ClassificacaoClienteResponse:

    # Utiliza o próprio CPF como entrada determinística.
    # Não consulta nenhum cadastro real.

    numero = int(cpf)

    resultado = numero % 3

    if resultado == 0:
        classificacao = "baixo risco"
        descricao = "Perfil simulado com baixo risco de crédito."
    elif resultado == 1:
        classificacao = "médio risco"
        descricao = "Perfil simulado com risco de crédito moderado."
    else:
        classificacao = "alto risco"
        descricao = "Perfil simulado com maior risco de crédito."

    return ClassificacaoClienteResponse(
        cpf=cpf,
        classificacao_credito=classificacao,
        descricao=descricao
    )


# ============================================================
# PREDIÇÃO DE DEMANDA
# ============================================================

def executar_predicao_demanda(
    id_produto: int,
    periodo: str
) -> PredicaoDemandaResponse:

    data = datetime.strptime(periodo, "%Y-%m")

    # Fórmula determinística para simular um modelo.
    quantidade = (
        500
        + (id_produto * 37) % 1000
        + data.month * 25
        + (data.year - 2020) * 10
    )

    return PredicaoDemandaResponse(
        id_produto=id_produto,
        periodo=periodo,
        quantidade_prevista=quantidade,
        unidade="unidades"
    )


# ============================================================
# CLASSIFICAÇÃO DE SENTIMENTO
# ============================================================

PALAVRAS_POSITIVAS = {
    "bom",
    "boa",
    "ótimo",
    "ótima",
    "excelente",
    "excelência",
    "gostei",
    "gosto",
    "satisfeito",
    "satisfeita",
    "rápido",
    "rápida",
    "maravilhoso",
    "maravilhosa",
    "perfeito",
    "perfeita",
    "agradável",
    "recomendo",
}

PALAVRAS_NEGATIVAS = {
    "ruim",
    "péssimo",
    "péssima",
    "horrível",
    "odiei",
    "insatisfeito",
    "insatisfeita",
    "lento",
    "lenta",
    "problema",
    "problemas",
    "erro",
    "erros",
    "decepcionado",
    "decepcionada",
    "terrível",
    "não",
}


def executar_classificacao_sentimento(
    texto: str
) -> ClassificacaoSentimentoResponse:

    palavras = re.findall(
        r"\b[\wÀ-ÿ]+\b",
        texto.lower()
    )

    positivas = sum(
        1 for palavra in palavras
        if palavra in PALAVRAS_POSITIVAS
    )

    negativas = sum(
        1 for palavra in palavras
        if palavra in PALAVRAS_NEGATIVAS
    )

    total = positivas + negativas

    if total == 0:
        sentimento = "neutro"
        confianca = 0.60

    elif positivas > negativas:
        sentimento = "positivo"

        diferenca = positivas - negativas
        confianca = min(
            0.60 + (diferenca * 0.10),
            0.95
        )

    elif negativas > positivas:
        sentimento = "negativo"

        diferenca = negativas - positivas
        confianca = min(
            0.60 + (diferenca * 0.10),
            0.95
        )

    else:
        sentimento = "neutro"
        confianca = 0.50

    return ClassificacaoSentimentoResponse(
        texto_analisado=texto,
        sentimento=sentimento,
        confianca=round(confianca, 2)
    )