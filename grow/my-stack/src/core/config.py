from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TITLE: str = "My API"
    DESCRIPTION: str = ""
    # DOCS_URL: str = "/docs"
    # OPENAPI_URL: str = "/auth/docs_token"
    # SECRET_KEY: str
    # ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
