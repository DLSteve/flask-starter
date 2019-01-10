"""init

Revision ID: 10a08adb17d5
Revises: 
Create Date: 2017-10-18 11:05:26.930793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10a08adb17d5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Unicode(length=64), nullable=True),
    sa.Column('first_name', sa.Unicode(length=64), nullable=True),
    sa.Column('last_name', sa.Unicode(length=64), nullable=True),
    sa.Column('user_id', sa.Unicode(length=64), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_last_name'), 'users', ['last_name'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('warehouse_password_resets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('agent', sa.String(length=100), nullable=True),
    sa.Column('acct', sa.String(length=100), nullable=True),
    sa.Column('acct_location', sa.String(length=100), nullable=True),
    sa.Column('reset_date', sa.Date(), nullable=True),
    sa.Column('reset_day', sa.String(length=100), nullable=True),
    sa.Column('reset_type', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('warehouse_password_resets')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_last_name'), table_name='users')
    op.drop_index(op.f('ix_users_first_name'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###