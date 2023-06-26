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

    # OPENAPI_URL: str = "/accounts/auth/docs_token"


settings = Settings()
