"""empty message

Revision ID: 3cd78300dede
Revises: 2f311bfa412c
Create Date: 2014-12-07 15:13:31.205707

"""

# revision identifiers, used by Alembic.
revision = '3cd78300dede'
down_revision = '2f311bfa412c'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_shares',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unified_user_id', sa.Integer(), nullable=False),
    sa.Column('post_comment_id', sa.Integer(), nullable=False),
    sa.Column('society_id', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('societies',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('society', sa.Unicode(length=8), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'third_party_users', sa.Column('society_id', sa.SmallInteger(), nullable=False))
    op.add_column(u'third_party_users', sa.Column('society_user_id', sa.CHAR(length=32), nullable=False))
    op.drop_column(u'third_party_users', 'source')
    op.drop_column(u'third_party_users', 'source_user_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'third_party_users', sa.Column('source_user_id', mysql.CHAR(length=32), nullable=False))
    op.add_column(u'third_party_users', sa.Column('source', mysql.SMALLINT(display_width=6), autoincrement=False, nullable=False))
    op.drop_column(u'third_party_users', 'society_user_id')
    op.drop_column(u'third_party_users', 'society_id')
    op.drop_table('societies')
    op.drop_table('post_shares')
    ### end Alembic commands ###