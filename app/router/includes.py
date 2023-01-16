from fastapi import APIRouter

from app.router.v1 import health, payment

app = APIRouter()


app.include_router(payment.app, tags=["Payment"])
app.include_router(health.router, tags=["Health"])
