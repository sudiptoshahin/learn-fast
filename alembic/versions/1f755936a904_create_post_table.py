"""create post table

Revision ID: 1f755936a904
Revises: 
Create Date: 2026-10-10 22:46:08.779685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f755936a904'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'posts',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('title', sa.String(200), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
