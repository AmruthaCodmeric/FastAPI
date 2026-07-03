"""Create phone number for user column

Revision ID: d800220bc992
Revises: 
Create Date: 2026-06-23 16:00:52.045152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd800220bc992'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    """pass"""


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
    pass
