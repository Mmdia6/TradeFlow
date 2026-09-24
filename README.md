# TradeFlow

Crypto Trading & Portfolio Platform for realistic paper trading.

TradeFlow is a full-stack portfolio project focused on backend engineering, transactional consistency, authentication, market-data caching, portfolio accounting, testing, and production-oriented development practices.

## Status

🚧 Active development — MVP foundation.

## Planned Stack

- Backend: Python, FastAPI, SQLAlchemy, Alembic
- Database: MySQL
- Cache / rate limiting: Redis
- Frontend: React, TypeScript
- Testing: pytest
- Infrastructure: Docker Compose

## Core Scope

- JWT authentication with refresh-token rotation
- Spot paper trading
- Market and limit orders
- Balance reservation and release
- Trade execution records
- Transaction ledger
- Portfolio and PnL calculations
- Market-data caching
- API rate limiting
- Automated tests

TradeFlow does not execute real-money trades.

## Development

Architecture and API decisions are documented under docs/. The application is being built incrementally, with each phase remaining runnable and tested before the next phase.
