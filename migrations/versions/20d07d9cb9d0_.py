"""empty message

Revision ID: 20d07d9cb9d0
Revises: 53208193a630
Create Date: 2017-04-08 17:03:37.529000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20d07d9cb9d0'
down_revision = '53208193a630'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('front_user', sa.Column('avatar', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('front_user', 'avatar')
    # ### end Alembic commands ###
