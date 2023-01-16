from typing import List

from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    HOST: HttpUrl = "http://127.0.0.1:8000"
    PAYMENT_METHOD_TYPES: List[str] = ["sepa_debit", "card"]
    API_DOC_URL: str = "/docs"
    API_OPENAPI_URL: str = "/openapi.json"
    API_REDOC_URL: str = "/redoc"
    API_TITLE: str = "Stripe Template"
    API_VERSION: str = "0.0.1"
    API_DESCRIPTION: str = (
        "Template for integrating stripe into your FastAPI application"
    )
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
