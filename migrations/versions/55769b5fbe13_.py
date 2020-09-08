"""empty message

Revision ID: 55769b5fbe13
Revises: c52c37a8398c
Create Date: 2020-09-07 19:45:55.195400

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '55769b5fbe13'
down_revision = 'c52c37a8398c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('filekey', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('filename', sa.String(length=32), nullable=True),
    sa.Column('ext', sa.String(length=128), nullable=True),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('permissions', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ),
    sa.PrimaryKeyConstraint('filekey'),
    sa.UniqueConstraint('filekey')
    )
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_table('images')
    # ### end Alembic commands ###
