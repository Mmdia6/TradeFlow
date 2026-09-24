# Order State Machine

## States

- PENDING
- OPEN
- PARTIALLY_FILLED
- FILLED
- CANCELLED
- REJECTED

## Allowed transitions

- PENDING → OPEN
- PENDING → FILLED
- PENDING → REJECTED
- OPEN → PARTIALLY_FILLED
- OPEN → FILLED
- OPEN → CANCELLED
- PARTIALLY_FILLED → FILLED
- PARTIALLY_FILLED → CANCELLED

Terminal states cannot transition back to active states.

Only OPEN and PARTIALLY_FILLED orders can be cancelled. Cancellation releases only the remaining reservation for a partially filled order.
