# TradeFlow

TradeFlow is a full-stack paper-trading and portfolio management platform built as a portfolio-grade engineering project.

> Scope: paper trading only. No real-money execution or custody.

## Status

**MVP implemented.**

The repository contains the backend trading/accounting flow, seeded markets, JWT authentication with rotating refresh tokens, Redis caching/rate limiting, a React dashboard, Docker Compose, Alembic migrations, tests and CI.

## Features

- FastAPI + SQLAlchemy + MySQL
- JWT access tokens and hashed rotating refresh tokens
- 10,000 USDT paper balance on registration
- BTC/USDT, ETH/USDT and SOL/USDT seeded markets
- Market orders and crossing/non-crossing limit orders
- Balance reservation and release
- Row locking for financial account mutations
- Idempotent order creation
- Trade records and transaction ledger
- Portfolio valuation and basic PnL
- Redis price caching and authentication rate limiting
- React + TypeScript dashboard
- Docker Compose and Alembic
- Pytest and GitHub Actions CI

## Paper execution model

TradeFlow deliberately does not implement a full exchange matching engine. It uses deterministic paper prices for supported markets.

- Market orders fill immediately.
- A limit BUY fills when its price is at or above the current paper price.
- A limit SELL fills when its price is at or below the current paper price.
- Otherwise the limit order remains OPEN until cancelled.

A future market-data worker/provider can replace the deterministic provider without changing the accounting boundaries.

## Architecture

React/TypeScript -> FastAPI -> application services -> SQLAlchemy -> MySQL
                                                   -> Redis

MySQL is authoritative for financial state. Redis is only a cache/rate-limit dependency.

## Local setup

1. Copy .env.example to .env.
2. Set a strong SECRET_KEY.
3. Start the backend infrastructure:

    docker compose up --build

4. API: http://localhost:8000
5. OpenAPI: http://localhost:8000/docs
6. Start the frontend:

    cd frontend
    npm install
    npm run dev

Optional:

    VITE_API_URL=http://localhost:8000/api/v1

## Tests

Backend:

    cd backend
    pip install -r requirements.txt
    pytest -q

Frontend:

    cd frontend
    npm install
    npm run build

## Engineering decisions

- Money, price and quantity use fixed-point DECIMAL values.
- Account rows are locked during financial mutations.
- Every order POST requires Idempotency-Key.
- Refresh tokens are stored only as SHA-256 hashes.
- Passwords use Argon2id through pwdlib.
- Business rules live in application services.
- Redis failures do not make financial writes authoritative.
- This project is paper trading and must not be presented as a real-money exchange.

See docs/ for architecture, database, API and development notes.
