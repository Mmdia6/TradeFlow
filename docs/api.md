# API Contract

Base path: /api/v1

## Auth

POST /auth/register
POST /auth/login
POST /auth/refresh
POST /auth/logout

## Markets

GET /markets
GET /markets/{symbol}

## Account and portfolio

GET /account
GET /portfolio

## Orders

GET /orders
POST /orders
GET /orders/{id}
DELETE /orders/{id}

Order creation requires an Idempotency-Key header.

## Trades

GET /trades

## Error format

{
  "error": {
    "code": "INSUFFICIENT_BALANCE",
    "message": "Insufficient USDT balance.",
    "details": {}
  }
}
