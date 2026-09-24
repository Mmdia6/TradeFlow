# Database

Core tables:

- users
- refresh_tokens
- assets
- markets
- accounts
- orders
- trades
- transactions
- portfolio_snapshots
- idempotency_keys

Financial values use DECIMAL(36,18). Account uniqueness is enforced by (user_id, asset_id).

Migration 0001 creates the core schema. Migration 0002 adds idempotency storage and seeds USDT, BTC, ETH, SOL plus BTC/USDT, ETH/USDT and SOL/USDT.
