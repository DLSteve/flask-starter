"""Added application settings.

Revision ID: e68659f4dfe8
Revises: fa5526bcf2a9
Create Date: 2017-11-30 07:31:19.613023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e68659f4dfe8'
down_revision = 'fa5526bcf2a9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('app_settings',
                    sa.Column('id', sa.Unicode(length=256), nullable=False),
                    sa.Column('value', sa.Unicode(length=256), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('app_settings')

