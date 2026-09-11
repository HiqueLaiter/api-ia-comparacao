import re
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

# --- Schemas do Serviço 1: Predição de Venda ---
class PredicaoVendaRequest(BaseModel):
    mes: int = Field(..., ge=1, le=12, description="Mês da predição (1-12)", example=10)
    ano: int = Field(..., ge=2000, le=2100, description="Ano da predição (2000-2100)", example=2026)

class PredicaoVendaResponse(BaseModel):
    mes: int
    ano: int
    previsao_vendas: float
    unidade: str = "BRL"


# --- Schemas do Serviço 2: Classificação de Cliente ---
class ClassificacaoClienteRequest(BaseModel):
    cpf: str = Field(..., description="CPF do cliente (com ou sem pontuação)", example="123.456.789-00")

    @field_validator("cpf")
    @classmethod
    def validar_formato_cpf(cls, v: str) -> str:
        digits_only = re.sub(r"\D", "", v)
        if len(digits_only) != 11:
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos.")
        if digits_only == digits_only[0] * 11:
            raise ValueError("CPF inválido (sequência de números repetidos).")
        return digits_only


class ClassificacaoClienteResponse(BaseModel):
    cpf: str
    classificacao_credito: str
    descricao: str


# --- Schemas do Serviço 3: Predição de Demanda ---
class PredicaoDemandaRequest(BaseModel):
    produto_id: str = Field(..., min_length=1, max_length=50, description="ID único do produto", example="PROD-102")
    periodo: str = Field(..., description="Período no formato AAAA-MM", example="2026-11")

    @field_validator("periodo")
    @classmethod
    def validar_formato_periodo(cls, v: str) -> str:
        if not re.match(r"^\d{4}-(0[1-9]|1[0-2])$", v):
            raise ValueError("O período deve estar no formato AAAA-MM (ex: 2026-05).")
        return v


class PredicaoDemandaResponse(BaseModel):
    produto_id: str
    periodo: str
    quantidade_prevista: int
    unidade: str = "unidades"


# --- Schemas do Serviço 4: Classificação de Sentimento ---
class ClassificacaoSentimentoRequest(BaseModel):
    texto: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Texto do cliente para análise de sentimento",
        example="O serviço prestado foi excelente e o atendimento muito rápido!"
    )

    @field_validator("texto")
    @classmethod
    def validar_texto_nao_vazio(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("O texto não pode ser vazio ou conter apenas espaços.")
        return stripped


class ClassificacaoSentimentoResponse(BaseModel):
    texto_analisado: str
    sentimento: str
    pontuacao_confianca: float