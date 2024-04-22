"""create posts table and fill with test data

Revision ID: 6aea46a7a3b4
Revises: de54d4ad6d54
Create Date: 2024-03-25 19:59:38.011709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6aea46a7a3b4'
down_revision: Union[str, None] = 'de54d4ad6d54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    posts_table = op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('published', sa.Boolean, server_default='True', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    )
    
    op.bulk_insert(
        posts_table,
        posts_data
    )

def downgrade() -> None:
    op.drop_table('posts')


posts_data = [
    {"title": "Best friend!", "content": "Jake is my best friend.", "user_id": 7},
    {"title": "Best friend!", "content": "Finn is my best friend.", "user_id": 3},
    {"title": "Sonic-Boom!", "content": "I'm the best zoner in street fighter!", "user_id": 6},
    {"title": "Chinese martial art", "content": "Wing Chun", "user_id": 2},
    {"title": "Spiral Arrow!", "content": "Cannon Spike!", "user_id": 5},
    {"title": "My name is -", "content": "Cammy", "user_id": 5},
]
