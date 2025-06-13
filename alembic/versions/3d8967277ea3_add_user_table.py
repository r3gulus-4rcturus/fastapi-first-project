"""add user table

Revision ID: 3d8967277ea3
Revises: 94f749408bf4
Create Date: 2025-06-12 15:06:24.516143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d8967277ea3'
down_revision: Union[str, None] = '94f749408bf4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'), # primary key untuk id
        # unique constraint untuk email, jadi tidak boleh ada 2 user dengan email yang sama
        sa.UniqueConstraint('email')  # unique constraint untuk email
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
