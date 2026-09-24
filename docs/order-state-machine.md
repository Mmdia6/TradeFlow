# Order State Machine

PENDING -> OPEN
PENDING -> FILLED
PENDING -> REJECTED
OPEN -> FILLED
OPEN -> CANCELLED
PARTIALLY_FILLED -> FILLED
PARTIALLY_FILLED -> CANCELLED

Terminal states are FILLED, CANCELLED and REJECTED.

The MVP executes orders atomically, so PARTIALLY_FILLED is reserved for future incremental execution support.
