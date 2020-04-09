"""Initial migration.

Revision ID: 577502d2f2de
Revises: 
Create Date: 2020-04-09 11:59:52.792716

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '577502d2f2de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movies')
    op.add_column('Movies', sa.Column('genre', sa.String(), nullable=True))
    op.add_column('Movies', sa.Column('length', sa.Float(), nullable=True))
    op.add_column('Movies', sa.Column('name', sa.String(), nullable=True))
    op.drop_column('Movies', 'title')
    op.drop_column('Movies', 'release')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Movies', sa.Column('release', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('Movies', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('Movies', 'name')
    op.drop_column('Movies', 'length')
    op.drop_column('Movies', 'genre')
    op.create_table('movies',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('release_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='movies_pkey')
    )
    # ### end Alembic commands ###
