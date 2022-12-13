"""empty message

Revision ID: 1520ed6c8a50
Revises: 7508b44c0fe2
Create Date: 2022-12-13 10:10:10.189762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1520ed6c8a50'
down_revision = '7508b44c0fe2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('provider', sa.Column('profile_views', sa.Integer(), nullable=False))
    op.drop_constraint('provider_services_ibfk_2', 'provider_services', type_='foreignkey')
    op.create_foreign_key(None, 'provider_services', 'provider', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'provider_services', type_='foreignkey')
    op.create_foreign_key('provider_services_ibfk_2', 'provider_services', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('provider', 'profile_views')
    # ### end Alembic commands ###
