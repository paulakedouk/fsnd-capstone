"""empty message

Revision ID: 451a2ea193d0
Revises: 82399156088f
Create Date: 2020-04-14 20:54:46.308703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '451a2ea193d0'
down_revision = '82399156088f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'movie', ['title'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'movie', type_='unique')
    # ### end Alembic commands ###