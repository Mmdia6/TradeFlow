# Development

## Quality gates

Before a feature is considered complete:

- Python compilation succeeds.
- Pytest passes.
- Alembic reaches head.
- Docker Compose starts the API after migrations.
- Frontend production build succeeds.
- No secrets are committed.

## Manual verification

1. Register a new user and confirm 10,000 USDT.
2. Login and rotate a refresh token.
3. Read seeded markets.
4. Submit a market order with an idempotency key.
5. Repeat the same request and confirm the same order is returned.
6. Submit a non-crossing limit order and cancel it.
7. Inspect balances, trades, ledger and portfolio.
