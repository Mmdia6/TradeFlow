from fastapi import APIRouter
from app.api.routes.account import router as account_router
from app.api.routes.auth import router as auth_router
from app.api.routes.markets import router as markets_router
from app.api.routes.orders import router as orders_router
from app.api.routes.portfolio import router as portfolio_router
from app.api.routes.system import router as system_router
from app.api.routes.trades import router as trades_router
api_router=APIRouter()
api_router.include_router(system_router)
api_router.include_router(auth_router,prefix="/auth",tags=["auth"])
api_router.include_router(markets_router,prefix="/markets",tags=["markets"])
api_router.include_router(account_router,prefix="/account",tags=["account"])
api_router.include_router(portfolio_router,prefix="/portfolio",tags=["portfolio"])
api_router.include_router(orders_router,prefix="/orders",tags=["orders"])
api_router.include_router(trades_router,prefix="/trades",tags=["trades"])
