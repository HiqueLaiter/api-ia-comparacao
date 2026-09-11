import re
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


# ============================================================
# PREDIÇÃO DE VENDA
# ============================================================

class PredicaoVendaRequest(BaseModel):
    mes: int = Field(
        ...,
        description="Mês da previsão, entre 1 e 12.",
        examples=[8]
    )

    ano: int = Field(
        ...,
        description="Ano da previsão.",
        examples=[2026]
    )

    @field_validator("mes")
    @classmethod
    def validar_mes(cls, valor: int) -> int:
        if valor < 1 or valor > 12:
            raise ValueError("O mês deve estar entre 1 e 12.")
        return valor

    @field_validator("ano")
    @classmethod
    def validar_ano(cls, valor: int) -> int:
        if valor < 2000 or valor > 2100:
            raise ValueError("O ano deve estar entre 2000 e 2100.")
        return valor


class PredicaoVendaResponse(BaseModel):
    mes: int
    ano: int
    previsao_vendas: float
    unidade: str


# ============================================================
# CLASSIFICAÇÃO DE CLIENTE
# ============================================================

class ClassificacaoClienteRequest(BaseModel):
    cpf: str = Field(
        ...,
        description="CPF com ou sem pontuação.",
        examples=["123.456.789-09"]
    )

    @field_validator("cpf")
    @classmethod
    def validar_cpf(cls, valor: str) -> str:
        cpf = re.sub(r"\D", "", valor)

        if len(cpf) != 11:
            raise ValueError(
                "CPF inválido. Informe um CPF com 11 dígitos."
            )

        if not cpf.isdigit():
            raise ValueError("CPF deve conter apenas números.")

        if len(set(cpf)) == 1:
            raise ValueError("CPF inválido.")

        # Validação dos dígitos verificadores
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        if int(cpf[9]) != digito1 or int(cpf[10]) != digito2:
            raise ValueError("CPF inválido.")

        return cpf


class ClassificacaoClienteResponse(BaseModel):
    cpf: str
    classificacao_credito: str
    descricao: str


# ============================================================
# PREDIÇÃO DE DEMANDA
# ============================================================

class PredicaoDemandaRequest(BaseModel):
    id_produto: int = Field(
        ...,
        gt=0,
        description="ID numérico positivo do produto.",
        examples=[101]
    )

    periodo: str = Field(
        ...,
        description="Período no formato AAAA-MM.",
        examples=["2026-08"]
    )

    @field_validator("periodo")
    @classmethod
    def validar_periodo(cls, valor: str) -> str:
        if not re.fullmatch(r"\d{4}-\d{2}", valor):
            raise ValueError(
                "O período deve estar no formato AAAA-MM."
            )

        try:
            datetime.strptime(valor, "%Y-%m")
        except ValueError:
            raise ValueError(
                "O período informado não representa uma data válida."
            )

        return valor


class PredicaoDemandaResponse(BaseModel):
    id_produto: int
    periodo: str
    quantidade_prevista: int
    unidade: str


# ============================================================
# CLASSIFICAÇÃO DE SENTIMENTO
# ============================================================

class ClassificacaoSentimentoRequest(BaseModel):
    texto: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Texto do cliente, entre 1 e 1000 caracteres.",
        examples=["O atendimento foi excelente e muito rápido."]
    )

    @field_validator("texto")
    @classmethod
    def validar_texto(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("O texto não pode estar vazio.")

        return valor.strip()


class ClassificacaoSentimentoResponse(BaseModel):
    texto_analisado: str
    sentimento: str
    confianca: float