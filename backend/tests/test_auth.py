from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.api.dependencies import db_session
from app.db.session import Base
from app.main import app
from app.models import Asset,Market
engine=create_engine("sqlite://",connect_args={"check_same_thread":False},poolclass=StaticPool); TestingSession=sessionmaker(bind=engine); Base.metadata.create_all(engine)
with TestingSession() as db:
    usdt,btc=Asset(symbol="USDT",name="Tether USD",decimals=6),Asset(symbol="BTC",name="Bitcoin",decimals=8); db.add_all([usdt,btc]); db.flush(); db.add(Market(symbol="BTC/USDT",base_asset_id=btc.id,quote_asset_id=usdt.id,min_quantity=0.000001,min_notional=10)); db.commit()
def override_db():
    db=TestingSession()
    try: yield db
    finally: db.close()
app.dependency_overrides[db_session]=override_db; client=TestClient(app)
def test_register_login_refresh_rotation_and_seed_balance():
    email="tester@example.com"; r=client.post("/api/v1/auth/register",json={"email":email,"password":"strong-pass-123"}); assert r.status_code==201
    access=r.json()["access_token"]; old=client.post("/api/v1/auth/login",json={"email":email,"password":"strong-pass-123"}).json()["refresh_token"]
    a=client.get("/api/v1/account",headers={"Authorization":"Bearer "+access}); assert a.status_code==200 and float(a.json()[0]["available_balance"])==10000
    rr=client.post("/api/v1/auth/refresh",json={"refresh_token":old}); assert rr.status_code==200
    assert client.post("/api/v1/auth/refresh",json={"refresh_token":old}).status_code==401
def test_market_order_and_idempotency():
    access=client.post("/api/v1/auth/login",json={"email":"tester@example.com","password":"strong-pass-123"}).json()["access_token"]
    payload={"market":"BTC/USDT","side":"BUY","type":"MARKET","quantity":"0.001"}; headers={"Authorization":"Bearer "+access,"Idempotency-Key":"order-test-1"}
    first=client.post("/api/v1/orders",json=payload,headers=headers); assert first.status_code==201 and first.json()["status"]=="FILLED"
    second=client.post("/api/v1/orders",json=payload,headers=headers); assert second.status_code==201 and second.json()["id"]==first.json()["id"]
