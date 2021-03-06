"""empty message

Revision ID: 5c6f6b4d3fad
Revises: 401dfc183ac6
Create Date: 2017-10-18 10:37:59.684474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c6f6b4d3fad'
down_revision = '401dfc183ac6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instituicoes', sa.Column('password', sa.String(), nullable=True))
    op.add_column('instituicoes', sa.Column('username', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'instituicoes', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'instituicoes', type_='unique')
    op.drop_column('instituicoes', 'username')
    op.drop_column('instituicoes', 'password')
    # ### end Alembic commands ###
