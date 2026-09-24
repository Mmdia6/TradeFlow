# Architecture

TradeFlow is a modular monolith for the MVP.

React/TypeScript frontend
→ FastAPI REST API
→ application services
→ SQLAlchemy
→ MySQL

Redis is used selectively for market-data caching and rate limiting.

## Principles

1. Business rules live in services, not HTTP handlers.
2. Financial operations have explicit database transaction boundaries.
3. Accounts are the source of truth for spendable balances.
4. Trades are the source of truth for executions.
5. Transactions provide an auditable financial ledger.
6. Portfolio snapshots are historical read models.
7. External market data is accessed through a provider boundary.
8. Distributed systems are intentionally out of scope for the MVP.

## Order flow

Request → authentication → validation → order service → account row lock → balance check/reservation → order creation → execution when applicable → ledger entries → commit.
