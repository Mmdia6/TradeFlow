from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_order_requires_authentication():
    r=client.post("/api/v1/orders",headers={"Idempotency-Key":"unauth"},json={"market":"BTC/USDT","side":"BUY","type":"MARKET","quantity":"0.001"}); assert r.status_code==401
