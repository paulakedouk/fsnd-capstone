"""empty message

Revision ID: 489b9709fc4c
Revises: 
Create Date: 2020-04-13 15:38:21.179727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '489b9709fc4c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'movie', ['title'])
    op.drop_constraint('movie_actor_id_fkey', 'movie', type_='foreignkey')
    op.drop_column('movie', 'actor_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movie', sa.Column('actor_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('movie_actor_id_fkey', 'movie', 'actor', ['actor_id'], ['id'])
    op.drop_constraint(None, 'movie', type_='unique')
    # ### end Alembic commands ###
