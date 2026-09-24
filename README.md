# TradeFlow

TradeFlow is a full-stack paper-trading and portfolio management platform built as a portfolio-grade engineering project.

> **Scope:** TradeFlow does not execute real-money trades or custody user funds.

## Current status

**Active development — foundation and database layer implemented.**

The repository currently contains:

- FastAPI backend foundation
- MySQL + SQLAlchemy + Alembic database layer
- Redis service in local Docker Compose
- JWT/password-security primitives
- Initial database models and migration
- React + TypeScript + Vite frontend foundation
- Pytest coverage for health and password hashing
- GitHub Actions CI for backend and frontend builds
- Architecture and API documentation

Trading execution, market-data providers, portfolio accounting, refresh-token rotation, rate limiting, and the production dashboard are being implemented in subsequent phases.

## Architecture

React/TypeScript frontend → FastAPI API → service layer → SQLAlchemy → MySQL

Redis is reserved for cache/rate-limiting concerns. Financial state is persisted in MySQL using fixed-point DECIMAL values and transactional updates.

See:

- docs/architecture.md
- docs/database.md
- docs/order-state-machine.md
- docs/api.md
- docs/development.md

## Stack

**Backend:** Python, FastAPI, SQLAlchemy, Alembic, MySQL, Redis, Pytest  
**Frontend:** React, TypeScript, Vite, CSS  
**Infrastructure:** Docker Compose, GitHub Actions

## Local development

Copy .env.example to .env and replace development secrets before using authenticated features.

Start infrastructure:

docker compose up --build

API: http://localhost:8000

OpenAPI: http://localhost:8000/docs

Backend tests:

cd backend
pip install -r requirements.txt
pytest

Frontend:

cd frontend
npm install
npm run dev

## Engineering principles

- Business rules stay outside HTTP handlers.
- Money, prices, and quantities use fixed-point decimals.
- Financial mutations use explicit database transaction boundaries.
- Account balances are treated as the source of truth for spendable funds.
- Trades are the source of truth for executions.
- Transactions form an auditable ledger.
- Secrets are never committed.
- Tests are required before a feature is considered complete.
