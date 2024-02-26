"""add content column to posts table

Revision ID: 9fcb22a14043
Revises: 9a24dc789d11
Create Date: 2024-02-23 12:51:35.459918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fcb22a14043'
down_revision: Union[str, None] = '9a24dc789d11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String(),nullable=False))
    pass

def downgrade() -> None:
    op.drop_column('posts','content')
    pass
