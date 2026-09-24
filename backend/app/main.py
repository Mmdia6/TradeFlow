from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings

app = FastAPI(title="TradeFlow API", version="0.1.0", description="Paper trading and portfolio management API.")
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}
