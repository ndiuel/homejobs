"""empty message

Revision ID: d8e736a90bac
Revises: 1520ed6c8a50
Create Date: 2022-12-13 10:11:33.366611

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd8e736a90bac'
down_revision = '1520ed6c8a50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('provider', sa.Column('rating', sa.Integer(), nullable=True))
    op.drop_column('provider', 'profile_views')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('provider', sa.Column('profile_views', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_column('provider', 'rating')
    # ### end Alembic commands ###
