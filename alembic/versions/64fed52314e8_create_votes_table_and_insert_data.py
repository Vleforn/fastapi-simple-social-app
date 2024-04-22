"""create votes table and insert data

Revision ID: 64fed52314e8
Revises: 6aea46a7a3b4
Create Date: 2024-03-26 15:35:42.786167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64fed52314e8'
down_revision: Union[str, None] = '6aea46a7a3b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    votes_table = op.create_table(
        'votes',
        sa.Column('post_id', sa.Integer, sa.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    )

    op.bulk_insert(
        votes_table,
        votes_data
    )

def downgrade() -> None:
    pass


votes_data = [
    {"post_id": 1, "user_id": 1},
    {"post_id": 2, "user_id": 1},
    {"post_id": 2, "user_id": 6},
    {"post_id": 3, "user_id": 2},
    {"post_id": 3, "user_id": 3},
    {"post_id": 3, "user_id": 4},
    {"post_id": 4, "user_id": 2},
    {"post_id": 5, "user_id": 2},
    {"post_id": 5, "user_id": 6},
]
