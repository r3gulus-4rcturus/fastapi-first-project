"""create posts table

Revision ID: 9e4cb294d9e6
Revises: 
Create Date: 2025-06-12 14:43:29.528700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e4cb294d9e6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
