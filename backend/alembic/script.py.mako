"""Migration template."""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "REVISION_ID"
down_revision: Union[str, Sequence[str], None] = "DOWN_REVISION"
branch_labels = None
depends_on = None

def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
