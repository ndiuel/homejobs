"""empty message

Revision ID: 1c3c35a214b0
Revises: d8e736a90bac
Create Date: 2022-12-13 10:11:45.871627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c3c35a214b0'
down_revision = 'd8e736a90bac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('provider', sa.Column('profile_views', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('provider', 'profile_views')
    # ### end Alembic commands ###
