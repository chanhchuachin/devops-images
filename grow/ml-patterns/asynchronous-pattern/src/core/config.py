from pydantic import BaseSettings


class Settings(BaseSettings):
    TITLE: str = "AI SERVICES"
    DESCRIPTION: str = "Run multiple models in one service !"


settings = Settings()

from pydantic import BaseSettings


class Settings(BaseSettings):
    TITLE: str = "AI SERVICES"
    DESCRIPTION: str = "Run multiple models in one service !"

    ROOT_PATH = "/api"
    DOCS_URL: str = "/api/docs"

    GOOGLE_SA_FILE: str = "drive-service.json"
    DRIVE_STORAGE_PATH: str = "TMT-MODEL/"
    ORIGINS = ["*"]
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"
    # OPENAPI_URL: str = "/accounts/auth/docs_token"


settings = Settings()
