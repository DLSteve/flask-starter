"""Added roles and permissions

Revision ID: fa5526bcf2a9
Revises: 0241a490f122
Create Date: 2017-11-29 07:40:29.227395

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fa5526bcf2a9'
down_revision = '0241a490f122'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('permission',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.Unicode(length=64), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_permission_name'), 'permission', ['name'], unique=True)
    op.create_table('role',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.Unicode(length=64), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_role_name'), 'role', ['name'], unique=True)
    op.create_table('role_permission_mapper',
                    sa.Column('permission_id', sa.Integer(), nullable=True),
                    sa.Column('role_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['permission_id'], ['permission.id']),
                    sa.ForeignKeyConstraint(['role_id'], ['role.id'])
                    )
    op.create_table('user_role_mapper',
                    sa.Column('role_id', sa.Integer(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['role_id'], ['role.id']),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'])
                    )


def downgrade():
    op.drop_table('user_role_mapper')
    op.drop_table('role_permission_mapper')
    op.drop_index(op.f('ix_role_name'), table_name='role')
    op.drop_table('role')
    op.drop_index(op.f('ix_permission_name'), table_name='permission')
    op.drop_table('permission')
