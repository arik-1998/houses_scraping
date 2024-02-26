"""empty message

Revision ID: bb9c41a9b771
Revises: 
Create Date: 2024-02-26 07:05:53.949321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bb9c41a9b771'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Houses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('housing_type', postgresql.ENUM('house', 'apartment', name='housingtypes'), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('adress', sa.String(), nullable=True),
    sa.Column('price', sa.String(), nullable=True),
    sa.Column('short_info', sa.JSON(), nullable=True),
    sa.Column('land_info', sa.String(), nullable=True),
    sa.Column('created_statement', sa.String(), nullable=True),
    sa.Column('updated_statement', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Houses')
    # ### end Alembic commands ###
