import hashlib

def calcular_predicao_venda(mes: int, ano: int) -> float:
    """
    Simulação determinística de vendas baseada no mês e ano.
    Fórmula base com variações sazonais determinísticas.
    """
    base = 50000.0
    fator_mes = (mes * 3210.50)
    fator_ano = (ano % 100) * 1500.00
    previsao = base + fator_mes + fator_ano
    return round(previsao, 2)


def calcular_classificacao_cliente(cpf_limpo: str) -> tuple[str, str]:
    """
    Simulação determinística de crédito utilizando hash MD5 do CPF.
    """
    hash_val = int(hashlib.md5(cpf_limpo.encode()).hexdigest(), 16)
    resto = hash_val % 3

    if resto == 0:
        return "baixo risco", "Cliente com excelente histórico financeiro e alta probabilidade de adimplência."
    elif resto == 1:
        return "médio risco", "Cliente com histórico financeiro moderado. Recomenda-se limite de crédito controlado."
    else:
        return "alto risco", "Cliente com inconsistências no perfil financeiro. Alta probabilidade de inadimplência."


def calcular_predicao_demanda(produto_id: str, periodo: str) -> int:
    """
    Simulação determinística de demanda por produto e período usando hash SHA256.
    """
    chave = f"{produto_id}_{periodo}"
    hash_val = int(hashlib.sha256(chave.encode()).hexdigest(), 16)
    demanda = (hash_val % 900) + 100  # Retorna valor entre 100 e 1000
    return demanda


def calcular_analise_sentimento(texto: str) -> tuple[str, float]:
    """
    Classificador léxico simples e determinístico baseado em palavras-chave.
    """
    texto_lower = texto.lower()

    palavras_positivas = ["excelente", "bom", "ótimo", "otimo", "maravilhoso", "rápido", "rapido", "gostei", "recomendo", "eficiente"]
    palavras_negativas = ["pessimo", "péssimo", "ruim", "horrivel", "horrível", "demorado", "decepcionado", "caro", "erro", "falha"]

    score_positivo = sum(1 for p in palavras_positivas if p in texto_lower)
    score_negativo = sum(1 for p in palavras_negativas if p in texto_lower)

    if score_positivo > score_negativo:
        confianca = min(0.60 + (score_positivo * 0.10), 0.99)
        return "positivo", round(confianca, 2)
    elif score_negativo > score_positivo:
        confianca = min(0.60 + (score_negativo * 0.10), 0.99)
        return "negativo", round(confianca, 2)
    else:
        return "neutro", 0.50