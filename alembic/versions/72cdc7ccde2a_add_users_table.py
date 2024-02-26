"""add users table

Revision ID: 72cdc7ccde2a
Revises: 9fcb22a14043
Create Date: 2024-02-23 16:12:10.634996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72cdc7ccde2a'
down_revision: Union[str, None] = '9fcb22a14043'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                     sa.Column('id', sa.Integer(),nullable=False),
                     sa.Column('email',sa.String(), nullable=False),
                     sa.Column('password', sa.String(), nullable=False),
                     sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
                     sa.PrimaryKeyConstraint('id'),
                     sa.UniqueConstraint('email'))      
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
