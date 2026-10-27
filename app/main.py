from fastapi import FastAPI

app = FastAPI(
    title="Fintrack API", description="API for Fintrack application", version="0.0.0"
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Fintrack API!"}
