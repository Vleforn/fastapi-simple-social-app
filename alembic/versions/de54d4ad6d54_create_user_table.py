"""create user table

Revision ID: de54d4ad6d54
Revises: 
Create Date: 2024-03-25 16:47:25.680857

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de54d4ad6d54'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    users_table = op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    
    op.bulk_insert(
        users_table,
        users_data
    )

def downgrade() -> None:
    op.drop_table('users')


users_data = [
    {"email": "ryu@hotmail.com", "password": "$2b$12$YZSWeYy152TiC7E5plWOGOSiMr22tAdcqU1hIQPv3fRl43wivnlqy"},
    {"email": "chunli@gmail.com", "password": "$2b$12$mVt.2Zwft4Q1J27Wp6DX5eMn5OYHcYak/zVdH3/QX41INx37P9QPm"},
    {"email": "jake@gmail.com", "password": "$2b$12$K/h/f0bWvxwTfB6ThkaSy.b8dw91AFdVki07lrZs3NNI9s/hD0.ru"},
    {"email": "betty@gmail.com", "password": "$2b$12$3Cqa1TGk7W6yu8Iqh9LKaertta3/e3JzKE9L4XCpi/S1CU9Z8nfxO"},
    {"email": "cammy@gmail.com", "password": "cammy123"},
    {"email": "guile@gmail.com", "password": "guile123"},
    {"email": "finn@gmail.com", "password": "finn123"},
]

