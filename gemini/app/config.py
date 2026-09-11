import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

class Settings:
    API_BEARER_TOKEN: str = os.getenv("API_BEARER_TOKEN", "token_padrao_dev_123")

settings = Settings()