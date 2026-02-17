"""baseline books

Revision ID: 5f4cf6a80af3
Revises: 564d730310df
Create Date: 2026-02-17 17:58:01.484139

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f4cf6a80af3'
down_revision: Union[str, Sequence[str], None] = '564d730310df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
