"""add foreign key to posts table

Revision ID: 48388ef8201f
Revises: 3d8967277ea3
Create Date: 2025-06-12 15:13:23.845031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48388ef8201f'
down_revision: Union[str, None] = '3d8967277ea3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    # set foreign key constraint untuk owner_id
    op.create_foreign_key('posts_owner_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_owner_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
