"""empty message

Revision ID: 5e44be3ecb83
Revises: 5bec84453794
Create Date: 2017-04-01 17:16:29.677000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5e44be3ecb83'
down_revision = '5bec84453794'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'highlightpost_ibfk_1', 'highlightpost', type_='foreignkey')
    op.drop_column('highlightpost', 'post_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('highlightpost', sa.Column('post_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key(u'highlightpost_ibfk_1', 'highlightpost', 'post', ['post_id'], ['id'])
    # ### end Alembic commands ###