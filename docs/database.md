# Database Design

MySQL is the source of truth for account and trading state.

## Tables

- users
- assets
- markets
- accounts
- orders
- trades
- transactions
- refresh_tokens
- portfolio_snapshots

Money, price and quantity fields use fixed-point DECIMAL values.

Balance-changing operations run inside database transactions. Relevant account rows are locked before balance checks and updates so concurrent requests cannot overspend an account.

The transactions table records balance-changing events with before/after balances and optional order/trade references.
