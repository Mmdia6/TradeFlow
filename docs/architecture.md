# Architecture

TradeFlow is a modular monolith for the MVP.

React/TypeScript
  -> FastAPI REST API
  -> application services
  -> SQLAlchemy
  -> MySQL
  -> Redis for cache and rate limiting

## Financial invariants

1. Available plus locked balance equals total balance for an asset.
2. Spendable funds are reduced before an order can execute.
3. Account rows are locked during order mutations.
4. Trades record executions.
5. Transactions record balance mutations.
6. Redis is never authoritative for financial state.
7. Decimal fixed-point values are used for money, price and quantity.

## Order flow

Authenticate -> validate -> idempotency check -> lock account -> validate balance -> reserve -> create order -> execute when applicable -> ledger/trade records -> commit.

The MVP uses deterministic paper prices rather than a full exchange matching engine.
