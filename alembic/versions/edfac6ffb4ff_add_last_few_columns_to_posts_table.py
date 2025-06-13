"""add last few columns to posts table

Revision ID: edfac6ffb4ff
Revises: 48388ef8201f
Create Date: 2025-06-12 15:18:33.246074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'edfac6ffb4ff'
down_revision: Union[str, None] = '48388ef8201f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    pass
