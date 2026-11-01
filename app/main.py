from fastapi import FastAPI

from app.handlers.health.router import router as health_router

app = FastAPI(
    title="Fintrack API", description="API for Fintrack application", version="0.0.0"
)

app.include_router(health_router)
