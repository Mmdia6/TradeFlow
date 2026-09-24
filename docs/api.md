# API Contract

Base path: /api/v1

## Auth
- POST /auth/register
- POST /auth/login
- POST /auth/refresh
- POST /auth/logout

## Markets
- GET /markets
- GET /markets/{symbol}

## Account and portfolio
- GET /account
- GET /portfolio

## Orders
- GET /orders
- GET /orders/{id}
- POST /orders
- DELETE /orders/{id}

POST /orders requires an Idempotency-Key header.

## Trades
- GET /trades

## Order example

    {
      "market": "BTC/USDT",
      "side": "BUY",
      "type": "MARKET",
      "quantity": "0.001"
    }

The MVP uses FastAPI's standard HTTP error detail and stable HTTP status codes.
