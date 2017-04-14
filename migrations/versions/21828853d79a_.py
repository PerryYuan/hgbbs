"""empty message

Revision ID: 21828853d79a
Revises: 9763ac9432b2
Create Date: 2017-04-01 17:09:29.430000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '21828853d79a'
down_revision = '9763ac9432b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('highlightpost', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('highlightpost', sa.Column('name', mysql.DATETIME(), nullable=True))
    # ### end Alembic commands ###