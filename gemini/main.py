from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routers import router as api_router

app = FastAPI(
    title="Data Science & AI Service API",
    description="API REST para disponibilização de modelos preditivos e analíticos.",
    version="1.0.0"
)

# Endpoint público para verificação de disponibilidade (Health Check)
@app.get("/health", tags=["Infraestrutura"], summary="Check de Saúde da API")
def health_check():
    return {"status": "healthy", "service": "DS & AI Services API"}

# Inclui os endpoints protegidos
app.include_router(api_router, tags=["Serviços Analíticos"])

# Tratador customizado para erros de validação (HTTP 422/400)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    erros = []
    for err in exc.errors():
        campo = " -> ".join(str(loc) for loc in err["loc"] if loc != "body")
        erros.append({"campo": campo, "mensagem": err["msg"]})
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "erro": "Dados de requisição inválidos",
            "detalhes": erros
        }
    )