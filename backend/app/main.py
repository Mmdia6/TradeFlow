from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings
app=FastAPI(title=settings.app_name,version="1.0.0",description="Portfolio-grade paper trading API.")
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(api_router,prefix="/api/v1")
@app.get("/health")
def health(): return {"status":"ok","service":"tradeflow-api"}
