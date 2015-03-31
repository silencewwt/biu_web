"""empty message

Revision ID: 2c2b25add54d
Revises: 3569be055f4d
Create Date: 2015-03-23 21:25:26.921600

"""

# revision identifiers, used by Alembic.
revision = '2c2b25add54d'
down_revision = '3569be055f4d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('privileges',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('username', sa.String(length=12), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('salt', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('privileges')
    ### end Alembic commands ###