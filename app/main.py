from fastapi import FastAPI

from app.handlers.health.router import router as health_router
from app.handlers.transactions.router import router as transactions_router

app = FastAPI(
    title="Fintrack API", description="API for Fintrack application", version="0.0.0"
)

app.include_router(health_router)
app.include_router(transactions_router)
