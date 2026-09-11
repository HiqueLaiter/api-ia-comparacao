import os
import secrets

from fastapi import Header, HTTPException, status


def verificar_token(authorization: str | None = Header(default=None)) -> None:
    """
    Verifica o Bearer Token enviado pelo cliente.

    O token esperado deve estar na variável de ambiente API_TOKEN.
    """

    token_configurado = os.getenv("API_TOKEN")

    if not token_configurado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token da API não configurado no servidor."
        )

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    partes = authorization.split(" ", 1)

    if len(partes) != 2 or partes[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de autenticação inválido. Utilize Bearer Token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_recebido = partes[1].strip()

    if not token_recebido or not secrets.compare_digest(
        token_recebido,
        token_configurado
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido.",
            headers={"WWW-Authenticate": "Bearer"},
        )