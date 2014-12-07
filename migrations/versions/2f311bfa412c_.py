"""empty message

Revision ID: 2f311bfa412c
Revises: 3b6c523c1b43
Create Date: 2014-12-07 12:10:14.861530

"""

# revision identifiers, used by Alembic.
revision = '2f311bfa412c'
down_revision = '3b6c523c1b43'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('third_party_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('source_user_id', sa.CHAR(length=32), nullable=False),
    sa.Column('created', sa.Integer(), nullable=False),
    sa.Column('source', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('third_party_users')
    ### end Alembic commands ###