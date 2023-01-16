from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router.includes import app as router
from app.settings.config import Settings

config = Settings()

app = FastAPI(
    description=config.API_DESCRIPTION,
    title=config.API_TITLE,
    version=config.API_VERSION,
    docs_url=config.API_DOC_URL,
    openapi_url=config.API_OPENAPI_URL,
    redoc_url=config.API_REDOC_URL,
    debug=config.DEBUG,
)

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
