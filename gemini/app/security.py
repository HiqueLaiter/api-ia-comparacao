from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.config import settings

security_scheme = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security_scheme)) -> str:
    """
    Valida o token Bearer enviado no cabeçalho Authorization.
    Lança HTTP 401 caso o token seja inválido ou ausente.
    """
    token = credentials.credentials
    if token != settings.API_BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token