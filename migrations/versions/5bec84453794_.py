"""empty message

Revision ID: 5bec84453794
Revises: 21828853d79a
Create Date: 2017-04-01 17:12:46.131000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bec84453794'
down_revision = '21828853d79a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('highlightpost', sa.Column('post_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'highlightpost', 'post', ['post_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'highlightpost', type_='foreignkey')
    op.drop_column('highlightpost', 'post_id')
    # ### end Alembic commands ###