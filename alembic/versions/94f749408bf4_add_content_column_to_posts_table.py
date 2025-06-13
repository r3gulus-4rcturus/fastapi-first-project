"""add content column to posts table

Revision ID: 94f749408bf4
Revises: 9e4cb294d9e6
Create Date: 2025-06-12 14:55:01.622490

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94f749408bf4'
down_revision: Union[str, None] = '9e4cb294d9e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.""" 
    # disini cukup add_column, tidak perlu create_table karena kita sudah membuat tabel posts pada migration sebelumnya
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False, server_default=''))
    # server_default='' agar kolom content tidak null, karena kita sudah menambahkan constraint nullable=False
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    # disini cukup drop_column, tidak perlu drop_table karena kita tidak menghapus tabel posts
    pass
