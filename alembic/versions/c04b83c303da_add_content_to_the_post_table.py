"""add content to the post table

Revision ID: c04b83c303da
Revises: 1f755936a904
Create Date: 2026-10-10 22:47:56.170529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c04b83c303da'
down_revision: Union[str, Sequence[str], None] = '1f755936a904'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts', 
        sa.Column('content', sa.String(255), nullable=False)
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
